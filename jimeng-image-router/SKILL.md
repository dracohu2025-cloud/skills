---
name: jimeng-image-router
description: Volcengine Jimeng SeeDream 4.5 Text-to-Image API Router. Use this skill to call Jimeng/Doubao image generation service to convert text descriptions to images. Supports text-to-image, image-to-image, multi-image fusion, different sizes and styles.
invocable: user
---

# Jimeng SeeDream 4.5 Text-to-Image API Router

This skill provides unified routing and invocation capabilities for Volcengine Jimeng SeeDream 4.5 Image Generation API.

## Use Cases

- Generate images from text descriptions (text-to-image)
- Generate new images based on reference images (image-to-image)
- Multi-image fusion generation
- Generate images in different sizes (square, landscape, portrait)
- Generate images in specific styles

## Prerequisites

Before using, obtain the following credentials from Volcengine Console:

1. **ARK_API_KEY**: Ark Model Service Platform API Key

Steps to obtain credentials:
1. Log in to [Volcengine Console](https://console.volcengine.com/)
2. Navigate to [Ark Model Service Platform](https://console.volcengine.com/ark)
3. Create an API Key
4. Enable `doubao-seedream-4-5` model service

## Environment Variable Configuration

```bash
# Ark API Key (Required)
export SEEDREAM_API_KEY="your_api_key"

# Or use generic naming
export ARK_API_KEY="your_api_key"

# Model name (Optional, default doubao-seedream-4-5-251128)
export JIMENG_MODEL_NAME="doubao-seedream-4-5-251128"
```

## API Invocation Methods

### 1. Using Router Script (Recommended)

Router script provides a unified interface with automatic authentication and request handling:

```bash
# Basic usage - text to image
python scripts/image_router.py --prompt "A cute orange cat sleeping in sunlight" --output cat.png

# Specify size (landscape)
python scripts/image_router.py --prompt "Cyberpunk style city night scene" --size 2560x1440 --output city.png

# Portrait image
python scripts/image_router.py --prompt "Ancient style beauty" --size 1440x2560 --output beauty.png

# Generate multiple images
python scripts/image_router.py --prompt "Futuristic tech car" --n 4 --output cars.png

# Image-to-image (reference image)
python scripts/image_router.py --prompt "Transform this image to watercolor style" --image ref.jpg --output watercolor.png
```

### 2. Direct API Call

#### Python SDK Example (Recommended)

```python
import os
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url='https://ark.cn-beijing.volces.com/api/v3',
    api_key=os.getenv('SEEDREAM_API_KEY') or os.getenv('ARK_API_KEY'),
)

# Text to image
response = client.images.generations.create(
    model="doubao-seedream-4-5-251128",
    prompt="Vibrant close-up editorial portrait, model with sharp gaze, wearing sculptural hat",
    n=1,
    size="1024x1024",
)

# Get image URL
image_url = response.data[0].url
print(f"Generated image: {image_url}")
```

#### Using OpenAI Compatible SDK

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("SEEDREAM_API_KEY") or os.environ.get("ARK_API_KEY"),
)

response = client.images.generate(
    model="doubao-seedream-4-5-251128",
    prompt="A Chinese landscape painting with distant mountains and serene atmosphere",
    n=1,
    size="1024x1024",
)

print(response.data[0].url)
```

#### HTTP Request Example

```bash
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SEEDREAM_API_KEY" \
  -d '{
    "model": "doubao-seedream-4-5-251128",
    "prompt": "A cute Shiba Inu running on grass",
    "n": 1,
    "size": "1024x1024"
  }'
```

## Supported Image Sizes

SeeDream 4.5 requires at least 3,686,400 pixels (approximately 1920x1920).

| Size | Ratio | Description |
|------|-------|-------------|
| `1920x1920` | 1:1 | Square (default) |
| `2048x2048` | 1:1 | HD square |
| `2560x1440` | 16:9 | Landscape widescreen |
| `1920x1080` | 16:9 | Standard landscape |
| `1440x2560` | 9:16 | Portrait (mobile screen) |
| `1080x1920` | 9:16 | Standard portrait |
| `2048x1536` | 4:3 | Landscape |
| `1536x2048` | 3:4 | Portrait |

## Parameter Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | Required | Image description text |
| `model` | string | doubao-seedream-4-5-251128 | Model name |
| `n` | int | 1 | Number of images to generate (1-4) |
| `size` | string | 1920x1920 | Image size |
| `response_format` | string | url | Return format: url or b64_json |

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
| 401 | Authentication failed | Check if API Key is correct |
| 400 | Parameter error | Check prompt and other parameter formats |
| 429 | Rate limit exceeded | Reduce request frequency |
| 500 | Server error | Retry later |

## File Structure

```
jimeng-image-router/
├── SKILL.md                  # This file
├── scripts/
│   └── image_router.py       # Unified router script
└── references/
    └── api_docs.md           # Complete API documentation
```

## Related Resources

- [Volcengine Ark Model Service Platform](https://console.volcengine.com/ark)
- [SeeDream 4.5 API Documentation](https://www.volcengine.com/docs/82379/1535980)
- [Doubao Image Model Introduction](https://www.volcengine.com/docs/6791/1298562)
