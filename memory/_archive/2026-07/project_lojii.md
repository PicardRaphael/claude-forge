---
name: lojii-project
description: "Projet frontend Vue 3 / Vuetify 3 gestion immobilière, 634 composants, migration Composition API en cours"
metadata: 
  node_type: memory
  type: project
  originSessionId: e49ae7dd-c314-4666-aaa1-9c4885ca823f
---

Lojii = frontend gestion locative/copropriété Neoteem. Vue 3.5 + Vuetify 3.7 + Pinia + Vite 6. JavaScript pur (pas TS).

**Why:** Projet critique Neoteem, 634 composants, dette technique importante (43% Options API, tests quasi inexistants, NeoChat 3140L). 51 micro-apps Vue 2 + 914 écrans WinDev à migrer vers Vue 3.

**How to apply:** Toujours vérifier les conventions lojii (rem, _bibliotheque, neoteem.query, PascalCase composants). Utiliser context7 pour docs Vue 3/Vuetify à jour. Vault neoteem-brain pour mapping WinDev/Vue2.

Vault : [[lojii]], [[analyse-claude-code-2026-05-13]]
Chemin : `C:\Users\raphael.picard_neote\Documents\neofront\lojii`
Repo : Bitbucket (develop/test/prepilote/master)

Config Claude Code déployée (2026-05-13) :
- CLAUDE.md 87L (optimisé)
- 4 agents : architect, vue-dev, code-reviewer, test-writer
- 8 skills : lojii-conventions, lojii-design-system, lojii-windev-mapping, lojii-vue2-mapping, lojii-testing, go, spec, recap
- 10 rules : vue-conventions, quality-gates, api-patterns, agent-limits, check-before-create, learn-from-mistakes, dev-discipline, testing-mandatory, agent-delegation, shared-learnings
- 7 hooks : architect-guard, commit-guard, format-and-lint, env-protect, session-health, agent-marker-writer, pipeline-reset
- MCP : context7 (.mcp.json)
- .claude/ partagé équipe (settings.local.json ignoré)
