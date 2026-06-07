---
titre: "Kill TDD strict via hooks bloquants — convention agent suffit"
aliases:
  - "kill tdd-guard 21 mai 2026"
  - "raisonnement tdd strict supprimé"
  - "tdd convention vs hook bloquant"
  - "raisonnement refonte hooks neo_ia ia_back"
  - "1 test à la fois anthropic"
  - "tdd-guard friction sans valeur"
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
  - "#technique/agents"
  - "#technique/hooks"
  - "#projet/neo_ia"
  - "#projet/ia_back"
resume: "Session 21 mai 2026 — TDD strict via PreToolUse hook bloquant supprimé (neo_ia + ia_back). Convention agent suffit. Best practice Anthropic confirmée : 'ONE failing test per behavior per cycle', JAMAIS de batch."
derniere-maj: 2026-05-21
auteur: claude
type: raisonnement
domaine: claude-code
sources:
  - "Session Raphael 21 mai 2026 — 4h+ sur fix BERNAT bloqué par hooks neo_ia"
  - "Web search Boris Cherny / Anthropic / Thariq Shihipar (21 mai 2026)"
  - "[[raisonnement-kill-tdd-strict-hooks-mai-2026]]"
  - "[[critique-2026-05-21-refonte-hooks-16-vers-6]]"
  - "[[workflow-claude-code-optimal]]"
  - "https://howborisusesclaudecode.com/"
  - "https://claude.com/blog/how-anthropic-teams-use-claude-code"
---

# Raisonnement — Kill TDD strict via hooks bloquants

## Contexte déclencheur

Soir du 21 mai 2026. Raphael passe 4h+ sur un fix bug (BERNAT, filtres `lister_donnees` neo_ia). Pipeline TDD strict (architect → test-writer phase RED → dev → code-reviewer) avec hooks bloquants (`tdd-guard.py`, `architect-guard.py`, `marker-protect.py`, `session-reset-markers.py`) :

- 600k+ tokens consommés, 0 ligne de code source écrite
- test-writer écrit 68 tests pour modules **qui n'existent pas encore** (anti-pattern Anthropic)
- `/clear` wipe le marker → re-dispatch architect "fast pass" UNIQUEMENT pour reposer un fichier marker
- `marker-protect.py` bloque même `ls .architect-marker` (effet de bord)
- AskUserQuestion plante, blocages UI fréquents
- Raphael : *"j'en peux plus"*

→ Frustration → demande de challenge frontal.

## Question discriminante

**TDD oui/non n'est PAS la bonne question.** La vraie question :

> **TDD (méthode) vs enforcement-par-hook-bloquant (mécanisme)** — les deux ont été muddlés.

## Évidence collectée

### 1. Web search Boris Cherny + Anthropic (21 mai 2026)

| Source | Citation clé |
|--------|-------------|
| Boris Cherny | *"TDD = single strongest pattern, 2-3x quality improvement"* — via **feedback loops** (red→green), pas hook bloquant |
| Anthropic doc | *"RED: Write ONE test that fails. Just one. GREEN: Write minimal code to pass that test only."* |
| Anthropic doc | *"Tests written in bulk test imagined behavior, not observed behavior."* |
| Boris | *"CLAUDE.md is advisory (80% compliance). Hooks are deterministic (100%)."* — mais **JAMAIS de citation prescrivant TDD via hook bloquant** |

### 2. DA verdict (vault `critique-2026-05-21-setup-tdd-strict-neoia.md`)

- **EVOLVE** (ni KILL ni KEEP)
- 6 bloquants, 4 avertissements, 2 nitpicks
- Phrase clé : *"Boris/Erik/Thariq/Karpathy/Cat Wu ne prescrivent NULLE PART le TDD bloquant par hook"*

### 3. DA second tour (vault `critique-2026-05-21-refonte-hooks-16-vers-6.md`)

- Kill list initiale "16 → 6 hooks" : **trop large pour le soir**
- 4 bloquants empêchant la refonte complète :
  1. Triplet auth = 3 events Claude Code distincts, fusion impossible
  2. `pipeline-reset.py` n'est PAS un hook event — c'est un script appelé par `/go` (skill ligne 160). Suppression = casse `/go`
  3. `typecheck.ts` = 30s timeout × N edits, décision binaire requise (async ou kill)
  4. `guard-core-imports.ts` = règle archi hexagonale, ni ruff ni ts-prune ne la remplacent
- **Verdict ce soir** : 3 kills propres uniquement (`tdd-guard.py` × 2 + `on-env-protect.py`)

### 4. Le vault avait déjà tranché 24h avant

- [[workflow-claude-code-optimal]] (22 mai 2026) : "phase REFACTOR test-writer SUPPRIMÉE", "MAX 3 tests par comportement" (révisé ce soir : "1 test à la fois")
- `feedback_pipeline_quality_gates` (mémoire) : "gates CONDITIONNELLES, 5 étapes CRUD pas 8"

→ La doctrine 22 mai n'avait juste **pas été déployée sur neo_ia**. Contradiction `testing-mandatory.md` ligne 124 vs `quality-gates.md` ligne 116.

## Décisions prises

