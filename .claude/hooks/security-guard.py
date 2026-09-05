#!/usr/bin/env python3
"""Block destructive shell commands before execution.

This hook is intentionally conservative: commands that can erase work or
rewrite shared Git history require an explicit user decision.  It is a second
line of defence behind Claude Code permissions, not a substitute for them.
"""
import json
import re
import sys

def is_dangerous(cmd: str) -> str | None:
    flags = re.IGNORECASE
    patterns = [
        (
            r"\brm\b(?=[^\r\n;&|]*?(?:-[A-Za-z]*r[A-Za-z]*|--recursive))"
            r"(?=[^\r\n;&|]*?(?:-[A-Za-z]*f[A-Za-z]*|--force))[^\r\n;&|]*\s\S+",
            "suppression recursive et forcee (demande explicite requise)",
        ),
        (
            r"\bremove-item\b(?=[^\r\n;&|]*?(?:-recurse|-recursive))"
            r"(?=[^\r\n;&|]*?-force)\b",
            "Remove-Item -Recurse -Force (demande explicite requise)",
        ),
        (
            r"\bgit\b(?:\s+-C\s+\S+)*\s+branch\b[^\r\n;&|]*\s-D\b",
            "suppression de branche -d/-D (demande explicite requise)",
        ),
        (r"\bgit\b(?:\s+-C\s+\S+)*\s+push\b[^\r\n;&|]*(?:--force(?:-with-lease)?|-f)\b", "git push force"),
        (r"\bgit\b(?:\s+-C\s+\S+)*\s+push\b[^\r\n;&|]*\s--delete\b", "git push --delete"),
        (r"\bgit\b(?:\s+-C\s+\S+)*\s+push\b[^\r\n;&|]*\s(?::|\+)\S+", "git push destructive refspec"),
        (r"\bgit\b(?:\s+-C\s+\S+)*\s+reset\s+--hard\b", "git reset --hard"),
        (r"\bgit\b(?:\s+-C\s+\S+)*\s+clean\s+-[A-Za-z]*f", "git clean -f"),
        (r"\bgit\b(?:\s+-C\s+\S+)*\s+restore\b", "git restore (discard possible)"),
        (r"\bgit\b(?:\s+-C\s+\S+)*\s+checkout\s+--\s+", "git checkout -- (discard)"),
        (
            r"\bgit\b(?:\s+-C\s+\S+)*\s+config\b[^\r\n;&|]*\balias\.[\w.-]+\s+!?",
            "git alias definition (shell alias possible)",
        ),
        (r"\bgit\b\s+-c\s+alias\.[\w.-]+=[\"']?!", "temporary Git shell alias"),
    ]
    for pattern, reason in patterns:
        if re.search(pattern, cmd, flags):
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
