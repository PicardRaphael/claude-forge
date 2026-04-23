# Regles de reformulation — neo-brain-support

## Principe

Le vault neoteem-brain contient de la documentation technique (tables PG, fonctions, schemas, architecture). Le support n'a pas besoin de ces details. Cette reference definit comment transformer une reponse technique en reponse support.

## Substitutions obligatoires

### Base de donnees

| Technique | Support |
|-----------|---------|
| Table `t_bail` | "le bail" |
| Table `t_acteur` | "le contact" / "la personne" |
| Table `t_lot` | "le lot" / "le bien" |
| Table `t_copropriete` | "la copropriete" |
| Table `t_ecriture` | "l'ecriture comptable" |
| Table `t_appel_fonds` | "l'appel de fonds" |
| Colonne `psbyid` | "identifiant" (ne jamais montrer la valeur) |
| Colonne `statut = 'ACTIF'` | "statut Actif" |
| `schema_xxx` | "module [nom]" |
| Toute requete SQL | Description du resultat en francais |

### Fonctions PG

| Technique | Support |
|-----------|---------|
| `f_calc_charges` | "le calcul des charges" |
| `f_get_locataires_actifs` | "la liste des locataires actifs" |
| `f_rapprochement_bancaire` | "le rapprochement bancaire" |
| Tout nom de fonction `f_*` | Description de l'action en francais |

### Architecture

| Technique | Support |
|-----------|---------|
| "API endpoint /api/v2/baux" | "ecran Baux dans Lojii" |
| "Service ws / neo-ia / ia-back" | Ne pas mentionner |
| "Requete POST/GET" | Ne pas mentionner |
| "Micro-frontend lojii-xxx" | "ecran [nom]" ou "module [nom]" |

### Navigation

Toujours donner le chemin dans l'interface :

- **Format** : `Menu principal > Sous-menu > Onglet > Bouton`
- **Exemple** : "Gerance > Baux > Recherche > filtrer par nom"
- Si le chemin ecran n'est pas connu, dire "dans le module [nom]" sans inventer

### Erreurs et codes

| Technique | Support |
|-----------|---------|
| Code erreur interne (224, etc.) | "une erreur de [type]" + que faire |
| Stack trace | Ne jamais montrer |
| Log serveur | Ne jamais montrer |
| Message d'erreur technique | Reformuler en action : "Verifier que..." |

## Regles generales

1. **Jamais d'identifiant technique** — pas de psbyid, pas d'ID, pas de UUID
2. **Jamais de nom de table/colonne** — toujours le terme metier
3. **Jamais de SQL** — decrire le resultat, pas la requete
4. **Jamais d'architecture** — le support n'a pas besoin de savoir quel service fait quoi
5. **Toujours une action** — chaque reponse doit dire quoi faire, pas juste expliquer
6. **Toujours un chemin ecran** — quand c'est possible, indiquer ou cliquer
7. **Escalade claire** — si le support ne peut pas resoudre, dire a qui transmettre
