#!/usr/bin/env python3
"""Adversarial + characterization tests for vault-write-guard.py.

SCOPE DECLARED BY THE HOOK (vault-write-guard.py docstring):
  Wired on matcher "Write|Edit|MultiEdit" (settings.json — registered in phase 2).
  Blocks DIRECT writes to forge-brain vault NOTES: tool_input.file_path that is a
  .md inside the vault marker "vault/claude-forge" — EXCEPT the ".claude/" subtree
  (agent memory, not Obsidian notes, no MCP route → false positive if blocked).
  Only .md is blocked: .obsidian/*.json, .gitkeep, future .canvas/.base/attachments
  have no MCP route, so the .md filter closes that whole false-positive class.
  Condition ORDER: .claude/ exemption is checked BEFORE the .md filter, so a .md
  under .claude/ (e.g. MEMORY.md agent memory) passes.
  Boundary by FULL PATH SEGMENT, never by file name. Blocks in BOTH contexts
  (main + sub-agent) — NO main-session exemption (unlike vault-cat-guard).
  Exit 2 blocks. Fail-open (exit 0) on parse error.

WHAT THESE TESTS VERIFY:
  - Vault notes blocked across Write / Edit / MultiEdit (the 3:1 BLOCK anchors).
  - For each BLOCK case, >=3 PASS cases proving the guard blocks ONLY vault notes:
    .claude/ at repo root, mcp-forge-brain/, a .md outside the vault, memory/.
  - DISCRIMINATOR: a path with "claude-forge/" but NOT "vault/claude-forge/" (the
    repo root itself) → PASS. Proves the marker requires the "vault/" segment, so
    the whole repo is not locked (the most plausible over-block).
  - EXCLUSION (Raphael's mandate): vault/claude-forge/.claude/agent-memory/MEMORY.md
    → PASS (the .claude subtree exemption works).
  - SEGMENT, not substring: a note that embeds ".claude" in its filename
    (vault/claude-forge/04-Techniques/x-.claude-y.md) still BLOCKS — a note cannot
    smuggle past the exemption.
  - Cross-separator / cross-casing detection (Windows backslash, uppercase).
  - Fail-open on malformed stdin (exit 0).

WHAT THESE TESTS DO *NOT* VERIFY (out-of-scope by design):
  - Read / Bash access to the vault: owned by vault-cat-guard.py, not this hook.
    One test documents that a non-write tool is ignored here.
  - Content validation (frontmatter, wikilinks): by design this hook never
    re-validates content (MCP owns that). Not tested because not claimed.
  - Bash write redirects into the vault (echo > vault/...): no file_path on Bash,
    out of this hook's scope.

Ratio: 3 BLOCK anchors (Write/Edit/MultiEdit) vs >=9 in-scope PASS/adversarial
cases that prove the guard does NOT over-block. >=3:1, in-scope (no padding with
patterns the hook never claimed to catch).

Run: py -m pytest tests/test_vault_write_guard.py -v
"""
import importlib.util
import json
import os
import subprocess
import sys

