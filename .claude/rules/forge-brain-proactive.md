---
description: Query forge-brain vault proactively — at session start, before creating components, after learning, and after mistakes
globs: "*"
---

# Forge Brain — Requêtage proactif

Le vault forge-brain est la mémoire infinie. L'interroger est un RÉFLEXE, pas une option.

## COMMENT interroger — CLI Obsidian (OBLIGATOIRE)

Ne JAMAIS utiliser Grep/Read brut sur le vault. Toujours la CLI :

```bash
# Pre-check
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh version 2>/dev/null

# Chercher
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" search query="sujet" limit=10

# Lire une note
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" read file="Nom Note"

# Backlinks (naviguer le graphe)
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" backlinks file="Nom Note"

# Tags (vue structurelle)
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" tags sort=count counts

# Après écriture, mettre à jour derniere-maj
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" property:set name="derniere-maj" value="YYYY-MM-DD" file="Note"
```

Fallback Read/Glob/Grep si Obsidian est fermé (pre-check échoue).

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

## QUOI ÉCRIRE dans le vault

| Situation | Dossier | Template |
|-----------|---------|----------|
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
