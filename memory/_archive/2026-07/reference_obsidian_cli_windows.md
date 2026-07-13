---
name: obsidian-cli-windows-gotcha
description: On Windows Git Bash, `obsidian` resolves to Obsidian.exe (GUI) not Obsidian.com (CLI console) — must use wrapper script
type: reference
---

## Obsidian CLI sur Windows — Gotcha critique

Sur Windows, `C:\Program Files\Obsidian\` contient DEUX executables :
- `Obsidian.exe` — app GUI (ce que Git Bash resout par defaut)
- `Obsidian.com` — console CLI (ce qu'il faut utiliser)

Git Bash resout `obsidian` vers `.exe` (GUI) au lieu de `.com` (CLI). Le CLI ne produit aucune sortie, l'app s'ouvre juste.

### Fix : wrapper `obsidian-cli.sh`

Le wrapper dans `neo-brain/scripts/obsidian-cli.sh` resout automatiquement `Obsidian.com` sur Windows et fallback vers `obsidian` sur Linux/Mac.

Emplacements :
- Source : `claude-forge/output/neo-brain/scripts/obsidian-cli.sh`
- Deploye : `.claude/skills/neo-brain/scripts/obsidian-cli.sh` dans chaque repo
- Standalone : `neoteem-brain/neo-brain/scripts/obsidian-cli.sh`

### Activation CLI

La CLI est integree a l'app Obsidian (pas un plugin npm). Activer dans :
- Obsidian > Settings > General > Enable Obsidian CLI
- Verifie dans `%APPDATA%/obsidian/obsidian.json` : `"cli": true`

### Emojis dans git hooks Windows

Git Bash corrompt les emojis UTF-8 dans les heredocs bash. Utiliser Python pour les scripts qui envoient des emojis (webhooks Google Chat).
