#!/usr/bin/env python3
"""Block meta-commentary anti-patterns in forge components (.claude/, CLAUDE.md).

Scope: PreToolUse Write|Edit|MultiEdit on forge config files only.
Blocked patterns: italicized tradeoff lines, source attributions, author attributions,
parenthesized academic citations, historical justifications in titles.
Exclusions checked FIRST: vault/, Knowledge/, references/, RECAP.md, CHANGELOG.md.
Exceptions: YAML frontmatter, bare wikilinks, short parenthetical disambiguations (<=3 words).

Fail-open on parse errors (exit 0) — same convention as delegate-guard and security-guard.

Doctrine: [[erreur-meta-commentaires-composants]]
"""
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# File scope
# ---------------------------------------------------------------------------

# Files that MUST NOT be scanned — exclusions checked before scope match
EXCLUDED_PREFIXES = (
    "vault/",
    "vault\\",
    "knowledge/",
    "knowledge\\",
    "references/",
    "references\\",
)
EXCLUDED_SUFFIXES = ("RECAP.md", "recap.md", "CHANGELOG.md", "changelog.md")

# Files that MUST be scanned — scope match (after exclusions pass)
SCOPED_PATTERNS = (
    re.compile(r"(^|[/\\])CLAUDE\.md$"),
    re.compile(r"[/\\]\.claude[/\\]agents[/\\][^/\\]+\.md$"),
    re.compile(r"[/\\]\.claude[/\\]skills[/\\](.+?[/\\])?SKILL\.md$"),
    re.compile(r"[/\\]\.claude[/\\]rules[/\\][^/\\]+\.md$"),
    re.compile(r"[/\\]\.claude[/\\]hooks[/\\][^/\\]+$"),
)


def is_excluded(path: str) -> bool:
    p = path.replace("\\", "/").lower()
    # Check by prefix (relative to any common prefix)
    for prefix in EXCLUDED_PREFIXES:
        norm_prefix = prefix.replace("\\", "/").lower()
        if norm_prefix in p:
            return True
    # Check by suffix
    base = p.rsplit("/", 1)[-1]
    for suffix in EXCLUDED_SUFFIXES:
        if base == suffix.lower():
            return True
    return False


def is_in_scope(path: str) -> bool:
    if is_excluded(path):
        return False
    p = path.replace("\\", "/")
    for pat in SCOPED_PATTERNS:
        if pat.search(p):
            return True
    return False


# ---------------------------------------------------------------------------
# Frontmatter detection
# ---------------------------------------------------------------------------

def strip_frontmatter(text: str) -> tuple[str, int]:
    """Return (body_without_frontmatter, line_offset_of_body).

    If the file starts with --- ... ---, body starts after it.
    Returns the full text and offset 0 if no frontmatter.
    """
    lines = text.splitlines(keepends=True)
    if not lines or not lines[0].strip() == "---":
        return text, 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            # i is the closing --- line; body starts at i+1
            return "".join(lines[i + 1:]), i + 1
    # Unclosed frontmatter — treat entire file as frontmatter, no body to scan
    return "", len(lines)


# ---------------------------------------------------------------------------
# Pattern detection
# ---------------------------------------------------------------------------

