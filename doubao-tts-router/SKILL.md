---
name: doubao-tts-router
description: Volcengine Doubao TTS 2.0 Text-to-Speech API Router. Use this skill to call Doubao speech synthesis service to convert text to speech. Supports streaming/non-streaming synthesis, multiple voice types, speed/pitch adjustment, and long text async synthesis.
invocable: user
---

# Doubao TTS 2.0 API Router

This skill provides unified routing and invocation capabilities for Volcengine Doubao Speech Synthesis 2.0 API.

## Use Cases

- Convert text to speech (TTS)
- Generate speech content with emotions
- Long text speech synthesis (supports up to 100,000 characters)
- Real-time streaming speech synthesis
- High-quality Chinese/English/Japanese/Spanish voice output

## Prerequisites

Before using, obtain the following credentials from Volcengine Console:

1. **APPID**: Application identifier (from Volcengine Console)
2. **ACCESS_TOKEN**: Access token (from Volcengine Console)

Steps to obtain credentials:
1. Log in to [Volcengine Console](https://console.volcengine.com/)
2. Navigate to "Doubao Voice" product
3. Create an application to get APPID
4. Generate Access Token

## Environment Variable Configuration

```bash
export DOUBAO_TTS_APPID="your_appid"
export DOUBAO_TTS_ACCESS_TOKEN="your_access_token"
```

## API Invocation Methods

### 1. Using Router Script (Recommended)

Router script provides a unified interface with automatic authentication and request handling:

```bash
# Basic usage - text to speech
python scripts/tts_router.py --text "Hello, welcome to Doubao speech synthesis" --output output.mp3

# Specify voice type
python scripts/tts_router.py --text "This is a test" --voice "zh_female_shuangkuaisisi_moon_bigtts" --output test.mp3

# Adjust speed and pitch
python scripts/tts_router.py --text "Faster speech example" --speed 1.5 --pitch 1.2 --output fast.mp3

# Streaming output
python scripts/tts_router.py --text "Streaming speech synthesis" --stream --output stream.mp3

# Long text async synthesis (read from file)
python scripts/tts_router.py --file long_text.txt --async-mode --output long.mp3
```

### 2. Direct API Call

#### HTTP Request Example

```python
import requests
import os

def synthesize_speech(text: str, voice_type: str = "zh_female_shuangkuaisisi_moon_bigtts"):
    """Call Doubao TTS 2.0 API to synthesize speech"""

    url = "https://openspeech.bytedance.com/api/v1/tts"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer;{os.environ['DOUBAO_TTS_ACCESS_TOKEN']}"
    }

    payload = {
        "app": {
            "appid": os.environ["DOUBAO_TTS_APPID"],
            "token": os.environ["DOUBAO_TTS_ACCESS_TOKEN"],
            "cluster": "volcano_tts"
        },
        "user": {
            "uid": "default_user"
        },
        "audio": {
            "voice_type": voice_type,
            "encoding": "mp3",
            "speed_ratio": 1.0,
            "pitch_ratio": 1.0
        },
        "request": {
            "reqid": "unique_request_id",
            "text": text,
            "operation": "query"
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.content
```

## Supported Voice Types

### Chinese Voices (Partial)
| Voice ID | Description |
|----------|-------------|
| `zh_female_shuangkuaisisi_moon_bigtts` | Female - Energetic Sisi |
| `zh_male_aojiaobazong_moon_bigtts` | Male - Arrogant Boss |
| `zh_female_wanwanxiaohe_moon_bigtts` | Female - Taiwanese Xiaohe |
| `zh_male_yangguangqingnian_moon_bigtts` | Male - Sunny Youth |

See `references/voice_types.md` for the complete voice list.

## Parameter Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | Required | Text content to synthesize |
| `voice_type` | string | Default voice | Voice type |
| `speed_ratio` | float | 1.0 | Speed, range 0.5-2.0 |
| `pitch_ratio` | float | 1.0 | Pitch, range 0.1-3.0 |
| `encoding` | string | "mp3" | Output format: mp3/pcm/ogg_opus |
| `sample_rate` | int | 24000 | Sample rate: 8000/16000/24000/48000 |

## Error Handling

Common error codes:

| Error Code | Description | Solution |
|------------|-------------|----------|
| 401 | Authentication failed | Check APPID and ACCESS_TOKEN |
| 429 | Rate limit exceeded | Reduce request frequency or upgrade plan |
| 500 | Server error | Retry later |

## File Structure

```
doubao-tts-router/
├── SKILL.md              # This file
├── scripts/
│   └── tts_router.py     # Unified router script
└── references/
    ├── api_docs.md       # Complete API documentation
    └── voice_types.md    # Voice type list
```

## Related Resources

- [Volcengine Doubao Voice Official Documentation](https://www.volcengine.com/docs/6561/1257543)
- [Doubao Speech Synthesis 2.0 Capabilities](https://www.volcengine.com/docs/6561/1329503)
- [Console](https://console.volcengine.com/)
