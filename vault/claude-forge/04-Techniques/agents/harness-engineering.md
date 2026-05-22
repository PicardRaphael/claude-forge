---
titre: "Harness Engineering"
resume: "Nouvelle discipline 2026 : tout ce qui entoure le modèle LLM (état, outils, feedback loops, contraintes, orchestration) — contraintes déterministes > prompts suggestifs"
aliases:
  - "harness engineering"
  - "agent harness"
  - "model harness"
  - "agentic harness"
  - "everything around the model"
  - "agent infrastructure"
domaine: technique
type: technique
derniere-maj: 2026-05-14
auteur: claude
sources:
  - "https://martinfowler.com/articles/harness-engineering.html"
  - "Simon Willison — Agentic Engineering Patterns ch.12"
  - "Addy Osmani — agent infrastructure"
tags:
  - "#type/technique"
  - "#domaine/agents"
---

## Description

Discipline émergente (mars 2026+) définie par Martin Fowler (ThoughtWorks), Addy Osmani, et Simon Willison.

**Formule centrale :**

> Agent = Modèle + Harness

Le harness = tout ce qui **entoure** le modèle et qui n'est pas le modèle lui-même.

## Composants du Harness

| Composant | Description |
|---|---|
| **State management** | Persistance de l'état entre les appels (mémoire, contexte) |
| **Tool execution** | Couche d'exécution et validation des tool calls |
| **Feedback loops** | Signaux de succès/échec retournés au modèle |
| **Enforceable constraints** | Contraintes déterministes (linters, guards, hooks) |
| **Context management** | Assemblage dynamique du contexte par tâche |
| **Sub-agent orchestration** | Coordination d'agents spécialisés |

## Insight clé : déterministe > suggestif

> **Linters qui bloquent > Prompts qui suggèrent**

Un prompt disant "ne modifie pas les fichiers de configuration" sera ignoré 5% du temps.  
Un hook qui exit(2) quand un fichier de config est modifié = 100% d'enforcement.

C'est le passage de l'**advisory** (instructions) au **déterministe** (contraintes exécutables).

## Relation avec le vault forge

Le vault forge-brain applique déjà ce principe :
- `delegate-guard.py` — bloque les edits directs de skills/agents
- `devil-advocate-guard.py` — force le devil's advocate sur les livrables
- `vault-query-guard.py` — bloque les writes sans consultation vault préalable

Ces hooks = harness engineering appliqué à Claude Code.

## Couches du Harness (architecture)

```
┌─────────────────────────────────┐
│  Orchestration (subagents)      │
├─────────────────────────────────┤
│  Context Assembly               │
├─────────────────────────────────┤
│  Enforceable Constraints/Hooks  │
├─────────────────────────────────┤
│  Tool Execution Layer           │
├─────────────────────────────────┤
│  State Management               │
└─────────────────────────────────┘
         ↕ modèle LLM ↕
```

## Évolution du paradigme (mai 2026)

**Reconnu comme 4e paradigme** de l'AI Engineering (TechTimes, 13 mai 2026) :

```
Prompt Engineering (2022-24) → Context Engineering (2025) → Harness Engineering (2026)
```

**65% des échecs d'agents** tracent à des défauts de harness, PAS à des limitations du modèle.

### Feedforward vs Feedback (Fowler)

| Type | Quand | Exemples |
|------|-------|----------|
| **Feedforward (guides)** | AVANT action — anticipation | CLAUDE.md, SKILL.md contraintes, architecture docs |
| **Feedback (sensors)** | APRÈS action — correction | Hooks exit 2, linters, tests, type checkers |

**Feedforward > Feedback** — mieux vaut anticiper que corriger. Mais les deux sont nécessaires.

### Computational vs Inferential

| | Computational | Inferential |
|---|---|---|
| Vitesse | ms-sec | sec-min |
| Fiabilité | Déterministe, 100% | Probabiliste, ~95% |
| Exemples | Linters, hooks, tests | AI code review, semantic analysis |
| Coût | CPU, quasi gratuit | GPU/API, cher |

**Priorité : Computational d'abord, Inferential en complément.**

### Ashby's Law appliquée

Réduire la variété que l'agent doit gérer → réduire le scope → harness plus complet possible. 1 skill = 1 responsabilité.

### Ressources

- awesome-harness-engineering (GitHub ai-boost) — catalogue complet patterns/outils
- Martin Fowler article — référence canonique
- Augment Code Guide — application au coding

## Quand utiliser

- Design d'un système multi-agent
- Audit d'un agent existant qui a des comportements imprévisibles
- **Diagnostic de skill Cowork qui ne suit pas les instructions** — c'est un problème de harness
- Décider entre "prompt instruction" et "hook déterministe"
- Évaluation de la robustesse d'un pipeline agentic

## Liens

- [[Context Engineering]] — Composant "orchestration" du harness
- [[workflow-claude-code-optimal]] — Patterns de harness appliqués (Boris, Karpathy)
- [[agents-securite]] — Sandboxing et permissions = couches du harness
- [[mass-multi-agent-system-search]] — Optimisation automatisée du harness multi-agent
- [[MOC-Techniques]]
