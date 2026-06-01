---
titre: "NotebookLM — guide de maîtrise power-user 2026"
resume: "Guide actionnable NotebookLM 2026 : Studio 4 tuiles, Audio/Video Overviews + 4 formats + customisation, Configure Chat (auditor mode), living documents Drive, sync Gemini bidirectionnel, quotas 6 tiers vérifiés sources Google."
aliases:
  - "notebooklm"
  - "notebook lm"
  - "google notebooklm"
  - "notebooklm power user"
  - "audio overview personnalisé"
  - "notebooklm studio"
  - "notebooklm 2026"
domaine: outils-veille
type: technique
derniere-maj: 2026-06-01
auteur: claude
sources:
  - "https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-video-overviews-studio-upgrades/"
  - "https://workspaceupdates.googleblog.com/2026/03/new-ways-to-customize-and-interact-with-your-content-in-NotebookLM.html"
  - "https://support.google.com/notebooklm/answer/16213268?hl=en"
  - "https://support.google.com/notebooklm/answer/16179559?hl=en"
  - "https://support.google.com/notebooklm/answer/16212820?hl=en"
  - "https://workspaceupdates.googleblog.com/2026/05/keep-your-sources-up-to-date-with-automatic-Drive-syncing-in-NotebookLM.html"
  - "https://blog.google/innovation-and-ai/products/gemini-app/notebooks-gemini-notebooklm/"
tags:
  - "#type/technique"
  - "#domaine/veille"
  - "#casquette/responsable-ia"
---

# NotebookLM — guide de maîtrise power-user 2026

> Recherche web multi-agents (5 axes, 24 sources, vérification adversariale 3 votes/claim — 13 findings confirmés, 2 réfutés). Sources majoritairement primaires Google. État au 1er juin 2026.

## Description

NotebookLM 2026 n'est plus un simple assistant d'étude : c'est un **environnement de recherche, synthèse et production de contenu** ancré sur tes propres sources (RAG stateless, cf [[RAG]]). La maîtrise tient à **3 leviers** : (1) la profondeur de customisation des outputs Studio, (2) le pilotage du Chat par persona/instruction, (3) la curation rigoureuse des sources.

## Le panneau Studio — 4 tuiles

Layout 2026 : **Sources (gauche) / Chat (centre) / Studio (droite)**, fini le tab-flipping. Studio expose **4 tuiles** : Audio Overviews, Video Overviews, Mind Maps, Reports. Nouveauté clé : **plusieurs outputs du même type par notebook** (ex. plusieurs Audio Overviews en différentes langues) — l'ancienne limite « un seul de chaque » a sauté. Multi-tâche possible (écouter l'audio en explorant la Mind Map).

`Reports` est un **conteneur** regroupant Briefing Docs, Study Guides, FAQs et Timelines.

## Audio Overviews — la fonction « personnalisé »

C'est le bouton « personnalisé / Customize » que tu vois à la génération. **4 formats** :

| Format | Description |
|---|---|
| **Deep Dive** (défaut) | 2 hôtes IA en conversation animée |
| **The Brief** | 1 seul intervenant, points clés en < 2 min |
| **The Critique** | 2 hôtes évaluant de façon constructive un essai/doc |
| **The Debate** | 2 hôtes en débat formel contradictoire |

Customisation : **prompt libre** (« concentre-toi sur le chapitre 4 », « niveau expert »), **longueur** Shorter/Default/Longer (anglais seulement), **80+ langues** de sortie.

**Mode interactif** : tu rejoins l'audio **à la voix**, poses une question, les hôtes répondent depuis tes sources puis reprennent. Contraintes : **anglais uniquement**, seulement sur les overviews **nouvellement générés**, **pas inclus dans les versions partagées/téléchargées**.

## Video Overviews

Format initial = **slides narrées** : un hôte IA génère les visuels et tire images, diagrammes, citations et chiffres de tes documents. Customisable par sujet, objectifs d'apprentissage, audience (novice → expert).

**Cinematic Video Overviews** (mars 2026) : vidéos immersives, animations fluides, Gemini prend des centaines de décisions structurelles/stylistiques. Idéal récits complexes & recherche académique. **Anglais seulement au lancement.** Les Video Overviews standard supportent 80 langues.

> ⚠️ Réfuté en vérification : l'idée que les Cinematic seraient réservés à des tiers payants précis (vote 1-2). Ne pas l'affirmer.

## Slides

Feedback **slide par slide** (stylistique ou factuel), régénération dans Studio, **export PPTX** (en plus du PDF). Caveats : les révisions ne re-consultent pas les sources, le PPTX exporté est en couches d'images, ajout/suppression de slide non supporté.

