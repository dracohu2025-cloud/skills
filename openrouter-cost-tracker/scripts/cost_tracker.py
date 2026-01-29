#!/usr/bin/env python3
"""
OpenRouter 成本统计 Router

追踪、统计和分析 OpenRouter API 调用成本。
支持按模型、日期、会话等维度分析。

Usage:
    python cost_tracker.py stats --today
    python cost_tracker.py stats --by-model
    python cost_tracker.py export --format csv --output report.csv
    python cost_tracker.py call --model "google/gemini-2.0-flash-001" --prompt "Hello" --track
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
from collections import defaultdict
import functools


# ============== 配置 ==============

OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
DEFAULT_USAGE_FILE = Path.home() / ".openrouter" / "usage.jsonl"


# ============== 工具函数 ==============

def get_api_key() -> str:
    """获取 OpenRouter API Key"""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: 请设置 OPENROUTER_API_KEY 环境变量")
        print("获取 API Key: https://openrouter.ai/keys")
        sys.exit(1)
    return api_key


def get_usage_file() -> Path:
    """获取使用记录文件路径"""
    path = os.environ.get("OPENROUTER_USAGE_FILE")
    if path:
        return Path(path)
    return DEFAULT_USAGE_FILE


def ensure_usage_dir():
    """确保存储目录存在"""
    usage_file = get_usage_file()
    usage_file.parent.mkdir(parents=True, exist_ok=True)


# ============== 成本追踪器 ==============

class CostTracker:
    """OpenRouter 成本追踪器"""

    def __init__(self, usage_file: Optional[Path] = None):
        self.usage_file = usage_file or get_usage_file()
        ensure_usage_dir()

    def log_usage(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float,
        generation_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> Dict:
        """
        记录一次 API 调用的使用情况

        Args:
            model: 模型名称
            prompt_tokens: 输入 token 数
            completion_tokens: 输出 token 数
            cost: 费用（USD）
            generation_id: OpenRouter generation ID
            metadata: 额外元数据

        Returns:
            记录的数据
        """
        record = {
            "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "cost": cost,
        }

        if generation_id:
            record["id"] = generation_id

        if metadata:
            record["metadata"] = metadata

        # 追加到文件
        with open(self.usage_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        return record

    def load_records(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        model: Optional[str] = None,
    ) -> List[Dict]:
        """
        加载使用记录

        Args:
            start_date: 开始日期
            end_date: 结束日期
            model: 筛选特定模型

        Returns:
            记录列表
        """
        if not self.usage_file.exists():
            return []

        records = []
        with open(self.usage_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    ts_str = record["ts"].rstrip("Z")
                    ts = datetime.fromisoformat(ts_str).replace(tzinfo=timezone.utc)

                    # 日期过滤
                    if start_date:
                        start_aware = start_date.replace(tzinfo=timezone.utc) if start_date.tzinfo is None else start_date
                        if ts < start_aware:
                            continue
                    if end_date:
                        end_aware = end_date.replace(tzinfo=timezone.utc) if end_date.tzinfo is None else end_date
                        if ts > end_aware:
                            continue

                    # 模型过滤
                    if model and record.get("model") != model:
                        continue

                    records.append(record)
                except (json.JSONDecodeError, KeyError):
                    continue

        return records

    def summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict:
        """生成统计摘要"""
        records = self.load_records(start_date, end_date)

        if not records:
            return {
                "total_calls": 0,
                "total_tokens": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_cost": 0.0,
                "by_model": {},
            }

        by_model = defaultdict(lambda: {
            "calls": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "cost": 0.0,
        })

        total_prompt = 0
        total_completion = 0
        total_cost = 0.0

        for r in records:
            model = r.get("model", "unknown")
            prompt = r.get("prompt_tokens", 0)
            completion = r.get("completion_tokens", 0)
            cost = r.get("cost", 0.0)

            by_model[model]["calls"] += 1
            by_model[model]["prompt_tokens"] += prompt
            by_model[model]["completion_tokens"] += completion
            by_model[model]["cost"] += cost

            total_prompt += prompt
            total_completion += completion
            total_cost += cost

        return {
            "total_calls": len(records),
            "total_tokens": total_prompt + total_completion,
            "prompt_tokens": total_prompt,
            "completion_tokens": total_completion,
            "total_cost": total_cost,
            "by_model": dict(by_model),
        }

    def daily_summary(self, days: int = 7) -> List[Dict]:
        """按天统计最近 N 天"""
        now = datetime.now(timezone.utc)
        end_date = now
        start_date = now - timedelta(days=days)

        records = self.load_records(start_date, end_date)

        by_day = defaultdict(lambda: {"calls": 0, "tokens": 0, "cost": 0.0})

        for r in records:
            ts = datetime.fromisoformat(r["ts"].rstrip("Z"))
            day = ts.strftime("%Y-%m-%d")
            by_day[day]["calls"] += 1
            by_day[day]["tokens"] += r.get("total_tokens", 0)
            by_day[day]["cost"] += r.get("cost", 0.0)

        # 补全缺失的日期
        result = []
        current = start_date
        while current <= end_date:
            day = current.strftime("%Y-%m-%d")
            data = by_day.get(day, {"calls": 0, "tokens": 0, "cost": 0.0})
            result.append({"date": day, **data})
            current += timedelta(days=1)

        return result

    def export_csv(self, output_path: str, **filters):
        """导出为 CSV"""
        records = self.load_records(**filters)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("timestamp,model,prompt_tokens,completion_tokens,total_tokens,cost,generation_id\n")
            for r in records:
                f.write(f"{r.get('ts','')},{r.get('model','')},{r.get('prompt_tokens',0)},"
                       f"{r.get('completion_tokens',0)},{r.get('total_tokens',0)},"
                       f"{r.get('cost',0.0)},{r.get('id','')}\n")

        print(f"Exported {len(records)} records to {output_path}")

    def clean(self, before_date: datetime):
        """清理旧数据"""
        records = self.load_records()
        kept = []

        for r in records:
            ts = datetime.fromisoformat(r["ts"].rstrip("Z"))
            if ts >= before_date:
                kept.append(r)

        removed = len(records) - len(kept)

        # 重写文件
        with open(self.usage_file, "w", encoding="utf-8") as f:
            for r in kept:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

        print(f"Removed {removed} records before {before_date.strftime('%Y-%m-%d')}")
        print(f"Kept {len(kept)} records")


# ============== API 调用 ==============

class OpenRouterClient:
    """OpenRouter API 客户端（带成本追踪）"""

    def __init__(self, api_key: Optional[str] = None, tracker: Optional[CostTracker] = None):
        self.api_key = api_key or get_api_key()
        self.tracker = tracker or CostTracker()

    def chat_completion(
        self,
        messages: List[Dict],
        model: str = "google/gemini-2.0-flash-001",
        track: bool = True,
        **kwargs,
    ) -> Dict:
        """
        调用 chat completion API

        Args:
            messages: 消息列表
            model: 模型名称
            track: 是否记录成本
            **kwargs: 其他参数

        Returns:
            API 响应
        """
        url = f"{OPENROUTER_API_BASE}/chat/completions"

        payload = {
            "model": model,
            "messages": messages,
            **kwargs,
        }

        # 启用 usage 返回
        if "usage" not in payload:
            payload["usage"] = {"include": True}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/anthropics/claude-code",
            "X-Title": "Claude Code Cost Tracker",
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))

                # 记录成本
                if track and "usage" in result:
                    usage = result["usage"]
                    self.tracker.log_usage(
                        model=model,
                        prompt_tokens=usage.get("prompt_tokens", 0),
                        completion_tokens=usage.get("completion_tokens", 0),
                        cost=usage.get("cost", 0.0),
                        generation_id=result.get("id"),
                    )

                return result

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            raise Exception(f"API Error [{e.code}]: {error_body}")

    def get_generation(self, generation_id: str) -> Dict:
        """
        获取 generation 详情（包含精确成本）

        Args:
            generation_id: Generation ID

        Returns:
            Generation 详情
        """
        url = f"{OPENROUTER_API_BASE}/generation?id={generation_id}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            raise Exception(f"API Error [{e.code}]: {error_body}")


# ============== 装饰器和上下文管理器 ==============

def track_cost(func):
    """装饰器：自动追踪函数的 API 调用成本"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        # 尝试从结果中提取 usage
        if isinstance(result, dict) and "usage" in result:
            tracker = CostTracker()
            usage = result["usage"]
            tracker.log_usage(
                model=result.get("model", "unknown"),
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0),
                cost=usage.get("cost", 0.0),
                generation_id=result.get("id"),
            )

        return result
    return wrapper


