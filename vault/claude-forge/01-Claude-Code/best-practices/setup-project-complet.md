---
titre: "Setup projet Claude Code — Guide complet"
resume: "Toutes les configs, commandes, plugins et best practices pour setup un projet CC"
aliases:
  - "setup projet"
  - "configuration claude code"
  - "project setup guide"
domaine: claude-code
type: best-practice
derniere-maj: 2026-04-26
auteur: claude
sources:
  - "[[Best practices Boris Thariq]]"
  - "cc-features-ref"
  - "plugin claude-code-setup (Anthropic)"
tags:
  - "#type/best-practice"
  - "#domaine/claude-code"
---

## Permissions par stack

| Stack | Permissions `settings.json` |
|-------|----------------------------|
| Node/npm | `Bash(npm test:*)`, `Bash(npm run:*)`, `Bash(npx:*)` |
| Node/yarn | `Bash(yarn test:*)`, `Bash(yarn run:*)` |
| Node/pnpm | `Bash(pnpm test:*)`, `Bash(pnpm run:*)` |
| Python | `Bash(python -m pytest:*)`, `Bash(ruff:*)`, `Bash(pip:*)` |
| Go | `Bash(go test:*)`, `Bash(go build:*)` |
| Rust | `Bash(cargo test:*)`, `Bash(cargo build:*)` |
| Git (toujours) | `Bash(git *)` |
| TypeScript | `Bash(tsc:*)` |

## Variables d'environnement

| Variable | Quand | Effet |
|----------|-------|-------|
| `CLAUDE_CODE_NO_FLICKER: "1"` | Terminal | Renderer sans scintillement |
| `ENABLE_PROMPT_CACHING_1H: "1"` | API key / Bedrock / Vertex | Cache prompt 1h |
| `FORCE_PROMPT_CACHING_5M: "1"` | TTL court souhaité | Force TTL 5 min |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"` | Multi-agents coordonnés | Active Agent Teams |

## Flags CLI

| Flag | Usage | Quand recommander |
|------|-------|-------------------|
| `--worktree <feature>` / `-w` | Worktree isolé | Multi-feature en parallèle |
| `--tmux` | Session tmux dédiée | Linux/macOS/WSL |
| `--bare` | 10x plus rapide, sans UI | Scripts, CI, automatisation |
| `--agent <nom>` | Agent custom comme principal | Si agents spécialisés |
| `-p "<prompt>"` | Mode headless | CI/pre-commit |
| `--from-pr <url>` | Worktree depuis une PR | Workflow PR-based |
| `--add-dir <path>` | Multi-repo | Si dépendances cross-repo |
| `--continue` | Reprendre dernière session | Toujours utile |
| `--channels` | Permissions via mobile | Workflow remote |

## Slash commands clés

| Commande | Quand | Condition |
|----------|-------|-----------|
| `/compact` | Après analyse longue, AVANT implem | Toujours |
| `/compact "instructions"` | Compaction ciblée | Session complexe multi-sujets |
| `/clear` | Entre tâches non liées | Toujours — "piège #1" (Boris) |
| `/simplify` | Après implem majeure | Si code modifié |
| `/doctor` | Diagnostiquer MCP + config | Si MCP configurés |
| `/batch <instruction>` | Changement sur 5-30 fichiers | Refactor/migration |
| `/loop <interval> <skill>` | Polling régulier | Workflow récurrent |
| `/schedule "<cron>" <skill>` | Tâche planifiée | Besoin récurrent |
| `/recap` | Résumé au retour | Sessions longues |
| `/focus` | Focus view zone de code | Gros codebase |
| `/btw <note>` | Question sidebar coût zéro | Toujours |
| `/teleport` | Push vers claude.ai/code | Continuer sur web |
| `/autofix-pr` | Fix PR au cloud | Workflow PR-based |
| `/fewer-permission-prompts` | Réduire les prompts | Projet mature |

## Auto Mode (v2.1.119, Boris tip #1 Opus 4.7)

- **Shift+Tab** pour cycler : Ask → Plan → Auto
- Auto-approve via classifier ML — plus besoin de babysitter
- Disponible Opus 4.7 pour Max, Teams, Enterprise
- Combiné avec worktrees = parallélisme massif sans friction
- Alternative à `--dangerously-skip-permissions` (plus sûr)

## Best practices session (Boris)

- `/clear` entre tâches non liées — sessions fourre-tout = piège #1
- `/compact` proactif à 70% — pas attendre l'auto-compact
- "Document & Clear" — dump plan dans un .md, `/clear`, nouvelle session
- Vérification = tip #1 — toujours donner à Claude un moyen de vérifier son output (2-3x qualité)
- Hooks = 100% déterministe. CLAUDE.md = ~80%.
- Extension Chromium pour vérification frontend (Boris, avril 2026)
- `/fewer-permission-prompts` — nouvelle skill Anthropic pour tuner les permissions
- Recaps — résumé de session au retour, utile pour sessions longues

## .mcp.json — partage équipe

Checker dans git pour standardiser l'équipe. Exemple :
```json
{
  "mcpServers": {
    "context7": { "command": "npx", "args": ["-y", "@context7/mcp"] }
  }
}
```

## additionalDirectories

Si multi-repo, ajouter dans `settings.json` :
```json
{ "additionalDirectories": ["/chemin/vers/autre-repo"] }
```
**ATTENTION** : hooks doivent utiliser des chemins absolus si configuré.

## Plugins workflow

| Signal | Plugin | Install |
|--------|--------|---------|
| Git commits fréquents | `commit-commands` | `/plugin install commit-commands@claude-plugins-official` |
| Frontend React/Vue/Angular | `frontend-design` | `/plugin install frontend-design@claude-plugins-official` |
| Code auth/paiement/PII | `security-guidance` | `/plugin install security-guidance@claude-plugins-official` |
| Feature planning | `feature-dev` | `/plugin install feature-dev@claude-plugins-official` |
| Building plugins | `plugin-dev` | `/plugin install plugin-dev@claude-plugins-official` |

## Plugins LSP

| Langage | Plugin |
|---------|--------|
| TypeScript/JS | `typescript-lsp` |
| Python | `pyright-lsp` |
| Go | `gopls-lsp` |
| Rust | `rust-analyzer-lsp` |
| Java | `jdtls-lsp` |
| C/C++ | `clangd-lsp` |
| Kotlin | `kotlin-lsp` |
| C# | `csharp-lsp` |
| PHP | `php-lsp` |
| Swift | `swift-lsp` |
| Lua | `lua-lsp` |

Install : `/plugin install <nom>@claude-plugins-official`

## Hooks par framework

| Signal détecté | Hook recommandé |
|----------------|-----------------|
| Prettier config | PostToolUse Write\|Edit → auto-format |
| ESLint config | PostToolUse Write\|Edit → auto-lint |
| Ruff/Black config | PostToolUse Write\|Edit → format Python |
| tsconfig.json | PostToolUse Write\|Edit → tsc --noEmit |
| mypy/pyright config | PostToolUse Write\|Edit → type check |
| Test directory | PostToolUse Write\|Edit → run tests liés |
| `.env` files | PreToolUse Write\|Edit → bloquer |
| Lock files | PreToolUse Write\|Edit → bloquer |
| Go project | PostToolUse Write\|Edit → gofmt |
| Rust project | PostToolUse Write\|Edit → rustfmt |

## Liens

- [[MOC-Claude-Code]]
- [[Plugin Marketplace]]
- [[Best practices Boris Thariq]]
- [[analyse-plugin-claude-code-setup]]
