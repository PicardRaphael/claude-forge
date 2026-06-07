---
aliases:
  - Google MIT scaling agent systems
  - Towards a Science of Scaling Agent Systems
  - arXiv 2512.08296
  - 180 expériences multi-agent
  - quantitative scaling principles
  - sequential degradation 39 70
resume: "Paper Google + MIT (Kim et al. 2025, arXiv 2512.08296) — 180 expériences contrôlées. Sequential tasks dégradent 39-70%, parallel +81%, threshold single-agent 45%, error amplification 17x vs 4.4x centralisé."
derniere-maj: 2026-06-07
tags:
  - "#type/technique"
  - "#domaine/agents"
  - "#source/arxiv"
  - "#statut/canonique"
---

# Google + MIT — Towards a Science of Scaling Agent Systems

## Source primaire

- Paper : arXiv 2512.08296
- Auteurs : Kim et al. (Google Research + MIT)
- Date : décembre 2025
- Méthode : **180 expériences contrôlées** sur multi-agent systems

Première étude qui quantifie les principes de scaling pour systèmes d'agents.

## Résultats chiffrés clés

### ✅ Parallel tasks (financial analysis type)

Coordination multi-agent centralisée : **+81% performance** quand les sous-tâches sont indépendantes (analyse trends, costs, market data en parallèle, agrégation finale).

### ❌ Sequential tasks (PlanCraft, Minecraft planning)

**Toute variante multi-agent dégrade -39% à -70%** sur tâches séquentielles où chaque action dépend de l'état précédent (inventaire Minecraft, etc.).

Raison : overhead de communication fragmente le raisonnement, "cognitive budget" insuffisant pour la tâche réelle.

### Single-agent threshold

Quand un single agent atteint **>45% success rate** sur une tâche, le multi-agent n'est pas cost-effective.

### Tool-use bottleneck

Plus de tools = plus de coordination cost. À partir d'un seuil, coordination > gain.

### Error amplification

- **Agents indépendants** : erreurs amplifiées jusqu'à **17x** (propagation non vérifiée)
- **Coordination centralisée** : amplification limitée à **4.4x** (orchestrateur valide outputs)

## Conclusion verbatim

> "Multi-agent benefits depend critically on task structure rather than team size alone. Effective system design requires matching coordination topology to problem characteristics, rather than assuming uniform benefits from scaling agent count."

Le framework identifie l'architecture optimale pour **87% des configurations held-out**.

## Implications pour forge / claude-forge

1. **Auditer chaque agent forge** : la tâche est-elle séquentielle ou parallèle ?
2. **Threshold 45%** : single agent suffit-il ? Si oui, pas de sub-agent.
3. **Orchestrateur central > swarm indépendant** (17x → 4.4x error amplification)
4. **Mesurer success rate single-agent AVANT** de proposer sub-agent

## Liens

- [[comment-creer-agent]] — à enrichir avec threshold 45%
- [[workflow-claude-code-optimal]] — coordination topology
- [[will-vs-ecc-deux-doctrines-anthropic]] — résolution paradoxe minimum vs maximum
- [[multi-agent-handoff-loss-pattern]]

## Référence

- [arXiv 2512.08296](https://arxiv.org/pdf/2512.08296)
- [InfoQ Feb 2026 coverage](https://www.infoq.com/news/2026/02/google-agent-scaling-principles/)
- [The Decoder coverage](https://the-decoder.com/more-ai-agents-isnt-always-better-new-google-and-mit-study-finds/)