class CostSession:
    """上下文管理器：追踪会话内的总成本"""

    def __init__(self, name: str = "session"):
        self.name = name
        self.tracker = CostTracker()
        self.start_time = None
        self.records = []
        self.total_cost = 0.0

    def __enter__(self):
        self.start_time = datetime.now(timezone.utc)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.now(timezone.utc)
        # 加载这段时间内的记录
        self.records = self.tracker.load_records(self.start_time, end_time)
        self.total_cost = sum(r.get("cost", 0.0) for r in self.records)

    def log(self, **kwargs):
        """手动记录"""
        record = self.tracker.log_usage(**kwargs)
        self.records.append(record)
        self.total_cost += record.get("cost", 0.0)


# ============== CLI ==============

def format_cost(cost: float) -> str:
    """格式化费用显示"""
    if cost < 0.01:
        return f"${cost:.6f}"
    elif cost < 1:
        return f"${cost:.4f}"
    else:
        return f"${cost:.2f}"


def format_number(n: int) -> str:
    """格式化数字（千位分隔）"""
    return f"{n:,}"


def print_summary(summary: Dict, title: str = "统计"):
    """打印统计摘要"""
    print(f"\n📊 OpenRouter 成本{title}")
    print("=" * 45)
    print(f"总调用次数: {format_number(summary['total_calls'])}")
    print(f"总 Token 数: {format_number(summary['total_tokens'])}")
    print(f"  - 输入: {format_number(summary['prompt_tokens'])}")
    print(f"  - 输出: {format_number(summary['completion_tokens'])}")
    print(f"总费用: {format_cost(summary['total_cost'])}")

    if summary["by_model"]:
        print("\n按模型分布:")
        total = summary["total_cost"] or 1
        sorted_models = sorted(
            summary["by_model"].items(),
            key=lambda x: x[1]["cost"],
            reverse=True
        )
        for model, data in sorted_models:
            pct = (data["cost"] / total) * 100 if total > 0 else 0
            print(f"  {model}: {format_cost(data['cost'])} ({pct:.1f}%)")


