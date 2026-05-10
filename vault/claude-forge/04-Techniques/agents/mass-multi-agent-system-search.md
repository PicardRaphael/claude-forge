---
titre: "MASS — Multi-Agent System Search"
resume: "Framework Google DeepMind + Cambridge (ICLR 2026) pour optimiser automatiquement les systèmes multi-agents : prompts individuels, topologie des interactions, et prompts globaux en 3 étapes interleaved"
aliases:
  - "MASS"
  - "multi-agent system search"
  - "MASS DeepMind"
  - "agent topology optimization"
  - "arXiv 2502.02533"
  - "multi-agent prompt optimization"
domaine: technique
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://arxiv.org/abs/2502.02533"
tags:
  - "#type/technique"
  - "#domaine/agents"
---

## Description

Framework automatisé de Google DeepMind + Cambridge, présenté à ICLR 2026 (arXiv 2502.02533). Optimise conjointement les prompts des agents individuels ET la topologie de leurs interactions — une première.

Premier framework à résoudre simultanément :
1. **Comment** chaque agent est instruit
2. **Comment** les agents s'organisent entre eux

## Les 3 étapes MASS (interleaved)

### Étape 1 — Block-level prompt optimization

Optimise les instructions de chaque agent individuellement.  
"Bloc" = un agent ou sous-système cohérent.  
Technique : optimisation itérative des prompts par feedback sur les sorties.

### Étape 2 — Workflow topology optimization

Restructure les interactions entre agents :
- Quel agent appelle quel autre ?
- Parallèle ou séquentiel ?
- Loops de feedback ou pipeline linéaire ?

La topologie est traitée comme une variable d'optimisation, pas comme un design figé.

### Étape 3 — Workflow-level prompt optimization

Optimise les prompts **globaux** du système (context commun, instructions de coordination) sur la base de la topologie finale.

L'interleaving signifie que ces 3 étapes se nourrissent mutuellement : une meilleure topologie informe les prompts locaux, et vice-versa.

## Pourquoi c'est important

Avant MASS, l'optimisation des systèmes multi-agents était manuelle et partielle :
- On optimisait les prompts sans toucher la topologie
- Ou on restructurait la topologie sans re-optimiser les prompts

MASS prouve que les deux sont interdépendants et doivent être optimisés ensemble.

## Application à forge

Le harness forge (hooks, agents spécialisés, skill-creator, devil's advocate) est un système multi-agent dont la topologie a été designée manuellement. MASS suggère que cette topologie pourrait être optimisée automatiquement — sujet d'exploration futur.

## Quand utiliser

- Design d'un pipeline multi-agent complexe (> 3 agents)
- Diagnostic d'un système multi-agent sous-performant
- Audit de la topologie d'orchestration existante

## Liens

- [[harness-engineering]] — Framework conceptuel pour les systèmes agentic
- [[Context Engineering]] — Composant orchestration (pilier 4)
- [[agents-architecture]] — Patterns d'architecture agents existants
- [[MOC-Techniques]]
