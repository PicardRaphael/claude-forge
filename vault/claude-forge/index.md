---
titre: "Index vault forge-brain — orientation LLM"
resume: "Index content-oriented Karpathy : par concepts/erreurs/canoniques pour permettre au LLM de trouver une note en 1 saut, pas via les MOCs en 3 sauts. Catalogue navigable, pas table des matières exhaustive — l'exhaustif vit dans les _index de sous-dossiers."
aliases:
  - "index vault"
  - "index forge-brain"
  - "vault index"
  - "orientation LLM vault"
  - "karpathy index content-oriented"
derniere-maj: 2026-06-09
auteur: claude
type: index
tags:
  - "#type/index"
  - "#karpathy/index"
---

# Index vault forge-brain

> Pattern Karpathy LLM Wiki : index **content-oriented** (par concepts), pas sommaire généré (par dossiers). Le LLM trouve une note en 1 saut. **Cet index est un catalogue navigable, pas un dump des 480 notes** — pour l'exhaustif d'un sous-domaine, suivre le `_index` du dossier concerné.

---

## Si tu cherches "comment faire X" — notes canoniques (source de vérité actionnable)

Produit au chantier 22 mai 2026, vit dans `04-Techniques/claude-code/` :

- **Comment écrire un CLAUDE.md** → [[comment-ecrire-claudemd]] (target 200L, 5 anti-patterns Anthropic)
- **Comment créer une skill** → [[comment-creer-skill]] (9 catégories Thariq, < 500L, description 1 ligne)
- **Comment créer un agent** → [[comment-creer-agent]] (Sonnet/Opus split, 8 couleurs, 2-agent Justin Young)
- **Comment créer un hook** → [[comment-creer-hook]] (29 events officiels, doctrine 22 mai lint/sécu/scope)
- **Workflow Claude Code optimal** → [[workflow-claude-code-optimal]] (routines Boris, advisor strategy Brad Abrams, leaf nodes Erik)
- **Analyser un repo et proposer config CC** → [[methode-analyser-repo]] (MÉTA, 6 étapes, ORDRE CANONIQUE A→B→C→D→E)
- **Pivoter une doctrine sans drift résiduel** → [[methode-pivoter-doctrine]] (checklist 5 étapes, 23 mai)
- **MCP vs Skills vs Bash (quand quoi)** → [[mcp-vs-skills-doctrine]] (MCP data / Skills how-to / Bash exploration)
- **Pattern vault LLM Karpathy** → [[pattern-vault-llm-karpathy]] (3-layers, 3 ops, 2 fichiers oblig. + drift réel mesuré 8 juin)
- **Pattern STOP + ESCALADE sub-agents** → [[anti-reentrance-sub-agents-pattern-escalade]] (sub-agent non-réentrant)
- **Comparaison skill Anthropic claude-code-setup** → [[comparaison-skill-anthropic-claude-code-setup]]
- **Setup entreprise sécu publique** → [[trail-of-bits-config]]

---

## Si tu cherches un PATTERN technique — `04-Techniques/patterns/` + `claude-code/`

### Vault / MCP / mémoire
- [[mcp-vault-llm-design]] — design canonique MCP LLM-optimized (9 ops, forge-brain v1.4)
- [[architecture-cerveau-obsidian-mcp]] — architecture cerveau Obsidian + MCP, standard qualité
- [[comparaison-mcp-forge-brain-vs-mcp-brain-28mai2026]] — audit 14 critères, verdict A (forge mieux conçu)
- [[pattern-fts5-aliases-vs-embeddings]] — pourquoi BM25+alias FR plutôt que vectoriel
- [[pattern-maintenance-hybride-corpus-accumulatif]] — 3 acteurs (MEMORY/vault/feedback), seuils, dormants
- [[mcp-alias-ambigu-chemin-exact]] — stem ambigu (log/index/CHANGELOG) → chemin exact
- [[vault-edit-gotchas-outillage]] — 3 gotchas écriture vault (delegate-guard, insert_section, SQLite désync)
- [[pattern-mcp-brief-then-direct]] — brief MCP verbatim in-body (skills frontmatter ignorées cross-repo)
- [[pattern-vault-source-unique-sync-mecanique]] · [[pattern-vault-query-guard]]
- [[limite-mcp-lock-inter-ecritures]] · [[limite-mcp-lag-reindexation-agregats]] — limites MCP connues + triggers

### Spec / dev / workflow
- [[pattern-spec-driven-development]] · [[pattern-sdd-triangle]] · [[pattern-github-spec-kit]] · [[pattern-gsd-framework]]
- [[running-implementation-notes]] — notes d'implémentation Thariq (4 sections)
- [[pattern-spec-skill-deployment]] · [[workflow-args-array-gotcha]] (Dynamic Workflow array → undefined)
- [[bug-caracterise-fix-trivial-vs-couteux]] · [[context-drift-throw-vs-patch]]
- [[programmatic-tool-calling]] · [[pre-compute-vs-inference-loops-boris]] · [[concevoir-loops-travail]]

