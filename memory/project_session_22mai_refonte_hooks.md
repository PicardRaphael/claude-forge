---
name: session-22mai-refonte-hooks-doctrine
description: "Session 22 mai 2026 — refonte complète hooks workflow ia_back + neo_ia. Suppression 7 hooks par repo, split architect quick/deep, doctrine pure. Commits poussés sur 3 repos. Pour /recap en autre session."
metadata: 
  node_type: memory
  type: project
  date: 2026-05-22
  status: completed
  duration: session intense 22 mai 2026
  originSessionId: deb625dd-9d36-4882-84e1-bb7100f3a88c
---

## TL;DR

Refonte complète du workflow Claude Code sur **ia_back** + **neo_ia** : suppression de 7 hooks de workflow enforcement par repo (architect-guard, commit-guard, dispatch-guard, marker-protect, agent-marker-writer, pipeline-reset, session-reset-markers). Doctrine Anthropic 2026 ("Claude decides when to invoke", Boris Cherny "thinnest wrapper") encodée dans rules + descriptions d'agents. Split architect en quick (sonnet) + deep (opus xhigh).

**3 commits poussés**, tests adverses 13/13 passés, capitalisation vault complète.

## Pourquoi cette refonte

**Symptôme utilisateur** : "développer une feature, c'est 6× plus long qu'avant. Je ne peux même pas dire que c'est mieux. L'architecte est tout le temps appelé."

