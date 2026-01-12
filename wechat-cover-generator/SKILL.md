---
name: wechat-cover-generator
description: Generates cover images suitable for WeChat Official Account articles. Uses Nano Banana Pro (Gemini 3 Pro Image) as the image generation backend.
invocable: user
---

# WeChat Official Account Cover Generator

Generates cover images suitable for WeChat Official Account articles. Uses Nano Banana Pro (Gemini 3 Pro Image) as the image generation backend.

## Use Cases

Use this skill when users need to generate cover images for WeChat Official Account articles. Trigger keywords include:
- "Generate WeChat cover"
- "Official account cover image"
- "WeChat article cover"
- "WeChat cover"

## Prerequisites

Configure OpenRouter API Key (in `~/.claude/.env`):

```bash
OPENROUTER_API_KEY=your_api_key
```

## Cover Image Specifications

| Type | Ratio | Recommended Size | API Parameter |
|------|-------|------------------|---------------|
| Featured Article Cover | 2.35:1 | 900x383 | `--aspect 21:9` |
| Secondary Article Cover | 1:1 | 200x200 | `--aspect 1:1` |
| Thumbnail Cover | 3:2 | 300x200 | `--aspect 3:2` |

## Workflow

### 1. Analyze Article Content

Read the article and extract:
- Theme and core message
- Keywords
- Emotional tone (technical/emotional/humorous)

### 2. Design Cover Approach

**Tech Articles**: Dark background + neon glow effects, code/chip/terminal elements
**Tutorials**: Clear and professional, brand colors + high contrast, icons/flowcharts
**Opinion Pieces**: Artistic feel, abstract graphics, atmosphere

### 3. Generate Cover Image

```bash
export OPENROUTER_API_KEY="your_key"

python ~/.claude/skills/nanobanana-router/scripts/image_router.py \
  --prompt "YOUR_PROMPT" \
  --aspect 21:9 \
  --size 2K \
  --output "output.png"
```

## Prompt Template

```
A WeChat article cover image. [Style].

Theme: [Article theme]
Visual elements: [Element list]
Color scheme: [Color tone]
Text: [Chinese title, optional]

Requirements: 21:9 ultra-wide ratio, 2K HD, no watermark, visual center aligned
```

## Examples

**Tech Articles:**
```
A futuristic tech cover for WeChat article. Dark background with
blue-purple gradient glow. Floating terminal windows, code snippets,
AI chip elements. Chinese text 'Zero-Cost AI API' in center.
Cyberpunk aesthetic, high contrast, neon accents. No watermarks.
```

**Tutorials:**
```
A clean tutorial cover for WeChat article about Python. Light gradient
background (white to soft blue). Python logo with code editor mockup.
Minimalist style. Text 'Python Beginner Guide'. Modern, educational. No watermarks.
```

## Output

- Save to project `assets/` directory
- Naming: `{topic}-cover.png`
- Generate 2-3 versions for selection
