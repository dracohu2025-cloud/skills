---
description: 使用 bm.md 服务进行 Markdown 排版、渲染和格式转换。支持微信公众号、知乎、掘金等多平台发布。当用户需要格式化 Markdown、转换为富文本、或准备跨平台发布时使用此 skill。
---

# bm.md Markdown Formatter

专业的 Markdown 排版和格式转换工具，支持一键生成适配多平台的富文本内容。

## 核心功能

| 功能 | 描述 | 适用场景 |
|------|------|----------|
| **Markdown 渲染** | 转换为带内联样式的 HTML | 公众号发布、富文本编辑 |
| **HTML 转 Markdown** | 逆向转换 HTML 源码 | 内容迁移、存档 |
| **纯文本提取** | 移除格式，保留文本 | 字数统计、内容分析 |
| **格式校验修复** | 自动修复 Markdown 问题 | 代码规范、格式统一 |

## 🎨 排版样式

### 视觉风格 (markdownStyle)
- `ayu-light` - 清新淡雅 | `botanical` - 自然柔和 | `newsprint` - 报纸风格
- `bauhaus` - 包豪斯 | `sketch` - 手绘素描 | `terminal` - 终端风格
- `neo-brutalism` - 新野兽派 | `professional` - 专业商务 | `retro` - 复古怀旧

### 代码主题 (codeTheme)
- 浅色: `kimbie-light`, `tokyo-night-light`, `rose-pine-dawn`
- 深色: `kimbie-dark`, `tokyo-night-dark`, `rose-pine`

### 目标平台 (platform)
- `html` - 通用网页
- `wechat` - 微信公众号 (推荐)
- `zhihu` - 知乎专栏
- `juejin` - 掘金

## 命令行使用

### 渲染 Markdown 为富文本

```bash
# 默认渲染
python3 scripts/bm_md.py render article.md

# 渲染为微信公众号格式
python3 scripts/bm_md.py render article.md --style botanical --platform wechat

# 使用深色代码主题
python3 scripts/bm_md.py render article.md --code-theme tokyo-night-dark

# 保存到文件
python3 scripts/bm_md.py render article.md -o output.html
```

### HTML 转 Markdown

```bash
python3 scripts/bm_md.py parse webpage.html
```

### 提取纯文本

```bash
python3 scripts/bm_md.py extract article.md
```

### 修复格式问题

```bash
python3 scripts/bm_md.py lint messy.md -o fixed.md
```

## 工作流示例

### 发布到微信公众号

```bash
# 1. 渲染为微信格式
python3 scripts/bm_md.py render article.md --style botanical --platform wechat > styled.html

# 2. 打开 styled.html，复制内容
# 3. 粘贴到微信公众号编辑器
```

### 跨平台发布

```bash
# 同一篇文章，生成不同平台版本
python3 scripts/bm_md.py render article.md --platform wechat > wechat.html
python3 scripts/bm_md.py render article.md --platform zhihu > zhihu.html
python3 scripts/bm_md.py render article.md --platform juejin > juejin.html
```

## Python API 使用

```python
from scripts.bm_md import render_markdown, parse_html, extract_text

# 渲染 Markdown
html = render_markdown(
    markdown="# Hello World\n\nThis is **bold**.",
    style="botanical",
    platform="wechat"
)

# HTML 转 Markdown
md = parse_html(html)

# 提取纯文本
text = extract_text(markdown)
```

## 注意事项

- 支持 GFM 语法（表格、任务列表、删除线）
- 支持数学公式：`$行内$` 和 `$$块级$$`
- 图片需为可公开访问的 URL
- 输出 HTML 已内联 CSS 样式，可直接复制使用
- API 响应时间通常 < 2 秒

## 官方文档

https://bm.md