**Diagnostic** :
1. Description architect "ALWAYS invoke FIRST" / "PROACTIVELY" → auto-appel session principale sur S
2. Architect = opus xhigh + 8 skills + plan mode → 30s-2min par appel
3. Mode S "5 lignes max" ignoré par Opus 4.7 (overthinking documenté)
4. Hook `architect-guard` re-déclenche architect si edit src/** sans marker → 2× overhead
5. Hook `commit-guard` force code-reviewer marker avant `git commit`
6. Hook `dispatch-guard` interdit à la session principale d'écrire dans src/
7. Markers + writer + reset = couche de complexité sans valeur

**Sources doctrine consultées** (recherche web 22 mai) :
- Anthropic Agent SDK : "Claude decides when to invoke subagents"
- Boris Cherny (Latent Space, Pragmatic Engineer) : "thinnest wrapper", "complex scaffolding rendered obsolete by next model"
- Hooks reference Claude Code : exemples = rm -rf, force-push, secret leak, lint — **JAMAIS workflow**
- CLAUDE.md doctrine : advisory, pour guidelines/préférences

**Conclusion** : hooks workflow = anti-pattern Anthropic. À supprimer.

## Ce qui a été fait — 8 vagues

### Vague 1 — Suppression hooks workflow (les 2 repos en parallèle)

Supprimés sur ia_back + neo_ia :
- `architect-guard.{ts,py}` — forçait architect avant Write/Edit dans src/**
- `commit-guard.{ts,py}` — forçait code-reviewer marker avant git commit
- `dispatch-guard.{ts,py}` — bloquait session principale d'écrire dans src/
- `marker-protect.{ts,py}` — protection markers
- `agent-marker-writer.{ts,py}` — écriture markers post-Task
- `pipeline-reset.{ts,py}` — reset markers post-push
- `session-reset-markers.{ts,py}` — reset SessionStart

Plus : markers `.architect-marker`, `.code-reviewer-marker`, `.dispatch-bypass` supprimés.
`settings.json` nettoyés (entrées hooks retirées).

### Vague 2 — Split architect quick/deep (les 2 repos)

- `architect-deep.md` (renommé de architect.md) : config existante opus xhigh, 5-8 skills, plan mode, plan complet
- `architect-quick.md` (créé) : sonnet, effort high, 2 skills max, pas plan mode, **OUTPUT 5 LIGNES MAX OBLIGATOIRE**

Descriptions discriminantes pour que la session choisisse selon scope.

### Vague 3 — Doctrine dans rules (les 2 repos)

- **Nouvelle rule** `when-to-architect.md` : matrice de décision quick/deep/skip
- **Réécriture complète** `quality-gates.md` : gates conditionnelles selon critères, pas forcées
- **Update** `orchestrator-mindset.md` : retrait "ne codes pas, hook bloque" → "tu juges"
- **Réécriture complète** `agent-delegation.md` : table routage + quand coder directement

### Vague 4 — Skills forge claude-forge

Audit confirmé : aucune référence aux hooks supprimés ni "ALWAYS architect" dans les skills forge ni CLAUDE.md forge. Rien à modifier.

### Vague 5 — Capitalisation vault forge-brain

**Notes créées :**
- `Knowledge/raisonnements/raisonnement-22mai-doctrine-vs-enforcement.md` — décision centrale, sources web, plan d'action
- `Knowledge/erreurs/erreur-hooks-workflow-enforcement.md` — anti-pattern à ne pas refaire

**Notes mises à jour (via MCP forge-brain append) :**
- `04-Techniques/patterns/pipeline-boris-adapte-neoteem.md`
- `05-Leaders/claude-code/Boris Cherny.md`
- `01-Claude/Code/best-practices/hooks-guide.md`
- `1-Projets/Neoteem/ia_back/ia_back.md`
- `1-Projets/Neoteem/neo_ia/neo_ia.md`
- `vault/claude-forge/CHANGELOG.md`

### Vague 6 — Révision mémoire forge

- `feedback_enforce_not_advise.md` : **révisé** avec scope (s'applique si advisory skippé, PAS si sur-conformité existe — sur-enforcement = mode de défaillance)
- `feedback_hooks_enforcement_pattern.md` : marqué **obsolete** (anti-pattern selon doctrine)
- `feedback_markers_pipeline_complete.md` : marqué **obsolete**
- MEMORY.md : entrées révisées + nouvelle ligne pointant le raisonnement vault

### Vague 7 — CLAUDE.md des 2 repos

- **neo_ia** : section "TDD OBLIGATOIRE" → "TDD convention agent, pas obligation". Gotcha note suppression 22 mai. Liste rules updatée (+ when-to-architect).
- **ia_back** : Stack .claude updaté (17 agents, 7 hooks). Gotchas note suppression 22 mai. Mention architect-quick + architect-deep.

### Vague 8 — Auto-memory locale ia_back

- `feedback_pipeline_enforcement.md` (root ia_back) : marqué **obsolete**
- `feedback_no_direct_coding.md` (root ia_back) : marqué **obsolete**

## État final des repos

### ia_back
- **Hooks (7)** : `typecheck`, `guard-core-imports`, `guard-pg-repo-readonly`, `guard-test-scope`, `on-push-notify`, `session-health`, `spec-brief-boundary-guard`
- **Agents (17)** : `architect-quick`, `architect-deep`, `dev`, `api-designer`, `db-inspector`, `debugger`, `refactor-pg-function`, `schema-mapper`, `sql-optimizer`, `validator`, `security-auditor`, `performance-engineer`, `codebase-analyst`, `code-reviewer`, `test-writer`, `outcomes-grader`, `repo-functions-analyzer`
- **Rules (18)** : + `when-to-architect`, `quality-gates` réécrit, `orchestrator-mindset` adapté, `agent-delegation` réécrit
- Commit `8ab3d82` poussé sur `develop`

### neo_ia
- **Hooks (7)** : `repo-scope-guard`, `guard-pytest-scope`, `auth-detector`, `auth-cleanup`, `on-push-notify`, `session-health`, `spec-brief-boundary-guard` + ruff format/check inline
- **Agents (13)** : `architect-quick`, `architect-deep`, `build-error-resolver`, `codebase-analyst`, `code-reviewer`, `dev-lead`, `dev-neochat`, `dev-neodoc`, `dev-neomail`, `dev-shared-tools`, `outcomes-grader`, `security-reviewer`, `test-writer`
- **Rules (20)** : + `when-to-architect`, `quality-gates` réécrit, `orchestrator-mindset` adapté, `agent-delegation` réécrit
- Commit `c33acc5` poussé sur `develop`

### claude-forge
- Vault capitalisé (2 notes créées, 5 notes mises à jour, CHANGELOG vault)
- Mémoire forge révisée (3 feedbacks)
- Commit `9056055` poussé sur `main`

## Tests adverses passés

- **ia_back hook architect-guard allowlist** (version intermédiaire avant suppression) : 6/6 PASS (test file allow, src/utils allow, src/db/schema block, small diff bypass, Router pattern block, marker bypass)
- **neo_ia hook architect-guard allowlist** (version intermédiaire) : 7/7 PASS (test file allow, utils allow, alembic block, agents/ block, small diff bypass, main.py block, marker bypass)
- **Hooks restants ia_back** : 7/7 compilent OK (bun build)
- **Hooks restants neo_ia** : 7/7 compilent OK (py_compile)

## Effets attendus sur le workflow

| Cas | Avant | Après |
|-----|-------|-------|
| Fix typo / mock test | architect (1-2min) + dev + bloqué par hook | Edit direct (~5s) |
| Bug fix 1 fichier | architect xhigh + dev + test-writer + code-reviewer | architect-quick (60s) + edit (~3-5 min) |
| Nouvelle feature | architect xhigh + tout le pipeline | Idem (le pipeline garde sa valeur ici) |
| Touch schema DB | hook bloque sans architect | Doctrine dit "appelle architect-deep" — session juge |
| git commit | bloqué si pas de marker code-reviewer | Tu commit quand tu veux |

**Mesure de succès** : développer une feature M doit prendre < 30 min (vs 3h avant).

## Risque accepté

~20% des cas où la session skip architect sur du vrai architectural. Pari : architect-quick cheap + doctrine claire > friction 6× actuelle qui faisait abandonner.

## Conflit résolu (mémoire forge ↔ Anthropic doctrine)

- **Avant** : `feedback_enforce_not_advise` disait "advisory = 80%, créer hook bloquant"
- **Après révision 22 mai** : règle valable quand advisory **skippé**. PAS quand sur-conformité. Sur-enforcement = mode de défaillance.

## À tester par Raphael

1. Edit direct `src/utils/foo.ts` ia_back → doit passer
2. Edit mock `__tests__/foo.test.ts` → doit passer (incident initial du jour)
3. Edit `src/db/schema/users.ts` sans architect → passe (doctrine dit penser à architect-deep, rien ne bloque)
4. `git commit` sans code-reviewer → passe
5. Invoquer `architect-quick` sur edit < 30 LOC → doit sortir 5 lignes en < 60s
6. Invoquer `architect-deep` sur nouvelle feature → plan complet comme avant

## Limite honnête

Pas pu tester runtime que `architect-quick` produit bien 5 lignes (Opus 4.7 overthinking). Si dérive, durcir la description.

## Tâches en cours / suspendues

**Aucune.** La refonte est complète, commit, push. Prêt à test runtime utilisateur.

## Mémoire infinie référence

- Vault : [[raisonnement-22mai-doctrine-vs-enforcement]]
- Vault : [[erreur-hooks-workflow-enforcement]]
- Mémoire révisée : `feedback_enforce_not_advise.md`

## Sources web doctrine Anthropic

- https://code.claude.com/docs/en/agent-sdk/overview
- https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
- https://code.claude.com/docs/en/hooks
- https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny
- https://howborisusesclaudecode.com/

## Commandes utiles pour reprendre en autre session

```bash
# Recap général
/recap

# Statut des 3 repos
cd C:/Users/raphael.picard_neote/Documents/neot-v2/ia_back && git log --oneline -5
cd C:/Users/raphael.picard_neote/Documents/neot-v2/neo_ia && git log --oneline -5
cd C:/Users/raphael.picard_neote/Documents/claude-forge && git log --oneline -5

# Vérifier hooks restants ia_back
ls C:/Users/raphael.picard_neote/Documents/neot-v2/ia_back/.claude/hooks/

# Vérifier hooks restants neo_ia
ls C:/Users/raphael.picard_neote/Documents/neot-v2/neo_ia/.claude/hooks/

# Lire le raisonnement complet (via MCP forge-brain)
# Outil MCP : mcp__forge-brain__read_note file="raisonnement-22mai-doctrine-vs-enforcement"
```
