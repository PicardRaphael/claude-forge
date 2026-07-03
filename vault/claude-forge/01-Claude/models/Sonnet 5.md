---
titre: "Claude Sonnet 5"
resume: "Sonnet le plus agentique — défaut Claude Code (v2.1.197), 1M contexte natif, nouveau tokenizer (~1.0-1.35× tokens), pricing promo $2/$10 jusqu'au 31 août 2026"
aliases:
  - "sonnet-5"
  - "claude-sonnet-5"
  - "sonnet 5"
  - "claude sonnet 5"
  - "modele sonnet 5"
  - "sonnet 5 tokenizer"
domaine: claude-code
type: modele
derniere-maj: 2026-07-02
auteur: claude
sources:
  - "https://www.anthropic.com/news/claude-sonnet-5"
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
tags:
  - "#type/modele"
  - "#domaine/claude"
  - "#domaine/claude-code"
---

# Claude Sonnet 5

> Annoncé **30 juin 2026** (anthropic.com/news/claude-sonnet-5). Modèle Sonnet le plus agentique d'Anthropic, gains substantiels vs Sonnet 4.6 en raisonnement, tool use, coding, knowledge work.

## Specifications

| Propriété | Valeur |
|-----------|--------|
| Contexte natif | **1M tokens** (Claude Code, v2.1.197) |
| Thinking | Adaptive |
| Tokenizer | **Nouveau** — même texte → **~1.0-1.35× tokens** selon le type de contenu (rebaser `max_tokens` et budgets contexte/coût) |
| Défaut | **Free / Pro** (Claude Platform) + **défaut Claude Code depuis v2.1.197** |

## Pricing

- **Promo** : **$2 / MTok input · $10 / MTok output** jusqu'au **31 août 2026**
- **Standard** ensuite : **$3 / MTok input · $15 / MTok output**

## Claude Code

- **Nouveau modèle par défaut depuis CC v2.1.197** (cf [[CC juillet 2026 - Sonnet 5 + v2.1.198]]).
- Contexte natif 1M tokens.
- ⚠️ Le nouveau tokenizer gonfle le compte de tokens (~30 % sur contenu typique, jusqu'à ~1.35×) → impacte budgets contexte et coût à l'usage.

## Benchmarks (déclarés Anthropic)

- Humanity's Last Exam (baseline Sonnet 4.6 mis à jour) : 34.6 % sans outils / 46.8 % avec outils
- OSWorld-Verified (baseline Sonnet 4.6) : 78.5 %
- Sécu : n'a pas développé d'exploit Firefox fonctionnel (0.0 %) ; taux de comportements désalignés < Sonnet 4.6, mais > Opus 4.8 et Mythos Preview
- Détail complet : System Card Sonnet 5 (lien anthropic.com).

## Implications forge

- **Défaut CC** = les sessions et sub-agents `model: sonnet` tournent désormais sur Sonnet 5. Vérifier que la doctrine effort (cf [[effort-opus-47-doctrine-anthropic-2026]]) reste calibrée : Sonnet 5 = exécution/comparatif, Opus 4.8 = jugement (préférence modèle Raphael tracée en mémoire forge : Opus 4.8 pour le jugement).
- Le tokenizer plus gourmand renforce la discipline tokens (MEMORY.md, notes courtes).

## Liens

- [[Sonnet 4.6]] — génération précédente
- [[Opus 4.7]] — génération Opus courante (pas de fiche Opus 4.8 dédiée)
- [[CC juillet 2026 - Sonnet 5 + v2.1.198]] — changelog CC associé
- [[MOC-Modeles]]
