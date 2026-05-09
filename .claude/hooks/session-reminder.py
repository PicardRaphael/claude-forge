#!/usr/bin/env python3
"""Display a reminder of recent project memory at session start."""
import glob
import os
import sys
import tempfile

# Clean markers from previous session
_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)

for marker_name in [
    os.path.join(tempfile.gettempdir(), "claude-forge-learning-reminded"),
    os.path.join(_CLAUDE_DIR, ".devil-advocate-done"),
    os.path.join(_CLAUDE_DIR, ".devil-advocate-needed"),
    os.path.join(_CLAUDE_DIR, ".session-vault-queried"),
]:
    if os.path.exists(marker_name):
        try:
            os.remove(marker_name)
        except Exception:
            pass

def find_latest_memory():
    pattern = os.path.expanduser("~/.claude/projects/*/memory/MEMORY.md")
    local_pattern = ".claude/projects/*/memory/MEMORY.md"
    candidates = glob.glob(pattern) + glob.glob(local_pattern)
    if not candidates:
        return None
    candidates.sort(key=lambda f: os.path.getmtime(f), reverse=True)
    return candidates[0]

try:
    memory_file = find_latest_memory()
    if memory_file:
        with open(memory_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content:
            preview = content[:500]
            if len(content) > 500:
                preview += "\n..."
            print(f"[Session reminder] Derniere memoire projet :\n{preview}")
    sys.exit(0)
except Exception:
    sys.exit(0)
