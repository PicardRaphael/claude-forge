#!/usr/bin/env python3
"""UserPromptSubmit: surface at most two active, indexed memory pointers.

``memory/MEMORY.md`` is the active registry. A file that merely exists in the
directory is not recallable. Expired, archived and review-required entries are
excluded. Only metadata is injected; the selected file must be opened before
its contents can influence a response. All failures are silent and fail-open.
"""

from datetime import date
import hashlib
import json
import os
import re
import sys
import tempfile

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_HOOK_DIR))
_MEMORY_DIR = os.path.join(_REPO_ROOT, "memory")
_INDEX_PATH = os.path.join(_MEMORY_DIR, "MEMORY.md")
_CACHE = os.path.join(
    tempfile.gettempdir(),
    "forge-memrecall-" + hashlib.md5(_MEMORY_DIR.encode()).hexdigest()[:12] + ".json",
)
_MAX_INJECTED = 2
_MAX_CHARS = 800
_MIN_SCORE = 6
_MIN_PROMPT_LEN = 15
_INACTIVE_STATUSES = {"archived", "inactive", "review-required", "superseded"}
_EXCLUDED = {"MEMORY.md", "_index_archive.md", "review-recurrences.md"}
_LINK = re.compile(r"\]\(([^)#?]+\.md)(?:#[^)]+)?\)", re.IGNORECASE)
_WORD = re.compile(r"[a-z0-9_-]{3,}")
_STOP = {
    "le", "la", "les", "un", "une", "des", "de", "du", "et", "ou", "au",
    "aux", "en", "dans", "sur", "pour", "par", "avec", "sans", "que", "qui",
    "quoi", "dont", "est", "sont", "faire", "fait", "fais", "peux", "veux",
    "dois", "tout", "tous", "plus", "moins", "bien", "the", "and", "for",
    "with", "this", "that", "you", "your", "are", "from", "nous", "vous",
    "mon", "mes", "ton", "tes", "quand", "comme", "alors", "donc", "aussi",
}
_FLEX = ("e", "es", "er", "ez", "ee", "ees", "ent", "ons", "ait", "aient", "s", "r", "rs", "nt")


def _tokens(text: str) -> set[str]:
    return {word for word in _WORD.findall(text.lower()) if word not in _STOP}


def _contains(needle: str, haystack: str) -> bool:
    """Word-boundary match with a small closed list of French inflections."""
    needle = needle.lower().strip()
    if not needle:
        return False
    start = 0
    while True:
        index = haystack.find(needle, start)
        if index < 0:
            return False
        before = haystack[index - 1] if index else ""
        if not (before.isalnum() or before == "_"):
            end = index + len(needle)
            after = haystack[end] if end < len(haystack) else ""
            if not (after.isalnum() or after == "_"):
                return True
            if len(needle) >= 4:
                stop = end
                while stop < len(haystack) and (haystack[stop].isalnum() or haystack[stop] == "_"):
                    stop += 1
                if haystack[end:stop] in _FLEX:
                    return True
        start = index + 1


def _linked_files() -> list[str]:
    try:
        with open(_INDEX_PATH, "r", encoding="utf-8-sig") as handle:
            content = handle.read()
    except OSError:
        return []
    found: list[str] = []
    for match in _LINK.finditer(content):
        filename = os.path.basename(match.group(1).replace("\\", "/"))
        if filename not in _EXCLUDED and filename not in found:
            found.append(filename)
    return found


def _parse(path: str) -> dict[str, object] | None:
    try:
        with open(path, "r", encoding="utf-8-sig") as handle:
            head = handle.read(3000)
    except OSError:
        return None
    if not head.startswith("---"):
        return None
    parts = head.split("---", 2)
    if len(parts) < 3:
        return None
    fields: dict[str, str] = {}
    for raw_line in parts[1].splitlines():
        if ":" in raw_line:
            key, value = raw_line.split(":", 1)
            fields[key.strip().lower()] = value.strip().strip("\"'")
    return {
        "n": fields.get("name", ""),
        "t": [part.strip().strip("\"'") for part in fields.get("trigger", "").split(",") if part.strip()],
        "type": fields.get("type", "memory"),
        "status": fields.get("status", "active").lower(),
        "expires": fields.get("expires", ""),
    }


