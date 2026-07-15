---
titre: "Personnaliser ChatGPT (l'app, pas Codex) — instructions, Projects, mémoire, GPTs, connectors, API"
resume: "Note canonique forge — leviers réels de personnalisation de ChatGPT l'application (≠ Codex l'agent de code) : custom instructions, Projects (mémoire scopée), mémoire native 2 couches, GPTs, connectors/plugins, Assistants API (sunset 26 août 2026) → Responses API. PAS de hooks/AGENTS.md/skills au sens Codex. Provenance dégradée (403 WebFetch → paraphrase). Au 15 juil. 2026."
aliases:
  - "personnalisation chatgpt"
  - "chatgpt custom instructions"
  - "chatgpt projects memoire"
  - "chatgpt memoire native"
  - "custom gpts 2026"
  - "chatgpt connectors plugins"
  - "assistants api responses api sunset"
  - "chatgpt work agent"
derniere-maj: 2026-07-15
auteur: claude
type: technique
sources:
  - "help.openai.com (custom instructions, memory, projects, GPTs, connectors) — 403 WebFetch, contenu via WebSearch"
  - "https://developers.openai.com/api/docs/deprecations (Assistants API sunset)"
  - "9to5mac.com / Bloomberg / MacRumors 9 juil. 2026 (ChatGPT Work)"
tags:
  - "#type/technique"
  - "#domaine/openai"
  - "#domaine/chatgpt"
  - "#doctrine/2026"
---
# Personnaliser ChatGPT (l'app) — leviers réels

> Note canonique forge — la personnalisation de **ChatGPT l'application** (modèle/app grand public), à ne PAS confondre avec **Codex** l'agent de code. **Ici : PAS de hooks, PAS d'AGENTS.md, PAS de skills au sens Codex.** Les leviers sont : custom instructions, Projects, mémoire native, GPTs, connectors, API. Vérifié au **15 juil. 2026**.

> ⚠️ **PROVENANCE DÉGRADÉE — à lire.** `help.openai.com` et `openai.com/index/*` renvoient **403 à WebFetch**. Tout le contenu ci-dessous vient de **résumés WebSearch** (paraphrase moteur mêlant help center + presse tech). Les formulations entre guillemets sont **reconstituées, PAS du verbatim mot-à-mot**. Chiffres marqués *à vérifier*. Pour figer les strings et les chiffres, un accès authentifié (navigateur / MCP fetch) est nécessaire. Cette note est un **corpus court et honnête**, pas une référence de production.

---

## 1. Custom instructions (PROBABLE)

Instructions appliquées à **toutes les conversations**, éditables/supprimables, effet sur les conversations **futures** uniquement. Tous plans (Web/Desktop/iOS/Android). Limites *à vérifier* : ~1500 chars/champ, ~4500 total (perso), 8000 pour un Custom GPT. Pas d'API pour les custom instructions (utiliser les system messages en Chat Completions).

## 2. Projects (PROBABLE)

Espaces regroupant chats + fichiers + instructions. Les **instructions de projet surchargent les instructions globales**. Partageables en équipe (Business/Enterprise/Edu). Fichiers *à vérifier* : 5–40 selon plan, 512 MB/fichier. **Mémoire scopée par projet** : « project-only » (ne fuit ni vers le main chat ni vers d'autres projets) ou « default » ; un projet **partagé** est forcé en project-only (non réversible).

## 3. Mémoire native (PROBABLE)

Deux couches :
- **Reference saved memories** — faits discrets, éditables/supprimables individuellement, toujours pris en compte sauf suppression.
- **Reference chat history** — puise dans l'ensemble des conversations passées (contenu évolutif).

**Contrôle parent/enfant** (confirmé sur 2 articles help) : couper « Reference saved memories » **coupe aussi** « Reference chat history » ; l'inverse est possible (couper chat history seul). Réglages sous Settings → Personalization → Memory. Temporary Chat = sans mémoire. Supprimer une conversation ≠ supprimer la mémoire qui en dérive.

> « Dreaming V3 » (process de synthèse mémoire, revendiqué déployé le 4 juin 2026) = **claim purement tierce** (chatgptmemory.com / memx, NON OpenAI). **Ne pas capitaliser comme fait** — mentionné ici uniquement pour traçabilité, à confirmer en primaire.

## 4. GPTs (custom GPTs) — toujours d'actualité (PROBABLE)

Pleinement supportés en 2026. Builder web (Create conversationnel / Configure manuel : Name, Description, Instructions, Knowledge, Capabilities, Actions). Création réservée Plus+, browsing du GPT Store dès le Free. Knowledge *à vérifier* : jusqu'à 20 fichiers, 512 MB. Actions = connexion API externes ; « a GPT can use either apps or actions, but not both at the same time ».

## 5. Connectors → Plugin directory unifié (PROBABLE)

Connectors = tirer des fichiers de services externes (Google Drive, Gmail, SharePoint, Dropbox, Box… 15+ apps). Le **9 juil. 2026**, OpenAI a migré vers un **Plugin directory unifié** — « plugins are the primary way to discover workflow capabilities across ChatGPT and Codex ; a plugin can include skills, apps, and app templates ». Limite : recherche **une source à la fois**, keyword matching (pas sémantique).

## 6. API — Assistants vs Responses (PROBABLE→CERTAIN, 3+ sources)

**Assistants API dépréciée, arrêt dur le 26 août 2026** (annoncé le 26 août 2025). Remplacée par **Responses API** (+ Conversations API). Mapping : Assistants→Prompts, Threads→Conversations, Runs→Responses, Run Steps→Items. → Pour la perso/état programmatique côté OpenAI, c'est **Responses + Conversations API**, pas Assistants.

## 7. ChatGPT Work (agent, 9 juil. 2026 — presse)

Agent ChatGPT avec Codex intégré : prend un objectif, rassemble l'info sur les apps connectées, découpe en étapes, exécute en background sur des heures. @-mention de services (Slack/Teams/Drive/SharePoint) via le Plugin directory. L'ancienne app → « ChatGPT Classic » ; Codex devient la nouvelle app desktop. Propulsé par GPT-5.6. **Pertinence perso** : c'est un agent d'**exécution** — la personnalisation qu'il exploite reste celle des sections 1–5 (il n'introduit pas de nouveau levier de mémoire documenté).

---

## Ce que ChatGPT-app N'A PAS (vs Codex)

Pas de `AGENTS.md`, pas de `config.toml`/profils, pas de hooks, pas de `codex exec`, pas de subagents TOML. Les Skills existent côté produit (via plugins) mais la mécanique d'agent de code (sandbox, délégation TOML, CI) est **Codex**, pas ChatGPT-app. Arbitrage : [[codex-vs-chatgpt-seul]].

---

## SOURCES

- `help.openai.com` (custom instructions / memory / projects / GPTs / connectors) — **403 WebFetch, contenu via WebSearch** (paraphrase).
- `developers.openai.com/api/docs/deprecations` — Assistants API sunset 26 août 2026 (convergent 3 sources).
- Presse ChatGPT Work : 9to5mac / Bloomberg / MacRumors, 9 juil. 2026.

---

## WIKILINKS

- [[codex-vs-chatgpt-seul]] — quand utiliser Codex vs ChatGPT-app
- [[memoire-optimale-codex-chatgpt]] — montage mémoire cross-tool
- [[OpenAI Codex]] — l'agent de code (fiche produit)
- [[workflow-codex-optimal]] — le versant Codex
