---
name: analyze-project
description: Analyzes any project and proposes or optimizes Claude Code components. Use when the user says "analyse ce projet", "propose des skills pour X", "optimise les composants de Y".
user-invokable: true
disable-model-invocation: true
argument-hint: "/path/to/project ou https://github.com/..."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, Write
context: fork
agent: opus
---

# Analyse de projet — $ARGUMENTS

## Etape 1 — Explorer le projet

Utilise tes outils pour collecter ces informations sur le chemin `$ARGUMENTS` :

1. **Structure** : `Glob` avec $ARGUMENTS/**/* (maxdepth 3) pour lister les fichiers clés (*.py, *.ts, *.js, package.json, pyproject.toml, Cargo.toml, go.mod)
2. **CLAUDE.md** : `Read` le fichier $ARGUMENTS/CLAUDE.md s'il existe
3. **Agents** : `Glob` avec $ARGUMENTS/.claude/agents/*.md
4. **Skills** : `Glob` avec $ARGUMENTS/.claude/skills/*/SKILL.md
5. **Hooks/Settings** : `Read` le fichier $ARGUMENTS/.claude/settings.json s'il existe
6. **Git** : `Bash` avec `git -C <path> log --oneline -5`

Lance les lectures en parallèle quand possible.

---

## Etape 2 — Produire le rapport

### 1. Identifier le stack

Langage, framework, build, test, lint, services externes.

### 2. Choisir le mode

**Composants existants → Optimisation**
Lire chaque composant et évaluer : description ligne unique ? gotchas ? tools minimum ? effort ?

**Pas de composants → Création**
Stratégie complète from scratch.

### 3. Vérifier features récentes si pertinent

`site:github.com/anthropics/claude-code [feature]`

### 4. Rapport

```
## Rapport — [Projet]
Date : [aujourd'hui] | Stack : [...] | Mode : [Optimisation/Création]

### CLAUDE.md [optimisé/proposé]
[contenu complet prêt à copier]

### 🔴 Priorité 1 — Impact immédiat
[composant] : [ce qu'il fait]

### 🟡 Priorité 2 — Qualité de vie
[composants]

### 🟢 Nice to have
[composants]

### Automatisations récurrentes
[uniquement si pertinent — ne pas forcer]
/loop = polling régulier (ex: /loop 5m /deploy-check). PAS pour workflows multi-étapes.
/schedule = tâche planifiée cron. Agent Teams = coordination multi-agents.

### Optimisations existantes
[si mode Optimisation]
```

### 5. Demander confirmation

"Veux-tu que je crée/optimise les composants 🔴 maintenant ?"

## Apprentissage — Sauvegarder en mémoire projet

Après chaque analyse, sauvegarder en mémoire :
- **Stack et architecture** du projet analysé
- **Composants existants** et leur état (bien fait / à optimiser)
- **Recommandations acceptées** par l'utilisateur (pour ne pas reproposer ce qui a été refusé)
- **Patterns spécifiques** du projet (conventions de nommage, structure, gotchas)

## Règles

- Lire les vrais fichiers avant de proposer
- Adapter au stack réel — jamais générique
- Inclure toujours le CLAUDE.md
- Signaler si info potentiellement datée (post 31 mars 2026)
