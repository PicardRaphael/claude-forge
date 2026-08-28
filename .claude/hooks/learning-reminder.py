#!/usr/bin/env python3
"""Stop hook advisory: surface uncaptured learning signals without continuing.

This is a deterministic lint, not a memory writer or workflow orchestrator. It
scans the local transcript for a small closed list of signals, subtracts only
the categories that have matching evidence of capitalisation, and emits a
non-blocking ``systemMessage`` once per session. Fail-open on every error.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from collections.abc import Iterable

_TAIL_LINES = 4000

_SIGNALS: tuple[tuple[str, re.Pattern[str], str], ...] = (
    (
        "correction",
        re.compile(
            r"\b(?:faut (?:pas|jamais)|ne (?:refais|refait) (?:plus|jamais)|"
            r"c'est faux|c'est pas (?:ça|ca|bon)|tu (?:as|a) tort|pas comme ça|pas comme ca)",
            re.I,
        ),
        "correction explicite de Raphaël",
    ),
    (
        "norm",
        re.compile(
            r"\b(?:désormais|desormais|dorénavant|dorenavant|à partir de maintenant|"
            r"a partir de maintenant|nouvelle (?:norme|règle|regle))",
            re.I,
        ),
        "nouvelle norme énoncée",
    ),
    (
        "stale",
        re.compile(
            r"\b(?:péri(?:mé|me)|obsol(?:è|e)te|plus (?:valide|à jour|a jour)|"
            r"claim fausse|fait faux|était faux|etait faux)",
            re.I,
        ),
        "fait ou doctrine signalé comme périmé",
    ),
    (
        "gotcha",
        re.compile(
            r"\b(?:gotcha|piège découvert|piege decouvert|bug (?:trouvé|trouve|réel|reel))",
            re.I,
        ),
        "gotcha ou bug découvert",
    ),
    (
        "profile",
        re.compile(
            r"\b(?:je préfère|je prefere|j'aime|je n'aime pas|je travaille|"
            r"mon objectif|je veux que (?:tu|claude|chatgpt|codex)|apprends? (?:ça|ca) sur moi|"
            r"mémorise (?:ça|ca|ceci) sur moi)",
            re.I,
        ),
        "fait ou préférence personnelle explicite",
    ),
)

_PROFILE_EVIDENCE = re.compile(
    r"__tool__:(?:Edit|Write|MultiEdit|apply_patch)\b[^\n]*"
    r"memory/user_raphael_profile\.md"
    r"|__tool__:mcp__forge(?:-|_)brain__(?:append_note|append_note_by_path|"
    r"insert_section|insert_section_by_path|update_note|update_note_by_path|"
    r"update_property|update_property_by_path)\b[^\n]*"
    r"(?:\"file\"\s*:\s*\"Raphael-Picard\"|"
    r"\"path\"\s*:\s*\"2-Casquettes/Raphael-Picard\.md\")",
    re.I,
)
_MEMORY_EVIDENCE = re.compile(r"memory/(?:feedback|reference)_[a-z0-9_-]+\.md", re.I)
_VAULT_EVIDENCE = re.compile(
    r"mcp__forge-brain__(?:create_note|append_note|insert_section|update_note|update_property)"
    r"|mcp__forge_brain__(?:create_note|append_note|insert_section|update_note|update_property)",
    re.I,
)
_DONE_EVIDENCE = re.compile(r"## Session done\s*[—-]|### Appliqué", re.I)


def _tail(path: str) -> list[str]:
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return handle.readlines()[-_TAIL_LINES:]
    except OSError:
        return []


def _texts(lines: Iterable[str]) -> Iterable[str]:
    """Yield model-visible text and tool inputs from JSONL transcript events."""
    for raw in lines:
        try:
            event = json.loads(raw)
        except (TypeError, ValueError):
            continue
        message = event.get("message") or {}
        content = message.get("content")
        if isinstance(content, str):
            yield content
        elif isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text":
                    yield block.get("text") or ""
                elif block.get("type") == "tool_use":
                    name = str(block.get("name") or "unknown")
                    payload = json.dumps(block.get("input") or {}, ensure_ascii=False)
                    yield f"__tool__:{name} {payload}"


def analyse(lines: Iterable[str]) -> tuple[dict[str, str], set[str]]:
    """Return detected signal labels and categories with matching evidence."""
    found: dict[str, str] = {}
    handled: set[str] = set()
    for text in _texts(lines):
        for category, pattern, label in _SIGNALS:
            if pattern.search(text):
                found.setdefault(category, label)
        if _DONE_EVIDENCE.search(text):
            handled.update(category for category, _, _ in _SIGNALS)
        if _PROFILE_EVIDENCE.search(text):
            handled.add("profile")
        if _MEMORY_EVIDENCE.search(text):
            handled.update({"correction", "gotcha"})
        if _VAULT_EVIDENCE.search(text):
            handled.update({"norm", "stale", "gotcha"})
    return found, handled


def pending_labels(lines: Iterable[str]) -> list[str]:
    found, handled = analyse(lines)
    return [label for category, label in found.items() if category not in handled]


def main() -> None:
    try:
        data = json.load(sys.stdin)
        if data.get("stop_hook_active"):
            return
        transcript = data.get("transcript_path")
        session = str(data.get("session_id") or "nosession")
        if not transcript or not os.path.isfile(transcript):
            return

        pending = pending_labels(_tail(transcript))
        if not pending:
            return

        marker = os.path.join(tempfile.gettempdir(), f"forge-learning-advisory-{session}")
        if os.path.exists(marker):
            return
        try:
            with open(marker, "w", encoding="utf-8") as handle:
                handle.write("1")
        except OSError:
            return

        labels = "; ".join(pending)
        message = (
            f"[learning-reminder] Candidats non capitalisés : {labels}. "
            "Le hook ne bloque et n'écrit rien. Utiliser /done seulement si le "
            "contrat docs/second-brain/session-capture.md autorise le delta."
        )
        print(json.dumps({"systemMessage": message}, ensure_ascii=False))
    except Exception:
        return


if __name__ == "__main__":
    main()