## Configure Chat — le levier prompting (mode auditeur)

3 styles conversationnels : **Default** (recherche/brainstorm), **Learning Guide** (pédagogique), **Custom**. Le style **Custom accepte une instruction libre jusqu'à 10 000 caractères** (« Réponds comme un doctorant », « Joue un maître de jeu de rôle »). C'est le cœur du prompting avancé et du **mode auditeur** :

> **Hack auditeur** : au lieu de résumer, force NotebookLM à vérifier *« ce qui MANQUE, où les sources font des hypothèses, où elles se contredisent »*. Levier pour découvrir ce qu'on ne sait pas.

Caveat source : l'app mobile peut avoir des limitations ; les requêtes trop créatives peuvent être refusées.

## Gestion des sources

- **Types** : PDF, Google Docs/Slides/Sheets, URLs web, texte, YouTube, audio, EPUB.
- **Living documents** : les Docs/Sheets/Slides issus de Drive se **resynchronisent automatiquement** (quelques minutes, zéro config) quand l'original change — fini le re-sync manuel. Suppressions et révocations de permission strictement appliquées. (S'applique aux fichiers Drive, pas à tout type de source — les PDF restent statiques.)
- **Curation** : la qualité des insights est directement liée à la qualité des sources. Fusionner les fichiers liés pour réduire le nombre de sources (attention à la précision de retrieval sur très gros fichiers), n'uploader que le pertinent.

## Intégration Gemini cross-notebook

Les sources se **synchronisent bidirectionnellement** entre les Notebooks de l'app Gemini et NotebookLM : une source ajoutée d'un côté apparaît de l'autre. **Mais** Video Overviews et Infographics restent **exclusifs à NotebookLM** (raison d'ouvrir le notebook dans NotebookLM). ⚠️ Sync bidirectionnelle pour les **sources uniquement**, pas symétrique pour tous les objets : les notebooks NotebookLM partagés ne sont pas visibles dans Gemini ; les chats Gemini apparaissent comme sources en lecture seule.

## Quotas par tier (vérifiés support Google, mai-juin 2026)

6 tiers : Standard (free) / Plus / Pro / Ultra 20TB / Ultra 30TB / Enterprise.

| Limite | Standard | Plus | Pro | Ultra 20TB | Ultra 30TB |
|---|---|---|---|---|---|
| **Sources / notebook** | 50 | 100 | 300 | 500 | 600 |
| **Notebooks / user** | 100 | 200 | 500 | 500 | 500 |
| **Chats / jour** | 50 | 200 | 500 | 2 500 | 5 000 |
| **Audio Overviews / jour** | 3 | 6 | 20 | 100 | 200 |
| **Video Overviews / jour** | 3 | 6 | 20 | 100 | 200 |
| **Deep Research** | 10/**mois** | 3/jour | 20/jour | 75/jour | 200/jour |

Particularités : Audio = Video (mêmes plafonds). **Deep Research** est le seul à passer d'un quota **mensuel** (free) à **journalier** (payant). Cinematic Video Overviews ont un **sous-plafond plus bas séparé** (10/j Ultra-20TB, 20/j Ultra-30TB ; indisponible Free/Pro). Enterprise = quota notebooks décrit qualitativement (« 5X ou plus »).

> ⚠️ Réfuté : l'idée que les payants reçoivent « exactement 5× plus » sur toutes les métriques (vote 1-2). Faux — les ratios varient par métrique.

## Quand utiliser

- **Synthèse rapide d'un corpus** (rapport, FAQ, briefing) sans chunking manuel → Reports.
- **Apprendre un sujet en mobilité** → Audio Overview Deep Dive + mode interactif.
- **Présentation exec** → Video Overview (audience « novice ») ou Slides → export PPTX.
- **Audit de sources contradictoires** → Configure Chat Custom en mode auditeur.
- **Veille sur sources vivantes** (docs Neoteem évolutifs) → sources Drive + living documents.
- Pour la veille IA continue : intégrer au pipeline [[index|hub veille responsable-ia]].

## Caveats généraux

Les quotas sont **très volatils** (split Ultra 20TB/30TB post-Google I/O mai 2026) : vérifier `support.google.com/notebooklm/answer/16213268` avant de s'appuyer sur des chiffres exacts. Plusieurs restrictions « anglais seulement » (longueur audio, mode interactif, Cinematic) pourraient avoir sauté depuis (Google signale « more soon »).

## Liens

- [[RAG]] — NotebookLM = synthèse RAG stateless (contraste wiki cumulatif Karpathy)
- [[index|Hub veille IA responsable-ia]] — intégrer au pipeline signal → action
- [[Gemini CLI]] — autre produit Google, écosystème Gemini
