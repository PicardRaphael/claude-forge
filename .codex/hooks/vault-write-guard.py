#!/usr/bin/env python3
"""Block direct Write/Edit/MultiEdit of forge-brain vault NOTES — enforce MCP-only writes.

Scope: PreToolUse on Write, Edit, MultiEdit.
  Block (exit 2) when tool_input.file_path is a NOTE (.md) inside the forge-brain
  vault (any path containing "vault/claude-forge") — EXCEPT the ".claude/" subtree.

Only .md notes are blocked. The MCP forge-brain tools are note-(.md)-oriented
  (create_note / update_note / *_by_path); .obsidian/*.json config, .gitkeep, and
  any future .canvas/.base/attachment have NO MCP route, so blocking them would be
  a false positive with no sanctioned alternative — the same class arbitrated for
  the .claude/ subtree. Restricting to .md closes that whole gap (present AND
  future formats) without enumerating per-segment exemptions.

Why this hook exists (architecture, not discipline):
  The MCP forge-brain server is the only sanctioned write path to vault notes.
  A direct disk Edit does NOT trigger index_note → the SQLite index desyncs until
  the 30s poll. Until 2026-06-07 there was no write-by-path MCP tool, so the
  sanctioned fallback for ambiguous stems (log/index/CHANGELOG) was "Read+Edit the
  exact path" — which IS the desync cause. The pieces-1 update_*_by_path tools now
  cover exact-path writes via MCP, so direct Edit no longer has a reason to exist →
  this guard can finally block it cleanly. Mantra: "MCP validates the content, the
  hook forbids the bypass" — this hook does NOT re-validate frontmatter/wikilinks
  (that lives in MCP create_note; re-implementing here = drift vs single-source).

Boundary is by FULL PATH SEGMENT, never by file name (delegate-guard lesson: a name
  like agents-*.md exists in BOTH the vault and .claude/agents/). The ".claude/"
  exclusion matches ".claude" as a whole path COMPONENT appearing AFTER the
  "vault/claude-forge" marker — so a note cannot smuggle itself past the guard by
  embedding ".claude" in a filename (e.g. vault/claude-forge/04-Techniques/x-.claude-y.md
  still BLOCKS). The excluded subtree holds agent memory (vault/claude-forge/.claude/
  agent-memory/*.md) — NOT Obsidian notes, and nothing routes it through MCP, so
  blocking it would be a false positive with no sanctioned alternative.

No context rule: writes block in BOTH main session and sub-agent. Unlike
  vault-cat-guard (which exempts the main session's Read for audit/lookup), here
  the main session is exactly who must stop Editing the vault directly — the
  exemption would make the hook inert.

Exit 2 blocks. Fail-open (exit 0) on any parse error.
Debug log (append): <tempdir>/vault-write-guard-debug.log
"""
import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Vault marker present in every vault path (cloned from vault-cat-guard.py)
VAULT_MARKER = "vault/claude-forge"

# The path segment, appearing AFTER the marker, that exempts a subtree.
CLAUDE_SEGMENT = ".claude"

LOG_PATH = Path(tempfile.gettempdir()) / "vault-write-guard-debug.log"


def debug_log(msg: str) -> None:
    """Append timestamped message to debug log. Fail silently."""
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    except Exception:
        pass


def normalize(text: str) -> str:
    """Forward-slashes, lowercased — cross-separator / cross-casing path matching."""
    return text.replace("\\", "/").lower()


def references_vault(path: str) -> bool:
    """True if the path points inside the forge-brain vault."""
    return VAULT_MARKER in normalize(path)


def is_claude_subtree(path: str) -> bool:
    """True if ".claude" is a whole path SEGMENT appearing AFTER the vault marker.

    Segment match, not substring: split the normalized path and require an exact
    ".claude" component positioned after the "vault" / "claude-forge" pair. A file
    merely containing ".claude" in its name (e.g. x-.claude-y.md) is NOT exempted —
    only a real vault/claude-forge/.claude/... subtree is.
    """
    norm = normalize(path)
    if VAULT_MARKER not in norm:
        return False
    segments = norm.split("/")
    # Locate the marker pair "vault" -> "claude-forge" (consecutive segments).
    marker_end = None
    for i in range(len(segments) - 1):
        if segments[i] == "vault" and segments[i + 1] == "claude-forge":
            marker_end = i + 1  # index of "claude-forge"
            break
    if marker_end is None:
        return False
    # ".claude" must be an exact segment strictly after "claude-forge".
    return CLAUDE_SEGMENT in segments[marker_end + 1:]


def is_md(path: str) -> bool:
    """True if the path is a Markdown note (the only files with an MCP route)."""
    return normalize(path).endswith(".md")


def violation(tool_name: str, tool_input: dict) -> str | None:
    """Return the offending file_path if this write targets a vault note, else None.

    A vault note = a .md inside the vault marker AND not in the exempt .claude/
    subtree. Tool-agnostic across Write/Edit/MultiEdit: all carry file_path.

    Condition ORDER matters: the .claude/ exemption is checked BEFORE the .md
    filter, so a .md under .claude/ (agent memory like MEMORY.md) passes — it is
    exempt by subtree even though it is a .md. Only .md notes OUTSIDE .claude/ block.
    """
    if tool_name not in ("Write", "Edit", "MultiEdit"):
        return None
    file_path = tool_input.get("file_path", "")
    if not file_path:
        return None
    if not references_vault(file_path):
        return None
    if is_claude_subtree(file_path):  # agent memory subtree — exempt FIRST
        return None
    if not is_md(file_path):  # only .md notes have an MCP route
        return None
    return file_path


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        offending = violation(tool_name, tool_input)
        if offending is None:
            sys.exit(0)

        debug_log(f"BLOCKED tool={tool_name} file={offending[:160]!r}")
        # Point to the RIGHT MCP alternative: Write creates a new note, Edit/MultiEdit
        # modify an existing one.
        if tool_name == "Write":
            alternative = (
                "Pour créer une note neuve : create_note (valide le frontmatter, indexe).\n"
            )
        else:
            alternative = (
                "Pour modifier une note existante : update_note / append_note / insert_section / "
                "update_property (par alias unique), ou les variantes *_by_path pour un chemin exact "
                "ambigu (update_note_by_path / append_note_by_path / insert_section_by_path / "
                "update_property_by_path).\n"
            )
        print(
            "BLOQUÉ: écriture directe d'une note du vault forge-brain interdite.\n"
            f"Outil: {tool_name}\n"
            f"Fichier: {offending[:200]}\n"
            "Le vault s'écrit UNIQUEMENT via le MCP forge-brain (la doctrine 'jamais Edit direct').\n"
            "Une écriture disque ne déclenche PAS la réindexation → l'index SQLite désynchronise.\n"
            + alternative
            + "Si le MCP est indisponible : relancer le MCP forge-brain, JAMAIS contourner par Edit.\n"
            "Doctrine : voir vault [[feedback_mcp_alias_ambigu_chemin_exact]] + [[vault-edit-gotchas-outillage]].",
            file=sys.stderr,
        )
        sys.exit(2)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
