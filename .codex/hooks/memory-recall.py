#!/usr/bin/env python3
"""Codex runtime adapter for the shared Claude/Codex memory recall policy."""

from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "memory-recall.py"
exec(compile(_SHARED.read_text(encoding="utf-8"), str(_SHARED), "exec"), globals())
