# 豆包 TTS API 完整文档

> 官方文档：https://www.volcengine.com/docs/6561/1598757

## API 版本

火山引擎豆包 TTS 有两个 API 版本：

| 版本 | URL | 说明 |
|------|-----|------|
| **v3** | `/api/v3/tts/unidirectional` | 推荐 - 新一代接口，更简洁 |
| **v1** | `/api/v1/tts` | 兼容 - 旧版接口 |

---

## v3 API（推荐）

### API 端点

| 接口 | URL | 说明 |
|------|-----|------|
| 同步合成（流式） | `https://openspeech.bytedance.com/api/v3/tts/unidirectional` | 单向流式 HTTP |
| 异步提交 | `https://openspeech.bytedance.com/api/v3/tts/async` | 长文本异步合成 |
| 异步查询 | `https://openspeech.bytedance.com/api/v3/tts/async/query` | 查询异步任务结果 |

### 请求头

```http
Content-Type: application/json
X-Api-App-Id: {appid}
X-Api-Access-Key: {access_token}
X-Api-Resource-Id: {resource_id}
```

| 头部 | 说明 | 示例 |
|------|------|------|
| `X-Api-App-Id` | 应用 ID | `8117610877` |
| `X-Api-Access-Key` | 访问令牌 | `oP4f8vFqqr...` |
| `X-Api-Resource-Id` | 资源 ID（必填） | `seed-tts-2.0` |

### Resource ID

| 资源 ID | 说明 |
|---------|------|
| `seed-tts-1.0` | 豆包语音合成模型 1.0 |
| `seed-tts-2.0` | 豆包语音合成模型 2.0 |
| `seed-tts-1.0-concurr` | 模型 1.0 并发版 |
| `seed-icl-1.0` | 声音复刻 1.0 |
| `seed-icl-2.0` | 声音复刻 2.0 |

### 请求体格式

```json
{
    "user": {
        "uid": "user_id"
    },
    "req_params": {
        "text": "要合成的文本",
        "speaker": "zh_female_mizai_saturn_bigtts",
        "model": "seed-tts-1.1",
        "audio_params": {
            "format": "mp3",
            "sample_rate": 24000,
            "speech_rate": 0,
            "emotion": "happy",
            "loudness_rate": 0
        },
        "additions": {
            "silence_duration": 0,
            "enable_timestamp": false
        }
    }
}
```

### 参数说明

#### req_params 基础参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `text` | string | 是 | 输入文本 |
| `speaker` | string | 是 | 发音人 ID（见音色列表） |
| `model` | string | 否 | 模型版本，如 `seed-tts-1.1` 可提升音质 |

#### audio_params 音频参数

| 参数 | 类型 | 默认值 | 范围 |
|------|------|--------|------|
| `format` | string | mp3 | mp3 / wav / pcm / ogg_opus |
| `sample_rate` | int | 24000 | 8000/16000/22050/24000/32000/44100/48000 |
| `speech_rate` | int | 0 | -50~100（0=正常，100=2倍速，-50=0.5倍速） |
| `loudness_rate` | int | 0 | -50~100（音量调节） |
| `emotion` | string | - | happy/sad/angry/surprised/neutral |
| `emotion_scale` | int | 4 | 1~5（情绪强度） |
| `bit_rate` | int | - | 比特率，如 16000/32000 |

#### additions 扩展参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `silence_duration` | int | 0 | 句尾静音时长（0-30000ms） |
| `enable_timestamp` | bool | false | 返回句/字级别时间戳 |
| `enable_language_detector` | bool | false | 自动识别语种 |
| `disable_markdown_filter` | bool | false | 解析 markdown 语法 |
| `disable_emoji_filter` | bool | false | 不过滤 emoji |
| `enable_latex_tn` | bool | false | 播报 latex 公式 |
| `explicit_language` | string | - | 明确语种：zh-cn/en/ja/es-mx 等 |

### 响应格式（流式多行 JSON）

v3 API 返回**流式多行 JSON**，需要逐行解析：

```json
{"code": 0, "message": "", "data": "base64音频数据块1"}
{"code": 0, "message": "", "data": "base64音频数据块2"}
...
{"code": 20000000, "message": "ok", "data": null, "usage": {"text_words": 10}}
```

