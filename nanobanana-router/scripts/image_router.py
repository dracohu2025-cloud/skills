#!/usr/bin/env python3
"""
Nano Banana Pro Image Router (OpenRouter)

通过 OpenRouter 调用 Gemini 3 Pro Image Generation API。
支持文生图、图生图、多图融合、2K/4K 高清输出等功能。
自动返回费用信息和详细的 usage metadata。

Usage:
    python image_router.py --prompt "一只可爱的橘猫" --output cat.png
    python image_router.py --prompt "赛博朋克城市" --aspect 16:9 --size 4K --output city.png
    python image_router.py --prompt "水彩风格" --image ref.jpg --output result.png
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, List


# ============== 配置 ==============

# OpenRouter API 端点
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
CHAT_COMPLETIONS_URL = f"{OPENROUTER_API_BASE}/chat/completions"

# 模型名称 (OpenRouter 格式)
DEFAULT_MODEL = "google/gemini-3-pro-image-preview"  # Nano Banana Pro
FLASH_MODEL = "google/gemini-2.5-flash-preview-image"  # Nano Banana (更快)

# 支持的宽高比
SUPPORTED_ASPECTS = [
    "1:1",   # 方形
    "2:3",   # 竖版
    "3:2",   # 横版
    "3:4",   # 竖版
    "4:3",   # 横版
    "4:5",   # 竖版
    "5:4",   # 横版
    "9:16",  # 手机竖屏
    "16:9",  # 宽屏
    "21:9",  # 超宽屏
]

# 支持的图片尺寸
SUPPORTED_SIZES = ["1K", "2K", "4K"]


# ============== 工具函数 ==============

def get_api_key() -> str:
    """获取 OpenRouter API Key"""
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        print("Error: 请设置环境变量 OPENROUTER_API_KEY")
        print()
        print("获取 API Key: https://openrouter.ai/keys")
        sys.exit(1)

    return api_key


def image_to_base64(image_path: str) -> tuple[str, str]:
    """
    将图片文件转换为 base64

    Returns:
        (base64_data, mime_type)
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"图片文件不存在: {image_path}")

    # 确定 MIME 类型
    suffix = path.suffix.lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    mime_type = mime_types.get(suffix, "image/png")

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8"), mime_type


def save_base64_image(b64_data: str, output_path: str) -> None:
    """保存 base64 图片到本地"""
    image_data = base64.b64decode(b64_data)
    with open(output_path, "wb") as f:
        f.write(image_data)


def extract_images_from_response(response: dict) -> List[dict]:
    """从 OpenRouter API 响应中提取图片数据"""
    images = []

    choices = response.get("choices", [])
    for choice in choices:
        message = choice.get("message", {})

        # 方式1: 检查 message.images 数组 (OpenRouter 推荐格式)
        message_images = message.get("images", [])
        for img in message_images:
            if isinstance(img, str):
                # 直接是 base64 字符串
                if img.startswith("data:"):
                    try:
                        header, data = img.split(",", 1)
                        mime_type = header.split(":")[1].split(";")[0]
                        images.append({
                            "data": data,
                            "mime_type": mime_type
                        })
                    except (ValueError, IndexError):
                        pass
                else:
                    # 假设是纯 base64 数据
                    images.append({
                        "data": img,
                        "mime_type": "image/png"
                    })
            elif isinstance(img, dict):
                # 检查 {type: "image_url", image_url: {url: "data:..."}} 格式
                if img.get("type") == "image_url":
                    image_url = img.get("image_url", {})
                    url = image_url.get("url", "") if isinstance(image_url, dict) else ""
                    if url.startswith("data:"):
                        try:
                            header, data = url.split(",", 1)
                            mime_type = header.split(":")[1].split(";")[0]
                            images.append({
                                "data": data,
                                "mime_type": mime_type
                            })
                        except (ValueError, IndexError):
                            pass
                # 检查 {data: ..., mime_type: ...} 格式
                elif "data" in img:
                    images.append({
                        "data": img.get("data", ""),
                        "mime_type": img.get("mime_type", "image/png")
                    })
                # 检查 {url: "data:..."} 格式
                elif "url" in img:
                    url = img["url"]
                    if url.startswith("data:"):
                        try:
                            header, data = url.split(",", 1)
                            mime_type = header.split(":")[1].split(";")[0]
                            images.append({
                                "data": data,
                                "mime_type": mime_type
                            })
                        except (ValueError, IndexError):
                            pass

        # 方式2: 检查 content 数组格式 (备用)
        content = message.get("content", [])

        # content 可能是字符串或数组
        if isinstance(content, str):
            continue

        for part in content:
            if isinstance(part, dict):
                # 检查 inline_data 格式
                if "inline_data" in part:
                    inline_data = part["inline_data"]
                    images.append({
                        "data": inline_data.get("data", ""),
                        "mime_type": inline_data.get("mime_type", "image/png")
                    })
                # 检查 image_url 格式
                elif part.get("type") == "image_url":
                    image_url = part.get("image_url", {})
                    url = image_url.get("url", "")
                    if url.startswith("data:"):
                        try:
                            header, data = url.split(",", 1)
                            mime_type = header.split(":")[1].split(";")[0]
                            images.append({
                                "data": data,
                                "mime_type": mime_type
                            })
                        except (ValueError, IndexError):
                            pass

    return images


