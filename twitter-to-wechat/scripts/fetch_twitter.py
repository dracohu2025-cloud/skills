#!/usr/bin/env python3
"""
Twitter/X Content Fetcher using Playwright
用于获取 Twitter/X 上需要 JavaScript 渲染的内容
"""

from playwright.sync_api import sync_playwright
import sys
import time
import argparse


def fetch_twitter_content(url: str, scroll_times: int = 10, wait_seconds: int = 8) -> tuple:
    """
    使用 Playwright 无头浏览器获取 Twitter/X 内容

    Args:
        url: Twitter/X 推文 URL
        scroll_times: 滚动次数，用于加载更多内容
        wait_seconds: 初始等待秒数

    Returns:
        (页面文本内容, 图片URL列表)
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 2000}
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
        except Exception as e:
            print(f"Navigation warning (may still work): {e}", file=sys.stderr)

        # Wait for page to render
        time.sleep(wait_seconds)

        # Scroll down to load more content
        for i in range(scroll_times):
            page.evaluate('window.scrollBy(0, 1000)')
            time.sleep(1)

        # Scroll back to top
        page.evaluate('window.scrollTo(0, 0)')
        time.sleep(2)

        # Get full page text
        try:
            body_text = page.locator('body').inner_text()
        except Exception as e:
            print(f"Error getting text: {e}", file=sys.stderr)
            body_text = ""

        # Extract image URLs from the tweet
        image_urls = []
        try:
            # Use article selector which is more reliable
            images = page.locator('article img').all()
            seen_urls = set()
            for img in images:
                src = img.get_attribute('src')
                # Filter for content images (media), skip profile avatars
                if src and 'pbs.twimg.com/media' in src and src not in seen_urls:
                    # Get the highest quality version (replace &name= suffix)
                    high_quality_src = src.split('&name=')[0] + '&name=orig'
                    image_urls.append(high_quality_src)
                    seen_urls.add(src)
        except Exception as e:
            print(f"Error extracting images: {e}", file=sys.stderr)

        browser.close()
        return body_text, image_urls


def extract_tweet_content(raw_text: str) -> str:
    """
    从原始页面文本中提取推文内容，去除页面杂项

    Args:
        raw_text: 原始页面文本

    Returns:
        清理后的推文内容
    """
    lines = raw_text.split('\n')

    # 标记内容开始和结束的关键词
    skip_prefixes = [
        "Don't miss what's happening",
        "People on X are the first to know",
        "Log in",
        "Sign up",
        "See new posts",
        "New to X?",
        "Sign up now",
        "Sign up with",
        "Create account",
        "By signing up",
        "Trending now",
        "What's happening",
        "Terms of Service",
        "Privacy Policy",
        "Cookie Policy",
        "Accessibility",
        "Ads info",
        "More",
        "© 20",
        "Show more",
        "Read ",  # "Read X replies"
        "Want to publish",
        "Upgrade to Premium",
    ]

    # 过滤掉不需要的行
    filtered_lines = []
    in_content = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 检查是否应该跳过这行
        should_skip = False
        for prefix in skip_prefixes:
            if line.startswith(prefix):
                should_skip = True
                break

        # 跳过 trending 部分
        if "Trending" in line or "posts" in line and any(c.isdigit() for c in line):
            should_skip = True

        if not should_skip:
            filtered_lines.append(line)

    return '\n'.join(filtered_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Fetch Twitter/X content using Playwright headless browser'
    )
    parser.add_argument('url', help='Twitter/X URL to fetch')
    parser.add_argument('--scroll', type=int, default=10,
                        help='Number of scroll iterations (default: 10)')
    parser.add_argument('--wait', type=int, default=8,
                        help='Initial wait time in seconds (default: 8)')
    parser.add_argument('--raw', action='store_true',
                        help='Output raw content without filtering')
    parser.add_argument('--output', '-o', type=str,
                        help='Output file path (default: stdout)')
    parser.add_argument('--images', action='store_true',
                        help='Also output image URLs found in the tweet')

    args = parser.parse_args()

    print(f"Fetching content from: {args.url}", file=sys.stderr)

    raw_content, image_urls = fetch_twitter_content(
        args.url,
        scroll_times=args.scroll,
        wait_seconds=args.wait
    )

    if args.raw:
        content = raw_content
    else:
        content = extract_tweet_content(raw_content)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Content saved to: {args.output}", file=sys.stderr)
    else:
        print(content)

    # Output image URLs if requested
    if args.images and image_urls:
        print("\n=== IMAGES FOUND ===", file=sys.stderr)
        for i, img_url in enumerate(image_urls, 1):
            print(f"Image {i}: {img_url}")
        print(f"Total: {len(image_urls)} images", file=sys.stderr)


if __name__ == '__main__':
    main()
