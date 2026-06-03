---
name: install-forge
description: Installs claude-forge globally by copying .claude/* to ~/.claude/ with diff and verification. Use when the user says "installe forge", "deploy globally", "install forge", "cp to global".
user-invocable: true
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

Si $ARGUMENTS contient `--dry-run` : s'arrêter ici et afficher un résumé de ce qui serait copié/mis à jour.

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
- Ne PAS copier `.claude/projects/` (emplacement natif obsolète — la mémoire portable vit dans `<repo>/memory/` et se charge via l'@import du CLAUDE.md versionné, pas par copie globale)

## Mémoire portable

La mémoire de claude-forge est **repo-locale**, pas globale.

- **Où elle vit** : `<repo>/memory/` — versionnée git, suit le `git clone`. Rien dans `~/.claude/`.
- **Comment elle se charge** : la ligne `@memory/MEMORY.md` dans le CLAUDE.md versionné (résolution relative au fichier). Comme CLAUDE.md suit le clone, zéro setup par machine pour la mémoire.
- **Distinction composants vs mémoire** : les agents/skills/hooks s'installent GLOBALEMENT (étape 4, `cp` vers `~/.claude/`). La mémoire NON — elle reste repo-local, chargée par @import. Deux mécanismes différents.
- **Double-source transitoire** : l'auto-memory native (`~/.claude/projects/`) peut encore être injectée en parallèle de l'@import. Comportement accepté temporairement (dette tracée).
- **Dialogue d'approbation @import** : au premier lancement sur une nouvelle machine, Claude Code peut demander d'approuver l'@import du CLAUDE.md. L'accepter — sinon les imports sont désactivés silencieusement. Peut ne pas s'afficher si le projet est déjà trusté.
- **TODO différé** : désactiver l'auto-memory native pour atteindre la single-source (probablement une clé settings global — zone hard-block classifier, donc modif manuelle requise). Déclencher si la pollution de contexte par la double-source devient problématique, ou avant communication externe du studio.

## Résultat attendu

Tableau : composant | action (copié/mis à jour/ignoré)
