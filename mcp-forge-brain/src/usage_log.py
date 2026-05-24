"""Lightweight usage logging for MCP tool calls.

Appends one JSON line per call to logs/usage.jsonl.
Format: {"ts": ISO, "tool": str, "args": {...}, "duration_ms": int, "result_chars": int, "error": str|null}
"""

import functools
import json
import time
from datetime import datetime, timezone
from pathlib import Path

_LOG_PATH: Path | None = None
_DISABLED = False


def configure(log_dir: Path):
    """Set log directory (called once at server startup)."""
    global _LOG_PATH
    log_dir.mkdir(parents=True, exist_ok=True)
    _LOG_PATH = log_dir / "usage.jsonl"


def disable():
    """Disable logging (used in tests)."""
    global _DISABLED
    _DISABLED = True


def enable():
    global _DISABLED
    _DISABLED = False


def _redact_arg(value):
    """Truncate large string args to keep log file small."""
    if isinstance(value, str) and len(value) > 200:
        return value[:200] + f"...[truncated {len(value)} chars]"
    return value


def log_call(tool_name: str):
    """Decorator: log each call with timing + result size + error.

    Wraps both sync and async tools. Errors logged but not swallowed.
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if _DISABLED or _LOG_PATH is None:
                return fn(*args, **kwargs)
            start = time.perf_counter()
            error = None
            result = None
            try:
                result = fn(*args, **kwargs)
                return result
            except Exception as e:
                error = f"{type(e).__name__}: {e}"
                raise
            finally:
                duration_ms = int((time.perf_counter() - start) * 1000)
                entry = {
                    "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "tool": tool_name,
                    "args": {k: _redact_arg(v) for k, v in kwargs.items()},
                    "duration_ms": duration_ms,
                    "result_chars": len(result) if isinstance(result, str) else 0,
                    "error": error,
                }
                try:
                    with open(_LOG_PATH, "a", encoding="utf-8") as f:
                        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                except OSError:
                    pass  # never break the tool because of logging
        return wrapper
    return decorator


def stats(days: int = 7) -> dict:
    """Aggregate usage stats from log file (last N days).

    Returns: {tool: {calls, total_ms, errors, avg_result_chars}}
    """
    if _LOG_PATH is None or not _LOG_PATH.exists():
        return {}
    from collections import defaultdict
    counts = defaultdict(lambda: {"calls": 0, "total_ms": 0, "errors": 0, "result_chars_sum": 0})
    cutoff = time.time() - days * 86400
    with open(_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                ts = datetime.fromisoformat(entry["ts"]).timestamp()
                if ts < cutoff:
                    continue
                t = entry["tool"]
                counts[t]["calls"] += 1
                counts[t]["total_ms"] += entry.get("duration_ms", 0)
                if entry.get("error"):
                    counts[t]["errors"] += 1
                counts[t]["result_chars_sum"] += entry.get("result_chars", 0)
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    result = {}
    for tool, s in counts.items():
        result[tool] = {
            "calls": s["calls"],
            "total_ms": s["total_ms"],
            "errors": s["errors"],
            "avg_result_chars": s["result_chars_sum"] // s["calls"] if s["calls"] else 0,
        }
    return result
