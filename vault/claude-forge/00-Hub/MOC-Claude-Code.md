---
titre: "MOC — Claude Code"
resume: "Index de tout le savoir Claude Code : features, changelog, hooks, skills, best practices"
aliases:
  - "MOC Claude Code"
  - "CC index"
  - "claude code features"
  - "index claude code"
  - "CC features map"
type: index
derniere-maj: 2026-09-30
auteur: claude
sources: []
tags:
  - "#type/index"
  - "#domaine/claude-code"
---
# Claude Code

## ⭐ Notes canoniques chantier 22 mai 2026 (source de vérité actionnable)

Quand on demande "analyse ce repo, propose-moi la config CC", la doctrine se trouve ici :

- [[comment-ecrire-claudemd]] — target 200L, 5 anti-patterns Anthropic, compounding Boris
- [[comment-creer-skill]] — 9 catégories Thariq (post Anthropic mars 2026), frontmatter trigger 3e personne, budget de listing (drop de descriptions entières, pas troncature)
- [[comment-creer-agent]] — 2-agent Justin Young (sans split modèles), Sonnet/Opus split doctrine forge (Cat Wu + Brad Abrams), convention 8 couleurs
- [[comment-creer-hook]] — **33 events officiels au 5 sept. 2026** (le compte bouge par version : revalider en source avant de citer un chiffre), timeouts 600s/30s/60s par type, doctrine "rule 100% → hook", Böckeler Guides+Sensors
- [[workflow-claude-code-optimal]] — routines Boris + **Advisor Strategy Brad Abrams** + leaf nodes Erik
- [[methode-analyser-repo]] (META) — grille 6 étapes + pipeline architect→dev→reviewer→test
- [[mcp-vs-skills-doctrine]] — MCP data / Skills how-to / Bash exploration, lethal trifecta = Willison
- [[pattern-vault-llm-karpathy]] — 3-layers raw/wiki/schema, qmd Tobi Lütke
- [[pattern-maintenance-hybride-corpus-accumulatif]] — maintenir un corpus qui grossit sans le réécrire à chaque pivot
- [[trail-of-bits-config]] — setup entreprise sécu publique (anti-rationalization Stop hook + 3-tier sandbox)
- [[methode-pivoter-doctrine]] — checklist 5 étapes pour pivot doctrinal sans régression silencieuse
- [[comparaison-skill-anthropic-claude-code-setup]] — vault forge vs skill officielle (15× plus profond, 3 bits utiles repris)

### Doctrine par modèle (lignée Opus 5 / Fable 5.1)

- [[doctrine-par-modele-opus5-fable5]] — les règles de prompting diffèrent PAR MODÈLE, pas par génération : Opus 5 s'auto-vérifie et sur-délègue, Fable 5.1 refuse les instructions show-your-reasoning (`reasoning_extraction`)
- [[effort-opus-47-doctrine-anthropic-2026]] — source de vérité sur `effort:` : `high` est le point de départ sur Opus 5 / Fable 5 / Sonnet 5, `xhigh` = step-up mesuré. Porte le sweep mesuré du 5 sept. 2026
- [[prompting-fable5-cheatsheet]] — prompting Fable par symptôme

## ⚙️ Rules transverses

- `.claude/rules/sequence-canonique-modification.md` — séquence A→B→C→D→E obligatoire pour création/modification/optimisation

## Changelog (consolidé par mois)

- [[CC septembre 2026 - Opus 5.5 + v2.1.263-282]] — couvre v2.1.263 → v2.1.285 : **Opus 5.5 défaut Opus** (effort API `medium`), **Sonnet 5.5 défaut Sonnet** sur l'API Anthropic (2.1.284), auto mode par défaut sans `permissions.defaultMode`, Ultracode devenu toggle séparé, `/doctor prompt-audit`, hooks agent-type interdits sur PermissionRequest, AGENTS.md sans CLAUDE.md, TaskOutput supprimé, omitClaudeMd, maxEffortLevel, namespace `anthropic-skills` réservé (réservation `claude-ai` annulée en 2.1.283)

- [[CC juillet 2026 - Opus 5 + v2.1.212-220]] — **Opus 5 défaut Opus**, /fork background + /subtask, EndConversation, patch sécu PowerShell 5.1, nesting depth 3 + caps, skills context:fork background
- [[CC juillet 2026 - v2.1.203-211]] — auto mode défaut gateways, screen reader, transcripts -79x, hardening anti-injection Agent
- [[CC juillet 2026 - Sonnet 5 + v2.1.198]] — Sonnet 5 défaut (1M natif), /dataviz, Chrome GA, v2.1.191→202 (Dynamic workflow size, mode Manual, slash-skills empilées)
- [[CC juin 2026 - v2.1.160 ultracode]] — ultracode, Fable 5 intro, v2.1.150→190
- [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] — Opus 4.8 + orchestration native (devenue workflows nommés `.claude/workflows/` en juillet, cf AJOUT 27 juil. de la note)
- [[CC mai 2026 - Code with Claude]] — Desktop GUI, web UI, v2.1.126→v2.1.136, cache TTL fix, memory leak fix
- [[CC avril 2026]] — Opus 4.7, Auto Mode, CLI binaire natif, Windows sans Git Bash, v2.1.110→v2.1.123

