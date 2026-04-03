---
name: schema-output-format
description: Strict templates for schema-mapper generated files. Domain files format (tables + functions), synthesis report, and function map.
user-invokable: false
---

# Format de sortie schema-mapper

Templates EXACTS. Ne jamais dévier.

---

## Template 1 : Fichier domaine (`doc/schemas/cluster_NNN.md`)

```markdown
# Domaine : cluster_NNN

> **Tables :** {nombre} | **Fonctions liées :** {nombre} | **A renommer par :** [nom métier à définir]

## Tables principales

| Table | Description probable | Colonnes clés | Référencée par |
|-------|---------------------|---------------|----------------|
| `{table}` | {description déduite des colonnes} | {colonnes PK + principales} | {nombre de FK entrantes} tables |

> Triées par FK entrantes décroissant.

## Arbre de relations

```
table_centrale
  ├── enfant_1 (fk_column → table_centrale.id)
  │     └── petit_enfant (fk_column → enfant_1.id)
  ├── enfant_2 (fk_column → table_centrale.id)
  └── enfant_3 (fk_column → table_centrale.id)
```

## Fonctions associées

Fonctions qui lisent ou écrivent dans les tables de ce domaine :

### Lecture (f_*)

| Fonction | Schéma | Arguments | Retour | Tables lues |
|----------|--------|-----------|--------|-------------|
| `f_{name}` | {schema} | {args résumés} | {return} | `table_a`, `table_b` |

### Écriture (p_*)

| Fonction | Schéma | Arguments | Tables modifiées | Appelle |
|----------|--------|-----------|-----------------|---------|
| `p_{name}` | {schema} | {args résumés} | `table_a` | `f_{other}` |

### Triggers (tr_*)

| Trigger | Table | Événement | Timing |
|---------|-------|-----------|--------|
| `tr_{name}` | `{table}` | INSERT/UPDATE/DELETE | BEFORE/AFTER |

### Procédures (proc_*)

| Procédure | Schéma | Arguments | Tables impactées | Appelle |
|-----------|--------|-----------|-----------------|---------|
| `proc_{name}` | {schema} | {args résumés} | `table_a`, `table_b` | `p_{x}`, `f_{y}` |

## Règles métier extraites du code

Règles implicites découvertes en lisant le source des fonctions. **C'est la section la plus importante pour la migration.**

### Valeurs de référence (IDs magiques)

Valeurs codées en dur trouvées dans les fonctions (WHERE col = N, CASE WHEN col = N) :

| Table | Colonne | Valeur | Signification (déduite du contexte) | Trouvée dans |
|-------|---------|--------|-------------------------------------|-------------|
| `{table}` | `{col}` | `{valeur}` | {ce que ça signifie d'après le nom de la fonction et le contexte} | `f_{name}`, `p_{name}` |

> Lister TOUTES les valeurs en dur trouvées. C'est critique pour la migration.

### Jointures conditionnelles

Jointures qui dépendent d'une valeur ou d'un type :

```sql
-- Trouvée dans f_{name} :
-- "Si role_id = 1 alors c'est un propriétaire"
JOIN acteur_role ON acteur_role.acteur_id = acteur.id
  AND acteur_role.role_id = 1
```

### Règles de filtrage implicites

Conditions WHERE récurrentes dans plusieurs fonctions (soft-delete, statut actif, etc.) :

| Règle | Condition SQL | Trouvée dans |
|-------|-------------|-------------|
| {description} | `WHERE {condition}` | `f_{a}`, `f_{b}`, `p_{c}` |

> Ex: "Toujours filtrer les enregistrements supprimés" → `WHERE deleted_at IS NULL` trouvé dans 12 fonctions

### Logique métier complexe

Blocs CASE WHEN, IF/ELSIF, ou logique non triviale trouvés dans les fonctions :

| Fonction | Règle résumée | Impact |
|----------|--------------|--------|
| `{name}` | {résumé de la logique en français} | {quelles tables/colonnes sont impactées} |

## Jointures fréquentes

- **{nom du parcours}** : `table_a → table_b → table_c`
  ```sql
  FROM table_a
  JOIN table_b ON table_b.a_id = table_a.id
  JOIN table_c ON table_c.b_id = table_b.id
  ```

> Maximum 5 jointures par fichier.

## Colonnes notables

| Table | Colonne | Type | Note |
|-------|---------|------|------|
| `{table}` | `{colonne}` | {type} | {pourquoi notable} |

## Tables ponts

| Table | Aussi dans | FK concernée |
|-------|-----------|--------------|
| `{table}` | cluster_NNN ({nom probable}) | `{fk}` |

## TODO humain

- [ ] Renommer `cluster_NNN.md` → `{nom-metier}.md`
- [ ] Valider les descriptions de tables et fonctions
- [ ] Ajouter les pièges métier
- [ ] Marquer les fonctions candidates à la migration applicative
- [ ] Vérifier les dépendances entre fonctions
```

