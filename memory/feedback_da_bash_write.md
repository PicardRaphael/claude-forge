---
name: da-bash-write-disguised
description: Ne jamais utiliser Bash cat/heredoc pour écrire quand Write/Edit sont dans disallowedTools — utiliser MCP create_note
type: feedback
originSessionId: 3d8f5cd0-3050-44f0-8294-d41edd60c377
---
Un agent avec `disallowedTools: Write, Edit` qui utilise `Bash cat >` pour écrire = write déguisé qui échoue silencieusement. Découvert sur devil's advocate : 2/4+ critiques non sauvegardées.

**2026-05-22 — Confirmation en production** : le DA a bouclé 5 minutes sur 5 tentatives consécutives d'écriture .md (Bash heredoc, PowerShell here-string, Python -c, /tmp, etc.), toutes fail à cause du Windows quoting. La critique elle-même était produite vite, c'est la sauvegarde qui plante.

**Why:** `disallowedTools` bloque Write/Edit mais Bash passe parfois → comportement non déterministe, pas d'erreur visible. Sur Windows, ajouter le quoting des heredoc qui fail toujours.

**How to apply:**
- Quand un agent doit écrire dans le vault mais a Write/Edit interdits, utiliser `mcp__forge-brain__create_note` (MCP non bloqué par disallowedTools), **et déclarer ce MCP dans `tools:` du frontmatter** (sinon non accessible).
- Si MCP non disponible, l'agent doit **renvoyer le contenu en sortie texte** et laisser l'orchestrateur (session principale) écrire. JAMAIS de fallback Bash/heredoc — c'est documenté dans devils-advocate.md ligne ~57 depuis le 22 mai 2026.