_hook_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "vault-write-guard.py",
)
_spec = importlib.util.spec_from_file_location("vault_write_guard", _hook_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

references_vault = _mod.references_vault
is_claude_subtree = _mod.is_claude_subtree
is_md = _mod.is_md
violation = _mod.violation
VAULT_MARKER = _mod.VAULT_MARKER


# A real vault note path used as the canonical "must block" fixture.
VAULT_NOTE = "vault/claude-forge/04-Techniques/une-note.md"


# --------------------------------------------------------------------------
# references_vault — path detection across separators / casing
# --------------------------------------------------------------------------

def test_references_vault_unix_path():
    assert references_vault(VAULT_NOTE) is True


def test_references_vault_windows_backslash():
    assert references_vault(r"C:\Users\x\Documents\claude-forge\vault\claude-forge\foo.md") is True


def test_references_vault_uppercase():
    assert references_vault("VAULT/CLAUDE-FORGE/foo.md") is True


def test_references_vault_repo_root_not_vault():
    # The repo dir is "claude-forge" but the marker needs the "vault/" segment.
    assert references_vault("C:/Users/x/Documents/claude-forge/.claude/settings.json") is False


def test_references_vault_memory_not_vault():
    assert references_vault("memory/feedback_x.md") is False


# --------------------------------------------------------------------------
# is_claude_subtree — SEGMENT match after the marker, not substring
# --------------------------------------------------------------------------

def test_claude_subtree_agent_memory_exempt():
    # Raphael's mandate: vault/claude-forge/.claude/agent-memory/MEMORY.md is exempt
    assert is_claude_subtree("vault/claude-forge/.claude/agent-memory/MEMORY.md") is True


def test_claude_subtree_agent_memory_feedback_exempt():
    assert is_claude_subtree("vault/claude-forge/.claude/agent-memory/agent-creator/feedback_x.md") is True


def test_claude_subtree_windows_backslash_exempt():
    assert is_claude_subtree(r"C:\repo\vault\claude-forge\.claude\agent-memory\MEMORY.md") is True


def test_claude_in_filename_is_not_a_segment():
    # ".claude" embedded in a filename is NOT a segment → NOT exempt → will block
    assert is_claude_subtree("vault/claude-forge/04-Techniques/ma-note-.claude-truc.md") is False


def test_claude_as_filename_stem_is_not_a_segment():
    # a note literally named ".claude.md" is still a filename, not a directory segment
    assert is_claude_subtree("vault/claude-forge/04-Techniques/.claude.md") is False


def test_claude_subtree_requires_marker():
    # .claude segment but no vault marker → not our concern → False
    assert is_claude_subtree(".claude/hooks/vault-write-guard.py") is False


def test_claude_before_marker_does_not_exempt():
    # .claude appearing BEFORE the vault marker (repo-root .claude in the abs path)
    # must NOT exempt a real vault note deeper in the path.
    p = "C:/Users/x/.claude/projects/repo/vault/claude-forge/04-Techniques/note.md"
    assert is_claude_subtree(p) is False


# --------------------------------------------------------------------------
# violation — the 3 BLOCK anchors (one per write tool)
# --------------------------------------------------------------------------

def test_violation_edit_vault_note_blocks():
    assert violation("Edit", {"file_path": VAULT_NOTE}) == VAULT_NOTE


def test_violation_write_vault_note_blocks():
    p = "vault/claude-forge/index.md"
    assert violation("Write", {"file_path": p}) == p


def test_violation_multiedit_vault_note_blocks():
    p = "vault/claude-forge/Knowledge/erreurs/x.md"
    assert violation("MultiEdit", {"file_path": p}) == p


def test_violation_windows_backslash_vault_note_blocks():
    p = r"C:\Users\x\Documents\claude-forge\vault\claude-forge\index.md"
    assert violation("Edit", {"file_path": p}) == p


def test_violation_segment_trap_filename_dotclaude_blocks():
    # ".claude" in the FILENAME (not a segment) must still BLOCK — the exemption
    # is by segment, so a note can't hide behind a ".claude" substring.
    p = "vault/claude-forge/04-Techniques/ma-note-.claude-truc.md"
    assert violation("Edit", {"file_path": p}) == p


# --------------------------------------------------------------------------
# violation — PASS cases (>=3:1, in-scope): the guard must NOT over-block
# --------------------------------------------------------------------------

def test_violation_claude_root_passes():
    # .claude/ at the repo root → not the vault → PASS
    assert violation("Edit", {"file_path": "C:/Users/x/Documents/claude-forge/.claude/settings.json"}) is None


def test_violation_mcp_forge_brain_passes():
    # the MCP server source tree (mcp-forge-brain/...) is not the vault
    assert violation("Edit", {"file_path": "C:/Users/x/Documents/claude-forge/mcp-forge-brain/tools/brain.py"}) is None


def test_violation_md_outside_vault_passes():
    # a .md outside the vault (e.g. repo README) → PASS
    assert violation("Write", {"file_path": "C:/Users/x/Documents/claude-forge/README.md"}) is None


def test_violation_memory_feedback_passes():
    # memory/ is NOT the vault → PASS
    assert violation("Edit", {"file_path": "memory/feedback_x.md"}) is None


def test_violation_repo_root_discriminator_passes():
    # DISCRIMINATOR: path contains "claude-forge/" but NOT "vault/claude-forge/"
    # → must PASS (proves the marker needs the vault/ segment, repo not locked).
    assert violation("Write", {"file_path": "C:/Users/x/Documents/claude-forge/CLAUDE.md"}) is None


def test_violation_agent_memory_subtree_passes():
    # Raphael's mandate: the .claude/ subtree UNDER the vault is exempt → PASS
    p = "vault/claude-forge/.claude/agent-memory/MEMORY.md"
    assert violation("Edit", {"file_path": p}) is None


def test_violation_agent_memory_feedback_subtree_passes():
    p = "vault/claude-forge/.claude/agent-memory/agent-creator/feedback_delegate_guard_bypass.md"
    assert violation("Write", {"file_path": p}) is None


def test_violation_other_repo_md_passes():
    # a .md in a sibling repo → PASS (not the forge vault)
    assert violation("Edit", {"file_path": "C:/Users/x/Documents/neot-v2/ia_back/.claude/agents/x.md"}) is None


def test_violation_missing_file_path_passes():
    # no file_path → nothing to block
    assert violation("Edit", {}) is None


# --------------------------------------------------------------------------
# .md-only filter — non-note files under the vault PASS (no MCP route)
# Order check: .claude/ exemption runs BEFORE the .md filter (Raphael's mandate).
# --------------------------------------------------------------------------

def test_is_md_true():
    assert is_md("vault/claude-forge/x.md") is True


def test_is_md_uppercase_extension_true():
    assert is_md("vault/claude-forge/X.MD") is True


def test_is_md_json_false():
    assert is_md("vault/claude-forge/.obsidian/app.json") is False


def test_violation_obsidian_json_passes():
    # .obsidian/*.json config → not a note, no MCP route → PASS
    assert violation("Write", {"file_path": "vault/claude-forge/.obsidian/app.json"}) is None


def test_violation_gitkeep_passes():
    # .gitkeep placeholder → not a note → PASS
    assert violation("Write", {"file_path": "vault/claude-forge/Knowledge/questions/.gitkeep"}) is None


def test_violation_future_canvas_passes():
    # a future .canvas (json-canvas skill) → no MCP route → PASS
    # proves .md-only closes the gap for formats that don't exist yet.
    assert violation("Write", {"file_path": "vault/claude-forge/00-Hub/map.canvas"}) is None


def test_violation_future_base_passes():
    # a future .base (obsidian-bases skill) → no MCP route → PASS
    assert violation("Write", {"file_path": "vault/claude-forge/00-Hub/notes.base"}) is None


def test_violation_md_under_claude_subtree_passes_despite_md():
    # CRITICAL ORDER CHECK: MEMORY.md is a .md, but it sits under .claude/ →
    # the subtree exemption must win over the .md filter → PASS.
    p = "vault/claude-forge/.claude/agent-memory/MEMORY.md"
    assert violation("Edit", {"file_path": p}) is None


def test_violation_md_outside_claude_subtree_blocks():
    # symmetric to the above: a .md NOT under .claude/ → BLOCK.
    p = "vault/claude-forge/Knowledge/erreurs/note.md"
    assert violation("Edit", {"file_path": p}) == p


# --------------------------------------------------------------------------
# violation — out-of-scope tools ignored (documents the boundary)
# --------------------------------------------------------------------------

def test_violation_read_tool_ignored():
    # Read of a vault note is vault-cat-guard's business, not this hook's.
    assert violation("Read", {"file_path": VAULT_NOTE}) is None


def test_violation_bash_tool_ignored():
    # Bash carries no file_path here; vault content access is vault-cat-guard's.
    assert violation("Bash", {"command": f"cat {VAULT_NOTE}"}) is None


def test_violation_mcp_write_tool_ignored():
    # MCP write tools are the SANCTIONED path — never blocked by this hook.
    assert violation("mcp__forge-brain__append_note_by_path", {"file": VAULT_NOTE}) is None


# --------------------------------------------------------------------------
# end-to-end via subprocess — exit codes
# --------------------------------------------------------------------------

def _run_hook(stdin_obj: dict) -> int:
    proc = subprocess.run(
        [sys.executable, _hook_path],
        input=json.dumps(stdin_obj),
        capture_output=True,
        text=True,
    )
    return proc.returncode


def test_e2e_edit_vault_note_blocked_exit2():
    rc = _run_hook({"tool_name": "Edit", "tool_input": {"file_path": VAULT_NOTE}})
    assert rc == 2


def test_e2e_write_vault_note_blocked_exit2():
    rc = _run_hook({"tool_name": "Write", "tool_input": {"file_path": "vault/claude-forge/index.md"}})
    assert rc == 2


def test_e2e_multiedit_vault_note_blocked_exit2():
    rc = _run_hook({
        "tool_name": "MultiEdit",
        "tool_input": {"file_path": "vault/claude-forge/Knowledge/erreurs/x.md"},
    })
    assert rc == 2


def test_e2e_segment_trap_filename_dotclaude_blocked_exit2():
    rc = _run_hook({
        "tool_name": "Edit",
        "tool_input": {"file_path": "vault/claude-forge/04-Techniques/ma-note-.claude-truc.md"},
    })
    assert rc == 2


def test_e2e_agent_memory_subtree_allowed_exit0():
    # the .claude/ subtree under the vault is exempt → allowed
    rc = _run_hook({
        "tool_name": "Edit",
        "tool_input": {"file_path": "vault/claude-forge/.claude/agent-memory/MEMORY.md"},
    })
    assert rc == 0


def test_e2e_claude_root_allowed_exit0():
    rc = _run_hook({
        "tool_name": "Edit",
        "tool_input": {"file_path": "C:/Users/x/Documents/claude-forge/.claude/settings.json"},
    })
    assert rc == 0


def test_e2e_md_outside_vault_allowed_exit0():
    rc = _run_hook({
        "tool_name": "Write",
        "tool_input": {"file_path": "C:/Users/x/Documents/claude-forge/README.md"},
    })
    assert rc == 0


def test_e2e_repo_root_discriminator_allowed_exit0():
    rc = _run_hook({
        "tool_name": "Write",
        "tool_input": {"file_path": "C:/Users/x/Documents/claude-forge/CLAUDE.md"},
    })
    assert rc == 0


def test_e2e_read_vault_note_allowed_exit0():
    # Read is out of scope for this hook → allowed (vault-cat-guard owns Read).
    rc = _run_hook({"tool_name": "Read", "tool_input": {"file_path": VAULT_NOTE}})
    assert rc == 0


def test_e2e_obsidian_json_allowed_exit0():
    rc = _run_hook({
        "tool_name": "Write",
        "tool_input": {"file_path": "vault/claude-forge/.obsidian/app.json"},
    })
    assert rc == 0


def test_e2e_future_canvas_allowed_exit0():
    rc = _run_hook({
        "tool_name": "Write",
        "tool_input": {"file_path": "vault/claude-forge/00-Hub/map.canvas"},
    })
    assert rc == 0


def test_e2e_malformed_stdin_fail_open():
    proc = subprocess.run(
        [sys.executable, _hook_path],
        input="not json",
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0


# --------------------------------------------------------------------------
# blocking message points to the RIGHT MCP alternative (Write vs Edit)
# --------------------------------------------------------------------------

def _run_hook_stderr(stdin_obj: dict) -> str:
    # Bytes mode end-to-end: input MUST be bytes when text=False, else subprocess
    # mismatches str/bytes on the stdin writer thread and HANGS on Windows (the
    # bug that froze this run at test 50/52). Decode stderr tolerantly because the
    # child's accented French message may land in cp1252; we only assert on ASCII
    # tool names (create_note / update_note / by_path).
    proc = subprocess.run(
        [sys.executable, _hook_path],
        input=json.dumps(stdin_obj).encode("utf-8"),
        capture_output=True,
    )
    return proc.stderr.decode("utf-8", errors="replace")


def test_message_write_points_to_create_note():
    # Write = new note → message must mention create_note, not update_note.
    err = _run_hook_stderr({"tool_name": "Write", "tool_input": {"file_path": VAULT_NOTE}})
    assert "create_note" in err


def test_message_edit_points_to_update_and_by_path():
    # Edit = existing note → message must mention update_note + by-path variants.
    err = _run_hook_stderr({"tool_name": "Edit", "tool_input": {"file_path": VAULT_NOTE}})
    assert "update_note" in err
    assert "by_path" in err
