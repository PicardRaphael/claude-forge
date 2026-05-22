---
titre: "Pattern Behavioral Dispatch Test — Vérification post-setup"
resume: "Suite de tests comportementaux PASS/FAIL pour vérifier que chaque agent, skill, hook et rule se déclenche au bon moment après un setup ou audit. Observables de dispatch, pas processus mental."
aliases:
  - "behavioral dispatch test"
  - "test comportemental dispatch"
  - "test dispatch agents"
  - "verification post-setup"
  - "test pipeline TDD"
  - "smoke test setup CC"
type: technique
domaine: claude-code
derniere-maj: 2026-05-21
auteur: claude
sources:
  - "Session 2026-05-21 — 5 tests blueprint claude-forge, validés 37/37"
  - "[[workflow-claude-code-optimal]]"
  - "[[synthese-audit-coherence-neo-ia-ia-back]]"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/agents"
  - "#pattern/testing"
---
# Pattern Behavioral Dispatch Test

## Principe

Après un setup Claude Code, un audit, ou des modifications massives (agents, skills, hooks, rules), **livrer une suite de tests comportementaux** que l'humain lance dans une session fraîche pour vérifier que tout dispatch correctement.

Les critères sont des **observables de transcript** — pas des étapes mentales de Claude :

| Observable | Exemple |
|-----------|---------|
| Agent invoqué | "L'agent `architect` est visible dans le transcript" |
| Hook bloquant | "Exit 2 de `dispatch-guard.py` avec message visible" |
| Skill chargée | "La skill `/go` déclenche lint → tests → review → commit" |
| Ordre de pipeline | "architect AVANT dev, test-writer AVANT code-reviewer" |
| Dispatch correct | "dev-neochat invoqué, PAS dev-lead, car modif intra-app" |

## Quand produire un test comportemental

| Situation | Test ? |
|-----------|--------|
| Setup complet d'un nouveau repo | OUI — couvre pipeline + hooks + skills |
| Audit + corrections d'un repo existant | OUI — vérifie que les corrections marchent |
| Création de 3+ agents/skills | OUI — vérifie le dispatch |
| Modification de rules de routing | OUI — vérifie les changements |
| Fix d'un hook individuel | NON — trop petit |
| Ajout d'un gotcha au CLAUDE.md | NON — pas de dispatch |

## Structure type d'un test

```markdown
# Test comportemental — [repo]

## Scénario N — [nom]

**Prompt à lancer :**
> [prompt réaliste qui déclenche la chaîne à tester]

**Critères PASS/FAIL (observable dans le transcript) :**
- [ ] [observable 1]
- [ ] [observable 2]

**Score : /N**
```

## Catégories de scénarios

### 1. Pipeline TDD complet
Teste la chaîne : architect → test-writer red → dev → test-writer refactor → code-reviewer.
Prompt = une feature réaliste de taille M.

### 2. Dispatch dev correct
Teste que le bon agent dev est invoqué selon le scope.
Prompt = un bug ou feature qui touche un scope spécifique (intra-app vs cross-app).

### 3. Triggers agents spécifiques
Teste que chaque agent spécialisé (db-inspector, security-auditor, performance-engineer...) répond à ses mots-clés triggers.
Prompt = 3-5 sous-tests avec les mots-clés de chaque description.

### 4. Skills slash commands
Teste /recap, /go, /spec, /build-fix.
Prompt = lancer chaque slash et vérifier le comportement.

### 5. Hooks bloquants (tests négatifs)
Teste que les hooks bloquent les mauvais comportements.
Prompt = intentionnellement "mauvais" (coder sans plan, sans test, sur session principale).

### 6. Triggers domaine (si applicable)
Teste les agents spécialisés par domaine métier (api-designer, schema-mapper...).

## Comment adapter à un repo