| code | 说明 |
|------|------|
| `0` | 音频数据块，`data` 字段包含 base64 编码的音频 |
| `20000000` | 合成完成（结束标记） |
| 其他 | 错误码 |

### 响应解析示例

```python
import requests
import base64
import json

response = requests.post(url, json=payload, headers=headers, stream=True)

audio_chunks = []
for line in response.iter_lines(decode_unicode=True):
    if not line.strip():
        continue
    result = json.loads(line)
    if result["code"] == 20000000:
        break  # 结束
    if result["code"] == 0 and result.get("data"):
        audio_chunks.append(base64.b64decode(result["data"]))

audio_data = b"".join(audio_chunks)
```

---

## v1 API（兼容）

### API 端点

| 接口 | URL |
|------|-----|
| 同步合成 | `https://openspeech.bytedance.com/api/v1/tts` |
| 异步提交 | `https://openspeech.bytedance.com/api/v1/tts/async` |
| 异步查询 | `https://openspeech.bytedance.com/api/v1/tts/async/query` |

### 请求头

```http
Content-Type: application/json
Authorization: Bearer;{access_token}
```

注意：`Bearer` 和 token 之间使用分号 `;` 分隔。

### 请求体格式

```json
{
    "app": {
        "appid": "your_appid",
        "token": "your_access_token",
        "cluster": "volcano_tts"
    },
    "user": {
        "uid": "user_id"
    },
    "audio": {
        "voice_type": "zh_female_mizai_saturn_bigtts",
        "encoding": "mp3",
        "speed_ratio": 1.0,
        "pitch_ratio": 1.0,
        "sample_rate": 24000
    },
    "request": {
        "reqid": "unique_request_id",
        "text": "要合成的文本",
        "operation": "query"
    }
}
```

### 响应格式

```json
{
    "code": 3000,
    "message": "Success",
    "data": "base64_encoded_audio_data"
}
```

---

## 错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 0 / 3000 | 成功 | - |
| 20000000 | 流式结束标记（v3） | 正常完成 |
| 400 | 请求参数错误 | 检查参数格式 |
| 401 | 认证失败 | 检查 appid/token |
| 403 | 权限不足 | 检查账户配额 |
| 429 | 请求过于频繁 | 降低频率 |
| 45000000 | resource_id 为空 | 添加 X-Api-Resource-Id 头 |
| 500 / 503 | 服务器错误 | 稍后重试 |

---

## 使用限制

| 限制项 | 同步接口 | 异步接口 |
|--------|----------|----------|
| 单次文本长度 | 3000 字符 | 100,000 字符 |
| QPS 限制 | 根据套餐 | 根据套餐 |
| 结果保留时间 | - | 7 天 |
| 下载链接有效期 | - | 1 小时 |

---

## 支持的语言

| 语言 | 代码 | 说明 |
|------|------|------|
| 中文 | zh | 默认，支持中英混合 |
| 英语 | en | 美式/英式 |
| 日语 | ja | - |
| 西班牙语 | es | - |
| 印尼语 | id | - |
| 葡萄牙语 | pt-br | 巴西葡萄牙语 |

---

## SSML 支持

**注意**：豆包语音合成 2.0（`uranus_bigtts` 音色）目前**不支持** SSML。

需要 SSML 的场景请使用 1.0 版本音色（`moon_bigtts` / `saturn_bigtts`）。

---

## 最佳实践

1. **推荐使用 v3 API**：更简洁的请求格式，更好的性能
2. **流式响应处理**：v3 API 需要逐行解析 JSON，收到 `code=20000000` 表示结束
3. **连接复用**：使用 `requests.Session()` 复用 TCP 连接
4. **语速转换**：v3 API 的 `speech_rate` 与 v1 的 `speed_ratio` 不同
   - v1: `speed_ratio=1.5` (1.5倍)
   - v3: `speech_rate=50` (1.5倍，公式: `(ratio-1)*100`)
5. **长文本**：超过 3000 字符时使用异步接口
6. **错误重试**：5xx 错误使用指数退避重试

---

## 相关链接

- [控制台](https://console.volcengine.com/)
- [v3 API 文档](https://www.volcengine.com/docs/6561/1598757)
- [音色列表](https://www.volcengine.com/docs/6561/1257544)