### Axe 1 — TDD : KEEP la méthode, KILL le hook bloquant ✅

**Fait** :
- Supprimé `tdd-guard.py` (neo_ia)
- Supprimé `tdd-guard.ts` (ia_back)
- Supprimé `on-env-protect.py` (neo_ia) — permissions Claude Code suffisent
- test-writer reste en phase 2 du pipeline (mais 1 test à la fois)

### Axe 2 — Pipeline 5 étapes conditionnelles ✅

**Fait** :
- `testing-mandatory.md` neo_ia + ia_back : workflow 5 étapes
- Citation Anthropic intégrée : *"ONE failing test per behavior per cycle"*
- Phase REFACTOR test-writer définitivement supprimée

### Axe 3 — Refonte hooks 16/15 → ~6 ⛔ REPORTÉ

**DA a refusé pour ce soir**. Diff entre intention (réduire friction) et réalité (4 bloquants techniques).

→ À traiter demain avec analyse fine par hook (project-auditor + DA fresh + tests comportementaux PASS/FAIL en session fraîche).

## Bug bonus diagnostiqué pendant la session

**Marker `.architect-marker` disparaît entre dispatches dev**.

Root cause : `session-reset-markers.py` se déclenche sur `SessionStart` au démarrage de **chaque sub-agent en isolation worktree** (v2.1.69+ Anthropic doc). Le wipe était inconditionnel sauf `source==resume`.

Fix : ne wipe QUE si `source==startup` ET pas d'`agent_type`/`agent_id`/`subagent_type` présent dans le stdin.

Commits : neo_ia `25abe5d` + ia_back `a9fb5fd`.

## Apprentissage méta — règle Jarvis

> **Quand un workaround revient ≥ 2 fois dans la même session, c'est un bug à diagnostiquer, pas un workflow à mémoriser.**

Raphael a accepté 3× "je relance l'architect en fast-pass pour reposer le marker". À la 3e fois = signal fort. **À l'avenir, dès la 2e occurrence du workaround, diagnostiquer le hook** au lieu d'absorber le surcoût.

## Apprentissage méta — raisonner par friction/valeur, pas par budget

Proposition initiale "16 → 6 hooks" = **anti-pattern**. Raisonnement par budget de comptage ("trop d'hooks") au lieu de friction/valeur (lequel cause de la friction sans valeur ajoutée).

Bonne question : **"Quel hook cause de la friction sans valeur ajoutée ?"** → kill ciblé.
Mauvaise question : **"Comment réduire de 16 à 6 ?"** → kill aveugle qui casse `/go`.

## Apprentissage méta — Anthropic ≠ "max 3 tests batch"

L'erreur de la doctrine 22 mai : "MAX 3 tests par comportement". Lu sans contexte, ça permet **3 tests en batch d'un coup**.

La vraie best practice Anthropic : **1 test à la fois en boucle red-green courte**. La couverture finale d'une feature peut atteindre 6-8 tests, mais générés en 6-8 cycles red-green courts, pas en batch.

→ Doctrine corrigée 21 mai dans :
- `neo_ia/.claude/agents/test-writer.md`
- `ia_back/.claude/agents/test-writer.md`
- `neo_ia/.claude/rules/testing-mandatory.md`
- `ia_back/.claude/rules/testing-mandatory.md`

## Commits

| Repo | Hash | Description |
|------|------|-------------|
| neo_ia | `a27ccec` | 3 hooks patchés (bypass agents, resume, read-only) |
| neo_ia | `25abe5d` | Fix marker wipe sub-agent worktree |
| neo_ia | `342a8b0` | Kill tdd-guard + on-env-protect + nettoyage doctrine |
| ia_back | `a78f996` | 3 hooks miroir |
| ia_back | `a9fb5fd` | Fix marker miroir |
| ia_back | `6d037e1` | Kill tdd-guard.ts miroir |

## Pipeline final ce soir (à appliquer demain matin)

```
[Bug fix S] architect (fast pass 30-60s, BYPASS tests) → dev → code-reviewer → commit
[Bug fix M] architect → test-writer (1 test non-régression) → dev → code-reviewer → commit
[Feature M] architect (plan + matrice) → test-writer (1 test happy path) → dev → boucle 1 test edge / dev → code-reviewer → commit
[Feature L] advisor → architect → test-writer (1 test à la fois) → dev (boucle) → code-reviewer → security/perf si applicable → commit
```

## Liens

- [[raisonnement-kill-tdd-strict-hooks-mai-2026]] — DA verdict initial
- [[critique-2026-05-21-refonte-hooks-16-vers-6]] — DA verdict refonte hooks
- [[workflow-claude-code-optimal]] — pipeline canonique mis à jour
- [[workflow-claude-code-optimal]] — référence Boris/Erik/Thariq/Karpathy
- [[erreur-pipeline-trop-long-frustration]] — erreur déclencheur 21 mai
- [[raisonnement-22mai-doctrine-vs-enforcement]] — bug marker initial (3 root causes)
- [[raisonnement-revirement-pipeline-mai-2026]] — pivot précédent 22 mai
- [[workflow-claude-code-optimal]]
