---
name: notes
description: ALWAYS invoke when user types `/notes <feature-slug>` or `/notes <path/to/feature>`. Initialises `docs/implementation-notes/<slug>.md` pre-filled with 4 Thariq sections. DO NOT create without resolving repo path first.
argument-hint: "<feature-slug or path/to/feature>"
allowed-tools: Bash, Read, Write, AskUserQuestion
user-invokable: true
---

# Notes — Running Implementation Notes

Initialise un fichier `implementation-notes` pré-rempli avec les 4 sections du pattern Thariq.
Référence : [[running-implementation-notes]] (vault `04-Techniques/patterns/`)

## Étapes

### 1. Parser l'argument

L'argument fourni par l'utilisateur est `$ARGUMENTS`.

- Si l'argument contient `/` → c'est un chemin relatif d'app (ex : `apps/neochat/payments`). Extraire le slug depuis le basename (`payments`). Conserver le préfixe comme indication d'emplacement.
- Si l'argument ne contient pas `/` → c'est un slug simple (ex : `paiement-stripe`).

Le slug final = dernière partie du path (après le dernier `/`). Normaliser en kebab-case (pas d'espaces, pas de majuscules).

### 2. Détecter le repo courant

Exécuter via Bash :

```bash
git rev-parse --show-toplevel
```

Identifier le repo à partir du chemin retourné :
- Contient `ia_back` → repo `ia_back`
- Contient `neo_ia` → repo `neo_ia` (monorepo)
- Contient `claude-forge` → repo `claude-forge`
- Autre → repo générique

### 3. Résoudre le path de sortie

**Règles par repo :**

- `ia_back` → `docs/implementation-notes/<slug>.md` (depuis la racine du repo)
- `claude-forge` → `docs/implementation-notes/<slug>.md` (depuis la racine du repo)
- Repo générique → `docs/implementation-notes/<slug>.md` (depuis la racine du repo)
- `neo_ia` (monorepo) → logique conditionnelle :
  - Si l'argument contenait un préfixe (ex : `apps/neochat/payments`) → path = `apps/neochat/docs/implementation-notes/<slug>.md`
  - Si l'argument était un slug simple → utiliser `AskUserQuestion` pour demander : "Quel app dans neo_ia ? (`apps/neochat`, `apps/neomail`, `apps/neodoc`) ou racine monorepo ?"

### 4. Vérifier l'existence du fichier et du dossier

Utiliser Bash pour vérifier si le fichier existe :

```bash
test -f "<path-résolu>" && echo "EXISTS" || echo "NEW"
```

- Si le fichier **n'existe pas** :
  - Vérifier que le dossier parent existe. S'il n'existe pas, le créer avec `mkdir -p`.
  - Continuer vers l'étape 5.
- Si le fichier **existe déjà** → utiliser `AskUserQuestion` :
  > Le fichier `<path>` existe déjà. Que faire ? (append / overwrite / cancel)
  - `append` → ouvrir le fichier existant et ajouter une section `## Session YYYY-MM-DD` à la fin
  - `overwrite` → continuer vers l'étape 5 (écriture complète)
  - `cancel` → arrêter et informer l'utilisateur

### 5. Écrire le fichier

La date du jour est accessible via Bash : `date +%Y-%m-%d`

Créer le fichier avec le template suivant (remplacer `<slug>` par le slug résolu et `<YYYY-MM-DD>` par la date du jour) :

```markdown
---
feature: <slug>
date_start: <YYYY-MM-DD>
status: in-progress
---

# Implementation notes — <slug>

> Pattern Thariq : maintenu PENDANT l'implémentation, pas après. Append-only, format léger.

## Design decisions

_Choix faits où le ticket/spec était ambigu, avec la raison._

-

## Deviations

_Départs intentionnels du ticket/spec, avec la raison._

-

## Tradeoffs

_Alternatives considérées + pourquoi le choix retenu._

-

## Open questions

_À confirmer en review._

-
```

### 6. Confirmer à l'utilisateur

Afficher :
- Le path absolu du fichier créé
- Un rappel d'usage : "Complète ce fichier AU FUR ET À MESURE de l'implémentation (append-only). Ne pas attendre la fin."

## Gotchas

- **`$ARGUMENTS` interdit dans les backticks shell** — le slug vient de l'argument textuel lu dans `$ARGUMENTS`, jamais injecté directement dans une commande bash. Parser l'argument dans le raisonnement, puis passer la valeur résolue (variable locale) dans les commandes Bash.
- **neo_ia monorepo** — ne pas supposer le path par défaut. Si pas de préfixe `/` dans l'argument, toujours demander via AskUserQuestion plutôt que deviner.
- **mkdir -p avant Write** — si le dossier `docs/implementation-notes/` n'existe pas, le créer avant d'écrire le fichier.
- **Mode append** — si l'utilisateur choisit `append`, NE PAS réécrire le frontmatter. Ajouter uniquement une section datée à la fin du fichier existant.
- **Slug normalisation** — convertir les espaces en tirets, passer en minuscules. Ex : `Paiement Stripe` → `paiement-stripe`.

## Liens

- [[running-implementation-notes]] — Pattern Thariq source, vault `04-Techniques/patterns/`
- [[pattern-spec-driven-development]] — Pattern complémentaire (avant/après vs pendant)
- [[subagent-explore-then-edit]] — Variante avancée avec subagents pour grosses features

## Apprentissage

Après chaque utilisation significative de cette skill :
- Si un repo ne correspond à aucun pattern connu → documenter le mapping dans cette section
- Si le path monorepo pose problème → noter la convention retenue ici
- Si l'utilisateur a un workflow différent (ex : `.notes/` au lieu de `docs/`) → sauvegarder en mémoire projet
