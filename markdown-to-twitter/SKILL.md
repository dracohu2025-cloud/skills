---
description: Converts Markdown articles into Twitter-friendly formats. Supports converting to threaded tweets with auto-numbering, or generating Unicode-styled text (bold/italic) for pasting into Twitter Articles or regular tweets. Use when users want to publish long-form content to X/Twitter.
---

# Markdown to Twitter Converter

Utilities for converting long-form Markdown content into Twitter-friendly formats.

## Features

- **Thread Generation**: Automatically splits long articles into a thread of tweets (with `1/n` numbering).
- **Unicode Styling**: Converts Markdown bold (`**text**`) and italic (`*text*`) into Unicode characters (𝐞.𝐠., 𝐛𝐨𝐥𝐝) to preserve styling in plain text tweets.
- **Image Extraction**: Identifies and lists image URLs for manual upload.

## Usage

### Convert to Thread (Recommended)

Splits the article into multiple tweets.

```bash
python3 scripts/converter.py your_article.md --thread --style
```

### Convert to Styled Text

Generates a single block of text with Unicode styles, suitable for pasting into the Twitter Article editor or a single long tweet (for Blue subscribers).

```bash
python3 scripts/converter.py your_article.md --style
```

## Options

- `--thread`: Enable thread splitting and numbering.
- `--style`: Apply Unicode styling (bold/italic) to Markdown syntax.

## Example

Input (`article.md`):
```markdown
# My Post
This is a **bold** statement.
```

Output (`--style`):
```text
# My Post
This is a 𝐛𝐨𝐥𝐝 statement.
```
