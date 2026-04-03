# claude-forge 🔨

**Assistant personnel Claude Code — Conseiller, Créateur, Optimiseur**

Créé le : 31 mars 2026

## Ce que c'est

Un projet standalone installé dans `~/.claude/` qui t'assiste dans TOUS tes autres projets Claude Code.
Il conseille, crée, optimise et reste à jour automatiquement.

## Structure

```
claude-forge/
└── .claude/
    ├── CLAUDE.md                          ← mémoire et règles du studio
    │
    ├── agents/
    │   ├── project-analyzer.md            ← analyse un projet, propose tout
    │   ├── claudemd-optimizer.md          ← crée/optimise les CLAUDE.md
    │   ├── agent-creator.md               ← crée/modifie des agents
    │   ├── skill-creator.md               ← crée/modifie des skills
    │   └── hook-creator.md               ← crée/modifie des hooks
    │
    └── skills/
        ├── cc-advisor/SKILL.md            ← conseille le bon composant à créer
        ├── analyze-project/SKILL.md       ← /analyze-project <path> slash command
        ├── cc-features-ref/SKILL.md       ← référence toutes les features 2026
        ├── cc-agents-ref/SKILL.md         ← référence format agents
        ├── cc-skills-ref/SKILL.md         ← référence format skills
        ├── cc-hooks-ref/SKILL.md          ← référence format hooks
        └── cc-news/SKILL.md               ← cherche les dernières nouveautés
```

## Installation

```bash
# Copier dans ~/.claude/ pour l'avoir dans TOUS tes projets
cp -r .claude/* ~/.claude/

# Vérifier
claude /agents
claude /skills
```

## Utilisation

```bash
# Analyser un projet complet
/analyze-project /path/to/mon-projet

# Analyser plusieurs projets en parallèle
/batch "Run /analyze-project on: /path/neochat, /path/neodoc, /path/neomail"

# Besoin flou → le conseiller décide
"J'ai besoin d'automatiser mes PRs"

# Créer un composant
"Crée un agent qui audite mon codebase"
"Je veux une skill /commit pour mon projet"
"J'ai besoin d'un hook de formatage Python"

# Optimiser
"Optimise mon CLAUDE.md"
"Améliore cette skill"

# Rester à jour
"Quoi de neuf dans Claude Code ?"
```

## Modèles utilisés

- `opus + effort:max` → project-analyzer (analyse complexe + thinking)
- `sonnet + effort:high` → creators (génération réfléchie)
- `haiku` → tâches rapides

## Mise à jour

La skill `cc-news` vérifie automatiquement les nouveautés post 31 mars 2026
et met à jour la mémoire du projet.
