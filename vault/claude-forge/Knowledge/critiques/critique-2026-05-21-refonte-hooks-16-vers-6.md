---
titre: "Critique — Refonte hooks neo_ia + ia_back (16/15 → ~6)"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-21
auteur: claude
aliases:
  - "critique refonte hooks 21 mai"
  - "da hooks neoia iaback 6 essentiels"
  - "verdict kill tdd guard et hooks"
  - "critique fusion triplet auth"
tags:
  - "#type/critique"
  - "#projet/neo_ia"
  - "#projet/ia_back"
  - "#technique/hooks"
  - "#domaine/claude-code"
resume: "DA 21 mai sur la proposition Axe 1 (kill tdd-guard) + Axe 2 (5 étapes conditionnelles) + Axe 3 (16/15 hooks → ~6). Verdict LIVRER AVEC CORRECTIONS — 4 bloquants factuels après lecture du code : le triplet auth-detector/repo-scope-guard/auth-cleanup est NON FUSIONNABLE (3 events différents), pipeline-reset.py n'est PAS un hook event mais un script appelé par /go ligne 160 de SKILL.md, typecheck.ts est un piège performance 30s/edit non documenté, guard-core-imports.ts est une règle archi hexagonale irremplaçable par ruff/ts-prune. Ce soir : 3 kills ciblés (tdd-guard × 2 + on-env-protect). Demain : refonte ciblée avec DA fresh + tests comportementaux."
sources:
  - "Lecture directe code 9 hooks neo_ia + 4 hooks ia_back"
  - "Vault critique-2026-05-21-setup-tdd-strict-neoia.md (DA précédent verdict EVOLVE)"
  - "Memory feedback_session_multi_chantiers + behavioral-test-after-setup + tests-adverses-obligatoires"
  - "Commits a27ccec (neo_ia) + a78f996 (ia_back) déjà appliqués"
---

# Critique — Refonte hooks neo_ia + ia_back (16/15 → ~6)

## Verdict synthétique

**Bloquants : 4 | Avertissements : 5 | Nitpicks : 2**
**Décision : LIVRER AVEC CORRECTIONS — refonte ciblée demain, pas refonte massive ce soir.**

## Bloquants factuels (vérifiés en lisant le code)

### Bloquant 1 — Triplet auth NON FUSIONNABLE
Les 3 hooks tournent sur 3 events Claude Code différents :
- `auth-detector.py` = UserPromptSubmit (crée marker depuis phrase Raphael)
- `repo-scope-guard.py` = PreToolUse (lit marker, bloque accès)
- `auth-cleanup.py` = SessionStart (wipe markers)

Impossible de câbler un seul .py sur trois events. La fusion forcerait un méga-hook fragile détectant son contexte via stdin. Coût > bénéfice. KEEP séparé.

### Bloquant 2 — pipeline-reset.py N'EST PAS un hook redondant
Grep confirme : appelé explicitement par `.claude/skills/go/SKILL.md` ligne 160. Pas event-triggered. Le supprimer = casser la skill `/go` silencieusement. session-reset-markers.py est le hook SessionStart avec logique distincte (skip si source==resume). Garder les deux.

### Bloquant 3 — typecheck.ts piège performance
Code : `Bun.spawnSync(["bun", "run", "typecheck"], { timeout: 30_000 })` sur CHAQUE write .ts. 10 edits = 50-150s de latence cumulée bloquante. Décision binaire requise : async (PostToolUse non-bloquant) ou kill et déléguer à pre-commit. Pas "à vérifier".

### Bloquant 4 — guard-core-imports.ts N'EST PAS un linter
36 lignes qui bloquent `src/core/` important `@infra/` ou `drizzle-orm`. C'est une règle d'architecture hexagonale. Ni ruff (Python) ni ts-prune (dead exports) ne valident ça. Remplaçable seulement par ESLint custom (`no-restricted-imports` ou `eslint-plugin-boundaries`). KEEP tant que ESLint config pas en place.

## Plan ce soir vs demain

**Ce soir (30 min max, sûr) :**
1. KILL `tdd-guard.py` neo_ia + `tdd-guard.ts` ia_back
2. KILL `on-env-protect.py` neo_ia (30L, redondant gitignore + auto-mode classifier)
3. Commit + dodo

**Demain (refonte ciblée, DA fresh, tests comportementaux) :**
- Décision typecheck.ts (async ou kill)
- Décision guard-pytest-scope / guard-test-scope
- Audit complet hooks restants (session-health pas mentionné)
- Test PASS/FAIL en session fraîche

## Verdict détaillé par hook

**neo_ia :**
- tdd-guard.py : KILL ce soir
- guard-pytest-scope.py : KILL-DIFFÉRÉ ou KEEP (non fusionnable, scope Bash ≠ dispatch-guard Write)
- pipeline-reset.py : KEEP (script /go, pas hook)
- on-env-protect.py : KILL ce soir
- repo-scope-guard.py / auth-detector.py / auth-cleanup.py : KEEP (triplet non fusionnable)
- spec-brief-boundary-guard.py : KEEP (déjà conditionnel ligne 174)
- on-push-notify.py : KEEP (notification, silent si pas de webhook)

**ia_back :**
- tdd-guard.ts : KILL ce soir
- guard-test-scope.ts : KILL-DIFFÉRÉ
- pipeline-reset.ts : KEEP (probable, vérifier comme côté Python)
- guard-core-imports.ts : KEEP (règle archi, irremplaçable par ruff/ts-prune)
- spec-brief-boundary-guard.ts : KEEP
- typecheck.ts : DÉCISION REQUISE demain (async ou kill)

## Risques

- Refonte ciblée (kill tdd-guard ×2 + on-env-protect) : risque régression 2/10
- Refonte massive ce soir telle que proposée : risque régression 7/10 (casse /go, perd archi hexagonale, fusion triplet impossible = 3 bugs demain matin)

## Ancrage vault

- `critique-2026-05-21-setup-tdd-strict-neoia.md` : DA précédent verdict EVOLVE, pas refonte. La proposition actuelle dépasse ce verdict.
- Memory `feedback_session_multi_chantiers` : "JAMAIS 4+ chantiers en fin de session fatiguée"
- Memory `behavioral-test-after-setup` : "Tester PASS/FAIL en session fraîche AVANT déclarer fonctionnel"
- Memory `tests-adverses-obligatoires` : "Hooks sécurité/enforcement : DA AVANT push"
- Memory `enforce-not-advise` : "Tout advisory skippé = hook bloquant". La refonte va dans le sens INVERSE — à acter consciemment, pas par fatigue.

## Pattern à mémoriser

**Anti-pattern observé : raisonner par budget de hooks ("16 → 6") au lieu de par friction/valeur de chaque hook.** Le bon nombre n'est pas une cible — c'est le résultat de l'audit hook-par-hook (valeur métier × fréquence × friction tolérable). Réinstaller cette discipline avant toute refonte hooks future.

Lié : [[pipeline-boris-adapte-neoteem]], [[critique-2026-05-21-setup-tdd-strict-neoia]]
