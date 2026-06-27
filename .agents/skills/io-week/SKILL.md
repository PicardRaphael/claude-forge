---
name: io-week
description: Use when the user types /io-week or asks for weekly I/O metrics digest. Aggregates last 7 daily JSONL files from .claude/_metrics/ and produces trend analysis.
user-invocable: true
allowed-tools: Read, Write, Bash
argument-hint: "[date fin YYYY-MM-DD optionnel, défaut aujourd'hui]"
---

# Rôle

Produit un digest hebdomadaire des métriques I/O outils sur les 7 derniers jours à partir des fichiers `.claude/_metrics/YYYY-MM-DD.jsonl`.

## Étapes

### 1. Déterminer la plage de dates

Si `$ARGUMENTS` contient une date de fin `YYYY-MM-DD`, l'utiliser comme J0. Sinon, obtenir la date du jour :

```bash
Get-Date -Format "yyyy-MM-dd"
```

Calculer J-6 à J0 :

```bash
$end = [DateTime]"<date>"
0..6 | ForEach-Object { $end.AddDays(-$_).ToString("yyyy-MM-dd") } | Sort-Object
```

### 2. Lire les fichiers JSONL disponibles

Pour chaque date de la plage, tenter de lire `.claude/_metrics/<date>.jsonl` via Read.
Ignorer silencieusement les dates sans fichier. Mémoriser quelles dates ont des données.

Si moins de 3 jours ont des données : afficher "Pas assez de données pour digest hebdo (besoin >= 3 jours, trouvé : N)" et s'arrêter.

### 3. Parser et agréger

Pour chaque fichier présent, accumuler :
- Par jour : somme `estimated_tokens`, nombre d'invocations
- Sur la semaine : somme `estimated_tokens` par outil, nombre d'invocations par outil

### 4. Calculer les métriques

- **Tendance quotidienne** : table estimated_tokens + invocations par jour (J-6 → J0)
- **Jour pic** : date avec le plus grand total estimated_tokens
- **Jour creux** : date avec le plus faible total estimated_tokens (parmi les jours avec données)
- **Top 10 outils sur la semaine** : par estimated_tokens total
- **Bottlenecks** : outils représentant > 20 % du total estimated_tokens de la semaine (signaler explicitement)

### 5. Formater le résumé console (Markdown)

```markdown
## Digest hebdomadaire I/O — <J-6> → <J0>

### Tendance quotidienne
| Date | Invocations | estimated_tokens |
|---|---|---|
| ... | ... | ... |

Jour pic : <date> (<N> tokens) | Jour creux : <date> (<N> tokens)

### Top 10 outils — semaine (par estimated_tokens)
| Outil | estimated_tokens | % total |
|---|---|---|
| ... | ... | ...% |

### Bottlenecks (> 20 % du total)
- <Outil> : <N> tokens (<X>%)

---
> Note : `estimated_tokens` est un proxy I/O outils, **pas** les tokens API Claude réels. Pour les tokens session réels, utiliser `/context`.
```

Si aucun bottleneck : afficher "Aucun outil ne dépasse 20 % du total."

Afficher ce résumé dans la console.

### 6. Sauvegarder

Écrire le résumé dans `.claude/_metrics/weekly-summary-<J0>.md` via Write.

## Gotchas

- **Moins de 3 jours de données** : stopper proprement avec message explicatif, ne pas créer de fichier de sortie.
- **Lignes JSON malformées** : ignorer silencieusement par ligne, signaler le total ignoré si > 0.
- **Calcul des dates en PowerShell** : utiliser `[DateTime]` et `.AddDays()`, pas de calcul manuel sur les chaînes.
- **Bottleneck à 0 %** : impossible en pratique — si le total est 0, sauter la section bottleneck.
- **Jours avec 0 données vs jours absents** : ne pas confondre un jour sans invocations (fichier vide) et un jour sans fichier. Les deux sont légitimes ; n'afficher que les jours présents dans la table.
- **proxy ≠ tokens réels** : toujours inclure la note de bas de résumé sur la nuance proxy.

## Apprentissage

Après chaque usage, si la plage de 7 jours révèle un outil dominant inattendu, noter en mémoire projet pour orienter les optimisations de sessions suivantes (ex. : trop de Read sur vault → chercher à consolider).