### Audit / config multi-repo
- [[audit-claude-folder-pattern]] · [[audit-tripartite-doctrinal-pattern]] (Boris/Will/ECC)
- [[config-guardian-pattern]] · [[quartet-analyse-multi-repo]] · [[codebase-maps-pattern]]
- [[hooks-conformite-audit-passif-continu]] · [[pattern-behavioral-dispatch-test]]
- [[resolution-path-3-contextes]] · [[mcp-paths-relatifs-portabilite]]

### Design / intégration
- [[pattern-figma-mcp-claude-code]] — Figma MCP + Claude Code

---

## Si tu cherches doctrine arbitrée — pivot 22 mai 2026 + suites

Le 22 mai 2026, doctrine inversée : hooks pour lint/security/scope, **JAMAIS** workflow agentique.

- **Doctrine vs enforcement (pivot fondateur)** → [[raisonnement-22mai-doctrine-vs-enforcement]]
- **Kill TDD strict hooks** → [[raisonnement-kill-tdd-strict-hooks-mai-2026]]
- **Revirement pipeline (long → court)** → [[raisonnement-revirement-pipeline-mai-2026]]
- **Doctrine vivante (méta)** → [[doctrine-vivante]]
- **Effort calibré par type de tâche** → [[effort-opus-47-doctrine-anthropic-2026]]
- **Anti-pattern hookify / workflow hooks** → [[anti-pattern-hookify-workflow-hooks]]
- **Critique chantier 22 mai 8 canoniques** → [[critique-2026-05-22-8-canoniques-chantier]]
- **Décisions d'architecture raisonnées** → [[Knowledge/raisonnements/_index]] (hook maison vs plugin, mémoire portable, niveaux de mesure agents, byte-for-byte splice…)

---

## Si tu cherches "ne pas refaire l'erreur" — `Knowledge/erreurs/` (39 incidents)

**Index complet** → [[Knowledge/erreurs/_index]]. Garde-fous réflexes les plus structurants :

### Hooks / settings
- [[erreur-hooks-workflow-enforcement]] — workflow hooks = anti-pattern (pivot 22 mai)
- [[erreur-hooks-bash-quoting-windows]] — bash heredoc cassé Windows
- [[erreur-auto-mode-classifier-self-modification]] — hard block `.claude/settings.json`
- [[erreur-settings-paths-hardcodes-multi-poste]] · [[erreur-deny-global-ecrase-allow-projet]]
- [[erreur-hook-garde-hors-vault-bloque-plan-file]] · [[erreur-subagent-bypass-delegate-guard]]

### MCP / vault
- [[erreur-mcp-stopwords-semantiques]] — NLTK FR 153 stop words cassent la recherche
- [[erreur-mcp-yaml-dump-corruption]] — yaml.dump corrompt le frontmatter
- [[erreur-password-postgres-clair-mcp-json]] — JAMAIS secret en clair
- [[erreur-vault-jamais-consulte-session-principale]] — réflexe vault d'abord (raté fine-tuning)

### Skills / agents / capitalisation
- [[erreur-edit-direct-skills]] — délégation skill-creator obligatoire
- [[erreur-skill-monolithique-sans-references]] — < 500L + references/
- [[e-descriptions-keyword-stuffing]] · [[erreur-emphasis-overtriggering]] — description trigger, pas stuffing
- [[erreur-seuils-canoniques-agents-inventes-2026-05-22]] — seuls CLAUDE.md<200 / SKILL.md<500 canoniques
- [[erreur-capitalisation-ex-post-23-24mai]] — capitaliser en direct, pas ex-post

### DA / advisor / vérification
- [[erreur-devils-advocate-tronque]] — résultat DA tronqué = relancer
- [[erreur-deploy-sans-advisor-da-cwc2026]] — advisor + DA AVANT
- [[erreur-tests-heureux-vs-adverses]] — tests adverses obligatoires sur code destructif
- [[agents-ia-22-claims-fausses-2026-05-23]] · [[erreur-audit-rag-11-faux-2026-05-23]] — vérifier claims, sources primaires

---

## Si tu cherches "qui a dit quoi" — Leaders (80 fiches, 6 sous-domaines)

### Équipe Claude Code / Anthropic
- [[Boris Cherny]] — créateur CC, compounding error-driven · [[cat-wu]] — Head of Product CC+Cowork
- [[Erik Schluntz]] — vibe coding in prod (leaf nodes) · [[Thariq Shihipar]] — 9 catégories skills
- [[lisa-crofoot]] · [[angela-jiang]] (advisor strategy) · [[justin-young]] (2-agent) · [[Noah Zweben]]
- [[daisy-hollman]] · [[jeremy-hadfield]] (Dreaming) · [[Lydia Hallie]] · [[Alex Albert]] · [[Brad-Abrams]]
- [[affaan-mustafa-ecc-hackathon-winner]] — pattern personal dev setup ECC

