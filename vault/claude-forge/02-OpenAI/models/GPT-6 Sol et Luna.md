---
titre: "GPT-6 Sol et GPT-6 Luna — la gamme GPT-6 sous Astra (22 septembre 2026)"
resume: "Sortis le 22 sept. 2026, modèles de raisonnement via Responses API et Chat Completions. Sol ($2 / $0,20 cache / $10, 1,05M contexte, effort none→max avec medium par défaut) est recommandé par Codex pour le coding agentique ; Luna ($0,10 / $0,01 / $0,50, repris du changelog API) vise le volume. Contrairement à Astra, Sol accepte l'effort none. Benchmarks non vérifiés."
aliases:
  - "GPT-6 Sol"
  - "GPT-6 Luna"
  - "gpt-6-sol"
  - "gpt-6-luna"
  - "Sol Luna OpenAI"
derniere-maj: 2026-09-25
auteur: claude
type: modele
sources:
  - "https://developers.openai.com/api/docs/models/gpt-6-sol"
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
| Contexte | 1 050 000 tokens | non consulté |
| Reasoning effort | `none` · `low` · **`medium` (défaut)** · `high` · `xhigh` · `max` | non consulté |
| API | Responses **et** Chat Completions | idem |

Vérification : la ligne Sol vient de la fiche modèle officielle (`developers.openai.com/api/docs/models/gpt-6-sol`), consultée pendant le run du 25 sept. 2026. La ligne Luna vient du changelog API ; sa fiche modèle n'a pas été consultée. L'annonce `openai.com/index/introducing-gpt-6-sol-and-luna/` a renvoyé 403.

## Ce qui change par rapport à Astra

- **Sol accepte l'effort `none`**, qu'Astra refuse — le seul modèle GPT-6 utilisable sans raisonnement.
- Prix : Sol coûte **5× moins** qu'Astra en entrée et en sortie. Le palier long contexte (×2 input, ×1,5 output au-delà de 272K) est documenté pour Astra ; son application à Sol n'est pas vérifiée.

## Côté Codex

- Sol et Luna apparaissent dans le sélecteur en CLI **0.156.1** (23 sept.) et sur Amazon Bedrock en **0.157.0** (25 sept.). Le message de rate-limit recommande de passer sur Luna.
- La doc Codex ne nomme plus de défaut (*« uses a recommended model »*) et recommande Sol pour le coding agentique complexe (effort de départ Medium), Luna pour le volume (High). Plusieurs sources tierces disent `gpt-6-sol` défaut : non confirmé en primaire. Détail : [[OpenAI Codex]].
- `gpt-5.5` est retiré de ChatGPT, ChatGPT Work et Codex le **14 oct. 2026** ; le remplacement conseillé est `gpt-6-sol`.

## ⚠️ Non vérifié

- Benchmark vendeur rapporté par un agrégateur : Sol à `xhigh` au-dessus d'Opus 5 à `max` sur AutomationBench pour 9 % du coût. Claim vendeur, source non primaire — **ne pas citer**.
- « −50 % par rapport aux tarifs promotionnels de GPT-5.6 » : agrégateur uniquement.

## Pertinence

Pour du routage de modèles en production (agents, RAG), Sol à $2/$10 se place au même prix que [[Sonnet 5]] ($2/$10) et sous [[Opus 5.5]] ($4/$20) ; Luna concurrence les petits modèles sur le volume. À comparer sur des évals réelles avant tout arbitrage.

## Liens

- [[GPT-6 Astra]] — flagship GPT-6
- [[GPT-5.6]] — génération Sol/Terra/Luna précédente
- [[OpenAI Codex]] — sélection de modèle dans Codex
- [[MOC-Modeles]]
