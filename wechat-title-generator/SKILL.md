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

### 3. Generate Titles and Write to Frontmatter

Generate **5** title candidates for each article, write to the beginning of the article in YAML Frontmatter format:

```yaml
---
title_candidates:
  - title: "Title 1"
    strategy: "Strategy explanation"
  - title: "Title 2"
    strategy: "Strategy explanation"
  - title: "Title 3"
    strategy: "Strategy explanation"
  - title: "Title 4"
    strategy: "Strategy explanation"
  - title: "Title 5"
    strategy: "Strategy explanation"
selected_title: ""  # Fill in after user selects
---
```

**Note**: If the article already has Frontmatter, merge into existing Frontmatter; if not, create new.

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

### Output (Written to Article Frontmatter)

```yaml
---
title_candidates:
  - title: "Claude Code Users Rejoice! Use This Tool for Unlimited Free Opus 4.5 Quota"
    strategy: "Group identity + Benefit-driven"
  - title: "Antigravity + Claude Code: I Found the Ultimate Money-Saving Solution for AI Programming"
    strategy: "Combination + Personal discovery"
  - title: "Subscribed to Google One? Congrats, Claude Code is Now Free for You"
    strategy: "Conditional opening, precisely filter target readers"
  - title: "Claude Code Too Expensive? This Trick Makes Your Tokens Last Forever"
    strategy: "Pain point opening + Suspense"
  - title: "Make Competitors Work for Claude Code! Antigravity Manager God-Tier Technique"
    strategy: "Contrast + Curiosity"
selected_title: ""
---
```
