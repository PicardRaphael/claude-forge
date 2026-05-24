"""Tests usage_log decorator + stats aggregation."""

import json
from pathlib import Path

import pytest

from src import usage_log


@pytest.fixture
def tmp_log(tmp_path):
    usage_log.configure(tmp_path / "logs")
    usage_log.enable()
    yield tmp_path / "logs" / "usage.jsonl"
    usage_log.disable()


def test_log_call_records_success(tmp_log):
    @usage_log.log_call("test_tool")
    def fn(x: int) -> str:
        return "ok" * x

    result = fn(x=5)
    assert result == "okokokokok"
    assert tmp_log.exists()
    line = tmp_log.read_text(encoding="utf-8").strip()
    entry = json.loads(line)
    assert entry["tool"] == "test_tool"
    assert entry["args"] == {"x": 5}
    assert entry["result_chars"] == 10
    assert entry["error"] is None


def test_log_call_records_error(tmp_log):
    @usage_log.log_call("failing_tool")
    def fn():
        raise ValueError("boom")

    with pytest.raises(ValueError):
        fn()
    line = tmp_log.read_text(encoding="utf-8").strip()
    entry = json.loads(line)
    assert entry["tool"] == "failing_tool"
    assert "boom" in entry["error"]


def test_log_call_truncates_large_args(tmp_log):
    @usage_log.log_call("big_arg")
    def fn(content: str):
        return "ok"

    fn(content="x" * 500)
    entry = json.loads(tmp_log.read_text(encoding="utf-8").strip())
    assert "truncated 500 chars" in entry["args"]["content"]


def test_stats_aggregation(tmp_log):
    @usage_log.log_call("a")
    def a():
        return "x"

    @usage_log.log_call("b")
    def b():
        return "yyy"

    for _ in range(3):
        a()
    b()

    stats = usage_log.stats(days=1)
    assert stats["a"]["calls"] == 3
    assert stats["b"]["calls"] == 1
    assert stats["a"]["avg_result_chars"] == 1
    assert stats["b"]["avg_result_chars"] == 3
    assert stats["a"]["errors"] == 0
