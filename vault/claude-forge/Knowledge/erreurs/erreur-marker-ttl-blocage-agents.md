---
titre: Markers architect avec TTL bloquaient les sous-agents
resume: TTL 60min sur architect-guard causait des blocages en cascade — remplace par existence seule
domaine: hooks, agents, workflow
derniere-maj: 2026-05-07
auteur: claude
tags:
  - "#type/erreur"
  - "#domaine/tech"
  - "#statut/resolu"
aliases:
  - marker TTL blocage
  - architect-guard timeout
  - agent bloque marker expire
---

# Markers architect avec TTL — blocage systématique des sous-agents

## Ce qui s'est passé

Les repos ia_back et neo_ia avaient un système de markers horodatés pour forcer le workflow `architect → dev → test-writer → code-reviewer → commit` (pattern Boris/Thariq). Le hook `architect-guard` vérifiait que le marker avait **moins de 60 minutes**. Résultat :

- Sessions longues (>1h) → dev agent bloqué en plein milieu
- Message : "BLOQUÉ : architect doit être appelé en premier"
- L'agent ne pouvait pas se débloquer seul (marker-protect empêche l'écriture manuelle)
- Erreurs "Tool result missing due to internal error" quand le nombre de tool calls explosait

## Pourquoi c'était une erreur

Le TTL ne résout pas le bon problème. On veut vérifier que architect a été appelé **avant** le dev, pas qu'il a été appelé **récemment**. Un dev agent qui code depuis 3h sur un plan validé par architect est parfaitement légitime. Le TTL punit les sessions longues, pas les sessions qui sautent architect.

## Autres problèmes découverts en même temps

1. **Hook NeoBoard user-level** (`~/.claude/neoboard-safety-check.js`) — bloquait `git commit/push` dans TOUS les projets, pas juste NeoBoard. Supprimé.
2. **Hook no-inline-python user-level** (`~/.claude/no-inline-python.js`) — se déclenchait sur chaque Bash de chaque projet. Retiré du settings.json.
3. **Hooks PostToolUse synchrones** (ruff check/format sur neo_ia, typecheck sur ia_back) — bloquaient les Write/Edit inutilement. Passés en `async: true`.
4. **Permissions Bash trop spécifiques** dans settings.local.json — commandes exactes au lieu de wildcards, cruft de sessions passées. Nettoyé avec wildcards.
5. **Permissions manquantes** sur neoteem-brain — `Bash(obsidian *)` et `Bash(python3 *)` absents, sous-agents ne pouvaient pas utiliser la CLI.

## Ce qu'on a fait

- **Markers** : supprimé le TTL, vérification d'existence seule (`existsSync` / `Path.exists()`)
- **Hooks PostToolUse** : `async: true` sur ruff et typecheck
- **Hooks user-level** : NeoBoard supprimé, no-inline-python retiré
- **Permissions** : wildcards partout, nettoyage cruft multi-sessions
- **Neoteem-brain** : ajout Bash(obsidian/python) dans settings.json

## Pattern correct pour architect-first

Le pattern Boris fonctionne, c'est l'implémentation qui comptait :
- `architect-guard` → vérifie que `.architect-marker` **existe** (pas de TTL)
- `agent-marker-writer` → écrit le marker quand architect est invoqué (PostToolUse Agent)
- `marker-protect` → empêche les agents de tricher via Bash
- `commit-guard` → vérifie que `.code-reviewer-marker` **existe** avant commit
- Reset des markers = suppression manuelle ou hook SessionStart (optionnel)

## Leçon

Les hooks de **guard** (PreToolUse) doivent être les plus simples possible — un check binaire (existe/existe pas), pas de logique temporelle. Plus un hook est complexe, plus il risque de bloquer des cas légitimes. Les hooks de **quality** (PostToolUse) comme ruff/typecheck doivent être `async: true` pour ne pas multiplier les tool calls bloquantes.
