---
name: analyze-project
description: Analyzes any project and proposes or optimizes Claude Code components. Use when the user says "analyse ce projet", "propose des skills pour X", "optimise les composants de Y".
user-invocable: true
disable-model-invocation: true
argument-hint: "/path/to/project ou https://github.com/..."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, Write
context: fork
agent: opus
---

# Analyse de projet — $ARGUMENTS

## Contexte injecté automatiquement

!`echo "=== Projet ===" && echo "$ARGUMENTS"`
!`if [ -d "$ARGUMENTS" ]; then echo "=== Structure ===" && find "$ARGUMENTS" -maxdepth 3 \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "package.json" -o -name "pyproject.toml" -o -name "Cargo.toml" -o -name "go.mod" \) 2>/dev/null | head -40; fi`
!`if [ -d "$ARGUMENTS" ]; then echo "=== CLAUDE.md ===" && cat "$ARGUMENTS/CLAUDE.md" 2>/dev/null || echo "Aucun"; fi`
!`if [ -d "$ARGUMENTS" ]; then echo "=== Agents ===" && ls "$ARGUMENTS/.claude/agents/" 2>/dev/null || echo "Aucun"; fi`
!`if [ -d "$ARGUMENTS" ]; then echo "=== Skills ===" && ls "$ARGUMENTS/.claude/skills/" 2>/dev/null || echo "Aucune"; fi`
!`if [ -d "$ARGUMENTS" ]; then echo "=== Hooks ===" && cat "$ARGUMENTS/.claude/settings.json" 2>/dev/null || echo "Aucun"; fi`
!`if [ -d "$ARGUMENTS" ]; then echo "=== Git ===" && git -C "$ARGUMENTS" log --oneline -5 2>/dev/null || echo "Pas de git"; fi`

---

## Mission

Avec toutes ces informations, produis un rapport complet :

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

### /loop recommandés
[si workflows récurrents]

### Optimisations existantes
[si mode Optimisation]
```

### 5. Demander confirmation

"Veux-tu que je crée/optimise les composants 🔴 maintenant ?"

## Règles

- Lire les vrais fichiers avant de proposer
- Adapter au stack réel — jamais générique
- Inclure toujours le CLAUDE.md
- Signaler si info potentiellement datée (post 31 mars 2026)
