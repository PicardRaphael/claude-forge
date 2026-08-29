#!/usr/bin/env python3
"""SessionStart: report actionable lifecycle defects in temporary memory."""

from datetime import date
import json
import os
from pathlib import Path
import sys

_MEMORY_DIR = Path(__file__).resolve().parents[2] / "memory"
_INDEX_PATH = _MEMORY_DIR / "MEMORY.md"


def _field(path: Path, name: str) -> str:
    try:
        head = path.read_text(encoding="utf-8-sig")[:2500]
    except OSError:
        return ""
    if not head.startswith("---"):
        return ""
    for line in head.split("---", 2)[1].splitlines():
        if line.lower().startswith(name.lower() + ":"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return ""


def lifecycle_issues(memory_dir: Path, *, today: date | None = None) -> tuple[list[str], list[str]]:
    missing: list[str] = []
    expired: list[str] = []
    current = today or date.today()
    try:
        projects = sorted(memory_dir.glob("project_*.md"))
    except OSError:
        return missing, expired
    for path in projects:
        raw = _field(path, "expires")
        if not raw:
            missing.append(path.name)
            continue
        try:
            if date.fromisoformat(raw[:10]) < current:
                expired.append(path.name)
        except ValueError:
            missing.append(path.name)
    return missing, expired


def warning(memory_dir: Path = _MEMORY_DIR, index_path: Path = _INDEX_PATH) -> str | None:
    missing, expired = lifecycle_issues(memory_dir)
    issues: list[str] = []
    if missing:
        issues.append(f"{len(missing)} mémoire(s) projet sans expiration valide")
    if expired:
        issues.append(f"{len(expired)} mémoire(s) projet expirée(s)")
    try:
        if index_path.stat().st_size > 16_000:
            issues.append("l'index actif dépasse 16 Ko")
    except OSError:
        pass
    if not issues:
        return None
    return "[memory-health] " + "; ".join(issues) + ". Lancer /clean-memory pour décider, sans suppression automatique."


if __name__ == "__main__":
    try:
        sys.stdin.read()
        message = warning()
        if message:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": message}}))
    except Exception:
        pass
    sys.exit(0)
