---
titre: "CC juillet 2026 — Opus 5 + v2.1.212 → v2.1.220"
resume: "Série 17-25 juillet : Opus 5 défaut Opus (2.1.219), /fork background + /subtask (2.1.212), tool EndConversation + patch sécu permissions PowerShell 5.1 (2.1.214), flip-flop nesting subagents (off 2.1.217 → depth 3 2.1.219), skills context:fork en background par défaut (2.1.218), param mode du Task tool déprécié"
aliases:
  - "CC v2.1.220"
  - "CC v2.1.219"
  - "CC v2.1.212"
  - "changelog CC fin juillet 2026"
  - "claude code 2.1.212-220"
domaine: claude-code
type: changelog
derniere-maj: 2026-07-27
auteur: claude
sources:
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
  - "https://github.com/anthropics/claude-code/releases"
  - "https://www.anthropic.com/news/claude-opus-5"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

Suite de [[CC juillet 2026 - v2.1.203-211]]. Fenêtre 17-25 juillet 2026, 8 versions (2.1.213 sautée).

## v2.1.212 (17 juil.)

- **`/fork` copie la conversation vers une session background** ; l'ancien fork in-session renommé **`/subtask`**
- **Paramètre `mode` du Task tool DÉPRÉCIÉ (ignoré)** — les subagents héritent du permission mode parent
- Caps par session : **200 WebSearch** + **200 spawns de subagents** (défauts)
- Appels MCP > 2 min passent automatiquement en background
- `claude auto-mode reset` ; `/resume` en vue agent ouvre un picker de sessions passées
- Nombreux fixes (plan mode, worktree, SIGTERM, Windows, stream-json)

## v2.1.214 (18 juil.)

- **Gros patch sécurité permissions** : fix bypass du permission-check en **PowerShell 5.1** (⚠️ machines Windows), règles `dir/**` qui auto-approuvaient trop large, checks Bash fail-closed sur les redirects file-descriptor, commandes > 10 000 chars prompt toujours
- **Nouveau tool `EndConversation`** — Claude peut clore une session sur abus soutenu / tentatives de jailbreak
- SessionStart hooks : nouvelle source `'fork'`
- Heartbeat de progression sur les tool calls longs ; timestamp ISO `modified` dans le frontmatter memory
- Nouveaux attributs OpenTelemetry + `CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH` ; prompts sur `docker` avec flags daemon-redirect

## v2.1.215 (19 juil.)

- **Claude ne lance plus `/verify` ni `/code-review` de sa propre initiative** (invocation manuelle uniquement)

## v2.1.216 (20 juil.)

- Setting `sandbox.filesystem.disabled`
- Fix ralentissement quadratique en longues sessions ; fixes OAuth, AskUserQuestion, worktree, background sessions

## v2.1.217 (21 juil.)

- **Nesting des subagents DÉSACTIVÉ par défaut** + cap **20 subagents concurrents** (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) — revert partiel 3 jours plus tard, cf 2.1.219
- Autocomplete emoji (`emojiCompletionEnabled`) ; warnings sur les échecs d'écriture transcript
- Fixes memory leak MCP, auto-update Windows, background sessions

## v2.1.218 (22 juil.)

- **`/code-review` tourne en subagent background**
- **Skills `context: fork` passent en background par défaut** (opt-out `background: false`)
- Noms d'agents avec `:` rejetés (réservé aux plugins) ; `/deep-research` sur invocation manuelle uniquement
- Annonces screen-reader pour suppressions mot/ligne ; fixes (chemins Windows, `/context`, `/ultrareview`, multi-line paste)

## v2.1.219 (24 juil.) — Opus 5

- **[[Opus 5]] (`claude-opus-5`) ajouté et devient le défaut Opus** — 1M contexte, fast mode $10/$50 par MTok
- **Opus 4.7 retiré du fast mode** (fast = Opus 5 + Opus 4.8)
- **Nesting subagents réactivé jusqu'à depth 3 par défaut** (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` pour revenir à l'ancien comportement) + forwarding stream-json des subagents depth 2+
- **Nouveau hook event `DirectoryAdded`** (fire après `/add-dir` ou ajout SDK d'un working directory mid-session)
- `sandbox.network.strictAllowlist`, `mcp_server_errors`, `workflowSizeGuideline`

## v2.1.220 (25 juil.)

- Bug fixes et améliorations de fiabilité

## Saga nesting subagents — lecture doctrine

Off par défaut le 21/07 (2.1.217) → réactivé depth 3 le 24/07 (2.1.219). Lecture : Anthropic assume désormais les hiérarchies d'agents profondes (3 niveaux) avec garde-fous quantitatifs (200 spawns/session, 20 concurrents) plutôt que l'interdiction. Impacte [[comment-creer-agent]] et [[anti-reentrance-sub-agents-pattern-escalade]].

## Liens

- [[CC juillet 2026 - v2.1.203-211]] — épisode précédent
- [[Opus 5]] — note modèle
- [[MOC-Claude-Code]]
