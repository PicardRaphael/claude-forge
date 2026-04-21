---
titre: "Claude Code v2.1.110 — Release majeure"
resume: "TUI fullscreen, push notifs, PreCompact hook, channels, side chat, remote control élargi"
aliases: ["v2.1.110", "2.1.110"]
domaine: claude-code
type: changelog
derniere-maj: 2026-04-21
auteur: claude
sources: ["https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"]
tags: ["#type/changelog", "#domaine/claude-code"]
---

## Changements
- **`/tui fullscreen`** — Mode fullscreen sans scintillement
- **Push notifications** mobiles (Remote Control + config)
- **`autoScrollEnabled`** — Désactiver auto-scroll en fullscreen
- **Ctrl+G** — Dernière réponse Claude en commentaire dans éditeur
- **Ctrl+O** — Bascule normal ↔ verbose. Focus view → `/focus`
- **`--resume`/`--continue`** — Ressuscite tâches planifiées
- **Remote Control élargi** : `/autocompact`, `/context`, `/exit`, `/reload-plugins`
- **Write tool amélioré** — Informe quand on édite le diff IDE
- **PreCompact hook** — Blocage possible via exit code 2
- **`--channels`** — Relay approbation permissions vers téléphone
- **MCP tool result** — Override jusqu'à 500K chars
- **Session recap** active même sans télémétrie
- 25+ fixes

## Liens
- Suivant : [[CC v2.1.111]]
- [[MOC-Claude-Code]]
