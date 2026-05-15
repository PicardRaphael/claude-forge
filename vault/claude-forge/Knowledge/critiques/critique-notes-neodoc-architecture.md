---
titre: "Critique — Notes architecture NeoDoc (3 notes vault)"
type: knowledge
domaine: neo_ia
derniere-maj: 2026-05-11
auteur: claude
aliases:
  - "critique neodoc architecture"
  - "critique notes neodoc"
  - "devil advocate neodoc archi"
  - "review neodoc vault"
tags:
  - "#type/knowledge"
  - "#domaine/neoteem"
resume: "Critique DA des 3 notes architecture NeoDoc — research agent, ingestion pipeline, architecture. Objections et recommandations sur la documentation vault."
---

## Verdict : LIVRER TEL QUEL

Vérifié contre le code source `apps/neodoc/` :

- **Graph** : 5 nœuds confirmés (decompose, retrieve, full_doc_retrieve, generate, respond), routing conditionnel exact
- **State** : ResearchState TypedDict correspond au code (13+ champs)
- **Ingestion** : pipeline 7 étapes correspond à `ingestion_service.py`, modes sync/async/batch/folder confirmés
- **Discovery Engine** : v1alpha SDK, 3 clients, filtres multi-tenant exacts
- **google-genai natif** dans decompose_node (pas LangChain) : confirmé

## Aucune erreur factuelle détectée

Les notes sont exactes et complètes pour une documentation d'architecture vault.

## Liens

- [[neodoc-architecture]]
- [[neodoc-research-agent]]
- [[neodoc-ingestion-pipeline]]
