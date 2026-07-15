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
