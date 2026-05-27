#!/usr/bin/env python3
"""Adversarial + characterization tests for delegate-guard.py.

SCOPE DECLARED BY THE HOOK (delegate-guard.py docstring + PROTECTED dict):
  Wired on matcher "Edit|Write|MultiEdit" (settings.json). Blocks DIRECT edits
  of these targets, ONLY inside the claude-forge project, UNLESS a specialist
  bypass applies:
    - SKILL.md            -> skill-creator
    - CLAUDE.md           -> claudemd-optimizer
    - .claude/agents/*.md -> agent-creator
  Bypass sources (first match wins): agent_type, agent_id, CLAUDE_AGENT env,
  transcript parsing. Typo pass-through: Edit with both strings < 20 chars.
  Exempt skill dirs (external/kepano): json-canvas, defuddle, obsidian-cli,
  obsidian-markdown, obsidian-bases.

WHAT THESE TESTS VERIFY:
  - Protected paths are detected across path variants (separators, casing,
    nesting) — adversarial path tricks.
  - Bypass logic: legitimate specialists pass; non-specialists are blocked.
  - Regression guard: the former substring-match-on-agent_id bug (fixed
    2026-05-27) stays fixed — exact match only.

WHAT THESE TESTS DO *NOT* VERIFY (out-of-scope by design):
  - Bash bypasses (echo > file, sed -i, tee, cp, python -c open(...,'w')):
    delegate-guard is wired on Edit|Write|MultiEdit only, NEVER on Bash. A bash
    redirect carries no `file_path`, so this hook cannot and does not see it.
    That gap belongs to a Bash-matcher hook, not here. Enumerated in
    test_documented_bash_bypass_gap.
  - Editing settings.json or .claude/hooks/*.py: NOT in PROTECTED by design.

Run: py -m pytest tests/test_delegate_guard.py -v
"""
import importlib.util
import os
import sys

