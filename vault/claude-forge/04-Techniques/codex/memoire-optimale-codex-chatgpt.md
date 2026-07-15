---
titre: "Système de mémoire optimal — Codex ET ChatGPT (montage cross-tool)"
resume: "Note canonique forge — le meilleur montage mémoire selon l'outil : côté Codex (AGENTS.md règles durables + skills + [memories] auto + profils), côté ChatGPT-app (mémoire native 2 couches + Projects + custom instructions). Quelle brique pour quel type de savoir. Au 15 juil. 2026."
aliases:
  - "memoire codex chatgpt"
  - "systeme memoire optimal openai"
  - "memoire cross-tool codex"
  - "ou ranger le savoir codex"
  - "agents.md vs memories vs skills"
derniere-maj: 2026-07-15
auteur: claude
type: technique
sources:
  - "Synthèse des notes corpus Codex + personnalisation-chatgpt-app (sources primaires y figurent)"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#domaine/openai"
  - "#doctrine/2026"
---
# Système de mémoire optimal — Codex ET ChatGPT

> Note canonique forge — **où ranger chaque type de savoir** selon l'outil OpenAI. Note de synthèse : les faits et sources primaires vivent dans les notes-foyers (liées) — ici, l'**arbitrage**, pas la re-documentation. Au **15 juil. 2026**.

---

## Principe — la mémoire n'est pas un seul mécanisme

Comme côté Claude Code (CLAUDE.md ≠ mémoire ≠ vault), OpenAI a **plusieurs couches** avec des rôles distincts. Ranger un savoir dans la mauvaise couche = soit il dérive (règle durable mise en recall volatil), soit il sature (how-to dans AGENTS.md).

## Côté CODEX (agent de code)

| Type de savoir | Couche | Pourquoi | Foyer |
|----------------|--------|----------|-------|
| **Règles durables** du repo (conventions, commandes, review) | `AGENTS.md` | toujours chargé, nesté, cap 32 KiB | [[agents-md-codex]] |
| **Réglages machine** (modèle, sandbox, MCP) + variantes | `config.toml` + **profils** (1 fichier/profil) | par machine/projet, pas dans le prompt | [[config-toml-profils-codex]] |
| **How-to réutilisable** (procédures) | **Skills** (`.agents/skills`) | progressive disclosure, invocable | [[comment-creer-skill-codex]] |
| **Contexte récent / recall** (préférences, faits de sessions passées) | **`[memories]`** (auto, background) | recall layer, PAS la règle dure | [[loop-apprentissage-codex]] |
| **Enforcement 100 %** | Hooks (trust model) | déterministe | [[comment-creer-hook-codex]] |

**Le montage optimal Codex** : AGENTS.md porte les règles ; les skills portent le how-to ; `[memories]` capture le recall automatiquement ; une scheduled task « scan sessions → update skills » ferme la boucle de compounding (cf [[loop-apprentissage-codex]]). Règle d'or : **`[memories]` ne remplace jamais AGENTS.md/skills** — c'est un « recall layer, not the only source for rules that must always apply » (verbatim doc).

## Côté CHATGPT (l'app)

| Type de savoir | Couche | Foyer |
|----------------|--------|-------|
| **Directives permanentes** (ton, format, rôle) | Custom instructions | [[personnalisation-chatgpt-app]] |
| **Contexte d'un chantier** (fichiers, instructions scopées) | **Projects** (mémoire scopée project-only) | [[personnalisation-chatgpt-app]] |
| **Faits persistants + historique** | Mémoire native 2 couches (saved memories + chat history) | [[personnalisation-chatgpt-app]] |
| **Assistant packagé réutilisable** | Custom GPT (instructions + knowledge + actions) | [[personnalisation-chatgpt-app]] |

*(Tous les détails, chiffres et la mise en garde de provenance 403 sont dans la note-foyer — non répétés ici.)*

## Le montage cross-tool

- **Le savoir de CODE** (conventions repo, procédures dev, enforcement) vit côté **Codex** (AGENTS.md/skills/hooks) — versionnable, partagé équipe.
- **Le savoir de RÉFLEXION/rédaction** (préférences de ton, dossiers de travail, faits perso) vit côté **ChatGPT** (custom instructions/Projects/mémoire native).
- Pont : les **Skills** sont le format partagé (standard ouvert) qui peut transiter entre Codex et un client compatible — mais **pas byte-identique** (cf [[comment-creer-skill-codex]]).

---

## Mémoire GÉRÉE par l'utilisateur (au-delà du recall auto) — recherche 15 juil. 2026