# Pre-compiled patterns — names used in error output
PATTERNS: list[tuple[str, re.Pattern]] = [
    # 1. Italicized tradeoff / softener line after a bullet directive
    #    Matches a standalone *italic block* (20+ chars) preceded by a list item
    ("italicized-tradeoff", re.compile(
        r"(?m)^[ \t]*-[ \t]+.+\n[ \t]*\*[^*\n]{20,}\*[ \t]*$"
    )),
    # 2a. Source: label
    ("source-label", re.compile(r"(?m)^\s*Source\s*:", re.IGNORECASE)),
    # 2b. Cf doctrine
    ("cf-doctrine", re.compile(r"\bCf doctrine\b", re.IGNORECASE)),
    # 2c. D'après (straight apostrophe, typographic left/right)
    ("daprès", re.compile(r"\bD['‘’]apr[èe]s\b")),
    # 3a. Author attribution: = tip #N Name
    ("tip-attribution", re.compile(r"=\s*tip\s+#\d+\s+\w+")),
    # 3b. Author attribution: — FirstName LastName at end of line
    ("author-em-dash", re.compile(r"[—–]\s*[A-Z][a-z]+\s+[A-Z][a-z]+\s*$", re.MULTILINE)),
    # 4a. Parenthesized arXiv-style UCL citation
    ("ucl-arxiv-citation", re.compile(r"\(UCL\s+\d+[\.\d]+\)")),
    # 4b. Parenthesized arXiv ID
    ("arxiv-citation", re.compile(r"\(arXiv:\d+[\.\d]+\)")),
    # 5. Historical justification in heading/section — "since <date>" inside parens
    #    Resserré: exige un chiffre (jour/année) après "depuis"
    ("since-justification", re.compile(
        r"\([^)]{0,60}depuis\s+\d+[^)]{0,40}\)", re.IGNORECASE
    )),
    # 6. Validation attribution — "(validé N mot)" e.g. "(validé 21 mai)"
    ("validation-attribution", re.compile(r"\(validé\s+\d+\s+\w+", re.IGNORECASE)),
]

# Pattern for detecting a bare wikilink on a line — OK, no flag
_WIKILINK_ONLY = re.compile(r"^\s*\[\[[^\]]+\]\]\s*$")

# Parenthetical content — for disambiguation exception
_PAREN_CONTENT = re.compile(r"\(([^)]+)\)")


def _has_short_paren(text: str) -> bool:
    """Return True if ALL parens in text qualify as short disambiguations (<=3 words)."""
    parens = _PAREN_CONTENT.findall(text)
    return all(len(p.split()) <= 3 for p in parens) if parens else False


def _is_python_comment_line(line: str) -> bool:
    return line.strip().startswith("#")


# Patterns for which the "short paren <=3 words" exception does NOT apply.
# Academic citations and validation attributions are never valid disambiguations,
# even if the content is short (e.g. "UCL 2601.00880" = 2 words, "validé 21 mai" = 3 words).
_NO_PAREN_EXCEPTION = {"ucl-arxiv-citation", "arxiv-citation", "validation-attribution"}


def check_line(line: str, lineno: int, is_hook_file: bool) -> list[tuple[int, str, str]]:
    """Return list of (lineno, pattern_name, matched_text) violations for one line."""
    violations = []

    # Bare wikilink line — always OK
    if _WIKILINK_ONLY.match(line):
        return []

    # Python comment in hook files:
    # - If the comment line has no attribution keyword → skip (WHY non-obvious comments are OK)
    # - If it has an attribution keyword → scan the comment text for patterns
    if is_hook_file and _is_python_comment_line(line):
        comment_text = line.strip()
        attribution_markers = ["Source:", "D’apr", "’apr", "‘apr", "Cf doctrine"]
        has_attribution = any(m in comment_text for m in attribution_markers)
        if not has_attribution:
            return []
        # Attribution found — scan the comment body (text after #) for specific patterns
        comment_body = comment_text.lstrip("#").strip()
        for pattern_name, pattern in PATTERNS:
            if pattern_name == "italicized-tradeoff":
                continue
            if pattern.search(comment_body):
                violations.append((lineno, pattern_name, comment_body[:80]))
        return violations

    for pattern_name, pattern in PATTERNS:
        # Skip multi-line pattern (1) here — handled in check_content
        if pattern_name == "italicized-tradeoff":
            continue
        match = pattern.search(line)
        if not match:
            continue
        # Disambiguation exception: <=3 words in paren → skip patterns 2/5 ONLY
        # Academic citations (4a/4b) are NEVER exempt — they are always a violation
        if pattern_name not in _NO_PAREN_EXCEPTION and pattern_name in (
            "source-label", "cf-doctrine", "daprès",
            "since-justification",
        ):
            parens = _PAREN_CONTENT.findall(line)
            if parens:
                matched_text = match.group(0)
                # If the match falls entirely within a <=3-word paren, skip
                short_parens = [p for p in parens if len(p.split()) <= 3]
                if any(matched_text in p or matched_text.strip("()") in p for p in short_parens):
                    continue

        violations.append((lineno, pattern_name, match.group(0).strip()))

    return violations


