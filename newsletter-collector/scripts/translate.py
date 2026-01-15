#!/usr/bin/env python3
"""
Article Translator using OpenRouter API
Translates English Markdown articles to Simplified Chinese
Uses gemini-3-flash-preview for cost-effective translation
"""

import os
import sys
import re
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
MODEL = os.getenv('TEXT_PROCESSING_MODEL', 'google/gemini-3-flash-preview')
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'

TRANSLATION_PROMPT = """你是一位资深的内容翻译专家，擅长将英文文章翻译成简体中文。

## 翻译风格要求
- **生动有趣**：使用活泼、吸引人的表达方式，避免死板翻译
- **通俗易懂**：用大白话解释专业术语，让普通读者也能看懂
- **保持原意**：忠实传达原文的核心观点和情感
- **适合微信公众号阅读**：段落适中，适合手机阅读

## 格式要求
1. 保持 Markdown 格式不变
2. **图片必须原样保留** - 所有 `![...](...)`格式的图片链接必须原封不动保留在译文中相同的位置
3. 专业术语格式：`中文翻译 (English Original)`
4. 保留原文链接 URL 不变

## 输出格式
```markdown
# [翻译后的标题]

> 原文：[Original Title](Original-URL)
> 作者：Dan Koe | 翻译：AI (gemini-3-flash)

---

[翻译后的正文，图片保留在原位置]

---
*由 Knowledge Base Pipeline 自动翻译*
```

请翻译以下文章：

---

{article_content}
"""

def translate_article(content: str) -> str:
    """Translate article using OpenRouter API"""
    
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found in environment")
    
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://github.com/knowledge_base',
        'X-Title': 'Knowledge Base Translator'
    }
    
    payload = {
        'model': MODEL,
        'messages': [
            {
                'role': 'user',
                'content': TRANSLATION_PROMPT.format(article_content=content)
            }
        ],
        'max_tokens': 16000,
        'temperature': 0.7
    }
    
    print(f"🔄 Translating with {MODEL}...")
    
    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    
    result = response.json()
    translated = result['choices'][0]['message']['content']
    
    # Extract markdown content if wrapped in code blocks
    if '```markdown' in translated:
        match = re.search(r'```markdown\n(.*?)```', translated, re.DOTALL)
        if match:
            translated = match.group(1)
    elif '```' in translated:
        match = re.search(r'```\n?(.*?)```', translated, re.DOTALL)
        if match:
            translated = match.group(1)
    
    return translated.strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: python translate.py <input_file> [output_file]")
        print("  input_file: Path to English Markdown article")
        print("  output_file: Optional. Default: ../cn/<same_filename>")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        sys.exit(1)
    
    # Default output path: ../cn/<filename>
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.parent.parent / 'cn' / input_path.name
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"📖 Reading: {input_path}")
    content = input_path.read_text(encoding='utf-8')
    
    print(f"🔤 Article size: {len(content)} characters")
    
    try:
        translated = translate_article(content)
        
        output_path.write_text(translated, encoding='utf-8')
        print(f"✅ Saved to: {output_path}")
        print(f"📝 Translated size: {len(translated)} characters")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
