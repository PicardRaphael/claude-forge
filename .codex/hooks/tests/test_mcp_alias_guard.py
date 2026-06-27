#!/usr/bin/env python3
"""Adversarial + characterization tests for mcp-alias-guard.py.

SCOPE DECLARED BY THE HOOK (mcp-alias-guard.py docstring):
  Wired on 8 forge-brain tools (settings.json pipe-separated matcher). Blocks a
  bare-stem `file` argument when >1 vault file shares that stem (ambiguous FTS
  resolution). Exact paths (with separator) and unique/absent stems pass.
  Exit 2 blocks. Fail-open (exit 0) on parse error / unscanned vault.
  Logic is tool-agnostic: only inspects tool_input.file, ignores tool_name.

WHAT THESE TESTS VERIFY:
  - Ambiguous bare stem (log/index/CHANGELOG with >1 match) → blocked.
  - Exact path → allowed (never ambiguous).
  - Unique stem → allowed.
  - Absent stem → allowed (not this guard's concern).
  - .md extension handled; case-insensitive matching.
  - All 8 matched tools block ambiguous stems (E2E subprocess, real vault).
  - Exact path allowed on a non-append_note tool (tool-agnostic confirmation).

Run: py -m pytest tests/test_mcp_alias_guard.py -v
"""
import importlib.util
import json
import os
import subprocess
import sys

