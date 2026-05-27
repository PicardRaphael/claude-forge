---
name: use-brain-skills-not-grep
description: Pour questions metier Neoteem, utiliser les skills neo-brain (dev/support) avec MCP, jamais fallback grep manuel
type: feedback
originSessionId: 3deba384-7dfb-4d29-890d-01b8723f7a5f
---
Pour toute question metier Neoteem (regles, fonctions PG, comportement appli), utiliser les skills `neoteem-brain-dev:neo-brain` ou `neoteem-brain-support:neo-brain-support` qui passent par le MCP obsidian-brain.

**Why:** Le grep manuel sur le vault + le code SQL a pris 6+ appels d'outils et beaucoup de tokens pour une question qui aurait du etre resolue en 2-3 appels MCP (search_brain + read_note). L'utilisateur attend une reponse rapide et economique.

**How to apply:** 
1. Invoquer la skill neo-brain-dev ou neo-brain-support
2. Utiliser les tools MCP prescrits par la skill (search_brain, read_note, get_backlinks)
3. Si les tools MCP ne sont pas disponibles dans la session, le signaler immediatement a l'utilisateur plutot que de partir en fallback grep
4. Ne JAMAIS grep manuellement le vault ou le code SQL comme substitut — c'est trop couteux en tokens
