---
name: deploy-methods-other-repos
description: Deployer le standard methodes integrees + qualite notes sur neo_ia, ia_back, neoteem-brain lors du prochain skill-evolve
type: project
status: review-required
expires: 2026-09-15
originSessionId: be761cf9-3fd0-4016-adb8-3e189b4efb1f
---
## À déployer sur les autres repos

### Méthodes intégrées (9e principe)
- cc-skills-ref déjà mis à jour — les FUTURES skills appliqueront automatiquement
- Skills EXISTANTES sur neo_ia (27) et ia_back (28) → à upgrader via `/skill-evolve all` par repo
- Priorité : skills métier (neochat-agents, neoia-conventions, etc.) > skills qualité > skills référence

### Standard qualité notes vault
- S'applique déjà au vault forge-brain via forge-brain-proactive.md
- neoteem-brain a son propre standard (aliases-obligatoires.md) — déjà en place
- Pas besoin de changer neoteem-brain, le standard est compatible

### MCP forge-brain
- Spécifique à forge, PAS à déployer sur les autres repos
- neo_ia/ia_back utilisent MCP neoteem-brain (port 8090)

**How to apply:** Prochain passage sur chaque repo → `/skill-evolve all` pour appliquer le 9e principe aux skills existantes.
