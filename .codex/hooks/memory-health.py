#!/usr/bin/env python3
"""Codex adapter for the shared temporary-memory lifecycle check."""

from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "memory-health.py"
exec(compile(_SHARED.read_text(encoding="utf-8"), str(_SHARED), "exec"), globals())
