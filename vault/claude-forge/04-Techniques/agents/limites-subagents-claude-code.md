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
derniere-maj: 2026-06-16
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

---

## AJOUT 16 juin 2026 — Le nesting n'est PLUS bloqué (v2.1.172) + méthode d'audit ci-dessus CORRIGÉE

> Source primaire : [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) § « Spawn nested subagents » + changelog v2.1.172 (10 juin 2026). Pattern + arbitrage complet : [[anti-reentrance-sub-agents-pattern-escalade]] § AJOUT 16 juin.

### Ce qui change

CC v2.1.172, verbatim : *« Sub-agents can now spawn their own sub-agents (up to 5 levels deep) »*. La section « Comment bloquer le nesting » ci-dessus partait de la prémisse « impossible » — **périmée**.

### ⚠️ La méthode d'audit `grep "^tools:"` ci-dessus est TROMPEUSE

Le claim « si aucun agent n'a Agent/Task → nesting impossible » et la conclusion « 3 repos Neoteem → nesting déjà bloqué » sont **faux**. Raison (doc primaire) :
> (frontmatter) « `tools` — Inherits all tools if omitted. »
> « Subagents inherit the internal tools and MCP tools available in the main conversation by default. »

Donc un agent qui **omet entièrement la ligne `tools:`** hérite de **TOUS** les outils, **`Agent` compris**, et **nest par défaut**. Le `grep "^tools:"` trouve les agents qui ONT une ligne tools ; il **rate exactement les agents sans ligne tools** — qui sont précisément ceux qui nestent.

### Méthode d'audit CORRIGÉE

Le nesting d'un agent est bloqué SEULEMENT si **l'une** de ces conditions tient :
1. ligne `tools:` **explicite SANS** `Agent` (ni `Task`), OU
2. `disallowedTools: Agent` (depuis v2.1.178, les specs MCP server-level `mcp__*` dans `disallowedTools` ne sont plus silencieusement ignorées), OU
3. `permissions.deny: ["Agent"]` (ou `Agent(type)` pour des types précis), OU
4. background au niveau 5 (plafond plateforme, automatique).

→ **Audit réel = repérer les agents qui OMETTENT la ligne `tools:`** (= héritent `Agent`), pas grep `^tools:`. Gouvernance globale du modèle des spawns : `permissions.deny: ["Agent(model:opus)"]` (syntaxe `Tool(param:value)` v2.1.178).

### À VÉRIFIER sur les repos Neoteem (fix concret, pas entretien doctrinal)

L'affirmation « 3 repos déjà bloqués » est à **re-auditer** avec la bonne méthode : grep les fichiers `.claude/agents/*.md` **sans** ligne `tools:` sur **ia_back** et **neo_ia** (et neoteem-brain). Chaque agent sans ligne `tools:` nest désormais par défaut. C'est le seul endroit où ce fil devient un fix réel (la plainte vient des collègues = ces repos). **forge vérifié sain** (16 juin) : 5 agents, tous avec ligne `tools:` explicite, seul `repo-inspector` a `Agent` (volontaire). Propagation à tracer via `.claude/rules/cross-repo-propagation.md`.

### `maxTurns` / profondeur ne sont pas des garde-fous fiables

Cohérent avec la table ci-dessus : `maxTurns` non enforcé (#41143), pas de timeout `Agent()` (#49150). Le seul mur dur est le **plafond background = 5 niveaux** (fixe, non configurable). Pour un arrêt déterministe → « STOP après N ops » dans le prompt + `tools:` explicite sans `Agent`.

`derniere-maj` → 2026-06-16.


---

## AJOUT 27 juillet 2026 — nesting : depth 3 par défaut + caps quantitatifs (v2.1.217-219)

Après l'amende v2.1.172 (« up to 5 levels deep ») ci-dessus, la fenêtre 21-24 juillet a rebattu les valeurs par défaut ([[CC juillet 2026 - Opus 5 + v2.1.212-220]]) :

- **v2.1.217 (21 juil.)** : nesting DÉSACTIVÉ par défaut + cap **20 subagents concurrents** (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`).
- **v2.1.219 (24 juil.)** : nesting réactivé **jusqu'à depth 3 par défaut** (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` pour l'ancien comportement) + forwarding stream-json des subagents depth 2+.
- Caps par session depuis v2.1.212 : **200 spawns** + 200 WebSearch.
- Le paramètre `mode` du Task tool est **déprécié/ignoré** (héritage du permission mode parent).

Les valeurs « foreground toute profondeur / background plafond 5 » de l'amende du 16 juin décrivent l'ère v2.1.172-216 — depuis v2.1.219, raisonner en « depth 3 par défaut, configurable ». La recommandation design (escalade session principale par défaut) reste inchangée, cf [[anti-reentrance-sub-agents-pattern-escalade]].