def print_daily_trend(daily: List[Dict]):
    """打印每日趋势"""
    print("\n📈 每日成本趋势")
    print("=" * 45)

    max_cost = max(d["cost"] for d in daily) if daily else 0

    for d in daily:
        date = d["date"]
        cost = d["cost"]
        bar_len = int((cost / max_cost) * 30) if max_cost > 0 else 0
        bar = "█" * bar_len
        print(f"{date}: {format_cost(cost):>10} {bar}")


def main():
    parser = argparse.ArgumentParser(
        description="OpenRouter 成本统计 Router",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="查看统计")
    stats_parser.add_argument("--today", action="store_true", help="今日统计")
    stats_parser.add_argument("--week", action="store_true", help="本周统计")
    stats_parser.add_argument("--month", action="store_true", help="本月统计")
    stats_parser.add_argument("--all", action="store_true", help="全部统计")
    stats_parser.add_argument("--by-model", action="store_true", help="按模型分组")
    stats_parser.add_argument("--trend", action="store_true", help="显示趋势")
    stats_parser.add_argument("--days", type=int, default=7, help="趋势天数")

    # export 命令
    export_parser = subparsers.add_parser("export", help="导出报告")
    export_parser.add_argument("--format", choices=["csv", "json"], default="csv")
    export_parser.add_argument("--output", "-o", required=True, help="输出文件")

    # query 命令
    query_parser = subparsers.add_parser("query", help="查询 generation")
    query_parser.add_argument("--id", required=True, help="Generation ID")

    # call 命令
    call_parser = subparsers.add_parser("call", help="调用 API")
    call_parser.add_argument("--model", "-m", default="google/gemini-2.0-flash-001")
    call_parser.add_argument("--prompt", "-p", required=True, help="提示词")
    call_parser.add_argument("--track", action="store_true", help="记录成本")
    call_parser.add_argument("--json", action="store_true", help="输出 JSON")

    # clean 命令
    clean_parser = subparsers.add_parser("clean", help="清理数据")
    clean_parser.add_argument("--before", required=True, help="日期 (YYYY-MM-DD)")

    # alert 命令
    alert_parser = subparsers.add_parser("alert", help="成本预警")
    alert_parser.add_argument("--daily-limit", type=float, help="日限额 (USD)")
    alert_parser.add_argument("--monthly-limit", type=float, help="月限额 (USD)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    tracker = CostTracker()

    if args.command == "stats":
        now = datetime.now(timezone.utc)

        if args.today:
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            summary = tracker.summary(start_date=start)
            print_summary(summary, f" (今日 {now.strftime('%Y-%m-%d')})")

        elif args.week:
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            summary = tracker.summary(start_date=start)
            print_summary(summary, " (本周)")

        elif args.month:
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            summary = tracker.summary(start_date=start)
            print_summary(summary, f" ({now.strftime('%Y年%m月')})")

        elif args.trend:
            daily = tracker.daily_summary(days=args.days)
            print_daily_trend(daily)

        else:
            summary = tracker.summary()
            print_summary(summary, " (全部)")

    elif args.command == "export":
        if args.format == "csv":
            tracker.export_csv(args.output)
        else:
            records = tracker.load_records()
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
            print(f"Exported {len(records)} records to {args.output}")

    elif args.command == "query":
        client = OpenRouterClient()
        try:
            result = client.get_generation(args.id)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif args.command == "call":
        client = OpenRouterClient(tracker=tracker)
        try:
            result = client.chat_completion(
                messages=[{"role": "user", "content": args.prompt}],
                model=args.model,
                track=args.track,
            )

            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                content = result["choices"][0]["message"]["content"]
                print(content)

                if args.track and "usage" in result:
                    usage = result["usage"]
                    print(f"\n--- Usage ---")
                    print(f"Tokens: {usage.get('prompt_tokens', 0)} + {usage.get('completion_tokens', 0)}")
                    print(f"Cost: {format_cost(usage.get('cost', 0.0))}")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif args.command == "clean":
        try:
            before_date = datetime.strptime(args.before, "%Y-%m-%d")
            tracker.clean(before_date)
        except ValueError:
            print("Error: 日期格式应为 YYYY-MM-DD")
            sys.exit(1)

    elif args.command == "alert":
        now = datetime.now(timezone.utc)

        if args.daily_limit:
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            summary = tracker.summary(start_date=start)
            current = summary["total_cost"]

            if current >= args.daily_limit:
                print(f"⚠️  警告: 今日成本 {format_cost(current)} 已超过限额 {format_cost(args.daily_limit)}")
                sys.exit(1)
            else:
                remaining = args.daily_limit - current
                print(f"✓ 今日成本: {format_cost(current)} / {format_cost(args.daily_limit)}")
                print(f"  剩余额度: {format_cost(remaining)}")

        if args.monthly_limit:
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            summary = tracker.summary(start_date=start)
            current = summary["total_cost"]

            if current >= args.monthly_limit:
                print(f"⚠️  警告: 本月成本 {format_cost(current)} 已超过限额 {format_cost(args.monthly_limit)}")
                sys.exit(1)
            else:
                remaining = args.monthly_limit - current
                print(f"✓ 本月成本: {format_cost(current)} / {format_cost(args.monthly_limit)}")
                print(f"  剩余额度: {format_cost(remaining)}")


if __name__ == "__main__":
    main()
