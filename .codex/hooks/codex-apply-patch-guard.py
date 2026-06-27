#!/usr/bin/env python3
"""Codex PreToolUse guard for apply_patch.

The Claude Code write guards expect Write/Edit/MultiEdit payloads with
tool_input.file_path. Codex often writes through apply_patch, whose payload can
be a patch blob instead. This guard blocks direct patch edits to forge-brain
vault markdown notes before the broader Claude-origin write dispatcher runs.
"""

import json
import re
import sys


PATCH_PATH_RE = re.compile(
    r"^\*\*\* (?:Add File|Update File|Delete File|Move to):\s+(.+?)\s*$",
    re.MULTILINE,
)


def is_blocked_vault_note(path: str) -> bool:
    normalized = path.strip().strip('"').replace("\\", "/").lstrip("./")
    return normalized.startswith("vault/claude-forge/") and normalized.lower().endswith(".md")


def extract_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from extract_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from extract_strings(item)


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)

    try:
        data = json.loads(raw)
    except Exception:
        data = raw

    candidate_texts = list(extract_strings(data))
    if not candidate_texts and isinstance(data, str):
        candidate_texts = [data]

    for text in candidate_texts:
        for match in PATCH_PATH_RE.finditer(text):
            path = match.group(1)
            if is_blocked_vault_note(path):
                print(
                    "BLOQUE: apply_patch direct sur une note markdown du vault forge-brain.\n"
                    f"Fichier: {path}\n"
                    "Utilise le MCP forge-brain pour modifier le vault, afin de garder l'index synchronise.",
                    file=sys.stderr,
                )
                sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