def format_cost(usage: dict) -> str:
    """格式化费用信息"""
    if not usage:
        return "N/A"

    total_cost = usage.get("total_cost", 0)
    if total_cost:
        return f"${total_cost:.6f}"

    # 如果没有 total_cost，尝试从 native_tokens_cost 计算
    native = usage.get("native_tokens_cost", {})
    if native:
        input_cost = native.get("input", 0)
        output_cost = native.get("output", 0)
        return f"${input_cost + output_cost:.6f}"

    return "N/A"


# ============== API 调用 ==============

class NanoBananaRouter:
    """Nano Banana Pro 图像生成 API Router (via OpenRouter)"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        初始化 Router

        Args:
            api_key: OpenRouter API Key，不提供则从环境变量读取
            model: 模型名称，不提供则使用 Nano Banana Pro
        """
        self.api_key = api_key or get_api_key()
        self.model = model or DEFAULT_MODEL
        self.last_usage = None
        self.last_cost = None

    def generate(
        self,
        prompt: str,
        aspect_ratio: str = "1:1",
        image_size: str = "1K",
        reference_images: Optional[List[str]] = None,
    ) -> dict:
        """
        生成图片

        Args:
            prompt: 图片描述文本
            aspect_ratio: 宽高比 (1:1, 16:9, 9:16 等)
            image_size: 图片尺寸 (1K, 2K, 4K)
            reference_images: 参考图片路径列表（用于图生图）

        Returns:
            API 响应结果
        """
        # 验证参数
        if aspect_ratio not in SUPPORTED_ASPECTS:
            print(f"Warning: 不支持的宽高比 {aspect_ratio}，使用默认 1:1")
            aspect_ratio = "1:1"

        if image_size not in SUPPORTED_SIZES:
            print(f"Warning: 不支持的尺寸 {image_size}，使用默认 1K")
            image_size = "1K"

        # 构建 message content
        content = []

        # 添加参考图片
        if reference_images:
            for img_path in reference_images:
                b64_data, mime_type = image_to_base64(img_path)
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{b64_data}"
                    }
                })

        # 添加文本提示，包含图像生成指令和参数
        image_prompt = f"""Generate an image based on the following description.

Aspect Ratio: {aspect_ratio}
Image Size: {image_size}

Description: {prompt}

Please generate a high-quality image matching this description."""

        content.append({
            "type": "text",
            "text": image_prompt
        })

        # 构建请求体 (OpenRouter/OpenAI 格式)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],
            "max_tokens": 4096,
            # 关键：必须指定 modalities 才能生成图片
            "modalities": ["image", "text"],
        }

        # 发送请求
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/anthropics/claude-code",
            "X-Title": "Nano Banana Pro Router"
        }

        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            CHAT_COMPLETIONS_URL,
            data=data,
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                result = json.loads(response.read().decode("utf-8"))

                # 保存 usage 信息
                self.last_usage = result.get("usage", {})
                self.last_cost = format_cost(self.last_usage)

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
        aspect_ratio: str = "1:1",
        image_size: str = "1K",
        reference_images: Optional[List[str]] = None,
    ) -> List[str]:
        """
        生成图片并保存到本地

        Args:
            prompt: 图片描述文本
            output: 输出路径
            aspect_ratio: 宽高比
            image_size: 图片尺寸
            reference_images: 参考图片路径列表

        Returns:
            保存的文件路径列表
        """
        result = self.generate(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            image_size=image_size,
            reference_images=reference_images,
        )

        # 提取并保存图片
        images = extract_images_from_response(result)
        saved_files = []
        output_path = Path(output)

        for i, img_data in enumerate(images):
            # 构建输出文件名
            if len(images) > 1:
                file_path = output_path.parent / f"{output_path.stem}_{i+1}{output_path.suffix}"
            else:
                file_path = output_path

            # 保存图片
            save_base64_image(img_data["data"], str(file_path))
            saved_files.append(str(file_path))

        return saved_files

    def get_usage_info(self) -> dict:
        """获取上次请求的 usage 信息"""
        return {
            "usage": self.last_usage,
            "cost": self.last_cost
        }


