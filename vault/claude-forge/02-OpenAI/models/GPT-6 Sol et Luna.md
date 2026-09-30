---
titre: "GPT-6 Sol et GPT-6 Luna — la gamme GPT-6 sous Astra (22 septembre 2026)"
resume: "Sortis le 22 sept. 2026, modèles de raisonnement via Responses API et Chat Completions. Sol ($2 / $0,20 cache / $10, 1,05M contexte, effort none→max avec medium par défaut) vise le coding agentique ; Luna ($0,10 / $0,01 / $0,50, 1,05M contexte, fiche confirmée) vise le volume. Sol est suivi dès le 29 sept. par GPT-6.1 Sol, défaut du catalogue Codex. Benchmarks non vérifiés."
aliases:
  - "GPT-6 Sol"
  - "GPT-6 Luna"
  - "gpt-6-sol"
  - "gpt-6-luna"
  - "Sol Luna OpenAI"
derniere-maj: 2026-09-30
auteur: claude
type: modele
sources:
  - "https://developers.openai.com/api/docs/models/gpt-6-sol"
  - "https://developers.openai.com/api/docs/models/gpt-6-luna"
  - "https://developers.openai.com/api/docs/changelog"
  - "https://learn.chatgpt.com/docs/models"
  - "https://learn.chatgpt.com/docs/changelog"
tags:
  - "#type/modele"
  - "#domaine/openai"
  - "#domaine/modeles"
---

# GPT-6 Sol et GPT-6 Luna

> Annoncés le **22 septembre 2026** au changelog API officiel : *« GPT-6 Sol & GPT-6 Luna — reasoning models via Responses and Chat Completions APIs »*. Ils complètent [[GPT-6 Astra]] (3 sept.) en reprenant la segmentation de [[GPT-5.6]] : un flagship, un modèle de travail, un modèle de volume.

## Specs

| | GPT-6 Sol | GPT-6 Luna |
|---|---|---|
| Rôle | coding et workflows agentiques | tâches ciblées à fort volume |
| Prix ($/M, ≤ 272K d'entrée) | **2 input · 0,20 cache · 10 output** | **0,10 · 0,01 · 0,50** |
| Contexte | 1 050 000 tokens | 1 050 000 tokens · sortie max 128 000 · cutoff 18 mai 2026 |
| Reasoning effort | `none` · `low` · **`medium` (défaut)** · `high` · `xhigh` · `max` | non consulté |
| API | Responses **et** Chat Completions | idem |

Vérification : la ligne Sol vient de la fiche modèle officielle (`developers.openai.com/api/docs/models/gpt-6-sol`), consultée le 25 sept. 2026. La ligne Luna vient de sa fiche officielle (`…/models/gpt-6-luna`), consultée le 30 sept. 2026 par un chercheur (extrait résumé) : prix identiques au changelog. L'annonce `openai.com/index/introducing-gpt-6-sol-and-luna/` a renvoyé 403.

Changelog API du 25 sept. : correctif d'un bug d'encodage d'image qui dégradait la compréhension d'image de Sol et Luna (API et Codex, computer use compris) ; OpenAI conseille de relancer les évals image.

## Successeur : GPT-6.1 Sol (29 sept. 2026)

Changelog Codex, verbatim : *« GPT-6.1 Sol offers near-Astra performance for complex work at a lower cost than Astra. »* Fiche `gpt-6.1-sol` (lue par un chercheur, extrait résumé) : $2 input · $0,10 cache · $10 output, cache write $2,50, contexte 1,05M, sortie 128K, cutoff 30 avril 2026 ; multi-agent en beta via la Responses API. Défaut du catalogue Codex CLI depuis la 0.159.1. Pas de fiche vault dédiée à ce jour.

## Ce qui change par rapport à Astra

- **Sol accepte l'effort `none`**, qu'Astra refuse — le seul modèle GPT-6 utilisable sans raisonnement. D'après le guide de prompting GPT-6 (lu via un chercheur), 6.1 Sol ne l'accepte pas non plus.
- Prix : Sol coûte **5× moins** qu'Astra en entrée et en sortie. Le palier long contexte (×2 input, ×1,5 output au-delà de 272K) est documenté pour Astra ; son application à Sol n'est pas vérifiée.

## Côté Codex

- Sol et Luna apparaissent dans le sélecteur en CLI **0.156.1** (23 sept.) et sur Amazon Bedrock en **0.157.0** (25 sept.). Le message de rate-limit recommande de passer sur Luna.
- Du 22 au 28 sept., la doc Codex ne nommait pas de défaut (*« uses a recommended model »*) et recommandait Sol pour le coding agentique complexe (effort de départ Medium), Luna pour le volume (High). Des sources tierces disaient `gpt-6-sol` défaut, jamais confirmé en primaire. Depuis le 29 sept., le défaut du catalogue est `gpt-6.1-sol`. Détail : [[OpenAI Codex]].
- `gpt-5.5` est retiré de ChatGPT, ChatGPT Work et Codex le **14 oct. 2026** ; le remplacement conseillé est `gpt-6-sol`.

## ⚠️ Non vérifié

- Benchmark vendeur rapporté par un agrégateur : Sol à `xhigh` au-dessus d'Opus 5 à `max` sur AutomationBench pour 9 % du coût. Claim vendeur, source non primaire — **ne pas citer**.
- « −50 % par rapport aux tarifs promotionnels de GPT-5.6 » : agrégateur uniquement.

## Pertinence

Pour du routage de modèles en production (agents, RAG), Sol et 6.1 Sol à $2/$10 se placent au même prix que Sonnet 5.5 et [[Sonnet 5]] ($2/$10) et sous [[Opus 5.5]] ($4/$20) ; Luna concurrence les petits modèles sur le volume. À comparer sur des évals réelles avant tout arbitrage.

## Liens

- [[GPT-6 Astra]] — flagship GPT-6
- [[GPT-5.6]] — génération Sol/Terra/Luna précédente
- [[OpenAI Codex]] — sélection de modèle dans Codex
- [[MOC-Modeles]]
