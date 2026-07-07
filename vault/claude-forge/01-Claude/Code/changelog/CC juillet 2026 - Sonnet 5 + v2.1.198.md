---
titre: CC juillet 2026 — Sonnet 5 défaut + v2.1.191→202
resume: "Claude Code v2.1.191→202 : Sonnet 5 défaut (1M natif), /dataviz, Claude in Chrome GA, background agents auto-PR, hook matchers exact-match, Dynamic workflow size dans /config, AskUserQuestion no auto-continue, mode « default » renommé « Manual », sous-agents remontent erreurs API/partiels au parent"
derniere-maj: 2026-07-07
auteur: claude
sources:
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
  - "https://www.anthropic.com/news/claude-sonnet-5"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
aliases:
  - "CC juillet 2026"
  - "changelog CC juillet 2026"
  - "Sonnet 5 defaut Claude Code"
  - "v2.1.202"
  - "v2.1.199 slash-skills empilees"
  - "v2.1.200 mode Manual"
  - "hook matchers exact-match"
---

# CC juillet 2026 — Sonnet 5 + v2.1.191→198

> Scan cc-news du 2 juillet 2026. Versions postérieures à la référence précédente (v2.1.190). Vérifié en source primaire (CHANGELOG.md brut GitHub). Le CHANGELOG ne porte pas de dates — les versions sont ordonnées, dates fines via agrégateurs (non reproduites ici sauf Sonnet 5, sourcée anthropic.com).

## v2.1.202

- **`Dynamic workflow size`** dans `/config` — contrôle le nombre d'agents spawnés par les workflows ; attributs OTel `workflow.run_id` / `workflow.name` ajoutés à la télémétrie
- **Fix : re-invoquer une skill déjà chargée dupliquait ses instructions** (double contexte)
- `/review <pr>` repasse en **review single-pass rapide** (rollback du multi-pass)
- Fixes : crash Ctrl+R history search · `/rename` sessions background · mTLS handshake pendant rotation cert · Remote Control « Unknown command » · scripts workflow avec quotes unicode corrompues

## v2.1.201

- Sessions **Sonnet 5** : n'utilisent plus de rôle `system` en milieu de conversation pour les rappels harness

## v2.1.200

- **`AskUserQuestion` ne s'auto-continue plus par défaut** — opt-in d'un idle timeout via `/config`
- **Mode permission « default » renommé « Manual »** (CLI, `--help`, VS Code, JetBrains) — `--permission-mode manual` et `"defaultMode": "manual"` acceptés **à côté de** `default` (**non-breaking** : `default` reste valide, aucun frontmatter `permissionMode` forge à changer — cf [[permissionmode-enum-valid-values]])
- Salve de fixes **background agents** : crash startup si `disabledMcpServers`/`enabledMcpServers` non-array · sessions stoppées après sleep/wake · `daemon.lock` stale à PID recyclé · handover daemon jugé par build-timestamp · roster (corruption, champs préservés, tokens socket)
- Sous-agent coupé par rate-limit avant tout texte → résultat vide propre au lieu d'échec
- Fixes accessibilité (screen-reader glyphes/tables) · flicker tmux 3.4+ (synchronized output)

## v2.1.199

