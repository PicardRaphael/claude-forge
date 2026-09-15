#!/usr/bin/env python3
"""Adversarial + characterization tests for delegate-guard.py.

SCOPE DECLARED BY THE HOOK (delegate-guard.py docstring + PROTECTED dict):
  Wired on matcher "Edit|Write|MultiEdit" (settings.json). Blocks DIRECT edits
  of these targets, ONLY inside the claude-forge project, UNLESS a specialist
  bypass applies:
    - SKILL.md            -> skill-creator   (except external/kepano skills)
    - CLAUDE.md           -> claudemd-creator
    - .claude/agents/*.md -> subagent-creator
    - .claude/hooks/*.py  -> hook-creator     (except the guard itself + test_*.py)

  BYPASS MODEL (refactored 2026-06-06, CC 2.1.167):
    The ONLY sanctioned bypass is the transcript `attributionSkill` matching the
    REQUIRED specialist for THIS file type (strict, defense in depth). Skills are
    NOT sub-agents, so agent_type/agent_id are null when a skill runs — the hook
    parses attributionSkill from the transcript tail instead. Spoofable signals
    (CLAUDE_AGENT env var, agent_type/agent_id payload fields) were DELIBERATELY
    removed: they are circumvention vectors, not legitimate delegation.

WHAT THESE TESTS VERIFY:
  - Protected paths are detected across path variants (separators, casing,
    nesting) — adversarial path tricks (pure-function level).
  - Bypass logic END-TO-END via subprocess + forged stdin + a temp transcript:
    the right specialist passes, the WRONG specialist (a real specialist that
    does not own this file type) is still BLOCKED, and no-identity blocks.
  - Regression guard: a substring-only attributionSkill must NOT bypass — only
    an exact match for the required specialist does.

WHAT THESE TESTS DO *NOT* VERIFY (out-of-scope by design):
  - Bash bypasses (echo > file, sed -i, tee, cp, python -c open(...,'w')):
    delegate-guard is wired on Edit|Write|MultiEdit only, NEVER on Bash. A bash
    redirect carries no `file_path`, so this hook cannot and does not see it.
    That gap belongs to a Bash-matcher hook, not here. Enumerated in
    test_documented_bash_bypass_gap.
  - Editing settings.json: NOT in PROTECTED by design.

Run: py -m pytest tests/test_delegate_guard.py -v
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

_HOOK_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "delegate-guard.py",
)
_spec = importlib.util.spec_from_file_location("delegate_guard", _HOOK_PATH)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

required_specialist = _mod.required_specialist
is_inside_forge = _mod.is_inside_forge
is_agent_md = _mod.is_agent_md
is_exempt_skill = _mod.is_exempt_skill
is_typo_change = _mod.is_typo_change
is_security_critical = _mod.is_security_critical
active_skill_from_transcript = _mod.active_skill_from_transcript
skill_invocations_from_transcript = _mod.skill_invocations_from_transcript
normalize = _mod.normalize
FORGE = _mod.FORGE_PROJECT_DIR


def _p(rel):
    """Build an in-forge normalized path from a repo-relative tail."""
    return FORGE + "/" + rel.lstrip("/")


def _run_hook(file_path, tool_name="Edit", attribution_skill=None, tool_input=None):
    """Invoke the hook end-to-end via subprocess with forged stdin.

    Builds a temp transcript holding a single assistant event carrying
    attribution_skill (or no attributionSkill when None), wires it into the
    stdin payload, runs `py delegate-guard.py`, and returns (returncode, stderr).
    This exercises the REAL bypass path (main() reads the transcript), which the
    pure functions alone cannot cover since the bypass is inline in main().
    """
    if tool_input is None:
        tool_input = {"file_path": file_path, "old_string": "a" * 30, "new_string": "b" * 30}
    else:
        tool_input = {"file_path": file_path, **tool_input}

    transcript_path = ""
    tmp = None
    try:
        if attribution_skill is not None:
            tmp = tempfile.NamedTemporaryFile(
                mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
            )
            event = {"type": "assistant", "attributionSkill": attribution_skill}
            tmp.write(json.dumps(event) + "\n")
            tmp.close()
            transcript_path = tmp.name

        payload = {
            "tool_name": tool_name,
            "tool_input": tool_input,
            "transcript_path": transcript_path,
        }
        proc = subprocess.run(
            ["py", "-3", _HOOK_PATH],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
        )
        return proc.returncode, proc.stderr
    finally:
        if tmp is not None:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass


# ===========================================================================
# PROTECTED DETECTION — path-variant adversarial cases (>=3 per target)
# ===========================================================================

def test_agent_md_canonical():
    assert required_specialist(_p(".claude/agents/foo.md")) == "subagent-creator"


def test_agent_md_backslash_separators():
    """Adversarial: Windows backslashes must normalize and still be caught."""
    raw = FORGE.replace("/", "\\") + "\\.claude\\agents\\foo.md"
    assert required_specialist(normalize(raw)) == "subagent-creator"


def test_agent_md_nested_deeper_not_caught():
    """Characterization: is_agent_md requires parent dir == 'agents' exactly.
    A file under agents/sub/foo.md has parent 'sub' → NOT caught (documents the rule)."""
    assert required_specialist(_p(".claude/agents/sub/foo.md")) is None


def test_skill_md_canonical():
    assert required_specialist(_p(".claude/skills/bar/SKILL.md")) == "skill-creator"


def test_skill_md_basename_only_match():
    """Characterization: SKILL.md is matched only when a 'skills' segment is present.
    A SKILL.md outside any skills/ dir is NOT protected (is_skill_md requires 'skills')."""
    assert required_specialist(_p("random/place/SKILL.md")) is None


def test_skill_md_lowercase_not_matched():
    """Characterization: 'skill.md' lowercase != 'SKILL.md' → not protected (case-sensitive basename)."""
    assert required_specialist(_p(".claude/skills/bar/skill.md")) is None


def test_claude_md_canonical():
    assert required_specialist(_p("CLAUDE.md")) == "claudemd-creator"


def test_claude_md_in_subdir():
    """Characterization: CLAUDE.md matched by basename anywhere in forge."""
    assert required_specialist(_p("some/nested/CLAUDE.md")) == "claudemd-creator"


def test_settings_and_mcp_config_are_protected_without_typo_bypass():
    for path in (".claude/settings.json", ".claude/settings.local.json", ".mcp.json", ".codex/hooks.json"):
        normalized = _p(path)
        assert required_specialist(normalized) == "hook-creator"
        assert is_security_critical(normalized) is True


def test_memory_index_requires_a_memory_lifecycle_skill():
    path = _p("memory/MEMORY.md")
    assert required_specialist(path) == "done|clean-memory|project-memory"
    assert is_security_critical(path) is True


def test_memory_index_short_edit_without_lifecycle_skill_is_blocked():
    code, _ = _run_hook(
        _p("memory/MEMORY.md"),
        tool_input={"old_string": "# Memory Index", "new_string": "# Memory Registry"},
    )
    assert code == 2


def test_hook_py_canonical():
    """A .claude/hooks/*.py file is owned by hook-creator."""
    assert required_specialist(_p(".claude/hooks/some-guard.py")) == "hook-creator"


def test_hook_py_guard_itself_is_protected():
    assert required_specialist(_p(".claude/hooks/delegate-guard.py")) == "hook-creator"


def test_hook_py_test_file_exempt():
    """test_*.py under hooks/ is exempt (so this very suite can be edited freely)."""
    assert required_specialist(_p(".claude/hooks/tests/test_delegate_guard.py")) is None


# ===========================================================================
# EXEMPT SKILLS — external kepano skills must NOT be protected
# ===========================================================================

def test_exempt_json_canvas():
    assert required_specialist(_p(".claude/skills/json-canvas/SKILL.md")) is None


def test_exempt_obsidian_markdown():
    assert required_specialist(_p(".claude/skills/obsidian-markdown/SKILL.md")) is None


def test_non_exempt_skill_still_protected():
    """A non-exempt skill SKILL.md remains protected (contrast with exempt)."""
    assert required_specialist(_p(".claude/skills/forge-status/SKILL.md")) == "skill-creator"


# ===========================================================================
# OUT-OF-FORGE — paths outside the project are always allowed
# ===========================================================================

def test_outside_forge_agent_md_allowed():
    """Adversarial: an agents/*.md in ANOTHER repo must NOT be caught (per-repo scope)."""
    other = "c:/users/x/documents/other-repo/.claude/agents/foo.md"
    assert is_inside_forge(other) is False


def test_outside_forge_skill_md_allowed():
    other = "d:/projects/neo/.claude/skills/bar/SKILL.md"
    assert is_inside_forge(other) is False


def test_inside_forge_true():
    assert is_inside_forge(_p(".claude/agents/foo.md")) is True


# ===========================================================================
# attributionSkill PARSING — pure function over a forged transcript
# ===========================================================================

def test_active_skill_reads_latest_attribution():
    """active_skill_from_transcript returns the most recent attributionSkill."""
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8")
    try:
        tmp.write(json.dumps({"type": "assistant", "attributionSkill": "old-skill"}) + "\n")
        tmp.write(json.dumps({"type": "user"}) + "\n")
        tmp.write(json.dumps({"type": "assistant", "attributionSkill": "skill-creator"}) + "\n")
        tmp.close()
        assert active_skill_from_transcript(tmp.name) == "skill-creator"
    finally:
        os.unlink(tmp.name)


def test_active_skill_none_when_absent():
    """No attributionSkill anywhere in the tail → None (block by default upstream)."""
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8")
    try:
        tmp.write(json.dumps({"type": "assistant"}) + "\n")
        tmp.write(json.dumps({"type": "user"}) + "\n")
        tmp.close()
        assert active_skill_from_transcript(tmp.name) is None
    finally:
        os.unlink(tmp.name)


def test_active_skill_missing_file_fail_open_none():
    """Unreadable transcript path → None, never raises (fail-open)."""
    assert active_skill_from_transcript("/no/such/transcript.jsonl") is None


# ===========================================================================
# STACKED SKILLS — nested Skill(<specialist>) invocation in the tail unlocks
# (CC >= 2.1.202 keeps the turn's FIRST skill as attributionSkill)
# ===========================================================================

def test_nested_skill_invocation_from_older_turn_is_rejected():
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8")
    try:
        tmp.write(json.dumps({"type": "assistant", "attributionSkill": "forge-review"}) + "\n")
        tmp.write(json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Skill", "input": {"skill": "skill-creator"}}]}}) + "\n")
        for i in range(30):
            tmp.write(json.dumps({"type": "user"}) + "\n")
        tmp.write(json.dumps({"type": "assistant", "attributionSkill": "forge-review"}) + "\n")
        tmp.close()
        invoked = skill_invocations_from_transcript(tmp.name)
        assert "skill-creator" not in invoked
        assert active_skill_from_transcript(tmp.name) == "forge-review"
    finally:
        os.unlink(tmp.name)


def test_nested_invocation_strict_ownership():
    """An invocation of a DIFFERENT skill never unlocks the required specialist."""
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8")
    try:
        tmp.write(json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Skill", "input": {"skill": "cc-news"}}]}}) + "\n")
        tmp.close()
        invoked = skill_invocations_from_transcript(tmp.name)
        assert "skill-creator" not in invoked
        assert invoked == {"cc-news"}
    finally:
        os.unlink(tmp.name)


def test_skill_invocations_missing_file_fail_open_empty():
    """Unreadable transcript path → empty set, never raises (fail-open)."""
    assert skill_invocations_from_transcript("/no/such/transcript.jsonl") == set()


# ===========================================================================
# BYPASS LOGIC (end-to-end) — only the RIGHT specialist passes; impostors block
# ===========================================================================

def test_bypass_right_specialist_passes():
    """attributionSkill == required specialist for this file → bypass (exit 0)."""
    code, _err = _run_hook(_p(".claude/skills/bar/SKILL.md"), attribution_skill="skill-creator")
    assert code == 0


def test_bypass_agent_md_right_specialist_passes():
    code, _err = _run_hook(_p(".claude/agents/foo.md"), attribution_skill="subagent-creator")
    assert code == 0


def test_bypass_wrong_specialist_blocked():
    """DEFENSE IN DEPTH: a REAL specialist that does not OWN this file type must
    NOT unlock it. skill-creator may not unlock CLAUDE.md → still BLOCKED (exit 2).
    This is the core of the strict bypass model and was never tested before."""
    code, err = _run_hook(_p("CLAUDE.md"), attribution_skill="skill-creator")
    assert code == 2
    assert "claudemd-creator" in err


def test_bypass_no_attribution_blocked():
    """Adversarial: no active skill at all (no transcript) → block by default (exit 2)."""
    code, _err = _run_hook(_p(".claude/agents/foo.md"), attribution_skill=None)
    assert code == 2


def test_bypass_claude_agent_env_does_not_unlock():
    """Adversarial/REGRESSION: the legacy CLAUDE_AGENT env var no longer grants
    bypass (spoofable signal removed 2026-06-06). Even set to a real specialist,
    the file stays BLOCKED when attributionSkill is absent."""
    os.environ["CLAUDE_AGENT"] = "subagent-creator"
    try:
        code, _err = _run_hook(_p(".claude/agents/foo.md"), attribution_skill=None)
        assert code == 2
    finally:
        del os.environ["CLAUDE_AGENT"]


# ===========================================================================
# REGRESSION GUARD — substring/partial match must NOT grant bypass
# ===========================================================================

def test_attribution_substring_does_not_grant_bypass():
    """REGRESSION GUARD: an attributionSkill that merely CONTAINS the specialist
    name as a substring must NOT bypass — only an EXACT match does.

    History: until 2026-05-27 a substring match on the agent identity granted
    bypass to any value containing a specialist name (e.g.
    'totally-unrelated-skill-creator-suffix'). Hardened to exact match. The
    refactored hook compares `active_skill == required` (exact). This pins it."""
    code, _err = _run_hook(
        _p(".claude/skills/bar/SKILL.md"),
        attribution_skill="totally-unrelated-skill-creator-suffix",
    )
    assert code == 2  # substring no longer bypasses


def test_attribution_exact_match_still_grants_bypass():
    """Companion to the regression guard: an EXACT attributionSkill match bypasses."""
    code, _err = _run_hook(_p(".claude/skills/bar/SKILL.md"), attribution_skill="skill-creator")
    assert code == 0


# ===========================================================================
# TYPO PASS-THROUGH — Edit/MultiEdit with all changes < 20 chars
# ===========================================================================

def test_typo_change_short_both():
    assert is_typo_change("Edit", {"old_string": "abc", "new_string": "abd"}) is True


def test_typo_change_long_new_blocked():
    """Adversarial: smuggle a long change through typo path — new_string >= 20 → NOT a typo."""
    assert is_typo_change("Edit", {"old_string": "x", "new_string": "x" * 25}) is False


def test_typo_change_long_old_blocked():
    assert is_typo_change("Edit", {"old_string": "y" * 30, "new_string": "z"}) is False


def test_typo_change_multiedit_all_short():
    """MultiEdit is a typo only if EVERY edit is below threshold."""
    edits = [{"old_string": "a", "new_string": "b"}, {"old_string": "cc", "new_string": "dd"}]
    assert is_typo_change("MultiEdit", {"edits": edits}) is True


def test_typo_change_multiedit_one_long_blocked():
    """Adversarial: one long edit among short ones → NOT a typo (no smuggling)."""
    edits = [{"old_string": "a", "new_string": "b"}, {"old_string": "c", "new_string": "z" * 40}]
    assert is_typo_change("MultiEdit", {"edits": edits}) is False


def test_typo_change_write_is_never_typo():
    """Write is not Edit/MultiEdit → is_typo_change returns False (no string-length escape)."""
    assert is_typo_change("Write", {"content": "x"}) is False


# ===========================================================================
# HAPPY PATH — non-protected files pass
# ===========================================================================

def test_happy_vault_note_passes():
    """A vault note is not a protected component → required_specialist None."""
    assert required_specialist(_p("vault/claude-forge/Knowledge/erreurs/x.md")) is None


def test_happy_readme_passes():
    """README.md at root is not protected."""
    assert required_specialist(_p("README.md")) is None


# ===========================================================================
# DOCUMENTED GAP — bash bypasses (out of scope by hook wiring)
# ===========================================================================

def test_documented_bash_bypass_gap():
    """delegate-guard is wired on Edit|Write|MultiEdit ONLY. Bash redirects
    (echo > , sed -i, tee, cp, mv, python -c open(...,'w')) carry no file_path
    and are NEVER seen by this hook. This is an architectural boundary, not a
    bug in delegate-guard. Closing it requires a separate Bash-matcher hook.

    This test documents the boundary; there is nothing to assert against
    delegate-guard's pure functions because they operate on file_path which a
    bash command does not provide.
    """
    gaps = [
        "echo '...' > .claude/agents/x.md",
        "sed -i 's/a/b/' .claude/agents/x.md",
        "cat <<EOF > .claude/agents/x.md",
        "tee .claude/agents/x.md",
        "cp /tmp/forge.md .claude/agents/x.md",
        "python -c \"open('.claude/agents/x.md','w').write('x')\"",
    ]
    # No file_path → required_specialist has nothing to act on. Documented, not asserted.
    assert all(isinstance(g, str) for g in gaps)
    print(f"\n  [INFO] Bash bypass vectors out of delegate-guard scope: {len(gaps)} documented")


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
