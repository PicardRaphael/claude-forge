#!/usr/bin/env python3
import json
import re
import sys

_GIT_COMMIT_RE = re.compile(r"\bgit\b(?:\s+-\S+(?:\s+\S+)?)*\s+commit\b")
_MSG_FLAG_HERESTRING_RE = re.compile(r"(?:-m|--message|-am|-cm)\s*@['\"]")

_MESSAGE = (
    "BLOQUE : here-string PowerShell (@'...'@) dans un git commit via le tool Bash. "
    "Bash ne connait pas les here-strings PowerShell -> le @ est injecte en tete du sujet. "
    "Utilise des -m repetes : git commit -m \"titre\" -m \"corps\" -m \"Co-Authored-By...\". "
    "Cf feedback_commit_message_no_herestring_bash_tool."
)


def is_blocked(command: str) -> bool:
    if not command:
        return False
    if not _GIT_COMMIT_RE.search(command):
        return False
    return bool(_MSG_FLAG_HERESTRING_RE.search(command))


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    try:
        command = data.get("tool_input", {}).get("command", "")
        if is_blocked(command):
            print(_MESSAGE, file=sys.stderr)
            sys.exit(2)
        sys.exit(0)
    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
