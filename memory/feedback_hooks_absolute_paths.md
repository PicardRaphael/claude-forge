---
name: hooks-absolute-paths
description: Les hooks dans settings.json doivent utiliser des chemins absolus quand le projet a des additionalDirectories.
type: feedback
---

Les hooks dans settings.json doivent utiliser des chemins absolus, pas relatifs.

**Why:** Quand Claude Code travaille dans un `additionalDirectories`, le CWD change. Un hook avec `.claude/hooks/script.py` sera résolu depuis le CWD courant (ex: neo_ia/) au lieu du projet principal (claude-forge/). Résultat : "file not found".

**How to apply:** Toujours utiliser le chemin absolu dans les hooks de settings.json quand le projet utilise `additionalDirectories`. Ex: `python3 "/full/path/to/.claude/hooks/script.py"` au lieu de `python3 .claude/hooks/script.py`.
