#!/usr/bin/env python3
"""Codex adapter for the shared ephemeral session-state reset."""

from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "session-state-reset.py"
exec(compile(_SHARED.read_text(encoding="utf-8"), str(_SHARED), "exec"), globals())
