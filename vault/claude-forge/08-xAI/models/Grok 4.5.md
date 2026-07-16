---
titre: "Grok 4.5 — premier modèle SpaceXAI coding/agentic"
resume: "Lancé 8 juillet 2026 par SpaceXAI (rebrand xAI finalisé la veille) — 1.5T params V9, co-entraîné sur données Cursor, différenciateur = token efficiency (4.2x moins d'output qu'Opus 4.8 sur SWE-Bench Pro), 500K contexte, $2/$6"
aliases:
  - "Grok 4.5"
  - "grok-4-5"
  - "modèle SpaceXAI"
  - "Grok coding"
type: model
derniere-maj: 2026-07-16
auteur: claude
sources:
  - "https://x.ai/news/grok-4-5"
  - "https://www.axios.com/2026/07/08/spacexai-grok-new-model"
tags:
  - "#type/modele"
  - "#domaine/xai"
---

# Grok 4.5

Lancé le **8 juillet 2026** — premier modèle xAI/SpaceXAI conçu spécifiquement pour le coding et l'agentic (le rebrand **SpaceXAI** a été finalisé la veille, 7 juillet). Fondation V9 de **1.5T paramètres**, entraîné sur GPU GB300, **co-entraîné avec des données Cursor** (xAI/SpaceX a acquis Cursor — flywheel données éditeur → modèle).

## Positionnement

- PAS un top scorer absolu (Fable 5 mène la plupart des évals coding, Opus 4.8 le bat sur certaines) — le différenciateur est la **token efficiency** : 15 954 output tokens vs 67 020 pour Opus 4.8 sur SWE-Bench Pro (**4.2x d'écart**)
- ~80 tok/s, **$2/$6 par 1M tokens** — Musk : « roughly comparable to Opus 4.7, but much faster »
- Artificial Analysis Intelligence Index #4 global ; Elo 1 543 sur GDPval-AA v2 (entre Opus 4.8 et GLM-5.2) ; leader indépendant sur l'agentic tool use
- Contexte **réduit à 500K** (vs 1M sur Grok 4.3)

## Caveats

- **Leak d'un snapshot de codebase Cursor dans les données d'entraînement**, divulgué par Cursor : scores dérivés de CursorBench gonflés (benchmarks tiers non affectés)
- Pas disponible en EU au lancement (attendu mi-juillet)
- Contexte connexe : scandale Grok Build (upload de repos privés d'utilisateurs vers des serveurs xAI) → pledge Musk open-source du code X, 15 juil. — cf [[industrie-juillet-2026]]

## Liens

- [[xAI Grok]] — fiche produit
- [[grok-code-fast-1]] — modèle coding précédent
- [[MOC-Modeles]] · [[MOC-Outils-IA]]
