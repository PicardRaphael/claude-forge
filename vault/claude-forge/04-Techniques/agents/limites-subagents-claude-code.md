---
titre: "Limites techniques des sub-agents Claude Code"
resume: "200K ctx, 32K output, maxTurns casse, jamais en parallele dans un seul turn — bugs confirmes GitHub"
aliases:
  - subagent limits
  - agent crash
  - tool result missing
  - agent overload
domaine: claude-code
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://github.com/anthropics/claude-code/issues"
  - "https://code.claude.com/docs/en/sub-agents"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
---

## Description

Documentation des limites techniques hard des sub-agents Claude Code, avec bugs GitHub confirmes et workarounds. Reference pour tout projet utilisant des agents.

## Quand utiliser

Avant de concevoir une architecture multi-agents, ou pour diagnostiquer un crash/blocage d'agent.

## Limites concretes (confirmees mai 2026)

| Parametre | Valeur | Bug GitHub |
|-----------|--------|------------|
| Contexte subagent | **200K tokens max** (meme sur Opus 1M) | [#32603](https://github.com/anthropics/claude-code/issues/32603) |
| Output subagent | **32K tokens hardcode** (ignore `CLAUDE_CODE_MAX_OUTPUT_TOKENS`) | [#25569](https://github.com/anthropics/claude-code/issues/25569) |
| `maxTurns` | **Non enforce** — un agent a 10 turns en a fait 72 (verbatim issue) | [#41143](https://github.com/anthropics/claude-code/issues/41143) |
| `Task()` timeout | **Aucun** — peut bloquer (30+ min observe, verbatim issue) | [#49150](https://github.com/anthropics/claude-code/issues/49150) |
| Bash timeout | **120s** par defaut, SIGTERM tue le parent aussi | [#45717](https://github.com/anthropics/claude-code/issues/45717) |
| Agents orphelins | Issue confirmee (chiffres precis RAM/heure a re-verifier dans body issue) | [#19045](https://github.com/anthropics/claude-code/issues/19045) |

## Bugs critiques "Tool result missing"

- **[#43866](https://github.com/anthropics/claude-code/issues/43866)** — Skill tool retourne l'erreur, agent bloque, pas de retry
- **[#46767](https://github.com/anthropics/claude-code/issues/46767)** — Regression Windows v2.1.101 : resultats silencieusement perdus sur TOUS les outils
- **[#39830](https://github.com/anthropics/claude-code/issues/39830)** — **Agents en parallele dans un seul turn perdent les resultats** (bug d'agregation)
- **[#44068](https://github.com/anthropics/claude-code/issues/44068)** — Feature request auto-retry (issue closed, voir conclusion pour statut current)

## Regles d'or

### 1. JAMAIS d'agents en parallele dans un seul turn
Les resultats sont perdus (#39830). Sequencer : Agent 1 → consolider → Agent 2.

### 2. Scoping precis, pas de seuil numerique magique
Voir [[decoupe-agents-anti-crash]]. Les seuils "max 6-8 ops" et "max 5 fichiers" qui circulaient dans forge **ne sont PAS canoniques Anthropic** (audit 23 mai 2026). Ce qui compte : un prompt precis, un scope clair, un format de sortie attendu.

### 3. Ne pas se fier a `maxTurns`
Le runtime ne l'enforce pas (#41143). Ajouter "STOP apres N operations" explicitement dans le prompt si on veut un arret deterministe.

### 4. Prompt precis, pas de scope flou
"Analyse tout le projet" = crash quasi garanti. "Analyse packages/neochat/tools/ — 3 fichiers listes" = OK.

### 5. Limiter la taille de reponse demandee
"Sous 200 mots", "liste uniquement" — sinon l'output tape le plafond 32K.

## Approche Boris Cherny

Boris parallelise avec des **worktrees separes** (sessions independantes), pas en empilant des sub-agents profonds dans un meme contexte. Pattern documente sur [howborisusesclaudecode.com](https://howborisusesclaudecode.com/) et [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny) : 5 worktrees paralleles + **Plan Mode 80% du temps** (verbatim multi-sources), code 20%.

Note : Boris **recommande** les subagents pour l'investigation (cf docs Anthropic sub-agents) — il les utilise mais sans nesting profond.

## Comment bloquer le nesting

Pas de variable d'env ni de setting pour bloquer le nesting. La solution : **ne jamais donner `Agent` ou `Task` dans les `tools:` des agents**. Seule la session principale (qui a tous les outils par defaut) peut orchestrer.

Verification : `grep "^tools:" .claude/agents/*.md` — si aucun agent n'a Agent/Task, le nesting est impossible.

Sur les 3 repos Neoteem (neo_ia, ia_back, neoteem-brain) : **aucun agent n'a Agent/Task** → nesting deja bloque.

Standard pour tout nouveau repo :
- **Ne JAMAIS mettre Agent ou Task dans les tools d'un agent**
- Si un agent a besoin qu'un autre tourne → retourner le resultat a la session principale qui dispatch

## Comment decouper une tache

Voir [[decoupe-agents-anti-crash]] pour les principes qualitatifs detailles (par module, par phase, par type d'operation).

## Implementation standard Neoteem

- **Rule `agent-limits.md`** sur chaque repo (filet de securite permanent)
- **Section "Decoupage" dans l'agent architect** (planification intelligente)
- Les deux ensemble = double couverture

## Liens

- [[MOC-Techniques]]
- [[raisonnement-22mai-doctrine-vs-enforcement]]
- [[decoupe-agents-anti-crash]] — Principes qualitatifs decoupage
- [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]] — audit source
