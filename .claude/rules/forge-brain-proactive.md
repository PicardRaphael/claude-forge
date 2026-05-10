---
description: Query forge-brain vault proactively — at session start, before creating components, after learning, and after mistakes
globs: "*"
---

# Forge Brain — Requêtage proactif

Le vault forge-brain est la mémoire infinie. L'interroger est un RÉFLEXE, pas une option.

## COMMENT interroger — MCP forge-brain (OBLIGATOIRE)

Le MCP `forge-brain` (auto-start via hook SessionStart, port 8091) est le SEUL moyen d'accès au vault.
Ne JAMAIS utiliser Grep/Read/Glob brut sur le vault. Ne JAMAIS utiliser la CLI Obsidian.

### Outils MCP disponibles

| Outil | Usage |
|-------|-------|
| `search_brain(query, limit)` | Recherche full-text FTS5 sur tout le vault |
| `read_note(file)` | Lire une note par nom ou alias |
| `read_note_by_path(path)` | Lire par chemin exact |
| `get_backlinks(file)` | Naviguer le graphe de liens |
| `get_tags()` | Vue structurelle par tags |
| `get_property(file, name)` | Lire une propriété frontmatter |
| `list_notes(folder, limit)` | Lister les notes d'un dossier |
| `vault_stats()` | Stats vault (notes, tags, wikilinks, aliases) |
| `create_note(path, content)` | Créer une note |
| `append_note(file, content)` | Ajouter du contenu à une note |
| `update_property(file, name, value)` | Modifier une propriété frontmatter |

### Fallback (MCP crash uniquement)

Si le MCP ne répond pas malgré l'auto-start → Read/Glob direct sur `vault/claude-forge/`.
Ce cas ne devrait jamais arriver en usage normal.

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

| Situation | Dossier | Note |
|-----------|---------|------|
| Contexte de projet | `1-Projets/<nom>/` | 1 note/projet |
| Casquette de vie | `2-Casquettes/` | 1 note/casquette |
| Capture rapide à trier | `0-Inbox/` | temporaire |
| Feature Claude Code | `01-Claude-Code/features/` | 1 note/feature |
| Deprecation Claude Code | `01-Claude-Code/deprecations/` | 1 note/deprecation |
| Changelog CC (par mois) | `01-Claude-Code/changelog/` | 1 note/mois |
| Best practice CC | `01-Claude-Code/best-practices/` | 1 note/pattern |
| Agent CC documenté | `01-Claude-Code/agents/` | 1 note/agent |
| Produit concurrent | `02-Concurrents/<entreprise>/` | 1 note/produit (ChatGPT, Codex, Gemini, CLI...) |
| Modèle IA (specs, benchmarks) | `03-Modeles/<provider>/` | 1 note/modèle (GPT-5.5, Gemini 3...) |
| Technique RAG | `04-Techniques/rag/` | 1 note/technique |
| Technique agents | `04-Techniques/agents/` | 1 note/pattern |
| Technique prompt engineering | `04-Techniques/prompt-engineering/` | 1 note/technique |
| Technique fine-tuning | `04-Techniques/fine-tuning/` | 1 note/technique ou framework |
| Pattern/workflow réutilisable | `04-Techniques/patterns/` | 1 note/pattern |
| Context engineering | `04-Techniques/context-engineering/` | 1 note/concept |
| Leader RAG/embeddings | `05-Leaders/rag/` | 1 note/personne |
| Leader agents/automation | `05-Leaders/agents/` | 1 note/personne |
| Leader fine-tuning/local AI | `05-Leaders/fine-tuning/` | 1 note/personne |
| Leader prompt engineering | `05-Leaders/prompt/` | 1 note/personne |
| Leader industrie/CEO | `05-Leaders/industrie/` | 1 note/personne |
| Leader Claude Code/Anthropic | `05-Leaders/claude-code/` | 1 note/personne |
| News industrie (événement, funding) | `06-Industrie/` | 1 note/événement |
| System prompt réutilisable | `07-Prompts/system-prompts/` | 1 note/prompt |
| Technique de prompting | `07-Prompts/techniques/` | 1 note/technique |
| Index "quelle technique quand" | `07-Prompts/techniques/index-prompting.md` | 1 note unique |
| Erreur commise | `Knowledge/erreurs/` | 1 note/erreur |
| Critique devil's advocate | `Knowledge/critiques/` | 1 note/critique |
| Synthèse d'analyse | `Knowledge/syntheses/` | 1 note/synthèse |
| Question technique résolue | `Knowledge/questions/` | 1 note/question |
| Raisonnement multi-étapes | `Knowledge/raisonnements/` | via /reasoning-cache |
| Évolution de skill | `Knowledge/evolutions/` | via /skill-evolve |
| Review stratégique | `Knowledge/reviews/` | via /forge-review |

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
