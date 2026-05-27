---
name: commit-message-no-herestring-bash-tool
description: "Message de commit multi-lignes via le Bash tool (PowerShell/Windows) : here-string @'...'@ injecte un @ littéral en tête. Utiliser des -m répétés."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 492c167d-73c8-42da-8e57-f7b41a17bfa8
---

Le Bash tool tourne en PowerShell sous Windows. Un here-string `@'...'@` passé à `git commit -m` injecte le `@` comme premier caractère du titre du commit. Les `-m` répétés (1 par paragraphe) passent proprement.

**Why:** observé 27 mai (session A3), commit 1 titré "@ feat(skill):..." au lieu de "feat(skill):...", corrigé par `git commit --amend`.

**How to apply:** commit multi-lignes via Bash tool = `git commit -m "titre" -m "corps" -m "Co-Authored-By..."`. Jamais de here-string `@'...'@`. Cas distinct de [[erreur-hooks-bash-quoting-windows]] (qui porte sur `bash -c '...$()...'` dans les hooks) et du heredoc Git Bash (écriture de fichiers). Ici c'est spécifiquement le message de commit.
