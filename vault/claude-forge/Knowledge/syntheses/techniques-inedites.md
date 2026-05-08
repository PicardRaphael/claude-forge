---
titre: "Techniques inédites — Croisements RAG × Agents × Automation"
resume: "Combinaisons innovantes que personne ne fait encore, issues du croisement de 10 rapports de recherche RAG + Agents IA 2026"
aliases:
  - techniques inédites
  - innovations RAG agents
  - combinaisons IA
  - cross-domain innovations
  - techniques avant-garde
type: knowledge
derniere-maj: 2026-05-08
auteur: claude
sources: []
tags:
  - "#type/knowledge"
  - "#domaine/ia"
  - "#domaine/rag"
  - "#domaine/agents"
---

## Contexte

Croisement de 10 rapports de recherche (5 RAG + 5 Agents IA, mai 2026) pour identifier des **combinaisons que personne ne fait encore**. Chaque technique est construite sur des composants validés individuellement mais jamais assemblés ensemble.

---

## 1. Dreaming + Knowledge Vault Auto-Enrichment

**Composants existants** : Dreaming (Claude Managed Agents, mai 2026) + Obsidian vault + forge-brain CLI

**L'idée** : Un agent qui "rêve" entre les sessions — il analyse ses propres interactions passées, extrait les patterns récurrents, identifie les erreurs, et **enrichit automatiquement le vault** avec des notes atomiques. Le vault devient un cerveau qui grossit pendant que tu dors.

**Pourquoi c'est inédit** : Dreaming existe mais ne fait qu'optimiser la mémoire interne de l'agent. Personne ne le connecte à un vault structuré externe. La boucle feedback → knowledge → agent amélioré n'existe pas encore en production.

**Implémentation** : Claude Managed Agent + Routine nocturne + MCP obsidian-brain → analyse sessions → crée notes `Knowledge/syntheses/` + met à jour MOCs.

---

## 2. LATS Planning + Contextual Retrieval RAG

**Composants existants** : LATS (94.4% HumanEval, ICML 2024) + Contextual Retrieval (-67% échecs, Anthropic)

**L'idée** : Au lieu de faire une recherche RAG simple puis générer, utiliser **Monte Carlo Tree Search** pour explorer plusieurs chemins de retrieval en parallèle. Chaque branche de l'arbre fait son propre contextual retrieval, et le value function évalue quelle branche a le meilleur contexte. L'agent "planifie sa recherche" avant de chercher.

**Pourquoi c'est inédit** : LATS est utilisé pour le code et le raisonnement, jamais pour optimiser la retrieval elle-même. Contextual Retrieval est une technique d'indexation, jamais combinée avec une recherche arborescente.

**Impact estimé** : Sur des queries complexes multi-hop, pourrait réduire les échecs de retrieval de 67% (contextual seul) à possiblement 80-85%.

---

## 3. Browser Agent + RAG Pipeline Temps Réel

**Composants existants** : Stagehand (89% fiabilité) + defuddle (extraction web) + late chunking (Jina) + vector DB

**L'idée** : Un agent qui browse le web autonomement, extrait le contenu propre via defuddle, chunk avec late chunking, embed, et indexe dans un vector store — **en temps réel pendant qu'il cherche**. Le RAG se construit pendant la navigation, pas avant.

**Pourquoi c'est inédit** : Les RAG sont statiques (indexation offline). Les browser agents cherchent mais ne construisent pas de base vectorielle en live. La combinaison crée un **RAG dynamique qui s'auto-alimente**.

**Use case** : Veille concurrentielle automatique, analyse de marché temps réel, research agent qui accumule et structure sa connaissance au fil de la navigation.

---

## 4. GraphRAG + A2A Multi-Agent Spécialisés

**Composants existants** : GraphRAG (Microsoft, 3.4x accuracy multi-hop) + A2A protocol (Google, 150+ orgs)

**L'idée** : Au lieu d'un seul GraphRAG monolithique, décomposer le knowledge graph en **sous-graphes thématiques**, chacun géré par un agent spécialisé. Les agents communiquent via A2A pour résoudre des questions qui traversent plusieurs domaines. Un agent "routeur" dispatche les queries.

**Pourquoi c'est inédit** : GraphRAG est monolithique. A2A connecte des agents mais pas des sous-graphes de connaissances. La combinaison crée un **réseau distribué de spécialistes knowledge** qui scale mieux que le GraphRAG centralisé.

