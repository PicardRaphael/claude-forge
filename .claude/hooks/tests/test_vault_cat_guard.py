#!/usr/bin/env python3
"""Adversarial + characterization tests for vault-cat-guard.py.

SCOPE DECLARED BY THE HOOK (vault-cat-guard.py docstring):
  Wired on matcher "Bash|Read|PowerShell" (settings.json). Blocks raw filesystem
  access to the forge-brain vault (any path containing "vault/claude-forge"):
    - Read: file_path inside the vault
    - Bash / PowerShell: read commands (cat/find/grep/head/tail/sed/awk/less/more/
            rg/nl/tac/xxd/od/strings/type, Get-Content/gc/Select-String/sls/
            Get-ChildItem/gci) whose args reference the vault — content dumps
  Context-dependent blocking:
    - dump (Bash/PowerShell): blocked in BOTH contexts (main + sub-agent)
    - read (Read tool): blocked in SUB-AGENT only — main session legitimately
      Reads the vault to prepare an Edit (exact-path edit of ambiguous-stem note)
  Exit 2 blocks. Fail-open on errors.

WHAT THESE TESTS VERIFY:
  - Vault reads detected for Read and for each read command (Bash + PowerShell),
    across path separators and casing (adversarial).
  - Non-vault reads pass (false-positive guard).
  - Context rule: Read blocked in sub-agent, allowed in main session; dump blocked
    in both. No agent exemptions.
  - Write-class tools / MCP calls are not this hook's business (out of scope).

WHAT THESE TESTS DO *NOT* VERIFY (out-of-scope by design):
  - Write redirects into the vault (echo > vault/...): this guard targets READS,
    not writes; vault writes go through MCP or Edit (other guards). One test
    documents this gap.
  - MCP alias ambiguity: owned by mcp-alias-guard.py, not here.

Run: py -m pytest tests/test_vault_cat_guard.py -v
"""
import importlib.util
import json
import os
import subprocess
import sys