- **Slash-skills empilées** (`/skill-a /skill-b do XYZ`) → charge **jusqu'à 5 skills** en tête, plus seulement la première
- **Sous-agents coupés par rate-limit / erreur serveur → renvoient leur travail partiel au parent** au lieu d'échouer en silence
- **Sous-agents reportant une erreur API (ex : usage limit) comme un succès → l'erreur est désormais remontée au parent.** ⚠️ Atténue *partiellement* l'anti-pattern `post-dispatch-verify.md` : ne couvre PAS le Write-denied exit 0 → la vérif empirique post-dispatch reste obligatoire
- **Hooks `SessionStart` / `Setup` / `SubagentStart` : stderr sur exit 2 était caché → désormais affiché dans le transcript** (pertinent hooks forge Windows exit 2)
- `SendMessage` : détecte le misroute quand un agent respawné réutilise le nom d'un précédent → demande de recibler
- Streaming : réponse partielle conservée si erreur mid-stream (au lieu d'être jetée) · daemon Linux qui se tuait toutes les ~50s après shutdown sale · `claude stop` respecté par le respawn background
- 429 transitoires (hors usage limit) retentés avec backoff pour les subscribers · `CLAUDE_CODE_RETRY_WATCHDOG` monte le retry défaut à 300 · plan mode prompte enfin les tool calls navigateur state-changing (`browser_batch` read-only auto-allow)

## v2.1.197 — Claude Sonnet 5 défaut

- **Claude Sonnet 5 = nouveau modèle par défaut de Claude Code**, contexte natif **1M tokens**, pricing promo **$2/$10 par MTok jusqu'au 31 août**. Cf [[Sonnet 5]].

## v2.1.198

- `/dataviz` — skill de design de charts/dashboards + **validateur de palette de couleurs exécutable**
- **Claude in Chrome → GA**
- **Background agents (`claude agents`) auto-commit / push / ouvrent une draft PR** en fin de tâche worktree (au lieu de s'arrêter) — cohérent avec le feedback forge `pas-de-wakeup-pour-agents-background` (le harness pilote la fin des agents background)
- **L'agent Explore hérite du modèle de la session (cap Opus)** au lieu de tourner sur Haiku
- Sub-agents + compaction **héritent de la config extended-thinking**
- Sub-agents traitent les messages de leur agent lanceur comme direction de tâche, pas comme approbation utilisateur
- Agent Teams : un teammate mort sur erreur API reporte « failed » au lead
- Notifications background via hook `Notification` (`agent_needs_input` / `agent_completed`)
- Gateway : Claude Platform sur AWS (`anthropicAws`)
- Retrait du wizard `/agents` · highlight.js 11

## v2.1.196 — sécu spawn MCP

- **Sécu** : `claude mcp list`/`get` **ne spawn plus les serveurs `.mcp.json`** qu'un repo a auto-approuvés via un `.claude/settings.json` committé ; workspaces non fiables → « ⏸ Pending approval »
- Org default models (console admin) · watchdog streaming ON par défaut (abort/retry après 5 min sans event, `CLAUDE_ENABLE_STREAM_WATCHDOG=0`)
- Remote Control désactivé quand `ANTHROPIC_BASE_URL` pointe un host non-Anthropic
- `/code-review` : 5 finders cleanup fusionnés en 1 (−25 % tokens)

## v2.1.195 — hook matchers exact-match

- **Hook matchers avec identifiants hyphénés → exact-match** (avant : substring accidentel). Pour matcher tous les tools d'un serveur MCP hyphéné : `mcp__brave-search__.*`.
  - **Impact forge vérifié = NUL** : les matchers `.claude/settings.json` forge listent des noms MCP complets (`mcp__forge-brain__append_note`…), pas de wildcard sur serveur hyphéné. Rien à corriger.
- `CLAUDE_CODE_DISABLE_MOUSE_CLICKS` · fix plugins externes activés par project settings nécessitant consent d'install

## v2.1.193

- `autoMode.classifyAllShell` (route tout Bash/PowerShell via classifier auto)
- Raisons de refus auto-mode dans transcript + toast + `/permissions`
- MCP `headersHelper` : re-run + reconnexion sur 401/403 · notice startup si serveurs MCP à authentifier
- Plugin auto-rename suit les maps `renames` du marketplace automatiquement

## v2.1.191

- `/rewind` supporte la reprise **avant** un `/clear`
- Fix hooks à matchers séparés par virgule (`"Bash,PowerShell"`) qui ne firaient jamais
- Fixes MCP OAuth (retry transitoire), messages d'erreur MCP (404 montre l'URL)

## Liens

- [[Sonnet 5]] — modèle défaut
- [[CC juin 2026 - v2.1.160 ultracode]] — changelog précédent
- [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]]
- [[MOC-Claude-Code]]