_hook_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "mcp-alias-guard.py",
)
_spec = importlib.util.spec_from_file_location("mcp_alias_guard", _hook_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

is_bare_stem = _mod.is_bare_stem
stem_of = _mod.stem_of
count_vault_files_with_stem = _mod.count_vault_files_with_stem
is_ambiguous = _mod.is_ambiguous


# --------------------------------------------------------------------------
# fixture: fake vault with multi-stem (log x3) + unique stem (uniquenote x1)
# --------------------------------------------------------------------------

import pytest


@pytest.fixture
def fake_vault(tmp_path):
    root = tmp_path / "vault" / "claude-forge"
    (root / "a").mkdir(parents=True)
    (root / "b").mkdir(parents=True)
    (root / "c").mkdir(parents=True)
    # 3 files sharing stem "log"
    (root / "log.md").write_text("root log", encoding="utf-8")
    (root / "a" / "log.md").write_text("a log", encoding="utf-8")
    (root / "b" / "log.md").write_text("b log", encoding="utf-8")
    # 2 files sharing stem "index"
    (root / "index.md").write_text("root index", encoding="utf-8")
    (root / "a" / "index.md").write_text("a index", encoding="utf-8")
    # unique stem
    (root / "c" / "uniquenote.md").write_text("unique", encoding="utf-8")
    return root


# --------------------------------------------------------------------------
# is_bare_stem
# --------------------------------------------------------------------------

def test_bare_stem_true():
    assert is_bare_stem("log") is True


def test_bare_stem_false_unix_sep():
    assert is_bare_stem("vault/claude-forge/log.md") is False


def test_bare_stem_false_win_sep():
    assert is_bare_stem(r"vault\claude-forge\log.md") is False


# --------------------------------------------------------------------------
# stem_of
# --------------------------------------------------------------------------

def test_stem_of_bare():
    assert stem_of("log") == "log"


def test_stem_of_with_md():
    assert stem_of("log.md") == "log"


def test_stem_of_uppercase():
    assert stem_of("CHANGELOG.md") == "changelog"


def test_stem_of_alias_with_space():
    # "log vault" is an alias, not a stem — treated verbatim (lowercased)
    assert stem_of("log vault") == "log vault"


# --------------------------------------------------------------------------
# count_vault_files_with_stem
# --------------------------------------------------------------------------

def test_count_log_is_three(fake_vault):
    assert count_vault_files_with_stem("log", fake_vault) == 3


def test_count_index_is_two(fake_vault):
    assert count_vault_files_with_stem("index", fake_vault) == 2


def test_count_unique_is_one(fake_vault):
    assert count_vault_files_with_stem("uniquenote", fake_vault) == 1


def test_count_absent_is_zero(fake_vault):
    assert count_vault_files_with_stem("doesnotexist", fake_vault) == 0


def test_count_missing_vault_is_zero(tmp_path):
    # vault root doesn't exist → 0 (fail-open upstream)
    assert count_vault_files_with_stem("log", tmp_path / "nope") == 0


# --------------------------------------------------------------------------
# is_ambiguous — the core decision
# --------------------------------------------------------------------------

def test_ambiguous_bare_log_blocked(fake_vault):
    assert is_ambiguous("log", fake_vault) is True


def test_ambiguous_bare_log_md_blocked(fake_vault):
    assert is_ambiguous("log.md", fake_vault) is True


def test_ambiguous_index_blocked(fake_vault):
    assert is_ambiguous("index", fake_vault) is True


def test_exact_path_log_allowed(fake_vault):
    # exact path is never ambiguous, even for a multi-stem name
    assert is_ambiguous("vault/claude-forge/log.md", fake_vault) is False


def test_exact_path_win_sep_allowed(fake_vault):
    assert is_ambiguous(r"vault\claude-forge\a\log.md", fake_vault) is False


def test_unique_stem_allowed(fake_vault):
    assert is_ambiguous("uniquenote", fake_vault) is False


def test_absent_stem_allowed(fake_vault):
    assert is_ambiguous("brandnewnote", fake_vault) is False


# --------------------------------------------------------------------------
# end-to-end via subprocess — exit codes (uses the REAL vault)
# --------------------------------------------------------------------------

def _run_hook(stdin_obj: dict) -> int:
    proc = subprocess.run(
        [sys.executable, _hook_path],
        input=json.dumps(stdin_obj),
        capture_output=True,
        text=True,
    )
    return proc.returncode


def test_e2e_real_vault_bare_log_blocked():
    # The real forge vault has multiple log.md → bare "log" must be blocked.
    rc = _run_hook({
        "tool_name": "mcp__forge-brain__append_note",
        "tool_input": {"file": "log", "content": "x"},
    })
    assert rc == 2


def test_e2e_real_vault_exact_path_allowed():
    rc = _run_hook({
        "tool_name": "mcp__forge-brain__append_note",
        "tool_input": {"file": "vault/claude-forge/log.md", "content": "x"},
    })
    assert rc == 0


def test_e2e_no_file_arg_passes():
    rc = _run_hook({"tool_name": "mcp__forge-brain__append_note", "tool_input": {}})
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
# end-to-end via subprocess — coverage for the 7 additional matched tools
# The hook is tool-agnostic: same logic regardless of tool_name.
# Each test sends bare "log" (ambiguous in real vault) → must block exit 2.
# --------------------------------------------------------------------------

def test_e2e_insert_section_bare_log_blocked():
    rc = _run_hook({
        "tool_name": "mcp__forge-brain__insert_section",
        "tool_input": {"file": "log", "marker": "## Notes", "content": "x"},
    })
    assert rc == 2


def test_e2e_read_section_bare_log_blocked():
    rc = _run_hook({
        "tool_name": "mcp__forge-brain__read_section",
        "tool_input": {"file": "log", "heading": "## Notes"},
    })
    assert rc == 2


def test_e2e_update_note_bare_log_blocked():
    rc = _run_hook({
        "tool_name": "mcp__forge-brain__update_note",
        "tool_input": {"file": "log", "content": "new content"},
    })
    assert rc == 2


def test_e2e_delete_note_bare_log_blocked():
    rc = _run_hook({
        "tool_name": "mcp__forge-brain__delete_note",
        "tool_input": {"file": "log"},
    })
    assert rc == 2


def test_e2e_move_note_bare_log_blocked():
    rc = _run_hook({
        "tool_name": "mcp__forge-brain__move_note",
        "tool_input": {"file": "log", "new_path": "vault/claude-forge/a/log.md"},
    })
    assert rc == 2


def test_e2e_update_property_bare_log_blocked():
    rc = _run_hook({
        "tool_name": "mcp__forge-brain__update_property",
        "tool_input": {"file": "log", "name": "derniere-maj", "value": "2026-05-28"},
    })
    assert rc == 2


def test_e2e_bulk_update_property_bare_log_blocked():
    rc = _run_hook({
        "tool_name": "mcp__forge-brain__bulk_update_property",
        "tool_input": {"file": "log", "name": "derniere-maj", "value": "2026-05-28"},
    })
    assert rc == 2


def test_e2e_insert_section_exact_path_allowed():
    # Tool-agnostic check: exact path must pass on a non-append_note tool.
    rc = _run_hook({
        "tool_name": "mcp__forge-brain__insert_section",
        "tool_input": {
            "file": "vault/claude-forge/log.md",
            "marker": "## Notes",
            "content": "x",
        },
    })
    assert rc == 0
