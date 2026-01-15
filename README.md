# Claude Skills Collection

A curated collection of custom skills for Claude Code, focusing on content creation, automation, AI integration, and development efficiency.

## 📂 Skills Index

### 📝 Content Creation & Publishing (内容创作与发布)
| Skill | Description |
|-------|-------------|
| **[wechat-article-writer](wechat-article-writer/)** | 🤖 **Agentic** End-to-end workflow for writing WeChat Official Account articles (Research -> Draft -> Title) |
| **[bm-md-formatter](bm-md-formatter/)** | Markdown formatting service using bm.md API for multi-platform publishing |

| **[x-article-publisher](x-article-publisher/)** | Publishes Markdown articles to X (Twitter) Articles via clipboard automation |
| **[markdown-to-twitter](markdown-to-twitter/)** | Converts Markdown articles to Twitter threads or Unicode-styled text |
| **[content-research-writer](content-research-writer/)** | AI assistant for high-quality content research and writing |
| **[wechat-title-generator](wechat-title-generator/)** | Generates high-CTR titles for WeChat articles |

### 🌐 Localization & Translation (本地化与翻译)
| Skill | Description |
|-------|-------------|
| **[article-translator](article-translator/)** | 🖼️ **Visual Retention** English-to-Chinese translator with style switching (--style vivid) |
| **[twitter-to-wechat](twitter-to-wechat/)** | Converts Twitter/X threads into WeChat Official Account articles |

### 🖼️ AI Media & Design (AI 媒体与设计)
| Skill | Description |
|-------|-------------|
| **[jimeng-image-router](jimeng-image-router/)** | Text-to-Image generation using Volcengine SeeDream 4.5 |
| **[nanobanana-router](nanobanana-router/)** | High-quality image generation using Google Gemini 3 Pro |
| **[doubao-tts-router](doubao-tts-router/)** | Text-to-Speech synthesis using Volcengine Doubao TTS 2.0 |
| **[wechat-cover-generator](wechat-cover-generator/)** | Generates cover images for WeChat Official Account articles |
| **[image-enhancer](image-enhancer/)** | Enhances image resolution, sharpness, and clarity |
| **[slack-gif-creator](slack-gif-creator/)** | Creates optimized animated GIFs for Slack |

### 📄 Document Processing (文档处理)
| Skill | Description |
|-------|-------------|
| **[docx](docx/)** | Comprehensive Word document manipulation (create, edit, analyze) |
| **[pdf](pdf/)** | PDF toolkit for extraction, creation, merging, and form handling |

### 🛠️ Development & Automation (开发与自动化)
| Skill | Description |
|-------|-------------|
| **[agent-browser](agent-browser/)** | Headless browser automation CLI for scraping and testing |
| **[changelog-generator](changelog-generator/)** | Auto-generates user-friendly release notes from git commits |
| **[research-to-diagram](research-to-diagram/)** | Researches topics and generates knowledge graph PDFs |
| **[mcp-builder](mcp-builder/)** | Guide for creating MCP servers |
| **[file-organizer](file-organizer/)** | Intelligently organizes files and folders |

## 🚀 Usage

To use these skills with Claude Code:

1. Clone this repository or copy the specific skill folder to your local skills directory:
   ```bash
   cp -r skill-name ~/.claude/skills/
   ```

2. Claude Code will automatically detect the new skills. You can verify them by asking:
   > "List my available skills"

## 🔒 Security

This repository is configured with security best practices:
- **Pre-commit hooks**: Scans for secrets, large files, and private keys before every commit.
- **GitHub Actions**: Automated security scanning on every push.
- **.gitignore**: Ensures sensitive configuration files (`.env`, `*.key`) are never tracked.
- **Safe Execution**: All scripts use environment variables for credentials (`os.environ.get`), ensuring no hardcoded secrets exist in the codebase.

## 🤝 Contributing

Contributions are welcome! Please ensure you:
1. Run `pre-commit install` to set up the security hooks.
2. Do not commit any real API keys or credentials.
3. Add a `SKILL.md` description for any new skill.

---
*Maintained by [DracoHu](https://github.com/dracohu2025-cloud)*
