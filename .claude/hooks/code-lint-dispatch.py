#!/usr/bin/env python3
"""PostToolUse hook — dispatch lint selon la stack du fichier modifié.

Déclenché par code-dev.md (hooks inline Write|Edit|MultiEdit).
PostToolUse = feedback uniquement, jamais bloquant.
Fail-open sur toute exception.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

_HOOK_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _HOOK_DIR.parent.parent


def get_linter(ext: str) -> tuple[str, list[str]] | None:
    """Retourne (outil, args) selon l'extension, ou None si non supporté."""
    linters = {
        ".py": ("ruff", ["ruff", "check", "--select=E,F,W", "--quiet"]),
        ".ts": ("eslint", ["eslint", "--max-warnings=0", "--quiet"]),
        ".tsx": ("eslint", ["eslint", "--max-warnings=0", "--quiet"]),
        ".js": ("eslint", ["eslint", "--max-warnings=0", "--quiet"]),
        ".jsx": ("eslint", ["eslint", "--max-warnings=0", "--quiet"]),
        ".go": ("gofmt", ["gofmt", "-l"]),
        ".rs": ("cargo", ["cargo", "clippy", "--quiet", "--", "-D", "warnings"]),
    }
    return linters.get(ext)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        file_path = data.get("tool_input", {}).get("file_path", "")
        if not file_path:
            sys.exit(0)

        path = Path(file_path)
        ext = path.suffix.lower()

        linter_info = get_linter(ext)
        if not linter_info:
            sys.exit(0)

        tool_name, cmd = linter_info

        if not shutil.which(tool_name):
            sys.exit(0)

        # Go : gofmt -l retourne les fichiers non formatés (pas d'exit non-zéro)
        if tool_name == "gofmt":
            result = subprocess.run(
                cmd + [str(path)],
                capture_output=True, text=True, timeout=10
            )
            if result.stdout.strip():
                print(f"[code-lint] {path.name} non formaté — lance : gofmt -w {path.name}")
            sys.exit(0)

        # Rust : cargo clippy à la racine du projet
        if tool_name == "cargo":
            result = subprocess.run(
                cmd,
                capture_output=True, text=True, timeout=30,
                cwd=str(_REPO_ROOT)
            )
        else:
            result = subprocess.run(
                cmd + [str(path)],
                capture_output=True, text=True, timeout=10
            )

        if result.returncode != 0:
            output = (result.stdout or result.stderr or "").strip()
            print(f"[code-lint] {tool_name} → {output[:500]}")

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
