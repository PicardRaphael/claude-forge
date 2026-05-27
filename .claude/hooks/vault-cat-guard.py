#!/usr/bin/env python3
"""Block raw filesystem access to the forge-brain vault — enforce MCP-only doctrine.

Scope: PreToolUse on Bash, PowerShell, and Read.
  Bash / PowerShell: block read commands (cat/find/grep/head/tail/sed/awk/less/
        more, Get-Content/gc/Select-String/sls/Get-ChildItem/gci) whose args
        reference the vault — content dumps.
  Read: block file_path pointing inside the vault.

Target: any path containing "vault/claude-forge" (the forge-brain vault root).

Rationale: the MCP forge-brain server is the only sanctioned access path to the
vault. In a sub-agent context the MCP server is NOT connected (decorative
frontmatter, "No such tool available"), so an agent told to "read the vault"
falls back to cat/find/grep — violating MCP-only doctrine. This guard makes the
rule structural.

Context-dependent blocking:
  - Bash/PowerShell content dumps: blocked in BOTH contexts (main + sub-agent).
    A mass content dump is never the right way to access the vault.
  - Read on a vault file: blocked in SUB-AGENT only. The main session legitimately
    needs Read to prepare an Edit on the vault (e.g. exact-path edit of an
    ambiguous-stem note like log.md — see feedback_mcp_alias_ambigu_chemin_exact),
    and it has the MCP. A sub-agent reading the vault by Read is the fragile
    fallback we forbid.
  Exemption (all contexts): vault-maintainer — its job is to read/write the vault.

Exit 2 blocks. Fail-open (exit 0) on any parse error.
"""
import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Repo root = parent of .claude/hooks/ (robust to cwd, never os.environ)
FORGE_PROJECT_DIR = str(Path(__file__).resolve().parent.parent.parent).replace("\\", "/").lower()

# Vault marker present in every vault path
VAULT_MARKER = "vault/claude-forge"

# Agents allowed to access the vault directly (their job requires it)
EXEMPT_AGENTS = {"vault-maintainer"}

# Bash read commands that would dump vault content
READ_COMMANDS = (
    "cat", "find", "grep", "egrep", "fgrep", "rg", "head", "tail",
    "sed", "awk", "less", "more", "nl", "tac", "xxd", "od", "strings",
    "get-content", "gc", "select-string", "sls", "get-childitem", "gci",
    "type",
)

LOG_PATH = Path(tempfile.gettempdir()) / "vault-cat-guard-debug.log"


def debug_log(msg: str) -> None:
    """Append timestamped message to debug log. Fail silently."""
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    except Exception:
        pass


def normalize(text: str) -> str:
    return text.replace("\\", "/").lower()


def references_vault(text: str) -> bool:
    """True if the text (path or command) references the vault."""
    return VAULT_MARKER in normalize(text)


# Chain operators that split a command line into independent segments.
# ORDER MATTERS in this alternation: longer operators first so "&&" matches
# before "&" and "||" before "|" (re.split alternates left-to-right per position).
# A single "&" (e.g. "2>&1") is NOT a separator — it stays inside its segment.
_SEGMENT_SPLIT = re.compile(r"&&|\|\||;|\|")


def _segments(command: str) -> list[str]:
    """Split a shell command line into independent segments on &&, ||, ;, |.

    A read of the vault is only a violation when a read command AND the vault
    marker appear in the SAME segment. Splitting first prevents false positives
    like `git add "vault/..." && git push 2>&1 | tail -3` (vault in segment 1,
    tail in segment 3 — different segments, no raw read).
    """
    return _SEGMENT_SPLIT.split(command)


def _segment_reads_vault(segment: str) -> bool:
    """True if a single segment contains both a read command and the vault marker."""
    norm = normalize(segment)
    if VAULT_MARKER not in norm:
        return False
    for tok in re.split(r"[\s()]+", norm):
        base = tok.rsplit("/", 1)[-1]  # /usr/bin/grep -> grep
        if base in READ_COMMANDS:
            return True
    return False


