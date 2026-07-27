---
titre: "CC 28 mai 2026 — Opus 4.8 + Dynamic Workflows"
resume: "Opus 4.8 (claude-opus-4-8, 28 mai 2026, défaut effort high, fast mode 3× moins cher) + Dynamic Workflows research preview — Claude écrit un script JS d'orchestration lançant jusqu'à 1000 sous-agents (16 concurrents), coordination hors-contexte, déclenché par 'workflow' ou réglage ultracode."
aliases:
  - "Opus 4.8"
  - "claude-opus-4-8"
  - "Dynamic Workflows"
  - "ultracode"
  - "CC 28 mai 2026"
  - "v2.1.154"
  - "v2.1.156"
  - "workflow tool claude code"
domaine: claude-code
type: changelog
derniere-maj: 2026-07-27
auteur: claude
sources:
  - "https://www.anthropic.com/news/claude-opus-4-8"
  - "https://claude.com/blog/introducing-dynamic-workflows-in-claude-code"
  - "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
  - "#domaine/workflow"
  - "#doctrine/2026"
---

# CC 28 mai 2026 — Opus 4.8 + Dynamic Workflows

> Drop majeur 28 mai 2026 : nouveau modèle frontier + feature d'orchestration native. Source primaire vérifiée (WebFetch anthropic.com + claude.com 29 mai 2026).

## Claude Opus 4.8 (28 mai 2026)

| Fait | Valeur |
|------|--------|
| ID modèle | `claude-opus-4-8` |
| Date | 28 mai 2026 (41 jours après 4.7) |
| Prix standard | $5 / M input · $25 / M output (identique 4.7) |
| Prix fast mode | $10 / M input · $50 / M output (fast mode 3× moins cher qu'avant, vitesse 2.5×) |
| Effort par défaut | **high** (recommandé) · options `extra`/`xhigh` · `max` |
| Honnêteté code | ~4× moins susceptible de laisser passer une faille sans la signaler vs 4.7 |

Benchmarks vérifiés (source primaire) : Online-Mind2Web 84% · Legal Agent Benchmark premier modèle > 10% all-pass · OSWorld-Verified (4.7 révisé) 82.3%. (SWE-bench Pro 69.2% et USAMO 96.7% cités par presse tierce TechCrunch/MarkTechPost — non confirmés sur la page Anthropic, à traiter comme secondaire.)

## Dynamic Workflows (research preview, 28 mai 2026)

**Principe** : Claude rédige dynamiquement un **script d'orchestration** (JavaScript) qui lance des dizaines à des centaines de sous-agents en parallèle dans une session unique. La coordination se passe **hors de la conversation** (« the coordination happens outside the conversation ») : le plan vit dans le code, les résultats intermédiaires dans des variables de script, et seul le résultat final revient dans le contexte.

**Caps** (source : doc du tool Workflow) : jusqu'à **1000 agents** sur la durée de vie d'un run, **16 concurrents** simultanés (min(16, cores-2)). Vérification adversariale intégrée (agents indépendants tentent de réfuter les findings) + itération jusqu'à convergence.

**Déclenchement** :
1. Demander explicitement (« Create a workflow » / mentionner « workflow » dans le prompt)
2. Activer le réglage **`ultracode`** (menu effort) → fixe l'effort à `xhigh` ET laisse Claude décider automatiquement de lancer un workflow

**Durée** : peut s'étendre sur des heures, voire des jours. Runs **resumables** (progression sauvegardée en cas d'interruption — `resumeFromRunId`).

**Surfaces** : CLI + Desktop + extension VS Code. Visible via `/workflows`. Requiert **v2.1.154+**.

**Plans** : Max, Team, Enterprise (si activé par admin) + API / Bedrock / Vertex / Foundry.

**Coût** : consommation de tokens nettement supérieure à une session classique. Anthropic recommande de commencer scopé + activer auto mode.

**Cas réel cité** : Jarred Sumner a réécrit Bun (Zig → Rust), ~750k lignes en 11 jours, 99.8% des tests verts.

