#!/usr/bin/env python3
"""Inject up to three explicitly relevant project memories into Codex."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


_REPO_ROOT = Path(__file__).resolve().parents[2]
_MEMORY_DIR = _REPO_ROOT / "memory"
_CACHE = Path(tempfile.gettempdir()) / (
    "codex-memory-recall-"
    + hashlib.md5(str(_MEMORY_DIR).encode("utf-8"), usedforsecurity=False).hexdigest()[:12]
    + ".json"
)

_MAX_INJECTED = 3
_MIN_SCORE = 4
_MAX_CHARS = 1200
_MIN_PROMPT_LEN = 15

_EXCLUDED = {"MEMORY.md", "_index_archive.md", "review-recurrences.md"}
_STOP = {
    "le",
    "la",
    "les",
    "un",
    "une",
    "des",
    "de",
    "du",
    "et",
    "ou",
    "au",
    "aux",
    "en",
    "dans",
    "sur",
    "pour",
    "par",
    "avec",
    "sans",
    "que",
    "qui",
    "quoi",
    "dont",
    "est",
    "sont",
    "ete",
    "faire",
    "fait",
    "fais",
    "peux",
    "peut",
    "veux",
    "veut",
    "dois",
    "doit",
    "tout",
    "tous",
    "toute",
    "plus",
    "moins",
    "tres",
    "bien",
    "mal",
    "the",
    "and",
    "for",
    "with",
    "this",
    "that",
    "you",
    "your",
    "not",
    "are",
    "was",
    "can",
    "will",
    "from",
    "nous",
    "vous",
    "ils",
    "cette",
    "ces",
    "mon",
    "mes",
    "ton",
    "tes",
    "son",
    "sa",
    "ses",
    "quand",
    "comme",
    "alors",
    "donc",
    "aussi",
    "meme",
}
_WORD = re.compile(r"[a-z0-9_-]{3,}")
_FLEX = (
    "e",
    "es",
    "er",
    "ez",
    "ee",
    "ees",
    "ent",
    "ons",
    "ait",
    "aient",
    "s",
    "r",
    "rs",
    "nt",
)


def _tokens(text: str) -> set[str]:
    return {word for word in _WORD.findall(text.lower()) if word not in _STOP}


def _parse(path: Path) -> tuple[str, str, list[str], str] | None:
    """Read the fields needed for recall from a memory frontmatter."""
    try:
        head = path.read_text(encoding="utf-8-sig")[:2500]
    except (OSError, UnicodeError):
        return None
    if not head.startswith("---"):
        return None
    parts = head.split("---", 2)
    if len(parts) < 3:
        return None

    name = ""
    description = ""
    triggers: list[str] = []
    memory_type = ""
    for raw_line in parts[1].splitlines():
        line = raw_line.strip()
        if line.startswith("name:"):
            name = line[5:].strip().strip("\"'")
        elif line.startswith("description:"):
            description = line[12:].strip().strip("\"'")
        elif line.startswith("trigger:"):
            triggers = [
                item.strip().strip("\"'")
                for item in line[8:].split(",")
                if item.strip()
            ]
        elif line.startswith("type:") and not memory_type:
            memory_type = line[5:].strip().strip("\"'")
    return name, description, triggers, memory_type


def _contains(needle: str, haystack: str) -> bool:
    """Match a term at word boundaries with a closed French suffix list."""
    length = len(needle)
    if not length:
        return False
    start = 0
    while True:
        index = haystack.find(needle, start)
        if index < 0:
            return False
        before = haystack[index - 1] if index > 0 else ""
        if not (before.isalnum() or before == "_"):
            end = index + length
            after = haystack[end] if end < len(haystack) else ""
            if not (after.isalnum() or after == "_"):
                return True
            if length >= 4:
                suffix_end = end
                while suffix_end < len(haystack) and (
                    haystack[suffix_end].isalnum() or haystack[suffix_end] == "_"
                ):
                    suffix_end += 1
                if haystack[end:suffix_end] in _FLEX:
                    return True
        start = index + 1


def score(
    prompt_tokens: set[str],
    prompt_raw: str,
    name: str,
    description: str,
    triggers: list[str],
) -> int:
    """Give explicit triggers more weight than metadata overlap."""
    total = 0
    for trigger in triggers:
        normalized = trigger.lower().strip()
        if not normalized:
            continue
        if "/" in normalized or "*" in normalized:
            core = normalized.strip("*").strip("/").split("*")[0].strip("/")
            if core and _contains(core, prompt_raw):
                total += 4
        elif _contains(normalized, prompt_raw):
            total += 4
        elif _tokens(normalized) & prompt_tokens:
            total += 2
    total += 2 * len(_tokens(name.replace("-", " ").replace("_", " ")) & prompt_tokens)
    total += len(_tokens(description) & prompt_tokens)
    return total


def _memory_files() -> list[Path]:
    try:
        return sorted(
            path
            for path in _MEMORY_DIR.iterdir()
            if path.is_file() and path.suffix == ".md" and path.name not in _EXCLUDED
        )
    except OSError:
        return []


def _signature() -> str:
    parts: list[str] = []
    for path in _memory_files():
        stat = path.stat()
        parts.append(f"{path.name}:{stat.st_mtime_ns}:{stat.st_size}")
    return hashlib.md5("|".join(parts).encode("utf-8"), usedforsecurity=False).hexdigest()


def _build_index() -> list[dict[str, Any]]:
    index: list[dict[str, Any]] = []
    for path in _memory_files():
        parsed = _parse(path)
        if parsed is None:
            continue
        name, description, triggers, memory_type = parsed
        if memory_type == "user" and not triggers:
            continue
        index.append(
            {
                "f": path.name,
                "n": name,
                "d": description,
                "t": triggers,
            }
        )
    return index


def load_index() -> list[dict[str, Any]]:
    """Load the cached index, rebuilding it on any memory file change."""
    try:
        signature = _signature()
        cached = json.loads(_CACHE.read_text(encoding="utf-8"))
        if cached.get("sig") == signature and isinstance(cached.get("index"), list):
            return cached["index"]
    except (OSError, UnicodeError, json.JSONDecodeError, AttributeError):
        pass

    index = _build_index()
    try:
        _CACHE.write_text(
            json.dumps({"sig": _signature(), "index": index}, ensure_ascii=False),
            encoding="utf-8",
        )
    except (OSError, UnicodeError):
        pass
    return index


def collect(prompt_raw: str, prompt_tokens: set[str]) -> list[tuple[int, str, str, str]]:
    hits: list[tuple[int, str, str, str]] = []
    for item in load_index():
        value = score(
            prompt_tokens,
            prompt_raw,
            str(item.get("n", "")),
            str(item.get("d", "")),
            [str(trigger) for trigger in item.get("t", [])],
        )
        if value >= _MIN_SCORE:
            filename = str(item.get("f", ""))
            hits.append(
                (
                    value,
                    str(item.get("n", "")) or Path(filename).stem,
                    str(item.get("d", "")),
                    filename,
                )
            )
    hits.sort(key=lambda hit: (-hit[0], hit[3]))
    return hits


def _context_for(hits: list[tuple[int, str, str, str]]) -> str:
    selected = hits[:_MAX_INJECTED]
    noun = "souvenir" if len(selected) == 1 else "souvenirs"
    header = (
        f"Ce repo contient {len(selected)} {noun} dont les mots-cles recoupent "
        "la demande en cours :\n"
    )
    lines = [
        f"- **{name}** (`memory/{filename}`) — {description[:200]}"
        for _, name, description, filename in selected
    ]
    return (header + "\n".join(lines))[:_MAX_CHARS]


def main() -> None:
    try:
        data = json.load(sys.stdin)
        prompt = str(data.get("prompt") or "").strip()
        if len(prompt) < _MIN_PROMPT_LEN or not _MEMORY_DIR.is_dir():
            raise SystemExit(0)

        prompt_raw = prompt.lower()
        prompt_tokens = _tokens(prompt_raw)
        if not prompt_tokens:
            raise SystemExit(0)

        hits = collect(prompt_raw, prompt_tokens)
        if not hits:
            raise SystemExit(0)

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": _context_for(hits),
            }
        }
        sys.stdout.write(json.dumps(output, ensure_ascii=False))
        raise SystemExit(0)
    except SystemExit:
        raise
    except Exception:
        raise SystemExit(0) from None


if __name__ == "__main__":
    main()
