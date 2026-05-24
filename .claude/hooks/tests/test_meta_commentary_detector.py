#!/usr/bin/env python3
"""Adversarial tests for meta-commentary-detector.py.

7 adversarial cases (each maps to a documented infraction).
3 legitimate cases that must PASS.
1 bypass-attempt case (Python comment with "Source:").

Run: py tests/test_meta_commentary_detector.py
"""
import sys
import os

# Import hook module — filename uses hyphens, use importlib
import importlib.util

_hook_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "meta-commentary-detector.py",
)
_spec = importlib.util.spec_from_file_location("meta_commentary_detector", _hook_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

check_content = _mod.check_content
is_in_scope = _mod.is_in_scope


def assert_blocks(name: str, content: str, path: str = ".claude/rules/test.md") -> None:
    violations = check_content(content, path)
    assert violations, (
        f"[FAIL] Expected BLOCK on {name!r} — got no violations\n"
        f"  path={path!r}\n  content={content!r}"
    )
    print(f"  [PASS] BLOCKED as expected: {name!r}  ({violations[0][1]})")


def assert_passes(name: str, content: str, path: str = ".claude/rules/test.md") -> None:
    violations = check_content(content, path)
    assert not violations, (
        f"[FAIL] Expected PASS on {name!r} — got violations: {violations}\n"
        f"  path={path!r}\n  content={content!r}"
    )
    print(f"  [PASS] Allowed as expected: {name!r}")


def test_adversarial_italicized_tradeoff() -> None:
    """BLOCKING-1: italic softener after a directive bullet."""
    content = (
        "- Toujours utiliser skill-creator pour modifier une skill\n"
        "*Note: dans les cas urgents on peut déroger si contexte précis et validé*\n"
    )
    assert_blocks("italic-tradeoff after bullet", content)


def test_adversarial_source_label() -> None:
    """BLOCKING-2a: explicit Source: line."""
    content = "Appliquer X.\nSource: [[comment-creer-hook]]\n"
    assert_blocks("Source: attribution line", content)


def test_adversarial_cf_doctrine() -> None:
    """BLOCKING-2b: 'Cf doctrine' inline reference."""
    content = "Utiliser Y (cf doctrine 22 mai) dans ce contexte.\n"
    assert_blocks("Cf doctrine inline", content)


def test_adversarial_daprès_typographic() -> None:
    """BLOCKING-2c: D'après with typographic apostrophe (two variants)."""
    content_right = "D’après Boris, utiliser /compact.\n"
    content_left = "D‘après Thariq, ceci est vrai.\n"
    assert_blocks("D'après typographic right quote", content_right)
    assert_blocks("D'après typographic left quote", content_left)


def test_adversarial_tip_attribution() -> None:
    """BLOCKING-3a: '= tip #N Name' inline attribution."""
    content = "**Vérification = tip #1 Boris**\n"
    assert_blocks("= tip #1 Boris attribution", content)


def test_adversarial_author_emdash() -> None:
    """BLOCKING-3b: '— FirstName LastName' author attribution at end of line."""
    content = "Éviter les sessions longues — Boris Cherny\n"
    assert_blocks("em-dash author attribution", content)


def test_adversarial_arxiv_citation() -> None:
    """BLOCKING-4: parenthesized academic citation (UCL arXiv ID)."""
    content = "Sweet spot CLAUDE.md / prompts agents : 150-300 mots. Au-delà, dégradation quadratique (UCL 2601.00880)\n"
    assert_blocks("UCL arXiv citation in parens", content)


def test_adversarial_since_justification() -> None:
    """BLOCKING-5: historical justification with date inside parens."""
    content = "## Vault path (pattern Karpathy strict depuis 22 mai)\n"
    assert_blocks("since-justification in section heading", content)


def test_adversarial_validation_attribution() -> None:
    """BLOCKING-6: validation attribution in parens — (validé 21 mai) style."""
    content = "**Modèles** : Sonnet exécution, Opus jugement (validé 21 mai).\n"
    assert_blocks("validation-attribution (validé 21 mai)", content)


# --- Legitimate cases that MUST pass ---

def test_legitimate_frontmatter_excluded() -> None:
    """Frontmatter YAML block must be excluded from scanning."""
    content = (
        "---\n"
        "aliases:\n"
        "  - Source: quelque-chose\n"
        "tags:\n"
        "  - '#type/hook'\n"
        "---\n"
        "Corps du fichier sans méta-commentaire.\n"
    )
    assert_passes("frontmatter YAML block excluded", content)


def test_legitimate_bare_wikilink() -> None:
    """A bare wikilink on its own line is always allowed."""
    content = "[[comment-creer-hook]]\n"
    assert_passes("bare wikilink allowed", content)


def test_legitimate_short_paren_disambiguation() -> None:
    """Parenthetical of <=3 words is a valid disambiguation — must pass."""
    content = "Utiliser auto mode (pas auto) dans ce contexte.\n"
    assert_passes("short paren disambiguation (3 words)", content)


def test_legitimate_vault_path_excluded() -> None:
    """Files under vault/ are explicitly excluded from scope."""
    content = "Source: [[erreur-meta-commentaires-composants]]\n"
    path = "vault/claude-forge/Knowledge/erreurs/erreur-meta.md"
    assert_passes("vault path excluded from scope", content, path=path)


# --- Bypass attempt ---

def test_bypass_python_comment_with_source() -> None:
    """Python comment containing 'Source:' in a hook file MUST be blocked.

    Rationale: doctrine says 'why lives in the vault', even in hook scripts.
    A comment 'Source: [[X]]' is an attribution that should live in the vault, not inline.
    """
    content = "# Source: [[comment-creer-hook]]\ndef main(): pass\n"
    path = ".claude/hooks/test.py"
    assert_blocks("python comment with Source: in hook file", content, path=path)


# --- Scope check ---

def test_scope_detection() -> None:
    in_scope = [
        "/path/to/project/CLAUDE.md",
        "/path/.claude/agents/my-agent.md",
        "/path/.claude/skills/my-skill/SKILL.md",
        "/path/.claude/rules/my-rule.md",
        "/path/.claude/hooks/my-hook.py",
    ]
    out_of_scope = [
        "/path/vault/claude-forge/Knowledge/erreurs/test.md",
        "/path/references/my-ref.md",
        "/path/to/RECAP.md",
        "/path/to/CHANGELOG.md",
        "/path/src/main.py",
        "/path/docs/README.md",
    ]
    for p in in_scope:
        assert is_in_scope(p), f"[FAIL] Expected in-scope: {p!r}"
        print(f"  [PASS] in-scope: {p!r}")
    for p in out_of_scope:
        assert not is_in_scope(p), f"[FAIL] Expected out-of-scope: {p!r}"
        print(f"  [PASS] out-of-scope: {p!r}")


if __name__ == "__main__":
    failures = []
    tests = [
        test_adversarial_italicized_tradeoff,
        test_adversarial_source_label,
        test_adversarial_cf_doctrine,
        test_adversarial_daprès_typographic,
        test_adversarial_tip_attribution,
        test_adversarial_author_emdash,
        test_adversarial_arxiv_citation,
        test_adversarial_since_justification,
        test_adversarial_validation_attribution,
        test_legitimate_frontmatter_excluded,
        test_legitimate_bare_wikilink,
        test_legitimate_short_paren_disambiguation,
        test_legitimate_vault_path_excluded,
        test_bypass_python_comment_with_source,
        test_scope_detection,
    ]

    for test_fn in tests:
        print(f"\n{test_fn.__name__}")
        try:
            test_fn()
        except AssertionError as e:
            print(f"  {e}", file=sys.stderr)
            failures.append(test_fn.__name__)
        except Exception as e:
            print(f"  [ERROR] {e}", file=sys.stderr)
            failures.append(test_fn.__name__)

    print(f"\n{'='*60}")
    if failures:
        print(f"FAILED: {len(failures)}/{len(tests)} — {failures}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"ALL PASSED: {len(tests)}/{len(tests)}")
        sys.exit(0)
