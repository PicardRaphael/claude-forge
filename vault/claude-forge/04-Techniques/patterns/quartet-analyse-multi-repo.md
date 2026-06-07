---
titre: "Quartet d'agents forge pour analyse multi-repo"
resume: "Pattern d'analyse complet d'un repo via 4 agents forge complémentaires : project-analyzer (vue projet) + project-auditor (audit .claude/) + codebase-scanner (code applicatif) + devils-advocate (critique livrables). Évite general-purpose catch-all et l'agent local par repo."
aliases:
  - "quartet analyse multi-repo"
  - "4 agents analyse repo"
  - "project-analyzer project-auditor codebase-scanner"
  - "codebase-scanner forge"
  - "analyse repo agents forge"
  - "trio + DA analyse"
derniere-maj: 2026-05-25
auteur: claude
type: technique
sources:
  - "[[methode-analyser-repo]]"
  - "Session forge 25 mai 2026 : audit neo_ia 15 tâches"
tags:
  - "#type/technique"
  - "#type/pattern"
  - "#domaine/claude-code"
  - "#domaine/orchestration"
  - "#pattern/audit"
---

# Quartet d'agents forge pour analyse multi-repo

## QUOI

4 agents forge complémentaires couvrant l'intégralité de l'analyse d'un repo applicatif :

| Agent | Scope | Modèle | Couleur | Output |
|-------|-------|--------|---------|--------|
| **`project-analyzer`** | Vue projet haut niveau + recommandations | Opus | purple | Analyse globale + propositions CC |
| **`project-auditor`** | Audit `.claude/` (config Claude Code) | Sonnet/Opus | purple | Rapport conformité canoniques |
| **`codebase-scanner`** | Code applicatif réel (étape 1b/1c/1d/5 de [[methode-analyser-repo]]) | Sonnet | purple | Topologie + 5 fichiers + patterns + candidats CC |
| **`devils-advocate`** | Critique livrables majeurs | Opus | red | Verdict BLOCKING/PASS/WARN |

## POURQUOI

Avant cette innovation (25 mai 2026) :
- `project-auditor` seul → couvre `.claude/` mais ignore le code applicatif
- `project-analyzer` seul → vue projet sans descente technique
- `general-purpose` catch-all → pas spécialisé, prompt à réinventer à chaque fois
- Solution alternative envisagée : agent `codebase-analyst` LOCAL à chaque repo (vu dans neo_ia) → multiplication d'agents identiques cross-repos, anti-DRY

Le quartet résout : **1 agent forge agnostique du repo cible**, dispatché par session principale claude-forge.

## COMMENT — Pattern d'invocation

### Mode "audit complet d'un repo X"

Session principale forge dispatche en **parallèle (1 message, multi-Agent)** :

```
Agent(project-auditor)    — audit .claude/ par catégorie (1 agent par cluster : agents / skills / hooks / rules+CLAUDE.md = 4 sub-agents)
Agent(codebase-scanner)   — scan code réel (1 sub-agent)
Agent(project-analyzer)   — vue projet + propositions (si pas déjà fait via les 5 ci-dessus)
```

Soit **5 sub-agents en parallèle** pour `.claude/` × 4 catégories + 1 codebase-scanner = couverture complète sans overlap.

Puis :
```
Agent(devils-advocate)    — critique du plan d'action issu des 5 audits (si livrable majeur)
```

### Mode "scan code uniquement"

`Agent(codebase-scanner)` seul, avec brief = repo cible + méthode 6 étapes 1b/1c/1d/5.

## QUAND L'UTILISER

| Situation | Quartet ? |
|-----------|-----------|
| "Analyse poussée de X" | OUI — complet |
| "Audit `.claude/` de X" | NON — project-auditor seul suffit |
| "Propose-moi config CC pour X" | OUI — quartet (Anthropic 6 étapes méthode-analyser-repo) |
| Repo familier, fix mineur | NON — overkill |
| Découverte nouveau repo | OUI — quartet |
| Avant refonte structurelle | OUI — quartet + DA |

## SÉQUENCE D'EXÉCUTION

```
Phase 1 — Brief (session principale)
   ↓
   Lire canoniques EN ENTIER via MCP forge-brain (read_note)
   Lister composants `.claude/` du repo cible (Glob)
   Dispatcher les 4-5 sub-agents en parallèle
   ↓
Phase 2 — Audits parallèles
   ↓
   project-auditor × N (1 par cluster)
   codebase-scanner × 1
   ↓
Phase 3 — Vérif empirique session principale
   ↓
   Grep / Read / Bash pour valider claims sub-agents (cf [[feedback_audit_claims_after_brief]])
   ↓
Phase 4 — Plan priorisé
   ↓
   Croiser les 5 rapports → écarts mesurables → vagues P0/P1/P2/P3
   ↓
Phase 5 — Validation Raphael
   ↓
   Phase 6 — Exécution en vagues parallèles
```

## RÉSULTAT MESURÉ — neo_ia 25 mai 2026

- 15 tâches enchaînées (5 audits + 10 fixes en 4 vagues)
- 100% succès
- ~660 LOC supprimées (déduplication + consolidation)
- 4 nouvelles skills code-gen (compounding patterns observés)
- 3 nouveaux hooks lint (boundaries empiriques)
- 1 nouvel agent forge (codebase-scanner) né de l'exercice lui-même

## ANTI-PATTERNS

- ❌ Quartet sur tâche S (< 30 min) — overkill, 1 agent suffit
- ❌ Sub-agents en série au lieu de parallèle — perte de temps × 5
- ❌ Pas de vérif empirique entre sub-agents et synthèse — risque claims non vérifiés
- ❌ Dispatcher quartet sans avoir lu canoniques EN ENTIER avant (biais perception, cf [[feedback_lire_canoniques_avant_audit]])

## SOURCES

- [[methode-analyser-repo]] section ORDRE CANONIQUE A→B→C→D→E
- [[anti-reentrance-sub-agents-pattern-escalade]]
- Session neo_ia 25 mai 2026 (commit `7b86ea5`)

## WIKILINKS

- [[methode-analyser-repo]]
- [[comment-creer-agent]]
- [[workflow-claude-code-optimal]]
- [[anti-reentrance-sub-agents-pattern-escalade]]
- [[feedback_audit_claims_after_brief]]
- [[feedback_fix_vagues_paralleles]]
- [[feedback_audit_repo_method]]