def check_content(content: str, path: str) -> list[tuple[int, str, str]]:
    """Scan a full file content and return all violations.

    Returns [] if path is excluded (vault, Knowledge, references, RECAP, CHANGELOG).
    Exclusion guard here mirrors main() so tests calling check_content directly are consistent.
    """
    if is_excluded(path):
        return []
    # Match hook paths both absolute (…/.claude/hooks/…) and relative (.claude/hooks/…)
    is_hook = bool(re.search(r"(^|[/\\])\.claude[/\\]hooks[/\\]", path))

    body, offset = strip_frontmatter(content)
    lines = body.splitlines()
    violations = []

    # Pattern 1: multi-line — scan on body directly
    for m in PATTERNS[0][1].finditer(body):
        lineno = body[:m.start()].count("\n") + offset + 1
        violations.append((lineno, "italicized-tradeoff", m.group(0).strip()[:80]))

    # All other patterns: line-by-line
    for i, line in enumerate(lines):
        lineno = i + offset + 1
        violations.extend(check_line(line, lineno, is_hook))

    return violations


# ---------------------------------------------------------------------------
# Virtual file content — apply edit to on-disk content
# ---------------------------------------------------------------------------

def read_file_content(path: str) -> str | None:
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def apply_write(tool_input: dict) -> str | None:
    return tool_input.get("content")


def apply_edit(tool_input: dict, original: str) -> str | None:
    old = tool_input.get("old_string", "")
    new = tool_input.get("new_string", "")
    if old not in original:
        return new  # fallback: scan only the new string
    return original.replace(old, new, 1)


def apply_multiedit(tool_input: dict, original: str) -> str | None:
    content = original
    for edit in tool_input.get("edits", []):
        old = edit.get("old_string", "")
        new = edit.get("new_string", "")
        if old in content:
            replace_all = edit.get("replace_all", False)
            if replace_all:
                content = content.replace(old, new)
            else:
                content = content.replace(old, new, 1)
        else:
            # old not found — apply just the new string as fallback
            content = content + "\n" + new
    return content


