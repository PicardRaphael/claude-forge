"""Parse Obsidian .md files: frontmatter, aliases, tags, wikilinks."""

import logging
import re
from dataclasses import dataclass, field

import yaml

log = logging.getLogger(__name__)


@dataclass
class ParsedNote:
    file_stem: str
    path: str
    content: str
    frontmatter_raw: str
    aliases: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    wikilinks: list[str] = field(default_factory=list)
    lint_warnings: list[str] = field(default_factory=list)


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
# Code regions: wikilinks inside fenced/inline code are SYNTAX EXAMPLES, not real
# links. Strip them before extraction so docs that show `[[X]]` don't pollute the
# links graph nor trigger false broken-wikilink lint.
_CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`]*`")


def _strip_code(text: str) -> str:
    """Replace fenced + inline code spans with spaces (preserves offsets-ish)."""
    text = _CODE_FENCE_RE.sub(" ", text)
    text = _INLINE_CODE_RE.sub(" ", text)
    return text
# Detect duplicate aliases declarations: inline `aliases: [...]` followed by
# orphan list items `  - "..."` on next lines (the common Obsidian editor bug).
_ALIASES_INLINE_THEN_LIST_RE = re.compile(
    r"^aliases:\s*\[.*?\]\s*\n(?:\s+-\s+\S)", re.MULTILINE | re.DOTALL
)
# Or two separate `aliases:` keys (rarer).
_ALIASES_KEY_RE = re.compile(r"^aliases:", re.MULTILINE)


def _clean_str_list(raw, field_name: str, file_stem: str) -> list[str]:
    """Convert YAML list/str to clean list[str], filtering None/empty."""
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw] if raw.strip() else []
    if isinstance(raw, list):
        out = []
        for item in raw:
            if item is None:
                log.warning("Note %s: %s contains null entry, skipped", file_stem, field_name)
                continue
            s = str(item).strip()
            if s:
                out.append(s)
            else:
                log.warning("Note %s: %s contains empty string, skipped", file_stem, field_name)
        return out
    return []


def parse_note(file_stem: str, path: str, content: str) -> ParsedNote:
    frontmatter_raw = ""
    aliases: list[str] = []
    tags: list[str] = []
    lint_warnings: list[str] = []

    fm_match = _FRONTMATTER_RE.match(content)
    if fm_match:
        frontmatter_raw = fm_match.group(1)

        # Lint: detect duplicate aliases declarations
        # Case 1: inline `aliases: [...]` followed by orphan list items
        # Case 2: two `aliases:` keys
        alias_keys = len(_ALIASES_KEY_RE.findall(frontmatter_raw))
        has_inline_then_list = bool(_ALIASES_INLINE_THEN_LIST_RE.search(frontmatter_raw))
        if alias_keys > 1 or has_inline_then_list:
            warning = "aliases declared TWICE (inline + list orphans, or duplicate keys) — YAML parser will likely fail or keep one only"
            lint_warnings.append(warning)
            log.warning("Note %s: %s", file_stem, warning)

        try:
            fm = yaml.safe_load(frontmatter_raw)
            if isinstance(fm, dict):
                aliases = _clean_str_list(fm.get("aliases"), "aliases", file_stem)
                tags = _clean_str_list(fm.get("tags"), "tags", file_stem)
        except yaml.YAMLError as e:
            lint_warnings.append(f"YAML parse error: {e}")
            log.warning("Note %s: YAML parse error: %s", file_stem, e)

    wikilinks = _WIKILINK_RE.findall(_strip_code(content))
    seen: set[str] = set()
    unique_links: list[str] = []
    for link in wikilinks:
        link_stem = link.strip()
        if link_stem not in seen:
            seen.add(link_stem)
            unique_links.append(link_stem)

    return ParsedNote(
        file_stem=file_stem,
        path=path,
        content=content,
        frontmatter_raw=frontmatter_raw,
        aliases=aliases,
        tags=tags,
        wikilinks=unique_links,
        lint_warnings=lint_warnings,
    )
