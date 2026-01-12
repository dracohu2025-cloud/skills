# 即梦 SeeDream 4.5 API 完整文档

## 概述

即梦 SeeDream 4.5 是火山引擎方舟大模型服务平台提供的图像生成模型，由字节跳动/Seed 团队开发。支持文生图、图生图、多图融合等多种图像生成能力。

模型 ID: `doubao-seedream-4-5-251128`

## API 端点

### 基础 URL

```
https://ark.cn-beijing.volces.com/api/v3
```

### 图像生成端点

```
POST /images/generations
```

## 认证

使用 Bearer Token 认证：

```
Authorization: Bearer {your_api_key}
```

## 请求参数

### images/generations

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `model` | string | 是 | - | 模型名称，如 `doubao-seedream-4-5-251128` |
| `prompt` | string | 是 | - | 图片描述文本 |
| `n` | integer | 否 | 1 | 生成图片数量，范围 1-4 |
| `size` | string | 否 | 1024x1024 | 图片尺寸 |
| `response_format` | string | 否 | url | 返回格式：`url` 或 `b64_json` |
| `image` | string | 否 | - | 参考图片（base64 格式，用于图生图） |

### 支持的尺寸

| 尺寸 | 宽高比 | 说明 |
|------|--------|------|
| 1024x1024 | 1:1 | 方形（默认） |
| 1024x576 | 16:9 | 横版宽屏 |
| 576x1024 | 9:16 | 竖版（手机屏幕） |
| 1024x768 | 4:3 | 横版标准 |
| 768x1024 | 3:4 | 竖版标准 |

## 响应格式

### 成功响应

```json
{
  "created": 1704067200,
  "data": [
    {
      "url": "https://xxx.volccdn.com/xxx/image.png",
      "revised_prompt": "优化后的提示词"
    }
  ]
}
```

### 使用 b64_json 格式

```json
{
  "created": 1704067200,
  "data": [
    {
      "b64_json": "iVBORw0KGgo...",
      "revised_prompt": "优化后的提示词"
    }
  ]
}
```

### 错误响应

```json
{
  "error": {
    "code": "invalid_api_key",
    "message": "Incorrect API key provided",
    "type": "invalid_request_error"
  }
}
```

## 错误码

| HTTP 状态码 | 错误码 | 说明 |
|------------|--------|------|
| 400 | invalid_request_error | 请求参数错误 |
| 401 | invalid_api_key | API Key 无效 |
| 403 | access_denied | 无权访问该模型 |
| 429 | rate_limit_exceeded | 请求频率超限 |
| 500 | internal_error | 服务器内部错误 |

## 完整请求示例

### cURL

```bash
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SEEDREAM_API_KEY" \
  -d '{
    "model": "doubao-seedream-4-5-251128",
    "prompt": "一只可爱的橘猫在阳光下睡觉，毛发蓬松，表情满足",
    "n": 1,
    "size": "1024x1024",
    "response_format": "url"
  }'
```

### Python (volcenginesdkarkruntime)

```python
import os
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url='https://ark.cn-beijing.volces.com/api/v3',
    api_key=os.getenv('SEEDREAM_API_KEY'),
)

response = client.images.generations.create(
    model="doubao-seedream-4-5-251128",
    prompt="充满活力的特写编辑肖像，模特眼神犀利",
    n=1,
    size="1024x1024",
)

for image in response.data:
    print(f"Image URL: {image.url}")
```

### Python (OpenAI SDK 兼容)

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("SEEDREAM_API_KEY"),
)

response = client.images.generate(
    model="doubao-seedream-4-5-251128",
    prompt="赛博朋克风格的城市夜景，霓虹灯闪烁",
    n=1,
    size="1024x576",
)

print(response.data[0].url)
```

### Python (纯 HTTP)

```python
import json
import urllib.request

url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
api_key = "your_api_key"

payload = {
    "model": "doubao-seedream-4-5-251128",
    "prompt": "一幅中国山水画，意境悠远",
    "n": 1,
    "size": "1024x1024"
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
    print(result["data"][0]["url"])
```

## 高级功能

### 图生图 (Image-to-Image)

通过 `image` 参数传入参考图片：

```python
import base64

# 读取参考图片
with open("reference.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

response = client.images.generations.create(
    model="doubao-seedream-4-5-251128",
    prompt="将这张照片转换为水彩画风格",
    image=f"data:image/jpeg;base64,{image_b64}",
    size="1024x1024",
)
```

### 多图融合

SeeDream 4.5 支持多张参考图片融合：

```python
# 多张参考图片（具体格式请参考最新 API 文档）
response = client.images.generations.create(
    model="doubao-seedream-4-5-251128",
    prompt="融合这些图片的风格和元素",
    images=[
        f"data:image/png;base64,{image1_b64}",
        f"data:image/png;base64,{image2_b64}",
    ],
    size="1024x1024",
)
```

## Prompt 最佳实践

### 结构化描述

```
[主体] + [环境/场景] + [风格] + [光线] + [构图] + [技术参数]
```

### 示例

**人像摄影**:
```
充满活力的特写编辑肖像，模特眼神犀利，头戴雕塑感帽子，色彩拼接丰富，
眼部焦点锐利，景深较浅，具有Vogue杂志封面的美学风格，
采用中画幅拍摄，工作室灯光效果强烈。
```

**产品摄影**:
```
高端机械腕表产品摄影，银色表盘，精钢表壳，黑色皮革表带，
纯黑色背景，柔和的侧面照明突出金属质感，
4K超高清细节，商业广告级别品质。
```

**中国画风格**:
```
一幅传统中国山水画，远山含黛，近水微澜，
松柏苍翠，渔舟唱晚，意境悠远，
水墨风格，留白丰富，宋代院体画风格。
```

**科幻场景**:
```
赛博朋克风格的未来城市夜景，高楼林立，霓虹灯闪烁，
飞行汽车穿梭，雨后湿润的街道反射着五彩灯光，
电影级别的视觉效果，宽屏16:9构图。
```

## 限制与配额

- 单次请求最多生成 4 张图片
- 图片 URL 有效期：24 小时
- 请求超时：120 秒
- 并发限制：根据账户级别不同

## 相关资源

- [火山引擎方舟控制台](https://console.volcengine.com/ark)
- [API Key 管理](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)
- [模型列表](https://www.volcengine.com/docs/82379/1099522)
- [SeeDream 4.5 教程](https://www.volcengine.com/docs/82379/1535980)
