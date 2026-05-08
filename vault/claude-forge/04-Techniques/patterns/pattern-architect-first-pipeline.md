---
titre: Pattern architect-first pipeline complet
resume: SessionStart reset → architect → dev séquentiel → /go → pipeline-reset, markers sans TTL
domaine: hooks, agents, workflow, architecture
derniere-maj: 2026-05-08
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/tech"
  - "#statut/actif"
aliases:
  - architect-first
  - pipeline markers
  - workflow dev complet
---

# Pattern Architect-First Pipeline

Pattern Boris Cherny adapté Neoteem. Force un plan avant chaque tâche de code.

## Le flow complet

```
Session start
    │
    ▼
SessionStart hook → supprime les markers (table rase)
    │
    ▼
"Réalise X"
    │
    ▼
architect-guard → pas de marker → BLOQUÉ
    │
    ▼
Session dispatch architect (fast-pass taille S ou plan taille M/L)
    │
    ▼
agent-marker-writer → écrit .architect-marker
    │
    ▼
Session dispatch dev agent 1 (scope: 5 fichiers max)
    ← attend, consolide
Session dispatch dev agent 2 (scope: 5 fichiers max)
    ← attend, consolide
    │
    ▼
/go
    1. lint/typecheck
    2. code-reviewer (via Task) → .code-reviewer-marker
    3. changelog
    4. git commit → commit-guard vérifie code-reviewer-marker
    5. git push
    6. pipeline-reset → supprime les markers
    │
    ▼
"Réalise Y" → pas de marker → architect obligatoire à nouveau
```

## Les 6 hooks

| Hook | Événement | Rôle |
|------|-----------|------|
| `session-reset-markers` | SessionStart | Supprime markers au démarrage |
| `architect-guard` | PreToolUse Write\|Edit | Bloque si pas de .architect-marker |
| `agent-marker-writer` | PostToolUse Agent\|Task | Écrit marker quand architect/code-reviewer invoqué |
| `marker-protect` | PreToolUse Bash | Bloque les commandes avec noms de markers |
| `commit-guard` | PreToolUse Bash | Bloque git commit sans .code-reviewer-marker |
| `pipeline-reset` | Appelé par /go | Script dédié qui supprime markers (contourne marker-protect) |

## Principes

1. **Markers = existence seule, jamais de TTL** — le TTL bloque les sessions longues légitimes
2. **Reset par tâche, pas par session** — /go supprime les markers après push
3. **Session principale = seul orchestrateur** — agents n'ont pas Agent/Task dans leurs tools
4. **Agents séquentiels, jamais parallèles** — bug GitHub #39830
5. **Max 6-8 ops par agent** — au-delà le contexte sature (200K max)
6. **pipeline-reset = script dédié** — car marker-protect bloque les commandes contenant les noms de markers

## Déployé sur

- neo_ia (Python) — architect.md + hooks .py
- ia_back (TypeScript) — architect.md + hooks .ts

## Liens

- [[limites-subagents-claude-code]] — limites techniques des sub-agents
- [[erreur-marker-ttl-blocage-agents]] — erreur qui a mené à ce pattern
- [[decoupe-agents-anti-crash]] — découpage des tâches
- [[Fleet Commander]] — pattern Boris parallélisation sessions
