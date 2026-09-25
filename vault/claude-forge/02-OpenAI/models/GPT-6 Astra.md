---
titre: "GPT-6 Astra — flagship OpenAI du 3 septembre 2026"
resume: "Nouveau flagship OpenAI annoncé le 3 sept. 2026, « built for the hardest end-to-end work ». Contraintes API dures : pas de reasoning effort none, pas de temperature/top_p custom, pas de logprobs, et tool calling réservé à la Responses API. Prix confirmé en primaire le 25 sept. : $10/$50 (cache $1), contexte 1,05M, output 128K, tarif ×2 input / ×1,5 output sur toute la requête au-delà de 272K tokens d'entrée. Défaut bundled de Codex CLI en 0.153.4 (4 sept.) ; depuis la sortie de GPT-6 Sol/Luna (22 sept.), la doc Codex ne nomme plus de défaut fixe. Benchmarks non confirmés en primaire."
aliases:
  - "GPT-6 Astra"
  - "GPT-6"
  - "gpt-6-astra"
  - "Astra OpenAI"
  - "OpenAI Astra"
derniere-maj: 2026-09-25
auteur: claude
type: modele
sources:
  - "https://developers.openai.com/api/docs/models/gpt-6-astra"
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

## Specs et prix — confirmé source primaire (25 sept. 2026)

Fiche modèle officielle `developers.openai.com/api/docs/models/gpt-6-astra` :

| Item | Valeur |
|---|---|
| Prix | **$10 / M input · $1 / M cached input · $50 / M output** |
| Long contexte | verbatim : *« Prompts exceeding 272K input tokens are priced at 2x input and cache rates and 1.5x output for the full request »* → $20 / $2 / $75 dès que l'entrée dépasse 272K |
| Contexte | **1 050 000 tokens** |
| Output max | **128 000 tokens** |
| Knowledge cutoff | 30 avril 2026 |
| Reasoning effort | `low` · `medium` · `high` · `xhigh` · `max` (pas de `none`) |
| Endpoints | Chat Completions, Responses et Batch marqués « Supported » ; Realtime, Assistants, fine-tuning non supportés |

⚠️ Le seuil de 272K porte sur **toute la requête** : dans un long run agentique (Codex), le contexte accumulé franchit vite ce seuil et le coût effectif passe au palier haut pour chaque tour suivant.

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

## Codex — défaut bundled en 0.153.4, plus de défaut nommé depuis Sol/Luna

Chronologie vérifiée au changelog Codex officiel (5 sept. 2026) :

| Version | Date | Verbatim |
|---|---|---|
| 0.153.1 | 3 sept. | *« Added support for configuring GPT-6-Astra through the API **without changing the default model** or showing it in the model picker »* |
| 0.153.2 | 3 sept. | *« Corrected the GPT-6-Astra Fast tier description to say '2x speed, increased usage' instead of '1.5x' »* |
| 0.153.3 | 4 sept. | *« Added GPT-6-Astra to the Amazon Bedrock model picker for Mantle and Runtime global/US routes »* |
| 0.153.4 | 4 sept. | *« Fixed Astra's visibility in the bundled model picker and **made it the bundled default when no model is explicitly configured** »* |

**État au 25 sept. 2026 — non tranché en primaire.** Après la sortie de **GPT-6 Sol et GPT-6 Luna** (22 sept., Codex CLI 0.156.x → 0.157.0), la page `learn.chatgpt.com/docs/models` ne nomme plus de modèle par défaut : *« If you don't specify a model, the ChatGPT desktop app, Codex CLI, or IDE extension uses a recommended model »*. Elle recommande Sol pour le coding agentique complexe et Luna pour le volume. Des sources tierces affirment que `gpt-6-sol` est devenu le défaut — non confirmé par le changelog ni la doc. Conséquence pratique : **épingler le modèle dans `~/.codex/config.toml`** si le choix compte, plutôt que dépendre d'un défaut qui a déjà changé deux fois en trois semaines. Voir [[OpenAI Codex]].

**Leçon de méthode** : sur un modèle en cours de déploiement, une assertion de type « X est le défaut » se périme en heures ou en jours. Ce genre de claim doit être daté précisément ou pas écrit du tout.

## ⚠️ Non confirmé en source primaire

- Benchmarks rapportés : FrontierMath Tier 4 à 97,6 % · ARC-AGI-3 à 99,9 % (harness provider-adapter OpenAI) · ExploitBench 100 % · MRCR v2 8-needle 100 % (bande 256K–512K) et 96,3 % (bande 512K–1M).
- Tiers « Power options » (Astra Light / Medium / Extra High, Sol Light, Terra Light) : rapportés par des trackers tiers, absents de la page modèles officielle.

## Lecture croisée — convergence frontier de septembre 2026

Astra et [[Fable 5.1]] sortent à 48 h d'intervalle avec un profil remarquablement proche : même tier de prix affiché ($10/$50), contexte du même ordre (~1M), output max identique (128K). Les deux livrent aussi le **même mouvement produit** : la possibilité de **changer le niveau d'effort en cours de conversation sans invalider le cache de prompt** (Responses API côté OpenAI, effort mid-conversation en beta côté Anthropic). Le raisonnement devient un curseur qu'on module pendant la tâche, plus un réglage figé au lancement.

## Liens

- [[GPT-5.6]] — génération précédente (Sol/Terra/Luna)
- [[GPT-5.5]] — flagship printemps 2026
- [[OpenAI Codex]] — CLI OpenAI
- [[Fable 5.1]] — flagship Anthropic sorti 2 jours plus tôt
- [[parametres-echantillonnage-llm]] — boutons de raisonnement par fournisseur
- [[MOC-Modeles]]
