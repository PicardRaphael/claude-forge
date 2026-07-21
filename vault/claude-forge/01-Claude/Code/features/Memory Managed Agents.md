---
titre: "Memory for Claude Managed Agents — Architecture & Principes"
resume: "Memory = filesystem monté dans l'agent. Permission scopes (read-only org-wide + read-write working), optimistic concurrency, version history, attribution metadata. Public beta avril 2026. Opus 4.7 state-of-the-art file-based memory"
aliases:
  - "memory managed agents"
  - "claude memory api"
  - "agent memory"
  - "memory filesystem"
  - "memory anthropic"
  - "managed agents memory"
type: feature
derniere-maj: 2026-07-21
auteur: claude
sources:
  - "https://www.youtube.com/watch?v=RtywqDFBYnQ"
  - "https://claude.com/code-with-claude/session/sf-memory-and-dreaming-for-self-learning-agents"
tags:
  - "#type/feature"
  - "#domaine/claude-code"
  - "#domaine/agents"
---

## Contexte

Présenté par **Mahesh Murag** (PM Platform, Anthropic) à Code with Claude SF, 6 mai 2026. Memory = primitive suivante après MCP, harnesses (Claude Code, Agent SDK) et Skills.

## Architecture — 3 couches

| Couche | Rôle |
|--------|------|
| **Storage** | Où les données sont stockées, métadonnées, attribution |
| **Structure & Content** | Memory modélisée comme filesystem + Skills comme mémoire procédurale |
| **Process** | Fréquence de mise à jour, triggers, sources de décision → c'est ici qu'intervient [[Dreaming Managed Agents]] |

## Principes de design

### 1. Memory = filesystem
Pas un tool call spécifique — Claude gère un filesystem de fichiers avec hiérarchie et format. Il utilise bash et grep pour lire, écrire, organiser. Opus 4.7 est state-of-the-art en file-based memory : meilleur discernement de quoi retenir, meilleure structure.

### 2. Permission scopes
- **Read-only** : mémoire org-wide (runbooks, best practices, SLO guidelines)
- **Read-write** : working memory spécifique à la tâche, fréquemment mise à jour

