# Nano Banana Pro API 完整文档 (OpenRouter)

## 概述

Nano Banana Pro 是 Google Gemini 3 Pro 系列的图像生成模型，专为专业级图像生成和编辑任务优化。

本文档描述通过 **OpenRouter** 调用该模型的方式，相比直接调用 Google API，OpenRouter 提供：
- 详细的费用信息
- 统一的 API 格式
- 更简单的认证方式

## 模型信息

| 属性 | 值 |
|------|---|
| OpenRouter 模型 ID | `google/gemini-3-pro-image-preview` |
| Flash 版本 | `google/gemini-2.5-flash-preview-image` |
| 输入价格 | $1.25 / 1M tokens |
| 输出价格 | $10.00 / 1M tokens |
| 上下文长度 | 1M tokens |

## API 端点

### 基础 URL

```
https://openrouter.ai/api/v1
```

### Chat Completions 端点

```
POST /chat/completions
```

完整 URL：
```
https://openrouter.ai/api/v1/chat/completions
```

## 认证

使用 Bearer Token 认证：

```
Authorization: Bearer {your_openrouter_api_key}
```

## 请求参数

### chat/completions

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型名称，如 `google/gemini-3-pro-image-preview` |
| `messages` | array | 是 | 消息数组 |
| `modalities` | array | 是 | **必须包含 `["image", "text"]`** 才能生成图片 |
| `max_tokens` | integer | 否 | 最大输出 token 数 |
| `temperature` | float | 否 | 温度参数 |

### messages 格式

```json
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "Generate an image: ..."
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "data:image/jpeg;base64,..."
      }
    }
  ]
}
```

### 支持的宽高比

在 prompt 中指定，模型会尝试遵循：
- `1:1` - 方形
- `2:3` / `3:2` - 竖版/横版
- `3:4` / `4:3` - 竖版/横版
- `4:5` / `5:4` - 竖版/横版
- `9:16` / `16:9` - 手机竖屏/宽屏
- `21:9` - 超宽屏

### 支持的图片尺寸

在 prompt 中指定：
- `1K` - 约 1024px（默认）
- `2K` - 约 2048px
- `4K` - 约 4096px

## 响应格式

### 成功响应

```json
{
  "id": "gen-xxxxx",
  "provider": "Google",
  "object": "chat.completion",
  "created": 1704067200,
  "model": "google/gemini-3-pro-image-preview",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "",
        "reasoning": "...",
        "images": [
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/png;base64,iVBORw0KGgo..."
            },
            "index": 0
          }
        ]
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 1400,
    "total_tokens": 1500
  }
}
```

**重要说明**：
- 图片数据位于 `choices[0].message.images` 数组中
- 每个图片对象包含 `type: "image_url"` 和 `image_url.url` 字段
- `image_url.url` 是 base64 编码的 data URL（如 `data:image/png;base64,...`）
- `content` 字段通常为空字符串，模型的推理过程在 `reasoning` 字段中

### 错误响应

```json
{
  "error": {
    "code": 400,
    "message": "Invalid request",
    "type": "invalid_request_error"
  }
}
```

## 错误码

| HTTP 状态码 | 说明 |
|------------|------|
| 400 | 请求参数错误 |
| 401 | API Key 无效 |
| 402 | 账户余额不足 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |
| 502 | 上游服务错误（Google API） |

## 完整请求示例

### cURL - 文生图

```bash
curl -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "HTTP-Referer: https://your-app.com" \
  -d '{
    "model": "google/gemini-3-pro-image-preview",
    "modalities": ["image", "text"],
    "messages": [
      {
        "role": "user",
        "content": "Generate an image based on the following description.\n\nAspect Ratio: 1:1\nImage Size: 2K\n\nDescription: A cute orange cat sleeping in warm sunlight, fluffy fur, peaceful expression"
      }
    ],
    "max_tokens": 4096
  }'
```

### cURL - 图生图

```bash
# 先将图片转为 base64
IMAGE_B64=$(base64 -i input.jpg)

curl -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d "{
    \"model\": \"google/gemini-3-pro-image-preview\",
    \"modalities\": [\"image\", \"text\"],
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": [
          {
            \"type\": \"image_url\",
            \"image_url\": {
              \"url\": \"data:image/jpeg;base64,$IMAGE_B64\"
            }
          },
          {
            \"type\": \"text\",
            \"text\": \"Transform this image into watercolor painting style\"
          }
        ]
      }
    ],
    \"max_tokens\": 4096
  }"
```

### Python (纯 HTTP)