## Changelog CLI associé (v2.1.141 → v2.1.156)

Versions postérieures à v2.1.140 pertinentes pour forge :

- **v2.1.156** — fix erreurs API Opus 4.8 (thinking blocks modifiés).
- **v2.1.154** — Opus 4.8 + Dynamic Workflows + `/workflows` ; **lean system prompt par défaut** (sauf modèles ≤4.7) ; `/simplify` = cleanup-only ; labels effort « Faster »/« Smarter » ; `claude agents` : `!<cmd>` en background, `claude --bg --exec` ; plugins `defaultEnabled: false` ; MCP `.mcp.json` non approuvés → `⏸ Pending approval` au lieu d'auto-approuver ; stdio MCP reçoit `CLAUDE_CODE_SESSION_ID`/`CLAUDECODE=1` ; classifier auto-mode renforcé (exfiltration data / transferts repo en masse) ; fix `rm -rf $HOME` non bloqué si `HOME` a un slash final ; fix subagents background contournant la garde worktree-isolation.
- **v2.1.153** — keybinding `modelPicker:setAsDefault` renommé `modelPicker:thisSessionOnly` ; `skipLfs` option marketplace ; `COLUMNS`/`LINES` passés aux status line commands.
- **v2.1.152** — **skills/slash commands peuvent set `disallowed-tools` en frontmatter** ; `/reload-skills` ; `SessionStart` hook → `reloadSkills: true` + `hookSpecificOutput.sessionTitle` ; **nouvel event hook `MessageDisplay`** (transformer/cacher le texte assistant) ; auto mode ne requiert plus d'opt-in consent.
- **v2.1.149** — `/usage` breakdown par catégorie (skills/subagents/plugins/coût par MCP) ; fix bypass permission PowerShell (`cd` natif changeait CWD sans détection) ; fixes wildcard PowerShell.
- **v2.1.147** — `/simplify` renommé `/code-review` (`--comment` PR inline) ; fix `if` de hook `PowerShell(git push*)` jamais matché.
- **v2.1.145** — `claude agents --json` ; Stop/SubagentStop hook input inclut `background_tasks` + `session_crons` ; fix boucle skill `context: fork`.
- **v2.1.143** — stop hooks bloquants en boucle : fin de session après **8 blocages consécutifs** ; PowerShell tool passe `-ExecutionPolicy Bypass` par défaut (opt-out `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1`) ; `worktree.bgIsolation`.

## Deadline imminente

- **`CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` supprimé le 01/06/2026** (changelog 2.1.154). Migrer vers `/model claude-opus-4-6[1m]` puis `/fast on`.
- Rappel : `claude-sonnet-4-20250514` + `claude-opus-4-20250514` retirés de l'API **15 juin 2026**.

## Impact doctrine forge

Confronté à [[workflow-claude-code-optimal]] (Advisor Strategy, multi-clauding, PTC) et [[feedback_no_cto_agent]] (« no orchestrator agent ») via skill `doctrine-impact-check` :

