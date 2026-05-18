---
titre: "Pattern architect-first pipeline complet"
resume: "SessionStart reset → architect → dev sequentiel → /go → pipeline-reset, markers sans TTL"
aliases:
  - architect-first
  - pipeline markers
  - workflow dev complet
domaine: claude-code
type: technique
derniere-maj: 2026-05-08
auteur: claude
sources: []
tags:
  - "#type/technique"
  - "#domaine/claude-code"
---

## Description

Pattern Boris Cherny adapte Neoteem. Force un plan architect avant chaque tache de code via des hooks deterministes et des markers fichier.

## Quand utiliser

Sur tout projet avec des agents de developpement. Garantit qu'un plan existe avant toute ecriture de code.

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

## Exemple

```
/recap → "implemente X" → architect-guard bloque → architect planifie → marker pose → dev-agent execute → /go → tests + review + commit + push → markers reset
```

## Liens

- [[MOC-Techniques]]
- [[limites-subagents-claude-code]] — limites techniques des sub-agents
- [[erreur-marker-ttl-blocage-agents]] — erreur qui a mene a ce pattern
- [[decoupe-agents-anti-crash]] — decoupage des taches
- [[Workflow Boris]] — pattern Boris parallelisation sessions


## Mise à jour mai 2026 — Advisor avant Architect

Le pipeline intègre désormais un step **advisor** avant l'architect pour les grosses tâches :

```
exploration → advisor (scope/approche) → architect (plan) → dev → tests → architect review → livraison
```

### Quand invoquer advisor
- Brief ambigu ou scope pas clair
- Nouveau scope ≥ 3 fichiers (pas un fix)
- Décision impactante (stack, pattern, dépendance)
- Brief multi-tiers / multi-phases

### Pourquoi
Session neo_ia 2026-05-11 : advisor consulté tardivement → va-et-vient sur le scope (Tier 0 vs 9 thèmes). Avec advisor dès le début, le scope aurait été clair immédiatement.

L'advisor voit la conversation complète (transcript), l'architect ne voit que le prompt. L'advisor recadre le **quoi**, l'architect planifie le **comment**.

Rule forge : `pipeline-grosse-tache.md`