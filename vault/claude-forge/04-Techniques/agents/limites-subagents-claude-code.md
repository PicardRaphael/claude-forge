---
titre: Limites techniques des sub-agents Claude Code
resume: 200K ctx, 32K output, maxTurns cassé, jamais en parallèle — bugs confirmés GitHub
domaine: claude-code, agents, architecture
derniere-maj: 2026-05-08
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/tech"
  - "#statut/actif"
aliases:
  - subagent limits
  - agent crash
  - tool result missing
  - agent overload
  - découpage agents
---

# Limites techniques des sub-agents Claude Code

## Limites concrètes (confirmées mai 2026)

| Paramètre | Valeur | Bug GitHub |
|-----------|--------|------------|
| Contexte subagent | **200K tokens max** (même sur Opus 1M) | #32603 |
| Output subagent | **32K tokens hardcodé** (ignore `CLAUDE_CODE_MAX_OUTPUT_TOKENS`) | #25569 |
| `maxTurns` | **Non enforcé** — un agent à 10 turns en a fait 72 | #41143 |
| `Task()` timeout | **Aucun** — peut bloquer indéfiniment (30+ min observé) | #49150 |
| Bash timeout | **120s** par défaut, SIGTERM tue le parent aussi | #45717 |
| Agents orphelins | ~400MB RAM chacun, 20+ s'accumulent par heure | #19045 |

## Bugs critiques "Tool result missing"

- **#43866** — Skill tool retourne l'erreur, agent bloqué, pas de retry
- **#46767** — Régression Windows v2.1.101 : résultats silencieusement perdus sur TOUS les outils
- **#39830** — **Agents en parallèle dans un seul turn perdent les résultats** (bug d'agrégation)
- **#44068** — Feature request auto-retry (pas encore implémenté)

## Règles d'or

### 1. JAMAIS d'agents en parallèle dans un seul turn
Les résultats sont perdus (#39830). Séquencer : Agent 1 → consolider → Agent 2.

### 2. Max 6-8 opérations lourdes par agent
Search, read gros fichier, grep large = opération lourde. Au-delà, le contexte sature.

### 3. Max 5 fichiers par agent
Plus = risque de dépasser les 200K tokens.

### 4. Ne pas se fier à `maxTurns`
Le runtime ne l'enforce pas (#41143). Ajouter "STOP après N opérations" explicitement dans le prompt.

### 5. Prompt précis, pas de scope flou
"Analyse tout le projet" = crash. "Analyse packages/neochat/tools/ — 3 fichiers listés" = OK.

### 6. Limiter la taille de réponse demandée
"Sous 200 mots", "liste uniquement" — sinon l'output tape le plafond 32K.

## Approche Boris Cherny (confirmée)

Boris ne fait PAS de sub-agents profonds. Il parallélise avec des **worktrees séparés** (sessions indépendantes), pas en empilant des agents dans un même contexte. Chaque session reste légère.

Son pattern : 5 worktrees parallèles, chacun avec sa propre session Claude Code. Plan Mode 80% du temps, code 20%.

## Comment bloquer le nesting

Pas de variable d'env ni de setting pour bloquer le nesting. La solution : **ne jamais donner `Agent` ou `Task` dans les `tools:` des agents**. Seule la session principale (qui a tous les outils par défaut) peut orchestrer.

Vérification : `grep "^tools:" .claude/agents/*.md` — si aucun agent n'a Agent/Task, le nesting est impossible.

Sur les 3 repos Neoteem (neo_ia, ia_back, neoteem-brain) : **aucun agent n'a Agent/Task** → nesting déjà bloqué.

Standard pour tout nouveau repo :
- **Ne JAMAIS mettre Agent ou Task dans les tools d'un agent**
- Si un agent a besoin qu'un autre tourne → retourner le résultat à la session principale qui dispatch

## Comment découper une tâche

**Par module :**
```
Agent 1 : packages/neochat/ (3 fichiers)
Agent 2 : packages/shared_utils/ (2 fichiers)
→ session consolide
```

**Par phase :**
```
Agent 1 : exploration read-only (Grep, Read, Glob)
→ session consolide les findings
Agent 2 : implémentation (Write, Edit)
```

**Par type d'opération :**
```
Agent 1 : 5 web searches thème A
Agent 2 : 5 web searches thème B
→ session synthétise (pas en parallèle !)
```

## Implémentation standard Neoteem

- **Rule `agent-limits.md`** sur chaque repo (filet de sécurité permanent)
- **Section "Découpage" dans l'agent architect** (planification intelligente)
- Les deux ensemble = double couverture

## Liens

- [[erreur-marker-ttl-blocage-agents]] — autre source de blocage agents (corrigé)
- [[decoupe-agents-anti-crash]] — note technique découpage
