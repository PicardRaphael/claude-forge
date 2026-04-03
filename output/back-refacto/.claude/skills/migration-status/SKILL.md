---
name: migration-status
description: Track PostgreSQL function migration progress. Shows which functions are migrated, pending, or blocked per domain. Auto-updated by migrate-function and create-endpoint. Use when user says "avancement", "migration status", "où on en est", "combien de fonctions".
allowed-tools: Read, Write, Grep, Glob
---

# Suivi de migration PostgreSQL → applicatif

## Fichier de tracking

Le fichier `doc/migration-tracker.md` est la source de vérité.

### Si le fichier n'existe pas

Le générer à partir de :
1. `doc/schemas/RAPPORT.md` → liste des domaines
2. `Glob "{repo_fonctions}/**/*.sql"` → toutes les fonctions
3. Créer le fichier avec toutes les fonctions en status `⬜ pending`

### Format du fichier

```markdown
# Migration tracker

> Dernière mise à jour : {YYYY-MM-DD}
> Total : {migré}/{total} fonctions ({pourcentage}%)

## Vue d'ensemble

| Domaine | Total | ✅ Migrées | ⬜ Pending | 🚫 Ignorées | % |
|---------|-------|-----------|-----------|-------------|---|
| {domaine} | {n} | {n} | {n} | {n} | {n}% |
| **Total** | **{n}** | **{n}** | **{n}** | **{n}** | **{n}%** |

## {domaine}

### ✅ Migrées

| Fonction | Endpoint | Date | Notes |
|----------|----------|------|-------|
| `f_{name}` | `GET /copros/:id` | {YYYY-MM-DD} | — |

### ⬜ Pending

| Fonction | Convention | Complexité | Dépend de |
|----------|-----------|-----------|-----------|
| `f_{name}` | read | {simple/moyenne/complexe} | — |
| `proc_{name}` | procedure | complexe | `f_{x}`, `p_{y}` non migrées |

### 🚫 Ignorées

| Fonction | Raison |
|----------|--------|
| `tr_{name}` | Trigger géré côté ORM |
```

## Actions

### `/migration-status` (sans argument)

Afficher le résumé : pourcentage global + par domaine.

### `/migration-status {domaine}`

Afficher le détail d'un domaine : fonctions migrées, pending, ignorées.

### Mise à jour automatique

Les skills `/migrate-function` et `/create-endpoint` doivent appeler cette logique après chaque migration :

1. Lire `doc/migration-tracker.md`
2. Passer la fonction de `⬜ Pending` à `✅ Migrées`
3. Ajouter l'endpoint, la date, et les notes
4. Recalculer les pourcentages
5. Si la fonction migrée était une dépendance d'autres fonctions → mettre à jour leur colonne "Dépend de"

### Marquer comme ignorée

Le dev dit "ignore `tr_copro_audit`" → passer en `🚫 Ignorées` avec la raison.

## Règles

- Ne JAMAIS modifier les fichiers du repo fonctions
- Le tracker est dans le repo back, pas dans le repo fonctions
- Si le tracker et la réalité divergent (nouvelle fonction dans le repo) → signaler au dev
- Les pourcentages excluent les fonctions ignorées du total
