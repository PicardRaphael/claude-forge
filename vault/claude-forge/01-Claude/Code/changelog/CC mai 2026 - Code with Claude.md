---
titre: "CC Mai 2026 — Code with Claude Drop"
resume: "Desktop GUI, web UI, Plan mode, Auto mode, Security, Dreaming, CLI updates, deprecations Sonnet 4/Opus 4"
aliases:
  - "Code with Claude mai 2026"
  - "CC mai 2026"
  - "claude code may 2026"
  - "CC changelog mai"
  - "code with claude drop"
  - "CC desktop GUI"
  - "v2.1.126"
  - "v2.1.128"
  - "v2.1.129"
  - "v2.1.132"
  - "v2.1.133"
  - "v2.1.136"
  - "v2.1.139"
  - "v2.1.140"
domaine: claude-code
type: changelog
derniere-maj: 2026-05-24
auteur: claude
sources:
  - "https://www.anthropic.com/news"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

## Features majeures (6 mai)

- **Claude Code on the web** — coder sans terminal (claude.ai/code)
- **Claude Code on Desktop** — GUI plein ecran avec preview, images, rich outputs
- **Plan mode** — review du plan avant execution
- **Auto mode** (research preview Team) — alternative safe a --dangerously-skip-permissions
- **Claude Security** — scan vulnerabilites repos (public beta Enterprise)
- **Claude Design** — prototypes visuels
- **Claude Mythos Preview** — cybersecurite (Project Glasswing)
- **Dreaming** (research preview) — auto-review sessions passees overnight
- **Routines** (Boris) — "higher-order prompts", automations async

## CLI updates

- `CLAUDE_CODE_FORK_SUBAGENT=1` en sessions non-interactives
- Skill folder protection (skip-permissions ne prompt plus pour .claude/skills/)
- MCP auto-retry (3 tentatives) sur erreur transitoire
- `alwaysLoad` option MCP — skip tool-search deferral
- `claude plugin prune` — nettoyage dependances orphelines
- `/model` picker via gateway /v1/models

## Deprecations

- `TaskOutput` tool deprecie → utiliser Read
- **claude-sonnet-4-20250514** et **claude-opus-4-20250514** retirement API **15 juin 2026**
- 1M context beta Sonnet 4/4.5 retiree

## Metrics

- CC = 4% des commits GitHub publics (Boris, CNBC)
- Rate limits 5h doubles (Pro/Max/Enterprise)
- Suppression throttling peak hours

## Changelog CLI détaillé

### v2.1.126 (1er mai)

- `/model` picker via gateway `/v1/models`, `claude project purge`
- **PermissionDenied hook** (`{retry: true}`)
- **PowerShell principal Windows** (plus Bash par défaut)
- PowerShell 7 détection Microsoft Store/MSI/.NET
- `CLAUDE_CODE_NO_FLICKER=1`, OTel `skill_activated` event

### v2.1.128 (3 mai)

- `/color` random, `/mcp` tool count par serveur
- `EnterWorktree` branch depuis local HEAD (unpushed commits préservés)
- `--plugin-dir` accepte `.zip` archives
- Auto mode hints quand classifier échoue

### v2.1.129 (5 mai)

- `--plugin-url`, `skillOverrides` setting
- **CRITIQUE : cache TTL 1h silencieusement réduit à 5min**
- `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`
- Ctrl+R history = all projects, Ctrl+S pour narrower

### v2.1.132 (6 mai)

- `CLAUDE_CODE_SESSION_ID` env var
- **Fix fuite mémoire 10GB+** (MCP stdout non-drainé)
- Fix fullscreen après sleep/wake, mouse wheel Cursor/VS Code

### v2.1.133 (7 mai)

- `worktree.baseRef` (fresh/head), `$CLAUDE_EFFORT` dans hooks
- `sandbox.bwrapPath`/`sandbox.socatPath` configurables
- `parentSettingsBehavior` (admin), fix parallel sessions 401

### v2.1.136 (8 mai)

- `autoMode.hard_deny` (liste noire auto mode)
- @file picker >100, WSL2 image paste, plan mode fix
- Fix MCP après `/clear`, OAuth refresh fix

### v2.1.139 (~11 mai)

- **`/goal` command** — condition de completion, Claude travaille de facon autonome jusqu'a l'atteindre. Mode interactif, `-p`, et Remote Control
- **Agent View** (`claude agents`) — dashboard unique pour toutes les sessions (en cours, bloquees, terminees)

