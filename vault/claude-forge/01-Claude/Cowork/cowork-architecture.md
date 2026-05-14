---
titre: "Architecture Claude Cowork — Vue d'ensemble"
resume: "Architecture Claude Cowork — produit agentique knowledge workers avec VM isolee, 38+ connecteurs, plugins cross-compatibles CC, Dispatch mobile et Routines cloud"
aliases:
  - "cowork architecture"
  - "claude cowork overview"
  - "cowork vue d'ensemble"
  - "cowork guide"
  - "cowork plugins architecture"
domaine: claude-code
type: technique
derniere-maj: 2026-05-14
auteur: claude
sources:
  - "https://claude.com/blog/cowork-plugins-across-enterprise"
  - "https://support.claude.com/en/articles/13947068-assign-tasks-to-claude-from-anywhere-in-cowork"
  - "https://claude.com/blog/product-management-on-the-ai-exponential"
tags:
  - "#type/technique"
  - "#domaine/cowork"
  - "#domaine/claude-code"
---

## Qu'est-ce que Cowork

Produit agentique pour knowledge workers. Meme moteur que Claude Code, dans Claude Desktop, sans terminal. Cat Wu : "Claude.ai = thought partner, Claude Code = building, Cowork = everything else."

| Aspect | Detail |
|--------|--------|
| Ou | Claude Desktop (macOS + Windows) |
| Acces | Pro ($20/mo), Max ($100-200/mo), Team ($30/user/mo), Enterprise |
| Execution | Dossier local autorise, VM isolee, sub-agents automatiques |
| Modele | Opus 4.7 par defaut (depuis avril 2026) |

## 3 surfaces Claude Code (Cat Wu, CwC 2026)

1. **CLI** — customisations/controle, hooks, skills, agents
2. **IDE** — agents dans l'UI pour tracker les changements
3. **Desktop** — GUI plein ecran avec preview/rich outputs (= Cowork)

## Plugins

Un plugin = bundle de 3 composants :

```
Plugin
  ├── Skills (actions auto-invoquees par Claude)
  ├── Connectors (OAuth via MCP vers services externes)
  └── Sub-agents (agents automatiques du bundle)
```

### 38+ connecteurs disponibles

Google Drive, Gmail, Calendar, Slack, Jira, Linear, Asana, DocuSign, Apollo, Clay, Outreach, SimilarWeb, FactSet, Microsoft 365 (Outlook, SharePoint, OneDrive)...

### Scope des plugins

Plugins cross-compatibles Cowork ↔ Claude Code. Organisations peuvent creer des **marketplaces privees**. GitHub repos prives comme source (beta).

### Hierarchie des skills

Enterprise > Personal > Project. Plugin skills utilisent le namespace `plugin-name:skill-name`.

### 11 plugins built-in

Bio, Research, Customer Support, Data, Enterprise, Search, Finance, Legal, Marketing, Product Management, Productivity, Sales.

### 3 methodes de deploiement team

1. **Marketplace Cowork UI** — admin cree marketplace, par plugin : auto-install / self-service / hidden
2. **settings.json dans le repo** — `extraKnownMarketplaces` + `enabledPlugins`, membres recoivent au git pull
3. **managed-settings.json** — force totale, admin only, fetch au demarrage + poll horaire

## Dispatch (mars 2026)

Remote control : telephone (Claude mobile) → desktop (Cowork).

```
Mobile (interface) ←→ Cloud Anthropic ←→ Desktop (moteur d'execution)
```

Taches persistantes, scheduling ("verifie mes emails chaque matin"), peut lancer Claude Code. Necessite Max plan + desktop allume.

## Routines (cloud execution)

Execution cloud pour taches planifiees/recurrentes. Corrige la limitation desktop (machine doit etre eveillee).

## Direction produit (Cat Wu, mai 2026)

### Les 3 phases

1. **Synchrone** — dev real-time back-and-forth (actuel)
2. **Automation de routines** — taches recurrentes (support client, reporting)
3. **IA proactive** — Claude anticipe les besoins avant qu'on les articule

> "Claude understands what you work on, and just sets up some of these automations for you."

### Dreaming dans Cowork

Process background qui analyse les sessions passees, detecte les patterns, restructure la memoire. Harvey : 6x improvement en completion.

## Securite

| Risque | Detail |
|--------|--------|
| ToxicSkills (Snyk, fev 2026) | 13.4% des skills publics vulnerables |
| CVE-2025-59536 | settings.json manipulable pour exec arbitraire |
| Audit Logs | Activite Cowork ABSENTE des logs — probleme pour industries regulees |
| Prompt injection | Skills malveillants peuvent exfiltrer des donnees |

Conseil : accorder acces uniquement aux dossiers et connecteurs qu'on accepte que Claude utilise de facon autonome.

Simon Willison : "I do not think it is fair to tell regular non-programmer users to watch out for suspicious actions that may indicate prompt injection."

## Gotchas

- Skills dans `.claude/skills/` = PAS visibles dans Cowork. Utiliser `~/.claude/skills/` ou plugin
- Connecteurs passent par le cloud Anthropic, pas par le reseau local
- Dispatch necessite desktop allume et connecte
- Computer Use est en research preview (mars 2026) — pas stable
- Bug #50669 : Cowork ne charge que 3/27 skills personnelles
- Budget contexte plus serre (plugins + MCP en competition)

## Liens

- [[cowork-skills-reliability]] — Problemes de fiabilite skills
- [[skills-guide]] — Format identique CC ↔ Cowork
- [[hooks-guide]] — Hooks pour enforcement dans Cowork
- [[prompting-chat-cowork-code]] — Differences de prompting par plateforme
- [[agents-orchestration]] — Agent Teams et multi-agent