```python
import json
import base64
import urllib.request
import os

api_key = os.environ.get("OPENROUTER_API_KEY")
url = "https://openrouter.ai/api/v1/chat/completions"

# 构建 prompt
prompt = """Generate an image based on the following description.

Aspect Ratio: 16:9
Image Size: 2K

Description: A cyberpunk city at night with neon lights"""

payload = {
    "model": "google/gemini-3-pro-image-preview",
    "modalities": ["image", "text"],  # 必须指定才能生成图片
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "max_tokens": 4096
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://your-app.com"
    },
    method="POST"
)

with urllib.request.urlopen(req, timeout=300) as response:
    result = json.loads(response.read())

    # 打印 usage 信息
    usage = result.get("usage", {})
    print(f"Prompt Tokens: {usage.get('prompt_tokens')}")
    print(f"Completion Tokens: {usage.get('completion_tokens')}")
    print(f"Total Tokens: {usage.get('total_tokens')}")

    # 提取图片 - 图片在 message.images 数组中
    choices = result.get("choices", [])
    for choice in choices:
        message = choice.get("message", {})
        images = message.get("images", [])
        for i, img in enumerate(images):
            if img.get("type") == "image_url":
                url = img["image_url"]["url"]
                if url.startswith("data:"):
                    # 解析 data URL
                    header, data = url.split(",", 1)
                    image_bytes = base64.b64decode(data)
                    with open(f"output_{i}.png", "wb") as f:
                        f.write(image_bytes)
                    print(f"Image saved to output_{i}.png")
```

### Python (openai SDK)

```python
from openai import OpenAI
import os
import base64

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

response = client.chat.completions.create(
    model="google/gemini-3-pro-image-preview",
    messages=[
        {
            "role": "user",
            "content": "Generate an image: A cute cat sleeping in sunlight"
        }
    ],
    max_tokens=4096,
    extra_body={"modalities": ["image", "text"]}  # 必须指定才能生成图片
)

# 图片在 response.choices[0].message.images 中
message = response.choices[0].message
if hasattr(message, 'images') and message.images:
    for i, img in enumerate(message.images):
        url = img.image_url.url
        if url.startswith("data:"):
            header, data = url.split(",", 1)
            image_bytes = base64.b64decode(data)
            with open(f"output_{i}.png", "wb") as f:
                f.write(image_bytes)

print(f"Usage: {response.usage}")
```

## 高级功能

### 图生图 (Image-to-Image)

通过在 messages 中添加图片实现：

```python
import base64

# 读取并编码图片
with open("reference.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

payload = {
    "model": "google/gemini-3-pro-image-preview",
    "modalities": ["image", "text"],  # 必须指定
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_b64}"
                    }
                },
                {
                    "type": "text",
                    "text": "Transform this image into watercolor painting style"
                }
            ]
        }
    ],
    "max_tokens": 4096
}
```

### 多图融合

支持多张参考图片：

```python
payload = {
    "model": "google/gemini-3-pro-image-preview",
    "modalities": ["image", "text"],  # 必须指定
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image1_b64}"}},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image2_b64}"}},
                {"type": "text", "text": "Blend these images together into a new composition"}
            ]
        }
    ],
    "max_tokens": 4096
}
```

## 模型对比

| 特性 | Nano Banana Pro | Nano Banana |
|------|-----------------|-------------|
| OpenRouter ID | google/gemini-3-pro-image-preview | google/gemini-2.5-flash-preview-image |
| 定位 | 专业级生产 | 快速高效 |
| 文字渲染 | ~94% 准确率 | 一般 |
| 最大参考图 | 14 张 | 较少 |
| 输出尺寸 | 1K/2K/4K | 1K/2K |
| 输入价格 | $1.25/1M | 更便宜 |
| 输出价格 | $10.00/1M | 更便宜 |

## 费用计算

OpenRouter 按 token 计费，每次请求的 usage 字段包含：

```json
{
  "usage": {
    "prompt_tokens": 100,      // 输入 token
    "completion_tokens": 500,  // 输出 token（包括图片数据）
    "total_tokens": 600
  }
}
```

**费用计算公式**:
```
费用 = (prompt_tokens × 1.25 + completion_tokens × 10) / 1,000,000
```

**示例**:
- 输入 100 tokens，输出 500 tokens
- 费用 = (100 × 1.25 + 500 × 10) / 1,000,000 = $0.005125

## 最佳实践

### Prompt 结构

```
Generate an image based on the following description.

Aspect Ratio: {ratio}
Image Size: {size}

Description: {detailed_description}

Please generate a high-quality image matching this description.
```

### 示例 Prompt

**人像摄影**:
```
Generate an image based on the following description.

Aspect Ratio: 3:4
Image Size: 2K

Description: A vibrant close-up editorial portrait, model with sharp gaze,
wearing sculptural hat, rich color blocking, sharp eye focus,
shallow depth of field, Vogue cover aesthetic,
medium format, strong studio lighting.
```

**产品摄影**:
```
Generate an image based on the following description.

Aspect Ratio: 1:1
Image Size: 4K

Description: Luxury mechanical watch product photography,
silver dial, steel case, black leather strap,
pure black background, soft side lighting highlighting metal texture,
4K ultra-high definition details, commercial advertising quality.
```

## 限制与配额

- 单次请求最多处理 14 张参考图片
- 请求超时：300 秒
- 并发限制：根据 OpenRouter 账户级别

## 相关资源

- [OpenRouter](https://openrouter.ai/)
- [OpenRouter API 文档](https://openrouter.ai/docs)
- [Gemini 3 Pro Image 模型页面](https://openrouter.ai/google/gemini-3-pro-image-preview)
- [API Key 管理](https://openrouter.ai/keys)
- [使用量和账单](https://openrouter.ai/activity)
