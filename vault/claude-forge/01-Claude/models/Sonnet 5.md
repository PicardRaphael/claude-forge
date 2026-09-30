---
titre: "Claude Sonnet 5"
resume: "Sonnet du 30 juin 2026, legacy depuis la sortie de Sonnet 5.5 (28 sept. 2026) mais toujours disponible : 1M contexte, $2/$10 devenu prix standard (la hausse à $3/$15 prévue le 1er sept. n'a pas eu lieu), tokenizer ~1.0-1.35× tokens."
aliases:
  - "sonnet-5"
  - "claude-sonnet-5"
  - "sonnet 5"
  - "claude sonnet 5"
  - "modele sonnet 5"
  - "sonnet 5 tokenizer"
domaine: claude-code
type: modele
derniere-maj: 2026-09-30
auteur: claude
sources:
  - "https://www.anthropic.com/news/claude-sonnet-5"
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
  - "https://platform.claude.com/docs/en/about-claude/pricing"
  - "https://platform.claude.com/docs/en/about-claude/model-deprecations"
  - "https://code.claude.com/docs/en/model-config"
tags:
  - "#type/modele"
  - "#domaine/claude"
  - "#domaine/claude-code"
---

# Claude Sonnet 5

> Annoncé **30 juin 2026** (anthropic.com/news/claude-sonnet-5). Modèle Sonnet le plus agentique d'Anthropic à sa sortie, gains substantiels vs Sonnet 4.6 en raisonnement, tool use, coding, knowledge work.
>
> **Statut au 30 sept. 2026** : **legacy, toujours disponible** (`claude-sonnet-5`, retrait pas avant le 30 juin 2027). Remplacé comme Sonnet courant par **Sonnet 5.5** (`claude-sonnet-5-5`, sorti le 28 sept. 2026, même prix, 5 breaking changes). Source : models overview + model deprecations, platform.claude.com.

## Specifications

| Propriété | Valeur |
|-----------|--------|
| Contexte natif | **1M tokens** (Claude Code, v2.1.197) |
| Thinking | Adaptive |
| Tokenizer | **Nouveau** — même texte → **~1.0-1.35× tokens** selon le type de contenu (rebaser `max_tokens` et budgets contexte/coût). Sonnet 5.5 garde le même tokenizer |
| Cache minimum | 1 024 tokens (512 sur Sonnet 5.5) |
| Défaut | N'est plus le défaut nulle part dans Claude Code : Pro et Team Standard passés sur Opus en v2.1.280 ; Sonnet 5.5 devient le Sonnet par défaut sur l'API Anthropic en v2.1.284 |

## Pricing

Verbatim page Pricing (30 sept. 2026) : *« The $2/$10 per million input/output token pricing for Claude Sonnet 5, announced at launch as introductory pricing through August 31, 2026, is now the standard price. The previously scheduled increase to $3/$15 per million input/output tokens on September 1, 2026 will not occur. »*

| Poste | Prix |
|---|---|
| Input | $2 / MTok |
| Output | $10 / MTok |
| Cache write 5 min / 1 h | $2,50 / $4 par MTok |
| Cache read | $0,20 / MTok |
| Batch | $1 / $5 par MTok |

Historique : au lancement, $2/$10 était présenté comme promotionnel jusqu'au 31 août 2026, avec un passage annoncé à $3/$15 — passage annulé.

## Claude Code

- Modèle par défaut de Claude Code de **v2.1.197** (juillet 2026) jusqu'au basculement des plans Pro/Team Standard sur Opus en **v2.1.280** (cf [[CC juillet 2026 - Sonnet 5 + v2.1.198]] et [[CC septembre 2026 - Opus 5.5 + v2.1.263-282]]).
- Contexte natif 1M tokens.
- ⚠️ Le tokenizer gonfle le compte de tokens (~30 % sur contenu typique, jusqu'à ~1.35×) → impacte budgets contexte et coût à l'usage.

## Benchmarks (déclarés Anthropic)

- Humanity's Last Exam (baseline Sonnet 4.6 mis à jour) : 34.6 % sans outils / 46.8 % avec outils
- OSWorld-Verified (baseline Sonnet 4.6) : 78.5 %
- Sécu : n'a pas développé d'exploit Firefox fonctionnel (0.0 %) ; taux de comportements désalignés < Sonnet 4.6, mais > Opus 4.8 et Mythos Preview
- Détail complet : System Card Sonnet 5 (lien anthropic.com).

## Implications forge

- L'alias `sonnet` des frontmatters ne désigne plus Sonnet 5 : sur l'API Anthropic il résout vers **Sonnet 5.5** (table « alias resolution » de `code.claude.com/docs/en/model-config`, vérifiée le 30 sept. 2026 ; ailleurs : Sonnet 4.6 sur Claude Platform on AWS, Sonnet 4.5 sur Bedrock / Google Cloud / Foundry). Forge n'a plus aucun composant `sonnet` depuis le 30 sept. 2026 (Opus `medium` pour l'exécution, [[raisonnement-2026-09-30-zero-sonnet]]) ; les repos projet qui gardent `model: sonnet` tournent sur Sonnet 5.5.
- Même page : dans Claude Code, **Sonnet 5.5 démarre à l'effort `medium`** faute de réglage explicite (*« `high` on every model that supports effort, except that Opus 5.5 and Sonnet 5.5 default to `medium` »*), alors que le défaut de l'API est `high`. Un composant `sonnet` sans `effort:` tourne en `medium`.
- Sonnet 5.5 recalibre les niveaux d'effort (*« Re-run your effort sweep rather than carrying a setting over »*) : un réglage validé sur Sonnet 5 ne se transpose pas tel quel. Voir [[effort-opus-47-doctrine-anthropic-2026]].
- L'advisor tool refuse Sonnet 5 comme conseiller d'un exécuteur Sonnet 5.5 (400).
- Le tokenizer plus gourmand renforce la discipline tokens (MEMORY.md, notes courtes).

## Liens

- [[Sonnet 4.6]] — génération précédente
- [[Opus 5.5]] — génération Opus courante
- [[CC juillet 2026 - Sonnet 5 + v2.1.198]] — changelog CC associé
- [[MOC-Modeles]]
