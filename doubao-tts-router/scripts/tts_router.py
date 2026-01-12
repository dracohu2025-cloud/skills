#!/usr/bin/env python3
"""
豆包 TTS API Router - 支持火山引擎 v3 API

统一的火山引擎豆包语音合成 API 调用脚本。
支持流式/非流式合成、多种音色、语速/音调调节、长文本异步合成。

API 文档：https://www.volcengine.com/docs/6561/1598757

Usage:
    python tts_router.py --text "你好" --output hello.mp3
    python tts_router.py --text "测试" --voice "zh_male_dayi_saturn_bigtts" --output test.mp3
    python tts_router.py --file input.txt --async-mode --output output.mp3
"""

import argparse
import base64
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: requests library not installed. Run: pip install requests")
    sys.exit(1)


# ============== 配置 ==============

# v3 API 端点
TTS_API_V3_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
TTS_ASYNC_API_V3_URL = "https://openspeech.bytedance.com/api/v3/tts/async"
TTS_QUERY_API_V3_URL = "https://openspeech.bytedance.com/api/v3/tts/async/query"

# 默认音色（使用 saturn 系列稳定音色）
DEFAULT_VOICE = "zh_female_mizai_saturn_bigtts"

# v1 API 端点（兼容保留）
TTS_API_V1_URL = "https://openspeech.bytedance.com/api/v1/tts"
TTS_ASYNC_API_V1_URL = "https://openspeech.bytedance.com/api/v1/tts/async"
TTS_QUERY_API_V1_URL = "https://openspeech.bytedance.com/api/v1/tts/async/query"


# ============== 工具函数 ==============

def get_credentials() -> tuple[str, str, str]:
    """获取 API 凭证（兼容多种环境变量命名）"""
    # 支持多种环境变量命名格式
    appid = (
        os.environ.get("DOUBAO_TTS_APPID") or
        os.environ.get("VOLCENGINE_TTS_APP_ID")
    )
    token = (
        os.environ.get("DOUBAO_TTS_ACCESS_TOKEN") or
        os.environ.get("VOLCENGINE_TTS_ACCESS_TOKEN")
    )
    # v3 API 需要 resource_id
    resource_id = (
        os.environ.get("DOUBAO_TTS_RESOURCE_ID") or
        os.environ.get("VOLCENGINE_TTS_2_RESOURCE_ID") or
        "seed-tts-2.0"  # 默认值
    )

    if not appid or not token:
        print("Error: 请设置环境变量")
        print()
        print("支持的环境变量格式:")
        print('  方式1: DOUBAO_TTS_APPID + DOUBAO_TTS_ACCESS_TOKEN')
        print('  方式2: VOLCENGINE_TTS_APP_ID + VOLCENGINE_TTS_ACCESS_TOKEN')
        print()
        print("凭证获取: https://console.volcengine.com/")
        sys.exit(1)

    return appid, token, resource_id


def speed_ratio_to_speech_rate(speed_ratio: float) -> int:
    """
    将语速比例转换为 v3 API 的 speech_rate 参数

    v3 API: speech_rate 范围 -50 到 100
    - 0 = 正常语速 (1.0x)
    - 100 = 2倍语速 (2.0x)
    - -50 = 0.5倍语速 (0.5x)

    Args:
        speed_ratio: 语速比例 (0.5 - 2.0)

    Returns:
        speech_rate 值 (-50 - 100)
    """
    # 1.0 -> 0, 2.0 -> 100, 0.5 -> -50
    return int((speed_ratio - 1.0) * 100)


# ============== TTS API 调用 ==============

