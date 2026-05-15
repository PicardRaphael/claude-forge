---
titre: "Tests architecture multi-agents — plan de validation"
resume: "Checklist de tests à exécuter pour valider que tous les composants forge fonctionnent correctement ensemble — agents, skills, hooks, DA, advisor"
aliases:
  - "tests architecture"
  - "validation agents skills hooks"
  - "test multi-agents"
  - "checklist tests forge"
type: context
status: active
derniere-maj: 2026-05-14
auteur: claude
tags:
  - "#type/context"
  - "#meta/testing"
---

## Objectif

Valider que l'architecture forge fonctionne en conditions réelles — inspiré par Kimi K2.6 qui scale à 300 sub-agents.

## Tests à faire sur forge (claude-forge)

### Activation & Routing
- [ ] skill-activation.py déclenche sur les bons triggers (tester chaque skill du .skill-triggers.json)
- [ ] delegate-guard bloque les edits directs ET laisse passer les specialists
- [ ] vault-before-specialist bloque si vault pas consulté
- [ ] vault-write-tracker compte correctement et déclenche DA à 3+
- [ ] proactivity-reminder fire en fin de session > 5 tours
- [ ] learning-reminder fire en fin de session

### Devil's Advocate Pipeline
- [ ] devil-advocate-guard fire après skill-creator, agent-creator, hook-creator, claudemd-optimizer
- [ ] devil-advocate-stop bloque si .devil-advocate-needed sans .devil-advocate-done
- [ ] devil-advocate-tracker écrit le marker après DA
- [ ] vault-write-tracker crée .devil-advocate-needed après 3+ writes vault

### Agents Specialists
- [ ] skill-creator consulte le vault (étape 0) puis crée une skill conforme
- [ ] agent-creator consulte le vault puis crée un agent conforme
- [ ] hook-creator crée un hook + met à jour settings.json
- [ ] claudemd-optimizer respecte < 200 lignes

### Skills Reference
- [ ] cc-skills-ref charge correctement quand skill-creator invoqué
- [ ] cc-hooks-ref charge correctement quand hook-creator invoqué
- [ ] cc-agents-ref charge correctement quand agent-creator invoqué

### Scénario intégré
- [ ] Créer une skill de A à Z → vérifier que TOUS les hooks fire dans l'ordre : vault-before-specialist → skill-creator → devil-advocate-guard → devil-advocate-stop

## Tests à faire sur les futurs repos (ia_back, neo_ia, neoteem-brain, bdd)

### Avant déploiement config
- [ ] CLAUDE.md < 200 lignes et chaque ligne justifiée
- [ ] Rules dans .claude/rules/ avec paths: si scope limité
- [ ] Hooks critiques doublent les rules les plus importantes
- [ ] settings.json avec chemins Python portables (python via PATH)
- [ ] Pas de chemins durs spécifiques à un poste

### Après déploiement
- [ ] /recap fonctionne et donne un snapshot utile
- [ ] Les skills se déclenchent sur les bons triggers
- [ ] Le vault est consulté avant chaque création de composant
- [ ] Le DA fire sur les livrables majeurs

## Pattern Kimi K2.6 — scaling agents

Kimi K2.6 scale à 300 sub-agents / 4000 étapes coordonnées. Pour forge, tester :
- Audit multi-repo en parallèle (1 agent par repo, lancés simultanément)
- Batch de notes vault (10+ agents en parallèle pour créer/enrichir)
- Limite pratique : combien d'agents parallèles avant dégradation ?

## Liens

- [[agents-orchestration]] — Patterns multi-agents
- [[harness-engineering]] — Pourquoi tester le harness, pas juste le modèle
- [[cowork-skills-reliability]] — Debugging skills
