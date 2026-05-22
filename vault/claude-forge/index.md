---
titre: "Index vault forge-brain — orientation LLM"
resume: "Index content-oriented Karpathy : par concepts/erreurs/canoniques pour permettre au LLM de trouver une note en 1 saut, pas via les MOCs en 3 sauts."
aliases:
  - "index vault"
  - "index forge-brain"
  - "vault index"
  - "orientation LLM vault"
  - "karpathy index content-oriented"
derniere-maj: 2026-05-22
auteur: claude
type: index
tags:
  - "#type/index"
  - "#karpathy/index"
---

# Index vault forge-brain

> Pattern Karpathy LLM Wiki : index **content-oriented** (par concepts), pas sommaire genere (par dossiers). Le LLM trouve une note en 1 saut.

---

## Si tu cherches "comment faire X" — 8 notes canoniques

Source de verite actionnable produite 22 mai 2026 dans `04-Techniques/claude-code/` :

- **Comment ecrire un CLAUDE.md** → [[comment-ecrire-claudemd]]
- **Comment creer une skill** → [[comment-creer-skill]] (9 categories Thariq)
- **Comment creer un agent** → [[comment-creer-agent]] (Sonnet/Opus split, 8 couleurs)
- **Comment creer un hook** → [[comment-creer-hook]] (25+ events reels, doctrine 22 mai)
- **Workflow Claude Code optimal** → [[workflow-claude-code-optimal]] (routines Boris, advisor Angela Jiang)
- **Analyser un repo et proposer config CC** → [[methode-analyser-repo]] (META 6 etapes)
- **MCP vs Skills (quand quoi)** → [[mcp-vs-skills-doctrine]]
- **Pattern vault LLM Karpathy** → [[pattern-vault-llm-karpathy]]
- **Setup entreprise secu publique** → [[trail-of-bits-config]]

---

## Si tu cherches doctrine arbitree — pivot 22 mai 2026

Le 22 mai 2026, doctrine inversee : hooks pour lint/security/scope, **JAMAIS** workflow agentique.

- **Doctrine vs enforcement (pivot)** → [[raisonnement-22mai-doctrine-vs-enforcement]]
- **Kill TDD strict hooks** → [[raisonnement-kill-tdd-strict-hooks-mai-2026]]
- **Revirement pipeline (long → court)** → [[raisonnement-revirement-pipeline-mai-2026]]
- **Critique chantier 22 mai 8 canoniques** → [[critique-2026-05-22-8-canoniques-chantier]]

---

## Si tu cherches "ne pas refaire l'erreur" — Knowledge/erreurs

20 incidents documentes. Avant d'agir, chercher si l'erreur existe deja :

### Erreurs hooks / settings
- [[erreur-hooks-workflow-enforcement]] — Anti-pattern workflow hooks
- [[erreur-hooks-bash-quoting-windows]] — Bash heredoc bug Windows
- [[erreur-settings-paths-hardcodes-multi-poste]] — Settings paths multi-poste
- [[erreur-claude-agent-env-var-dead-code]] — CLAUDE_AGENT env var inutile
- [[erreur-auto-mode-classifier-self-modification]] — Hard block .claude/settings.json

### Erreurs MCP / vault
- [[erreur-mcp-stopwords-semantiques]] — NLTK FR 153 stop words fucked search
- [[erreur-mcp-yaml-dump-corruption]] — yaml.dump corruption frontmatter
- [[erreur-password-postgres-clair-mcp-json]] — JAMAIS secret en clair MCP json
- [[erreur-vault-before-specialist-ttl-scope]] — TTL marker workflow = anti-pattern

### Erreurs skills / agents
- [[erreur-edit-direct-skills]] — Delegation skill-creator obligatoire
- [[erreur-skill-monolithique-sans-references]] — < 500L + references/
- [[e-descriptions-keyword-stuffing]] — Description trigger, pas stuffing
- [[erreur-stop-critique-position-gotcha-fin]] — Critique < ligne 25
- [[erreur-architect-neo_ia-fouille-bdd]] — Scope agent boundary
- [[erreur-advisory-rules-insuffisantes]] — Advisory = compliance partielle

