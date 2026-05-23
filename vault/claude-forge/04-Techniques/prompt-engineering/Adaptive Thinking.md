---
titre: "Adaptive Thinking"
resume: "Thinking adaptatif Claude — steerable via effort+prompt, surpasse extended thinking en evals internes, calibrage dynamique par complexité"
aliases:
  - "adaptive thinking"
  - "extended thinking"
  - "reflexion etendue"
  - "thinking mode claude"
  - "chain of thought claude"
  - "interleaved thinking"
domaine: technique
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7"
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices"
tags:
  - "#type/technique"
  - "#domaine/prompt-engineering"
---

## Description

Mode de réflexion de Claude qui calibre dynamiquement **quand** et **combien** penser selon deux facteurs : le paramètre `effort` et la complexité de la query. En evals internes Anthropic, adaptive thinking *reliably outperforms* extended thinking avec `budget_tokens` ("surpasse de manière fiable" — verbatim Anthropic, "systématiquement" était une sur-traduction).

## Configuration API

```python
client.messages.create(
    model="claude-opus-4-7",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[{"role": "user", "content": "..."}],
)
```

## Comportement

- **Off par défaut** — `thinking: {type: "adaptive"}` explicite requis
- `budget_tokens` : **deprecated sur Opus 4.6 / Sonnet 4.6** (fonctionnel mais à migrer), **removed sur Opus 4.7** (erreur 400 si passé). Migration officielle vers `effort` (cf migration guide Anthropic).
- Sur queries simples qui ne nécessitent pas de thinking → répond directement
- Sur queries complexes → raisonne en profondeur

## Steerability (guide officiel Anthropic)

Le triggering est **promptable**. Si le modèle pense trop souvent (system prompts longs/complexes) :
```text
Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multi-step reasoning. When in doubt, respond directly.
```

Pour guider le thinking interleaved (après tool results) — verbatim complet Anthropic (corrigé 2026-05-23, version forge précédente tronquée) :
```text
After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding. Use your thinking to plan and iterate based on this new information, and then take the best next action.
```

## Bonnes pratiques (Anthropic)

- Instructions générales > steps prescriptifs — "think thoroughly" produit souvent un meilleur raisonnement qu'un plan étape-par-étape écrit à la main
- Multishot fonctionne avec thinking — utiliser `<thinking>` dans les few-shot examples
- Self-check : "Before you finish, verify your answer against [test criteria]" — particulièrement fiable pour coding/math
- CoT manuel reste possible en fallback quand thinking est off — demander à Claude de raisonner avec des tags `<thinking>` et `<answer>`

## Migration depuis extended thinking

| Avant (extended thinking) | Après (adaptive) |
|--------------------------|------------------|
| `thinking: {type: "enabled", budget_tokens: 32000}` | `thinking: {type: "adaptive"}` + `effort: "high"` |
| Contrôle par `budget_tokens` | Contrôle par `effort` |
| Budget fixe | Calibrage dynamique |

## Liens

- [[Opus 4.7]]
- [[Effort Levels Guide]]
- [[deprecated-techniques-2026]]
- [[MOC-Techniques]]
