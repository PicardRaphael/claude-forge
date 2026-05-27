---
name: deny-global-ecrase-allow-projet
description: Permission Bash refusée malgré allow projet = chercher deny dans ~/.claude/ global EN PREMIER. Deny global > allow projet
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f598fcbc-1e1f-4161-bd42-75eddf13fbdf
---

Quand une commande Bash précise (`git commit`, `git push`) est refusée alors que `Bash(git *)` est en allow dans le settings PROJET, et que les sous-commandes simples (`git status`, `git add`, `git --version`) passent → la cause est un `deny` ciblé dans `~/.claude/settings.json` **global**.

**Why:** Précédence Claude Code = `deny` > `ask` > `allow`, et scope global écrase scope projet. Un deny global rend inopérant tout allow projet. Le 27 mai, j'ai perdu plusieurs tours à modifier le settings projet (bypassPermissions inutile) + redémarrer la session, avant que Raphael pointe le `.claude` global.

**How to apply:** Dès qu'une permission Bash est refusée malgré un allow projet → `Read ~/.claude/settings.json` AVANT toute autre hypothèse. Vérifier le bloc `deny`. Le deny est relu à chaud (pas besoin de redémarrer après édition). Le deny git global est un garde-fou volontaire — le modifier seulement avec accord explicite utilisateur.

Voir [[erreur-deny-global-ecrase-allow-projet]] (vault Knowledge/erreurs).
