---
name: use-brain-skills-not-grep
description: Pour questions metier Neoteem, utiliser les skills neo-brain (dev/support) avec MCP, jamais fallback grep manuel
trigger: neoteem, metier, copropriete, syndic, gerance, brain
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

**Extension 10 juin 2026 (re-violation corrigée)** : la règle vaut aussi pour le CÂBLAGE des composants — un agent/skill d'un repo qui a besoin du métier doit invoquer/précharger la skill `neo-brain-dev-ia` (plugin neoteem, croise vault + code réel), JAMAIS être câblé sur `mcp__neobrain__search_brain` en direct. Pattern : `skills: [neo-brain-dev-ia]` en frontmatter agent (préchargement, comme ia_back architect-deep/db-inspector) + `mcpServers: [neobrain]` pour la tuyauterie. J'avais câblé le MCP direct sur neoteem-back-ts → corrigé par Raphael (« il doit passer par ce skill, c'est le plus important »).

**Extension 10 juin 2026 soir (2 rappels même session)** : quand Raphael NOMME une skill/source dans sa demande (« via le skill neo-brain-dev-ia », « regarde le vault »), l'invoquer VISIBLEMENT et TÔT — dès la phase de plan (les lectures sont read-only autorisées en plan mode), jamais la reporter « à l'exécution ». Écrire « je consulterai X » dans un plan sans call = vécu comme « tu n'appelles jamais ce que je demande ». Réflexe : la demande nomme un outil → le 1er tool call de la réponse l'utilise (ou l'invoque via Skill).
