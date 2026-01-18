---
name: wechat-title-generator
description: Generates high-click-rate title candidates for WeChat Official Account articles.
invocable: user
---

# WeChat Official Account Title Generator

Generates high-click-rate title candidates for WeChat Official Account articles.

## Use Cases

Use this skill when users need titles for Official Account articles. Trigger keywords:
- "Generate WeChat title"
- "Create a title"
- "Article title"
- "Viral title"

## Workflow

### 1. Analyze Article Content

Read the article and extract:
- **Core Value**: What will readers gain?
- **Target Audience**: Who would be interested in this article?
- **Emotional Tone**: Technical insights/money-saving tips/opinion piece/tutorial guide
- **Keywords**: Tools, technologies, concepts mentioned in the article

### 2. Choose Title Strategy

Select 2-3 strategy combinations based on article type:

| Strategy | Use Case | Example |
|----------|----------|---------|
| **Benefit-Driven** | Saving money, efficiency, solving pain points | "Save $300/month..." |
| **Curiosity** | Novel approaches, counterintuitive | "Why programmers are all..." |
| **Specific Numbers** | Tutorials, lists, comparisons | "5 minutes to master...", "3 tools..." |
| **Negative Form** | Breaking perceptions, creating conflict | "Stop using XX!" |
| **Group Identity** | Circle culture, identity labels | "Essential for programmers...", "XX users rejoice" |
| **Personal Experience** | Real stories, pitfall sharing | "After 3 years, I finally..." |
| **Suspense** | Methodologies, clever tricks | "This trick lets you..." |
| **Contrast** | Tool comparison, solution upgrade | "Goodbye XX, I choose..." |

### 3. Generate Titles and Write to Markdown

Generate **5** title candidates for each article, write to the beginning of the article in a Markdown Callout block format:

```markdown
> [!abstract] 微信公众号标题候选 (WeChat Title Candidates)
> - **标题 1**: "Title 1" (策略: Strategy explanation)
> - **标题 2**: "Title 2" (策略: Strategy explanation)
> - **标题 3**: "Title 3" (策略: Strategy explanation)
> - **标题 4**: "Title 4" (策略: Strategy explanation)
> - **标题 5**: "Title 5" (策略: Strategy explanation)
> 
> **已选标题**: 
```

**Note**: Always insert this block at the very top of the Markdown file, above any other content. If there's an existing candidate block, replace it.

## Title Formula Templates

### Technical Tutorial Type
```
- Master [technical problem] in [number] minutes, [result]
- [Tool name] beginner guide: From zero to [achievement]
- Step-by-step [action], must-read for [target audience]
```

### Tool Recommendation Type
```
- [Pain point]? This [tool type] lets you [solution]
- Must-install for [target audience]! [number] [tool type] recommendations
- After using [tool], I never want to [old approach] again
```

### Money-Saving/Efficiency Type
```
- Save [amount] every month! The right way to [method]
- [Product] too expensive? This method gives you [savings result]
- Free [resource]! Exclusive perk for [condition] users
```

### Opinion/Experience Type
```
- Why is [group] all [behavior]? [reason/answer]
- [Time period] of [experience], I summarized [number] lessons
- Goodbye [old approach], why I chose [new approach]
```

## Title Optimization Principles

1. **Character Count**: Under 22 characters is best, max 30 characters
2. **First 8 Characters Golden Zone**: Put core info at the beginning
3. **Avoid Clickbait**: Content must deliver on title promise
4. **Conversational Tone**: Like chatting with a friend, not formal writing
5. **Emotional Words Accent**: Rejoice, finally, game-changer, clever trick (use moderately)

## Example

### Input Article Topic
> Using Antigravity Manager to reverse proxy Antigravity tokens for Claude Code use

### Output (Written to Article Top)

```markdown
> [!abstract] 微信公众号标题候选 (WeChat Title Candidates)
> - **标题 1**: "Claude Code 用户福音！一招解锁免费 Opus 4.5 额度" (策略: Group identity + Benefit-driven)
> - **标题 2**: "Antigravity + Claude Code：我找到了 AI 编程的终极省钱方案" (策略: Combination + Personal discovery)
> - **标题 3**: "订阅了 Google One？恭喜，你的 Claude Code 已经免费了" (策略: Conditional opening, precisely filter target readers)
> - **标题 4**: "Claude Code 流量不够用？这个黑科技让你的 Token 翻倍" (策略: Pain point opening + Suspense)
> - **标题 5**: "让竞品为 Claude Code 打工！Antigravity Manager 神级配置教程" (策略: Contrast + Curiosity)
> 
> **已选标题**: 
```
