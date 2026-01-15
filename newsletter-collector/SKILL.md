---
name: newsletter-collector
description: Collects newsletter articles from KOL archive pages and translates them to Simplified Chinese. This skill should be used when users want to scrape newsletter content from writers like Dan Koe, Naval, James Clear, etc., and optionally translate articles using OpenRouter API with gemini-3-flash-preview.
---

# Newsletter Collector

Scrapes newsletter articles from KOL (Key Opinion Leader) archive pages and translates them to Simplified Chinese using OpenRouter API.

## Capabilities

1. **Article Collection** - Scrape articles from newsletter archive pages (e.g., Dan Koe's Letters)
2. **Content Extraction** - Extract full article content including images using `read_url_content`
3. **Translation** - Translate English articles to vivid, easy-to-understand Simplified Chinese
4. **Image Preservation** - Maintain all original images in their correct positions

## Prerequisites

- OpenRouter API key in `.env` file:
  ```
  OPENROUTER_API_KEY=sk-or-v1-...
  TEXT_PROCESSING_MODEL=google/gemini-3-flash-preview
  ```
- Python 3.9+ with `requests` and `python-dotenv`

## Workflow

### Step 1: Identify Archive URL

To find the newsletter archive, locate the KOL's "Letters", "Archive", or "Newsletter" page.

Common patterns:

- Dan Koe: `https://thedankoe.com/letters/`
- Substack: `https://[name].substack.com/archive`

### Step 2: Extract Article Links

To get article URLs from archive page, use `agent-browser`:

```bash
# Get clickable snapshot
agent-browser snapshot -c

# Look for article links with pattern like:
# link "[Article Title]" [ref=eXXX]:
#   /url: https://domain.com/letters/article-slug/
```

### Step 3: Scrape Article Content

To extract full article with images, use `read_url_content`:

1. Call `read_url_content` with article URL
2. View all content chunks using `view_content_chunk`
3. Look for `<img>` tags in chunks and preserve them

> **Critical: Image Preservation**
>
> Images in chunks appear as HTML:
>
> ```html
> [<img src="https://..." alt="..." />](https://...)
> ```
>
> Convert to Markdown:
>
> ```markdown
> ![Alt Text](https://...)
> ```

### Step 4: Save Raw Article

To save article as Markdown, use this structure:

```markdown
# [Article Title]

> **Original:** [Title](URL) > **Author:** [Author Name]

---

[Article content with preserved images]

---

_Scraped from [KOL] Newsletter Archive_
```

Save to: `knowledge_base/<kol-name>/raw/<article-slug>.md`

### Step 5: Translate Article

To translate using OpenRouter API, run:

```bash
cd /path/to/knowledge_base
source .venv/bin/activate
python scripts/translate.py <kol-name>/raw/<article>.md
```

Output: `<kol-name>/cn/<article>.md`

## Translation Style

The translation prompt enforces:

- **Vivid & engaging** (生动有趣) - conversational, not academic
- **Easy to understand** (通俗易懂) - plain language, simple terms
- **Image retention** - all `![](url)` preserved in original positions
- **Technical terms** - format as `中文 (English)`

## Directory Structure

```
knowledge_base/
├── <kol-name>/
│   ├── raw/           # English originals
│   └── cn/            # Chinese translations
├── scripts/
│   └── translate.py   # OpenRouter translation script
├── .venv/             # Python virtual environment
└── .env               # API keys
```

## Supported KOLs

| KOL                  | Archive URL            | Image Host      |
| -------------------- | ---------------------- | --------------- |
| Dan Koe              | thedankoe.com/letters/ | substackcdn.com |
| [Add more as needed] |                        |                 |

## Scripts

### translate.py

Translates a single article using OpenRouter API.

```bash
python scripts/translate.py <input_file> [output_file]
```

Reference: [scripts/translate.py](scripts/translate.py)