1. **Lister agents** : `ls .claude/agents/*.md` — chaque agent doit apparaître dans au moins 1 scénario
2. **Lister hooks bloquants** : ceux avec `exit 2` — chacun doit avoir un scénario négatif
3. **Lister skills user-invokable** : chaque `/slash` doit être testée
4. **Identifier les chaînes critiques** : pipeline TDD, migration, deploy — 1 scénario par chaîne
5. **Adapter les prompts** : utiliser le vocabulaire métier du projet (pas générique)

## Bonnes pratiques

- **Session fraîche obligatoire** — le contexte de la session de création pollue le test
- **Pas de commit/push** — observer uniquement
- **Prompts réalistes** — utiliser des noms de tables/fonctions/endpoints qui existent dans le repo
- **Score quantitatif** — /N permet de comparer avant/après modifications
- **Archiver les résultats** — noter le score + date pour tracking d'évolution

## Intégration dans le workflow

```
setup/audit → corrections → devil's advocate → TEST COMPORTEMENTAL → livraison
```

Le test comportemental est le **dernier gate avant livraison**, après le devil's advocate. DA vérifie la conception, le test comportemental vérifie l'exécution.

## Liens

- [[workflow-claude-code-optimal]] — checklist setup, le test comportemental = Phase 7
- [[synthese-audit-coherence-neo-ia-ia-back]] — 8 checks d'audit, les tests comportementaux complètent
- [[erreur-claude-agent-env-var-dead-code]] — DA sur le dispatch guard


## Pièges identifiés (feedback neo_ia, mai 2026)

### 1. Hooks en cascade (défense en profondeur)

Si 3 hooks bloquent la même action (dispatch-guard → architect-guard → tdd-guard), seul le premier se déclenche. Les suivants sont invisibles dans le transcript.

**Fix** : un sous-prompt par hook, pas un seul prompt qui teste les 3. Chaque sous-prompt contourne les hooks précédents pour isoler celui qu'on teste.

### 2. /go sans diff

`/go` exige des changements committables. Lancer `/go` sans diff git préalable produit un comportement indéfini (skip ou erreur).

**Fix** : noter "lancer après scénario 1" ou "nécessite un diff préalable".

### 3. Guard-scope invisible si agents corrects

Un hook comme `guard-pytest-scope.py` ne se déclenche que si un agent fait une erreur. Si test-writer scope correctement ses tests, le hook est invisible (PASS silencieux).

**Fix** : reformuler en "les tests sont lancés avec un scope spécifique (observable dans les commandes Bash)" plutôt que "le hook bloque".


### 4. Prompts de test doivent être vérifiables dans le code réel

Un prompt qui dit "le bug affecte aussi neochat" alors que grep montre 0 call-sites est un faux test. L'architect correct refusera de planifier — et c'est un PASS de l'architect, pas un FAIL du dispatch.

**Fix** : avant de rédiger un scénario cross-app, vérifier que les fichiers/fonctions mentionnés existent réellement et ont des dépendances vérifiables par grep. Sinon l'architect (correctement) STOP et le test ne mesure rien.

Source : test neo_ia scénario 2, mai 2026 — architect a invalidé la prémisse du test par grep.


### 5. Défense en profondeur : agents bloquent avant les hooks

Les agents bien configurés (rules + memory) refusent eux-mêmes les actions interdites AVANT que les hooks ne se déclenchent. C'est le meilleur résultat possible — mais ça rend les hooks inobservables dans les tests.

**Conséquence** : les critères de test négatifs doivent mesurer "l'action est empêchée" (peu importe le niveau), pas "le hook X a bloqué". Ajouter une note observateur pour tracer QUEL niveau a bloqué.

**Pour tester un hook en isolation** : il faudrait un agent "naïf" (sans rules, sans memory) qui tenterait le Write — ce qui n'existe pas dans un setup correct. Les hooks sont le filet de sécurité pour les cas où les rules advisory échouent (~20% théorique), pas le mécanisme principal.

Source : test neo_ia scénario 4, mai 2026 — 3/3 prompts bloqués par les agents, 0/3 par les hooks.
