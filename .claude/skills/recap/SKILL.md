---
name: recap
description: Produces a 30-second project status snapshot — git state, vault stats, memory, cc-news date, and one-line context suggestion. Use when resuming a session after a break or switching context.
allowed-tools: Read, Glob, Grep, Bash
user-invokable: true
model: sonnet
effort: high
---

# recap — Snapshot de contexte claude-forge

Produit un snapshot complet de l'état du projet en < 10 secondes. **Read-only — aucune modification.**

Usage : `/recap`

## Étapes

### Phase unique — Collectes parallèles (OBLIGATOIRE)

Lancer **toutes les commandes ci-dessous dans un seul message** (parallel tool_use). Ne pas attendre le résultat de l'une pour lancer la suivante.

#### Collecte 1 — Git état

```bash
git status -sb | head -5
git log --oneline --format="%h — %s (%ar)" -5
```

#### Collecte 2 — Vault stats

Utiliser les outils MCP forge-brain :

```
forge-brain:vault_stats
```
Donne : nombre total de notes, tags, wikilinks, aliases, répartition par dossier.

```
forge-brain:get_tags
```
Donne le top des tags par fréquence. Afficher les 10 premiers dans le rapport.

```bash
# Notes modifiées dans les 7 derniers jours — ordre plus récent en premier
# (find est le seul usage acceptable ici : le MCP n'a pas de filtre par date de modification)
find vault/claude-forge -name "*.md" ! -path "*/Templates/*" -mtime -7   -printf "%T@ %p
" 2>/dev/null | sort -rn | head -10 | cut -d' ' -f2-
```

#### Collecte 3 — Derniers feedbacks mémoire

```bash
ls -lt ~/.claude/projects/$(claude-project-id)/memory/feedback_*.md 2>/dev/null | head -5
```

#### Collecte 3b — Dernières erreurs vault

Utiliser l'outil MCP forge-brain :

```
forge-brain:search_brain  query="erreur" limit=5
```

Lire le **resume** frontmatter de chaque note trouvée pour l'afficher dans le rapport.

#### Collecte 3c — Dernières notes Knowledge

```bash
# find est ici le seul usage acceptable : le MCP n'a pas de filtre par date de modification
find vault/claude-forge/Knowledge -name "*.md" -mtime -14 -printf "%T@ %p
" 2>/dev/null | sort -rn | head -5 | cut -d' ' -f2-
```

#### Collecte 3e — Dernières notes contexte (projets + casquettes)

```bash
# find est ici le seul usage acceptable : le MCP n'a pas de filtre par date de modification
find vault/claude-forge/1-Projets vault/claude-forge/2-Casquettes -name "*.md" -mtime -14 -printf "%T@ %p
" 2>/dev/null | sort -rn | head -5 | cut -d' ' -f2-
```

#### Collecte 3d — Best practices et techniques récentes

Utiliser l'outil MCP forge-brain :

```
forge-brain:search_brain  query="best practices" limit=5
```

#### Collecte 4 — Date de référence cc-news

Utiliser l'outil Grep :
- pattern: `Date de référence`
- file: `.claude/skills/cc-news/SKILL.md`
- output_mode: content

#### Collecte 5 — Compteurs composants

```bash
ls .claude/agents/*.md 2>/dev/null | wc -l
ls -d .claude/skills/*/ 2>/dev/null | wc -l
```

### Phase 2 — Compilation du rapport

Agréger les résultats et produire le rapport au format suivant :

```
# Recap — claude-forge

**Branche :** [branch] ([N ahead/behind] ou "à jour")
**Dernière activité :** [hash] — [message] ([temps relatif])

## Git — 5 derniers commits
1. [hash] — [message] ([temps relatif])
2. ...

Fichiers modifiés : [liste depuis git status -sb, ou "répertoire propre"]

## Vault forge-brain
- [N] notes totales
- [N] notes modifiées < 7 jours : [noms fichiers, pas chemins complets]
- Top 5 tags : [tag (count), ...]

## Composants
- [N] agents, [N] skills

## Mémoire
- Derniers feedbacks : [noms fichiers sans path, sans extension]

## Knowledge vault (dernières 2 semaines)
- Erreurs récentes : [resume de chaque note erreur récente]
- Synthèses : [notes Knowledge récentes]
- Techniques : [best practices trouvées]

## cc-news
- Date de référence : [date extraite]

## Suggestion
[Une phrase descriptive sur le contexte probable de la session]
```

La **Suggestion** se déduit des signaux observés :
- Commits récents → thème dominant de la session précédente
- Notes vault modifiées → sujets actifs dans le knowledge base
- Si > 5 commits non poussés → mentionner que des commits sont en attente
- Si vault 0 note nouvelle en 7 jours → contexte probablement code, pas documentation
- Si > 3 notes `Knowledge/erreurs/` modifiées récemment → période de correction active

## Gotchas

- **MCP forge-brain en premier, CLI en fallback** — utiliser `forge-brain:vault_stats`, `forge-brain:get_tags`, `forge-brain:search_brain` (MCP `localhost:8091`). Si le MCP est down, fallback CLI : `bash .claude/skills/forge-brain/scripts/obsidian-cli.sh version 2>/dev/null`. Sur Windows ne jamais appeler `obsidian` directement, toujours via le wrapper.
- **`find -newer FILE` non-déterministe** — le mtime du fichier de référence change. Toujours `-mtime -7` pour "7 derniers jours"
- **Paths absolus sur Git Bash Windows** — `find vault/claude-forge` retourne `/c/Users/...`. Afficher seulement `basename` dans le rapport
- **Suggestion = descriptive, pas prescriptive** — "Activité récente sur X" et non "Vous devriez faire Y"
- **Parallélisation obligatoire** — collectes en séquentiel = > 10 secondes. Toute la phase 1 dans un seul round de tool_use
- **Read-only absolu** — aucun Write, Edit. Si delegate-guard bloque, une modification a été tentée par erreur
- **Chemin mémoire fixe** — `~/.claude/projects/<project-id>` spécifique à cette machine. Si `ls` échoue : afficher "mémoire non accessible" sans erreur fatale

## Apprentissage

Après une session utilisant `/recap`, noter en mémoire projet si :
- La Suggestion était juste → mémoriser le signal (ex : commits `feat: hooks` = session enforcement)
- Le vault n'a aucune note récente sur un sujet abordé → noter le gap pour capitalisation future
- La CLI Obsidian échoue → mémoriser la version cassante dans `reference_obsidian_cli_windows.md`
