---
titre: "CC v2.1.126"
resume: "Model picker gateway, project purge, PermissionDenied hook, PowerShell primary Windows, OTel skills"
type: changelog
version: 2.1.126
date: 2026-05-01
derniere-maj: 2026-05-04
auteur: claude
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

# CC v2.1.126 — 1er mai 2026

## Features

- `/model` picker liste les modeles depuis `/v1/models` quand `ANTHROPIC_BASE_URL` pointe vers un gateway compatible
- `claude project purge [path]` — supprime tout l'etat CC d'un projet (transcripts, tasks, file history, config entry). Flags : `--dry-run`, `-y/--yes`, `-i/--interactive`, `--all`
- `--dangerously-skip-permissions` bypass maintenant writes vers `.claude/`, `.git/`, `.vscode/`, shell configs (catastrophic removal toujours prompt)
- `claude auth login` accepte le code OAuth colle dans le terminal (WSL2, SSH, containers)
- **OpenTelemetry** : `claude_code.skill_activated` event avec `invocation_trigger` (`user-slash`, `claude-proactive`, `nested-skill`)
- Auto mode : spinner rouge quand permission check bloque
- Host-managed deployments ne desactivent plus analytics auto sur Bedrock/Vertex/Foundry
- `CLAUDE_CODE_NO_FLICKER=1` — rendu alt-screen sans scintillement avec scrollback virtualise
- **PermissionDenied hook** — fire apres deny auto mode classifier, `{retry: true}` permet retry
- `X-Claude-Code-Session-Id` header sur requetes API (proxies)
- `.jj` et `.sl` exclus des VCS directories (Jujutsu, Sapling)

## Windows

- PowerShell est maintenant le shell principal quand PowerShell tool active (plus Bash par defaut)
- PowerShell 7 detecte via Microsoft Store, MSI sans PATH, .NET global tool
- Clipboard writes ne sont plus exposes dans les arguments de processus visibles par EDR/SIEM
- Fix selections >22KB ne passant pas dans le clipboard
- Fix CJK/Japonais/Coreen/Chinois garbled en mode no-flicker

## Bug Fixes

- Read tool : suppression reminder malware-assessment (refus spurious anciens modeles)
- Fix images >2000px cassant la session (downscale auto, retry)
- Fix OAuth login timeout (slow connections, IPv6, localhost callback)
- Fix race credential write OAuth refresh token
- Fix API retry countdown bloque a "0s"
- Fix "Stream idle timeout" apres wake Mac sleep
- Fix background/remote sessions false abort pendant thinking pauses
- Fix hang assistant finish thinking sans output
- Fix trackpad scrolling trop rapide Cursor/VS Code 1.92-1.104
- Fix claude.ai MCP connectors supprimes par servers needs-auth
- Fix `Ctrl+L` clearing prompt input (maintenant redraw only)
- Fix deferred tools indisponibles en `context: fork` et subagents au 1er turn
- Fix plan-mode tools indisponibles avec `--channels`
- Fix `/plugin` Uninstall affichant "Enabled"
- Fix file-modified reminders unbounded quand linter touche beaucoup de fichiers
- Fix `/remote-control` retries stuck "connecting..."
- Fix PowerShell bare `--` (git diff -- file) mis-flagge comme `--%`
- Fix Agent SDK hang sur malformed tool name en parallel tool call batch

## Security

- Fix `allowManagedDomainsOnly` / `allowManagedReadPathsOnly` ignores quand higher-priority managed-settings n'avait pas de bloc `sandbox`
