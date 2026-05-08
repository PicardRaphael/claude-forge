---
titre: "Config Guardian — Audit multi-repo"
resume: "Pattern pour auditer la config Claude Code de plusieurs repos depuis forge — 5 checks, corrections par stack, mémoire compounding"
aliases:
  - "config guardian"
  - "audit multi-repo"
  - "drift detection"
domaine: claude-code
type: technique
derniere-maj: 2026-05-04
auteur: claude
sources:
  - "[[best-practices-claude-code-leaders]]"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/neoteem"
---

## Description

Skill `/config-guardian` dans forge qui scanne les repos projet (ia_back, neo_ia, neoteem-brain) et produit un rapport d'ecarts par rapport a une baseline de regles Claude Code.

## Probleme

Quand on a 3+ repos avec chacun leur `.claude/` (agents, hooks, rules, settings), la config derive. Meme bug diagnostique 3 fois dans 3 repos differents. 8 sessions perdues sur des permissions git, hooks qui boucle, MCP manquant.

## Solution

Skill `/config-guardian` dans forge qui scanne les 3 repos et produit un rapport d'ecarts.

## 5 checks baseline

| # | Check | Quoi verifier |
|---|-------|---------------|
| 1 | Permissions git | commit/push allow, global deny vide |
| 2 | Hooks coherence stack | Tous les hooks dans le meme langage que le projet. Pas d'orphelins/fantomes |
| 3 | Rules obligatoires | check-before-create, learn-from-mistakes, quality-gates |
| 4 | MCP tools agents | Chaque agent declare les MCP dont il a besoin selon son role |
| 5 | Memoire compounding | memory:project agents, Gotchas CLAUDE.md, section Memoire, feedback rules |

## Principes

- Chaque repo a sa propre architecture — ne pas copier les MCP d'un repo a l'autre
- La baseline specifique par repo est dans `references/baseline-rules.md` de la skill
- **CLAUDE.md** ~100 lignes (Boris)

## Pattern Boris (memoire compounding)

1. CLAUDE.md = instructions de survie, pas de stockage
2. Erreurs → Auto Memory (`.claude/agent-memory/`)
3. Relire feedback rules en debut de tache
4. Compounding : 6 mois = centaines de rules, erreurs chutent

## Pattern Karpathy (LLM Wiki)

- "Obsidian is the IDE, the LLM is the programmer, the wiki is the codebase"
- Plain markdown > vector DB
- Le LLM compile le knowledge, pas juste le stocke

## Session reference

4 mai 2026 — audit complet ia_back + neo_ia + neoteem-brain :
- 14 agents ia_back sans MCP → corrige (context7 + postgres)
- Hook node residu neo_ia → supprime
- daily-sync.ps1 orphelin neoteem-brain → supprime
- Sections Memoire ajoutees dans 2 CLAUDE.md
- Score final : 15/15

## Quand utiliser

Apres chaque session de modification d'agents/hooks/rules sur un repo, ou en audit periodique (hebdomadaire). Detecte la derive de config avant qu'elle ne cause des problemes.

## Liens

- [[MOC-Techniques]]
- [[CC v2.1.126]]
- [[setup-project-complet]]
- [[kit-rules-standard]]
- [[pattern-agentic-engineering]]
