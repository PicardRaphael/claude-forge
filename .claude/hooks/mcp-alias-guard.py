#!/usr/bin/env python3
"""Block ambiguous-stem writes via MCP forge-brain append_note.

Scope: PreToolUse on mcp__forge-brain__append_note ONLY.

Problem: append_note(file="log") resolves by FTS alias and can match the WRONG
file when several notes share the same stem (log.md, index.md, CHANGELOG.md
exist in multiple vault folders). Observed 4 times in one day (27 May 2026);
text feedback proved insufficient — this is the structural guard.

Logic: if tool_input.file is a bare stem (no path separator) and more than one
vault file shares that stem, the resolution is ambiguous → exit 2. The fix is to
pass the exact path (vault/claude-forge/<dir>/<file>.md) or a unique frontmatter
alias, or to Read+Edit the exact file directly (vault edits are not hook-blocked).

A file argument containing a path separator (/) is treated as an exact path →
allowed. A stem unique in the vault → allowed.

Exit 2 blocks. Fail-open (exit 0) on any parse error or if the vault can't be
scanned.

Reactivation trigger: if a similar misresolution is ever observed on
insert_section or update_note, extend the settings.json matcher to include them
(the stem-uniqueness logic below is tool-agnostic).
"""
import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Repo root = parent of .claude/hooks/ (robust to cwd, never os.environ)
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VAULT_ROOT = _REPO_ROOT / "vault" / "claude-forge"

LOG_PATH = Path(tempfile.gettempdir()) / "mcp-alias-guard-debug.log"


def debug_log(msg: str) -> None:
    """Append timestamped message to debug log. Fail silently."""
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    except Exception:
        pass


def is_bare_stem(file_arg: str) -> bool:
    """True if file_arg is a bare alias/stem (no path separator)."""
    return "/" not in file_arg and "\\" not in file_arg


def stem_of(file_arg: str) -> str:
    """Return the stem (basename without .md extension), lowercased."""
    base = file_arg.replace("\\", "/").rsplit("/", 1)[-1]
    if base.lower().endswith(".md"):
        base = base[:-3]
    return base.lower()


def count_vault_files_with_stem(stem: str, vault_root: Path = VAULT_ROOT) -> int:
    """Count .md files in the vault whose filename stem matches (case-insensitive)."""
    if not vault_root.exists():
        return 0
    count = 0
    for p in vault_root.rglob("*.md"):
        if p.stem.lower() == stem:
            count += 1
    return count


def is_ambiguous(file_arg: str, vault_root: Path = VAULT_ROOT) -> bool:
    """True if file_arg is a bare stem matching >1 vault file (ambiguous resolution).

    An exact path (with separator) is never ambiguous. A stem unique or absent in
    the vault is not ambiguous (absent → append_note will create or error on its
    own; not this guard's concern).
    """
    if not is_bare_stem(file_arg):
        return False
    stem = stem_of(file_arg)
    return count_vault_files_with_stem(stem, vault_root) > 1


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        tool_input = data.get("tool_input", {})
        file_arg = tool_input.get("file", "")

        if not file_arg:
            sys.exit(0)

        if not is_ambiguous(file_arg):
            sys.exit(0)

        stem = stem_of(file_arg)
        n = count_vault_files_with_stem(stem)
        debug_log(f"BLOCKED ambiguous file={file_arg!r} stem={stem!r} matches={n}")
        print(
            f"BLOQUÉ: alias ambigu '{file_arg}' — {n} notes du vault partagent le stem '{stem}'.\n"
            "append_note résout par FTS et peut écrire dans le MAUVAIS fichier.\n"
            "Utilise le CHEMIN EXACT (vault/claude-forge/<dossier>/<fichier>.md) ou un alias unique du frontmatter.\n"
            "Pour log/index/CHANGELOG : Read + Edit le chemin exact (l'édition vault directe n'est pas bloquée).\n"
            "Doctrine : voir vault [[feedback_mcp_alias_ambigu_chemin_exact]].",
            file=sys.stderr,
        )
        sys.exit(2)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
