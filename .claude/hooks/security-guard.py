#!/usr/bin/env python3
"""Block dangerous shell commands before execution."""
import json
import re
import sys

def is_dangerous(cmd):
    patterns = [
        (r"rm\s+-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*\s+\S", "rm -rf (toute cible — demande explicite requise)"),
        (r"rm\s+-[a-zA-Z]*f[a-zA-Z]*r[a-zA-Z]*\s+\S", "rm -fr (toute cible — demande explicite requise)"),
        (r"git\s+branch\s+(?:-[a-zA-Z-]+\s+)*-D\b", "git branch -D (demande explicite requise)"),
        (r"git\s+push\s+.*--force", "git push --force"),
        (r"git\s+push\s+.*-f\b", "git push -f"),
        (r"git\s+reset\s+--hard(?!\s+\w)", "git reset --hard without target"),
        (r"git\s+clean\s+-[a-zA-Z]*f", "git clean -f"),
    ]
    for pattern, reason in patterns:
        if re.search(pattern, cmd):
            return reason
    return None

def main() -> None:
    try:
        data = json.load(sys.stdin)
        command = data.get("tool_input", {}).get("command", "")
        reason = is_dangerous(command)
        if reason:
            print(f"BLOCKED: {reason}", file=sys.stderr)
            sys.exit(2)
        sys.exit(0)
    except Exception as exc:
        # Hook sécurité : fail-CLOSED — un payload illisible ne doit pas laisser passer une commande destructrice.
        print(f"BLOCKED: security-guard payload error ({type(exc).__name__})", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
