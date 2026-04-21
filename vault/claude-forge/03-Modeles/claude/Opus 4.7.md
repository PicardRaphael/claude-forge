---
titre: "Claude Opus 4.7"
resume: "SWE-bench 87.6%, adaptive thinking, xhigh effort, nouveau tokenizer, 23 avril = défaut API"
aliases:
  - "opus-4-7"
  - "claude-opus-4-7"
domaine: claude-code
type: modele
derniere-maj: 2026-04-21
auteur: claude
sources:
  - "https://www.anthropic.com/news/claude-opus-4-7"
tags:
  - "#type/modele"
  - "#domaine/claude"
---

## Specs

| Propriété | Valeur |
|-----------|--------|
| Context window | 200K (standard) / 1M (beta) |
| Prix input | $5/MTok |
| Prix output | $25/MTok |
| Thinking | Adaptive (off par défaut, `thinking: {type: "adaptive"}` requis) |
| Vision | 2,576px long edge (3.75 MP) vs 1,568px pour 4.6 |
| Tokenizer | Nouveau, ~1x-1.35x plus de tokens selon contenu |

## Benchmarks

| Benchmark | Score | vs Opus 4.6 |
|-----------|-------|-------------|
| SWE-bench Verified | 87.6% | +6.8% (80.8%) |
| Terminal-Bench 2.0 | 69.4% | +4% (65.4%) |
| GPQA Diamond | 94.2% | +2.9% (91.3%) |

## Changements comportement vs 4.6

- Instructions plus littérales
- Moins de subagents spontanés
- Moins de tool calls
- → Être explicite sur le scope et le parallélisme
- `budget_tokens` **supprimé** (400 error) → utiliser adaptive thinking
- Task budgets (beta) : plafond token pour boucles agentiques

## Dates clés

- 16 avril 2026 : Lancement
- 23 avril 2026 : Devient modèle par défaut Enterprise + API

## Liens

- [[Effort Levels Guide]]
- [[Adaptive Thinking]]
- [[MOC-Modeles]]