def _active(item: dict[str, object], *, today: date | None = None) -> bool:
    if str(item.get("status", "active")).lower() in _INACTIVE_STATUSES:
        return False
    raw_expiry = str(item.get("expires", "")).strip()
    if not raw_expiry:
        return True
    try:
        expiry = date.fromisoformat(raw_expiry[:10])
    except ValueError:
        return False
    return expiry >= (today or date.today())


def _signature() -> str:
    parts: list[str] = []
    for filename in _linked_files():
        try:
            stat = os.stat(os.path.join(_MEMORY_DIR, filename))
        except OSError:
            continue
        parts.append(f"{filename}:{stat.st_mtime_ns}:{stat.st_size}")
    try:
        stat = os.stat(_INDEX_PATH)
        parts.append(f"MEMORY.md:{stat.st_mtime_ns}:{stat.st_size}")
    except OSError:
        pass
    return hashlib.md5("|".join(parts).encode()).hexdigest()


def _build_index() -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for filename in _linked_files():
        item = _parse(os.path.join(_MEMORY_DIR, filename))
        if item and _active(item):
            item["f"] = filename
            result.append(item)
    return result


def load_index() -> list[dict[str, object]]:
    signature = _signature()
    try:
        with open(_CACHE, "r", encoding="utf-8") as handle:
            cached = json.load(handle)
        if cached.get("sig") == signature:
            return cached.get("index") or []
    except Exception:
        pass
    result = _build_index()
    try:
        with open(_CACHE, "w", encoding="utf-8") as handle:
            json.dump({"sig": signature, "index": result}, handle, ensure_ascii=False)
    except OSError:
        pass
    return result


def score(prompt_tokens: set[str], prompt_raw: str, item: dict[str, object]) -> tuple[int, str]:
    total = 0
    reasons: list[str] = []
    name_tokens = _tokens(str(item.get("n", "")).replace("-", " ").replace("_", " "))
    name_tokens -= {"project", "memory", "feedback", "policy"}
    if len(name_tokens) >= 2 and name_tokens.issubset(prompt_tokens):
        total += 6
        reasons.append("nom exact")
    else:
        total += 2 * len(name_tokens & prompt_tokens)
    for raw_trigger in item.get("t", []):
        trigger = str(raw_trigger).lower().strip()
        core = trigger.strip("*").strip("/").split("*")[0].strip("/")
        if core and _contains(core, prompt_raw):
            total += 4
            reasons.append(f"trigger {raw_trigger}")
        elif _tokens(trigger) & prompt_tokens:
            total += 2
    return total, ", ".join(reasons[:2]) or "mots-clés"


def collect(prompt_raw: str, prompt_tokens: set[str]) -> list[tuple[int, str, str, str, str]]:
    hits: list[tuple[int, str, str, str, str]] = []
    for item in load_index():
        value, reason = score(prompt_tokens, prompt_raw, item)
        if value >= _MIN_SCORE:
            filename = str(item["f"])
            hits.append((value, str(item.get("n") or filename[:-3]), str(item.get("type") or "memory"), filename, reason))
    hits.sort(key=lambda hit: (-hit[0], hit[3]))
    return hits


def main() -> None:
    try:
        data = json.load(sys.stdin)
        prompt = (data.get("prompt") or "").strip()
        if len(prompt) < _MIN_PROMPT_LEN or not os.path.isdir(_MEMORY_DIR):
            sys.exit(0)
        prompt_raw = prompt.lower()
        lines: list[str] = []
        for _, name, memory_type, filename, reason in collect(prompt_raw, _tokens(prompt_raw))[:_MAX_INJECTED]:
            line = f"- **{name}** ({memory_type}; `memory/{filename}`) — {reason}"
            if sum(map(len, lines)) + len(line) > _MAX_CHARS:
                break
            lines.append(line)
        if not lines:
            sys.exit(0)
        context = "Pointeurs mémoire actifs possiblement pertinents (contenu non chargé ; ouvrir avant usage) :\n" + "\n".join(lines)
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": context}}))
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
