---
name: cc-cowork-ref
description: Reference for Claude Cowork, Dispatch, Agent Teams, and plugins marketplace. Use when configuring Cowork automations, Dispatch tasks, Agent Teams, or when user mentions Cowork, Dispatch, or collaborative agents.
user-invokable: false
---

# Reference — Claude Cowork, Dispatch & Agent Teams

_Mise a jour : 8 avril 2026_

## Claude Cowork

Produit agentic pour knowledge workers. Meme moteur que Claude Code, dans Claude Desktop, sans terminal.

| Aspect | Detail |
|--------|--------|
| Ou | Claude Desktop (macOS + Windows) |
| Acces | Pro ($20/mo), Max ($100-200/mo), Team ($30/user/mo), Enterprise |
| Execution | Dossier local autorise, VM isolee, sub-agents automatiques |
| Plugins | Cross-compatibles avec Claude Code via marketplace |

### Flux d'une tache

1. Decrire l'objectif
2. Claude presente un plan → attendre approbation
3. Claude execute : lit fichiers, appelle connecteurs, coordonne sub-agents
4. Rediriger a chaque etape

### Connecteurs disponibles

Google Drive, Gmail, Calendar, Slack, Jira, Linear, Asana, DocuSign, Apollo, Clay, Outreach, SimilarWeb, FactSet, Microsoft 365 (Outlook, SharePoint, OneDrive)...

## Dispatch (mars 2026)

Remote control : telephone (Claude mobile) → desktop (Cowork).

```
Mobile (interface) ←→ Cloud Anthropic ←→ Desktop (moteur d'execution)
```

| Feature | Detail |
|---------|--------|
| Taches persistantes | Assigner depuis mobile, recuperer plus tard |
| Schedule | "Verifie mes emails chaque matin" |
| Claude Code | Peut lancer Claude Code depuis Dispatch |
| API | Accessible via Claude API + Agent SDK |
| Pricing | Max d'abord, puis Pro. Teams : admin must enable |

### Configurer Dispatch

1. Claude Desktop → onglet Cowork
2. Activer Dispatch dans les settings
3. Installer Claude mobile
4. Les deux se connectent automatiquement via le meme compte

## Agent Teams (Claude Code — experimental)

Feature distincte de Cowork. Subagents qui se parlent directement.

### Activer

```json
// settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### Architecture

```
Team Lead (session principale)
  ├── Teammate A (instance Claude Code independante)
  ├── Teammate B
  └── Teammate C
      ↕ Task list partagee + Mailbox
```

- **Teammates** = instances Claude Code independantes (pas des subagents)
- Communication directe entre teammates (mailbox)
- Task list partagee pour coordination
- Chaque teammate a son propre contexte

### Difference subagents vs teammates

| | Subagents | Teammates (Agent Teams) |
|---|---|---|
| Communication | Rapportent au parent uniquement | Se parlent entre eux |
| Contexte | Heritent du parent | Independant |
| Skills/MCP | Du frontmatter agent | Heritent de project/user settings |
| Hooks | Partages | `TeammateIdle`, `TaskCreated`, `TaskCompleted` |
| Stabilite | Stable | Experimental |

### Hooks Agent Teams

| Hook | Declenchement | Blocage |
|------|--------------|---------|
| `TeammateIdle` | Un teammate n'a plus de tache | Non |
| `TaskCreated` | Nouvelle tache sur le board | Non |
| `TaskCompleted` | Tache terminee | Oui (exit 2 = renvoyer feedback) |

### Quand utiliser Agent Teams vs subagents

- **Subagents** : taches sequentielles, pipeline (architect → dev → reviewer)
- **Agent Teams** : taches paralleles independantes avec coordination (3 migrations en parallele)

## Plugins Cowork

### Types de composants

```
Plugin = bundle
  ├── Skills (actions auto-invoquees par Claude)
  ├── Connectors (OAuth vers services externes)
  └── Sub-agents (agents automatiques du bundle)
