"""Parse Obsidian .md files: frontmatter, aliases, tags, wikilinks."""

import re
from dataclasses import dataclass, field

import yaml


@dataclass
class ParsedNote:
    file_stem: str
    path: str
    content: str
    frontmatter_raw: str
    aliases: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    wikilinks: list[str] = field(default_factory=list)


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def parse_note(file_stem: str, path: str, content: str) -> ParsedNote:
    frontmatter_raw = ""
    aliases: list[str] = []
    tags: list[str] = []

    fm_match = _FRONTMATTER_RE.match(content)
    if fm_match:
        frontmatter_raw = fm_match.group(1)
        try:
            fm = yaml.safe_load(frontmatter_raw)
            if isinstance(fm, dict):
                raw_aliases = fm.get("aliases", [])
                if isinstance(raw_aliases, str):
                    aliases = [raw_aliases]
                elif isinstance(raw_aliases, list):
                    aliases = [str(a) for a in raw_aliases]

                raw_tags = fm.get("tags", [])
                if isinstance(raw_tags, str):
                    tags = [raw_tags]
                elif isinstance(raw_tags, list):
                    tags = [str(t) for t in raw_tags]
        except yaml.YAMLError:
            pass

    wikilinks = _WIKILINK_RE.findall(content)
    seen: set[str] = set()
    unique_links: list[str] = []
    for link in wikilinks:
        link_stem = link.strip()
        if link_stem not in seen:
            seen.add(link_stem)
            unique_links.append(link_stem)

    # Auto-boost by folder — aliases ×8 gives these notes ranking priority
    folder = path.split("/")[0] if "/" in path else ""
    if folder == "Knowledge":
        aliases.extend(["knowledge", "synthese"])
    elif folder == "07-Support":
        aliases.append("support")

    return ParsedNote(
        file_stem=file_stem,
        path=path,
        content=content,
        frontmatter_raw=frontmatter_raw,
        aliases=aliases,
        tags=tags,
        wikilinks=unique_links,
    )
