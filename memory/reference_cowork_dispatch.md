---
name: cowork-dispatch-reference
description: Claude Cowork GA + Dispatch (remote CC sessions + Computer Use) + Managed Agents beta + plugins Team propagation. Recherche 12 avril 2026.
type: reference
originSessionId: f3b37008-cac0-4a75-ae36-b058217ea80b
---
## Claude Cowork

Produit agentic Anthropic pour knowledge workers. Meme moteur que Claude Code, dans Claude Desktop, sans terminal.
- Launch : janvier 2026 (Mac), fevrier 2026 (Windows)
- **GA tous plans payes** (avril 2026) : RBAC, group spend limits, OpenTelemetry, usage analytics Enterprise
- Architecture : dossier local autorise, VM isolee, sub-agents automatiques
- Plugins cross-compatibles avec Claude Code via marketplace

## Dispatch (mars 2026, maj avril 2026)

Remote control : telephone (Claude mobile) → desktop (Cowork). Taches persistantes.
- **Lance maintenant des sessions Claude Code** (pas juste Cowork)
- **Computer Use integre** — agit sur l'ecran pendant absence utilisateur
- API + Agent SDK pour integrations tierces
- **Team : desactive par defaut, admin doit activer org-wide**
- Pas de granularite par utilisateur pendant la beta
- Risque prompt injection documente

## Managed Agents (beta publique, 8 avril 2026)

Harness d'agents heberge par Anthropic :
- Sandboxing, SSE streaming, $0.08/session-hour
- Adopte par Notion, Rakuten, Asana
- Distinct de Claude Code local — serverless

## Agent Teams (Claude Code)

Feature distincte, experimentale :
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- Team lead + Teammates + Task list partagee + Mailbox
- Teammates se parlent directement (vs subagents qui rapportent au parent)
- Hooks : `TeammateIdle`, `TaskCreated`, `TaskCompleted`
- Skills/mcpServers du frontmatter NE s'appliquent PAS aux teammates

## Plugin propagation Team — 3 methodes

### 1. Marketplace Cowork UI (le plus simple)
- Admin cree marketplace dans l'interface web
- Par plugin : **auto-install** (tous), self-service (catalogue), hidden
- GitHub sync optionnel : merge PR → resync auto (jusqu'a 30 min)
- Changements actifs au prochain refresh session

### 2. settings.json dans le repo (pour Claude Code)
```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": { "source": "github", "repo": "acme/plugins" }
    }
  },
  "enabledPlugins": {
    "mon-plugin@company-tools": true
  }
}
```
Membres recoivent au `git pull`. **Bug connu** : `enabledPlugins` dans settings.local.json ignore si la cle n'existe pas dans settings.json → mettre `"enabledPlugins": {}` dans settings.json.

### 3. managed-settings.json (force totale)
- Server-managed (console admin) : fetch au demarrage + poll toutes les heures
- Fichier systeme (MDM) : `/Library/Application Support/ClaudeCode/managed-settings.json` (mac) ou Registry Windows
- `strictKnownMarketplaces` = managed-only (impossible a contourner)
- **Server-managed > endpoint-managed > project > user > local**
- Drop-in directory : `managed-settings.d/*.json` mergent alphabetiquement

### Sources plugin
ZIP (Cowork UI), GitHub repo + marketplace.json, npm, git URL, git-subdir (monorepo)

## Taches planifiees (/schedule)

- Disponible tous plans payes (Pro, Max, Team, Enterprise)
- **Machine doit etre eveillee + Claude Desktop ouvert** (sinon skippee, relancee au reveil)
- Acces a tous connecteurs et plugins installes
- **PAS de triggers partages entre membres** — chaque utilisateur configure les siens
- Pas de cron centralise cote serveur pour Team

## Managed Settings — emplacements

| Mecanisme | Emplacement |
|-----------|-------------|
| Server-managed | Claude.ai → Admin → Claude Code → Managed settings |
| Fichier macOS | `/Library/Application Support/ClaudeCode/managed-settings.json` |
| Windows Registry | `HKLM\SOFTWARE\Policies\ClaudeCode` |
| Windows fichier | `C:\Program Files\ClaudeCode\managed-settings.json` |

Settings managed-only : `strictKnownMarketplaces`, `allowManagedPermissionRulesOnly`, `forceRemoteSettingsRefresh`

## Securite

- ToxicSkills (Snyk fev 2026) : 13.4% des skills publics vulnerables
- CVE-2025-59536 : settings.json manipulable
- Dispatch peut executer toute action que Cowork a permission de faire
- Pas de traces dans Audit Logs

## Microsoft Copilot Cowork

Partenariat Anthropic/Microsoft (9 mars 2026). Meme archi dans M365 Copilot, mais cloud (tenant M365).