```

### Installation individuelle

1. Claude Desktop → Cowork → **Customize**
2. **Browse plugins** → Install
3. Ou upload un plugin custom

### Deploiement Team — 3 methodes

**1. Marketplace Cowork UI (le plus simple)**
- Admin cree marketplace dans l'interface web
- Par plugin : **auto-install** (tous), self-service (catalogue), hidden
- GitHub sync optionnel : merge PR → resync auto (30 min max)

**2. settings.json dans le repo (pour Claude Code)**
```json
{
  "extraKnownMarketplaces": {
    "neoteem-tools": {
      "source": { "source": "github", "repo": "acme/plugins" }
    }
  },
  "enabledPlugins": { "mon-plugin@neoteem-tools": true }
}
```
Membres recoivent au `git pull`.

**3. managed-settings.json (force totale, admin only)**
- Console admin OU fichier systeme MDM
- Fetch au demarrage + poll toutes les heures
- `strictKnownMarketplaces` = managed-only (impossible a contourner)
- **Priorite : server-managed > endpoint-managed > project > user > local**

### Bug connu

`enabledPlugins` dans `settings.local.json` est ignore si la cle n'existe pas dans `settings.json`. Workaround : mettre `"enabledPlugins": {}` dans settings.json.

### 11 plugins built-in

Bio, Research, Customer Support, Data, Enterprise, Search, Finance, Legal, Marketing, Product Management, Productivity, Sales.

### Sources plugin supportees

ZIP (Cowork UI), GitHub repo + marketplace.json, npm, git URL, git-subdir (monorepo).

## Securite — Points critiques

| Risque | Detail |
|--------|--------|
| ToxicSkills (Snyk, fev 2026) | 13.4% des skills publics vulnerables |
| CVE-2025-59536 | settings.json manipulable pour exec arbitraire |
| Audit Logs | Activite Cowork ABSENTE des logs — probleme pour industries regulees |
| Prompt injection | Skills malveillants peuvent exfiltrer des donnees |

**Conseil :** accorder acces uniquement aux dossiers et connecteurs qu'on accepte que Claude utilise de facon autonome.

## Microsoft Copilot Cowork (mars 2026)

Partenariat Anthropic/Microsoft. Meme architecture dans M365 Copilot.
- Version Microsoft : cloud (tenant M365), avec Work IQ (emails, fichiers, meetings)
- Version Anthropic : local sur le device

## Skills Cowork = Skills Claude Code

**Format identique.** Meme SKILL.md, meme frontmatter YAML, meme structure dossier. Cross-compatible sans modification.

### Scopes

| Scope | Emplacement | Disponibilite |
|-------|-------------|---------------|
| project | `.claude/skills/` | Claude Code dans ce projet |
| user | `~/.claude/skills/` | Claude Code + Cowork partout |
| plugin | via marketplace ou ZIP | Claude Code + Cowork partout |

Pour qu'une skill soit disponible dans Cowork, elle doit etre au scope `user` ou dans un plugin.

### Creer une skill Cowork

**Via l'interface :** Cowork → Customize → Skills → Skill Creator (interview guide)
**Via upload :** Zipper le dossier skill, uploader dans Customize → Skills
**Via Claude Code :** Creer dans `~/.claude/skills/` → disponible dans les deux

### Standard ouvert

[agentskills.io](https://agentskills.io) — spec ouverte, portable vers d'autres outils compatibles.

### Repos officiels

- [github.com/anthropics/skills](https://github.com/anthropics/skills) — skills officielles
- [github.com/anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) — plugins Cowork

## Taches planifiees

### Cowork Desktop

- Tous plans payes (Pro, Max, Team, Enterprise)
- `/schedule` dans le chat → configure intervalle
- **Machine doit etre eveillee + Claude Desktop ouvert** (sinon skip → relance au reveil)
- Acces a tous connecteurs et plugins installes
- **PAS de triggers partages** — chaque utilisateur configure les siens

### Depuis Claude Code (/schedule)

```bash
/schedule "0 9 * * 1-5" /brain-check    # lundi-vendredi 9h
/schedule "0 8 * * 1" /weekly-report     # lundi 8h
```

Necessite GitHub connecte (triggers cloud). Si bloque par l'orga → Task Scheduler local.

### Dispatch (mobile → desktop)

```
"Verifie mes emails chaque matin a 9h et resume les urgences"
"Chaque vendredi, fais un resume de la semaine dans un doc"
```

**Team : desactive par defaut.** Admin doit activer org-wide. Pas de granularite par utilisateur.

### Prompt optimal pour tache planifiee

```
Contexte : [qui tu es, quel projet]
Objectif : [ce que tu veux, mesurable]
Sources : [ou chercher l'info]
Format : [comment presenter le resultat]
Destination : [ou sauvegarder / envoyer]
```

## Gotchas

- Plugins cross-compatibles Cowork ↔ Claude Code, MAIS les teammates (Agent Teams) n'heritent PAS les skills/mcpServers du frontmatter — ils heritent de project/user settings
- Connecteurs Cowork passent par le cloud Anthropic, pas par le reseau local
- Dispatch necessite que le desktop soit allume et connecte
- Computer Use est en research preview (mars 2026) — pas stable pour production
- Skills projet (`.claude/skills/`) ne sont PAS visibles dans Cowork — utiliser `~/.claude/skills/` ou plugin
- ToxicSkills : 13.4% des skills publiques vulnerables (Snyk fev 2026) — auditer avant d'installer


## Apprentissage

Après chaque usage significatif, sauvegarder en mémoire projet les patterns efficaces et erreurs rencontrées.

_Aucune entrée pour le moment._