## Features (notes existantes)

- [[auto-mode-classifier]] — Classifier auto-mode, hard-block settings.json + hooks sécu, bug antislash Windows
- [[architecture-claude-folder]] — Anatomie complète du dossier .claude/ (settings, skills, agents, hooks, rules)
- [[worktrees-sessions-paralleles]] — Worktrees natifs vs convention develop, sessions parallèles
- [[skills-metadata-tokens-load]] — Coût tokens du chargement des métadonnées skills
- [[skills-externes-upstream-sync]] — Skills marketplace : upstream sync, jamais fabriquer
- [[enableallprojectmcp-permissions-allow]] — enableAllProjectMcpServers vs permissions.allow tool-level
- [[agent-teams-natif-anthropic]] — Agent Teams natif (teammates, mailbox, plan approval)
- [[Computer Use CC]]
- [[Claude Security]]
- [[claude-desktop-preferences]] — Profil, Cowork, pattern vault-first MCP pour non-devs
- [[mcp-obsidian-brain-v2]] — MCP SQLite FTS5 autonome, déployé sur VM, accessible via VPN
- [[cowork-architecture]] — Architecture Cowork, Dispatch, Plugin Marketplace, Agent Teams
- [[programmatic-tool-calling]] — PTC : code orchestre, modèle juge
- [[How we contain Claude]] — containment cross-produits : sandbox −84 % prompts, « deterministic boundary »

## Features (à documenter)

Routines · Session Sharing · Remote Control · Dynamic Loop

## Best Practices

- [[workflow-claude-code-optimal]] — Fleet commander, 5 terminaux, worktrees — synthèse Boris, Erik, Thariq, Cat Wu, Karpathy
- [[delegate-guard-pattern]] — Hook PreToolUse forge-only : bloque edits directs, redirige vers agents spécialisés
- [[hook-intercepte-mcp-et-read-tools]] — ce qu'un matcher de hook attrape vraiment (MCP, Read), et pourquoi ses angles morts ne s'exploitent pas
- [[methode-analyser-repo]] — 3 rules obligatoires tout projet : check-before-create, quality-gates, learn-from-mistakes
- [[comment-ecrire-claudemd]] — Consensus Boris + Anthropic : 100-200L max, monthly audit
- [[mcp-vs-cli-vs-skills]] — Quand MCP, quand CLI, quand skill : matrice de décision
- [[audit-tripartite-doctrinal-pattern]] — auditer une config `.claude/` sous 3 lentilles (Discipline / Minimalisme / Couverture)
- [[verification-sources-canoniques]] — matrice de crédit des sources avant capitalisation
- [[steps-of-ai-adoption-boris]] — échelle de maturité 0-4 (16 juil. 2026), bottlenecks + guardrails par transition
- [[fireside-cat-wu-thariq-aiewf-2026]] — doctrine prompting frontière (system prompt −80 %), fewer tools, evals

## Agents forge

> ⚠️ **Pivot 6 juin 2026** — Architecture agents mise à jour. Créateurs devenus des **skills** (thread principal). Auditeurs absorbés dans `repo-inspector`.

Les agents actifs dans `.claude/agents/` :
- `repo-inspector` — Analyse / audit / scan repos (modes audit/analyze/scan). Intègre les 3 lentilles doctrinales (Discipline Boris / Minimalisme Will / Couverture ECC). (purple)
- `code-dev` — Développement multi-stack, remplace python-dev (green)
- `devils-advocate` — Critique livrables majeurs (red)
- `outcomes-grader` — Évaluation livrables (yellow)
- `self-updater` — Maintenance skills de référence (cyan)

Skills créatrices (thread principal — plus des agents) :
- `skill-creator`, `subagent-creator`, `hook-creator`, `claudemd-creator`, `responsable-ia`

Agents supprimés : python-dev → code-dev ; boris-auditor + ecc-auditor + will-auditor → repo-inspector ; agent-creator + hook-creator + skill-creator + claudemd-optimizer → skills.

Convention couleurs : voir [[agents-color-convention]].

## Dépréciations

- [[Deprecation Haiku 3]]
- [[Deprecation Sonnet 4 Opus 4]]
- [[Deprecation 1M Context Beta]]
- [[Deprecation budget_tokens]]
- [[claude-mythos-preview]] — déprécié le 9 juin 2026, retrait « To be announced » (page deprecations au 30 sept. 2026)

## Liens

### Ajouts mai 2026

- [[Code with Claude 2026]] — Conférence SF 6 mai : SpaceX, Dreaming, Outcomes, Multi-agent, Routines
- [[Memory Managed Agents]] — Memory = filesystem, permission scopes, optimistic concurrency, version history
- [[Dreaming Managed Agents]] — Review cross-sessions, déduplication, vérification, enrichissement mémoire

### Leaders ajoutés audit 23 mai 2026

- [[Brad-Abrams]] — Product Lead Anthropic, créateur Advisor Strategy (CwC SF avec Mario Rodriguez GitHub)
- [[Mitchell-Hashimoto]] — popularisateur "harness engineering" (5 fév 2026)

## Synthèses

- [[outils-portabilite-forge]] — Liste des outils CLI à installer quand on utilise claude-forge depuis un nouveau PC : defuddle, yt-dlp, obsidian-cli, node, python.
