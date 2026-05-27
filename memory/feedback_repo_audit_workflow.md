---
name: repo-audit-workflow
description: Workflow complet pour analyser un repo Neoteem depuis forge — scan parallèle, corrections par stack, commit par repo. Session référence 4 mai 2026.
type: feedback
originSessionId: fdb162f8-52a4-438b-a60a-c8e2ce6e37cf
---
Workflow d'audit repo depuis forge :

1. **Scanner en parallèle** — lancer 3 agents Explore simultanés, un par repo
2. **Produire le rapport** — tableau par repo, 5 checks, statut OK/WARN/CRITIQUE
3. **Corriger par stack** — ia_back=bun agents, neo_ia=python agents, neoteem-brain=python. Toujours respecter la stack du projet
4. **Commit par repo** — 1 commit séparé par repo avec message descriptif
5. **Push** — forge depuis ici, les 3 autres repos nécessitent permissions cd+git dans settings.local.json

**Why:** Session 4 mai 2026 — on a scanné, diagnostiqué et corrigé 3 repos en une session. Pattern reproductible.

**How to apply:** 
- Utiliser `/config-guardian` pour le diagnostic (la baseline par repo est dans la skill)
- Pour les corrections : agents general-purpose en parallèle (1 par repo)
- Chaque repo a sa propre architecture et ses propres besoins MCP — ne pas copier d'un repo à l'autre
- Toujours vérifier le global ~/.claude/settings.json pour les deny rules
