---
name: creer-workflow-cc
description: Règles de design apprises au 1er build réel d'un workflow .claude/workflows/ (verify-diff neo_ia, 27 juil. 2026) — à promouvoir en canonique vault au 2e-3e workflow
metadata:
  type: reference
---

Premier workflow réel construit : `verify-diff` (neo_ia, fan-out reviewer/security/performance). Règles de design vérifiées :

1. **`agentType: '<nom>'` résout les agents projet du repo où la SESSION tourne** — un workflow neo_ia utilisant `reviewer` n'est testable que depuis une session neo_ia, pas depuis forge. Écrire cross-repo OK, tester = session cible.
2. **JAMAIS `isolation: worktree` si les agents doivent lire des fichiers gitignorés** (`.tmpclaude/`, relais /feature) — un worktree frais ne les contient pas. Fan-out read-only = pas de worktree nécessaire de toute façon.
3. **Le script JS n'a pas accès au filesystem ni à git** → la session appelante passe le scope via `args` (files, sections de relais lues par elle), OU une 1re stage « scout » (agent effort low + schema) calcule le diff. Vérifier quels agents ont Bash : ceux qui l'ont lisent le diff eux-mêmes, ceux qui ne l'ont pas (reviewer neo_ia) reçoivent la liste en brief.
4. **Contrat args tout-optionnel** = le workflow marche en slash command manuel (auto-détection par heuristiques de chemins) ET en invocation pipeline (l'appelant passe verifiers/relay explicites).
5. **Consolidation en JS pur** (dedup clé file:line:desc, mapping des taxonomies de sévérité entre agents) — pas d'agent consolidateur, aucun finding perdu ; vérificateur mort → verdict `INCOMPLET`, jamais silencieux.
6. **Point d'intégration minimal** : ne remplacer le dispatch direct QUE là où ≥ 2 agents tournent (parallélisme réel) — 1 seul agent = le workflow n'apporte que du surcoût. Les boucles à checkpoint humain restent en skill.
7. **Valider par `node --check`** avant commit (syntaxe JS, node dispo sur la machine).
8. Méthode chantier cross-repo quand le checkout cible est occupé par une branche en cours : `git worktree add <chemin-hors-repo> -b chore/<sujet> origin/develop`, édits dans le worktree, push, `git worktree remove` — zéro pollution du travail en vol.

**Prochain cas d'usage prévu** : workflow cc-news (orchestration 16 agents). Au 2e-3e build → promouvoir en note canonique vault `comment-creer-workflow` (cf memory-discipline).