### Erreurs DA / advisor
- [[erreur-devils-advocate-tronque]] — Resultat DA tronque = relancer
- [[erreur-da-heredoc-bash-silencieux]] — Heredoc Bash silencieux
- [[erreur-deploy-sans-advisor-da-cwc2026]] — Toujours advisor+DA AVANT
- [[erreur-tests-heureux-vs-adverses]] — Tests adverses obligatoires
- [[erreur-pipeline-trop-long-frustration]] — Pipeline > 30min CRUD = anti-pattern

---

## Si tu cherches "qui a dit quoi" — Leaders Anthropic 2026

### Equipe Claude Code Anthropic
- [[Boris Cherny]] — Createur CC, compounding error-driven, "coding is solved"
- [[cat-wu]] — Head of Product CC+Cowork, +200% PRs/eng org
- [[lisa-crofoot]] — Research PM, "scaffolding holds Claude back"
- [[angela-jiang]] — Claude Platform, advisor strategy 5x cost reduction
- [[Erik Schluntz]] — Co-fondateur, Vibe Coding in Prod (PM/leaf/human/checkpoints)
- [[Thariq Shihipar]] — 9 categories skills, 3-way trade-offs
- [[Noah Zweben]] — +300% PRs equipe Anthropic 3 mois
- [[justin-young]] — MTS, two-agent architecture canonique
- [[daisy-hollman]] — "Beyond the Basics" London
- [[jeremy-hadfield]] — Dreaming feature research preview
- [[Lydia Hallie]] — CC workshops
- [[Alex Albert]] — Head of Claude Relations

### Agents / Harness
- [[Andrej Karpathy]] — LLM Wiki, agentic engineering, chez Anthropic 19 mai 2026
- [[martin-fowler]] — Guides+Sensors, "Agent = Model + Harness"
- [[addy-osmani]] — Harness Engineering, +21.8 pts Forge vs CC
- [[hashimoto]] — Origine "harness engineering", AGENTS.md
- [[Simon Willison]] — Lethal trifecta (juin 2025)
- [[tobi-lutke]] — CEO Shopify, createur qmd

---

## Si tu cherches "comment configurer le forge"

- [[claude-forge]] — Contexte projet
- [[forge-brain-proactive]] — Rule MCP forge-brain proactif
- [[delegate-guard-pattern]] — Hook PreToolUse forge-only
- [[audit-claude-folder-pattern]] — Audit `.claude/` d'un repo

---

## Navigation par dossier

- `00-Hub/` — MOCs (Modules of Content) classiques
- `01-Claude/Code/` — Features, deprecations, best-practices Claude Code
- `02-Concurrents/` — ChatGPT, Codex, Gemini CLI, Cursor
- `03-Modeles/` — Specs GPT-5, Gemini 3, Claude 4.7
- `04-Techniques/` — RAG, agents, fine-tuning, prompt engineering, patterns
- `05-Leaders/` — Personnes cles (claude-code, agents, fine-tuning, prompt, industrie)
- `06-Industrie/` — News funding, events, acquisitions
- `07-Prompts/` — System prompts, techniques prompting
- `1-Projets/` — Contexte projets stables
- `2-Casquettes/` — Aires de vie
- `Knowledge/` — Memoire compounding (erreurs, critiques, raisonnements, syntheses, questions, reviews)
- `raw/` — Sources immuables (Karpathy layer 1) : web research, transcripts, papers
- `Templates/` — Templates Templater
- `Archive/` — Notes archivees

---

## Schema vault

- Convention vault → [[SCHEMA]]
- Log append-only → [[log]]
- Changelog narratif → [[CHANGELOG]]

---

## Metadonnees vault

- **318+ notes** (post chantier 22 mai)
- **MCP** : `mcp__forge-brain__*` (port 8091, FTS5)
- **Pattern** : Karpathy LLM Wiki (3-layers : raw/wiki/schema)
- **Doctrine pivot** : 22 mai 2026 (hooks lint/security/scope, JAMAIS workflow)
