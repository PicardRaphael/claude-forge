---
name: da-bash-write-disguised
description: "Bash cat/heredoc = write déguisé quand Write/Edit dans disallowedTools — utiliser MCP create_note"
metadata:
  type: feedback
  originSessionId: 3d8f5cd0-3050-44f0-8294-d41edd60c377
---

Cf [[erreur-da-heredoc-bash-silencieux]] (doctrine canonique vault — pattern silent fail Windows quoting).

**Compléments 22 mai 2026 préservés** :
- Le DA a bouclé 5 minutes sur 5 tentatives consécutives d'écriture .md (Bash heredoc, PowerShell here-string, Python -c, /tmp), toutes fail Windows quoting. La critique elle-même produite vite, c'est la sauvegarde qui plante.
- Fix : `mcp__forge-brain__create_note` (MCP non bloqué par disallowedTools) ET déclarer le MCP dans `tools:` frontmatter (sinon non accessible).
- Si MCP non disponible : renvoyer contenu en texte, session principale écrit. JAMAIS fallback Bash/heredoc.
