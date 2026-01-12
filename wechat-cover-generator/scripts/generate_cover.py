#!/usr/bin/env python3
"""
微信公众号封面图生成器

基于 Nano Banana Pro (Gemini 3 Pro Image) 生成公众号封面图。

Usage:
    python generate_cover.py --title "文章标题" --style tech --output cover.png
    python generate_cover.py --title "Python入门" --style tutorial --output cover.png
    python generate_cover.py --prompt "自定义描述" --output cover.png
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Nano Banana Router 路径
ROUTER_SCRIPT = Path.home() / ".claude/skills/nanobanana-router/scripts/image_router.py"

# 预设风格模板
STYLE_TEMPLATES = {
    "tech": """A futuristic tech cover image for WeChat article.
Dark background with blue-purple gradient glow (blending purple #7C3AED and blue #4285F4).
Main visual: floating terminal windows, code snippets, AI chip elements.
{title_text}
Cyberpunk aesthetic, modern tech style. Professional, clean design.
High contrast, neon accents. No watermarks.""",

    "tutorial": """A clean tutorial cover for WeChat article.
Light gradient background from white to soft blue.
Central visual: educational icons, code editor mockup, clean typography.
{title_text}
Minimalist style, modern and professional. Educational feel.
Clear visual hierarchy. No watermarks.""",

    "tool": """A product showcase cover for WeChat article about developer tools.
Gradient background from dark purple to black.
Central visual: floating app icons and tool interfaces in 3D perspective.
{title_text}
Glossy, modern tech aesthetic. Premium feel. No watermarks.""",

    "opinion": """An artistic cover for WeChat opinion article.
Abstract gradient background with flowing shapes.
Conceptual visual elements suggesting thought and reflection.
{title_text}
Modern, artistic style. Thoughtful mood. No watermarks.""",

    "news": """A news-style cover for WeChat article.
Bold, high-contrast design with dynamic elements.
News broadcast aesthetic with modern touch.
{title_text}
Professional, authoritative feel. No watermarks.""",
}

# 封面比例配置
ASPECT_PRESETS = {
    "headline": "21:9",   # 头条封面 2.35:1
    "secondary": "1:1",   # 次条封面
    "thumbnail": "3:2",   # 小图封面
}


def build_prompt(title: str, style: str) -> str:
    """根据标题和风格构建 prompt"""
    template = STYLE_TEMPLATES.get(style, STYLE_TEMPLATES["tech"])

    if title:
        title_text = f"Include Chinese text '{title}' prominently displayed in the center."
    else:
        title_text = ""

    return template.format(title_text=title_text)


def generate_cover(
    prompt: str,
    output: str,
    aspect: str = "headline",
    size: str = "2K"
) -> bool:
    """调用 Nano Banana Router 生成封面图"""

    if not ROUTER_SCRIPT.exists():
        print(f"Error: Nano Banana Router not found at {ROUTER_SCRIPT}")
        print("Please install nanobanana-router skill first.")
        return False

    # 获取 API Key
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        # 尝试从 .env 文件读取
        env_file = Path.home() / ".claude/.env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith("OPENROUTER_API_KEY="):
                        api_key = line.strip().split("=", 1)[1]
                        os.environ["OPENROUTER_API_KEY"] = api_key
                        break

    if not api_key:
        print("Error: OPENROUTER_API_KEY not set")
        return False

    # 获取比例
    aspect_ratio = ASPECT_PRESETS.get(aspect, aspect)

    # 构建命令
    cmd = [
        sys.executable,
        str(ROUTER_SCRIPT),
        "--prompt", prompt,
        "--aspect", aspect_ratio,
        "--size", size,
        "--output", output,
        "--show-cost"
    ]

    print(f"Generating cover with style: {aspect_ratio}, size: {size}")
    print(f"Output: {output}")
    print()

    # 执行
    result = subprocess.run(cmd, env=os.environ)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(
        description="微信公众号封面图生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --title "零成本 AI API" --style tech -o cover.png
  %(prog)s --title "Python 入门指南" --style tutorial -o tutorial.png
  %(prog)s --prompt "自定义描述..." -o custom.png

预设风格:
  tech      科技/编程类（深色赛博朋克风）
  tutorial  教程/入门类（浅色清爽风）
  tool      工具推荐类（产品展示风）
  opinion   观点/思考类（艺术抽象风）
  news      新闻/资讯类（新闻播报风）

封面类型:
  headline   头条封面 (21:9, 默认)
  secondary  次条封面 (1:1)
  thumbnail  小图封面 (3:2)
        """
    )

    # 内容参数
    content_group = parser.add_mutually_exclusive_group(required=True)
    content_group.add_argument(
        "--title", "-t",
        help="文章标题（将显示在封面上）"
    )
    content_group.add_argument(
        "--prompt", "-p",
        help="自定义 prompt（完全自定义）"
    )

    # 风格参数
    parser.add_argument(
        "--style", "-s",
        choices=list(STYLE_TEMPLATES.keys()),
        default="tech",
        help="预设风格 (默认: tech)"
    )

    # 输出参数
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="输出文件路径"
    )
    parser.add_argument(
        "--type",
        choices=list(ASPECT_PRESETS.keys()),
        default="headline",
        help="封面类型 (默认: headline)"
    )
    parser.add_argument(
        "--size",
        choices=["1K", "2K", "4K"],
        default="2K",
        help="图片尺寸 (默认: 2K)"
    )

    args = parser.parse_args()

    # 构建 prompt
    if args.prompt:
        prompt = args.prompt
    else:
        prompt = build_prompt(args.title, args.style)

    print("=" * 50)
    print("微信公众号封面图生成器")
    print("=" * 50)
    print(f"\nPrompt:\n{prompt}\n")

    # 生成
    success = generate_cover(
        prompt=prompt,
        output=args.output,
        aspect=args.type,
        size=args.size
    )

    if success:
        print("\n✓ 封面图生成完成!")
    else:
        print("\n✗ 生成失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
