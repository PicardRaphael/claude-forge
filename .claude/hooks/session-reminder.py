#!/usr/bin/env python3
"""Display a reminder of recent project memory at session start."""
import glob
import os
import sys
import tempfile

# Clean learning-reminder marker from previous session
_marker = os.path.join(tempfile.gettempdir(), "claude-forge-learning-reminded")
if os.path.exists(_marker):
    try:
        os.remove(_marker)
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
