#!/usr/bin/env python3
"""
即梦 SeeDream 4.5 文生图 API Router

火山引擎即梦/豆包图像生成 API 统一调用脚本。
支持文生图、图生图、多图融合等功能。

API 文档：https://www.volcengine.com/docs/82379/1535980

Usage:
    python image_router.py --prompt "一只可爱的橘猫" --output cat.png
    python image_router.py --prompt "赛博朋克城市" --size 1024x576 --output city.png
    python image_router.py --prompt "水彩风格" --image ref.jpg --output result.png
"""

import argparse
import base64
import json
import os
import sys
import uuid
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, List


# ============== 配置 ==============

# API 端点
ARK_API_BASE = "https://ark.cn-beijing.volces.com/api/v3"
IMAGES_GENERATIONS_URL = f"{ARK_API_BASE}/images/generations"

# 默认模型
DEFAULT_MODEL = "doubao-seedream-4-5-251128"

# 支持的尺寸 (SeeDream 4.5 需要至少 3686400 像素)
SUPPORTED_SIZES = [
    "1920x1920",  # 1:1 方形
    "2560x1440",  # 16:9 横版
    "1440x2560",  # 9:16 竖版
    "2048x1536",  # 4:3 横版
    "1536x2048",  # 3:4 竖版
    "2048x2048",  # 1:1 高清方形
    "1920x1080",  # 16:9 标准横版
    "1080x1920",  # 9:16 标准竖版
]


# ============== 工具函数 ==============

def get_api_key() -> str:
    """获取 API Key（兼容多种环境变量命名）"""
    api_key = (
        os.environ.get("SEEDREAM_API_KEY") or
        os.environ.get("ARK_API_KEY") or
        os.environ.get("VOLCENGINE_API_KEY")
    )

    if not api_key:
        print("Error: 请设置环境变量")
        print()
        print("支持的环境变量格式:")
        print('  SEEDREAM_API_KEY')
        print('  ARK_API_KEY')
        print('  VOLCENGINE_API_KEY')
        print()
        print("获取 API Key: https://console.volcengine.com/ark")
        sys.exit(1)

    return api_key


def get_model_name() -> str:
    """获取模型名称"""
    return os.environ.get("JIMENG_MODEL_NAME") or DEFAULT_MODEL


def image_to_base64(image_path: str) -> str:
    """将图片文件转换为 base64"""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"图片文件不存在: {image_path}")

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def download_image(url: str, output_path: str) -> None:
    """下载图片到本地"""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "JimengImageRouter/1.0")

    with urllib.request.urlopen(req, timeout=120) as response:
        with open(output_path, "wb") as f:
            f.write(response.read())


def save_base64_image(b64_data: str, output_path: str) -> None:
    """保存 base64 图片到本地"""
    image_data = base64.b64decode(b64_data)
    with open(output_path, "wb") as f:
        f.write(image_data)


# ============== API 调用 ==============

