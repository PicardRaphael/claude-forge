---
titre: "Python natif Windows ne voit pas le /tmp de Git Bash (MSYS)"
resume: "Un script Python lancé via `py` sur Windows ne résout pas les chemins /tmp/* créés par Git Bash (MSYS les mappe ailleurs) — FileNotFoundError. Passer les données par un dossier repo réel, jamais /tmp partagé entre Bash et Python."
aliases: ["python windows tmp", "tmp msys python", "FileNotFoundError /tmp windows", "bash tmp python invisible", "partage fichiers bash python windows"]
type: erreur
derniere-maj: 2026-05-27
auteur: claude
tags: ["#type/erreur", "#domaine/claude-code"]
---

Sur Windows, un fichier écrit par Git Bash dans `/tmp/x.txt` n'est PAS lisible par un script Python lancé via `py script.py` : MSYS mappe `/tmp` vers un emplacement interne (`C:\Users\...\AppData\Local\Temp\` ou la racine MSYS), tandis que Python natif interprète `/tmp` comme `\tmp` à la racine du disque courant → `FileNotFoundError: '\\tmp\\x.txt'`.

## Symptôme
Script Bash génère des listes dans `/tmp/tier1.txt`, script Python les lit via `Path("/tmp/tier1.txt")` → crash. Observé 27 mai 2026 pendant clean-memory (passage de listes Bash→Python pour le split tier-1/tier-2).

## Solution
Passer les données intermédiaires par un **dossier réel du repo** (ex : `memory/_tmp_data/`), accessible identiquement par les deux. Nettoyer après usage.

## Lien
- [[resolution-path-3-contextes]] — résolution de chemin selon le contexte d'exécution
- reference `python-windows-cross-machine` (memory) + rule `windows-hooks` — `py` launcher pour les hooks Windows