### v2.1.140 (~12-13 mai)

- `command-hook args` — passage d'arguments aux hooks de type command
- `PostToolUse continueOnBlock` — option pour continuer malgre un hook bloquant
- `CLAUDE_PROJECT_DIR` pour MCP stdio servers et plugin commands
- `subagent_type` sur agent hook input — identifier le type d'agent dans les hooks
- Fix `ConfigChange` hooks et hierarchie `disableAllHooks`/`allowManagedHooksOnly`

## Liens

- [[Code with Claude Conference]]
- [[Managed Agents]]
- [[Cowork GA]]
- [[MOC-Claude-Code]]
- [[CC avril 2026]]


## London drop (19 mai 2026)

### Nouvelles features
- **Self-Hosted Sandboxes** (public beta) — exécution Managed Agents dans infra client (Cloudflare, Modal, Vercel, Daytona, custom containers)
- **MCP Tunnels** (research preview) — accès sécurisé aux MCP servers privés via tunnel outbound chiffré e2e

### Enrichissements existants
- **Outcomes** : max_iterations 3 default / 20 max, 8 webhook event types
- **Dreaming** : 100 sessions max par dream, header `dreaming-2026-04-21`, modèles Opus 4.7 + Sonnet 4.6 uniquement
- **Webhooks Managed Agents** : 8 events, at-least-once delivery, X-Webhook-Signature 5min replay protection

## Patterns canoniques émergents (CwC SF + London + écosystème)

### Advisor Strategy ([[Brad-Abrams]], CwC SF 6 mai 2026)

Talk avec **Mario Rodriguez** (GitHub CPO) : *"Caching, harnesses, and advisors: Building on Claude at GitHub scale"*.

Pattern :
- **Executor model** : smaller (Haiku), exécute la majorité des appels
- **Advisor model** : larger (Opus), consulté ponctuellement

Verbatim Brad Abrams :
> "We get close to Opus-level intelligence at much lower prices because we're being very conservative about the tokens that advisor actually sends"

Pattern utilisé chez GitHub Copilot à scale. Mario Rodriguez : cache hit rate > 94% comme métrique foundational ("1% efficiency means millions overall").

⚠️ Coquille corrigée 23 mai 2026 : avant cet audit, le vault forge attribuait à tort cette stratégie à "Angela Jiang 5× cost reduction" — coquille propagée depuis Simon Willison "Angela Kiang". Source canonique : [[Brad-Abrams]].

### Harness engineering ([[Mitchell-Hashimoto]], 5 fév 2026)

Concept "Agent = Model + Harness" :
- **Popularisé** par Hashimoto ([mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey)) — il hedge lui-même sur la paternité ("I didn't coin")
- Formalisé par LangChain (Vivek Trivedy, 17 fév 2026)
- Repris par Birgitta Böckeler (Thoughtworks, martinfowler.com 2 avril 2026) — "guides + sensors"
- Repris par Addy Osmani (qualitatif)

### Justin Young 2-agent ([[Justin-Young]], post Anthropic engineering)

Pattern Initializer + Coding agent. **Footnote 1 verbatim** : *"The system prompt, set of tools, and overall agent harness was otherwise identical"*. **Pas de split Opus/Sonnet** dans l'article (extrapolation forge corrigée 23 mai 2026).

### 9 catégories skills ([[Thariq Shihipar]], post Anthropic mars 2026)

Post *"Lessons from Building Claude Code: How We Use Skills"* : Anthropic runs hundreds of Skills internally, organized into 9 categories. Détail dans [[comment-creer-skill]].

### Pipeline architect → dev → reviewer → test (doctrine forge)

Pipeline recommandé tâches M/L/XL, conditionnel (skip selon taille). Détail dans [[methode-analyser-repo]].

## Liens audit 23 mai 2026

- [[CHANGELOG]] section "Audit thématique vault Claude Code" (23 mai 2026)
- [[comparaison-skill-anthropic-claude-code-setup]]
- `.claude/rules/sequence-canonique-modification.md` — rule transverse créée (hors vault)
- [[methode-analyser-repo]] — pipeline architect/dev/reviewer/test explicité
- [[Brad-Abrams]] — fiche leader créée
- [[Mitchell-Hashimoto]] — fiche leader créée