---

## Template 2 : Rapport de synthèse (`doc/schemas/RAPPORT.md`)

```markdown
# Rapport schema-mapper

| | |
|---|---|
| **Date** | {YYYY-MM-DD} |
| **Base** | {nom_base} |
| **Schémas** | {liste} |
| **Tables** | {nombre} |
| **FK** | {nombre} |
| **Fonctions** | {nombre total} |
| **Domaines détectés** | {nombre} |

## Résumé fonctions par convention

| Convention | Préfixe | Nombre | Rôle |
|-----------|---------|--------|------|
| read | `f_*` | {n} | Lecture de données |
| write | `p_*` | {n} | Modification de données |
| procedure | `proc_*` | {n} | Procédures stockées |
| trigger | `tr_*` | {n} | Fonctions de trigger |
| other | — | {n} | Non catégorisé |

## Résumé fonctions par schéma

| Schéma | Fonctions | f_* | p_* | proc_* | tr_* | other |
|--------|-----------|-----|-----|--------|------|-------|
| {schema} | {total} | {n} | {n} | {n} | {n} | {n} |

## Vue d'ensemble des domaines

| # | Fichier | Tables | Fonctions | Table centrale | Suggestion de nom |
|---|---------|--------|-----------|----------------|-------------------|
| 1 | cluster_001.md | {n} | {n} | {table} | {suggestion} |

## Tables de référentiel

| Table | Référencée par | Domaines concernés |
|-------|---------------|-------------------|
| `{table}` | {n} FK entrantes | cluster_001, cluster_003 |

## Tables isolées

| Table | Colonnes | Usage probable |
|-------|----------|---------------|
| `{table}` | {n} | {technique / config / orpheline ?} |

## Fonctions orphelines

Fonctions qui ne référencent aucune table connue :

| Fonction | Schéma | Convention | Source length |
|----------|--------|-----------|--------------|
| `{name}` | {schema} | {conv} | {n} chars |

## Chaînes d'appels critiques

Fonctions qui appellent le plus d'autres fonctions (hubs de dépendances) :

| Fonction | Appelle | Appelée par |
|----------|---------|-------------|
| `{name}` | {n} fonctions | {n} fonctions |

## Statistiques

- Table la plus référencée (FK entrantes) : `{table}` ({n})
- Fonction la plus longue : `{name}` ({n} chars)
- Schéma avec le plus de fonctions : `{schema}` ({n})
- Domaine le plus gros : cluster_{NNN} ({n} tables, {n} fonctions)

## Prochaines étapes

1. [ ] Renommer chaque `cluster_NNN.md` avec le vrai nom métier
2. [ ] Ajouter le contexte métier (pièges, règles, vocabulaire)
3. [ ] Identifier les fonctions prioritaires à migrer vers l'applicatif
4. [ ] Valider les chaînes d'appels entre fonctions
5. [ ] Marquer les fonctions obsolètes
```

---

## Règles de formatage

1. **Tables** en backticks : `ma_table`
2. **Colonnes** en backticks : `ma_colonne`
3. **Fonctions** en backticks : `f_get_data`
4. **FK** au format : `source.colonne → cible.colonne`
5. **Arbres** en ASCII : `├──`, `└──`, `│`
6. **Tri** : par pertinence (FK entrantes décroissant), jamais alphabétique
7. **Limite** : max 40 tables par fichier domaine
8. **SQL** : toujours `JOIN ... ON`, jamais `WHERE` implicite
9. **Descriptions** : directes, pas "Cette table..."
10. **Fonctions** : toujours groupées par convention (f_, p_, proc_, tr_)
