#!/usr/bin/env python3
"""SessionStart hook: warns when memory/ accumulates too many .md files.

Trigger   : SessionStart
Thresholds: WARNING 80, CRITICAL 100 (advisory, not blocking)
Doctrine  : Cible <100 fichiers (pattern-maintenance-hybride-corpus-accumulatif
            section "Architecture cognitive — trois acteurs"). Pattern memory =
            exceptions empiriques uniquement; doctrine vit dans le vault.
Behavior  : Fail-open — any error (missing dir, IO) -> exit 0 silently.
"""
import json
import os
import sys

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)
_REPO_ROOT = os.path.dirname(_CLAUDE_DIR)
_MEMORY_DIR = os.path.join(_REPO_ROOT, "memory")

_EXCLUDED = {"MEMORY.md", "_index_archive.md"}


def count_memory_files(memory_dir: str) -> int | None:
    """Return count of .md files in memory_dir (excluding MEMORY.md, _index_archive.md).

    Returns None if the directory cannot be read (fail-open).
    """
    try:
        entries = os.listdir(memory_dir)
    except Exception:
        return None
    count = 0
    for name in entries:
        if not name.endswith(".md"):
            continue
        if name in _EXCLUDED:
            continue
        full = os.path.join(memory_dir, name)
        if os.path.isfile(full):
            count += 1
    return count


def check_memory_saturation(
    memory_dir: str,
    warning: int = 80,
    critical: int = 100,
) -> str | None:
    """Return a warning message based on count, else None.

    - count < warning   -> None
    - warning <= count < critical -> WARNING message
    - count >= critical -> CRITICAL message
    """
    count = count_memory_files(memory_dir)
    if count is None:
        return None
    if count >= critical:
        return (
            f"[memory-saturation-watcher] CRITICAL: {count} fichiers memory/ (cible <100)."
            " Lancer /clean-memory en session dediee."
            " Cf [[pattern-maintenance-hybride-corpus-accumulatif]] section Architecture cognitive."
        )
    if count >= warning:
        return (
            f"[memory-saturation-watcher] WARNING: {count} fichiers memory/ (cible <100)."
            " Planifier /clean-memory prochainement."
            " Workflow nouveau feedback: search_brain vault d'abord (rule memory-discipline)."
        )
    return None


if __name__ == "__main__":
    try:
        sys.stdin.read()
    except Exception:
        pass
    try:
        msg = check_memory_saturation(_MEMORY_DIR)
        if msg:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": msg,
                }
            }
            print(json.dumps(output))
    except Exception:
        pass
    sys.exit(0)
