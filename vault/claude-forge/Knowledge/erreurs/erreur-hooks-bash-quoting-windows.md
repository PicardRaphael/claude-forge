---
titre: "Hooks bash -c avec single quotes cassent sur Windows"
resume: "bash -c '...$()...' empêche l'expansion shell sur Windows — utiliser python avec chemin relatif à la place"
aliases:
  - "erreur hooks quoting"
  - "bash single quotes windows"
  - "hooks boucle infinie"
  - "hooks portabilité"
  - "hook chemin relatif"
auteur: claude
derniere-maj: 2026-05-10
type: erreur
tags:
  - "#type/erreur"
  - "#erreur/hook"
  - "#domaine/claude-code"
---

## Ce qui s'est passé

10 hooks Claude Code configurés avec `bash -c 'python "$(git rev-parse --show-toplevel)/.claude/hooks/..."'`. Sur Windows, les single quotes empêchent l'expansion de `$(git rev-parse ...)`, causant une erreur `unexpected EOF while looking for matching quote`. Les stop hooks (`learning-reminder`, `devil-advocate-stop`) bouclaient indéfiniment à chaque fin de session.

## Pourquoi c'était une erreur

- Single quotes en bash = pas d'expansion de variables ni de commandes
- `$(git rev-parse --show-toplevel)` ne s'exécute jamais → chemin cassé
- Le pattern avait été choisi pour résoudre le CWD quand on `cd` dans un sous-dossier, mais les hooks Claude Code tournent déjà depuis la racine projet

## Ce qu'on a fait

Remplacé les 10 hooks de `bash -c 'python "$(git rev-parse --show-toplevel)/.claude/hooks/X.py"'` par `python ".claude/hooks/X.py"` — chemin relatif, portable entre Windows/Linux/macOS, pas de dépendance à bash.

## Pattern correct

```json
{
  "type": "command",
  "command": "python \".claude/hooks/mon-hook.py\"",
  "timeout": 5
}
```

## Liens

- [[erreur-marker-ttl-blocage-agents]]
- [[harness-engineering]]


## Régression du Fix 1 — chemin relatif cassé par cd

Le Fix 1 (`python ".claude/hooks/X.py"`) fonctionnait tant que le CWD restait la racine projet. Mais quand un `cd vault/claude-forge/...` est fait dans une commande Bash, le **CWD persiste entre les appels Bash** et les hooks PreToolUse s'exécutent depuis ce CWD. Résultat : `python ".claude/hooks/security-guard.py"` cherche `.claude/hooks/` dans le sous-dossier, pas à la racine.

## Fix 2 — chemin absolu sans bash -c (CORRECT)

```json
{
  "type": "command",
  "command": "python \"$(git rev-parse --show-toplevel)/.claude/hooks/mon-hook.py\"",
  "timeout": 5
}
```

Différences avec le pattern original cassé :
- **Pas de `bash -c`** — la commande est exécutée directement par le shell système
- **Double quotes** (pas single quotes) — `$(...)` est correctement expansé
- `$(git rev-parse --show-toplevel)` fonctionne en bash ET PowerShell

## Leçon

3 itérations pour trouver le bon pattern :
1. `bash -c '...$()...'` → single quotes empêchent expansion (Windows)
2. `python ".claude/hooks/..."` → casse quand CWD change (cd en Bash)
3. `python "$(git rev-parse --show-toplevel)/.claude/hooks/..."` → **correct** (absolu, portable, pas de bash -c)
