#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clean_subs.py — Nettoie les sous-titres SRT/VTT auto-generés par yt-dlp.

Usage : python clean_subs.py <fichier.srt|.vtt>
Output : transcription propre sur stdout (sans timestamps, sans tags inline)
"""

import re
import sys
from pathlib import Path


def clean_srt(content: str) -> str:
    """Nettoie un contenu SRT ou VTT converti en SRT."""
    lines = content.splitlines()
    cleaned = []
    for line in lines:
        # Supprimer les numéros de séquence (ligne = entier seul)
        if re.match(r"^\d+$", line.strip()):
            continue
        # Supprimer les lignes de timing (contiennent -->)
        if "-->" in line:
            continue
        # Supprimer les tags inline yt-dlp : <00:00:01.500>, <c>, </c>, etc.
        line = re.sub(r"<[^>]+>", "", line)
        # Supprimer les lignes vides
        if not line.strip():
            continue
        cleaned.append(line.strip())
    # Dédupliquer les lignes consécutives identiques (répétitions auto-gen)
    deduped = []
    prev = None
    for line in cleaned:
        if line != prev:
            deduped.append(line)
            prev = line
    return "\n".join(deduped)


def clean_vtt(content: str) -> str:
    """Nettoie un contenu VTT natif (avant conversion SRT)."""
    # Supprimer l'en-tête WEBVTT
    content = re.sub(r"^WEBVTT.*?\n", "", content, flags=re.MULTILINE)
    # Réutiliser clean_srt sur le reste
    return clean_srt(content)


def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_subs.py <fichier.srt|.vtt>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Erreur : fichier introuvable : {path}", file=sys.stderr)
        sys.exit(1)

    content = path.read_text(encoding="utf-8", errors="replace")

    if path.suffix.lower() == ".vtt":
        result = clean_vtt(content)
    else:
        result = clean_srt(content)

    print(result)


if __name__ == "__main__":
    main()