# ============== CLI ==============

def main():
    parser = argparse.ArgumentParser(
        description="Nano Banana Pro 图像生成 API Router (via OpenRouter)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --prompt "一只可爱的橘猫在阳光下睡觉" --output cat.png
  %(prog)s --prompt "赛博朋克城市夜景" --aspect 16:9 --size 4K -o city.png
  %(prog)s --prompt "水彩风格" --image photo.jpg -o watercolor.png
  %(prog)s --prompt "融合这两张图" --image img1.jpg --image img2.jpg -o merged.png

环境变量:
  OPENROUTER_API_KEY    OpenRouter API Key (必填)

支持的宽高比:
  1:1   方形 (默认)
  2:3   竖版
  3:2   横版
  3:4   竖版
  4:3   横版
  4:5   竖版
  5:4   横版
  9:16  手机竖屏
  16:9  宽屏
  21:9  超宽屏

支持的尺寸:
  1K    默认分辨率
  2K    高清
  4K    超高清
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
        "--aspect", "-a",
        default="1:1",
        choices=SUPPORTED_ASPECTS,
        help="图片宽高比 (默认: 1:1)"
    )
    parser.add_argument(
        "--size", "-s",
        default="1K",
        choices=SUPPORTED_SIZES,
        help="图片尺寸 (默认: 1K)"
    )
    parser.add_argument(
        "--image", "-i",
        action="append",
        help="参考图片路径（可多次使用以添加多张参考图）"
    )
    parser.add_argument(
        "--model", "-m",
        choices=[DEFAULT_MODEL, FLASH_MODEL],
        help=f"模型名称（默认: {DEFAULT_MODEL}）"
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
    parser.add_argument(
        "--show-cost",
        action="store_true",
        help="显示费用信息"
    )

    args = parser.parse_args()

    if args.verbose:
        print(f"Model: {args.model or DEFAULT_MODEL}")
        print(f"Prompt: {args.prompt}")
        print(f"Aspect: {args.aspect}")
        print(f"Size: {args.size}")
        if args.image:
            print(f"Reference images: {args.image}")
        print(f"Output: {args.output}")
        print()

    # 初始化 Router
    router = NanoBananaRouter(model=args.model)

    try:
        if args.json:
            # 只输出 JSON，不保存文件
            result = router.generate(
                prompt=args.prompt,
                aspect_ratio=args.aspect,
                image_size=args.size,
                reference_images=args.image,
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # 生成并保存
            print("Generating with Nano Banana Pro (via OpenRouter)...")
            saved_files = router.generate_and_save(
                prompt=args.prompt,
                output=args.output,
                aspect_ratio=args.aspect,
                image_size=args.size,
                reference_images=args.image,
            )

            if saved_files:
                for f in saved_files:
                    file_size = Path(f).stat().st_size
                    print(f"Saved: {f} ({file_size:,} bytes)")
                print(f"\n✓ Generated {len(saved_files)} image(s)")
            else:
                print("Warning: No images were extracted from the response.")
                print("The model may have returned text instead of an image.")

            # 显示 usage 信息
            usage_info = router.get_usage_info()
            if args.verbose or args.show_cost:
                print(f"\n--- Usage Info ---")
                if usage_info["usage"]:
                    usage = usage_info["usage"]
                    print(f"Prompt Tokens: {usage.get('prompt_tokens', 'N/A')}")
                    print(f"Completion Tokens: {usage.get('completion_tokens', 'N/A')}")
                    print(f"Total Tokens: {usage.get('total_tokens', 'N/A')}")
                print(f"Cost: {usage_info['cost']}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
