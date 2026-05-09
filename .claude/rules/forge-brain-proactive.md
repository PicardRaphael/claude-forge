---
description: Query forge-brain vault proactively — at session start, before creating components, after learning, and after mistakes
globs: "*"
---

# Forge Brain — Requêtage proactif

Le vault forge-brain est la mémoire infinie. L'interroger est un RÉFLEXE, pas une option.

## COMMENT interroger — 3 niveaux (du plus rapide au fallback)

Ne JAMAIS utiliser Grep/Read brut sur le vault. Hiérarchie d'accès :

### Niveau 1 — MCP forge-brain (PRÉFÉRÉ si disponible)

Le MCP `forge-brain` (http://localhost:8091/mcp) offre un accès SQLite FTS5 ultra-rapide :
- `search_brain(query, limit)` — recherche full-text sur tout le vault
- `read_note(file)` — lire une note par nom ou alias
- `get_backlinks(file)` — naviguer le graphe
- `get_tags()` — vue structurelle

Le MCP doit être lancé manuellement : `python mcp-forge-brain/start.py`

### Niveau 2 — CLI Obsidian (si Obsidian ouvert)

```bash
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh version 2>/dev/null
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" search query="sujet" limit=10
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" read file="Nom Note"
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" backlinks file="Nom Note"
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" property:set name="derniere-maj" value="YYYY-MM-DD" file="Note"
```

### Niveau 3 — Read/Glob direct (fallback ultime)

Si MCP down ET Obsidian fermé, accès direct aux fichiers vault/ avec Read/Glob.
À éviter — pas de search, pas de FTS, pas d'aliases.

## QUAND INTERROGER le vault

### 1. Début de session
- Rechercher les notes récentes pertinentes au contexte
- Rappeler le contexte des sujets susceptibles d'être abordés

### 2. Avant de CRÉER un composant (skill, agent, hook, prompt, rule, CLAUDE.md)
- Chercher les best practices dans le vault (`04-Techniques/`, `07-Prompts/`)
- Chercher les erreurs passées dans `Knowledge/erreurs/` pour ne pas les répéter
- Chercher les patterns similaires déjà documentés
- Chercher les prompts réutilisables dans `07-Prompts/`

### 3. Avant de répondre sur un sujet technique
- Feature, outil, modèle, technique → chercher dans le vault AVANT de répondre
- Vérifier `derniere-maj` — si > 7 jours, compléter avec recherche web

### 4. Analyse de repo / projet
- Chercher dans le vault les concurrents, patterns, techniques pertinentes
- Croiser avec les notes existantes pour enrichir l'analyse

### 5. Après cc-news ou toute recherche web
- Capitaliser les découvertes en notes atomiques
- Mettre à jour les notes existantes si l'info a évolué
- Mettre à jour les MOCs

### 6. Après une erreur significative
- Créer une note dans `Knowledge/erreurs/` (template `erreur.md`)
- Documenter : ce qui s'est passé, pourquoi c'était une erreur, quoi faire à la place
- Lier aux notes techniques pertinentes

## STANDARD QUALITÉ — OBLIGATOIRE pour TOUTE note

Chaque note vault DOIT respecter ces minimums :

| Champ | Minimum | Exemple |
|-------|---------|---------|
| `aliases` | 4-6 (FR + EN + variantes + abréviations) | `["claude-forge", "forge", "le forge", "framework forge"]` |
| `resume` | 1 phrase complète, spécifique, pas générique | `"Backend IA Neoteem — FastAPI Python, agents autonomes, RAG"` |
| `derniere-maj` | Date ISO du jour | `2026-05-09` |
| `tags` | Au moins 2 (type + domaine) | `["#type/context", "#projet/neoteem"]` |
| Wikilinks | Minimum 2 liens vers notes liées | `[[Raphael-Picard]], [[Neoteem]]` |

### Aliases — comment les choisir
- Nom complet FR
- Nom complet EN (si pertinent)
- Abréviation / acronyme
- Variante avec/sans tirets/espaces
- Terme que l'utilisateur utiliserait en conversation
- Synonyme technique

### Dossiers de rangement (ontologie par utilité)

| Je crée une note sur... | Dossier |
|------------------------|---------|
| Un projet en cours | `1-Projets/<nom-projet>/` |
| Une aire de responsabilité de vie | `2-Casquettes/` |
| Une capture rapide à trier | `0-Inbox/` |

## QUOI ÉCRIRE dans le vault

| Situation | Dossier | Template |
|-----------|---------|----------|
| Contexte de projet | `1-Projets/<nom>/` | context-projet |
| Casquette de vie | `2-Casquettes/` | context-casquette |
| Capture rapide | `0-Inbox/` | - |
| Nouvelle feature/outil découvert | `01-Claude-Code/` ou `02-Concurrents/` | feature / concurrent |
| Nouveau modèle ou update | `03-Modeles/` | modele |
| Technique/pattern appris | `04-Techniques/` | technique |
| Prompt efficace créé | `07-Prompts/` | prompt |
| Erreur commise | `Knowledge/erreurs/` | erreur |
| Synthèse d'analyse | `Knowledge/syntheses/` | knowledge |
| Question technique résolue | `Knowledge/questions/` | knowledge |
| Exploration technique | `Knowledge/explorations/` | knowledge |
| Raisonnement réussi (multi-étapes) | `Knowledge/raisonnements/` | raisonnement |
| Critique adversariale (devil's advocate) | `Knowledge/critiques/` | critique |
| Évolution de skill proposée | `Knowledge/evolutions/` | evolution |
| Review stratégique forge | `Knowledge/reviews/` | review |

## Cycle d'apprentissage vault (Jarvis)

Le vault n'est pas qu'une base de connaissances — c'est le système nerveux de forge. Chaque agent y lit ET y écrit.

| Agent/Skill | Lit dans | Écrit dans |
|-------------|----------|------------|
| `devils-advocate` | `Knowledge/erreurs/`, `Knowledge/critiques/` | `Knowledge/critiques/` |
| `reasoning-cache` | `Knowledge/raisonnements/` (prior art) | `Knowledge/raisonnements/` |
| `skill-evolve` | Skills + `Knowledge/evolutions/` + mémoire | `Knowledge/evolutions/` |
| `forge-review` | CLAUDE.md + rules + skills + agents | `Knowledge/reviews/` |

Pas de Langfuse, pas d'outil externe. Le vault = single source of truth pour l'apprentissage.

## Vault path

`vault/claude-forge/`
