---
name: use-obsidian-cli-not-raw-files
description: TOUJOURS utiliser obsidian CLI (search, backlinks, tags, property:set, append, read) au lieu de Glob/Read/Write brut sur le vault
type: feedback
originSessionId: 00ed39aa-17db-4d58-bcdc-ef097926d20a
---
TOUJOURS utiliser la CLI Obsidian pour interagir avec le vault forge-brain, pas Glob/Read/Write brut.

**Why:** Le vault est un graphe de connaissance, pas un filesystem. Read/Write/Glob ignorent les backlinks, tags, recherche indexée, propriétés. La CLI donne accès à tout ça. neoteem-brain utilise le MCP obsidian-brain (SQLite FTS5) — encore mieux. Raphael a constaté que je n'utilise jamais la CLI malgré qu'elle soit configurée et fonctionnelle (v1.12.7).

**How to apply:**
- `obsidian search query="X"` au lieu de Grep sur le vault
- `obsidian read file="Note"` au lieu de Read avec chemin complet (résout les wikilinks)
- `obsidian backlinks file="Note"` pour naviguer le graphe
- `obsidian tags` pour vision structurée
- `obsidian property:set` pour mettre à jour derniere-maj
- `obsidian append` pour ajouter du contenu sans réécrire
- Write uniquement pour créer des notes (frontmatter avec : casse la CLI)
- Pre-check obligatoire : `obsidian-cli.sh version` → fallback Read/Write si Obsidian fermé
- Wrapper obligatoire Windows : `bash .claude/skills/forge-brain/scripts/obsidian-cli.sh`
