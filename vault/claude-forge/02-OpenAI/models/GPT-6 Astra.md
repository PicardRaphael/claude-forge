---
titre: "GPT-6 Astra — flagship OpenAI du 3 septembre 2026"
resume: "Nouveau flagship OpenAI annoncé le 3 sept. 2026, « built for the hardest end-to-end work ». Contraintes API dures : pas de reasoning effort none, pas de temperature/top_p custom, pas de logprobs, et tool calling réservé à la Responses API. Livré avec async tool calling, mid-turn steering WebSockets et changement d'effort mid-conversation préservant le cache. Modèle par défaut de Codex CLI depuis la 0.153.4 (4 sept.). Pricing et benchmarks encore non confirmés en source primaire."
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
  - "https://learn.chatgpt.com/docs/changelog"
  - "https://learn.chatgpt.com/docs/models"
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

Déploiement par phases (source presse, crédit moyen) : les entreprises du programme cybersécurité sur candidature d'OpenAI en premier, puis ChatGPT Plus/Pro/Business/Enterprise, l'API OpenAI et AWS *« in the coming days »*. Sam Altman décrit Astra comme un *« new capability level »*. La doc modèles Codex précise que l'accès dépend du déploiement, de la méthode de connexion et du client utilisé.

## Codex — Astra est le modèle par défaut depuis le 4 septembre

⚠️ **Correction du 5 septembre 2026.** La première version de cette note affirmait « aucun changement de modèle par défaut détecté : Codex CLI reste sur `gpt-5.6-sol` ». C'était exact au soir du 3 septembre et **faux dès le lendemain** — le basculement a eu lieu en moins de 24 h, sur quatre versions publiées en deux jours. Chronologie vérifiée au changelog Codex officiel :

| Version | Date | Verbatim |
|---|---|---|
| 0.153.1 | 3 sept. | *« Added support for configuring GPT-6-Astra through the API **without changing the default model** or showing it in the model picker »* |
| 0.153.2 | 3 sept. | *« Corrected the GPT-6-Astra Fast tier description to say '2x speed, increased usage' instead of '1.5x' »* |
| 0.153.3 | 4 sept. | *« Added GPT-6-Astra to the Amazon Bedrock model picker for Mantle and Runtime global/US routes »* |
| 0.153.4 | 4 sept. | *« Fixed Astra's visibility in the bundled model picker and **made it the bundled default when no model is explicitly configured** »* |

Conséquence concrète : sur un Codex CLI à jour et sans configuration explicite de modèle, **c'est Astra qui répond**, avec ses contraintes API (pas de `temperature`/`top_p`, pas de reasoning effort `none`). Épingler `gpt-5.6-sol` dans `~/.codex/config.toml` reste possible et devient un choix délibéré, plus un défaut subi. Voir [[OpenAI Codex]].

**Leçon de méthode** : sur un modèle en cours de déploiement, une assertion de type « X n'a pas changé » se périme en heures, pas en semaines. Ce genre de claim doit être daté à l'heure près ou pas écrit du tout.

## ⚠️ Non confirmé en source primaire

Les éléments suivants circulent chez des trackers tiers et **n'ont pas été vérifiés sur une page de pricing ou de doc OpenAI**. À reconfirmer avant tout usage décisionnel :

- Pricing rapporté : **$10 / M input · $50 / M output**, cached input $1/M (−90 %). Requêtes au-delà de 272K tokens d'input facturées 2× input/cache et 1,5× output.
- Contexte rapporté : **1 050 000 tokens**, output max 128 000.
- Benchmarks rapportés : FrontierMath Tier 4 à 97,6 % · ARC-AGI-3 à 99,9 % (harness provider-adapter OpenAI) · ExploitBench 100 % · MRCR v2 8-needle 100 % (bande 256K–512K) et 96,3 % (bande 512K–1M).
- Tiers « Power options » (Astra Light / Medium / Extra High, Sol Light, Terra Light) : rapportés par des trackers tiers, absents de la page modèles officielle.

## Lecture croisée — convergence frontier de septembre 2026

Astra et [[Fable 5.1]] sortent à 48 h d'intervalle avec un profil remarquablement proche : même tier de prix affiché ($10/$50), contexte du même ordre (~1M), output max identique (128K). Les deux livrent aussi le **même mouvement produit** : la possibilité de **changer le niveau d'effort en cours de conversation sans invalider le cache de prompt** (Responses API côté OpenAI, effort mid-conversation en beta côté Anthropic). Le raisonnement devient un curseur qu'on module pendant la tâche, plus un réglage figé au lancement.

## Liens

- [[GPT-5.6]] — génération précédente (Sol/Terra/Luna)
- [[GPT-5.5]] — flagship printemps 2026
- [[OpenAI Codex]] — CLI OpenAI, dont Astra est désormais le défaut
- [[Fable 5.1]] — flagship Anthropic sorti 2 jours plus tôt
- [[parametres-echantillonnage-llm]] — boutons de raisonnement par fournisseur
- [[MOC-Modeles]]
