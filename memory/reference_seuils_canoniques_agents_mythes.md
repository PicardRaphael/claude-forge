---
name: seuils-canoniques-agents-mythes-2026-05-22
description: "5 seuils \"canoniques\" agents que je citais étaient des mythes confirmés par recherche web 2026-05-22 — ne plus les utiliser sans disclaimer"
metadata: 
  node_type: memory
  type: reference
  originSessionId: d16cea52-3288-48fe-b266-693dd7948ca2
---

Recherche web 2026-05-22 a confirmé que 4 sur 5 seuils "canoniques" pour les agents Claude Code que je citais sont des mythes ou extrapolations.

## Mythes confirmés (à NE PLUS utiliser)

| Seuil | Statut | Réalité |
|---|---|---|
| **"Max 6-8 ops/agent"** | ❌ Mythe | Aucune source. Confusion avec "1/2-4/10+ subagents" Anthropic |
| **"Agent < 200L"** | ❌ Mythe | 200L = pour CLAUDE.md, pas agents. Aucune source pour agents |
| **"Agent < 1500 mots"** | ⚠️ Single source | dbreunig.com seul : "1500-6000 **tokens**" (pas mots) |
| **"Max 8 tools/agent"** | ❌ Mythe | Anthropic refuse explicitement un chiffre — "scope au minimum nécessaire" |
| **"Max N skills frontmatter"** | ❌ Pas de règle | Budget contexte implicite, pas de seuil documenté |

## Seuils canoniques VRAIMENT confirmés

| Seuil | Sources convergentes |
|---|---|
| **CLAUDE.md < 200L** | ✅ Anthropic docs + HumanLayer + autres |
| **SKILL.md body < 500L** | ✅ Anthropic docs |

## Sources recherche web (2026-05-22)

- Anthropic Best practices Claude Code
- Anthropic Engineering — Effective harnesses for long-running agents
- HumanLayer — Writing a good CLAUDE.md
- dbreunig.com — How Claude Code Builds a System Prompt
- Anthropic — Building agents with Claude Agent SDK
- Claude API — Skill authoring best practices
- Claude Code Docs — sub-agents

**Why:** J'ai cité ces seuils pendant l'audit ia_back comme s'ils étaient canoniques. Raphael m'a challengé. Recherche web a montré qu'ils ne sont pas validés par 3+ sources. Conséquence : audits basés dessus = biais.

**How to apply:**
- AVANT de citer un seuil numérique pour un agent, vérifier qu'il est dans la liste "VRAIMENT confirmés" ci-dessus
- Sinon : appliquer la règle "scope au minimum nécessaire" (Anthropic verbatim) sans chiffre précis
- Si tu observes empiriquement qu'un agent paraît saturé → split par jugement, pas par règle numérique

Related : [[feedback_lire_canoniques_avant_audit]], [[feedback_always_best_techniques]].
