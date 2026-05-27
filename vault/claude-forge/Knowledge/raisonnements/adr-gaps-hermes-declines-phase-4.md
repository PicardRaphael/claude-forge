---
titre: "ADR — Gaps Hermes Agent déclinés (Phase 4)"
resume: "Décision architecturale : gaps où Hermes Agent est supérieur mais non pertinents pour le use case synchrone de claude-forge. Chaque gap décliné a un déclencheur de réactivation."
aliases:
  - "adr gaps hermes declines"
  - "hermes gaps declined"
  - "decision hermes phase 4"
  - "gaps declines hermes"
  - "adr hermes"
derniere-maj: 2026-05-27
tags:
  - "#type/raisonnement"
  - "#projet/claude-forge"
  - "#concurrent/hermes"
---

# ADR — Gaps Hermes Agent déclinés (Phase 4)

Lien : [[phase-4-comparaison-hermes-roadmap]], [[methode-analyser-repo]], [[workflow-claude-code-optimal]]

## Statut

Accepté — 2026-05-27.

## Contexte

Audit code source Hermes Agent (Nous Research, 169 296 stars, MIT) vs claude-forge.
Source : `C:\temp\hermes-audit\HERMES_ARCHITECTURE.md`.

Critère de pertinence : claude-forge sert un use case **session synchrone** (mémoire et apprentissage parfaits, compounding). PAS l'agent autonome. Hermes est conçu pour l'autonomie multi-canal. Plusieurs de ses forces sont donc structurellement non pertinentes ici.

## Décision

Décliner les gaps suivants. Chaque décision est réversible via son déclencheur.

### 1. Triggers async (cron, chat 6 canaux, webhook)

- Hermes : `cron/scheduler.py`, `gateway/` (Telegram, Discord, Slack, WhatsApp, Signal, Email), webhooks.
- Pourquoi décliné : le use case est synchrone. Raphael travaille TOUJOURS en session avec Claude. L'orga bloque aussi GitHub cloud/triggers ([[feedback_no_github_cloud]]).
- Déclencheur de réactivation : si Raphael adopte un workflow asynchrone (laisser tourner la nuit, recevoir des notifications mobiles) → réévaluer un trigger local Task Scheduler.

### 2. Background review autonome (capitalisation sans validation)

- Hermes : `agent/background_review.py` fork LLM toutes les 10 itérations, écrit skills/mémoire SANS validation humaine, notification après coup.
- Pourquoi décliné : viole le principe forge "Raphael tranche" et "humain dans la boucle". Pas de diff, pas d'historique git de `~/.hermes/skills/`. Incompatible avec le contrôle/traçabilité du use case synchrone.
- Ce qu'on importe quand même (croisement) : la COUVERTURE (proposer des capitalisations) sans l'AUTONOMIE — voir gap A3 dans [[phase-4-comparaison-hermes-roadmap]] (enrichir /done pour PROPOSER, Raphael valide).
- Déclencheur de réactivation : si le volume de sessions devient ingérable manuellement ET que la traçabilité git peut être préservée (diff auto + approbation batch) → réévaluer un mode semi-auto.

### 3. Self-evolution GEPA

- Hermes : repo séparé `hermes-agent-self-evolution`, GEPA (mutation texte de prompts/skills, pas fine-tuning), POC Phase 1/5, manuel, humain valide via PR, hors runtime. 3 610 stars.
- Pourquoi décliné : POC non production-ready (4/5 phases planifiées), hors runtime, coût $2-10/run, ROI incertain pour 1 utilisateur. La mutation auto de prompts sans cadre = anti-doctrine forge (advisor/DA avant toute proposition majeure).
- Déclencheur de réactivation : si dspy.GEPA devient packagé stable ET intégrable au runtime ET que skill-evolve montre ses limites sur >50 skills → réévaluer une optim guidée par traces.

### 4. Skills Hub / registry public

- Hermes : Skills Hub (GitHub/agentskills.io/URL), taps `openai/skills` + `anthropics/skills`, format portable.
- Pourquoi décliné : claude-forge est mono-utilisateur. Pas de besoin de distribution/découverte publique. Les skills forge sont volontairement couplées à la doctrine forge.
- Déclencheur de réactivation : si claude-forge devient multi-utilisateur (équipe Neoteem) ou si on publie des skills sur l'Agent Skills Spec → réévaluer un format portable + registry.

### 5. Sécurité supply-chain (exact-pin deps)

- Hermes : pyproject.toml exact-pin + lazy-install (réponse documentée au worm Shai-Hulud).
- Pourquoi décliné : surface de dépendances différente. claude-forge a peu de deps Python (MCP forge-brain). Le risque supply-chain est marginal.
- Déclencheur de réactivation : si le MCP forge-brain accumule des deps tierces nombreuses → adopter exact-pin + lock.

### 6. Communauté / portabilité OS / onboarding tiers

- Hermes : 169k stars, install.sh, Linux/macOS/WSL2/Windows, docs site.
- Pourquoi décliné : projet personnel Windows-first assumé. Pas d'objectif d'adoption massive.
- Déclencheur de réactivation : si claude-forge est partagé comme template public ou onboarding équipe → réévaluer portabilité + doc d'onboarding.

## Conséquences

- claude-forge reste concentré sur sa thèse : mémoire/apprentissage/compounding/conformité en session synchrone, avec humain dans la boucle.
- Les 3 gaps RÉELS et pertinents (recherche transcripts, lifecycle skills, capitalisation proactive) sont traités dans le plan A de [[phase-4-comparaison-hermes-roadmap]], pas ici.
- Asymétrie assumée : Hermes gagne sur l'automatisation autonome, claude-forge sur le contrôle structuré. Ce n'est pas un déficit, c'est un choix de positionnement ([[feedback_pas_de_symetrie_artificielle_priorisation]]).
