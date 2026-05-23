---
titre: "RAG Evaluation — Metriques et frameworks"
resume: "Métriques et frameworks pour évaluer un système RAG — RAGAS, DeepEval, LLM-as-judge, faithfulness, answer relevancy, context precision/recall."
aliases:
  - "rag evaluation"
  - "RAG evaluation"
  - "evaluation RAG"
  - "metriques RAG"
  - "RAGAS evaluation"
  - "DeepEval RAG"
type: technique
domaine: rag
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/"
  - "https://github.com/confident-ai/deepeval"
tags:
  - "#type/technique"
  - "#domaine/rag"
---

## Description

L'évaluation d'un système RAG mesure deux couches distinctes : la **retrieval** (les documents trouvés sont-ils pertinents et exhaustifs ?) et la **génération** (la réponse est-elle fidèle au contexte et correcte ?). Sans évaluation systématique, impossible de détecter les régressions ou d'optimiser objectivement.

## Métriques principales

### Métriques retrieval

- **Context Precision** — ranking des documents pertinents en haut (sans ground truth, via LLM judge)
- **Context Recall** — toute l'information nécessaire à la réponse a-t-elle été retrouvée (nécessite ground truth)
- **Hit Rate** — au moins 1 document pertinent dans le top-K
- **MRR (Mean Reciprocal Rank)** — position du premier document pertinent

### Métriques génération

- **Faithfulness** — la réponse est-elle entièrement supportée par les documents retrouvés (sans hallucination) ?
- **Answer Relevancy** — la réponse adresse-t-elle la question posée (pertinence sémantique) ?
- **Answer Correctness** — la réponse est-elle factuellement correcte (nécessite ground truth)
- **Hallucination Rate** — taux de réponses contenant des affirmations non supportées

## Frameworks

### RAGAS ([docs.ragas.io](https://docs.ragas.io))

Framework open-source dominant. Métriques LLM-as-judge automatisées avec ou sans ground truth. Intégration native LangChain et LlamaIndex. La doc officielle ne prescrit **pas** de seuils canoniques — les valeurs cibles (0.8+/0.9+) sont des recommandations communauté.

### DeepEval ([github.com/confident-ai/deepeval](https://github.com/confident-ai/deepeval))

Framework pytest-native pour CI/CD. Métriques composables, gates de qualité automatiques. Particulièrement adapté à l'intégration tests de régression.

### LLM-as-judge custom

Pour des critères métiers spécifiques que les frameworks standards ne couvrent pas. Implémenter un juge avec rubric explicite + few-shot examples + audit régulier des verdicts (les juges LLM ont leurs propres biais).

## Patterns d'évaluation

### Golden set frozen
Un jeu de référence (50-200 queries + réponses attendues + documents pertinents annotés) gelé dans le temps. Recalculer toutes les métriques à chaque release.

### A/B testing production
Compare deux configurations (chunking, embedding, reranker) sur traffic réel. Plus représentatif que benchmarks synthétiques.

### Drift detection
Re-embed le golden set régulièrement (hebdomadairement). Mesurer le shift cosinus pour détecter dégradation silencieuse.

### Feedback loops
Thumbs up/down utilisateur → cas de tests automatiques. [[rag-metadata#Feedback loops]] détaille les boucles RAGE.

## Pitfalls

- **Sur-optimiser une métrique** au détriment des autres (faithfulness vs answer relevancy peuvent s'opposer)
- **Juge LLM biaisé** par le modèle générateur (utiliser un juge d'une autre famille)
- **Golden set obsolète** par rapport au corpus actuel (refresh trimestriel minimum)
- **Pas de séparation retrieval vs génération** dans les métriques (impossible de diagnostiquer)

## Liens

- [[MOC-Techniques]]
- [[RAG]]
- [[rag-production]] — monitoring continu en production
- [[rag-metadata]] — métriques cibles et observabilité
- [[agents-evaluation]]
