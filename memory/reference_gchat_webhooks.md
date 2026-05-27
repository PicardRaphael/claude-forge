---
name: gchat-webhooks-neoteem
description: Google Chat webhook URLs and hook setup for ia_back, neo_ia, neoteem-brain push notifications
type: reference
---

## Webhooks Google Chat — Notifications push

3 repos ont des notifications push vers Google Chat :

| Repo | Espace Google Chat | Type notif |
|------|-------------------|------------|
| ia_back | AAQAt5B7YjU | "ALERTE CODE EN MOUVEMENT" |
| neo_ia | AAQAt5B7YjU (meme espace) | "ALERTE CODE EN MOUVEMENT" |
| neoteem-brain | AAQADXw8GqU (espace different) | "ALERTE CERVEAU EN MOUVEMENT" |

### Double hook

Chaque repo a DEUX mecanismes :
1. **Claude Code hook** (PostToolUse/Bash async) — se declenche quand Claude fait `git push`
2. **Git pre-push hook** (`.githooks/pre-push` Python) — se declenche pour tout le monde (terminal, IDE, Claude)

Le git hook necessite : `git config core.hooksPath .githooks` (a faire par chaque dev apres clone/pull).

### Stack hooks

- ia_back : Claude hook en TS (bun), git hook en Python
- neo_ia : Claude hook en Python, git hook en Python
- neoteem-brain : Claude hook en Python, git hook en Python

### Webhook claude-forge (rapport session)

Espace dedie pour les rapports de session claude-forge :
- Espace Google Chat : AAQAxJ9oKec
- Utiliser pour envoyer des rapports de session, alertes, ou notifications du forge
