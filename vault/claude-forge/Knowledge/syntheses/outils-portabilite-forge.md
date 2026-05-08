---
titre: "Outils portabilité forge — Installation multi-PC"
resume: "Liste des outils CLI à installer quand on utilise claude-forge depuis un nouveau PC : defuddle, yt-dlp, obsidian-cli, node, python"
aliases:
  - outils forge
  - installation forge
  - portabilité forge
  - setup nouveau PC
  - outils CLI forge
type: knowledge
derniere-maj: 2026-05-08
auteur: claude
sources: []
tags:
  - "#type/knowledge"
  - "#domaine/claude-code"
---

## Contexte

claude-forge est utilisé depuis plusieurs PCs. Certains outils CLI doivent être installés localement car ils ne font pas partie du repo git.

## Outils requis

### Obligatoires (core)

| Outil | Installation | Usage |
|-------|-------------|-------|
| **Node.js** (>= 18) | [nodejs.org](https://nodejs.org) | Runtime pour Claude Code, MCP, defuddle |
| **Python** (>= 3.11) | [python.org](https://python.org) | Hooks, scripts, yt-dlp |
| **Git** | [git-scm.com](https://git-scm.com) | Versionning |
| **Claude Code** | `npm install -g @anthropic-ai/claude-code` | Agent principal |

### Outils extraction web

| Outil | Installation | Usage |
|-------|-------------|-------|
| **defuddle** | `npm install -g defuddle-cli` | Extraction contenu propre de pages web (par Kepano/Obsidian) |
| **yt-dlp** | `pip install yt-dlp` | Extraction transcriptions YouTube, sous-titres |

### Optionnels (améliore l'expérience)

| Outil | Installation | Usage |
|-------|-------------|-------|
| **ffmpeg** | [ffmpeg.org](https://ffmpeg.org) | Améliore yt-dlp (meilleurs formats) |
| **deno** | [deno.land](https://deno.land) | JS runtime pour yt-dlp YouTube extraction |
| **Obsidian** | [obsidian.md](https://obsidian.md) | Vault viewer/editor |

## Script d'installation rapide

```powershell
# PowerShell — à lancer sur un nouveau PC
npm install -g defuddle-cli @anthropic-ai/claude-code
pip install yt-dlp
```

## Vérification

```bash
defuddle --version
python -m yt_dlp --version
claude --version
node --version
git --version
```

## Notes Windows

- `yt-dlp` s'installe via pip mais le binaire peut ne pas être dans le PATH Git Bash. Utiliser `python -m yt_dlp` en fallback.
- `defuddle` nécessite Node.js global.
- Les hooks Python de claude-forge utilisent le Python du PATH système.

## Liens

- [[RAG]] — yt-dlp utile pour extraire transcriptions vidéos RAG
