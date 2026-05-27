---
name: vibe-coding-setup-pattern
description: Pattern complet vibe coding deploye sur neo_ia et ia_back — /go, /recap, journalier.md, RECAP.md, shared-learnings, trio analyse, 100% opus
type: reference
originSessionId: a553b6f6-4880-433c-9a32-d422a31d3f1f
---
## Pattern Vibe Coding Complet (deploye 2026-05-04)

### Fichiers a creer dans .claude/ de tout nouveau projet

1. **Skills essentielles** : /recap, /go, /evolve, /audit-health, /refactor-scan
2. **Agent** : codebase-analyst (orchestre evolve + audit-health + refactor-scan)
3. **Rule** : shared-learnings (apprentissages commites, pas juste Auto Memory)
4. **Doc** : RECAP.md (bilan complet), journalier.md (guide journee type)

### Effort levels (100% opus)

- Analystes = opus high
- Devs = opus medium
- Gates = opus medium
- Securite = opus high

### Skills auto-chargees vs slash commands

Les skills dans le `skills:` d'un agent sont auto-chargees quand l'agent est dispatche. Les slash commands (`user-invokable: true`) sont pour les moments ou AUCUN agent ne le fait automatiquement.

Commandes 100% manuelles : /recap, /go, /evolve, /audit-health, /refactor-scan, /deploy-check
Commandes auto via agents : /add-endpoint, /create-agent, /create-tool (les agents les utilisent)

### Journee type

/recap → vibe coding → /go → repeat
70-80% contexte = reset (/go → /clear → /recap)

### Automatisation Jira (prochaine etape)

MCP Atlassian deja connecte. 3 options : /schedule, manuel "fais le ticket X", hook sur branche.

### Vault

Note detaillee : vault/claude-forge/04-Techniques/vibe-coding-setup-complet.md
