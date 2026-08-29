---
description: Toute décision de naming/structure prise sur un repo doit être propagée explicitement aux autres repos concernés. Les décisions ne s'auto-propagent jamais.
---

# Cross-repo propagation — Décisions naming/structure

## Principe

Quand une décision de naming, structure ou doctrine est prise sur un repo, elle ne se propage JAMAIS automatiquement aux autres. Réflexe immédiat après toute décision : **"est-ce que ça s'applique aux autres repos ?"**

## Checklist repos concernés

La procédure de résolution des chemins vit dans `AGENTS.md` : résoudre sur la machine courante, puis utiliser `git -C <chemin>`. Ne recopier aucun chemin absolu.

## Protocole

1. **Identifier le scope** : décision forge-only → pas de propagation. Décision multi-repo → continuer.
2. **Vérifier la présence du repo AVANT** (2 machines — un repo peut être absent ici et présent là-bas) : `[ -d "$repo/.git" ]`. Absent → annoncer le skip à Raphael, ne pas improviser de chemin.
3. **Pour chaque repo présent** :
   - Identifier le composant à modifier (agent, skill, rule, CLAUDE.md)
   - **Write en session principale** — jamais délégué à un sub-agent (bloqué cross-repo, et `delegate-guard` lit l'`attributionSkill` de la session principale). Cf `delegate-to-specialists.md` + `mcp-brief-then-direct.md` § contre-exemple.
   - Chemin résolu dynamiquement, jamais recopié (cf `AGENTS.md`)
4. **Vérifier empiriquement** après propagation : grep le terme modifié sur chaque repo.
4. **Documenter** dans le vault si décision à valeur canonique :
   ```
   mcp__forge-brain__create_note(path="Knowledge/decisions/<sujet>.md", ...)
   ```

## Aligner un repo jumeau (alignement de masse, pas décision ponctuelle)

Quand on aligne un repo entier sur un jumeau de référence (ex. neo_ia ↔ neoteem-back-ts, 11 juin 2026), ce N'EST PAS un copier-coller :

1. **Gap analysis par agent read-only** : un agent dresse la matrice CONFORME / MANQUANT / DIVERGENT du `.claude/` cible vs la référence, avec preuve `file:line` — on traite des écarts mesurés, pas une impression.
2. **Adapter à la stack, jamais copier l'outil** : l'équivalent d'intention, pas le binaire. `@ts-nocheck`→`# type: ignore` nu, jscpd-TS→jscpd-Python+import-linter, typecheck tsc Stop→mypy Stop scopé CI, agent sécu OWASP→4 risques IA (prompt injection/PII/hallucination/token leak). Un « manquant » qui ne mappe pas sur la stack (frontières hexagonales sur un repo non-hexagonal) = SKIP justifié, pas porté de force.
3. **Ratchet sur tout gate qualité posé sur du legacy** : seuil = état mesuré, jamais big-bang rouge (cf `reference_ratchet_gates_legacy` neo_ia). Mesurer AVANT de gater.
4. **Baliser le hors-prod sans l'auditer** : code hors prod (neomail/neodoc) exclu du strict (`per-file-ignores`, tests CI conditionnels par chemin) MAIS protégé comme cible interdite pour le prod (contrat import-linter neochat↛neomail). On ne fait pas semblant de le maintenir.
5. **Vraie sécu ≠ baseline silencieuse** : un risque réel détecté pendant l'alignement (SQL injection) → story dédiée, jamais noqa aveugle ; seul le bruit (asserts tests, faux positifs) se baseline.

## Gotchas

- **Décisions naming silencieuses** : renommer sans propager = drift pendant des semaines (ex : `cto-mindset` → `orchestrator-mindset` sur neo_ia, non propagé ia_back, découvert audit 25 mai)
- **Sub-agents bloqués write cross-repo** : session principale doit faire les writes cross-repo, pas déléguer
- **Path absolu obligatoire** pour agent cross-repo : chemin relatif = fail silencieux
- **Scope forge ≠ règle universelle** : vérifier si la règle s'applique à tous les repos avant propagation

Source : `memory/_archive/2026-07/feedback_propagate_decisions_cross_repo.md` (feedback d'origine absorbé par cette rule, archivé 2026-07-09)
