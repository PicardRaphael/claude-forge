---
titre: "Critique — Setup TDD strict neo_ia (architect-first + RED obligatoire + chaîne markers)"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-21
auteur: claude
aliases:
  - "critique tdd strict neo ia"
  - "da setup tdd 21 mai"
  - "verdict tdd bloquant neoteem"
  - "anthropic best practice tdd faux"
  - "critique pipeline neo_ia 4h fix bug"
tags:
  - "#type/critique"
  - "#projet/neo_ia"
  - "#technique/agents"
  - "#domaine/claude-code"
resume: "DA 21 mai sur la proposition implicite que le pipeline TDD strict neo_ia (architect-first bloquant + RED obligatoire + 5 hooks markers chaînés) est Anthropic best practice. Verdict EVOLVE — ni Boris ni Erik ni Thariq ni Karpathy ne prescrivent TDD-as-hook. La doctrine 22 mai (pipeline-boris-adapte-neoteem) corrige déjà mais n'est pas déployée sur neo_ia"
sources:
  - "Session 2026-05-21 frustration utilisateur 4h fix BERNAT"
  - "Vault Knowledge/erreurs/erreur-pipeline-trop-long-frustration.md"
  - "Vault Knowledge/raisonnements/raisonnement-revirement-pipeline-mai-2026.md"
  - "Vault Knowledge/erreurs/erreur-architect-marker-pipeline-neoia.md"
  - "Vault 04-Techniques/patterns/pipeline-boris-adapte-neoteem.md"
  - "Vault 04-Techniques/patterns/best-practices-claude-code-leaders.md"
  - "Vault 04-Techniques/patterns/boris-workflow-2026-may.md"
  - "Lecture directe neo_ia/.claude/rules/quality-gates.md + testing-mandatory.md"
---

# Critique — Setup TDD strict neo_ia (architect-first + RED obligatoire + chaîne markers)

## Proposition implicite analysée

> "Le setup TDD strict actuel de neo_ia (architect-first hook bloquant + test-writer phase RED obligatoire + marker .architect-marker + bypass impossibles + 3-5 tours d'agents avant la moindre ligne de code) est la bonne pratique recommandée par Anthropic / l'équipe Claude Code et doit être maintenu tel quel."

## Verdict

**Bloquants :** 6 (technique 4 + stratégique 2 + pratique 1, soit 7 avec recouvrement)
**Décision :** **EVOLVE urgent — ni KILL ni KEEP.**

## Diagnostic central

Le setup n'est PAS Anthropic best practice. C'est une sur-interprétation défensive interne neo_ia. La doctrine correcte existe DÉJÀ dans le vault depuis 24h (`pipeline-boris-adapte-neoteem.md`) mais n'a pas été déployée à neo_ia ou l'a été partiellement → contradictions internes entre rules (`quality-gates.md` ligne 116 dit "phase REFACTOR SUPPRIMEE" mais `testing-mandatory.md` ligne 124 la maintient comme étape 4 obligatoire).

## Plan d'action validé

### Ce soir (débloquer fix BERNAT)
1. STOP test-writer pour ce bug — c'est un bug fix avec repro, pas une feature greenfield
2. `git checkout` les 18 fichiers de tests créés pour modules inexistants
3. `touch .tdd-bypass` à la racine neo_ia
4. dev-shared-tools direct avec diagnostic architect dispatch 2 comme contexte
5. Fix BERNAT
6. Écrire 1-2 tests de non-régression APRÈS le fix
7. `rm .tdd-bypass` + commit

Si architect-guard bloque : `touch .architect-marker` manuellement (existence binaire).

### Demain (refonte neo_ia)
1. Aligner `testing-mandatory.md` avec `quality-gates.md` (supprimer étape 4 REFACTOR)
2. Patcher 3 bugs hooks documentés dans `erreur-architect-marker-pipeline-neoia.md`
3. Ajouter mode "BUG FIX REPRO" explicite dans matrice architect
4. Vérifier journalier.md reflète la doctrine 22 mai

### ia_back (préventif)
NE PAS recopier la chaîne 5 hooks markers. Garder uniquement `tdd-guard.py` + `dispatch-guard.py`.

## Citations vault qui démontrent que TDD strict n'est PAS Anthropic best practice

- `boris-workflow-2026-may.md` : Boris fait Plan Mode + auto-accept + 150 PRs/jour, zéro mention TDD-as-hook
- `best-practices-claude-code-leaders.md` : Boris/Erik = planifier avant, mais pas "tests rouges avant code"
- Erik Schluntz : "Forget the code, focus on the product" — anti-TDD-as-doctrine
- Thariq : "ne pas être trop spécifique, laisser de la flexibilité" — contre enforcement rigide
- Karpathy : "Simplicity, Surgical changes" en premier — 68 tests pour 1 bug fix = anti-Karpathy
- Citation Willison "red-green TDD it's like five tokens" parle de TDD LÉGER, pas pipeline 8-agents

Le seul défenseur du TDD strict cité dans le vault forge c'est la doctrine interne neo_ia elle-même. Pas de caution externe.

## Anti-patterns réactivés

Le setup actuel a réactivé 4 anti-patterns documentés dans le vault :
1. `pipeline-systematique-8-agents-meme-crud-simple` (erreur-pipeline-trop-long-frustration)
2. `test-writer-2-passes-RED-REFACTOR` (devrait être 1 passe)
3. `chaine-marker-5-hooks-combinatoire-fragile` (erreur-architect-marker-pipeline-neoia)
4. `workaround-becomes-sediment` (.tdd-bypass + CLAUDE_AGENT bypass + manual marker = sédiments)

## Méta-leçon

La doctrine forge évolue plus vite que son déploiement dans les repos applicatifs. Risque : désynchronisation entre vault (état corrigé) et repos (état précédent). Quand une révision majeure est capitalisée dans le vault, suivre dans les 24h par un déploiement effectif sur TOUS les repos concernés, sinon la session suivante revivra l'erreur initiale.

**Règle Jarvis confirmée** : "quand un workaround revient ≥ 2 fois dans la même session, c'est un bug à diagnostiquer, pas un workflow à mémoriser." Ce soir, 3 fast-pass architect = 240k tokens. Bugs documentés et non patchés.

## Liens

- [[erreur-pipeline-trop-long-frustration]]
- [[raisonnement-revirement-pipeline-mai-2026]]
- [[erreur-architect-marker-pipeline-neoia]]
- [[pipeline-boris-adapte-neoteem]]
- [[best-practices-claude-code-leaders]]
- [[boris-workflow-2026-may]]
- [[critique-2026-05-21-refonte-pipeline-boris-pattern]]
- [[feedback_workaround_sediment]] (mémoire)
- [[feedback_pipeline_quality_gates]] (mémoire — révisé 22 mai)
