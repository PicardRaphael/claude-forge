---
titre: "Claude Opus 5 — flagship Opus, proche de Fable 5 à moitié prix"
resume: "Lancé le 24 juillet 2026 : claude-opus-5, $5/$25 par MTok (inchangé vs 4.8), 1M contexte / 128k output, thinking ON par défaut, fast mode ~2,5× à $10/$50, SOTA Frontier-Bench (double Opus 4.8), défaut Opus dans Claude Code v2.1.219 et défaut Claude Max"
aliases:
  - "Claude Opus 5"
  - "Opus 5"
  - "claude-opus-5"
  - "opus-5"
  - "Claude Honeycomb"
derniere-maj: 2026-07-27
auteur: claude
type: modele
sources:
  - "https://www.anthropic.com/news/claude-opus-5"
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
  - "https://techcrunch.com/2026/07/24/anthropic-launches-opus-5/"
  - "https://www.axios.com/2026/07/24/anthropic-releases-new-model-opus-5"
tags:
  - "#type/modele"
  - "#domaine/anthropic"
  - "#domaine/claude"
---

# Claude Opus 5

> Annoncé **24 juillet 2026** (« Introducing Claude Opus 5 », vérifié source primaire). 4e modèle de la famille Claude 5 en moins de 2 mois (après Fable 5, Mythos 5, Sonnet 5). Successeur direct d'[[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows|Opus 4.8]]. Positionnement verbatim : *« comes close to the frontier intelligence of Claude Fable 5 at half the price »* — et *« much stronger at verifying its work and iterating carefully until it succeeds »*.

## Specs

| Item | Valeur |
|------|--------|
| ID modèle | `claude-opus-5` (Bedrock : `us./eu./au./global.anthropic.claude-opus-5`) |
| Date | 24 juillet 2026 |
| Prix standard | $5 / M input · $25 / M output (identique Opus 4.8, moitié de Fable 5) |
| Fast mode | $10 / $50 par MTok, ~2,5× la vitesse (research preview API + usage credits Claude Code) |
| Contexte | **1M tokens** / 128k output |
| Thinking | **ON par défaut** ; effort low/medium/high/**xhigh/max** |
| Défauts produit | Défaut **Claude Max** ; défaut Opus **Claude Code v2.1.219** ; plus fort modèle sur Pro |
| Dispo | Claude API, Bedrock, Vertex, Microsoft Foundry, claude.ai, Claude Code, Cowork — immédiate |

## Benchmarks (annonce officielle)

- **SOTA Frontier-Bench v0.1** — plus du **double d'Opus 4.8** ; SOTA **GDPval-AA**.
- À **0,5 % du pic de Fable 5** sur CursorBench 3.2, à moitié prix.
- **ARC-AGI 3 : 30,2 %** en High (3× le next-best, vérifié par ARC Prize le jour du launch).
- **OSWorld 2.0** : bat tout modèle à tout niveau de coût.
- Reste **derrière Mythos 5** en cybersécurité (exploit development) et biologie long-horizon.
- Alignement : *« most aligned model to date »*, score comportemental 2,3 (le plus bas des modèles récents). Requêtes flaggées → fallback **Opus 4.8** (même mécanique que Fable 5).

## ⚠️ Breaking changes migration (depuis Opus 4.8)

- **Thinking ON par défaut** ; `thinking: disabled` + effort xhigh/max → **erreur 400** (source secondaire, à re-vérifier docs plateforme).
- `speed: "fast"` sur **Opus 4.7 → erreur** désormais (retiré du fast mode, pas de fallback) — fast mode = Opus 5 + Opus 4.8 uniquement.
- 2 betas API lancées avec Opus 5 : **mid-conversation tool changes** (header `mid-conversation-tool-changes-2026-07-01`, préserve le prompt cache) et **automatic fallbacks** (requêtes flaggées re-routées au lieu de bloquées).

## Trail pré-launch (résolu)

- Leak **« Claude Honeycomb EAP »** vu 8-9 juillet quelques heures dans le model picker Cursor (« research model with per-turn controls and safety fallbacks, 1M context, xhigh effort ») — c'était Opus 5.
- Polymarket donnait 31 % pour un launch le jeudi 23 juillet — manqué d'un jour (vendredi 24).

## Contexte famille Claude 5 (au 27 juillet 2026)

4 tiers : [[Fable 5]] (Mythos-class) > **Opus 5** > [[Sonnet 5]] > Haiku 4.5 (aucun signal Haiku 5). Le 20 juillet, Fable 5 est recadré : inclus en permanence dans Max/Team Premium mais à 50 % des limites hebdo (réduites de 33 % le même jour) ; Pro/Team Standard passent en usage credits $10/$50 + crédit one-time $100.

## Pertinence forge

- **La ligne CLAUDE.md forge « `opus` = claude-opus-4-8 (dernier Opus) » est périmée** — `model: opus` dans les frontmatters d'agents résout désormais vers Opus 5.
- Doctrine [[feedback_allocation_modele_effort|allocation modèle/effort]] « Sonnet exécution / Opus jugement » : le tier jugement monte en capacité à prix constant — pas de raison de pivoter, mais vérifier le comportement thinking-ON-par-défaut sur les agents jugement.
- Gotcha : comme Fable 5, fallback classifier vers Opus 4.8 possible sur requêtes flaggées.

## Wikilinks

- [[Fable 5]] — tier au-dessus, recadrage limites 20 juillet
- [[Sonnet 5]] — tier en-dessous, défaut CC Free/Pro
- [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] — prédécesseur Opus 4.8
- [[CC juillet 2026 - Opus 5 + v2.1.212-220]] — versions CC liées
- [[MOC-Modeles]]
