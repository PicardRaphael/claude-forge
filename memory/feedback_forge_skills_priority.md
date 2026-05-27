---
name: forge-skills-priority
description: Skills forge (.claude/skills/) sont PRIORITAIRES sur les skills de plugins externes (plugin-dev, document-skills, superpowers). Toujours consulter memoire + skills forge AVANT les plugins.
type: feedback
originSessionId: a0d051cb-3e6f-429d-9908-b2cfe3295ea9
---
Les skills forge sont PRIORITAIRES sur tout plugin externe.

**Ordre de consultation :**
1. Memoire (MEMORY.md + fichiers memoire)
2. Skills forge (.claude/skills/ du projet claude-forge)
3. Plugins externes (plugin-dev, document-skills, superpowers) — uniquement si forge n'a pas l'info

**Why:** J'ai invoque `plugin-dev:plugin-structure` qui contenait des infos obsoletes (mentionnait `commands/` deprecie) alors que ma propre memoire (`reference_claude_code_architecture.md`) et ma skill `cc-cowork-ref` avaient deja l'info correcte et a jour. L'utilisateur a du me corriger deux fois : d'abord sur `commands/` deprecie, puis sur le fait que je n'ai pas utilise mes propres outils.

**How to apply:** Pour toute question sur Claude Code (architecture, plugins, skills, agents, hooks, features) :
1. Lire la memoire pertinente
2. Invoquer la skill forge correspondante (cc-*-ref, cc-advisor, cc-news)
3. Seulement si l'info manque → plugins externes ou recherche web
Ne JAMAIS utiliser un plugin externe quand une skill forge couvre le sujet.
