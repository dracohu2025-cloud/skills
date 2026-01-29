---
name: mindmap-generator
description: Converts a long-form article into a hierarchical markdown list suitable for visualization as a Mind Map (Markmap).
---

# Mind Map Generator Skill

## Purpose

To distill complex articles into structured, visualizable mind maps using the Markmap (Markdown Map) format.

## Dependencies

- `jq` (optional, for processing)
- An LLM API (e.g., Gemini via OpenRouter)

## Workflow

### 1. Input

A markdown file containing the article content.

### 2. Prompt Strategy

The LLM should be prompted to:

1.  Identify the central theme (Root Node).
2.  Extract 3-5 key pillars/arguments (Level 2 Nodes).
3.  Expand each pillar with supporting details (Level 3+ Nodes).
4.  Output **pure Markdown** with correct indentation.

**Prompt Template**:

```markdown
You are an expert at structural analysis and mind mapping.
Your task is to convert the following article into a Markdown Mind Map format compatible with markmap.js.

Rules:

1. The root node should be the Article Title (e.g., `# Title`).
2. Main sections should be `## Section`.
3. Sub-points should be bullet points `- Sub-point`.
4. Keep text concise (keywords or short phrases).
5. Do NOT use code blocks. Output raw markdown.
6. Do NOT include any intro or outro text.

Article Content:
{{article_content}}
```

### 3. Usage (Script)

See `scripts/batch_mindmap.py` in the knowledge base repository for the batch implementation.
