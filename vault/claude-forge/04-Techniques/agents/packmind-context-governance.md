---
titre: "Packmind — Gouvernance de contexte pour agents de codage IA"
resume: "Packmind (ex-Promyze, PackmindHub/packmind, Apache 2.0) capture les standards de code d'une équipe et les rend en CLAUDE.md/.cursor/rules/AGENTS.md depuis une source unique, avec versioning + détection de drift. Industrialise le single-source→multi-agent que la forge fait à la main."
aliases:
  - "Packmind"
  - "packmind.com"
  - "Promyze"
  - "PackmindHub"
  - "context engineering coding agents"
  - "gouvernance standards code IA"
domaine: ia
type: technique
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://github.com/PackmindHub/packmind"
  - "https://packmind.com/"
  - "https://packmind.com/how-it-works/"
  - "https://packmind.com/promyze-now-becomes-packmind/"
  - "https://news.ycombinator.com/item?id=45836219"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/agents"
---

## Description

**Packmind** (ex-**Promyze**, rebranding janvier 2024 ; repo `PackmindHub/packmind`, Apache 2.0) = plateforme de **capitalisation, versioning et diffusion des standards de code d'une équipe**, repositionnée autour d'un angle précis : **transformer ces standards en contexte gouverné pour les agents de codage IA** (Claude Code, Cursor, GitHub Copilot, Gemini Code Assist, OpenAI/AGENTS.md).

- Société **française** (Bordeaux), fondée 2016, ~1 M$ seed (rapporté). Lien Promyze→Packmind **confirmé** (même medium, même org GitHub historique, page officielle de rebrand).
- Thèse : chaque assistant IA part d'un snapshot de contexte différent (fichiers d'instructions périmés, wikis stale) → du code « localement correct mais globalement incohérent ». **Le problème n'est pas la génération mais la gouvernance du contexte.**

> [!tip] Croisement direct avec la doctrine forge (valeur Jarvis)
> Packmind **industrialise exactement ce que la forge fait à la main** : single source of truth → rendu multi-agent + versioning + détection de drift, propagé entre ia_back / neo_ia / neoteem-back-ts (cf rule `cross-repo-propagation.md` et `single-source-truth-vault-canonique`). Leur règle *« 25 mots max, verbe d'action, scope par pattern de fichier »* est l'équivalent externe et chiffré de [[comment-ecrire-claudemd]] / [[comment-creer-hook]] (scope par matcher). À surveiller comme alternative outillée si la propagation cross-repo manuelle devient un goulot.

## Comment ça marche — Capture → Version → Distribute → Govern

1. **Capture** — (a) importer l'existant (ADRs, docs Git/Wiki) ou (b) capturer en session via le **serveur MCP**. `/packmind-onboard` scanne un repo et génère jusqu'à 5 standards + 5 commands depuis les patterns réels (plutôt qu'inventer des règles).
2. **Version** — chaque modif de standard = version tracée, horodatée, attribuable. On sait quelle version de quelle règle était active quand un code a été généré.
3. **Distribute** — **génération automatique du format propre à chaque outil depuis une source unique** (le cœur du produit). Routage par repo/sous-dossier (monorepo via `packmind.json`).
4. **Govern / Enforce** — *« un linter sous stéroïdes »* : détecte le **drift** entre code généré et standards, remonte les violations dans l'IDE / CLI / agent, mesure adoption et conformité.

**Formats générés par cible** : Claude Code (`CLAUDE.md` et/ou `.claude/rules/`, commands, skills) · Cursor (`.cursor/rules/*.mdc`) · Copilot (`.github/copilot-instructions.md`) · OpenAI (`AGENTS.md`) · Kiro (`.kiro/steering/`).

**Serveur MCP — confirmé et central** : `{PACKMIND_URL}/mcp` (token requis), permet aux agents de créer/gérer les standards directement. CLI `packmind-cli init` → `/packmind-onboard` ; la CLI **fetch le contexte et ouvre une PR** qui rafraîchit les fichiers d'instructions.

## Quand utiliser (leur propre grille de décision)

| Situation | Reco |
|---|---|
| Dev solo, 1 projet | Fichiers natifs suffisent — un bon `CLAUDE.md` à la main couvre le besoin |
| Équipe 3-10, 1-2 agents | **Ruler** (OSS, sync multi-agents) suffit |
| Entreprise, multi-équipes / multi-repos / besoin d'audit | **Packmind** — cycle de vie complet (capture + version + distribute + drift) |

**Honnêteté notable** : Packmind admet que pour 1 agent + 1 repo + conventions stables, les fichiers natifs maintenus à la main suffisent. Point de bascule = 2e agent, 2e équipe, ou besoin d'auditabilité.

**vs linter (ESLint)** : un linter corrige du code **existant** (réactif) ; Packmind façonne ce que l'agent **génère avant** écriture (préventif). Complémentaire, pas substitut.

## Optimisation (recommandé par Packmind)

- Règles **courtes** (~25 mots), commençant par un **verbe d'action** (Use / Avoid / Prefer).
- Exemples **positifs ET négatifs** dans le langage cible.
- **Scoper par pattern de fichier** (`*.spec.ts` ne se déclenche que sur les tests) → anti-bruit.
- Onboarding auto (`/packmind-onboard`) plutôt qu'inventer.
- Faire vivre : versioning + dashboard de distribution + linter de conformité.

## Maturité

- **OSS** `PackmindHub/packmind`, Apache 2.0, TypeScript 99 %, monorepo Nx. **~295 ⭐**, 60 releases, dernière **v1.15.1 (15 juin 2026)** — projet actif mais audience GitHub modeste.
- Cœur OSS gratuit ; éditions payantes = enforcement, gouvernance, SSO/SCIM, RBAC. Déploiement cloud (`app.packmind.ai`) ou self-hosted (Docker/K8s).
- **Faible signal externe** : Show HN ~nov. 2025 = 1 point / 2 commentaires. Chiffres marketing (« 65 % des commits par IA ») non recoupés. Acteur **prometteur mais early-stage côté notoriété**, crédible côté produit (rebrand cohérent d'un acteur de 2016, OSS réel et actif).

## Réservations (non vérifié)

- Format Claude Code exact : divergence interne `CLAUDE.md` vs `.claude/rules/`.
- Intégration revue de code (forte chez Promyze) non détaillée dans les pages Packmind actuelles.

## Liens

- [[comment-ecrire-claudemd]] — doctrine CLAUDE.md (équivalent forge des « standards »)
- [[comment-creer-hook]] — scope par matcher = équivalent du scope par pattern de fichier
- [[memoire-agent-mem0]] · [[memoire-agent-langmem]] — mem0 expose aussi des Agent Skills
- [[MOC-Techniques]]