class JimengImageRouter:
    """即梦 SeeDream 图像生成 API Router"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        初始化 Router

        Args:
            api_key: API Key，不提供则从环境变量读取
            model: 模型名称，不提供则使用默认值
        """
        self.api_key = api_key or get_api_key()
        self.model = model or get_model_name()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def generate(
        self,
        prompt: str,
        n: int = 1,
        size: str = "1024x1024",
        response_format: str = "url",
        reference_image: Optional[str] = None,
    ) -> dict:
        """
        生成图片

        Args:
            prompt: 图片描述文本
            n: 生成图片数量 (1-4)
            size: 图片尺寸
            response_format: 返回格式 (url 或 b64_json)
            reference_image: 参考图片路径（用于图生图）

        Returns:
            API 响应结果
        """
        if size not in SUPPORTED_SIZES:
            print(f"Warning: 不支持的尺寸 {size}，使用默认尺寸 1920x1920")
            size = "1920x1920"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "n": min(max(n, 1), 4),  # 限制 1-4
            "size": size,
            "response_format": response_format,
        }

        # 如果有参考图片，添加到请求中
        if reference_image:
            image_b64 = image_to_base64(reference_image)
            # 根据 API 要求构建 image 参数
            payload["image"] = f"data:image/png;base64,{image_b64}"

        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            IMAGES_GENERATIONS_URL,
            data=data,
            headers=self.headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            raise Exception(f"API Error [{e.code}]: {error_body}")
        except urllib.error.URLError as e:
            raise Exception(f"Network Error: {e.reason}")

    def generate_and_save(
        self,
        prompt: str,
        output: str,
        n: int = 1,
        size: str = "1024x1024",
        reference_image: Optional[str] = None,
    ) -> List[str]:
        """
        生成图片并保存到本地

        Args:
            prompt: 图片描述文本
            output: 输出路径（多张图片时自动添加序号）
            n: 生成图片数量
            size: 图片尺寸
            reference_image: 参考图片路径

        Returns:
            保存的文件路径列表
        """
        # 如果需要多张图片，使用 b64_json 可能更快
        response_format = "url"

        result = self.generate(
            prompt=prompt,
            n=n,
            size=size,
            response_format=response_format,
            reference_image=reference_image,
        )

        saved_files = []
        output_path = Path(output)

        for i, image_data in enumerate(result.get("data", [])):
            # 构建输出文件名
            if n > 1:
                file_path = output_path.parent / f"{output_path.stem}_{i+1}{output_path.suffix}"
            else:
                file_path = output_path

            # 保存图片
            if response_format == "url":
                url = image_data.get("url")
                if url:
                    download_image(url, str(file_path))
                    saved_files.append(str(file_path))
            else:
                b64 = image_data.get("b64_json")
                if b64:
                    save_base64_image(b64, str(file_path))
                    saved_files.append(str(file_path))

        return saved_files


# ============== CLI ==============

def main():
    parser = argparse.ArgumentParser(
        description="即梦 SeeDream 4.5 文生图 API Router",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --prompt "一只可爱的橘猫在阳光下睡觉" --output cat.png
  %(prog)s --prompt "赛博朋克城市夜景" --size 2560x1440 -o city.png
  %(prog)s --prompt "未来科技感汽车" --n 4 -o cars.png
  %(prog)s --prompt "水彩风格" --image photo.jpg -o watercolor.png

环境变量:
  SEEDREAM_API_KEY    火山引擎方舟 API Key
  JIMENG_MODEL_NAME   模型名称（默认: doubao-seedream-4-5-251128）

支持的尺寸 (SeeDream 4.5 需要至少 3686400 像素):
  1920x1920  方形 (1:1, 默认)
  2048x2048  高清方形 (1:1)
  2560x1440  横版 (16:9)
  1920x1080  标准横版 (16:9)
  1440x2560  竖版 (9:16)
  1080x1920  标准竖版 (9:16)
  2048x1536  横版 (4:3)
  1536x2048  竖版 (3:4)
        """
    )

    # 必填参数
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="图片描述文本"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="输出文件路径"
    )

    # 可选参数
    parser.add_argument(
        "--size", "-s",
        default="1920x1920",
        choices=SUPPORTED_SIZES,
        help="图片尺寸 (默认: 1920x1920)"
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        help="生成图片数量 1-4 (默认: 1)"
    )
    parser.add_argument(
        "--image", "-i",
        help="参考图片路径（用于图生图）"
    )
    parser.add_argument(
        "--model", "-m",
        help="模型名称（默认从环境变量读取）"
    )

    # 调试
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细输出"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON 格式结果（不保存文件）"
    )

    args = parser.parse_args()

    if args.verbose:
        print(f"Model: {args.model or get_model_name()}")
        print(f"Prompt: {args.prompt}")
        print(f"Size: {args.size}")
        print(f"Count: {args.n}")
        if args.image:
            print(f"Reference: {args.image}")
        print(f"Output: {args.output}")
        print()

    # 初始化 Router
    router = JimengImageRouter(model=args.model)

    try:
        if args.json:
            # 只输出 JSON，不保存文件
            result = router.generate(
                prompt=args.prompt,
                n=args.n,
                size=args.size,
                reference_image=args.image,
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # 生成并保存
            print("Generating...")
            saved_files = router.generate_and_save(
                prompt=args.prompt,
                output=args.output,
                n=args.n,
                size=args.size,
                reference_image=args.image,
            )

            for f in saved_files:
                file_size = Path(f).stat().st_size
                print(f"Saved: {f} ({file_size:,} bytes)")

            print(f"\n✓ Generated {len(saved_files)} image(s)")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
