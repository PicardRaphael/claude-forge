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

## Contexte injecté automatiquement

!`P=$(cat <<'_ARG_'
$ARGUMENTS
_ARG_
) && echo "=== Projet ===" && echo "$P"`
!`P=$(cat <<'_ARG_'
$ARGUMENTS
_ARG_
) && [ -d "$P" ] && echo "=== Structure ===" && find "$P" -maxdepth 3 \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "package.json" -o -name "pyproject.toml" -o -name "Cargo.toml" -o -name "go.mod" \) 2>/dev/null | head -40`
!`P=$(cat <<'_ARG_'
$ARGUMENTS
_ARG_
) && [ -d "$P" ] && echo "=== CLAUDE.md ===" && cat "$P/CLAUDE.md" 2>/dev/null || echo "Aucun"`
!`P=$(cat <<'_ARG_'
$ARGUMENTS
_ARG_
) && [ -d "$P" ] && echo "=== Agents ===" && ls "$P/.claude/agents/" 2>/dev/null || echo "Aucun"`
!`P=$(cat <<'_ARG_'
$ARGUMENTS
_ARG_
) && [ -d "$P" ] && echo "=== Skills ===" && ls "$P/.claude/skills/" 2>/dev/null || echo "Aucune"`
!`P=$(cat <<'_ARG_'
$ARGUMENTS
_ARG_
) && [ -d "$P" ] && echo "=== Hooks ===" && cat "$P/.claude/settings.json" 2>/dev/null || echo "Aucun"`
!`P=$(cat <<'_ARG_'
$ARGUMENTS
_ARG_
) && [ -d "$P" ] && echo "=== Git ===" && git -C "$P" log --oneline -5 2>/dev/null || echo "Pas de git"`

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
