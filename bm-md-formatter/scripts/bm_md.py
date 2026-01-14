#!/usr/bin/env python3
"""
bm.md API Client - Markdown formatting and rendering tool

Provides four main functions:
1. render() - Convert Markdown to styled HTML
2. parse() - Convert HTML to Markdown
3. extract() - Extract plain text from Markdown
4. lint() - Validate and fix Markdown formatting

Usage:
    python bm_md.py render <file.md> [options]
    python bm_md.py parse <file.html>
    python bm_md.py extract <file.md>
    python bm_md.py lint <file.md>
"""

import argparse
import json
import sys
from typing import Any, Dict
import requests

API_BASE = "https://bm.md/api/markdown"


def call_api(endpoint: str, data: Dict[str, Any]) -> str:
    """Make API call to bm.md and return the result."""
    url = f"{API_BASE}/{endpoint}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("result", "")
    except requests.RequestException as e:
        print(f"Error calling API: {e}", file=sys.stderr)
        sys.exit(1)


def render_markdown(
    markdown: str,
    style: str = "ayu-light",
    code_theme: str = "kimbie-light",
    platform: str = "html",
    footnote_links: bool = True,
    new_window: bool = True
) -> str:
    """Render Markdown to styled HTML.

    Args:
        markdown: Markdown source text
        style: Visual style ID (default: ayu-light)
        code_theme: Code highlighting theme (default: kimbie-light)
        platform: Target platform - html, wechat, zhihu, juejin
        footnote_links: Convert links to footnotes
        new_window: Open links in new window

    Returns:
        Styled HTML string
    """
    data = {
        "markdown": markdown,
        "markdownStyle": style,
        "codeTheme": code_theme,
        "platform": platform,
        "enableFootnoteLinks": footnote_links,
        "openLinksInNewWindow": new_window
    }
    return call_api("render", data)


def parse_html(html: str) -> str:
    """Convert HTML to Markdown.

    Args:
        html: HTML source code

    Returns:
        Markdown string
    """
    return call_api("parse", {"html": html})


def extract_text(markdown: str) -> str:
    """Extract plain text from Markdown, removing all formatting.

    Args:
        markdown: Markdown source text

    Returns:
        Plain text with paragraphs preserved
    """
    return call_api("extract", {"markdown": markdown})


def lint_markdown(markdown: str) -> str:
    """Validate and fix Markdown formatting issues.

    Args:
        markdown: Markdown source text

    Returns:
        Fixed/formatted Markdown string
    """
    return call_api("lint", {"markdown": markdown})


def main():
    parser = argparse.ArgumentParser(
        description="bm.md Markdown formatter - Convert and style Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Render for WeChat
  python bm_md.py render article.md --style botanical --platform wechat

  # Render with dark theme
  python bm_md.py render article.md --code-theme tokyo-night-dark

  # Convert HTML to Markdown
  python bm_md.py parse webpage.html

  # Extract plain text
  python bm_md.py extract article.md

  # Fix formatting issues
  python bm_md.py lint messy.md
        """
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Render command
    render_parser = subparsers.add_parser("render", help="Render Markdown to HTML")
    render_parser.add_argument("file", help="Markdown file path")
    render_parser.add_argument("--style", default="ayu-light", help="Visual style (default: ayu-light)")
    render_parser.add_argument("--code-theme", default="kimbie-light", help="Code theme (default: kimbie-light)")
    render_parser.add_argument("--platform", default="html", choices=["html", "wechat", "zhihu", "juejin"], help="Target platform")
    render_parser.add_argument("--no-footnote-links", action="store_true", help="Disable footnote-style links")
    render_parser.add_argument("--same-window", action="store_true", help="Open links in same window")
    render_parser.add_argument("--output", "-o", help="Save to file instead of stdout")

    # Parse command
    parse_parser = subparsers.add_parser("parse", help="Convert HTML to Markdown")
    parse_parser.add_argument("file", help="HTML file path")
    parse_parser.add_argument("--output", "-o", help="Save to file instead of stdout")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract plain text from Markdown")
    extract_parser.add_argument("file", help="Markdown file path")
    extract_parser.add_argument("--output", "-o", help="Save to file instead of stdout")

    # Lint command
    lint_parser = subparsers.add_parser("lint", help="Fix Markdown formatting")
    lint_parser.add_argument("file", help="Markdown file path")
    lint_parser.add_argument("--output", "-o", help="Save to file instead of stdout")

    args = parser.parse_args()

    # Read input file
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Execute command
    if args.command == "render":
        result = render_markdown(
            content,
            style=args.style,
            code_theme=args.code_theme,
            platform=args.platform,
            footnote_links=not args.no_footnote_links,
            new_window=not args.same_window
        )
    elif args.command == "parse":
        result = parse_html(content)
    elif args.command == "extract":
        result = extract_text(content)
    elif args.command == "lint":
        result = lint_markdown(content)

    # Output
    if hasattr(args, "output") and args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Saved to: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