### 3. Optimistic concurrency
Hash de contenu avant overwrite — un agent vérifie qu'il ne va pas écraser la mémoire d'un autre agent. Critique pour les systèmes multi-agents (100s-1000s d'agents parallèles).

### 4. Version history + attribution
Audit log complet : quel agent a fait quelle modification, quand, dans quelle session. Rollback possible. Accessible aux agents eux-mêmes pour suivre l'historique.

### 5. Standalone API
API portable hors managed agents — PII scanning, cleanup pipelines, clonage vers systèmes externes.

## Résultats early adopters

- **Rakuten** : -97% first-pass errors, -27% coût, -34% latence avec memory
- **Netflix** : carry context across sessions, corrections human-in-the-loop persistées
- **Harvey** : +6% completion rate avec Dreaming

## Pattern SRE démontré

1. Agent SRE 1 reçoit alerte P1 → investigue → écrit findings dans memory store
2. Même alerte page à nouveau → Agent SRE 2 lit la mémoire → short-circuit l'investigation → gain immédiat tokens + intelligence

## Pertinence pour forge-brain

Notre vault Obsidian + MCP = une implémentation du même pattern :
- `vault/` = filesystem memory
- `04-Techniques/`, `Knowledge/erreurs/` = read-only org-wide knowledge
- `0-Inbox/context-actuel.md` = working memory
- git + CHANGELOG = version history
- MCP forge-brain = standalone API

**Gap identifié** : pas de process "dreaming" automatique (cross-session pattern detection, verification, deduplication).

## Liens

- [[Dreaming Managed Agents]] — Process de review/enrichissement automatique
- [[Managed Agents]] — Feature Managed Agents
- [[MOC-Claude-Code]]

---

## AJOUT 16 juin 2026 — Corrections + détails primaires (platform.claude.com)

> Vérifié sur [platform.claude.com/docs/en/managed-agents/memory](https://platform.claude.com/docs/en/managed-agents/memory.md) (16 juin). Précise/corrige le corps rédigé d'après la présentation orale du 6 mai.

### Mécanique réelle (primaire)

- **Montage** : le memory store (workspace-scoped, docs texte) est monté dans le sandbox sous **`/mnt/memory/`** ; l'agent l'édite avec ses file tools.
- **Permission scopes — correction** : il n'y a **PAS** de couche « read-only org-wide » système. Chaque store a un accès **`read_write` (défaut) ou `read_only`** (enforced filesystem). Le modèle « 2 couches » (référentiel partagé + working memory) s'obtient en **attachant plusieurs stores** à la session (un read_only partagé + un read_write par user/projet), pas via une hiérarchie native.
- **Optimistic concurrency** : précondition `content_sha256` sur `memories.update` (confirme le « hash avant overwrite » du corps).
- **Version history** : chaque mutation = version immuable `memver_...`, **rétention 30 jours** (les plus récentes toujours gardées), redactable (PII/GDPR).
- **Beta header** : `managed-agents-2026-04-01`. Setup : `POST /v1/memory_stores` → seed `POST .../memories` → attacher dans `resources[]` à la **création** de session (`access`, `instructions` ≤ 4096 chars) — uniquement à la création.
- **Caps** : **2000 memories/store**, **100 kB/memory**, **8 stores/session**.

### Modèle « state-of-the-art » — à élargir

Le corps dit « Opus 4.7 state-of-the-art file-based memory ». Depuis, **Opus 4.8** est le flagship et Dreaming supporte aussi `opus-4-8` (cf [[technique-dreaming-cross-session]] AJOUT 16 juin). Ne pas figer sur 4.7.

### Chiffres early adopters — prudence

« Rakuten -97% first-pass errors » : **non confirmé en primaire** (page client Rakuten = 79% time-to-market). Voir le détail dans [[technique-dreaming-cross-session]] § AJOUT 16 juin. Traiter le 97% comme à confirmer.

### Vaults ≠ Memory (ne pas confondre)

Côté Managed Agents, les **Vaults** (`vlt_...`) stockent des **credentials** par end-user (`mcp_oauth`/`static_bearer`/`environment_variable`, substitué à l'egress — l'agent ne voit jamais la vraie valeur), PAS de la mémoire. Les **scheduled deployments** (cron) ne persistent PAS le contexte entre runs par défaut → la persistance s'obtient en attachant des memory stores dans `resources[]`.

`derniere-maj` → 2026-06-16.


---

## AJOUT 21 juillet 2026 — Talk AI DevCon by Tessl : « Productionising memory » (Lamis, Applied AI Anthropic)

> Source primaire : talk AI DevCon by Tessl (Londres, 2026 — vidéo native X partagée le 19 juil. 2026, transcrite Whisper + slides analysées en session forge). Speakeuse : **Lamis** (nom de famille non capté), Member of Technical Staff, équipe **Applied AI** (entre research, product et GTM ; travaille avec startups/founders). ~31 min. La présentation publique la plus détaillée à date de l'architecture Memory + Dreaming.

### L'évolution de la mémoire agent — framing canonique en 4 stades

| Stade | Mécanisme | Apport | Limite découverte |
|---|---|---|---|
| 1. `CLAUDE.md` | single file injecté en début de session | « **unreasonably effective** » (verbatim) pour steerer | context bloat quand le fichier grossit |
| 2. Memory tool | `memory_read()/write()/edit()` — l'agent gère sa mémoire **in-band** | l'autonomie d'écriture marche très bien | reste dans le contexte de la session |
| 3. Skills | mémoire **procédurale**, progressive disclosure (frontmatter seul chargé) | détail profond sans surcharger le contexte — analogie « bibliothèque : je scanne les titres, je sors le dictionnaire de français quand on me parle français » | curation encore pilotée par l'humain |
| 4. **Memory = filesystem** | dossier `memory/` en markdown, lu/écrit par les agents avec bash/grep | state of the art — pas d'outils dédiés opinionated, la recherche filesystem EST la progressive disclosure | bottlenecks de production (ci-dessous) |

3 learnings distillés : (1) markdown = super format de lecture ; (2) laisser grossir la mémoire MAIS donner des outils d'indexation/recherche ; (3) autonomie aux agents en écriture.

### Les 3 bottlenecks de production (slides « Bottleneck 01-03 »)

1. **Continual learning — « Intelligence alone doesn't compound »** : cold start (chaque tâche repart de zéro), domain-specific (ce qui rend un agent brillant chez toi ne sort pas d'un modèle plus gros), no compounding (sans mémoire, la tâche 50 ne vaut pas mieux que la tâche 1).
2. **Productionising memory** : concurrent writes (plusieurs agents écrivent le même fichier), lost attribution (qui a écrit — toi ou l'agent — et quand ?), stale & mixed scopes (savoir org et notes de travail s'emmêlent).
3. **Memory over time — « In-band memory reaches its limits »** : **split focus** (l'agent divise son attention entre finir la tâche et curer la mémoire — « a very difficult optimization problem »), **patterns obfuscated** (un agent ne voit jamais les patterns cross-sessions/cross-agents — « it has a new context window in each of those »), **memories go stale** (doublons qui se contredisent, notes périmées « confidently wrong »).

### Principes de production (détail mécanique au-delà de la doc)

- **Versioning** : chaque write attribué à un auteur + une session + un timestamp ; full history inspectable + rollback. Exemple slide : `team/deploy.md` v1→v4, `written by sesn_011Ca7x`, contenu « Deploy via make ship, not ./deploy.sh. Reason: user corrected this on PRs #412, #418, #431 » — la mémoire porte sa propre provenance.
- **Concurrence — boucle hash-retry** (verbatim mécanique) : hash à la lecture → draft de l'édit → re-hash avant write → mismatch ⇒ l'agent **re-pull la mémoire, redrafte, re-tente le commit**. « Living in the harness, not the model » — la précondition est déterministe, pas confiée au modèle.
- **Permissioning** : org-wide knowledge (soigneusement curé) = **read-only** pour les agents ; scratchpad/working memory propre = read-write. Risque explicite : un agent qui écrirait une erreur dans le contexte org-wide → « that would scale to all of your agents and be pretty disastrous ».
- **⚠️ Memory poisoning par prompt injection** (risque nommé dans le talk) : une mémoire peut être « written incorrectly or even **maliciously injected** by someone trying to prompt inject your agents to write bad things to memory » → guardrails obligatoires sur l'écriture. À croiser avec [[agents-securite]] (le vault forge est exactement cette surface).
- **Portability** : la curation est l'actif → mémoire = fichiers + clean API standalone, accessible cross-surfaces.

### Résultats en production (slide « What teams see with memory »)

| Claim | Attribution slide (anonymisée) |
|---|---|
| **97% fewer first-pass errors** + « 27% lower cost and 34% lower latency, and learning stays under our control » | GM, AI for Business — Global commerce platform (cohérent Rakuten, non nommé) |
| **30% faster verification** (mémoire cross-session sur pipeline de vérification documentaire) | Head of Machine Learning — Document-AI platform |
| « Memory lets us stop building memory infrastructure and focus on the product itself » | Founder — early-stage AI startup |

→ Le « 97% » (flaggé « à confirmer » le 16 juin) est désormais attesté comme **slide officielle Anthropic** — toujours anonymisé, mais plus une rumeur secondaire. Cf [[technique-dreaming-cross-session]].

### Q&A — verbatims utiles

- « Vous réinventez les bases de données ? » → réponse : on cherche la **frontière autonomie agent vs programmatique** ; « we have enough signal now to know that those things should just be done in a very **deterministic way** » — les primitives éprouvées (hash, versions, permissions) **se codifient dans le harness**, pas dans le modèle. Convergence directe avec la doctrine forge [[raisonnement-22mai-doctrine-vs-enforcement]] (advisory vs déterministe).
- Produit : versioning/hashing/dreaming = exactement la **Memory & Dreaming API des Managed Agents** (« if you did want an out-of-box solution, that is where I would point you »).
- Dreaming × permissions : composables — on **choisit les transcripts attachés** au dreaming job pour matcher le permission set du memory store cible.
- **Pas spécifique au code** : « I use memory all the time when I'm producing presentations » (préférences de style, slides).

### Takeaways officiels (slide de clôture)

1. **Do the simple thing that works** — un bon CLAUDE.md + skills bien définies + mémoire écrite par les agents « already get you a long way ».
2. **Design for many, long-running agents** — permissioning, versioning, concurrency, portability.
3. **Add dreaming to consolidate memory out of band** — verify, organise, enrich entre les sessions.

### Trois takeaways appliqués à forge

Le chantier cognition forge (curator MCP, canonical cognition store, juillet 2026) implémente déjà : single-writer (≈ concurrence), séparation canonique/working (≈ permissioning), MCP standalone (≈ portability). Gap résiduel identique au diagnostic de mai : pas de dreaming pass automatisé cross-session — l'équivalent local reste `/done` + `vault-audit` manuels.