- **Dynamic Workflows = orchestration native hors-contexte** — Anthropic livre en produit ce que la doctrine forge interdisait de construire en agent custom (l'agent orchestrateur). La doctrine « pas d'agent orchestrateur » reste valide (on ne CONSTRUIT toujours pas d'agent CTO), mais elle est désormais **complétée** par un outil natif. Continuité directe de PTC ([[programmatic-tool-calling]]) : code orchestre, modèle juge — Dynamic Workflows applique le même principe au niveau Claude Code, pas API.
- **`disallowed-tools` en frontmatter skills (2.1.152)** — renforce la doctrine forge `disallowedTools: Write, Edit` (jusqu'ici sur agents, désormais aussi sur skills).
- **Event hook `MessageDisplay` (2.1.152)** — à ajouter aux events de `cc-hooks-ref`.
- **Mapping modèle CLAUDE.md** — `opus` = `claude-opus-4-7` dans les règles de génération forge ; à arbitrer (Raphael) : bumper vers `claude-opus-4-8`.
- **Stop hook 8 blocages → fin auto (2.1.143)** — pertinent pour [[feedback_stop_hook_injection]].

## Liens

- [[workflow-claude-code-optimal]] — canonique workflow (Dynamic Workflows = niveau natif de PTC)
- [[programmatic-tool-calling]] — PTC, même principe au niveau API
- [[CC mai 2026 - Code with Claude]] — drop précédent
- [[MOC-Claude-Code]]
- [[feedback_no_cto_agent]]


---

## AJOUT 27 juillet 2026 — workflows SAUVEGARDABLES : dossier `.claude/workflows/` (doc officielle vérifiée)

État de la feature au 27 juil. 2026 (source primaire : code.claude.com/docs/en/workflows, fetchée intégralement) — la research preview du 28 mai est devenue un système complet de workflows nommés :

- **Sauvegarde** : `/workflows` → sélectionner un run → touche `s` → deux emplacements : **`.claude/workflows/` (projet, partagé via le repo)** ou `~/.claude/workflows/` (perso, tous projets ; respecte `CLAUDE_CONFIG_DIR`). Le workflow sauvegardé devient une **slash command `/<nom>`** (autocomplete inclus). Conflit de nom : le projet gagne sur le perso.
- **Format du fichier** : `export const meta = { name, description }` (+ `phases`, `whenToUse` optionnels) puis body JavaScript plain avec top-level `await` — `agent()` spawne un subagent, `pipeline()` un par item. Écrit par Claude, éditable à la main.
- **Args** : un workflow sauvegardé accepte un input via `args` (« Run /triage-issues on issues 1024, 1025 ») — passé en données structurées, le script lit le global `args`.
- **Monorepo** (≥ 2.1.178) : sauvegarde dans le `.claude/workflows/` le plus proche du working dir ; chargement depuis TOUS les `.claude/workflows/` du chemin.
- **Plugins** : distribution via dossier `workflows/` à la racine du plugin, namespacé `/plugin:nom`.
- **Bundled** : `/deep-research` = workflow intégré (manuel uniquement depuis v2.1.218).
- **Déclenchement** (précisions post-mai) : mot-clé **`ultracode`** dans le prompt (avant v2.1.160 c'était `workflow`) OU demande en langage naturel (« use a workflow ») OU `/effort ultracode` (session entière, ≥ 2.1.203). Le mot-clé ne fire que sur input HUMAIN tapé (≥ 2.1.210 — plus via webhook/PR comment/-p).
- **Taille** : `workflowSizeGuideline` small/medium/large/unrestricted — **défaut `medium` (< 15 agents) depuis v2.1.219**. Advisory, pas un cap. Warning « Large workflow » à > 25 agents ou > 1,5M tokens projetés (≥ 2.1.203).
- **Permissions** : les subagents d'un workflow tournent TOUJOURS en `acceptEdits` + héritent de l'allowlist, quel que soit le mode session — file edits auto-approuvés ; bash/web/MCP hors allowlist peuvent prompter mid-run (allowlister AVANT un long run). Approbation par run avec « don't ask again » par workflow×projet.
- **Resume** : same-session only — agents complétés = résultats cachés ; sortir de CC pendant un run = repart de zéro à la session suivante.
- **Sécurité save** (≥ 2.1.216) : refus d'écrire à travers un symlink (`.claude`, `.claude/workflows` ou fichier cible côté projet).
- **Désactivation** : `/config` Dynamic workflows off · `"disableWorkflows": true` · `CLAUDE_CODE_DISABLE_WORKFLOWS=1` · managed settings org.

**Pertinence forge** : les orchestrations récurrentes (veille multi-agents type cc-news, sweeps d'audit) sont candidates à être figées en workflows nommés dans `.claude/workflows/` — la doc le dit explicitement : « If you already have an orchestrator built another way, such as a folder of subagent prompts or a skill that fans work out, you can point Claude at it and ask for a workflow that does the same thing. » Tableau comparatif officiel subagents/skills/agent-teams/workflows : « the difference is who holds the plan » — workflow = le script tient le plan, le contexte de Claude ne garde que la réponse finale.
