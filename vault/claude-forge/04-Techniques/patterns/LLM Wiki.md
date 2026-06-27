---
titre: "LLM Wiki — Pattern Karpathy"
resume: "Pattern Karpathy avril 2026 : un LLM compile et maintient un wiki markdown structuré plutôt que faire du RAG sur des sources brutes"
aliases:
  - "llm wiki"
  - "karpathy wiki"
  - "LLM knowledge base"
  - "wiki pattern karpathy"
  - "plain text knowledge management"
domaine: technique
type: technique
derniere-maj: 2026-06-27
auteur: claude
sources:
  - "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
  - "https://x.com/karpathy/status/1937902205765607626"
tags:
  - "#type/technique"
  - "#domaine/rag"
---

## Description

Pattern d'[[Andrej Karpathy]] publié sur X le 3 avril 2026 puis formalisé en gist GitHub le 4 avril 2026 (5K+ stars, 4K+ forks). Utiliser un LLM pour **compiler et maintenir** un wiki markdown structuré plutôt que faire du RAG à chaque requête.

> ✅ Verbatim Karpathy (gist) : *"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."*

## Quand utiliser

Alternative au RAG pour les bases de connaissances personnelles à moyenne échelle. Pour les corpus très larges (millions de mots), RAG reste pertinent.

## Specs verbatim Karpathy (gist)

- Échelle indicative : "~100 sources, ~hundreds of pages" (verbatim — pas de chiffre "400K mots" dans le gist direct)
- Plain text markdown — pas de base vectorielle, pas de chunking, pas d'embeddings
- 3 layers : `raw/` (sources immuables), `wiki/` (LLM-owned), schema/conventions
- Maintenance : LLM organise/cross-référence/update, humain source/explore/valide

> Verbatim Karpathy : *"The LLM makes edits based on our conversation."* + *"LLMs handle cross-referencing and bookkeeping; humans handle sourcing, exploration, and asking the right questions."*

## Pas de chiffre d'efficience attesté

Le chiffre "70x plus efficient que RAG" est cité par MindStudio (blog tiers) mais **n'apparaît pas dans le gist Karpathy ni ses tweets**. À traiter comme angle éditorial d'un blog, pas comme claim Karpathy.

## Lien avec forge-brain

> **STATUT 2026-06-27** : forge-brain s'est **émancipé** de ce pattern ([[decision-vault-agent-first]]). Karpathy fut l'échafaudage de départ ; aujourd'hui forge-brain est un **cerveau d'agent** piloté via MCP — `raw/` supprimé (sources distillées directement en wiki/), `index.md`/`log.md`/MOCs = couche humaine optionnelle. Le pattern Karpathy reste pertinent en **référence générique** pour d'autres vaults. Implémentation et état réel : [[pattern-vault-llm-karpathy]] (voir son bandeau STATUT) + [[decision-vault-agent-first]].

## Liens

- [[Andrej Karpathy]]
- [[pattern-vault-llm-karpathy]]
- [[decision-vault-agent-first]]
- [[Context Engineering]]
- [[MOC-Techniques]]
