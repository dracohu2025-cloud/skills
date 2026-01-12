---
name: nanobanana-router
description: Nano Banana Pro (Gemini 3 Pro Image) Image Generation API Router. Use this skill when you need to generate high-quality images using Google Gemini API. Supports text-to-image, image-to-image, multi-image fusion, Search Grounding, 2K/4K HD output, and various aspect ratios. Suitable for professional design, product visualization, storyboards, and complex multi-element composition.
invocable: user
---

# Nano Banana Pro Image Generation API Router

This skill invokes Google Gemini API's Nano Banana Pro (gemini-3-pro-image-preview) image generation capabilities through OpenRouter.

**Advantage**: Calling through OpenRouter provides detailed cost information and token usage statistics.

## Use Cases

- Generate high-quality images from text descriptions (text-to-image)
- Generate new images based on reference images (image-to-image)
- Multi-image fusion generation (up to 14 reference images)
- Generate 2K/4K HD images
- Generate images with different aspect ratios (square, landscape, portrait, ultra-wide)
- Complex multi-turn conversational image editing

## Prerequisites

Before using, obtain an OpenRouter API Key:

1. Visit [OpenRouter](https://openrouter.ai/keys)
2. Create an account and log in
3. Generate an API Key
4. Configure the API Key in environment variables

## Environment Variable Configuration

```bash
# OpenRouter API Key (Required)
export OPENROUTER_API_KEY="your_api_key"
```

Or configure in `~/.claude/.env` file:

```
OPENROUTER_API_KEY=your_api_key
```

## API Invocation Methods

### 1. Using Router Script (Recommended)

Router script provides a unified interface with automatic authentication and request handling:

```bash
# Basic usage - text to image
python scripts/image_router.py --prompt "A cute orange cat sleeping in sunlight" --output cat.png

# Specify aspect ratio and size
python scripts/image_router.py --prompt "Cyberpunk style city night scene" --aspect 16:9 --size 4K --output city.png

# Portrait image (mobile wallpaper)
python scripts/image_router.py --prompt "Ancient style beauty" --aspect 9:16 --size 2K --output beauty.png

# Image-to-image (reference image)
python scripts/image_router.py --prompt "Transform this image to watercolor style" --image ref.jpg --output watercolor.png

# Multi-image fusion
python scripts/image_router.py --prompt "Blend the styles of these two images" --image img1.jpg --image img2.jpg --output merged.png

# Show cost information
python scripts/image_router.py --prompt "Simple icon" --output icon.png --show-cost

# Use Flash model (faster but slightly lower quality)
python scripts/image_router.py --prompt "Simple icon" --model google/gemini-2.5-flash-preview-image --output icon.png
```

### 2. Direct OpenRouter API Call

#### Python Example

```python
import os
import json
import urllib.request

api_key = os.environ.get("OPENROUTER_API_KEY")
url = "https://openrouter.ai/api/v1/chat/completions"

payload = {
    "model": "google/gemini-3-pro-image-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate an image: A cute orange cat sleeping in sunlight"
                }
            ]
        }
    ],
    "max_tokens": 4096
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    method="POST"
)

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read())
    print(json.dumps(result, indent=2))
```

#### HTTP Request Example

```bash
curl -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
    "model": "google/gemini-3-pro-image-preview",
    "messages": [
      {
        "role": "user",
        "content": "Generate an image: A cute cat sleeping in sunlight"
      }
    ],
    "max_tokens": 4096
  }'
```

## Supported Aspect Ratios

| Aspect Ratio | Type | Description |
|--------------|------|-------------|
| `1:1` | Square | Default, suitable for avatars, icons |
| `2:3` | Portrait | Portrait photography |
| `3:2` | Landscape | Landscape photography |
| `3:4` | Portrait | Social media |
| `4:3` | Landscape | Traditional photos |
| `4:5` | Portrait | Instagram |
| `5:4` | Landscape | Slightly wide |
| `9:16` | Portrait | Mobile screen, short videos |
| `16:9` | Landscape | Widescreen, video covers |
| `21:9` | Ultra-wide | Cinematic aspect ratio |

## Supported Image Sizes

| Size | Description |
|------|-------------|
| `1K` | Default resolution (approx. 1024px) |
| `2K` | High definition (approx. 2048px) |
| `4K` | Ultra high definition (approx. 4096px) |

## Parameter Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | Required | Image description text |
| `aspect_ratio` | string | 1:1 | Aspect ratio |
| `image_size` | string | 1K | Image size |
| `reference_images` | list | - | Reference image path list (up to 14 images) |

## Cost Information

When calling through OpenRouter, the API returns detailed cost information:

```json
{
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 500,
    "total_tokens": 600
  }
}
```

Use `--show-cost` parameter to display cost per call:

```bash
python scripts/image_router.py --prompt "A cat" -o cat.png --show-cost
```

**OpenRouter Pricing Reference** (Nano Banana Pro):
- Input: $1.25 / 1M tokens
- Output: $10.00 / 1M tokens
- Image generation approx. $0.10-0.25 / image

## Nano Banana Pro Features

Compared to the basic Nano Banana (gemini-2.5-flash-image), the Pro version offers:

- **Advanced Synthesis Capabilities**: Improved multimodal reasoning, real-world grounding, high-fidelity visual synthesis
- **Rich Content Generation**: Supports infographics, charts, cinematic synthesis
- **Superior Text Rendering**: Industry-leading in-image text rendering, supports long paragraphs and multilingual typography (approx. 94% accuracy)
- **Consistent Imaging**: Supports cross-image identity preservation for up to 5 subjects
- **Fine Creative Control**: Local editing, lighting and focus adjustments, camera transforms, 2K/4K output, flexible aspect ratios
- **Multi-image Input**: Supports processing up to 14 reference images simultaneously

## Prompt Tips

1. **Describe specific details**: Include subject, environment, lighting, composition, etc.
2. **Specify style**: Such as "cyberpunk style", "watercolor style", "Chinese painting style"
3. **Use professional terms**: Such as "shallow depth of field", "studio lighting", "medium format"
4. **English prompts**: For complex scenes, English prompts may yield better results

### Prompt Examples

```
# Portrait
Vibrant close-up editorial portrait, model with sharp gaze, wearing sculptural hat,
rich color blocking, sharp eye focus, shallow depth of field, Vogue cover aesthetic,
medium format shot, strong studio lighting.

# Landscape
A Chinese landscape painting with distant misty mountains, calm waters,
verdant pines and cypresses, serene atmosphere, ink wash style, ample white space.

# Product
High-end watch product photography, black dial, rose gold case, pure black background,
soft side lighting, 4K HD details.
```

## Error Handling

Common error codes:

| Error Code | Description | Solution |
|------------|-------------|----------|
| 400 | Parameter error | Check prompt and other parameter formats |
| 401 | Authentication failed | Check if API Key is correct |
| 402 | Insufficient balance | Top up OpenRouter account |
| 429 | Rate limit exceeded | Reduce request frequency |
| 500 | Server error | Retry later |

## File Structure

```
nanobanana-router/
├── SKILL.md                  # This file
├── scripts/
│   └── image_router.py       # Unified router script (via OpenRouter)
└── references/
    └── api_docs.md           # Complete API documentation
```

## Related Resources

- [OpenRouter](https://openrouter.ai/)
- [OpenRouter API Documentation](https://openrouter.ai/docs)
- [Gemini 3 Pro Image on OpenRouter](https://openrouter.ai/google/gemini-3-pro-image-preview)
- [Nano Banana Pro Introduction](https://nano-banana.ai/)
