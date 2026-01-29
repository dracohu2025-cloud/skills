---
name: openrouter-cost-tracker
description: OpenRouter API cost tracking and analytics tool. Automatically logs token usage and costs for each API call, generates statistical reports, helps monitor and optimize AI model usage costs. Supports analysis by model, date, session, and other dimensions.
invocable: user
---

# OpenRouter Cost Tracking Router

This skill provides cost tracking, monitoring, and analysis capabilities for OpenRouter API calls.

## Use Cases

- Track token usage and costs for each API call
- Analyze cost distribution by model
- Analyze usage trends by date/time period
- Generate cost reports (JSON/CSV/Markdown)
- Set cost alert thresholds
- Optimize model selection to reduce costs

## Prerequisites

Set the OpenRouter API Key:

```bash
export OPENROUTER_API_KEY="sk-or-v1-xxx"
```

Get API Key: [OpenRouter Keys](https://openrouter.ai/keys)

## Core Features

### 1. Cost Tracker

Automatically logs cost information for each API call:

```python
from cost_tracker import CostTracker

tracker = CostTracker()

# Log a call
tracker.log_usage(
    model="google/gemini-2.0-flash-001",
    prompt_tokens=1500,
    completion_tokens=500,
    cost=0.0025,
    generation_id="gen-xxx"
)

# View statistics
print(tracker.summary())
```

### 2. CLI Usage

```bash
# View today's statistics
python scripts/cost_tracker.py stats --today

# View monthly statistics
python scripts/cost_tracker.py stats --month

# Group statistics by model
python scripts/cost_tracker.py stats --by-model

# Export report
python scripts/cost_tracker.py export --format csv --output report.csv

# Query cost for specific generation
python scripts/cost_tracker.py query --id gen-xxx

# Set cost alerts
python scripts/cost_tracker.py alert --daily-limit 10.0

# Clean old data
python scripts/cost_tracker.py clean --before 2024-01-01
```

### 3. API Call with Cost Tracking

```bash
# Call API and automatically log cost
python scripts/cost_tracker.py call \
  --model "google/gemini-2.0-flash-001" \
  --prompt "Hello, world!" \
  --track

# Streaming call
python scripts/cost_tracker.py call \
  --model "anthropic/claude-3.5-sonnet" \
  --prompt "Write a poem" \
  --stream --track
```

## OpenRouter Cost Fields Reference

The `usage` object returned by each API call contains:

| Field | Type | Description |
|-------|------|-------------|
| `prompt_tokens` | int | Number of input tokens |
| `completion_tokens` | int | Number of output tokens |
| `total_tokens` | int | Total token count |
| `cost` | float | Account charge amount (credits) |

More detailed information available via `/api/v1/generation/{id}`:

| Field | Description |
|-------|-------------|
| `native_tokens_prompt` | Input tokens calculated by native tokenizer |
| `native_tokens_completion` | Output tokens calculated by native tokenizer |
| `total_cost` | Total cost (USD) |
| `upstream_inference_cost` | Actual cost from upstream provider |

## Data Storage

Cost data is stored by default in `~/.openrouter/usage.jsonl`:

```jsonl
{"ts":"2025-01-15T10:30:00Z","model":"google/gemini-2.0-flash-001","prompt_tokens":1500,"completion_tokens":500,"cost":0.0025,"id":"gen-xxx"}
{"ts":"2025-01-15T11:00:00Z","model":"anthropic/claude-3.5-sonnet","prompt_tokens":2000,"completion_tokens":1000,"cost":0.015,"id":"gen-yyy"}
```

## Statistics Report Examples

### Daily Statistics
```
OpenRouter Cost Statistics (2025-01-15)
=====================================
Total Calls: 45
Total Tokens: 125,000
  - Input: 85,000
  - Output: 40,000
Total Cost: $2.35

By Model:
  google/gemini-2.0-flash-001: $0.85 (36%)
  anthropic/claude-3.5-sonnet: $1.20 (51%)
  openai/gpt-4o: $0.30 (13%)
```

### Monthly Trend
```
Monthly Cost Trend
================
2025-01-01: $1.20 ████████
2025-01-02: $2.50 ████████████████
2025-01-03: $1.80 ████████████
...
```

## Integration into Existing Projects

### Decorator Method

```python
from cost_tracker import track_cost

@track_cost
def call_openrouter(prompt: str, model: str = "google/gemini-2.0-flash-001"):
    # Your API call code
    response = client.chat.completions.create(...)
    return response
```

### Context Manager

```python
from cost_tracker import CostSession

with CostSession(name="my_task") as session:
    # Multiple API calls
    response1 = call_api(...)
    response2 = call_api(...)

print(f"Session cost: ${session.total_cost:.4f}")
```

## Environment Variable Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | - | API Key (Required) |
| `OPENROUTER_USAGE_FILE` | ~/.openrouter/usage.jsonl | Data storage path |
| `OPENROUTER_DAILY_LIMIT` | - | Daily cost limit (USD) |
| `OPENROUTER_MONTHLY_LIMIT` | - | Monthly cost limit (USD) |

## File Structure

```
openrouter-cost-tracker/
├── SKILL.md                  # This file
├── scripts/
│   └── cost_tracker.py       # Core script
└── references/
    └── api_docs.md           # API documentation
```

## Related Resources

- [OpenRouter Official Website](https://openrouter.ai)
- [OpenRouter Pricing](https://openrouter.ai/docs/pricing)
- [API Documentation](https://openrouter.ai/docs)