La mémoire native `[memories]` est **délibérément non pilotable à la main** (doc verbatim : *« Treat these files as generated state... don't rely on editing them by hand as your primary control surface »* — `learn.chatgpt.com/docs/customization/memories`). `/memories` = toggles on/off, pas de write/pin/force. **Donc une mémoire qu'on gère, versionne et audite = une couche EXTERNE possédée, que Codex consomme — jamais les `[memories]` bidouillés** (Codex les régénère/écrase). C'est le pattern forge (vault + `/done`) transposé.

### Deux couches à ne jamais confondre

| Couche | Rôle | Leviers Codex | Éditable/versionné ? |
|--------|------|---------------|----------------------|
| **Règles durables** (instruction-memory) | conventions, décisions, procédures | AGENTS.md + Skills `.agents/skills` | OUI (fichiers versionnés) |
| **Épisodique contrôlé** (learned-memory) | ce qui s'est passé aux sessions passées | serveur MCP mémoire **OU** hook `Stop`/`PreCompact`→`SessionStart` câblé | OUI si couche externe possédée |

> Verbatim praticien (codex.danielvaughan.com, 1 mai 2026) : *« Instructions belong in version-controlled files. Learned knowledge belongs in a searchable memory store. Mixing them creates maintenance headaches. »* La contrainte liante n'est PAS l'infra mais le **jugement** (quoi retenir, quand mettre à jour).

### Options concrètes pour la couche épisodique externe

- **Serveur MCP mémoire** — stanza `[mcp_servers.<id>]` dans config.toml (`codex mcp add` = stdio only ; HTTP → config manuel). « Mémoire via MCP » n'est PAS une feature native nommée : c'est un serveur tiers qui expose `add_memory`/`search_memories`.
  - **mem0** : Option A plugin marketplace (apporte MCP + Skills + 6 hooks lifecycle pré-câblés : `SessionStart` load, `UserPromptSubmit` search, `Stop` store summary, `PreCompact` store) ; Option B MCP direct (pas de hooks/skills). Scopé `user_id` → store partagé Codex + Cursor + Claude Code. Source : `docs.mem0.ai/integrations/codex`.
  - **Basic Memory** : vault **markdown local = source de vérité**, éditable/versionnable, cross-tool via MCP. Le plus proche d'un « vault qu'on possède » (mais c'est un produit).
- **DIY zéro-dépendance** : AGENTS.md + hook `SessionStart` (Python stdlib) lisant un vault markdown local. Faisable (mécanismes confirmés) mais **le « serveur MCP mémoire maison » n'est documenté nulle part** — inférence, pas recette prouvée. Basic Memory est l'équivalent produit le plus proche.
- **Letta** (MemFS git-backed, blocs markdown versionnés, `/remember`) : intégration Codex **moins clé-en-main** (MCP cloud construit par la communauté) — *à vérifier* avant adoption.

### Arbitrages honnêtes — « la mémoire parfaite n'existe pas encore »

- **Portabilité** : mémoire MCP = portable cross-provider ; `[memories]` OpenAI ne l'est pas. `[memories]` = per-user, cloud-only, **pas de partage équipe**, indisponible EEA/UK/Suisse au lancement (→ AGENTS.md only là-bas).
- **Staleness** : un mauvais backend injecte du contexte périmé qui **dégrade** la sortie. Empiler natif + MCP sans `disable_on_external_context = true` = injection redondante qui brûle le budget tokens.
- **Cap silencieux** : AGENTS.md tronqué au-delà de 32 KiB sans alerte → ne pas en faire une « grosse mémoire ».
- **Problème non résolu (versioned reads)** : deux agents qui écrivent en concurrence → le plan de l'un périme celui de l'autre. Aucun produit ne le résout proprement au 15/07. C'est *pourquoi* la mémoire « parfaite » reste ouverte.

> Provenance : recherche 2 agents 15 juil. 2026 (classifieur sécu indisponible → citations vérifiées manuellement). Willison **silencieux sur la mémoire Codex spécifiquement** (son foyer self-updating memory = Jesse Vincent/Superpowers, côté Claude Code). OpenAI en interne : amélioration continue **humain-pilotée** (100+ skills publiés/copiés + AI review), pas de loop auto-édition.

## ANTI-PATTERNS

- ❌ **Mettre du how-to dans AGENTS.md** — cap 32 KiB, toujours chargé → skill.
- ❌ **Traiter `[memories]` comme la source des règles dures** — recall layer.
- ❌ **Confondre mémoire ChatGPT-app et `[memories]` Codex** — deux produits, deux mécanismes.
- ❌ **Dupliquer les faits ici** — cette note arbitre ; les faits vivent dans les foyers liés.

---

## WIKILINKS

- [[workflow-codex-optimal]] — note maître
- [[agents-md-codex]] · [[config-toml-profils-codex]] · [[comment-creer-skill-codex]] · [[comment-creer-hook-codex]] · [[loop-apprentissage-codex]] — foyers Codex
- [[personnalisation-chatgpt-app]] — foyer ChatGPT (facts + provenance)
- [[codex-vs-chatgpt-seul]] — l'arbitrage produit
- [[pattern-vault-llm-karpathy]] — la mémoire multi-couches côté forge (miroir conceptuel)