_hook_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "delegate-guard.py",
)
_spec = importlib.util.spec_from_file_location("delegate_guard", _hook_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

required_agent = _mod.required_agent
agent_bypass_active = _mod.agent_bypass_active
is_inside_forge = _mod.is_inside_forge
is_agent_md = _mod.is_agent_md
is_exempt_skill = _mod.is_exempt_skill
is_typo_edit = _mod.is_typo_edit
normalize = _mod.normalize
FORGE = _mod.FORGE_PROJECT_DIR


def _p(rel):
    """Build an in-forge normalized path from a repo-relative tail."""
    return FORGE + "/" + rel.lstrip("/")


# ===========================================================================
# PROTECTED DETECTION — path-variant adversarial cases (>=3 per target)
# ===========================================================================

def test_agent_md_canonical():
    assert required_agent(_p(".claude/agents/foo.md")) == "agent-creator"


def test_agent_md_backslash_separators():
    """Adversarial: Windows backslashes must normalize and still be caught."""
    raw = FORGE.replace("/", "\\") + "\\.claude\\agents\\foo.md"
    assert required_agent(normalize(raw)) == "agent-creator"


def test_agent_md_nested_deeper_not_caught():
    """Characterization: is_agent_md requires parent dir == 'agents' exactly.
    A file under agents/sub/foo.md has parent 'sub' → NOT caught (documents the rule)."""
    assert required_agent(_p(".claude/agents/sub/foo.md")) is None


def test_skill_md_canonical():
    assert required_agent(_p(".claude/skills/bar/SKILL.md")) == "skill-creator"


def test_skill_md_basename_only_match():
    """Characterization: PROTECTED matches on basename SKILL.md anywhere in forge.
    Even outside a skills/ dir, a file named SKILL.md is protected."""
    assert required_agent(_p("random/place/SKILL.md")) == "skill-creator"


def test_skill_md_lowercase_not_matched():
    """Characterization: 'skill.md' lowercase != 'SKILL.md' → not protected (case-sensitive basename)."""
    assert required_agent(_p(".claude/skills/bar/skill.md")) is None


def test_claude_md_canonical():
    assert required_agent(_p("CLAUDE.md")) == "claudemd-optimizer"


def test_claude_md_in_subdir():
    """Characterization: CLAUDE.md matched by basename anywhere in forge."""
    assert required_agent(_p("some/nested/CLAUDE.md")) == "claudemd-optimizer"


# ===========================================================================
# EXEMPT SKILLS — external kepano skills must NOT be protected
# ===========================================================================

def test_exempt_json_canvas():
    assert required_agent(_p(".claude/skills/json-canvas/SKILL.md")) is None


def test_exempt_obsidian_markdown():
    assert required_agent(_p(".claude/skills/obsidian-markdown/SKILL.md")) is None


def test_non_exempt_skill_still_protected():
    """A non-exempt skill SKILL.md remains protected (contrast with exempt)."""
    assert required_agent(_p(".claude/skills/forge-status/SKILL.md")) == "skill-creator"


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
# BYPASS LOGIC — legitimate specialists pass; impostors blocked
# ===========================================================================

def test_bypass_agent_type_legit():
    ok, _src = agent_bypass_active({"agent_type": "skill-creator"})
    assert ok is True


def test_bypass_agent_type_impostor_blocked():
    """Adversarial: a non-specialist agent_type must NOT bypass."""
    ok, _src = agent_bypass_active({"agent_type": "evil-agent"})
    assert ok is False


def test_bypass_agent_id_legit():
    ok, _src = agent_bypass_active({"agent_id": "agent-creator"})
    assert ok is True


def test_bypass_empty_payload_blocked():
    """Adversarial: empty payload (no identity) must NOT bypass — block by default."""
    ok, _src = agent_bypass_active({})
    assert ok is False


def test_bypass_unrelated_fields_blocked():
    """Adversarial: payload with unrelated fields must NOT bypass."""
    ok, _src = agent_bypass_active({"tool_name": "Edit", "foo": "skill-creator-ish"})
    assert ok is False


def test_bypass_claude_agent_env(monkeypatch=None):
    """Adversarial/characterization: CLAUDE_AGENT env var grants bypass (legacy fallback)."""
    os.environ["CLAUDE_AGENT"] = "hook-creator"
    try:
        ok, _src = agent_bypass_active({})
        assert ok is True
    finally:
        del os.environ["CLAUDE_AGENT"]


def test_bypass_claude_agent_env_impostor():
    """Adversarial: CLAUDE_AGENT with non-specialist value must NOT bypass."""
    os.environ["CLAUDE_AGENT"] = "not-a-specialist"
    try:
        ok, _src = agent_bypass_active({})
        assert ok is False
    finally:
        del os.environ["CLAUDE_AGENT"]


# ===========================================================================
# REGRESSION GUARD — substring match on agent_id was a bug, now fixed
# ===========================================================================

def test_agent_id_substring_does_not_grant_bypass():
    """REGRESSION GUARD: an agent_id that merely CONTAINS a specialist name as
    substring must NOT grant bypass — only an exact match does.

    History: until 2026-05-27, delegate-guard had a substring match on agent_id
    that granted bypass to any agent_id containing a specialist name (e.g.
    'totally-unrelated-skill-creator-suffix'). Attack surface was low (agent_id
    is set by the Anthropic harness, not user-controllable) but the match was
    over-permissive. Hardened to exact-match. This test pins the FIXED behavior;
    if it ever fails, the substring bug has been reintroduced.
    """
    ok, _src = agent_bypass_active({"agent_id": "totally-unrelated-skill-creator-suffix"})
    assert ok is False  # fixed: substring no longer bypasses


def test_agent_id_exact_match_still_grants_bypass():
    """Companion to the regression guard: an EXACT agent_id match still bypasses."""
    ok, src = agent_bypass_active({"agent_id": "skill-creator"})
    assert ok is True
    assert "agent_id=" in src


# ===========================================================================
# TYPO PASS-THROUGH — Edit with both strings < 20 chars
# ===========================================================================

def test_typo_edit_short_both():
    assert is_typo_edit({"old_string": "abc", "new_string": "abd"}) is True


def test_typo_edit_long_new_blocked():
    """Adversarial: smuggle a long change through typo path — new_string >= 20 → NOT a typo."""
    assert is_typo_edit({"old_string": "x", "new_string": "x" * 25}) is False


def test_typo_edit_long_old_blocked():
    assert is_typo_edit({"old_string": "y" * 30, "new_string": "z"}) is False


# ===========================================================================
# HAPPY PATH (<=25%) — non-protected files pass
# ===========================================================================

def test_happy_vault_note_passes():
    """A vault note is not a protected component → required_agent None."""
    assert required_agent(_p("vault/claude-forge/Knowledge/erreurs/x.md")) is None


def test_happy_readme_passes():
    """README.md at root is not protected."""
    assert required_agent(_p("README.md")) is None


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
    # No file_path → required_agent has nothing to act on. Documented, not asserted.
    assert all(isinstance(g, str) for g in gaps)
    print(f"\n  [INFO] Bash bypass vectors out of delegate-guard scope: {len(gaps)} documented")


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