def resolve_content(tool_name: str, tool_input: dict, file_path: str) -> str | None:
    """Return the post-edit content to scan."""
    if tool_name == "Write":
        return apply_write(tool_input)

    original = read_file_content(file_path)
    if original is None:
        # File doesn't exist yet — scan only the new content
        if tool_name == "Edit":
            return tool_input.get("new_string", "")
        if tool_name == "MultiEdit":
            parts = [e.get("new_string", "") for e in tool_input.get("edits", [])]
            return "\n".join(parts)
        return None

    if tool_name == "Edit":
        return apply_edit(tool_input, original)
    if tool_name == "MultiEdit":
        return apply_multiedit(tool_input, original)

    return None


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def self_test() -> None:
    """Run built-in regression tests. Exit 0 on pass, 1 on failure."""
    failures = []

    def expect_block(name: str, content: str, path: str = ".claude/rules/test.md") -> None:
        violations = check_content(content, path)
        if not violations:
            failures.append(f"FAIL (expected block): {name!r}")

    def expect_pass(name: str, content: str, path: str = ".claude/rules/test.md") -> None:
        violations = check_content(content, path)
        if violations:
            failures.append(f"FAIL (expected pass): {name!r} — got {violations}")

    # --- Cases that MUST be blocked ---
    expect_block(
        "italicized-tradeoff after bullet",
        "- Toujours utiliser skill-creator\n*Note : dans les cas urgents on peut déroger si contexte précis et validé*\n",
    )
    expect_block(
        "source-label line",
        "Appliquer X.\nSource: [[comment-creer-hook]]\n",
    )
    expect_block(
        "cf-doctrine inline",
        "Utiliser Y (cf doctrine 22 mai).\n",
    )
    expect_block(
        "daprès typographic apostrophe",
        "D’après Boris, utiliser /compact.\n",
    )
    expect_block(
        "tip-attribution = tip #1 Boris",
        "**Vérification = tip #1 Boris**\n",
    )
    expect_block(
        "author em-dash attribution",
        "Éviter les sessions longues — Boris Cherny\n",
    )
    expect_block(
        "ucl-arxiv-citation",
        "Dégradation quadratique (UCL 2601.00880).\n",
    )
    expect_block(
        "since-justification historical",
        "## Vault path (pattern Karpathy strict depuis 22 mai)\n",
    )
    # Python comment with Source: in hook file MUST be blocked
    expect_block(
        "python-comment-source-in-hook",
        "# Source: [[comment-creer-hook]]\ndef main(): pass\n",
        path=".claude/hooks/test.py",
    )

    # --- Cases that MUST pass ---
    expect_pass(
        "frontmatter is excluded",
        "---\naliases:\n  - Source: foo\ntags:\n  - '#type/hook'\n---\nBody text.\n",
    )
    expect_pass(
        "bare wikilink is OK",
        "[[comment-creer-hook]]\n",
    )
    expect_pass(
        "short paren disambiguation",
        "Utiliser auto mode (pas auto) dans ce contexte.\n",
    )
    expect_pass(
        "vault file is excluded",
        "Source: [[erreur-meta-commentaires-composants]]\n",
        path="vault/claude-forge/Knowledge/erreurs/erreur-meta.md",
    )
    expect_pass(
        "regular python comment without attribution",
        "# This does not contain attribution keywords\ndef main(): pass\n",
        path=".claude/hooks/test.py",
    )
    # Self-immunity: the hook body (excluding test strings) must not trip.
    # Tests in self_test() contain deliberate pattern examples as strings —
    # those are expected to be detected if scanned. We verify the non-test
    # portion only by checking a known-clean excerpt of the module header.
    clean_excerpt = (
        '#!/usr/bin/env python3\n'
        '"""Block meta-commentary anti-patterns in forge components.\n'
        '\n'
        'Fail-open on parse errors (exit 0).\n'
        '"""\n'
        'import json\n'
        'import re\n'
        'import sys\n'
        'from pathlib import Path\n'
    )
    viol = check_content(clean_excerpt, str(Path(__file__)).replace("\\", "/"))
    if viol:
        failures.append(f"FAIL (self-immunity excerpt): clean header tripped: {viol}")

    if failures:
        for f in failures:
            print(f, file=sys.stderr)
        sys.exit(1)
    else:
        print("meta-commentary-detector: all self-tests passed.", file=sys.stderr)
        sys.exit(0)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if "--self-test" in sys.argv:
        self_test()
        return

    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")

        if not file_path:
            sys.exit(0)

        if not is_in_scope(file_path):
            sys.exit(0)

        content = resolve_content(tool_name, tool_input, file_path)
        if content is None:
            sys.exit(0)

        violations = check_content(content, file_path)
        if not violations:
            sys.exit(0)

        lineno, pattern_name, matched = violations[0]
        print(
            f"BLOQUÉ: meta-commentaire interdit dans {file_path}\n"
            f"Ligne {lineno} : {matched!r}\n"
            f"Pattern détecté : {pattern_name}\n"
            f"Doctrine : voir vault [[erreur-meta-commentaires-composants]]\n"
            f"Le pourquoi vit dans le vault canonique, pas dans le composant.",
            file=sys.stderr,
        )
        sys.exit(2)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
