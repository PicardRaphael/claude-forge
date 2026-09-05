---
titre: "GPT-6 Astra — flagship OpenAI du 3 septembre 2026"
resume: "Nouveau flagship OpenAI annoncé le 3 sept. 2026, « built for the hardest end-to-end work ». Contraintes API dures : pas de reasoning effort none, pas de temperature/top_p custom, pas de logprobs, et tool calling réservé à la Responses API. Livré avec async tool calling, mid-turn steering WebSockets et changement d'effort mid-conversation préservant le cache. Pricing et benchmarks encore non confirmés en source primaire."
aliases:
  - "GPT-6 Astra"
  - "GPT-6"
  - "gpt-6-astra"
  - "Astra OpenAI"
  - "OpenAI Astra"
derniere-maj: 2026-09-05
auteur: claude
type: modele
sources:
  - "https://developers.openai.com/api/docs/changelog"
  - "https://www.cnbc.com/2026/09/03/open-ai-astra-gpt-6-cyber.html"
tags:
  - "#type/modele"
  - "#domaine/openai"
  - "#domaine/modeles"
---

# GPT-6 Astra

> Annoncé le **3 septembre 2026** au changelog API officiel. Verbatim : *« our most capable model, built for the hardest end-to-end work »*.

## Contraintes API — confirmé source primaire

Ce sont les faits les plus actionnables : Astra **retire** des leviers disponibles sur les générations précédentes.

| Contrainte | Détail |
|---|---|
| Reasoning effort | **Le niveau `none` n'est pas supporté** |
| Sampling | **Pas de `temperature` ni `top_p` custom** |
| Observabilité | **Pas de log probabilities** |
| Tool calling | **Responses API obligatoire** — les utilisateurs de Chat Completions doivent migrer |
| Sécurité | Livré avec un **monitoring asynchrone de désalignement** |

## Nouveaux contrôles Responses API (livrés avec Astra)

Destinés au travail agentique longue durée :

- **Async tool calling** — le modèle continue de travailler pendant que l'application exécute les outils.
- **Mid-turn steering via WebSockets** — de nouvelles instructions peuvent être envoyées *pendant* la génération d'une réponse.
- **Changement de reasoning effort en cours de conversation**, en préservant les remises de prompt caching.

## Disponibilité

Déploiement par phases (source presse, crédit moyen) : les entreprises du programme cybersécurité sur candidature d'OpenAI en premier, puis ChatGPT Plus/Pro/Business/Enterprise, l'API OpenAI et AWS *« in the coming days »*. Sam Altman décrit Astra comme un *« new capability level »*.

## ⚠️ Non confirmé en source primaire

Les éléments suivants circulent chez des trackers tiers et **n'ont pas été vérifiés sur une page de pricing ou de doc OpenAI**. À reconfirmer avant tout usage décisionnel :

- Pricing rapporté : **$10 / M input · $50 / M output**, cached input $1/M (−90 %). Requêtes au-delà de 272K tokens d'input facturées 2× input/cache et 1,5× output.
- Contexte rapporté : **1 050 000 tokens**, output max 128 000.
- Benchmarks rapportés : FrontierMath Tier 4 à 97,6 % · ARC-AGI-3 à 99,9 % (harness provider-adapter OpenAI) · ExploitBench 100 % · MRCR v2 8-needle 100 % (bande 256K–512K) et 96,3 % (bande 512K–1M).

## Codex

Aucun changement de modèle par défaut détecté : Codex CLI reste sur `gpt-5.6-sol`. Un support de configuration d'Astra aurait été ajouté en v0.153.2 (source tierce, non confirmée). Voir [[OpenAI Codex]].

## Lecture croisée — convergence frontier de septembre 2026

Astra et [[Fable 5.1]] sortent à 48 h d'intervalle avec un profil remarquablement proche : même tier de prix affiché ($10/$50), contexte du même ordre (~1M), output max identique (128K). Les deux livrent aussi le **même mouvement produit** : la possibilité de **changer le niveau d'effort en cours de conversation sans invalider le cache de prompt** (Responses API côté OpenAI, `/effort` sur Fable 5.1 côté Claude Code v2.1.260). Le raisonnement devient un curseur qu'on module pendant la tâche, plus un réglage figé au lancement.

## Liens

- [[GPT-5.6]] — génération précédente (Sol/Terra/Luna)
- [[GPT-5.5]] — flagship printemps 2026
- [[OpenAI Codex]] — CLI OpenAI
- [[Fable 5.1]] — flagship Anthropic sorti 2 jours plus tôt
- [[parametres-echantillonnage-llm]] — boutons de raisonnement par fournisseur
- [[MOC-Modeles]]
