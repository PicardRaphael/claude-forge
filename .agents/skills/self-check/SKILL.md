---
name: self-check
description: Validates internal consistency of claude-forge — single-line descriptions, name matches folder, no README.md in skills, SKILL.md under 500 lines, referenced skills exist. Use when the user says "self-check", "valide le projet", "vérifie la cohérence".
user-invocable: true
disable-model-invocation: true
allowed-tools: Read, Glob, Bash, Grep
---

# Validation de cohérence — claude-forge

## Checks à effectuer

### 1. Skills

Pour chaque `.claude/skills/*/SKILL.md` :
- [ ] `description` YAML sur une seule ligne (pas de `\n`, `>-`, `|`)
- [ ] `name` YAML = nom du dossier parent
- [ ] Pas de fichier `README.md` dans le dossier
- [ ] SKILL.md < 500 lignes
- [ ] Si `allowed-tools` défini, outils valides

### 2. Agents

Pour chaque `.claude/agents/*.md` :
- [ ] `description` YAML sur une seule ligne
- [ ] Chaque skill dans `skills:` a un dossier dans `.claude/skills/`
- [ ] Chaque référence `.claude/agent-memory/<agent>/` pointe vers un dossier
  existant ; ne pas flagger le pattern entier comme obsolète

### 3. Settings

- [ ] `.claude/settings.json` est du JSON valide (`python -m json.tool`)
- [ ] `.claude/settings.local.json` est du JSON valide

### 4. Structure

- [ ] Tous les dossiers skills en kebab-case
- [ ] Pas de fichiers orphelins

## Format de sortie

| Composant | Check | Status | Détail |
|-----------|-------|--------|--------|
| skill/X | description | PASS/FAIL | ... |

Résumé : X pass, Y fail