### Agents / harness
- [[Andrej Karpathy]] — LLM Wiki, agentic engineering, chez Anthropic 19 mai 2026
- [[martin-fowler]] — Guides+Sensors · [[hashimoto]] / [[Mitchell-Hashimoto]] — harness engineering, AGENTS.md
- [[addy-osmani]] — harness engineering · [[Simon Willison]] — lethal trifecta
- [[Andrew Ng]] · [[Harrison Chase]] · [[Lilian Weng]] · [[Jim Fan]] · [[Shunyu Yao]] (ReAct) · [[Yohei Nakajima]]

### RAG · Fine-tuning · Prompt · Industrie
- RAG : [[Douwe Kiela]] · [[Omar Khattab]] (DSPy) · [[Jerry Liu]] · [[Nils Reimers]] · [[Han Xiao]] · [[Greg Kamradt]]
- Fine-tuning : [[Tim Dettmers]] (QLoRA) · [[Edward Hu]] (LoRA) · [[Tri Dao]] (FlashAttention) · [[Sebastian Raschka]] · [[Daniel Han]] · [[Maxime Labonne]]
- Prompt : [[Amanda Askell]] · [[Jason Wei]] (CoT) · [[Denny Zhou]] · [[Riley Goodside]] · [[Sander Schulhoff]]
- Industrie : [[Dario Amodei]] · [[Sam Altman]] · [[Demis Hassabis]] · [[tobi-lutke]] (qmd) · [[Arthur Mensch]] · [[Chip Huyen]]

---

## Si tu cherches une feature/news Claude Code — `01-Claude/`

- **Changelog** : [[CC juin 2026 - v2.1.160 ultracode]] · [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] · [[CC mai 2026 - Code with Claude]] · [[CC avril 2026]]
- **Features** : [[Agent Teams]] · [[Managed Agents]] · [[Dreaming Managed Agents]] · [[Cowork GA]] · [[auto-mode-classifier]] · [[MCP Tunnels]] · [[Self-Hosted Sandboxes]] · [[Session Sharing]]
- **Best practices** : [[delegate-guard-pattern]] · [[context-management]] · [[agents-color-convention]] · [[hook-intercepte-mcp-et-read-tools]] · [[mcp-vs-cli-vs-skills]]
- **Deprecations** : [[Deprecation Sonnet 4 Opus 4]] · [[Deprecation 1M Context Beta]] · [[Deprecation Haiku 3]] · [[Deprecation budget_tokens]]
- **Cowork** : [[cowork-architecture]] · [[cowork-skills-reliability]] · [[cowork-write-vault-headless-impossible]]

---

## Si tu cherches "comment configurer le forge"

- [[claude-forge]] — contexte projet · [[forge-brain-proactive]] — rule MCP forge-brain proactif
- [[delegate-guard-pattern]] — hook PreToolUse forge-only · [[audit-claude-folder-pattern]] — audit `.claude/` d'un repo
- [[methode-analyser-repo]] — séquence A→B→C→D→E pour proposer une config CC

---

## Navigation par dossier (ontologie utilité — Eliott Meunier Prisme One)

- `00-Hub/` — MOCs classiques (8 notes)
- `01-Claude/` — features, deprecations, best-practices CC + Cowork (35)
- `02-Concurrents/` — ChatGPT, Codex, Gemini CLI, Cursor (5)
- `03-Modeles/` — specs Opus 4.8, Gemini 3, GPT-5 (7)
- `04-Techniques/` — RAG, agents, fine-tuning, prompt, patterns, claude-code (133)
- `05-Leaders/` — personnes clés, 6 sous-domaines (80)
- `06-Industrie/` — funding, events, acquisitions (9)
- `07-Prompts/` — system prompts, techniques prompting (7)
- `1-Projets/` — contexte projets stables (28)
- `2-Casquettes/` — aires de vie, dont responsable-ia (46)
- `Knowledge/` — mémoire compounding : erreurs, critiques, raisonnements, synthèses, questions, reviews, evolutions (103)
- `raw/` — sources immuables (Karpathy layer 1) : web research, transcripts, papers (8)
- `Templates/` — Templates Templater · `Archive/` — notes archivées

---

## Schéma vault

- Conventions vault → [[SCHEMA]]
- Log append-only Karpathy → [[log]]
- Changelog narratif → [[CHANGELOG]]

---

## Métadonnées vault (au 9 juin 2026, source `vault_stats`)

- **480 notes** · **3193 wikilinks** · **2790 aliases** · **204 tags**
- **MCP** : `mcp__forge-brain__*` (port 8091, FTS5 SQLite, BM25 pondéré file_stem:10 / aliases:8 / content:1)
- **Pattern** : Karpathy LLM Wiki (3-layers raw/wiki/schema) — drift d'implémentation mesuré et arbitré le 8 juin (cf [[pattern-vault-llm-karpathy]] section REQUALIFICATION POST-MESURE)
- **Doctrine pivot** : 22 mai 2026 (hooks lint/security/scope, JAMAIS workflow agentique)
- **Retrieval** : BM25 lexical + alias expansion FR assumé (vectoriel écarté à la mesure : ratage réel 0,89% non-sémantique)
