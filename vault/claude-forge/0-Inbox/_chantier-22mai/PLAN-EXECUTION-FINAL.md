---
titre: "PLAN EXÉCUTION FINAL — Refonte vault forge-brain chantier 22 mai 2026"
resume: "Référence unique pour exécuter la refonte vault forge-brain après recherche exhaustive — doctrine arbitrée, notes à créer/supprimer, standard parfait, corrections d'attribution, verbatim canoniques"
aliases:
  - "plan execution final chantier 22 mai"
  - "plan refonte vault forge brain"
  - "reference unique chantier 22 mai"
  - "doctrine arbitree forge mai 2026"
derniere-maj: 2026-05-22
auteur: claude
type: plan
status: a-executer
tags:
  - "#type/plan"
  - "#projet/forge"
  - "#chantier/22mai2026"
---

# PLAN EXÉCUTION FINAL — Refonte vault forge-brain (22 mai 2026)

> **Référence unique** pour la nouvelle session après /compact. Tout ce qu'il faut savoir pour exécuter sans repartir de zéro.

---

## 0. CONTEXTE MISSION

### Demande utilisateur

Le vault forge-brain (318 notes) s'est accumulé. Doublons, contradictions, doctrine évoluée (22 mai = doctrine hooks/workflow inversée). Quand on demande "analyse ce repo et propose la config CC", les agents pêchent dans un knowledge bruité.

**Objectif final** : que demain on puisse dire à un agent "analyse ce repo, propose-moi un skill parfait, propose-moi le workflow" et qu'il trouve **immédiatement** la doctrine canonique dans le vault.

