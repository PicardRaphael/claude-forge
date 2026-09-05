---
titre: "Catalogue Gemini — quels modèles existent vraiment, et lesquels sont morts"
resume: "État vérifié au 5 sept. 2026 du catalogue Gemini : série 3 stable jusqu'à 3.8 Flash, 3.1 Pro encore en preview, 3.5 Pro toujours « Coming soon », Gemini 4.0 sans date annoncée (le vault affirmait à tort qu'il avait été annoncé à l'I/O du 19 mai — c'était Gemini 3.5 Flash). Quatre modèles shut down. Note catalogue unique, volontairement pas une fiche par modèle."
aliases:
  - "catalogue Gemini"
  - "modèles Gemini"
  - "Gemini 3.8 Flash"
  - "Gemini 3.1 Pro"
  - "Gemini 3.5 Pro"
  - "Gemini 4.0"
derniere-maj: 2026-09-05
auteur: claude
type: modele
sources:
  - "https://ai.google.dev/gemini-api/docs/models"
  - "https://deepmind.google/models/gemini/"
  - "https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/"
tags:
  - "#type/modele"
  - "#domaine/google"
  - "#domaine/modeles"
---

# Catalogue Gemini

> **Pourquoi une note catalogue et pas une fiche par modèle.** Google publie beaucoup de variantes Flash à cadence rapide, dont aucune n'est promptée au quotidien côté forge. Ce qui est utile ici est de savoir *qui existe, qui est mort, et où en est la prochaine génération* — pas d'entretenir huit fiches de specs. Une fiche dédiée ne se justifiera que pour un modèle Gemini réellement mis en production.

## Série 3 — stable au 5 septembre 2026

| Modèle | Note |
|---|---|
| **Gemini 3.8 Flash** | Le plus récent. Verbatim : *« engineered for long-horizon software engineering, autonomous agents »* |
| Gemini 3.7 Flash | Stable |
| Gemini 3.6 Flash | Stable |
| Gemini 3.5 Flash | Annonce phare de Google I/O 2026 (19 mai). Dépasserait Gemini 3.1 Pro sur les benchmarks coding/agentique/multimodal, ~4× plus rapide en tokens/s que d'autres modèles frontier |
| Gemini 3.5 Flash-Lite | Stable |
| Gemini 3.1 Flash-Lite | Stable |

Modèles image : **Nano Banana 2** (`gemini-3.1-flash-image`) et **Nano Banana Pro** (`gemini-3-pro-image`).

## Les trois modèles que le vault attendait

| Modèle | Statut réel au 5 sept. 2026 |
|---|---|
| **Gemini 3.1 Pro** | **Preview**, pas GA — `gemini-3.1-pro-preview`. ⚠️ `deepmind.google` l'affiche comme « Available » tandis que `ai.google.dev` le marque preview : les deux référentiels ne sont pas synchronisés, **la doc API fait foi pour l'intégration** |
| **Gemini 3.5 Pro** | Toujours **« Coming soon »**. Le vault l'attendait vers le 17 juillet 2026 — le report a de nouveau glissé |
| **Gemini 4.0** | **Aucune date de sortie annoncée.** Le pré-entraînement aurait démarré fin juillet 2026 (call résultats Q2 du 21 juillet, source tierce à reconfirmer) |

## ⛔ Correction d'une erreur factuelle du vault

Jusqu'au 5 septembre 2026, [[MOC-Modeles]] et [[Gemini CLI]] affirmaient : *« Gemini 4.0 — Annoncé Google I/O 19 mai 2026 »*.

**C'est faux.** Les annonces officielles de l'I/O 2026 portaient sur **Gemini 3.5 Flash**, Gemini Omni (génération vidéo), Gemini Spark (agent personnel) et l'AI Mode motorisé par 3.5 Flash. Aucune mention de Gemini 4.0. L'erreur consistait vraisemblablement à confondre 3.5 et 4.0, ou à dater 4.0 sur cet événement.

Leçon de méthode : une ligne « X attendu à l'événement Y » vieillit mal. Passé l'événement, elle devient une assertion active fausse si personne ne la relit — ici pendant près de quatre mois.

## Dépréciations — vérifié source officielle

| Modèle | Statut |
|---|---|
| Gemini 2.0 Flash (`gemini-2.0-flash`) | **Shut down** |
| Gemini 2.0 Flash-Lite | **Shut down** |
| Gemini 3.1 Flash-Lite Preview | **Shut down** |
| Gemini 3 Pro Preview (`gemini-3-pro-preview`) | **Shut down** |
| Imagen 4 | Déprécié |

Politique annoncée : **au moins 2 semaines de préavis** avant retrait d'un modèle.

## Optimisation

Le bouton de raisonnement Gemini est **`thinking_level`** (`minimal`/`low`/`medium`/`high`, support variable selon modèle), qui remplace `thinkingBudget`. Sans réglage explicite, *« Gemini models engage in dynamic thinking… automatically adjusting the amount of reasoning effort based on the complexity of the request »*.

⚠️ Sur **Gemini 3.x**, ne pas toucher au sampling — verbatim : *« we strongly recommend keeping them at their default values for Gemini 3.x models. Changing these parameters (for example, setting the temperature below 1.0) can cause unexpected behavior »*. C'est la seule dépréciation de technique explicitement formulée par un fournisseur lors du scan du 5 sept. 2026.

Détail cross-fournisseur : [[parametres-echantillonnage-llm]].

## Outillage

Gemini CLI n'est plus servi pour les comptes individuels depuis le 18 juin 2026 ; remplacé par Antigravity CLI et Antigravity 2.0. Détail et nuances : [[Gemini CLI]].

## Liens

- [[Gemini CLI]] — statut de l'outillage et transition Antigravity
- [[Gemma 4]] — modèles open-source Google
- [[parametres-echantillonnage-llm]] — `thinking_level` et sampling par fournisseur
- [[MOC-Modeles]]