class DoubaoTTSRouter:
    """豆包 TTS API Router - 支持 v1 和 v3 API"""

    def __init__(self, api_version: str = "v3"):
        """
        初始化 Router

        Args:
            api_version: API 版本，"v3" (推荐) 或 "v1" (兼容)
        """
        self.appid, self.token, self.resource_id = get_credentials()
        self.api_version = api_version

        if api_version == "v3":
            self.tts_url = TTS_API_V3_URL
            self.async_url = TTS_ASYNC_API_V3_URL
            self.query_url = TTS_QUERY_API_V3_URL
            # v3 使用不同的请求头
            self.headers = {
                "Content-Type": "application/json",
                "X-Api-App-Id": self.appid,
                "X-Api-Access-Key": self.token,
                "X-Api-Resource-Id": self.resource_id
            }
        else:
            self.tts_url = TTS_API_V1_URL
            self.async_url = TTS_ASYNC_API_V1_URL
            self.query_url = TTS_QUERY_API_V1_URL
            # v1 使用 Bearer 认证
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer;{self.token}"
            }

    def synthesize(
        self,
        text: str,
        voice_type: str = DEFAULT_VOICE,
        encoding: str = "mp3",
        speed_ratio: float = 1.0,
        pitch_ratio: float = 1.0,
        sample_rate: int = 24000,
    ) -> bytes:
        """
        同步语音合成

        Args:
            text: 要合成的文本
            voice_type: 音色类型
            encoding: 输出格式 (mp3/pcm/wav/ogg_opus)
            speed_ratio: 语速 (0.5-2.0)
            pitch_ratio: 音调预留参数
            sample_rate: 采样率 (8000/16000/22050/24000/32000/44100/48000)

        Returns:
            音频数据 (bytes)
        """
        if self.api_version == "v3":
            return self._synthesize_v3(text, voice_type, encoding, speed_ratio, sample_rate)
        else:
            return self._synthesize_v1(text, voice_type, encoding, speed_ratio, pitch_ratio, sample_rate)

    def _synthesize_v3(
        self,
        text: str,
        voice_type: str,
        encoding: str,
        speed_ratio: float,
        sample_rate: int,
    ) -> bytes:
        """v3 API 同步合成（流式多行 JSON 响应）"""
        payload = {
            "user": {
                "uid": "claude_code_user"
            },
            "req_params": {
                "text": text,
                "speaker": voice_type,
                "audio_params": {
                    "format": encoding,
                    "sample_rate": sample_rate,
                    "speech_rate": speed_ratio_to_speech_rate(speed_ratio),
                }
            }
        }

        if model := os.environ.get("DOUBAO_TTS_MODEL"):
            payload["req_params"]["model"] = model

        response = requests.post(
            self.tts_url,
            json=payload,
            headers=self.headers,
            timeout=30,
            stream=True  # 启用流式响应
        )

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        # v3 API 返回流式多行 JSON，需要逐行解析
        audio_chunks = []

        for line in response.iter_lines(decode_unicode=True):
            if not line.strip():
                continue

            try:
                result = json.loads(line)
                code = result.get("code")

                # 结束标记：code=20000000 表示成功完成
                if code == 20000000:
                    break

                # 错误处理
                if code != 0:
                    raise Exception(f"TTS Error [{code}]: {result.get('message', 'Unknown error')}")

                # 收集音频数据
                audio_data = result.get("data", "")
                if audio_data:
                    audio_chunks.append(base64.b64decode(audio_data))

            except json.JSONDecodeError as e:
                # 忽略无法解析的行
                continue

        if not audio_chunks:
            raise Exception("No audio data in response")

        # 拼接所有音频块
        return b"".join(audio_chunks)

    def _synthesize_v1(
        self,
        text: str,
        voice_type: str,
        encoding: str,
        speed_ratio: float,
        pitch_ratio: float,
        sample_rate: int,
    ) -> bytes:
        """v1 API 同步合成（兼容）"""
        payload = {
            "app": {
                "appid": self.appid,
                "token": self.token,
                "cluster": "volcano_tts"
            },
            "user": {
                "uid": "claude_code_user"
            },
            "audio": {
                "voice_type": voice_type,
                "encoding": encoding,
                "speed_ratio": speed_ratio,
                "pitch_ratio": pitch_ratio,
                "sample_rate": sample_rate
            },
            "request": {
                "reqid": str(uuid.uuid4()),
                "text": text,
                "operation": "query"
            }
        }

        response = requests.post(
            self.tts_url,
            json=payload,
            headers=self.headers,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        result = response.json()

        # v1 API: code=3000 或 0 表示成功
        code = result.get("code")
        if code not in (0, 3000):
            raise Exception(f"TTS Error [{code}]: {result.get('message', 'Unknown error')}")

        audio_data = result.get("data", "")
        if audio_data:
            return base64.b64decode(audio_data)

        raise Exception("No audio data in response")

    def synthesize_async(
        self,
        text: str,
        voice_type: str = DEFAULT_VOICE,
        encoding: str = "mp3",
        speed_ratio: float = 1.0,
    ) -> str:
        """
        异步语音合成（用于长文本）

        Args:
            text: 要合成的文本（支持最多 10 万字）
            voice_type: 音色类型
            encoding: 输出格式
            speed_ratio: 语速

        Returns:
            任务 ID
        """
        if self.api_version == "v3":
            return self._synthesize_async_v3(text, voice_type, encoding, speed_ratio)
        else:
            return self._synthesize_async_v1(text, voice_type, encoding, speed_ratio)

    def _synthesize_async_v3(
        self,
        text: str,
        voice_type: str,
        encoding: str,
        speed_ratio: float,
    ) -> str:
        """v3 API 异步合成"""
        payload = {
            "user": {
                "uid": "claude_code_user"
            },
            "req_params": {
                "text": text,
                "speaker": voice_type,
                "audio_params": {
                    "format": encoding,
                    "speech_rate": speed_ratio_to_speech_rate(speed_ratio),
                }
            }
        }

        response = requests.post(
            self.async_url,
            json=payload,
            headers=self.headers,
            timeout=60
        )

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        result = response.json()

        code = result.get("code")
        if code != 0:
            raise Exception(f"TTS Error [{code}]: {result.get('message', 'Unknown error')}")

        return result.get("task_id", "")

    def _synthesize_async_v1(
        self,
        text: str,
        voice_type: str,
        encoding: str,
        speed_ratio: float,
    ) -> str:
        """v1 API 异步合成（兼容）"""
        payload = {
            "app": {
                "appid": self.appid,
                "token": self.token,
                "cluster": "volcano_tts"
            },
            "user": {
                "uid": "claude_code_user"
            },
            "audio": {
                "voice_type": voice_type,
                "encoding": encoding,
                "speed_ratio": speed_ratio,
            },
            "request": {
                "reqid": str(uuid.uuid4()),
                "text": text,
                "operation": "submit"
            }
        }

        response = requests.post(
            self.async_url,
            json=payload,
            headers=self.headers,
            timeout=60
        )

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        result = response.json()

        code = result.get("code")
        if code not in (0, 3000):
            raise Exception(f"TTS Error [{code}]: {result.get('message', 'Unknown error')}")

        return result.get("task_id", "")

    def query_async_result(self, task_id: str) -> Optional[str]:
        """
        查询异步合成结果

        Args:
            task_id: 任务 ID

        Returns:
            音频下载 URL，如果任务未完成返回 None
        """
        payload = {
            "user": {"uid": "claude_code_user"},
            "task_id": task_id
        }

        response = requests.post(
            self.query_url,
            json=payload,
            headers=self.headers,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        result = response.json()

        code = result.get("code")
        if code != 0:
            raise Exception(f"Query Error [{code}]: {result.get('message', 'Unknown error')}")

        status = result.get("status")
        if status == "done":
            return result.get("audio_url")
        elif status == "failed":
            raise Exception(f"Synthesis failed: {result.get('message')}")

        return None  # 仍在处理中

    def download_audio(self, url: str) -> bytes:
        """下载音频文件"""
        response = requests.get(url, timeout=120)
        if response.status_code != 200:
            raise Exception(f"Download failed: {response.status_code}")
        return response.content


# ============== CLI ==============

def main():
    parser = argparse.ArgumentParser(
        description="豆包 TTS API Router - 火山引擎语音合成 (v3 API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --text "你好世界" --output hello.mp3
  %(prog)s --text "测试" --voice zh_male_dayi_saturn_bigtts -o test.mp3
  %(prog)s --file article.txt --async-mode --output article.mp3
  %(prog)s --text "快速语音" --speed 1.5 -o fast.mp3
  %(prog)s --text "慢速语音" --speed 0.7 -o slow.mp3

环境变量:
  VOLCENGINE_TTS_APP_ID         火山引擎 App ID
  VOLCENGINE_TTS_ACCESS_TOKEN  火山引擎 Access Token

语速说明:
  --speed 1.0  正常语速 (默认)
  --speed 2.0  2倍语速
  --speed 0.5  0.5倍语速
        """
    )

    # 输入源
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--text", "-t", help="要合成的文本")
    input_group.add_argument("--file", "-f", help="从文件读取文本")

    # 输出
    parser.add_argument("--output", "-o", required=True, help="输出音频文件路径")

    # 音频参数
    parser.add_argument("--voice", "-v", default=DEFAULT_VOICE, help=f"音色类型 (默认: {DEFAULT_VOICE})")
    parser.add_argument("--encoding", "-e", default="mp3", choices=["mp3", "pcm", "wav", "ogg_opus"], help="输出格式 (默认: mp3)")
    parser.add_argument("--speed", "-s", type=float, default=1.0, help="语速 0.5-2.0 (默认: 1.0)")
    parser.add_argument("--sample-rate", type=int, default=24000, choices=[8000, 16000, 22050, 24000, 32000, 44100, 48000], help="采样率 (默认: 24000)")

    # API 版本
    parser.add_argument("--api-version", default="v3", choices=["v1", "v3"], help="API 版本 (默认: v3)")

    # 模式
    parser.add_argument("--async-mode", action="store_true", help="使用异步模式（适合长文本）")

    # 调试
    parser.add_argument("--verbose", action="store_true", help="显示详细输出")

    args = parser.parse_args()

    # 获取文本
    if args.text:
        text = args.text
    else:
        text_path = Path(args.file)
        if not text_path.exists():
            print(f"Error: 文件不存在: {args.file}")
            sys.exit(1)
        text = text_path.read_text(encoding="utf-8")

    if args.verbose:
        print(f"API Version: {args.api_version}")
        print(f"Text length: {len(text)} chars")
        print(f"Voice: {args.voice}")
        print(f"Speed: {args.speed}x")
        print(f"Output: {args.output}")

    # 初始化 Router
    router = DoubaoTTSRouter(api_version=args.api_version)

    try:
        if args.async_mode:
            # 异步模式
            print("Submitting async synthesis task...")
            task_id = router.synthesize_async(
                text=text,
                voice_type=args.voice,
                encoding=args.encoding,
                speed_ratio=args.speed
            )
            print(f"Task ID: {task_id}")

            # 轮询结果
            import time
            print("Waiting for synthesis to complete...")
            for i in range(120):  # 最多等待 10 分钟
                audio_url = router.query_async_result(task_id)
                if audio_url:
                    print("Downloading audio...")
                    audio_data = router.download_audio(audio_url)
                    break
                print(f"  Checking... ({i*5}s)")
                time.sleep(5)
            else:
                print("Error: Synthesis timeout")
                sys.exit(1)
        else:
            # 同步模式
            print("Synthesizing...")
            audio_data = router.synthesize(
                text=text,
                voice_type=args.voice,
                encoding=args.encoding,
                speed_ratio=args.speed,
                sample_rate=args.sample_rate
            )

        # 保存音频
        output_path = Path(args.output)
        output_path.write_bytes(audio_data)
        print(f"Saved: {output_path} ({len(audio_data)} bytes)")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
