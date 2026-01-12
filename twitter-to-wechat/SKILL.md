---
name: twitter-to-wechat
description: 翻译 Twitter/X 长文为公众号文章风格。自动爬取 Twitter 内容，按照用户写作风格解读翻译，保存为 .md 文件到 projects/wechat_mp/ 目录。
invocable: user
---

# Twitter 长文转公众号文章

将 Twitter/X 上的长文翻译成符合用户写作风格的公众号文章。

## 触发条件

用户请求：
- 翻译 Twitter 长文
- 转发推文到公众号
- "帮我翻译这个 Twitter"
- 提供以 `https://x.com/` 或 `https://twitter.com/` 开头的链接

## 工作流程

### Step 1: 获取 Twitter 内容

使用 Playwright 脚本爬取 Twitter 内容和图片：

```bash
python ~/.claude/skills/twitter-to-wechat/scripts/fetch_twitter.py "<用户提供的URL>" --scroll 15 --wait 8 --images
```

**注意**：
- Twitter 需要 JavaScript 渲染，WebFetch 无法直接获取
- `--scroll 15`：滚动 15 次以加载长文完整内容
- `--wait 8`：等待 8 秒让页面完全渲染
- `--images`：**重要！** 同时提取推文中的图片 URL

**图片输出格式**：
```
=== IMAGES FOUND ===
Image 1: https://pbs.twimg.com/media/xxx&name=orig
Image 2: https://pbs.twimg.com/media/yyy&name=orig
Total: 2 images
```

**注意**：图片 URL 会输出到 stderr，文本内容输出到 stdout，两者互不干扰。

### Step 2: 读取用户写作风格

**重要**：翻译前必须读取用户的写作风格参考。

读取 `projects/wechat_mp/` 目录下的参考文章：
- `The death of value-based content.md`（Dan Koe 长文解读风格）
- `How to use Antigravity tokens in Claude Code.md`（技术教程风格）
- `How to build your own PKM system with VS Code.md`（保姆级教程风格）

**写作风格要点**：

1. **开头风格**
   - 对话式引入："最近 Dan Koe 又发了一篇炸裂长文"
   - 简洁说明："这篇文章信息量超大，我用自己的理解帮大家梳理一下"

2. **结构特点**
   - YAML Frontmatter：title_candidates（5个） + selected_title
   - 分段使用 `---` 分隔符
   - 编号章节（一、二、三...）或 ## 标题
   - 用引用块 `>` 突出核心观点
   - 结尾有"我的一点感想" + "共勉"

3. **语言风格**
   - **不是逐字翻译**，是解读式重新组织
   - 短句为主，节奏快
   - 口语化表达："扎心"、"狠话"、"怼了一下"、"对，你没看错"
   - 有情绪色彩，不是冷冰冰的翻译腔

4. **标题候选风格**
   - KOL 背书 + 好奇心缺口："Dan Koe 最新长文：..."
   - 否定式 + 对比反差："不是A，不是B，而是..."
   - 痛点共鸣 + 群体认同："学校不会教你的..."
   - 数字威胁 + 悬念设置："99%的人会被..."
   - 对比手法 + 承诺结果："从X到Y，掌握..."

5. **内容组织**
   - 核心观点提炼：开篇或章节开头用粗体/引用块总结
   - 分点叙述：用列表，但不是大段堆砌
   - 加入个人见解："Dan Koe 的话："、"他的结论："

### Step 3: 翻译/解读内容

**图片处理**：
- 保留原文中的所有图片
- 将图片放在译文中的合适位置（通常在相关段落之后或作为章节开头）
- 使用 Markdown 图片语法：`![图片描述](图片URL)`
- 图片描述可以用中文简述图片内容

**内容翻译**：
按照以下结构组织译文：

```markdown
---
title_candidates:
  - title: "标题候选1"
    strategy: "策略说明"
  - title: "标题候选2"
    strategy: "策略说明"
  ...（共5个）
selected_title: ""
---

# [主标题]

> 原文来自 [作者名] 于 [日期] 发布的 X 长文
> 原文链接：[URL]

[对话式开头]

---

## 核心观点：[一句话总结]

[Dan Koe 开篇观点解读]

---

## 一、[第一部分标题]

[解读内容，用引用块突出关键句]

---

## 二、[第二部分标题]

[解读内容]

---

## 我的一点感想

[个人总结，2-3段]

---

*本文解读自 [作者] 在 X (Twitter) 的长文*
```

### Step 4: 保存文件

1. 生成文件名：使用原文核心主题的英文或拼音，如 `The-most-important-skill-for-the-next-10-years.md`

2. 保存路径：`/Volumes/ORICO/Github/Notes/projects/wechat_mp/[文件名].md`

3. 使用 Write 工具保存文件

### Step 5: 更新 index.md

将新文章链接添加到 `/Volumes/ORICO/Github/Notes/projects/wechat_mp/index.md` 文件中。

**index.md 格式**：
```markdown
- [文章标题](/projects/wechat_mp/文件名.md)
```

**操作步骤**：
1. 读取当前 index.md 内容
2. 在列表末尾添加新文章链接（注意：文件名中的空格需编码为 `%20`）
3. 使用 Edit 工具更新 index.md，在最后一个链接后添加新的一行

**示例**：
```markdown
- [Dan Koe 长文解读：未来10年最重要的能力](/projects/wechat_mp/The-most-important-skill-for-the-next-10-years.md)
```

## 标题生成策略

根据文章类型生成 5 个标题候选：

| 文章类型 | 标题示例 |
|---------|---------|
| Dan Koe/观点类 | "Dan Koe 最新长文：未来10年最重要的能力，只有一个" |
| 技术/教程类 | "Claude Code 终极玩法：用 Antigravity Token 白嫖 Opus 4.5" |
| 方法论类 | "再见 Obsidian！我用 VS Code 打造了终极笔记系统" |
| 争议/热点类 | "不是AI在取代你，是你从来没有「品味」" |

## 注意事项

1. **第三方转述视角**：始终用"Dan Koe 认为..."、"他指出..."、"他的结论是..."
2. **保留图片**：使用 `--images` 参数获取图片 URL，将图片放在译文合适位置
3. **图片语法**：`![中文描述](原始图片URL)`，图片 URL 使用 `&name=orig` 获取原图
4. **控制篇幅**：原文可能很长，需要提炼核心观点，不要逐字翻译
5. **保持语气一致**：模仿用户的语气——亲切、有观点、不啰嗦

## 图片放置建议

| 图片类型 | 建议位置 |
|---------|---------|
| 文章主图/配图 | 正文开头或"核心观点"之后 |
| 数据图表 | 对应的数据解读段落之后 |
| 代码截图 | 代码说明段落之后 |
| 多图系列 | 按原文顺序依次放置，每张图配简短说明 |

## 示例输出

参考已完成的文件：
- `projects/wechat_mp/The-most-important-skill-for-the-next-10-years.md`
- `projects/wechat_mp/The death of value-based content.md`
