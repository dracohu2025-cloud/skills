#!/usr/bin/env python3
"""
Render Markdown using bm.md API and copy styled HTML to clipboard via browser.

This script:
1. Calls bm.md API to render Markdown to HTML
2. Opens a local browser page with the rendered HTML
3. Uses JavaScript to select and copy the content to clipboard
4. Keeps the browser open for manual verification

Usage:
    python render_and_copy.py <file.md> [options]
"""

import argparse
import json
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict
import requests

API_BASE = "https://bm.md/api/markdown"


def render_markdown(
    markdown: str,
    style: str = "botanical",
    code_theme: str = "kimbie-light",
    platform: str = "wechat"
) -> str:
    """Render Markdown to styled HTML via bm.md API."""
    url = f"{API_BASE}/render"
    headers = {"Content-Type": "application/json"}

    data = {
        "markdown": markdown,
        "markdownStyle": style,
        "codeTheme": code_theme,
        "platform": platform,
        "enableFootnoteLinks": True,
        "openLinksInNewWindow": True
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("result", "")
    except requests.RequestException as e:
        print(f"❌ Error calling bm.md API: {e}", file=sys.stderr)
        sys.exit(1)


def create_html_page(rendered_html: str) -> str:
    """Create a complete HTML page with JavaScript for auto-copy."""
    template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>bm.md Renderer - Auto Copy</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .info {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #2196f3;
        }
        .info h3 {
            margin: 0 0 10px 0;
            color: #1976d2;
        }
        .status {
            font-weight: bold;
            color: #4caf50;
        }
        .button {
            background: #2196f3;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 10px;
        }
        .button:hover {
            background: #1976d2;
        }
        #content {
            min-height: 100px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="info">
            <h3>📋 bm.md 渲染完成</h3>
            <p><span id="status" class="status">✓ 内容已自动复制到剪贴板！</span></p>
            <p>现在可以直接粘贴到微信公众号编辑器（Cmd+V）</p>
            <p>如果需要重新复制，点击下方按钮：</p>
            <button class="button" onclick="copyToClipboard()">🔄 重新复制</button>
            <button class="button" onclick="window.close()">关闭窗口</button>
        </div>
        <div id="content">
            {RENDERED_HTML}
        </div>
    </div>

    <script>
        async function copyToClipboard() {{
            try {{
                // Select the rendered content
                const content = document.getElementById('content');

                // Create a range to select the content
                const range = document.createRange();
                range.selectNodeContents(content);
                const selection = window.getSelection();
                selection.removeAllRanges();
                selection.addRange(range);

                // Execute copy command
                const successful = document.execCommand('copy');

                if (successful) {{
                    document.getElementById('status').textContent = '✓ 已复制到剪贴板！';
                    document.getElementById('status').style.color = '#4caf50';
                }} else {{
                    document.getElementById('status').textContent = '❌ 复制失败，请手动选择复制';
                    document.getElementById('status').style.color = '#f44336';
                }}
            }} catch (err) {{
                console.error('Copy failed:', err);
                // Fallback to Clipboard API
                try {{
                    const content = document.getElementById('content');
                    await navigator.clipboard.write([
                        new ClipboardItem({{
                            'text/html': new Blob([content.innerHTML], {{ type: 'text/html' }}),
                            'text/plain': new Blob([content.innerText], {{ type: 'text/plain' }})
                        }})
                    ]);
                    document.getElementById('status').textContent = '✓ 已复制到剪贴板！';
                }} catch (clipboardErr) {{
                    document.getElementById('status').textContent = '❌ 复制失败: ' + clipboardErr;
                    document.getElementById('status').style.color = '#f44336';
                }}
            }}
        }}

        // Auto-copy on page load
        window.addEventListener('load', () => {{
            setTimeout(copyToClipboard, 500);
        }});
    </script>
</body>
</html>"""
    return template.replace("{RENDERED_HTML}", rendered_html)


def main():
    parser = argparse.ArgumentParser(
        description="Render Markdown to HTML and copy to clipboard",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("file", help="Markdown file path")
    parser.add_argument("--style", default="botanical", help="Visual style (default: botanical)")
    parser.add_argument("--code-theme", default="kimbie-light", help="Code theme")
    parser.add_argument("--platform", default="wechat", choices=["html", "wechat", "zhihu", "juejin"], help="Target platform")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser, just render to file")

    args = parser.parse_args()

    # Read markdown file
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            markdown = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    print(f"🎨 Rendering {args.file} with bm.md API...")
    print(f"   Style: {args.style}")
    print(f"   Platform: {args.platform}")
    print(f"   Code Theme: {args.code_theme}")

    # Render markdown
    rendered_html = render_markdown(
        markdown,
        style=args.style,
        code_theme=args.code_theme,
        platform=args.platform
    )

    print("✓ API render complete")

    # Create HTML page
    html_page = create_html_page(rendered_html)

    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_page)
        temp_file = f.name

    print(f"✓ Saved to: {temp_file}")

    if args.no_browser:
        print("\n💡 Open the file in your browser to copy to clipboard:")
        print(f"   open {temp_file}")
    else:
        # Open in browser
        print("🌐 Opening browser...")
        try:
            # Try using open on macOS
            subprocess.run(['open', temp_file], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Try xdg-open on Linux
                subprocess.run(['xdg-open', temp_file], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback: just print the path
                print(f"💡 Please open in browser: {temp_file}")

        print("\n✅ Done! The content should be automatically copied to your clipboard.")
        print("   You can now paste directly into WeChat Official Account editor (Cmd+V)")


if __name__ == "__main__":
    main()
