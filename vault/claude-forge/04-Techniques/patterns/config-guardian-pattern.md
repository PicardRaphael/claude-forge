---
titre: "Config Guardian — Audit multi-repo"
resume: "Pattern pour auditer la config Claude Code de plusieurs repos depuis forge — 5 checks, corrections par stack, mémoire compounding"
aliases:
  - "config guardian"
  - "audit multi-repo"
  - "drift detection"
  - "audit config claude code"
  - "config guardian pattern"
domaine: claude-code
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
  - "[[workflow-claude-code-optimal]]"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/neoteem"
---

## Description

Skill `/config-guardian` dans forge qui scanne les repos projet (ia_back, neo_ia, neoteem-brain) et produit un rapport d'écarts par rapport à une baseline de règles Claude Code.

## Problème

Quand on a 3+ repos avec chacun leur `.claude/` (agents, hooks, rules, settings), la config dérive. Même bug diagnostiqué 3 fois dans 3 repos différents. 8 sessions perdues sur des permissions git, hooks qui boucle, MCP manquant.

## Solution

Skill `/config-guardian` dans forge qui scanne les 3 repos et produit un rapport d'écarts.

## 5 checks baseline

| # | Check | Quoi vérifier |
|---|-------|---------------|
| 1 | Permissions git | commit/push allow, global deny vide |
| 2 | Hooks cohérence stack | Tous les hooks dans le même langage que le projet. Pas d'orphelins/fantômes |
| 3 | Rules obligatoires | check-before-create, learn-from-mistakes, quality-gates |
| 4 | MCP tools agents | Chaque agent déclare les MCP dont il a besoin selon son rôle |
| 5 | Mémoire compounding | memory:project agents, Gotchas CLAUDE.md, section Mémoire, feedback rules |

## Principes

- Chaque repo a sa propre architecture — ne pas copier les MCP d'un repo à l'autre
- La baseline spécifique par repo est dans `references/baseline-rules.md` de la skill
- **CLAUDE.md** ~100 lignes (Boris)

## Pattern Boris (mémoire compounding)

1. CLAUDE.md = instructions de survie, pas de stockage
2. Erreurs → Auto Memory (`.claude/agent-memory/`)
3. Relire feedback rules en début de tâche
4. Compounding : 6 mois = centaines de rules, erreurs chutent

## Pattern Karpathy (LLM Wiki)

> ✅ Verbatim Karpathy (gist 4 avril 2026) : *"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."*

- Plain markdown > vector DB
- Le LLM compile le knowledge, pas juste le stocke

## Session référence

4 mai 2026 — audit complet ia_back + neo_ia + neoteem-brain :
- 14 agents ia_back sans MCP → corrigé (context7 + postgres)
- Hook node résidu neo_ia → supprimé
- daily-sync.ps1 orphelin neoteem-brain → supprimé
- Sections Mémoire ajoutées dans 2 CLAUDE.md
- Score final : 15/15

## Quand utiliser

Après chaque session de modification d'agents/hooks/rules sur un repo, ou en audit périodique (hebdomadaire). Détecte la dérive de config avant qu'elle ne cause des problèmes.

## Liens

- [[LLM Wiki]] — pattern Karpathy d'origine
- [[MOC-Techniques]]
- [[workflow-claude-code-optimal]]
