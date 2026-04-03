---
name: install-forge
description: Installs claude-forge globally by copying .claude/* to ~/.claude/ with diff and verification. Use when the user says "installe forge", "deploy globally", "install forge", "cp to global".
user-invokable: true
disable-model-invocation: true
argument-hint: "[--dry-run]"
allowed-tools: Bash, Read, Glob
---

# Installation globale de claude-forge

## Étapes

### 1. Inventaire de l'existant

Lister ce qui est déjà installé globalement :
- `Glob` : `~/.claude/agents/*.md`
- `Glob` : `~/.claude/skills/*/SKILL.md`

### 2. Diff des composants

Pour chaque fichier dans `.claude/agents/` et `.claude/skills/`, vérifier s'il existe dans `~/.claude/` et montrer les différences :
- `Bash` : `diff .claude/agents/<name>.md ~/.claude/agents/<name>.md 2>/dev/null`

### 3. Dry-run check

Si `$ARGUMENTS` contient `--dry-run` : s'arrêter ici et afficher un résumé de ce qui serait copié/mis à jour.

### 4. Copie

```bash
mkdir -p ~/.claude/agents ~/.claude/skills ~/.claude/hooks
cp -r .claude/agents/* ~/.claude/agents/
cp -r .claude/skills/* ~/.claude/skills/
cp .claude/settings.json ~/.claude/settings.json
cp -r .claude/hooks/* ~/.claude/hooks/ 2>/dev/null
```

### 5. Vérification post-copie

Comparer le nombre de fichiers source vs installés.

## Exclusions

- Ne PAS copier `settings.local.json` (permissions locales au projet)
- Ne PAS copier `.claude/projects/` (mémoire spécifique au projet)

## Résultat attendu

Tableau : composant | action (copié/mis à jour/ignoré)
