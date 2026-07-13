---
name: allocation-modele-effort-doctrine
description: Doctrine consolidée modèle/effort — Sonnet exécution / Opus jugement, xhigh RÉSERVÉ (architect, dev-lead, refactor-pg), calibrer par TYPE, questionner le biais tokens Anthropic, mesurer avant bump. Pipeline repos projet architect-first + code-reviewer séparé.
metadata:
  type: feedback
---

Chaîne décisionnelle 2026 (21 mai → 22 mai → 26 mai). Foyer canonique live : CLAUDE.md § « Effort calibré (doctrine 26 mai 2026) » + vault [[workflow-claude-code-optimal]] + [[effort-opus-47-doctrine-anthropic-2026]] + [[raisonnement-revirement-pipeline-mai-2026]]. Ce feedback porte les spécifiques repos projet et le réflexe anti-biais non repris ailleurs.

**Allocation modèle (validé CwC 2026 + Raphael 21 mai)** : agents d'EXÉCUTION (dev, schema-mapper) = `sonnet, high` ; agents de JUGEMENT (architect, code-reviewer, security, debugger, analystes read-only) = `opus`. Exception : `dev-neochat` reste Opus (LangGraph multi-agent trop complexe pour Sonnet). SUPERSEDE la politique « zero sonnet » du 5 mai 2026 (EVE Legal CwC : « frontier quality at 5x lower cost » en séparant exécution et conseil).

**Effort (révisé 22 mai après frustration 4h/feature, recalibré 26 mai)** : `xhigh` RÉSERVÉ à l'exploration agentique multi-tours profonde (`architect`, `dev-lead`, `refactor-pg-function` ; côté forge : architect-deep, project-auditor, project-analyzer). `high` PARTOUT ailleurs — dev exécution `sonnet, high`, test-writer `opus, high` (PAS xhigh), code-reviewer/security-reviewer/analystes `opus, high`. Mécanique pur (scan, maintenance, inspection) = `medium`/`low`. `max` jamais en frontmatter.

**Anti-biais Anthropic (verbatim Raphael 26 mai)** : « Anthropic réfléchit avec des tokens illimités, moi je paie le réel. xhigh partout = leur intérêt commercial, pas le mien. » xhigh ≈ +3-6 points pour 2× tokens vs high. Ne JAMAIS appliquer « Anthropic dit xhigh default » aveuglément : calibrer par TYPE de tâche réelle, et **mesurer empiriquement avant de bump** (1 run high vs 1 run xhigh sur la même tâche, comparer l'output).

**Pipeline repos projet (ia_back + neo_ia)** : architect-first obligatoire (même tâches S, fast pass 1 tour) → dev → test-writer (densité MAX 3 tests + bypass `.tdd-bypass` : [[feedback_test_writer_systematic]]) → code-reviewer SÉPARÉ (design ≠ review) → commit. `neo-brain-dev-ia` injecté UNIQUEMENT sur dev-neochat + dev-lead (seuls consommateurs de l'API ia_back).

**Why:** trois amendements successifs se désignaient chacun « fait foi » sur le précédent (all_opus 21 mai → opus47 22 mai → biais full-thune 26 mai) — la doctrine vivait éclatée sur 3 fichiers + CLAUDE.md, avec réconciliations manuelles répétées (cf log archive 2026-06-05). Un seul foyer memory désormais ; CLAUDE.md reste le résumé canonique chargé chaque session.
**How to apply:** au moment de fixer `model:`/`effort:` d'un agent (création, audit, revue de frontmatter) → appliquer le tableau ci-dessus ; en cas de doute sur un bump d'effort, mesurer avant.

Consolide depuis : [[feedback_all_opus]], [[feedback_opus47_workflow]], [[feedback_anthropic_doctrine_biais_full_thune]] (fusionnés le 9 juillet 2026 — amendements successifs, archivés dans `_archive/2026-07/`).
