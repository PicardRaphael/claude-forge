#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone

METRICS_DIR = None


def _get_metrics_dir(data):
    project_dir = (
        os.environ.get("CLAUDE_PROJECT_DIR")
        or data.get("cwd")
        or os.getcwd()
    )
    return os.path.join(project_dir, ".claude", "_metrics")


def _char_count(value):
    try:
        return len(json.dumps(value, default=str))
    except Exception:
        return len(str(value))


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)
        data = json.loads(raw)
    except Exception:
        sys.exit(0)

    try:
        metrics_dir = METRICS_DIR if METRICS_DIR is not None else _get_metrics_dir(data)
        os.makedirs(metrics_dir, exist_ok=True)

        input_chars = _char_count(data.get("tool_input", {}))
        output_chars = _char_count(data.get("tool_response", ""))
        estimated_tokens = int((input_chars + output_chars) / 3.3)

        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "session_id": data.get("session_id", ""),
            "tool": data.get("tool_name", ""),
            "input_chars": input_chars,
            "output_chars": output_chars,
            "estimated_tokens": estimated_tokens,
        }

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_path = os.path.join(metrics_dir, f"{today}.jsonl")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
