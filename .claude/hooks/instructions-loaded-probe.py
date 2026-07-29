#!/usr/bin/env python3
"""Sonde InstructionsLoaded — prouve QUAND chaque rule entre en contexte.

Usage : brancher sur InstructionsLoaded (sans matcher = toutes les raisons),
lancer une session, lire le log. Ne bloque jamais (exit code ignore par CC).

But : verifier empiriquement que `paths:` gate le CHARGEMENT et pas seulement
l'applicabilite. Precedent qui impose la preuve : `once: true` est documente
mais silencieusement ignore dans settings.json.

Lecture du log : une rule scopee ne doit PAS apparaitre en `session_start`,
et doit apparaitre en `path_glob_match` apres lecture d'un fichier cible.
"""
import datetime
import json
import os
import sys

_LOG = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "..", "output", "instructions-loaded.log",
)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    try:
        stamp = datetime.datetime.now().isoformat(timespec="seconds")
        reason = data.get("reason") or data.get("loadReason") or "?"
        # le nom du champ de chemin n'est pas documente -> on logge tout le payload
        path = data.get("path") or data.get("file_path") or data.get("filePath") or ""
        line = f"{stamp}  reason={reason:<18} path={path}\n"
        if not path:
            line = f"{stamp}  reason={reason:<18} payload={json.dumps(data, ensure_ascii=False)[:300]}\n"
        with open(os.path.abspath(_LOG), "a", encoding="utf-8") as fh:
            fh.write(line)
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
