---
name: allocation-modele-effort-doctrine
description: Doctrine consolidée modèle/effort — Sonnet exécution / Opus jugement, calibrer par TYPE, try-vs-know (Lydia Hallie) + mesurer avant bump. ⚠️ Point de départ xhigh PÉRIMÉ sur Opus 5 (officiel = high, low/medium en primary control, fresh effort sweep si settings hérités — vérifié 29 juil.). Pipeline repos projet architect-first + code-reviewer séparé.
metadata:
  type: feedback
---

Chaîne décisionnelle 2026 (21 mai → 22 mai → 26 mai). Foyer canonique live : CLAUDE.md § « Effort calibré (doctrine 26 mai 2026) » + vault [[workflow-claude-code-optimal]] + [[effort-opus-47-doctrine-anthropic-2026]] + [[raisonnement-revirement-pipeline-mai-2026]]. Ce feedback porte les spécifiques repos projet et le réflexe anti-biais non repris ailleurs.

**Allocation modèle (validé CwC 2026 + Raphael 21 mai)** : agents d'EXÉCUTION (dev, schema-mapper) = `sonnet, high` ; agents de JUGEMENT (architect, code-reviewer, security, debugger, analystes read-only) = `opus`. Exception : `dev-neochat` reste Opus (LangGraph multi-agent trop complexe pour Sonnet). SUPERSEDE la politique « zero sonnet » du 5 mai 2026 (EVE Legal CwC : « frontier quality at 5x lower cost » en séparant exécution et conseil).

**Effort (Option C, arbitrée 18 juin — remplace la formulation « xhigh réservé » du pivot 22 mai)** : `xhigh` = défaut de l'exploration agentique/coding multi-tool long-horizon (ex. `architect`, `dev-lead`, `refactor-pg-function` ; côté forge : repo-inspector). `high` = jugement/comparatif structuré — dev exécution `sonnet, high`, test-writer `opus, high` (PAS xhigh), code-reviewer/security-reviewer/analystes/**reviewers dont devils-advocate** `opus, high`. Mécanique pur (scan, maintenance, inspection) = `medium`/`low`. `max` jamais en frontmatter. Source : [[conflit-effort-xhigh-anthropic-vs-pivot-22mai]] (résolue) + [[effort-opus-47-doctrine-anthropic-2026]].

**Critère officiel effort vs modèle (Lydia Hallie, blog claude.com 7 juil. 2026, REINFORCE)** : « did it not *try* hard enough, or did it not *know* enough? » — fichiers sautés/vérification manquante → monter l'EFFORT ; erreur malgré contexte complet et vraie tentative → monter de MODÈLE. Modèle = plafond de capacité, effort = quantité de travail par tour.

**Opus 5 (24 juil. 2026)** : `opus` (alias frontmatter/CLAUDE.md) résout désormais vers `claude-opus-5` (nouveau défaut Opus, $5/$25 inchangé, thinking ON par défaut). Arbitrage Raphael 27 juil. : laisser les agents jugement tourner sur Opus 5 et surveiller ; épingler `claude-opus-4-8` explicitement seulement si dérive constatée.

**⚠️ PÉRIMÉ sur Opus 5 — point de départ xhigh (vérifié en primaire 29 juil. 2026)** : la page officielle [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) recommande `xhigh` pour Opus **4.7/4.8** mais **`high` pour Opus 5** : « Start with `high`, the default … use `low` and `medium` **liberally as your primary control** for token cost », plus l'avertissement qui vise exactement forge : « **If you carried effort settings over from an earlier model, run a fresh effort sweep on your evals rather than reusing them.** » Comme l'alias `opus` résout vers Opus 5, tous les agents `opus, xhigh` héritent d'un défaut désormais non recommandé. Le *principe* Option C (calibrer par TYPE) reste valide — c'est son point de départ qui descend de `xhigh` à `high`, `xhigh` devenant un step-up mesuré (« demanding coding and agentic work »). Détail + verbatims par modèle : [[effort-opus-47-doctrine-anthropic-2026]] § « Recommandation officielle Anthropic — DÉPEND DU MODÈLE ».

**Anti-biais CONFIRMÉ par Anthropic** : la ligne du 26 mai (ci-dessous) anticipait la doctrine officielle. Sur Opus 5, Anthropic désigne lui-même `low`/`medium` comme « primary control » du coût — forge ne les utilise quasiment pas. L'instinct « ne pas appliquer xhigh aveuglément » est désormais adossé à une source primaire, pas seulement à une préférence de coût.

**Anti-biais Anthropic (verbatim Raphael 26 mai)** : « Anthropic réfléchit avec des tokens illimités, moi je paie le réel. xhigh partout = leur intérêt commercial, pas le mien. » xhigh ≈ +3-6 points pour 2× tokens vs high. Ne JAMAIS appliquer « Anthropic dit xhigh default » aveuglément : calibrer par TYPE de tâche réelle, et **mesurer empiriquement avant de bump** (1 run high vs 1 run xhigh sur la même tâche, comparer l'output).

**Pipeline repos projet (ia_back + neo_ia)** : architect-first obligatoire (même tâches S, fast pass 1 tour) → dev → test-writer (densité MAX 3 tests + bypass `.tdd-bypass` : [[feedback_test_writer_systematic]]) → code-reviewer SÉPARÉ (design ≠ review) → commit. `neo-brain-dev-ia` injecté UNIQUEMENT sur dev-neochat + dev-lead (seuls consommateurs de l'API ia_back).

**Why:** trois amendements successifs se désignaient chacun « fait foi » sur le précédent (all_opus 21 mai → opus47 22 mai → biais full-thune 26 mai) — la doctrine vivait éclatée sur 3 fichiers + CLAUDE.md, avec réconciliations manuelles répétées (cf log archive 2026-06-05). Un seul foyer memory désormais ; CLAUDE.md reste le résumé canonique chargé chaque session.
**How to apply:** au moment de fixer `model:`/`effort:` d'un agent (création, audit, revue de frontmatter) → appliquer le tableau ci-dessus ; en cas de doute sur un bump d'effort, mesurer avant.

Consolide depuis : [[feedback_all_opus]], [[feedback_opus47_workflow]], [[feedback_anthropic_doctrine_biais_full_thune]] (fusionnés le 9 juillet 2026 — amendements successifs, archivés dans `_archive/2026-07/`).
