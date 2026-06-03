---
name: io-daily
description: Use when the user types /io-daily or asks for today's I/O metrics. Reads .claude/_metrics/YYYY-MM-DD.jsonl and produces a console summary plus saves it as daily-summary-YYYY-MM-DD.md.
user-invocable: true
allowed-tools: Read, Write, Bash
argument-hint: "[date YYYY-MM-DD optionnel, défaut aujourd'hui]"
---

# Rôle

Produit un résumé quotidien des métriques I/O outils à partir de `.claude/_metrics/YYYY-MM-DD.jsonl`.

## Étapes

### 1. Déterminer la date cible

Si `$ARGUMENTS` contient une date au format `YYYY-MM-DD`, l'utiliser. Sinon, obtenir la date du jour :

```bash
Get-Date -Format "yyyy-MM-dd"
```

### 2. Lire le fichier JSONL

Lire `.claude/_metrics/<date>.jsonl` via l'outil Read.

Si le fichier est absent : afficher "Pas de métriques pour cette date (<date>)" et s'arrêter proprement. Ne pas créer de fichier de sortie.

### 3. Parser ligne par ligne

Chaque ligne est un objet JSON indépendant :
```json
{"ts": "...", "session_id": "...", "tool": "Read", "input_chars": 1500, "output_chars": 5000, "estimated_tokens": 1970}
```

Parcourir toutes les lignes et accumuler :
- Compteur d'invocations par outil (`tool`)
- Somme `estimated_tokens` par outil
- Ensemble des `session_id` distincts
- Somme totale `estimated_tokens`

### 4. Calculer les métriques

- **Total invocations** : nombre de lignes
- **Total estimated_tokens** : somme de tous les `estimated_tokens`
- **Sessions distinctes** : cardinal de l'ensemble des `session_id`
- **Top 5 outils par fréquence** : outils les plus invoqués
- **Top 5 outils par estimated_tokens** : outils les plus consommateurs

### 5. Formater le résumé console (Markdown)

```markdown
## Métriques I/O — <date>

| Métrique | Valeur |
|---|---|
| Total invocations | N |
| Total estimated_tokens | N |
| Sessions distinctes | N |

### Top 5 — Fréquence
| Outil | Invocations |
|---|---|
| ... | ... |

### Top 5 — Tokens estimés
| Outil | estimated_tokens |
|---|---|
| ... | ... |

---
> Note : `estimated_tokens` est un proxy I/O outils, **pas** les tokens API Claude réels. Pour les tokens session réels, utiliser `/context`.
```

Afficher ce résumé dans la console.

### 6. Sauvegarder

Écrire le résumé dans `.claude/_metrics/daily-summary-<date>.md` via Write.

## Gotchas

- **Fichier absent** : ne pas créer de fichier de sortie, afficher le message d'absence et s'arrêter. Ne pas lever d'erreur.
- **Lignes JSON malformées** : ignorer silencieusement les lignes non parsables, signaler le nombre ignoré en bas du résumé si > 0.
- **`$ARGUMENTS` vide** : utiliser la date du jour via Bash PowerShell — ne pas assumer UTC.
- **Champ `estimated_tokens` manquant** : traiter comme 0 pour cette ligne.
- **proxy ≠ tokens réels** : toujours inclure la note de bas de résumé sur la nuance proxy.

## Apprentissage

Après chaque usage, si un pattern de log inattendu est observé (champs manquants, format divergent du hook metrics-tracker), le noter en mémoire projet pour aligner le hook.
