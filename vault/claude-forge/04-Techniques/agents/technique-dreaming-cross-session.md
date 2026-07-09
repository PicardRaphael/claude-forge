---
titre: "Dreaming — Review cross-session automatique des patterns"
resume: "Feature Anthropic Managed Agents (Research Preview, beta header dreaming-2026-04-21) : review automatique des sessions passees pour curer la memoire agent et faire emerger des insights"
aliases:
  - dreaming
  - dreaming anthropic
  - cross-session memory review
  - auto-improvement agents
  - memory dreaming claude
  - review automatique sessions
type: knowledge
derniere-maj: 2026-07-09
auteur: claude
sources:
  - "https://platform.claude.com/docs/en/managed-agents/dreams"
  - "https://www.edtechinnovationhub.com/news/anthropic-brings-persistent-memory-to-claude-managed-agents-in-public-beta"
  - "https://9to5mac.com/2026/05/07/anthropic-updates-claude-managed-agents-with-three-new-features/"
tags:
  - "#type/knowledge"
  - "#domaine/tech"
  - "#domaine/agents"
  - "#domaine/claude-code"
---

## Concept

**Dreaming** = job asynchrone qui lit une memory store existante + 1 a 100 sessions passees, produit une nouvelle memory store reorganisee (duplicates merges, entrees obsoletes remplacees, nouveaux insights surfaces).

> Verbatim docs Anthropic : "Dreams let Claude reflect on past sessions to curate an agent's memory and surface new insights."

**Statut** : Research Preview. Beta header requis : `managed-agents-2026-04-01,dreaming-2026-04-21`. Acces sur demande via [le formulaire Managed Agents](https://claude.com/form/claude-managed-agents).

## Comment ca marche

1. **Input** : une pre-existing memory store + 1-100 session transcripts
2. **Pipeline asynchrone** : claude-opus-4-7 ou claude-sonnet-4-6 traite (lifecycle : pending → running → completed/failed/canceled)
3. **Output** : une NOUVELLE memory store separee (l'input n'est jamais modifie)
4. **Review humain** : la sortie est inspectable via la Memory Stores API ou la Console, puis a attacher aux futures sessions ou a supprimer

## Cas d'usage en production

### Netflix
- Memoire pour persister le **contexte cross-session** : insights decouverts en plusieurs tours + corrections humaines mid-conversation
- Les corrections d'un reviewer humain sont persistees pour que l'agent ne refasse pas la meme erreur

### Rakuten
- Agents long-running avec memoire pour eviter de repeter les erreurs passees
- **97% reduction in initial critical errors** (verbatim Anthropic) dans un perimetre workspace-scoped et observable

## Equivalent forge / Claude Code local

Le Dreaming est une feature Managed Agents (cloud, Research Preview). Pour Claude Code local, l'equivalent qualitatif est :

| Dreaming feature | Equivalent local |
|-----------------|-----------------|
| Review cross-session | Skill `/done` (metacognition fin de session) |
| Extraction patterns | `learn-from-mistakes` rule + sections Apprentissage skills |
| Curation memoire | Auto memory dans `~/.claude/projects/<project>/memory/` (machine-local) |
| Controle humain | Review du diff vault avant commit |
| Planification | `/schedule` + `/dream` skill (a creer) |

### Pattern local recommande

```
1. Fin de session → /done extrait les apprentissages
2. Claude ecrit dans ~/.claude/projects/<project>/memory/MEMORY.md (machine-local)
3. Memoire vault commitee separement (git) si insights a partager equipe
4. Prochain dev beneficie via git pull
5. Periodiquement : review manuelle des memoires pour elaguer
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
avec le format :
- Erreur : <ce que tu as fait>
- Correction : <ce que l'utilisateur a demande>
- Why : <pourquoi c'etait faux>
```

## Limites Research Preview

| Limit | Value |
|---|---|
| Sessions par dream | 100 |
| `instructions` length | 4 096 caracteres |
| Models supportes | `claude-opus-4-7`, `claude-sonnet-4-6` |

Couts : tokens API standard du modele selectionne, scale lineaire avec le nombre/longueur des sessions input.

## Liens

- [[pattern-figma-mcp-claude-code]] — autre technique decouverte session lojii
- [[lojii]] — premier projet avec memoire partagee
- [[technique-shared-agent-memory]] — scopes memoire CLAUDE.md + auto memory

---

## AJOUT 16 juin 2026 — Corrections factuelles (source primaire platform.claude.com)

> Vérifié sur [platform.claude.com/docs/en/managed-agents/dreams](https://platform.claude.com/docs/en/managed-agents/dreams.md) + [.../memory](https://platform.claude.com/docs/en/managed-agents/memory.md) (16 juin). Corrige deux claims du corps ci-dessus.

### Modèles supportés — TROIS, pas deux

Le corps liste `claude-opus-4-7` + `claude-sonnet-4-6`. Doc primaire actuelle = **3 modèles** : **`claude-opus-4-8`, `claude-opus-4-7`, `claude-sonnet-4-6`**. (`opus-4-8` ajouté depuis la rédaction du 23 mai.)

### Le « 97% » est À CONFIRMER — pas un chiffre Rakuten vérifié

Le corps écrit « Rakuten — **97% reduction in initial critical errors** (verbatim Anthropic) ». **Non confirmé en source primaire.** La page client primaire [claude.com/customers/rakuten](https://claude.com/customers/rakuten) donne : **79% reduction in time to market**, 7 h de run autonome, 99.9% accuracy, 24 sessions parallèles. Le « 97% » apparaît dans des contextes secondaires (parfois rattaché à Netflix, non confirmé). **Traiter le 97% comme non vérifié** (cf [[llm-deep-research-version-numbers-hallucinated]] + [[verification-sources-canoniques]]) ; citer 79% TTM comme chiffre Rakuten solide. La présentation orale Code with Claude a pu énoncer un chiffre non repris dans la doc écrite → ne pas le relayer comme « verbatim Anthropic » certain.

### Caps Research Preview (complément primaire)

Sessions/dream : 100 · `instructions` ≤ 4096 chars · lifecycle pending→running→completed/failed/canceled · l'input n'est jamais modifié (output = nouvelle store).

`derniere-maj` → 2026-06-16.
