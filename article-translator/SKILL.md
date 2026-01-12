---
name: article-translator
description: Translates English articles to Simplified Chinese Markdown format suitable for WeChat Official Account publishing. Use this skill when users provide English article URLs and request translation, conversion to Chinese articles, or localization. Supports preserving original structure and images. Supports Twitter/X tweet fetching.
invocable: user
---

# Article Translator

Translates English articles completely into Simplified Chinese Markdown documents suitable for WeChat Official Account publishing.

## Trigger Conditions

Triggered when users provide an English article URL and request:
- Translation of English articles
- Converting English content to Chinese articles for WeChat
- Localizing English content

## Supported URL Types

1. **Regular Web Articles** - Fetched directly using WebFetch tool
2. **Twitter/X Tweets** - Fetched using Playwright headless browser (requires JavaScript rendering)

## Workflow

### Step 1: Identify URL Type and Fetch Content

#### 1a. Regular Web Articles

Use WebFetch tool to fetch the URL content provided by the user:

```
WebFetch(url: "<user-provided-URL>", prompt: "Extract the complete article content including: title, author, publication date, all paragraph text, all image URLs and alt text, all code blocks, quote blocks, lists, and other structured content. Maintain original structure order.")
```

#### 1b. Twitter/X Tweets (x.com or twitter.com)

Twitter/X requires JavaScript rendering, WebFetch cannot fetch content directly. Use Playwright headless browser:

**Method 1: Using Script**

```bash
python /Users/dracohu/.claude/skills/article-translator/scripts/fetch_twitter.py "<tweet-URL>"
```

Script parameters:
- `--scroll N`: Number of scrolls for loading long tweets (default 10)
- `--wait N`: Initial wait seconds (default 8)
- `--raw`: Output raw content without filtering page elements
- `-o FILE`: Output to file

**Method 2: Inline Playwright Code**

If the script is unavailable, write Playwright code directly:

```python
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        viewport={'width': 1280, 'height': 2000}
    )
    page = context.new_page()

    try:
        page.goto('<tweet-URL>', wait_until='domcontentloaded', timeout=30000)
    except Exception as e:
        print(f"Navigation warning: {e}")

    # Wait for page rendering
    time.sleep(8)

    # Scroll to load more content
    for i in range(10):
        page.evaluate('window.scrollBy(0, 1000)')
        time.sleep(1)

    # Scroll back to top
    page.evaluate('window.scrollTo(0, 0)')
    time.sleep(2)

    # Get content
    body_text = page.locator('body').inner_text()
    print(body_text)

    browser.close()
```

**Dependency Installation** (if Playwright is not installed):

```bash
pip install playwright && playwright install chromium
```

### Step 2: Analyze Article Structure

Identify and record the following elements:
- Main title and subtitles
- Paragraph hierarchy (H1-H6)
- Image positions and URLs
- Code blocks and their language identifiers
- Quote blocks
- Ordered/unordered lists
- Tables
- Author information and publication time

**Twitter/X Special Handling**:
- Tweets typically use Roman numerals (I, II, III...) or numbers to mark sections
- Author info is in @handle format
- Publication time is at the bottom of the tweet

### Step 3: Translate Content

Follow these translation principles:

**Title Handling**:
- Recreate main titles to fit WeChat reading habits
- Use eye-catching but not exaggerated expressions appropriately
- Maintain professionalism while increasing readability

**Body Translation**:
- Use fluent, natural Chinese expressions, avoid translationese
- Keep technical terms in English with Chinese explanations, format: `Chinese Translation (English Term)`
- Split long sentences appropriately to fit Chinese reading habits
- Maintain the original tone and style

**Special Content Handling**:
- Code blocks: Keep as-is, only translate comments
- Quote blocks: Translate content, preserve quote format
- Proper nouns: Include English original on first occurrence

### Step 4: Format Output

Output in standard Markdown format with this structure:

```markdown
# [Translated Attractive Title]

> Original link: [Original Title](Original-URL)
> Author: [Author Name] | Translation: AI Translation

---

[Translated body content]

## [Section Title]

[Section content]

![Image description](original-image-URL)

[Continue translated content...]

---

*This article was translated from [Source Website]*
```

**Twitter/X Format Special Case**:

```markdown
# [Translated Title]

> Original link: [Original Title](https://x.com/username/status/xxx)
> Author: [Author Name] (@username) | Translation: AI Translation
> Published: YYYY-MM-DD

---

[Translated body content]

---

*This article was translated from [Author Name]'s long post/thread on X*
```

### Image Handling Rules

1. **Preserve Original Image URLs**: Use image URLs directly from the original article
2. **Format**: `![Chinese image description](original-image-URL)`
3. **Image Description**: Translate English alt text to Chinese
4. **Position**: Maintain images' relative positions from the original

### Step 5: Quality Check

Perform the following checks after translation:
- [ ] All paragraphs translated
- [ ] Image URLs correctly embedded
- [ ] Code block format complete
- [ ] Title hierarchy correct
- [ ] No missing content
- [ ] Chinese expressions are fluent and natural

## Output Examples

### Regular Article Example

```markdown
# Why Rust is Changing the Future of Systems Programming

> Original link: [Why Rust is Changing the Future of Systems Programming](https://example.com/article)
> Author: John Smith | Translation: AI Translation

---

Over the past few years, the Rust programming language has gradually become a rising star in the systems programming field with its unique memory safety guarantees and zero-cost abstractions...

## Memory Safety: No Garbage Collection Needed

Rust's most compelling feature is its Ownership System. This innovative design allows developers to catch most memory errors at compile time...

![Rust Ownership Model Diagram](https://example.com/images/ownership.png)

---

*This article was translated from Example Tech Blog*
```

### Twitter/X Tweet Example

```markdown
# Curiosity Is Compound Interest for Your Brain

> Original link: [Curiosity Is Compound Interest for Your Brain](https://x.com/nurijanian/status/xxx)
> Author: George Nurijanian (@nurijanian) | Translation: AI Translation
> Published: 2025-12-29

---

## I. The Distraction Proposition

Distraction fragments attention. AI tools make it more fragmented - ChatGPT is like a slot machine with a keyboard...

## II. The Curiosity-Creativity Loop

Creativity doesn't appear from nowhere. It emerges from a specific engine: curiosity sustained long enough to produce unexpected combinations...

---

*This article was translated from George Nurijanian's long post on X*
```

## Notes

1. **Copyright Notice**: Always preserve original link and author information
2. **Image Availability**: Some websites may have hotlink protection, remind users when translating
3. **Long Article Handling**: For very long articles, translate in segments to ensure quality
4. **Technical Content**: Keep code and commands in technical articles as-is
5. **Twitter/X Special Notes**:
   - Twitter requires JavaScript rendering, WebFetch cannot fetch directly
   - Need to install Playwright first: `pip install playwright && playwright install chromium`
   - Fetching may require longer wait times (10-30 seconds)
   - If login wall encountered, most public tweet content can still be fetched

## Script Files

- `scripts/fetch_twitter.py` - Twitter/X content fetching script
