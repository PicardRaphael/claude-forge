#!/usr/bin/env python3
"""SessionStart: clear ephemeral markers without injecting memory content."""

import os
from pathlib import Path
import tempfile

_CLAUDE_DIR = Path(__file__).resolve().parents[1]
_MARKERS = [
    Path(tempfile.gettempdir()) / "claude-forge-learning-reminded",
    Path(tempfile.gettempdir()) / "claude-forge-proactivity-reminded",
    _CLAUDE_DIR / ".devil-advocate-done",
    _CLAUDE_DIR / ".devil-advocate-needed",
    _CLAUDE_DIR / ".session-vault-queried",
    _CLAUDE_DIR / ".skill-recommendations-session",
    _CLAUDE_DIR / ".vault-write-count",
]

for marker in _MARKERS:
    try:
        os.remove(marker)
    except FileNotFoundError:
        pass
    except OSError:
        pass
