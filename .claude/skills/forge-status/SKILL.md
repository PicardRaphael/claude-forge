---
name: forge-status
description: Dashboard showing claude-forge components in ~/.claude/ vs .claude/, signals differences and missing components. Use when the user says "forge status", "dashboard", "statut forge", "what's installed".
user-invokable: true
disable-model-invocation: true
allowed-tools: Bash, Read, Glob
---

# Statut claude-forge

## Étapes

### 1. Collecter les composants source

- `Glob` : `.claude/agents/*.md`
- `Glob` : `.claude/skills/*/SKILL.md`
- `Read` : `.claude/settings.json`

### 2. Collecter les composants installés

- `Glob` : `~/.claude/agents/*.md`
- `Glob` : `~/.claude/skills/*/SKILL.md`
- `Read` : `~/.claude/settings.json`

### 3. Comparer

Pour chaque composant :
- Existe dans source et installé → `diff` pour vérifier si identique
- Existe dans source seulement → "Non installé"
- Existe dans installé seulement → "Extra (pas dans source)"

### 4. Rapport

| Composant | Type | Source | Installé | Status |
|-----------|------|--------|----------|--------|
| repo-inspector | agent | oui | oui | synced/outdated |

Résumé : X synced, Y outdated, Z non installés

### 5. Suggestion

Si des composants sont outdated ou non installés → suggérer `/install-forge`
