---
titre: "Dreaming — Review cross-session automatique des patterns"
resume: "Feature Anthropic Managed Agents : review automatique des sessions passees pour extraire patterns et auto-ameliorer les agents, Netflix 97% moins d'erreurs"
aliases:
  - dreaming
  - dreaming anthropic
  - cross-session memory review
  - auto-improvement agents
  - memory dreaming claude
  - review automatique sessions
type: knowledge
derniere-maj: 2026-05-13
auteur: claude
sources:
  - "https://claude.com/blog/claude-managed-agents-memory"
  - "https://www.edtechinnovationhub.com/news/anthropic-brings-persistent-memory-to-claude-managed-agents-in-public-beta"
  - "https://9to5mac.com/2026/05/07/anthropic-updates-claude-managed-agents-with-three-new-features/"
tags:
  - "#type/knowledge"
  - "#domaine/tech"
  - "#technique/agents"
  - "#outil/claude-code"
---

## Concept

**Dreaming** = processus planifie qui review les sessions passees d'un agent et extrait les patterns pour ameliorer la memoire automatiquement. L'agent "reve" entre les sessions pour consolider ses apprentissages.

Annonce : Anthropic, avril-mai 2026, dans le cadre de [[Claude Managed Agents]] memory (beta publique).

## Comment ca marche

1. **Review planifiee** — un processus examine les sessions passees de l'agent
2. **Extraction de patterns** — identifie les corrections humaines recurrentes, les erreurs repetees, les approches qui fonctionnent
3. **Curation memoire** — met a jour la memoire de l'agent avec les insights extraits
4. **Controle humain** — 2 modes : auto-update OU review humaine avant application

## Cas d'usage en production

### Netflix
- Memoire pour persister le **contexte cross-session** : insights decouverts en plusieurs tours + corrections humaines mid-conversation
- Les corrections d'un reviewer humain sont persistees pour que l'agent ne refasse pas la meme erreur

### Rakuten
- Agents long-running avec memoire pour eviter de repeter les erreurs passees
- **97% moins d'erreurs first-pass** dans un perimetre workspace-scoped et observable

## Equivalent forge / Claude Code local

Le Dreaming est une feature Managed Agents (cloud). Pour Claude Code local, l'equivalent est :

| Dreaming feature | Equivalent local |
|-----------------|-----------------|
| Review cross-session | Skill `/done` (metacognition fin de session) |
| Extraction patterns | `learn-from-mistakes` rule + sections Apprentissage skills |
| Curation memoire | `memory: project` dans `.claude/agent-memory/` (commit + git) |
| Controle humain | Review du diff `.claude/agent-memory/` avant commit |
| Planification | `/schedule` + `/dream` skill (a creer) |

### Pattern local recommande

```
1. Fin de session → /done extrait les apprentissages
2. Agent ecrit dans .claude/agent-memory/<agent>/MEMORY.md
3. git commit des changements memoire
4. Prochain dev beneficie via git pull
5. Periodiquement : review manuelle des MEMORY.md pour elaguer
```

## Technique Netflix — Persister les corrections humaines

Quand un humain corrige un agent mid-conversation :
1. L'agent detecte la correction
2. Il l'ecrit dans sa memoire avec `**Why:**` et `**How to apply:**`
3. La correction est commitee → tous les devs en beneficient
4. L'agent ne refait plus la meme erreur

**Implementation** : ajouter dans le body de chaque agent :
```
Quand l'utilisateur te corrige, ecris la correction dans ta memoire agent
(.claude/agent-memory/<ton-nom>/MEMORY.md) avec le format :
- Erreur : <ce que tu as fait>
- Correction : <ce que l'utilisateur a demande>
- Why : <pourquoi c'etait faux>
```

## Liens

- [[pattern-figma-mcp-claude-code]] — autre technique decouverte session lojii
- [[lojii]] — premier projet avec memoire partagee agent-memory
- [[reference_dreaming_pattern]] — memoire forge existante sur le sujet