**Stratégie validée par Raphael** :
- **Clean slate** : on supprime sec (pas d'archive)
- **Notes neuves** créées from scratch avec titres nets, contenu précis, findability max
- **Aucune pitié** pour les notes existantes obsolètes ou redondantes
- **Forge = PERSONNEL** (pas Neoteem) — pas d'exemples ia_back/neo_ia dans les notes canoniques

### Hiérarchie de vérité (arbitrage)

1. **Équipe Claude Code / Anthropic officiel** = dernier mot (Boris, Cat Wu, Thariq, Lisa Crofoot, Erik Schluntz, Angela Jiang, Noah Zweben, Justin Young, Lydia Hallie, Alex Albert, docs Anthropic, blogs anthropic.com)
2. **Karpathy** = peut avoir dernier mot s'il est pertinent
3. **Autres** (Trail of Bits, Simon Willison, Addy Osmani, Fowler, Hashimoto, Ronacher) = sources secondaires. Si conflit avec #1 ou #2 → on suit #1/#2.

### Standard "note parfaite" (critères Raphael)

Chaque note canonique DOIT répondre EXPLICITEMENT à :

| Dimension | Question à laquelle la note répond |
|-----------|-----------------------------------|
| **QUOI** | Définition exacte + citations VERBATIM sources |
| **POURQUOI** | Le problème résolu, le besoin |
| **COMMENT** | Étapes concrètes, exemples code/config |
| **QUAND** | Critère d'application (quand utiliser, quand NE PAS) |
| **WORKFLOW** | "Pour X il faut Y qui appelle Z grâce à règle W" — chaîne complète |
| **APPELS** | Quelles autres notes/skills/agents/hooks/rules sont mobilisés, dans quel ordre |
| **OPTIMISATION** | Niveau (basique/avancé/expert), pourquoi cette optim |
| **POURQUOI CETTE OPTIM** | Le gain mesurable (coût, latence, fiabilité) avec chiffres |
| **ANTI-PATTERNS** | Ce qu'il ne faut PAS faire, pourquoi, exemple fail |
| **EXEMPLES** | 1-2 exemples concrets — UNIQUEMENT repos externes publics reconnus (PAS ia_back/neo_ia/lojii qui sont cibles d'application) |
| **SOURCES** | URLs verbatim, dates, auteurs |
| **GOTCHAS** | Pièges (Windows, MCP, paths, Python, frontmatter) |
| **ALIASES** | 6-10 minimum pour findability |
| **WIKILINKS** | Liens vers TOUTES notes liées |

**Longueur** : pas de plafond. 500-2000 lignes acceptées si justifié.

---

## 1. ÉTAT ACTUEL DU CHANTIER

### Inventaire des 15 rapports déposés (`vault/claude-forge/0-Inbox/_chantier-22mai/`)

| Fichier | Taille | Contenu clé |
|---------|--------|-------------|
| `recherche-blog-docs-anthropic.md` | 25 KB | Doctrine officielle, "MCP for data Skills for how-to", 200L CLAUDE.md, 5 anti-patterns officiels |
| `recherche-github-karpathy-leaders.md` | 23 KB | `anthropics/claude-code` minimaliste 3 commandes, `claude-for-legal/CLAUDE.md` 130L, 36 plugins officiels, Fowler/Böckeler Guides+Sensors |
| `recherche-x-twitter-leaders.md` | 27 KB | Boris 259 PRs Opus 4.5 déc 2025, Karpathy thread pivot 26 janv 2026, Addy Osmani harness +21.8 pts |
| `recherche-youtube-talks.md` | 28 KB | Trail of Bits config publique, Karpathy LLM Wiki Gist, Forrest Chang CLAUDE.md, Anti-rationalization Stop hook |
| `recherche-youtube-watch-vibe-coding.md` | 40 KB | Erik Schluntz vibe coding 22k LOC analogie, Boris Sequoia "coding solved" + /loop, Thariq SDK Workshop swiss cheese + lethal trifecta + bash>tools, Cat Wu/Boris London keynote routines + advisor 5× |
| `recherche-karpathy-vault-canonique.md` | 26 KB | Gist verbatim 3-layers raw/wiki/schema + Ingest/Query/Lint + index.md + log.md format strict, Karpathy chez Anthropic depuis 19 mai 2026 |
| `recherche-karpathy-youtube-vault.md` | 24 KB | 0 vidéo dédiée, 0 repo dédié, seul artefact `nanochat/.claude/skills/read-arxiv-paper/SKILL.md`, qmd = Tobi Lütke (PAS Karpathy) |
| `recherche-mcp-vs-skills-cli.md` | 21 KB | Doctrine Anthropic verbatim, Karpathy qmd = CLI+MCP les deux, Boris "MCP la réponse la plus simple", Thariq 3-way tools/bash/code-gen, Ronacher Sentry MCP ~8k tokens upfront |
| `audit-mcp-forge-brain.md` | 27 KB | 11 outils exacts, 4 forces uniques (fallback search 4-strat, alias FR, content-hash, BM25 10/1/8), 318 notes, 1774 aliases, FastMCP 2 + pyyaml |
| `audit-notes-existantes-vs-fraiches.md` | 53 KB | Verdicts ABSORBER/RÉÉCRIRE/REMPLACER/CRÉER par sujet, top 10 verbatim absents, fiches leaders manquantes |
| `audit-qualite-rapports-chantier.md` | 37 KB | 6/8 sujets produisibles, 2 bloquants levés, contradictions chiffrées arbitrées |
| `verif-claudemd-taille-officielle.md` | 6 KB | CONFIRMÉ : "target under 200 lines" verbatim, distinction MEMORY.md 200L hard limit |
| `verif-9-categories-skills-thariq.md` | 3 KB | 9 catégories verbatim LinkedIn 17 mars 2026 |
| `verif-hooks-anthropic-officielle.md` | 6 KB | 29 events officiels, timeout 60s, PostCompact existe, asyncRewake existe, exit 1 ≠ bloquant |
| `verif-finale-avant-canoniques.md` | 27 KB | 14 claims arbitrés, attributions corrigées |
| `verif-25k-et-compute-allocator.md` | (en cours créé) | 25k tokens CONFIRMÉ FORT (12 sources), compute allocator Thariq CONFIRMÉ (5 sources, talk HTML markdown) |

**Total** : 16 fichiers, ~373 KB de matière première vérifiée.

### État git

Branche : `main` à jour avec `origin/main`. Modifs en cours : `.claude/.session-turn-counter`, `vault/claude-forge/.obsidian/workspace.json`. Rien de critique.

---

## 2. NOTES À CRÉER (8 canoniques + 9-12 leaders + 1 entreprise)

### 2.1 — 8 notes canoniques

**Convention** : titres en kebab-case, slugs courts mais explicites, aliases riches (8-12 chacun), 1 dossier dédié `04-Techniques/claude-code/` (à créer).

| # | Slug | Titre H1 | Couvre quoi |
|---|------|----------|-------------|
| 1 | `comment-creer-skill.md` | Comment créer une skill Claude Code parfaite | 9 catégories Thariq, frontmatter, < 500L SKILL.md, gotchas-first, progressive disclosure, agentskills.io spec ouverte, anti-patterns, exemples Anthropic `frontend-design`/`skill-creator` |
| 2 | `comment-creer-agent.md` | Comment créer un agent Claude Code parfait | Frontmatter complet (name/description/tools/model/effort/color/memory/permissionMode/disallowedTools/skills), 2-agent architecture Justin Young (init+coding), modèles Sonnet/Opus split, color convention 8 couleurs, anti-patterns CTO orchestrator |
| 3 | `comment-creer-hook.md` | Comment créer un hook Claude Code parfait | 29 events officiels verbatim, timeout 60s, exit codes (0/1/2 + WorktreeCreate), `hookSpecificOutput`, `asyncRewake`, doctrine "If a rule must hold every time, make it a hook", Guides vs Sensors Fowler, anti-patterns hooks workflow |
| 4 | `comment-ecrire-claudemd.md` | Comment écrire un CLAUDE.md parfait | 200L target Anthropic verbatim (pas hard limit), distinction MEMORY.md 200L hard, 5 anti-patterns officiels (kitchen sink, correcting over and over, over-specified, trust-then-verify gap, infinite exploration), test "Would removing this cause mistakes?", Boris golden rule, compounding error-driven, exemple `anthropics/claude-for-legal/CLAUDE.md` 130L |
| 5 | `workflow-claude-code-optimal.md` | Workflow Claude Code optimal pour tout repo (mai 2026) | Routines = higher order prompt (Boris), advisor strategy 5× (Angela Jiang), leaf nodes (Erik Schluntz), human core, verifiable checkpoints, multi-clauding, /loop, planification 15-20 min, parallélisation 5-10 sessions, Sonnet/Opus split, compounding CLAUDE.md, **mention courte PR optionnel customisable** |
| 6 | `methode-analyser-repo.md` | Méthode pour analyser un repo et proposer config Claude Code | Grille 6 étapes (scan archi → identifier rôles → mapper agents → boundaries critiques → patterns → définir CLAUDE.md), Anthropic minimaliste 3 cmd, Trail of Bits stack complet, Forrest Chang 70L viral, anti-patterns (copier config externe sans analyse) |
| 7 | `pattern-vault-llm-karpathy.md` | Pattern vault LLM canonique Karpathy | Gist 3-layers (raw/wiki/schema), 3 ops (Ingest/Query/Lint), 2 fichiers obligatoires (index.md content-oriented + log.md format `## [YYYY-MM-DD] action \| titre`), métaphore "Obsidian IDE / LLM programmer / wiki codebase", qmd Tobi Lütke (PAS Karpathy), Karpathy chez Anthropic 19 mai 2026, forge dépasse Karpathy sur frontmatter strict |
| 8 | `mcp-vs-skills-doctrine.md` | MCP vs Skills+CLI : quand utiliser quoi (doctrine 2026) | Anthropic verbatim "MCP connects data, Skills teach what to do", Karpathy qmd = CLI+MCP les deux, Boris MCP simple cross-surface, Thariq tools/bash/code-gen trade-offs (atomic non-reversible / composable / dynamique), anti-pattern 50-100 tools "modèle se perd", verdict forge GARDER MCP forge-brain |

### 2.2 — Fiches leaders à créer (8 équipe CC + 4 autres + 1 entreprise = 13)

**Équipe Claude Code Anthropic** (dossier `05-Leaders/claude-code/`) :

| Slug | Personne | Rôle | Sources |
|------|----------|------|---------|
| `cat-wu.md` | Cat Wu | Anthropic, keynote London | London keynote, Opus tips |
| `lisa-crofoot.md` | Lisa Crofoot | Anthropic | "Scaffolding holds Claude back" London |
| `angela-jiang.md` | Angela Jiang | Anthropic | Advisor strategy 5× cost reduction London |
| `daisy-hollman.md` | Daisy Hollman | Anthropic | London speaker |
| `jeremy-hadfield.md` | Jeremy Hadfield | Anthropic | Dreaming feature London |
| `erik-schluntz.md` | Erik Schluntz | Co-fondateur Anthropic | Vibe Coding in Prod, leaf nodes, 22k LOC |
| `noah-zweben.md` | Noah Zweben | Anthropic | "+300% PRs équipe 3 mois" |
| `justin-young.md` | Justin Young | MTS Anthropic | 2-agent architecture init+coding, anthropic.com/engineering/effective-harnesses-for-long-running-agents |

**Autres leaders agents** (dossier `05-Leaders/agents/`) :

| Slug | Personne | Sources |
|------|----------|---------|
| `addy-osmani.md` | Addy Osmani | Harness Engineering, Ratchet Principle, +21.8 pts |
| `martin-fowler.md` | Martin Fowler + Birgitta Böckeler | Guides+Sensors taxonomy 2 avril 2026 |
| `hashimoto.md` | Hashimoto (Ghostty) | Origine "harness engineering", AGENTS.md compounding |
| `tobi-lutke.md` | Tobi Lütke | CEO Shopify, créateur qmd (BM25+vector+rerank) |

**Entreprise** (dossier `02-Concurrents/` ou nouveau `04-Techniques/claude-code/setups-publics/`) :

| Slug | Entité | Sources |
|------|--------|---------|
| `trail-of-bits-config.md` | Trail of Bits config CC publique | github.com/trailofbits/claude-code-config, anti-rationalization Stop hook, 3-tier sandbox |

### 2.3 — Note bonus : `anthropics-claude-code-setup-public.md`

Référence des setups Anthropic publics :
- `anthropics/claude-code` (minimaliste 3 cmd)
- `anthropics/claude-code-action/CLAUDE.md` (seul CLAUDE.md public Anthropic)
- `anthropics/claude-for-legal/CLAUDE.md` (130L, 5 sections)
- `anthropics/claude-plugins-official` (36 plugins canoniques)
- `anthropics/skills` (17 skills officielles)

---

## 3. NOTES À SUPPRIMER (rm sec — clean slate validée Raphael)

### 3.1 — À remplacer par les canoniques

| Note à supprimer | Remplacée par |
|------------------|---------------|
| `01-Claude/Code/best-practices/skills-guide.md` | `comment-creer-skill.md` |
| `01-Claude/Code/best-practices/agents-orchestration.md` | `comment-creer-agent.md` |
| `01-Claude/Code/best-practices/hooks-guide.md` | `comment-creer-hook.md` |
| `01-Claude/Code/best-practices/claudemd-guide.md` | `comment-ecrire-claudemd.md` |
| `04-Techniques/patterns/claudemd-maintenance.md` | absorbé dans `comment-ecrire-claudemd.md` |
| `04-Techniques/patterns/karpathy-llm-wiki-pattern.md` (v0.1 buggée) | `pattern-vault-llm-karpathy.md` (réécrit propre) |

### 3.2 — Obsolètes doctrine 22 mai

| Note à supprimer | Raison |
|------------------|--------|
| `04-Techniques/patterns/pattern-architect-first-pipeline.md` | Hooks workflow supprimés 22 mai |
| `04-Techniques/patterns/Workflow Boris.md` (avril) | Supersédé par `boris-workflow-2026-may.md` puis par `workflow-claude-code-optimal.md` |
| `04-Techniques/patterns/boris-workflow-2026-may.md` | Absorbé dans `workflow-claude-code-optimal.md` |
| `01-Claude/Code/best-practices/setup-project-complet.md` | Obsolète avril, absorbé dans `methode-analyser-repo.md` |
| `01-Claude/Code/best-practices/kit-rules-standard.md` | Absorbé dans `methode-analyser-repo.md` |
| `04-Techniques/patterns/vibe-coding-setup-complet.md` | Absorbé dans `workflow-claude-code-optimal.md` |
| `04-Techniques/patterns/best-practices-claude-code-leaders.md` | Absorbé dans `workflow-claude-code-optimal.md` |
| `04-Techniques/patterns/pipeline-boris-adapte-neoteem.md` | Trop Neoteem-spécifique, absorbé dans `workflow-claude-code-optimal.md` |
| `04-Techniques/agents/pattern-agentic-engineering.md` | Note dieu trop large, absorbée dans `workflow-claude-code-optimal.md` + `methode-analyser-repo.md` |
| `04-Techniques/agents/agentic-engineering-karpathy.md` | Absorbé dans fiche `Andrej Karpathy.md` enrichie |
| `04-Techniques/patterns/Karpathy Dev Discipline.md` | Absorbé dans fiche `Andrej Karpathy.md` enrichie |

### 3.3 — Obsolètes Knowledge (DA initial validé)

| Note Knowledge à supprimer | Raison |
|----------------------------|--------|
| `Knowledge/erreurs/erreur-marker-ttl-blocage-agents.md` | Système markers/TTL supprimé |
| `Knowledge/erreurs/erreur-architect-marker-pipeline-neoia.md` | Pipeline markers supprimé |
| `Knowledge/raisonnements/raisonnement-hook-agent-detection-method.md` | dispatch-guard supprimé |
| `Knowledge/critiques/critique-2026-05-22-architect-guard-allowlist.md` | architect-guard supprimé |
| `Knowledge/critiques/critique-2026-05-21-dispatch-guard-livraison.md` | dispatch-guard supprimé |
| `Knowledge/critiques/critique-2026-05-21-color-tdd-cto-mindset.md` | TDD hooks + dispatch-guard supprimés |
| `Knowledge/critiques/critique-tdd-neo-ia-proposal.md` | TDD strict supprimé |
| `Knowledge/erreurs/erreur-skip-checklist-skill-modification.md` | Doublon `erreur-edit-direct-skills` |
| `Knowledge/critiques/critique-2026-05-21-setup-tdd-strict-neoia.md` | Absorbé `raisonnement-kill-tdd-strict-hooks` |
| `Knowledge/critiques/critique-2026-05-10-mcp-forge-brain.md` | Bugs déjà dans 2 erreurs dédiées |
| `Knowledge/critiques/critique-2026-05-21-tdd-optimizations-handshake.md` | Doublon `erreur-advisory-rules-insuffisantes` |

**Total suppression** : ~22 notes vault.

### 3.4 — Notes Knowledge à PRÉSERVER (intactes, non touchées)

Raphael a dit "au pire on supprimera Knowledge/erreurs", mais l'audit montre que ces notes contiennent des incidents documentés irréplaçables. **Décision** : on garde celles qui ont un signal fort et on supprime les obsolètes (cf 3.3).

**À préserver** (35+ notes Knowledge/erreurs + raisonnements + critiques) :
- `raisonnement-22mai-doctrine-vs-enforcement.md` (pivot)
- `raisonnement-revirement-pipeline-mai-2026.md`
- `raisonnement-kill-tdd-strict-hooks-mai-2026.md`
- `erreur-hooks-workflow-enforcement.md`
- `erreur-pipeline-trop-long-frustration.md`
- `erreur-claude-agent-env-var-dead-code.md`
- `erreur-da-heredoc-bash-silencieux.md`
- `erreur-deploy-sans-advisor-da-cwc2026.md`
- `erreur-devils-advocate-tronque.md`
- `erreur-edit-direct-skills.md`
- `erreur-hooks-bash-quoting-windows.md`
- `erreur-mcp-stopwords-semantiques.md`
- `erreur-mcp-yaml-dump-corruption.md`
- `erreur-password-postgres-clair-mcp-json.md`
- `erreur-settings-paths-hardcodes-multi-poste.md`
- `erreur-skill-monolithique-sans-references.md`
- `erreur-stop-critique-position-gotcha-fin.md`
- `erreur-tests-heureux-vs-adverses.md`
- `erreur-architect-neo_ia-fouille-bdd.md`
- `e-descriptions-keyword-stuffing.md`
- `erreur-auto-mode-classifier-self-modification.md`
- `erreur-advisory-rules-insuffisantes.md` (annoté : "valide pour lint/security, invalide pour workflow")
- `erreur-vault-before-specialist-ttl-scope.md`
- `critique-2026-05-22-vault-doctrine-renversement.md`
- `critique-2026-05-22-audit-neo_ia.md`
- `critique-2026-05-21-refonte-hooks-16-vers-6.md` (HISTORIQUE pivot)
- `critique-2026-05-21-refonte-pipeline-boris-pattern.md` (HISTORIQUE pivot)
- `critique-2026-05-21-repartition-opus-sonnet.md`
- `critique-2026-05-21-brief-distant-template-spec.md`
- `critique-capitalisation-blog-large-codebases-tweet-thariq.md`
- `critique-session-2026-05-20-running-notes-decompose-xread-mcp.md`
- `critique-2026-05-09-skill-done.md`
- `critique-2026-05-13-setup-lojii.md`
- `synthese-audit-coherence-neo-ia-ia-back.md` (préservé même si Neoteem-spécifique : sécurité critique)
- `synthese-techniques-inedites.md`
- `synthese-neoteem-agentic-engineering-mapping.md`
- `synthese-analyse-plugin-claude-code-setup.md`
- `synthese-outils-portabilite-forge.md`
- `synthese-rag-obsidian-claude-video-analyse.md`
- `question-idor-coproprietes-conseil-syndical.md`
- `neo-ia-tests-lenteur-diagnostic.md`

---

## 4. CORRECTIONS D'ATTRIBUTION (à appliquer dans toutes notes)

| Claim original | Correction |
|----------------|------------|
| "Advisor strategy 5× cost reduction" attribué à Cat Wu | → **Angela Jiang** |
| "Scaffolding holds Claude back" attribué à Cat Wu | → **Lisa Crofoot** |
| "+300% PRs hebdo équipe Anthropic" attribué à Boris | → **Noah Zweben** (équipe, 3 mois) |
| "+200% PRs/eng Anthropic" | → **Cat Wu** (org Anthropic) |
| "2-agent architecture (init+coding)" | → **Justin Young, MTS Anthropic** — anthropic.com/engineering/effective-harnesses-for-long-running-agents |
| "qmd créé par Karpathy" | → **Tobi Lütke, CEO Shopify** (Karpathy le recommande, ne l'a pas créé) |
| Karpathy "vibe coding obsolète janvier 2026" | → **Tweet original "vibe coding" = fév 2025**, thread pivot = 26 janv 2026, déclaration formelle "agentic engineering" = Sequoia AI Ascent 29 avril 2026 |
| "Karpathy 220k stars" | → 110k stars Forrest Chang seul + 220k cumul avec mirror multica-ai. Citer les 2 distinctement |
| Boris "150 PRs/jour" | → Chronologie : 259 PRs/30j en décembre 2025 (Opus 4.5, ~8.6/j moyenne) ; "few dozen + 150 record" en avril 2026 (Sequoia, Opus 4.6-4.7) ; pas un conflit, évolution |
| Erik Schluntz "22k LOC en 1 jour" | → **Analogie cognitive verbatim**, PAS métrique brute. Lire le transcript pour le framing exact |
| Hook timeout "60s ET 50 tool-use turns" | → **Uniquement 60s** documenté. Aucune mention "50 turns" dans doc officielle |
| Building Effective Agents "co-auteur Amanda Askell" | → **Erik Schluntz + Barry Zhang uniquement** |

---

## 5. VERBATIM CANONIQUES À UTILISER

### Anthropic officiel (doctrine)

> "MCP connects Claude to data; Skills teach Claude what to do with that data."
> — claude.com/blog/skills-explained

> "If a rule must hold every time, make it a hook rather than a prompt instruction."
> — docs Anthropic, features-overview (validation totale doctrine 22 mai forge)

> "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."
> — code.claude.com/docs/en/memory (section Size, troubleshooting "My CLAUDE.md is too large")

> "Would removing this cause Claude to make mistakes? If not, cut it."
> — Anthropic best-practices

> "Anytime we see Claude do something incorrectly, we add it to CLAUDE.md"
> — Boris Cherny (Anthropic interne, Pragmatic Engineer)

### 5 anti-patterns officiels Anthropic (CLAUDE.md)

1. Kitchen sink (tout mettre)
2. Correcting over and over (même règle répétée)
3. Over-specified CLAUDE.md (trop précis sur l'inutile)
4. Trust-then-verify gap (lister rule mais pas la vérifier)
5. Infinite exploration (pas de bornes d'investigation)

### Erik Schluntz — Vibe Coding in Production

> "99% of your AI-generated tokens should go to planning, interfaces, and communication—not production code"
> — Code with Claude SF, talk "How I AI: HTML is the new markdown" (note : ce verbatim est de Thariq cité ci-dessous, vérifier attribution exacte avant usage final)

4 stratégies verbatim Erik Schluntz :
1. **PM guidance** — agent agit comme PM, pas dev
2. **Leaf nodes** — modifier les feuilles, pas les racines
3. **Human core** — l'humain garde le contrôle des décisions clés
4. **Verifiable checkpoints** — chaque étape vérifiable

Case study : 22 000 LOC, "2 semaines → 1 jour" = **analogie cognitive**, pas métrique brute (corriger framing dans note)

### Thariq Shihipar — Agent SDK Workshop + HTML markdown

3-way trade-offs verbatim :
- **Tools (MCP)** = atomic, non-reversible (write_file, send_email, approve PR)
- **Bash** = composable, exploratoire
- **Code gen** = dynamique, data analysis

Anti-pattern : 50-100 tools → "le modèle se perd"

> "99% of your AI-generated tokens should go to planning, interfaces, and communication—not production code"
> — Thariq, talk "How I AI: HTML is the new markdown"

> "we're all becoming 'compute allocators,' and our main job is to decide what's worth spending compute on"
> — Thariq, idem

Patterns :
- **Lethal trifecta** : (à compléter avec verbatim exact du transcript SDK Workshop)
- **Swiss cheese defense** : multi-layer defense, plusieurs hooks/skills imparfaits qui ensemble couvrent les trous
- **Bash > tools** : bash plus composable que tools structurés pour exploration

### 9 catégories skills Thariq (LinkedIn 17 mars 2026, ordre verbatim)

1. Library & API Reference
2. Product Verification
3. Data Fetching & Analysis
4. Business Process & Team Automation
5. Code Scaffolding & Templates
6. Code Quality & Review
7. CI/CD & Deployment
8. Runbooks
9. Infrastructure Operations

### Boris Cherny (Sequoia + Pragmatic + London)

> "coding is solved" — Sequoia AI Ascent avril 2026

> "I prompt Claude → I create a routine that prompts Claude"
> — Code with Claude London keynote (shift sémantique)

> "Give Claude a way to verify its work → 2-3x quality"
> — Tip #1 Boris

Records : 259 PRs/30j (déc 2025), "few dozen + 150 record" (avril 2026)

### Cat Wu — keynote London

> "scaffolding holds Claude back"
> — Lisa Crofoot (PAS Cat Wu, correction d'attribution)

> "+200% PRs/eng" — Cat Wu London (org Anthropic)
> "+300% PRs équipe sur 3 mois" — Noah Zweben (équipe pas org)

### Angela Jiang — keynote London

> "advisor strategy 5× cost reduction"
> — Angela Jiang Code with Claude London 19 mai 2026

### Karpathy — Gist LLM Wiki + Sequoia

> "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."
> — Gist LLM Wiki 4 avril 2026

> "Vibe coding is over → Agentic engineering"
> — Sequoia AI Ascent 29 avril 2026

4 failure patterns LLM coding (thread X 26 janv 2026) :
1. Silent assumptions
2. Hypertrophy
3. Collateral changes
4. No verifiable success criteria

Gist 3-layers :
- `raw/` = sources immuables
- `wiki/` = LLM-owned markdown compounding
- `CLAUDE.md` ou `AGENTS.md` = schema

3 opérations : **Ingest / Query / Lint**

2 fichiers obligatoires :
- `index.md` content-oriented (lu en premier par LLM)
- `log.md` append-only format strict `## [YYYY-MM-DD] action | titre`

Tooling : qmd (Tobi Lütke, BM25+vector+rerank, CLI+MCP), Obsidian Web Clipper, Marp, Dataview, git

**Karpathy a rejoint Anthropic le 19 mai 2026** — équipe pretraining + Claude-accelerated research. Confirmé CNBC/TechCrunch/X officiel.

### Simon Willison

> "Skills maybe a bigger deal than MCP"
> — simonwillison.net/2025/Oct/16/claude-skills/ (contexte : facilité de partage, PAS la mort de MCP)

### Addy Osmani — Harness Engineering

Stat verbatim : Forge 79.8% vs CC 58% sur Terminal Bench = **+21.8 pts harness > model** (même modèle, harness seul)

Ratchet Principle : ne jamais revenir en arrière sur les améliorations harness

### Fowler / Böckeler — Guides+Sensors (2 avril 2026)

Taxonomy :
- **Guides** = inferential (prompts, rules) — moyen
- **Sensors** = computational (hooks, tests) — fort

Evidence LangChain : 52.8% → 66.5% Terminal Bench avec **même modèle, harness changes seuls**

---

## 6. LIMITES TECHNIQUES CLAUDE CODE (CONFIRMÉES)

| Limite | Valeur | Source |
|--------|--------|--------|
| **Tool response max** | 25 000 tokens (Read + MCP) | 12 sources dont 4 issues officielles `anthropics/claude-code` (#4002, #9152, #14888, #15687), erreur littérale `exceeds maximum allowed tokens (25000)`, default env `MAX_MCP_OUTPUT_TOKENS=25000` |
| **Bash output max** | 50 000 tokens | env `BASH_MAX_OUTPUT_LENGTH=50000` |
| **Hook timeout** | 60 secondes | docs Anthropic officielle hooks |
| **CLAUDE.md target** | < 200 lignes (recommandation, pas hard) | code.claude.com/docs/en/memory verbatim |
| **MEMORY.md hard limit** | 200 lignes OU 25 KB (hard) | docs Anthropic |
| **Skills budget contexte** | 5k tokens chacun, budget combiné 25k post-compaction | docs Anthropic features-overview |
| **Hook events officiels** | 29 events | docs Anthropic verbatim |
| **Exit codes hook** | 0 (silent), 2 (BLOCKING), autre (stderr user). Exit 1 ≠ bloquant. Exception WorktreeCreate (tout non-zero abort) | docs Anthropic |

---

## 7. SLASH COMMANDS — DISTINCTION BUILTIN vs BUNDLED vs CUSTOM

| Commande | Type | Source |
|----------|------|--------|
| `/simplify` | bundled Skill (alias `/code-review`) | Anthropic |
| `/batch` | bundled Skill | Anthropic |
| `/loop` | bundled Skill | Anthropic |
| `/btw` | builtin command | Anthropic |
| `/goal` | builtin command | Anthropic |
| `/schedule` | builtin command | Anthropic |
| `/go` | **CUSTOM forge** (pas builtin) | claude-forge |
| `/spec` | **CUSTOM forge** | claude-forge |
| `/recap` | **CUSTOM forge** | claude-forge |
| `/done` | **CUSTOM forge** | claude-forge |

---

## 8. PR SCOPE — RÈGLE RAPHAEL

- ❌ **PAS de section PR-workflow** comme standard universel
- ✅ **Mention courte** : "PR workflow optionnel, à customiser selon repo. Forge utilise `/spec` etc. plutôt que CI/labels élaborés"
- ✅ Boris `@.claude` tag dans PRs = pattern à mentionner brièvement, pas une obligation

Forge = repos personnels, pas de CI/labels élaborés. Les notes canoniques ne doivent PAS présupposer un workflow PR standardisé.

---

## 9. AUDIT MCP FORGE-BRAIN (à intégrer note `mcp-vs-skills-doctrine.md` ou note dédiée)

### Inventaire 11 outils MCP forge-brain

1. `search_brain(query, limit, context)` — full-text FTS5 sur tout le vault
2. `read_note(file)` — lecture par nom ou alias
3. `read_note_by_path(path)` — lecture par chemin exact
4. `get_backlinks(file)` — graphe de liens
5. `get_tags()` — vue structurelle tags
6. `get_property(file, name)` — propriété frontmatter
7. `list_notes(folder, limit)` — listing dossier
8. `vault_stats()` — stats vault
9. `create_note(path, content)` — création note
10. `append_note(file, content)` — ajout fin de note
11. `update_property(file, name, value)` — modif frontmatter

**Pas de `delete_note`** — suppression doit passer par `Bash rm` (validé Raphael).

### 4 forces uniques (anchored code)

1. Fallback search 4-strat (AND → OR prefix → OR exact → alias expansion) — `database.py:192-220`
2. Alias expansion avec stem variants FR ad-hoc — `database.py:148-156`
3. Content-hash short-circuit watcher — `watcher.py:42-54` (skip reindex si mtime change mais hash identique)
4. BM25 pondéré opinionated 10/1/8 (file_stem/content/aliases)

### Faiblesses

- Watcher polling 30s (pas event-based)
- `git_sync` dead code en prod (`auto_commit: false`)
- 0 tests pytest malgré `testpaths` déclaré
- `_alias_expansion` LIKE O(n), OK à 1774 aliases
- 3 bugs historiques mai 2026 (stop words, yaml.dump, ranking) — corrigés

### Stats vault actuelles

- **318 notes** (pas 309)
- **1774 aliases**
- **1508 wikilinks**
- **118 tags**
- DB 5.18 MB
- Port 8091
- FastMCP 2 + pyyaml = 2 deps

### Architecture clarifiée Raphael

- **MCP forge-brain** = vault claude-forge (perso, port 8091)
- **MCP obsidian-brain** = vault neoteem-brain (business, distinct)
- **2 MCPs distincts** sur 2 vaults distincts
- ❌ **Langfuse ne peut PAS mesurer token cost MCP** (Langfuse trace LLM calls, pas MCP exchanges)

---

## 10. EXEMPLES CONCRETS À CITER (PAS ia_back/neo_ia/lojii)

Quand une note canonique a besoin d'exemples concrets, citer UNIQUEMENT :

### Repos Anthropic publics
- `anthropics/claude-code` — config minimaliste 3 slash commands
- `anthropics/claude-code-action/CLAUDE.md` — seul CLAUDE.md Anthropic exposé publiquement
- `anthropics/claude-for-legal/CLAUDE.md` — 130 lignes, 5 sections (validation, conventions, cookbooks, things-to-leave-alone)
- `anthropics/claude-plugins-official` — 36 plugins canoniques
- `anthropics/skills` — 17 skills officielles + spec ouverte agentskills.io

### Repos Karpathy
- `karpathy/nanochat/.claude/skills/read-arxiv-paper/SKILL.md` — seul skill public Karpathy, ~40 lignes, atomique
- Karpathy LLM Wiki Gist : gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

### Trail of Bits
- `github.com/trailofbits/claude-code-config` — config CC entreprise sécu complète
- Anti-rationalization Stop hook (pattern inédit, Haiku check cop-outs)
- Sandbox 3-tier (/sandbox builtin / devcontainer / dropkit DO droplets)

### Tech écosystème skills publics
- `forrestchang/andrej-karpathy-skills` — CLAUDE.md viral 110k stars, 70 lignes, 4 principes (note : PAS endorsé par Karpathy publiquement)
- Stripe, Vercel, Cloudflare, Sentry, OpenAI, HashiCorp, Figma, Netlify — skills publics
- Simon Willison `simonw/llm`
- Hashimoto Ghostty `AGENTS.md`

### Spec ouverte
- `agentskills.io` — adopté par ~40 produits (Cursor, Codex, Gemini CLI, Goose, Copilot, Roo, Kiro, Letta, Spring AI, Snowflake Cortex, Tabnine, Mistral Vibe, etc.)

---

## 11. PLAN D'EXÉCUTION PHASE B (PRODUCTION)

### Ordre d'exécution recommandé (après /compact)

**Pré-flight** :
1. Relire ce fichier PLAN-EXECUTION-FINAL.md en entier (référence unique)
2. `git status` clean + `git log` récent pour orienter
3. Créer dossier `04-Techniques/claude-code/` (nouveau dossier pour les 8 canoniques)

**Production canoniques (1 par 1 avec commit après chaque)** :

1. **Pilote `comment-ecrire-claudemd.md`** (sujet le plus utilisé, validation standard)
   - Présenter à Raphael pour validation du standard
   - Si OK → continuer
   - Si KO → itérer

2. `mcp-vs-skills-doctrine.md` (2e pilote, sujet sans note existante)

3. `comment-creer-skill.md`

4. `comment-creer-agent.md`

5. `comment-creer-hook.md`

6. `workflow-claude-code-optimal.md`

7. `methode-analyser-repo.md`

8. `pattern-vault-llm-karpathy.md`

**Production fiches leaders (13 fiches)** :
- 8 équipe CC + 4 autres + 1 entreprise
- Commits groupés par dossier (équipe CC, autres agents, entreprise)

**Phase nettoyage destructif** :
- AVANT chaque `rm` : `mcp__forge-brain__get_backlinks(file)` pour identifier les backlinks
- Mettre à jour les wikilinks pointants AVANT le `rm`
- `Bash rm` sec (Raphael a validé)
- Commit par batch logique (skills obsolètes, agents obsolètes, hooks obsolètes, Knowledge obsolètes)

**Phase index + CHANGELOG** :
- Mettre à jour `00-Hub/MOC-*` pointants vers les nouvelles canoniques
- `vault/claude-forge/CHANGELOG.md` — section `## 2026-05-22 — Refonte canonique chantier 22 mai`
- Lister explicitement : 8 canoniques créées, 13 leaders créés, 22 notes supprimées

**Phase DA final** :
- Lancer `devils-advocate` sur les 8 canoniques produites
- Si bloquants → itérer
- Si OK → commit final + push

---

## 12. RÈGLES ABSOLUES (à respecter dans chaque note canonique)

1. ✅ **Citation verbatim avec URL** chaque fois que possible (pas paraphrase)
2. ✅ **Dates exactes** (pas "récemment", pas "il y a peu")
3. ✅ **Métriques chiffrées** (LOC, tokens, durée, %, count)
4. ✅ **Anti-patterns nommés** explicitement
5. ✅ **Workflow étape par étape** (numéroté, pas généralités)
6. ✅ **Exemples concrets de repos externes uniquement** (pas ia_back/neo_ia/lojii)
7. ✅ **Aliases 6-10 minimum** pour findability
8. ✅ **Wikilinks vers toutes notes liées**
9. ✅ **8 dimensions standard "parfait"** couvertes (QUOI / POURQUOI / COMMENT / QUAND / WORKFLOW / APPELS / OPTIM / POURQUOI OPTIM / ANTI-PATTERNS / EXEMPLES / SOURCES / GOTCHAS / ALIASES / WIKILINKS)
10. ✅ **Hiérarchie sources** : équipe CC > Karpathy > autres. Si conflit → on suit équipe CC
11. ✅ **PR scope minimal** : mention courte uniquement, pas section
12. ✅ **Frontmatter complet** : titre, resume, aliases, derniere-maj, auteur, sources, tags, type

---

## 13. CHECKLIST À VALIDER AVANT CHAQUE COMMIT

Pour chaque note canonique produite :

- [ ] Frontmatter complet
- [ ] 8 dimensions standard couvertes
- [ ] Au moins 5 citations verbatim avec URL
- [ ] Au moins 3 exemples concrets repos externes
- [ ] Au moins 6 aliases
- [ ] Au moins 5 wikilinks vers notes vault
- [ ] Anti-patterns nommés
- [ ] Limites techniques chiffrées
- [ ] Corrections d'attribution appliquées (cf section 4)
- [ ] Pas de mention ia_back/neo_ia/lojii sauf si nécessaire (en exemple personnel pas en exemple générique)
- [ ] Pas de PR-workflow comme standard (juste mention courte)

---

## 14. RÉFÉRENCES — TOUS LES RAPPORTS DU CHANTIER

À consulter pendant la production :

- `recherche-blog-docs-anthropic.md` — doctrine officielle
- `recherche-github-karpathy-leaders.md` — setups publics + Karpathy
- `recherche-x-twitter-leaders.md` — verbatim threads X
- `recherche-youtube-talks.md` — Trail of Bits + Karpathy Gist + Forrest Chang
- `recherche-youtube-watch-vibe-coding.md` — **38k mots transcripts** (Erik / Boris / Thariq / Cat-Boris)
- `recherche-karpathy-vault-canonique.md` — Gist verbatim + repos
- `recherche-karpathy-youtube-vault.md` — confirmation 0 vidéo dédiée
- `recherche-mcp-vs-skills-cli.md` — doctrine MCP vs Skills
- `audit-mcp-forge-brain.md` — 11 outils + 4 forces
- `audit-notes-existantes-vs-fraiches.md` — verdicts par sujet
- `audit-qualite-rapports-chantier.md` — contradictions arbitrées
- `verif-claudemd-taille-officielle.md` — 200L verbatim
- `verif-9-categories-skills-thariq.md` — 9 catégories verbatim
- `verif-hooks-anthropic-officielle.md` — 29 events + timeout 60s
- `verif-finale-avant-canoniques.md` — 14 claims arbitrés
- `verif-25k-et-compute-allocator.md` — 2 claims CONFIRMÉS

---

## 15. RAPPEL CRITIQUE POUR NOUVELLE SESSION

**Tu reprends ce chantier dans une nouvelle session après /compact.**

**Première action** : `Read` ce fichier en entier (PLAN-EXECUTION-FINAL.md). C'est ta carte.

**Deuxième action** : `git log` + `git status` pour voir l'état réel.

**Troisième action** : confirmer à Raphael que tu as repris le fil avec ce PLAN.

**Quatrième action** : commencer par la note pilote `comment-ecrire-claudemd.md` (validation standard).

**Ne JAMAIS oublier** :
- Hiérarchie sources : équipe CC > Karpathy > autres
- Pas d'exemples ia_back/neo_ia/lojii dans les notes canoniques
- Pas de PR comme standard
- Standard "parfait" 14 dimensions (cf section 0)
- Corrections d'attribution (cf section 4) — Angela Jiang, Lisa Crofoot, Noah Zweben, Justin Young, Tobi Lütke
- Limites techniques (cf section 6) — 25k tool, 60s hook, 200L CLAUDE.md
- Distinction slash commands (cf section 7)
- Verbatim canoniques (cf section 5) — réutiliser directement
- Clean slate : `rm` sec, pas d'archive (Raphael validé)
- Backlinks mappés AVANT chaque `rm` (advisor)
- 1 commit par canonique terminée (advisor)

**Devil's advocate validations passées** :
- Hooks workflow = anti-pattern (doctrine 22 mai)
- DA initial sur ce chantier a flaggé : backlinks à mapper, attribution leaders à préserver, mesurer avant fusion
- DA initial a aussi validé : P0 recherche web pur bénéfice

**Posture Jarvis** : tu es partenaire pas exécutant. Proactif. Innovateur. Franc.

**Fin du PLAN — Bonne reprise.**