def bash_reads_vault(command: str) -> bool:
    """True if any chain segment is a read command targeting the vault.

    Segmentation on &&/||/;/| first, then per-segment check: a read command and
    the vault marker must co-occur in the SAME segment to be a violation. This
    guard only cares about raw content reads of the vault (cat/grep/Get-Content...).
    """
    return any(_segment_reads_vault(seg) for seg in _segments(command))


def detect_subagent_from_transcript(transcript_path: str) -> str | None:
    """Parse last 50 lines of transcript to find innermost active sub-agent.

    Walk lines in reverse. First terminal event wins:
      - agent_end / subagent_end / agent_complete → not inside a sub-agent → None
      - agent_start / subagent_start / subagent_type present → return its type
    Fail-open → None on any error.
    """
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in reversed(lines[-50:]):
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except Exception:
                continue
            event_type = event.get("type", "")
            if event_type in ("agent_end", "subagent_end", "agent_complete"):
                return None
            if event_type in ("agent_start", "subagent_start") or "subagent_type" in event:
                return event.get("subagent_type") or event.get("agent_type") or ""
    except Exception:
        pass
    return None


def active_agent(data: dict) -> str:
    """Return the active sub-agent type, or '' if main session / unknown."""
    agent_type = data.get("agent_type", "")
    if agent_type:
        return agent_type
    agent_id = data.get("agent_id", "")
    if agent_id:
        return agent_id
    transcript_path = data.get("transcript_path", "")
    if transcript_path:
        detected = detect_subagent_from_transcript(transcript_path)
        if detected:
            return detected
    return ""


def is_exempt(data: dict) -> bool:
    """True if the active agent is allowed to access the vault directly."""
    return active_agent(data) in EXEMPT_AGENTS


def violation(tool_name: str, tool_input: dict) -> tuple[str, str] | None:
    """Return (kind, target) if this call accesses the vault raw, else None.

    kind is "dump" for a Bash/PowerShell read command, "read" for a Read tool.
    The kind drives the context rule in should_block().
    """
    if tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        if file_path and references_vault(file_path):
            return ("read", file_path)
        return None
    if tool_name in ("Bash", "PowerShell"):
        command = tool_input.get("command", "")
        if command and bash_reads_vault(command):
            return ("dump", command)
        return None
    return None


def should_block(kind: str, data: dict) -> bool:
    """Apply the context rule. vault-maintainer is never blocked.

    - "dump" (Bash/PowerShell content dump): blocked in BOTH contexts.
    - "read" (Read tool): blocked in SUB-AGENT only; the main session legitimately
      Reads the vault to prepare an Edit and has the MCP.
    """
    if is_exempt(data):
        return False
    if kind == "dump":
        return True
    if kind == "read":
        return active_agent(data) != ""  # sub-agent only
    return False


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        v = violation(tool_name, tool_input)
        if v is None:
            sys.exit(0)

        kind, offending = v

        if not should_block(kind, data):
            debug_log(f"ALLOW kind={kind} agent={active_agent(data)!r} tool={tool_name} target={offending[:80]!r}")
            sys.exit(0)

        debug_log(f"BLOCKED kind={kind} tool={tool_name} target={offending[:120]!r} agent={active_agent(data)!r}")
        print(
            "BLOQUÉ: accès brut au vault forge-brain interdit.\n"
            f"Outil: {tool_name}\n"
            f"Cible: {offending[:200]}\n"
            "Le vault s'accède UNIQUEMENT via le MCP forge-brain (search_brain, read_note...).\n"
            "En sous-agent, le MCP n'est PAS connecté : si une canonique te manque, ESCALADE "
            "(demande-la à la session principale). Ne cat/find/grep/Read JAMAIS le vault directement.\n"
            "Doctrine : voir vault [[pattern-mcp-brief-then-direct]].",
            file=sys.stderr,
        )
        sys.exit(2)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
