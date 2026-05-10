---
titre: "RAG vs Fine-Tuning — Quand utiliser quoi"
resume: "Guide décisionnel RAG vs fine-tuning vs hybride — RAG pour les faits, fine-tuning pour le comportement, RAFT pour combiner, coûts et privacy comparés"
aliases:
  - "RAG vs fine-tuning"
  - "fine-tuning vs RAG"
  - "RAFT"
  - "quand fine-tuner"
  - "hybrid RAG fine-tuning"
type: technique
domaine: ia
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://gorilla.cs.berkeley.edu/blogs/9_raft.html"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/fine-tuning"
  - "#domaine/rag"
---

> **RAG change ce que le modèle peut VOIR maintenant. Fine-tuning change comment le modèle AGIT à chaque fois.**

## Matrice de décision

| Critère | RAG | Fine-Tuning | Les deux |
|---------|-----|-------------|----------|
| Connaissances mises à jour fréquemment | ✅ | — | — |
| Citations / traçabilité | ✅ | — | ✅ |
| Consistance comportementale | — | ✅ | — |
| Conformité format output | — | ✅ | — |
| Standardisation ton/style | — | ✅ | — |
| Raisonnement domaine + faits frais | — | — | ✅ |
| Workflow réglementé high-stakes | — | — | ✅ |

## Coûts comparés

| Dimension | RAG | Fine-Tuning |
|-----------|-----|-------------|
| Coût initial | Faible (vector DB + embeddings) | Élevé (GPU compute) |
| Coût récurrent | Moyen (infra retrieval) | Faible (servir une fois) |
| Time to value | Rapide (jours) | Moyen (jours-semaines) |
| Fraîcheur connaissances | Excellente | Faible (nécessite re-entraîner) |
| Consistance comportementale | Limitée | Excellente |

## L'hybride — défaut 2026

Architecture recommandée :
1. **Intent router** dirige les requêtes
2. **Path lookup** : RAG pour les requêtes factuelles avec citations
3. **Path behavior** : modèle fine-tuné pour outputs contraints/stylés
4. **Couche évaluation unifiée**

## RAFT — Retrieval Augmented Fine-Tuning

UC Berkeley/Microsoft/Meta. Entraîne le modèle en "open-book" avec 80/20 documents pertinents/distracteurs. Le modèle apprend à identifier les passages pertinents, ignorer les distracteurs, et citer les preuves.

## Raccourci < 200K tokens

Pour une base de connaissances < 200K tokens, le full-context prompting avec prompt caching peut être plus rapide et moins cher que RAG ou fine-tuning.

## Privacy

**RAG est naturellement plus privacy-friendly** : documents supprimables du vector store sans re-entraîner. Fine-tuning embarque dans les poids → problème d'unlearning.

**Approche optimale :** Fine-tune pour style/comportement (faible risque privacy) + RAG pour contenu factuel (facile à update/supprimer).

## Quand Fine-Tuning bat RAG

Lamini Memory Tuning (MoME) : 95% accuracy factuelle vs 50% GPT-4+RAG. Le fine-tuning est catégoriquement meilleur quand :
- Raisonnement domaine-spécifique à internaliser
- Format output rigide requis
- Latence ne tolère pas l'overhead retrieval
- Vocabulaire domaine trop spécialisé pour le modèle base

## Liens

- [[RAG]] — MOC RAG complet
- [[fine-tuning-techniques-peft]] — techniques PEFT
- [[fine-tuning-privacy]] — privacy et RGPD
- [[rag-architecture]] — patterns RAG avancés