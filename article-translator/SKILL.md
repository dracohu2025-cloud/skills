---
name: article-translator
description: English to Simplified Chinese article translator with Visual Retention rules. Supports standard web articles and Twitter/X threads. Features style switching (e.g., --style vivid) and platform-specific formatting.
invocable: user
---

# Article Translator (Enhanced with Visual Retention)

Translates English articles completely into Simplified Chinese Markdown documents. Optimized for WeChat Official Account publishing and X (Twitter) thread localization.

## 🔴 Hard Constraint: Visual Retention (Mandatory)

To ensure the integrity of the article's layout and impact, you **must** follow the "Visual Retention" principle:

1.  **Map Before Translate**: Before translating any text, identify every visual element (images, videos, charts, embedded tweets) and its exact position relative to the surrounding paragraphs.
2.  **Explicit Markers**: In your internal processing, mark where each visual belongs (e.g., "Image 1 follows Paragraph 3").
3.  **Zero Loss Policy**: No visual elements should be omitted. If a hotlinked image is unavailable, keep the placeholder with its original URL and alt text.
4.  **Layout Symmetry**: The sequence of "Text-Visual-Text" in the translation must mirror the original exactly.

## 🚀 Parameters & Styles

You can switch translation styles and target platforms using arguments:

- **Usage**: `skill: "article-translator", args: "<URL> --style <STYLE> --platform <PLATFORM>"`
- **Styles (`--style`)**:
    - `standard`: Balanced, professional, and faithful to the source.
    - `vivid` (Recommended for WeChat): Engaging, conversational, uses "We-media" style storytelling, and optimizes for mobile readability.
- **Platforms (`--platform`)**:
    - `wechat`: Optimizes for WeChat Editor (內联样式支持, footnote links).
    - `markdown`: Standard GitHub-flavored Markdown.

## 🛠 Workflow

### Step 1: Content Fetching & Visual Mapping
- **Regular Articles**: Use `WebFetch`.
- **Twitter/X Tweets**: Use Playwright (`scripts/fetch_twitter.py`).
- **MAPPING**: Create a detailed list of all paragraph-visual pairs.

### Step 2: Translation (Style-Aware)
- Apply the requested `--style`.
- **vivid mode**: Focus on catchy headings, "gold sentences" (金句), and a warm tone.
- **Terminology**: Use `Chinese (English Original)` format for technical terms.

### Step 3: Formatting & Output
- Standard Markdown structure.
- **Visual Integrity Check**: Verify all images from Step 1 are present in their correct translated context.

### Step 4: Update VitePress Index (VitePress Projects Only)
- **Auto-Discovery**: Check if an `index.md` exists in the target directory (e.g., the folder where you save the translation).
- **Entry Insertion**: Append or insert a link to the new article in the `index.md` file.
- **Format**: Use the standard VitePress list or sidebar format (e.g., `- [Translated Title](./filename.md)`).
- **Date Handling**: If the index is sorted by date, ensure the new entry is placed in the correct chronological position.

## 📄 Output Structure

```markdown
# [Translated Catchy Title]

> Original: [Original Title](Original-URL)
> Author: [Name] | Translation: AI (Style: [Requested Style])

---

[Translated Intro]

![Image 1 Alt](Original-Image-URL)

[Translated Body Paragraphs with preserved visuals...]

---
*Translated via Enhanced Article Translator*
```

## 📦 Required Scripts
- `scripts/fetch_twitter.py` - For JavaScript-heavy social platforms.
