import argparse
import re
import sys
from typing import List, Tuple

def to_bold(text: str) -> str:
    """Convert text to unicode bold."""
    # Mapping for lowercase and uppercase latin letters
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    bold = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"
    trans_table = str.maketrans(normal, bold)
    return text.translate(trans_table)

def to_italic(text: str) -> str:
    """Convert text to unicode italic."""
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    italic = "𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧"
    trans_table = str.maketrans(normal, italic)
    return text.translate(trans_table)

def apply_styles(text: str) -> str:
    """Apply unicode styles to markdown bold/italic."""
    # Bold: **text** or __text__
    text = re.sub(r'\*\*(.+?)\*\*', lambda m: to_bold(m.group(1)), text)
    text = re.sub(r'__(.+?)__', lambda m: to_bold(m.group(1)), text)

    # Italic: *text* or _text_
    text = re.sub(r'\*(.+?)\*', lambda m: to_italic(m.group(1)), text)
    # Avoid replacing _ inside words or urls
    text = re.sub(r'(?<!\w)_(.+?)_(?!\w)', lambda m: to_italic(m.group(1)), text)

    return text

def extract_images(text: str) -> Tuple[str, List[str]]:
    """Extract image URLs and remove them from text."""
    images = []
    def replace_img(match):
        alt = match.group(1)
        url = match.group(2)
        images.append(url)
        return f"[Image: {alt}]" if alt else "[Image]"

    # Markdown image: ![alt](url)
    cleaned_text = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_img, text)
    return cleaned_text, images

def split_into_tweets(text: str, max_length: int = 280) -> List[str]:
    """Split text into a thread of tweets."""
    tweets = []

    # Pre-process: split by double newlines to preserve paragraphs
    paragraphs = text.split('\n\n')

    current_tweet = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # If paragraph fits in current tweet
        if len(current_tweet) + len(para) + 2 <= max_length:
            if current_tweet:
                current_tweet += "\n\n" + para
            else:
                current_tweet = para
        else:
            # Current tweet is full, push it
            if current_tweet:
                tweets.append(current_tweet)
                current_tweet = ""

            # If paragraph itself is too long, split by sentences
            if len(para) > max_length:
                sentences = re.split(r'(?<=[.!?])\s+', para)
                for sentence in sentences:
                    if len(current_tweet) + len(sentence) + 1 <= max_length:
                        if current_tweet:
                            current_tweet += " " + sentence
                        else:
                            current_tweet = sentence
                    else:
                        if current_tweet:
                            tweets.append(current_tweet)
                        current_tweet = sentence
            else:
                current_tweet = para

    if current_tweet:
        tweets.append(current_tweet)

    return tweets

def format_thread(tweets: List[str]) -> List[str]:
    """Add numbering (1/n) to tweets."""
    total = len(tweets)
    if total <= 1:
        return tweets

    formatted = []
    for i, tweet in enumerate(tweets, 1):
        # Check if adding suffix exceeds limit (simple check)
        suffix = f" ({i}/{total})"
        if len(tweet) + len(suffix) > 280:
            # Truncate if necessary (though ideally we should account for this in split)
            tweet = tweet[:280-len(suffix)-3] + "..."
        formatted.append(f"{tweet}{suffix}")
    return formatted

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to Twitter Thread/Article format")
    parser.add_argument("file", help="Path to markdown file")
    parser.add_argument("--style", action="store_true", help="Apply Unicode bold/italic styles")
    parser.add_argument("--thread", action="store_true", help="Format as a thread with numbering")

    args = parser.parse_args()

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Extract images
        text_content, images = extract_images(content)

        # 2. Apply styles if requested
        if args.style:
            text_content = apply_styles(text_content)

        # 3. Output logic
        if args.thread:
            tweets = split_into_tweets(text_content, max_length=260) # Conservative limit
            formatted_tweets = format_thread(tweets)

            print("--- Generated Twitter Thread ---\n")
            for i, tweet in enumerate(formatted_tweets, 1):
                print(f"[Tweet {i}]\n{tweet}\n{'-'*20}")

            if images:
                print("\n[Extracted Images]")
                for img in images:
                    print(f"- {img}")
        else:
            print("--- Formatted Content (for Twitter Article) ---\n")
            print(text_content)
            if images:
                print("\n[Images to Upload Manually]")
                for img in images:
                    print(f"- {img}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
