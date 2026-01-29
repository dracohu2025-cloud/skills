# OpenRouter API 成本相关文档

## 概述

OpenRouter 是一个统一的 AI 模型 API 网关，支持多个提供商的模型。每次 API 调用都会返回详细的使用量和成本信息。

## API 端点

### 基础 URL

```
https://openrouter.ai/api/v1
```

### Chat Completions

```
POST /chat/completions
```

### 获取 Generation 详情

```
GET /generation?id={generation_id}
```

## 认证

使用 Bearer Token：

```
Authorization: Bearer sk-or-v1-xxx
```

## 响应中的 Usage 字段

### 启用 Usage 返回

在请求中添加：

```json
{
  "model": "google/gemini-2.0-flash-001",
  "messages": [...],
  "usage": {
    "include": true
  }
}
```

### 响应格式

```json
{
  "id": "gen-xxx",
  "model": "google/gemini-2.0-flash-001",
  "choices": [...],
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 250,
    "total_tokens": 400,
    "cost": 0.0012
  }
}
```

### Usage 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `prompt_tokens` | int | 输入 token 数（使用 GPT-4 tokenizer 标准化） |
| `completion_tokens` | int | 输出 token 数 |
| `total_tokens` | int | 总 token 数 |
| `cost` | float | 账户扣费金额（credits，约等于 USD） |

## Generation API

通过 generation ID 可获取更精确的成本信息：

### 请求

```bash
curl "https://openrouter.ai/api/v1/generation?id=gen-xxx" \
  -H "Authorization: Bearer sk-or-v1-xxx"
```

### 响应

```json
{
  "id": "gen-xxx",
  "model": "google/gemini-2.0-flash-001",
  "created_at": "2025-01-15T10:30:00Z",
  "native_tokens_prompt": 145,
  "native_tokens_completion": 248,
  "total_cost": 0.001156,
  "upstream_inference_cost": 0.0011,
  "generation_time": 1.234,
  "tokens_per_second": 201.3
}
```

### Generation 字段说明

| 字段 | 说明 |
|------|------|
| `native_tokens_prompt` | 原生 tokenizer 计算的输入 token（精确计费依据） |
| `native_tokens_completion` | 原生 tokenizer 计算的输出 token |
| `total_cost` | 总费用（USD） |
| `upstream_inference_cost` | 上游提供商实际收取的费用 |
| `generation_time` | 生成耗时（秒） |
| `tokens_per_second` | 输出速度 |

## 定价模型

### 计费方式

OpenRouter 按 token 计费，不同模型价格不同。价格以 per million tokens 为单位。

### 示例定价（2025）

| 模型 | 输入价格 | 输出价格 |
|------|----------|----------|
| google/gemini-2.0-flash-001 | $0.10/M | $0.40/M |
| anthropic/claude-3.5-sonnet | $3.00/M | $15.00/M |
| openai/gpt-4o | $2.50/M | $10.00/M |
| meta-llama/llama-3.1-70b-instruct | $0.52/M | $0.75/M |

### 费用计算

```
cost = (prompt_tokens * input_price + completion_tokens * output_price) / 1,000,000
```

### 平台费用

- 信用卡充值：5.5% 手续费（最低 $0.80）
- 加密货币充值：5% 手续费
- BYOK (自带 Key)：5% 使用费

## 流式响应中的 Usage

对于流式响应，usage 信息在最后一个 SSE 消息中返回：

```
data: {"id":"gen-xxx","choices":[{"delta":{"content":"Hello"}}]}

data: {"id":"gen-xxx","choices":[{"delta":{"content":" world"}}]}

data: {"id":"gen-xxx","choices":[],"usage":{"prompt_tokens":150,"completion_tokens":250,"cost":0.0012}}

data: