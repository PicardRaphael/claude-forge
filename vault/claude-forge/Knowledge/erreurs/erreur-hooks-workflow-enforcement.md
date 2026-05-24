---
titre: "Hooks qui forcent un workflow agentique = anti-pattern Anthropic"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-24
aliases:
  - "erreur hooks workflow enforcement"
  - "ne pas forcer architect par hook"
  - "anti-pattern decision scaffolding"
  - "hooks misuse workflow"
  - "ne pas refaire architect-guard"
resume: "Mettre un hook PreToolUse exit 2 pour forcer architect-first/commit-after-review/délégation au dev viole la doctrine Anthropic 2026. Hooks = lint/security/observabilité. Workflow = doctrine dans rules + session juge."
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#technique/hooks"
  - "#technique/agents"
sources:
  - "Session 22 mai 2026 — refonte ia_back + neo_ia"
  - "[[Boris Cherny]]"
  - "Anthropic Agent SDK overview"
  - "[[raisonnement-22mai-doctrine-vs-enforcement]]"
---

# Hooks workflow enforcement = anti-pattern

## L'erreur

Sur ia_back + neo_ia, créer des hooks PreToolUse exit 2 qui forcent :
- **architect-guard** : architect-marker requis avant Write/Edit dans `src/**`
- **commit-guard** : code-reviewer-marker requis avant `git commit`
- **dispatch-guard** : session principale ne peut PAS écrire dans `src/`
- **marker-protect**, **agent-marker-writer**, **pipeline-reset**, **session-reset-markers** : couche markers pour orchestrer

Logique apparente : "advisory = 80% compliance, hook exit 2 = 100%, donc forcer".

## Pourquoi c'est faux

### 1. Anthropic dit explicitement : hooks = lint/test/security, PAS workflow

Doctrine officielle 2026 ([Hooks reference](https://code.claude.com/docs/en/hooks)) : exemples = `rm -rf`, `--no-verify` git, force-push, secret leak, ruff/eslint blocant. **Aucun exemple** "force le pipeline agentique".

### 2. "Claude decides when to invoke" — Agent SDK

> "Claude decides when to parallelize — you're defining the capability, not the scheduling."

Le hook qui force architect-first **viole frontalement** cette doctrine. C'est la session principale qui doit choisir, pas un hook qui ferme la décision.

### 3. Boris Cherny — "thinnest wrapper", bitter lesson

> "Complex scaffolding is often rendered obsolete by the next model generation."

Tout hook qui encode :
- des paths du repo (allowlist ou blocklist)
- des patterns de noms de fichiers (Router/Dispatcher/Selector)
- une séquence forcée d'agents

= decision scaffolding qui devient obsolète au prochain refacto ou changement de modèle. Anti-pattern explicite.

### 4. Symptôme : friction 6×

Mesure utilisateur (Raphael, 22 mai 2026) : développer une feature prend 6× plus de temps qu'avant. Cause directe :
- architect appelé sur tout (description "ALWAYS invoke FIRST")
- opus xhigh + 8 skills = 30s-2min par appel
- hook bloque la session si oublié → re-appelle architect → 2× overhead
- chaîne complète architect → test-writer → dev → code-reviewer = 4 appels d'agents pour 1 edit trivial

## La règle correcte

**Hooks** : lint, formatage, security (rm -rf), secret detection, scope (repo-scope-guard), type check, test scope target.

**Doctrine** : workflow agentique → `CLAUDE.md` + `rules/` + descriptions d'agents.

**Session principale décide** : appelle architect quand pertinent (cross-file, fichier critique), skip pour typo/mock/hotfix < 30 LOC.

**Si l'advisory est skippé systématiquement** : améliorer la description de l'agent + la rule, pas créer un hook. Le skip indique souvent que l'advisory est mal calibré, pas que l'enforcement manque.

## Cas où le hook est légitime malgré tout

- **Sécurité non-négociable** : empêcher push sur main, empêcher commit de secrets
- **Scope strict** : empêcher l'agent de lire un repo voisin (`repo-scope-guard`)
- **Architecture immutable** : `guard-pg-repo-readonly` (le repo PG est en lecture seule)
- **Convention de test** : `guard-test-scope` (pas de `bun test` global = 1400 tests)
- **Architecture interdite** : `guard-core-imports` (src/core ne doit jamais importer @infra)

Différence clé : ces hooks défendent un **invariant technique non négociable**, pas un workflow.

## Symptômes à surveiller

Si tu envisages un hook, pose-toi ces questions :

1. Est-ce que je force une séquence d'agents (architect → dev → reviewer) ? → **NON, mets-le en rule**
2. Est-ce que je bloque la session principale d'écrire du code ? → **NON, viole doctrine**
3. Est-ce que mon hook utilise une liste de paths/fichiers critiques ? → **NON, ça devient obsolète**
4. Est-ce que j'ai des markers (`.foo-marker`) pour orchestrer ? → **NON, c'est de l'over-engineering**

Si oui à au moins une → l'erreur est en train d'être refaite.

## Que faire à la place

1. **Description d'agent** : "Use this agent when X" — Claude juge
2. **Rule `when-to-X.md`** : critères opérationnels pour la session
3. **CLAUDE.md gotchas** : 1-2 lignes "pour Y, pense à invoquer Z"
4. **Si vraiment besoin de forcer** : repenser la doctrine — le besoin est probablement mal défini

## Liens

- [[raisonnement-22mai-doctrine-vs-enforcement]] — décisions complètes
- [[Boris Cherny]]
- [[comment-creer-hook]]
- [[workflow-claude-code-optimal]]
- [[erreur-pipeline-trop-long-frustration]] — symptôme utilisateur
