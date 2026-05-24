"""Tests for lint_vault wikilink exclusions and # section handling."""

from src.tools.brain import _is_lint_excluded_wikilink


def test_feedback_prefix_excluded():
    assert _is_lint_excluded_wikilink("feedback_audit_claims_after_brief")
    assert _is_lint_excluded_wikilink("feedback_workaround_sediment")


def test_reference_prefix_excluded():
    assert _is_lint_excluded_wikilink("reference_seuils_canoniques")


def test_user_project_prefixes_excluded():
    assert _is_lint_excluded_wikilink("user_raphael_profile")
    assert _is_lint_excluded_wikilink("project_neo_ia")


def test_example_wikilinks_excluded():
    assert _is_lint_excluded_wikilink("note")
    assert _is_lint_excluded_wikilink("note a")
    assert _is_lint_excluded_wikilink("erreur-foo")
    assert _is_lint_excluded_wikilink("wikilink")


def test_agent_names_excluded():
    assert _is_lint_excluded_wikilink("agent-creator")
    assert _is_lint_excluded_wikilink("devils-advocate")
    assert _is_lint_excluded_wikilink("vault-maintainer")


def test_real_note_not_excluded():
    assert not _is_lint_excluded_wikilink("methode-analyser-repo")
    assert not _is_lint_excluded_wikilink("comment-creer-skill")
    assert not _is_lint_excluded_wikilink("boris cherny")


def test_case_insensitive_via_caller():
    # Caller lowercases before checking
    assert _is_lint_excluded_wikilink("note")  # lowercase
    # The caller is responsible for lowercasing — uppercase passed through is_excluded
    # would not match. This tests the contract: input must be lowercased.
    assert not _is_lint_excluded_wikilink("Note")  # raw stem with capital
