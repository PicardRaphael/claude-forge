---
titre: Hook vault-before-specialist avec TTL 60min et scope gonflé
aliases:
  - vault-before-specialist TTL
  - vault-before-specialist scope
  - erreur hook vault forge
  - hook vault TTL anti-pattern
  - is_specialist faux positifs
resume: Le hook vault-before-specialist.py de claude-forge avait un TTL 60min sur son marker (viole marker-ttl-antipattern), un scope de 10 agents dont 6 hors-rule, et is_specialist regardait le prompt produisant des faux positifs
derniere-maj: 2026-05-24
tags:
  - "#type/erreur"
  - "#erreur/hook"
  - "#domaine/claude-code"
  - "#projet/claude-forge"
---

# Hook vault-before-specialist avec TTL 60min et scope gonflé

## Ce qui s'est passé

Raphael a observé que devil's advocate et advisor (côté claude-forge) appelaient le MCP forge-brain trop souvent, coûtant des tokens. En investiguant, le hook `vault-before-specialist.py` montrait 4 défauts compoundés :

1. **TTL 60min sur le marker** — chaque session > 1h voyait son marker expirer, re-déclenchant un vault check au milieu d'un workflow (viole feedback : marker-ttl-antipattern)
2. **Scope = 10 agents** dont 6 ne créent rien dans `.claude/` (devils-advocate, project-analyzer, project-auditor, vault-maintainer, python-dev, self-updater)
3. **`is_specialist()`** matchait le nom d'agent dans le `prompt`/`description` → faux positifs garantis (mentionner "skill-creator" dans un prompt à general-purpose bloquait le dispatch)
4. **Pas de SessionStart reset** — un marker traînait potentiellement de session précédente

## Pourquoi c'était une erreur

Le hook a accompli sa mission éducative (3+ erreurs en prod historiques de skills/agents créés sans vault check). Mais il avait dérivé en "ceinture+bretelles+sangle" :
- Le TTL 60min violait directement feedback : marker-ttl-antipattern documenté par Raphael lui-même
- Les 6 agents hors-scope (analyse, audit, critique, dev Python) n'ont aucune raison d'être bloqués par check-before-create (rule qui vise skill/agent/hook/rule/prompt — pas analyse)
- Le matching dans le prompt produisait du blocage sur le mauvais signal

## La solution déployée (2026-05-21)

4 fixes en un patch, après devil's advocate verdict EVOLVE + advisor d'accord :

### Fix 1 — Retirer le TTL
Marker = existence-only. Plus de `MARKER_MAX_AGE_MINUTES`. Plus de `datetime` import. Une session = un check, point.

### Fix 2 — Scope réduit à 4 agents
`SPECIALIST_AGENTS` passe de 10 → 4 : skill-creator, agent-creator, hook-creator, claudemd-optimizer. C'est-à-dire les agents qui CRÉENT ou MODIFIENT des composants `.claude/`. Les agents d'analyse/audit/critique ne sont plus bloqués.

### Fix 3 — `is_specialist()` lit seulement `subagent_type`
Plus de matching dans `prompt` ou `description`. Si je dis "skill-creator" dans un dispatch à general-purpose, ça passe. C'est la donnée structurée du tool_input qui compte.

### Fix 4 — Nouveau hook `session-reset-vault-marker.py` (SessionStart)
Supprime le marker au démarrage de chaque session. Reset propre. Combine avec [Fix 1] = pattern existence-only + reset SessionStart, conforme [[workflow-claude-code-optimal]].

## Tests empiriques (validation)

6/6 PASS testés le 2026-05-21 :
- Specialist sans marker → exit 2 ✅
- devils-advocate (retiré du scope) → passe ✅
- general-purpose mentionnant "skill-creator" → passe (plus de faux positif) ✅
- Marker présent → passe ✅
- Marker vieux de 2h (mtime trafiqué) → passe toujours (TTL retiré) ✅
- SessionStart reset → marker supprimé ✅

## Découverte connexe : sub-agent vs main session

En investiguant, j'ai aussi compris que les 54k tokens consommés au tour 1 de cette session venaient de MA décision de déléguer le vault check à un sub-agent général, alors que le tracker `vault-query-tracker.py` (ligne 98-99) **pose déjà le marker quand `mcp__forge-brain__*` est appelé en main session**. Faire 2-3 `search_brain` directs coûte ~500 tokens contre 54k via sub-agent dédié.

**Leçon** : pour les vault checks orientés (sujet bien cadré), faire les appels en main session. Pour les recherches exploratoires multi-axes, sub-agent OK.

## Liens

- feedback : marker-ttl-antipattern
- [[delegate-guard-pattern]]
- [[workflow-claude-code-optimal]]
- feedback : enforce-not-advise
- [[raisonnement-22mai-doctrine-vs-enforcement]]
- [[erreur-advisory-rules-insuffisantes]]
- [[erreur-architect-neo_ia-fouille-bdd]]

## Méta — leçon Jarvis

Quand Raphael dit "j'ai peur que ça coûte trop de tokens", la posture par défaut **n'est pas** "il a raison, on relâche". C'est "vérifions empiriquement". Le DA a confirmé que tuer le hook = régression, mais que 3 défauts spécifiques le rendaient coûteux. La bonne réponse = chirurgical, pas "killer".

Important aussi : les hooks d'enforcement ne sont pas figés. Un hook qui éduque pendant 6 mois peut dériver en friction inutile sur un comportement acquis. Audit périodique nécessaire (revue mensuelle via `/forge-review` ?).