**Avantage** : LazyGraphRAG réduit le coût d'indexation à 0.1%, mais reste monolithique. Le pattern distribué permettrait de n'indexer que le sous-graphe pertinent, réduisant encore les coûts.

---

## 5. Episodic Memory + Eval-Driven Self-Improvement

**Composants existants** : Mem0 episodic memory + RAGAS evaluation + Reflexion pattern

**L'idée** : L'agent garde une mémoire épisodique de chaque tâche (query, actions, résultat, score RAGAS). Après N tâches, un meta-agent analyse les épisodes avec les scores les plus bas, identifie les patterns d'échec, et **modifie dynamiquement les prompts/tools/stratégies** de l'agent principal.

**Pourquoi c'est inédit** : Reflexion corrige au sein d'une tâche. Eval-driven development est fait par les humains. Personne ne ferme la boucle : eval automatique → diagnostic → modification agent → re-eval. C'est du **TDD continu pour agents**.

---

## 6. Dual-LLM Security + Contextual Embeddings

**Composants existants** : Pattern Dual-LLM (OWASP 2026) + Contextual Retrieval (Anthropic)

**L'idée** : Le LLM quarantainé (qui lit le contenu non-fiable) génère les contextual prefixes pour le RAG. Le LLM privilégié (qui a accès aux tools) ne voit que les résultats de retrieval déjà enrichis. Si le contenu non-fiable contient une injection, elle reste dans les prefixes — qui ne sont jamais exécutés, seulement utilisés pour le similarity search.

**Pourquoi c'est inédit** : Contextual Retrieval ne considère pas la sécurité. Le Dual-LLM ne considère pas le RAG. La combinaison crée un **RAG sécurisé par design** contre l'injection dans les documents source.

---

## 7. Adaptive RAG + Model Routing Agent

**Composants existants** : Adaptive RAG (classifieur T5-large, -30-50% coûts) + Model routing (40-60% savings)

**L'idée** : Un seul classifieur léger (T5-large, ~5-15ms) analyse chaque query et décide **simultanément** : (1) faut-il retriever ? (2) quel modèle utiliser ? (3) quelle stratégie de retrieval ? (4) faut-il un reranker ? Au lieu de 4 décisions indépendantes, une seule inférence détermine le pipeline optimal.

**Impact estimé** : Combiné caching + routing + adaptive = potentiellement **-80-90% coûts** vs pipeline fixe, avec qualité supérieure car la stratégie est adaptée par query.

---

## 8. Agent Teams + Hierarchical Chunking

**Composants existants** : Agent Teams (Claude Code) + H-RAG parent-child chunking

**L'idée** : Chaque agent de l'équipe travaille à un niveau différent de la hiérarchie documentaire. L'agent "scanner" utilise les child chunks (100-500 tokens) pour la précision. L'agent "analyste" utilise les parent chunks (500-2000 tokens) pour le contexte. L'agent "synthétiseur" croise les deux niveaux pour produire la réponse.

**Pourquoi c'est inédit** : Les Agent Teams travaillent sur le même index. H-RAG sépare parent/child mais un seul agent utilise les deux. La spécialisation par niveau de granularité est un pattern multi-agent jamais exploré.

---

## Matrice de priorité

| # | Technique | Faisabilité | Impact | Priorité |
|---|-----------|-------------|--------|----------|
| 1 | Dreaming + Vault | Haute (outils existants) | Très élevé | **P0** |
| 3 | Browser + RAG temps réel | Moyenne | Élevé | **P1** |
| 7 | Adaptive RAG + Model routing | Haute | Élevé (coûts) | **P1** |
| 5 | Episodic + Eval self-improvement | Moyenne | Très élevé | **P1** |
| 2 | LATS + Contextual Retrieval | Basse (R&D) | Très élevé | P2 |
| 4 | GraphRAG + A2A distribué | Basse (infra) | Élevé | P2 |
| 6 | Dual-LLM + Contextual security | Moyenne | Moyen | P2 |
| 8 | Agent Teams + Hierarchical chunks | Haute | Moyen | P2 |

## Liens

- [[RAG]] — Index RAG
- [[Agents IA]] — Index Agents
- [[rag-architecture]] — Patterns RAG avancés
- [[agents-architecture]] — Patterns agents
- [[agents-automation]] — Automation