_hook_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "vault-cat-guard.py",
)
_spec = importlib.util.spec_from_file_location("vault_cat_guard", _hook_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

references_vault = _mod.references_vault
bash_reads_vault = _mod.bash_reads_vault
violation = _mod.violation
should_block = _mod.should_block
active_agent = _mod.active_agent
READ_COMMANDS = _mod.READ_COMMANDS


# --------------------------------------------------------------------------
# references_vault — path detection across separators / casing
# --------------------------------------------------------------------------

def test_references_vault_unix_path():
    assert references_vault("vault/claude-forge/04-Techniques/foo.md") is True


def test_references_vault_windows_path():
    assert references_vault(r"C:\Users\x\Documents\claude-forge\vault\claude-forge\foo.md") is True


def test_references_vault_uppercase():
    assert references_vault("VAULT/CLAUDE-FORGE/foo.md") is True


def test_references_vault_non_vault_path():
    assert references_vault(".claude/hooks/delegate-guard.py") is False


def test_references_vault_memory_path_not_vault():
    # memory/ is NOT the vault — must not be blocked
    assert references_vault("memory/feedback_x.md") is False


# --------------------------------------------------------------------------
# bash_reads_vault — read command + vault target
# --------------------------------------------------------------------------

def test_bash_cat_vault_blocked():
    assert bash_reads_vault("cat vault/claude-forge/log.md") is True


def test_bash_grep_vault_blocked():
    assert bash_reads_vault("grep -rn 'pattern' vault/claude-forge/") is True


def test_bash_find_vault_blocked():
    assert bash_reads_vault("find vault/claude-forge -name '*.md'") is True


def test_bash_head_vault_blocked():
    assert bash_reads_vault("head -50 vault/claude-forge/index.md") is True


def test_bash_tail_vault_blocked():
    assert bash_reads_vault("tail -20 vault/claude-forge/CHANGELOG.md") is True


def test_bash_powershell_getcontent_vault_blocked():
    assert bash_reads_vault("Get-Content vault/claude-forge/log.md") is True


def test_bash_powershell_selectstring_vault_blocked():
    assert bash_reads_vault("Select-String -Path vault/claude-forge/*.md -Pattern x") is True


def test_bash_piped_grep_vault_blocked():
    # cat piped into grep, both target vault
    assert bash_reads_vault("cat vault/claude-forge/log.md | grep foo") is True


def test_bash_absolute_path_with_bin_prefix_blocked():
    # /usr/bin/cat should still be recognized as cat
    assert bash_reads_vault("/usr/bin/cat vault/claude-forge/log.md") is True


def test_bash_read_command_no_vault_passes():
    assert bash_reads_vault("cat .claude/settings.json") is False


def test_bash_vault_path_but_no_read_command_passes():
    # ls is not in READ_COMMANDS (it doesn't dump content); a bare path mention
    # without a read command should pass — this guard targets content dumps.
    assert bash_reads_vault("ls vault/claude-forge/") is False


def test_bash_git_on_vault_passes():
    # git operations on the vault are not raw content reads
    assert bash_reads_vault("git -C vault/claude-forge status") is False


# --------------------------------------------------------------------------
# chained commands — read-command and vault marker must be in the SAME segment
# (regression guard for the false positive found 27 May 2026: git add vault/...
#  && git push | tail was wrongly blocked because tail + vault marker co-occurred
#  across different segments)
# --------------------------------------------------------------------------

def test_chained_git_add_vault_then_push_pipe_tail_passes():
    # vault marker in segment 1 (git add), tail in segment 3 (git push | tail)
    # → different segments → NOT a raw read → must PASS
    cmd = 'git add "vault/claude-forge/x.md" && git push 2>&1 | tail -3'
    assert bash_reads_vault(cmd) is False


def test_chained_cat_vault_pipe_head_blocked():
    # cat + vault marker in the SAME segment → dump → must BLOCK
    assert bash_reads_vault("cat vault/claude-forge/log.md | head") is True


def test_chained_git_log_pipe_grep_vault_blocked():
    # grep + vault marker in the SAME (piped) segment → raw grep of vault → BLOCK
    assert bash_reads_vault("git log | grep vault/claude-forge/foo") is True


def test_chained_cat_readme_then_cat_vault_blocked():
    # dump in segment 2 (cat vault/...) → BLOCK
    assert bash_reads_vault("cat README.md && cat vault/claude-forge/x.md") is True


def test_chained_echo_vault_marker_no_read_command_passes():
    # marker present but no READ_COMMAND in that segment (echo) → PASS
    assert bash_reads_vault("cat README.md && echo vault/claude-forge/foo") is False


def test_chained_echo_marker_pipe_cat_passes():
    # echo "vault/..." | cat — marker in segment 1 (echo, not a read cmd),
    # cat in segment 2 (no marker). cat reads stdin, not the file → PASS.
    assert bash_reads_vault('echo "vault/claude-forge" | cat') is False


def test_redirect_2to1_not_treated_as_segment_separator():
    # single & in 2>&1 must NOT split the segment — cat+vault stay together → BLOCK
    assert bash_reads_vault("cat vault/claude-forge/log.md 2>&1") is True


# --------------------------------------------------------------------------
# violation — tool dispatch
# --------------------------------------------------------------------------

def test_violation_read_vault():
    assert violation("Read", {"file_path": "vault/claude-forge/log.md"}) is not None


def test_violation_read_non_vault():
    assert violation("Read", {"file_path": ".claude/agents/skill-creator.md"}) is None


def test_violation_bash_cat_vault():
    assert violation("Bash", {"command": "cat vault/claude-forge/log.md"}) is not None


def test_violation_bash_non_vault():
    assert violation("Bash", {"command": "cat README.md"}) is None


def test_violation_other_tool_ignored():
    # MCP write tools are not this hook's business
    assert violation("mcp__forge-brain__append_note", {"file": "log"}) is None


def test_violation_write_tool_ignored():
    # Out-of-scope by design: this guard targets READS. A write redirect into
    # the vault is not seen here (no file_path on Bash write redirects either).
    assert violation("Write", {"file_path": "vault/claude-forge/log.md"}) is None


# --------------------------------------------------------------------------
# active_agent — baseline
# --------------------------------------------------------------------------

def test_active_agent_empty_main_session():
    assert active_agent({}) == ""


# --------------------------------------------------------------------------
# violation — kind tagging (dump vs read) + PowerShell
# --------------------------------------------------------------------------

def test_violation_read_returns_read_kind():
    assert violation("Read", {"file_path": "vault/claude-forge/log.md"})[0] == "read"


def test_violation_bash_returns_dump_kind():
    assert violation("Bash", {"command": "cat vault/claude-forge/log.md"})[0] == "dump"


def test_violation_powershell_getcontent_dump_kind():
    assert violation("PowerShell", {"command": "Get-Content vault/claude-forge/log.md"})[0] == "dump"


def test_violation_powershell_selectstring_dump():
    assert violation("PowerShell", {"command": "Select-String -Path vault/claude-forge/x.md foo"})[0] == "dump"


def test_violation_powershell_non_vault_none():
    assert violation("PowerShell", {"command": "Get-Content README.md"}) is None


# --------------------------------------------------------------------------
# should_block — context rule (the core of the main-session Read exemption)
# --------------------------------------------------------------------------

def test_should_block_dump_main_session():
    # content dump blocked even in main session
    assert should_block("dump", {}) is True


def test_should_block_dump_subagent():
    assert should_block("dump", {"agent_type": "skill-creator"}) is True


def test_should_block_read_main_session_allowed():
    # Read in main session → NOT blocked (prepare Edit, has MCP)
    assert should_block("read", {}) is False


def test_should_block_read_subagent_blocked():
    assert should_block("read", {"agent_type": "skill-creator"}) is True


def test_should_block_read_former_exempt_now_blocked():
    # No more exemption: a sub-agent reading the vault is blocked like any other
    assert should_block("read", {"agent_type": "vault-maintainer"}) is True


def test_should_block_dump_former_exempt_now_blocked():
    # No more exemption: dumps blocked in all contexts, no agent escapes
    assert should_block("dump", {"agent_type": "vault-maintainer"}) is True


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


def test_e2e_cat_vault_blocked_exit2():
    rc = _run_hook({"tool_name": "Bash", "tool_input": {"command": "cat vault/claude-forge/log.md"}})
    assert rc == 2


def test_e2e_read_vault_main_session_allowed_exit0():
    # Read on the vault from the MAIN session (no agent fields) → allowed,
    # so the session can prepare an Edit on the vault.
    rc = _run_hook({"tool_name": "Read", "tool_input": {"file_path": "vault/claude-forge/log.md"}})
    assert rc == 0


def test_e2e_read_vault_subagent_blocked_exit2():
    # Read on the vault from a sub-agent → blocked (fragile fallback).
    rc = _run_hook({
        "tool_name": "Read",
        "tool_input": {"file_path": "vault/claude-forge/log.md"},
        "agent_type": "skill-creator",
    })
    assert rc == 2


def test_e2e_powershell_getcontent_vault_blocked_exit2():
    rc = _run_hook({
        "tool_name": "PowerShell",
        "tool_input": {"command": "Get-Content vault/claude-forge/log.md"},
    })
    assert rc == 2


def test_e2e_non_vault_passes_exit0():
    rc = _run_hook({"tool_name": "Bash", "tool_input": {"command": "cat README.md"}})
    assert rc == 0


def test_e2e_former_exempt_agent_read_subagent_blocked_exit2():
    # vault-maintainer removed: no exemption — a sub-agent Read of the vault blocks
    rc = _run_hook({
        "tool_name": "Read",
        "tool_input": {"file_path": "vault/claude-forge/log.md"},
        "agent_type": "vault-maintainer",
    })
    assert rc == 2


def test_e2e_malformed_stdin_fail_open():
    proc = subprocess.run(
        [sys.executable, _hook_path],
        input="not json",
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
