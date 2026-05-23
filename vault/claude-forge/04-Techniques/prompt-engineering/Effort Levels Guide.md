---
titre: "Effort Levels Guide"
resume: "5 niveaux d'effort Claude — strict respect sur Opus 4.7, risque under-thinking à low, 64k tokens requis à xhigh/max"
aliases: ["effort levels", "effort", "niveaux effort claude", "xhigh effort", "effort guide claude code", "effort parameter", "effort level best practice", "effort xhigh high medium low", "effort opus sonnet", "effort coding agentique", "task horizon effort", "claude effort config", "effort level recommendation"]
  - "effort levels"
  - "effort"
  - "niveaux effort claude"
  - "xhigh effort"
  - "effort guide claude code"
  - "effort parameter"
domaine: technique
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices"
tags:
  - "#type/technique"
  - "#domaine/prompt-engineering"
---
## Description

Contrôle du niveau de réflexion de Claude. 5 niveaux. Sur Opus 4.7, effort est **plus important que sur tout modèle précédent** et respecté strictement, surtout à low/medium.

## Niveaux

| Niveau | Usage | Notes |
|--------|-------|-------|
| `low` | Questions simples, lookups, latency-sensitive | Minimal thinking, risque under-thinking sur tâches complexes |
| `medium` | Tâches routinières, cost-sensitive | **JAMAIS pour Sonnet** — toujours `high`. Scope le travail au strict demandé |
| `high` | Sessions concurrentes, intelligence-sensitive | Minimum pour Sonnet, minimum recommandé Anthropic pour tâches intelligentes |
| `xhigh` | Défaut Opus 4.7, coding agentique | Sweet spot. Montre nettement plus de tool use en agentic search/coding |
| `max` | Problèmes très durs | Gains possibles mais diminishing returns, parfois prone to overthinking |

## Changement clé Opus 4.7

Opus 4.7 respecte les effort levels **strictement**, surtout à low/medium. À `low`/`medium`, le modèle scope son travail au strict demandé — ne va pas au-delà.

**Si raisonnement superficiel sur problème complexe** : monter effort à `high`/`xhigh` plutôt que prompter autour. Si contraint de rester à `low` pour la latence, ajouter :
```text
This task involves multi-step reasoning. Think carefully through the problem before responding.
```

**Budget tokens à xhigh/max** : Anthropic recommande de partir de 64k max_tokens (à tuner selon usage) pour laisser au modèle la place de penser et d'agir via subagents et tool calls. ("toujours configurer 64k+" était une sur-traduction forge — c'est un starting point recommandé, pas un absolu.)

## Effort et tool use

`high`/`xhigh` montrent nettement plus de tool usage en agentic search et coding. Pour augmenter le tool use sans changer d'effort : prompter explicitement quand et comment utiliser les outils.

## Effort et adaptive thinking

Le thinking adaptatif est steerable. Si le modèle pense trop souvent (peut arriver avec des system prompts longs/complexes) :
```text
Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multi-step reasoning. When in doubt, respond directly.
```

## Règles Claude-Forge

- **Sonnet : `effort: high` OBLIGATOIRE** — jamais medium
- **Opus 4.7 : `effort: xhigh`** = défaut (la plupart du coding agentique)
- `high` pour sessions concurrentes
- `max` uniquement pour problèmes très durs — tester au cas par cas

## Commande

```
/effort
```
Ouvre un slider interactif sans arguments (depuis v2.1.111).

## Liens

- [[Opus 4.7]]
- [[Adaptive Thinking]]
- [[deprecated-techniques-2026]]
- [[MOC-Techniques]]
