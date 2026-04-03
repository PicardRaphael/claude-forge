# Agent Delegation Rules - MANDATORY

## Regles de Delegation (OBLIGATOIRE)

**TOUJOURS deleguer aux agents specialises. Ne JAMAIS explorer ou coder directement.**

### Evaluation de la complexite (AVANT delegation)

| Taille | Criteres | Action |
|--------|----------|--------|
| **S** | Bug fix, <3 fichiers | Agent direct (debugger ou dev) |
| **M** | Nouveau endpoint, 3-5 fichiers | Architect (plan) → Dev |
| **L** | Migration domaine entier, >5 fichiers, multi-tables | Architect (plan) → TaskCreate → multi-Dev paralleles |

### → Agent `architect` (design + review)

Deleguer TOUJOURS quand :
- **Design** d'un nouvel endpoint ou modification
- **Analyse d'impact** d'un changement
- **Review du code** apres le dev
- **Planifier une migration** de fonction PostgreSQL
- **Explorer le codebase** pour comprendre l'architecture

Exemples : "J'ai besoin d'un endpoint pour...", "Comment migrer f_xxx ?", "Analyse l'impact de...", "Review le code du dev"

### → Agent `dev` (implementation)

Deleguer quand :
- **Implementer** un plan valide par l'architecte
- **Creer/modifier** un endpoint, service, repository
- **Appliquer un fix** valide par le debugger
- **Corriger** un probleme signale par security-auditor ou performance-engineer

Le dev charge la skill appropriee selon le type de tache :
- Migration → skill `migrate-function`
- Nouvel endpoint → skill `create-endpoint`
- Modification → skill `update-endpoint`

### → Agent `debugger` (diagnostic + fix)

Deleguer quand :
- **Bug** signale par l'utilisateur
- **Erreur** / crash / comportement inattendu
- **Donnees incorrectes** retournees par un endpoint

Exemples : "Y a un bug sur...", "Ca marche pas", "L'endpoint retourne des doublons", "Erreur 500 sur..."

### → Agent `validator` (equivalence comportementale)

Deleguer APRES le dev et l'architect review, quand :
- Une **fonction PostgreSQL a ete migree** vers un endpoint
- Besoin de verifier que le code migre fait la meme chose que l'original

**Hard gate** : FAIL = retour au dev.

### → Agent `performance-engineer` (profiling + review perf)

Deleguer quand :
- **Lenteur** signalee par l'utilisateur
- **Review performance** apres creation/modification d'un endpoint
- **Requete SQL complexe** (6+ jointures, pas d'index)

Exemples : "C'est lent sur...", "L'endpoint met 5 secondes"

Aussi appele systematiquement apres le dev pour les features et migrations.

### → Agent `security-auditor` (audit securite)

Deleguer quand :
- **Audit securite** demande (avant release, revue periodique)
- **Nouvel endpoint** cree (audit automatique)
- **Vulnerabilite** suspectee

Exemples : "Fais un audit secu", "Verifie la securite de...", "On release vendredi"

### → Agent `repo-functions-analyzer` (analyse repo fonctions)

Deleguer quand :
- **Comprendre un domaine** du repo fonctions PostgreSQL
- **Inventorier les fonctions** d'un schema
- **Analyser les dependances** entre fonctions

Exemples : "Analyse le domaine copro", "Quelles fonctions touchent la table X ?"

### → Agent `schema-mapper` (analyse BDD)

Deleguer quand :
- **Premiere analyse** de la BDD (generer doc/schemas/)
- **Decouverte des domaines** et clusters de tables

Exemples : "Analyse ma BDD", "Genere la doc des domaines"

### → Agent `sql-optimizer` (optimisation SQL)

Deleguer quand :
- Une **requete SQL a besoin d'optimisation**
- L'architect ou le performance-engineer identifie un probleme SQL

### → Main Claude directement (PAS de delegation)

Repondre directement UNIQUEMENT pour :
- **Questions** sur le projet, l'avancement, l'architecture
- **Statut migration** → lire doc/migration-tracker.md
- **Configuration** .claude/ (rules, hooks, settings)
- **Git** (commit, push, status)

## Workflows types

### Feature / Nouvel endpoint

```
Utilisateur : "J'ai besoin d'un endpoint pour recuperer les copros"
    |
Main Claude : taille = M, type = feature
    |
    +-- architect (design technique)
    |       +-- Produit : plan (route, SQL, types, fichiers)
    |
    +-- Main Claude : presente le plan, attend validation utilisateur
    |
    +-- dev (implemente le plan, skill create-endpoint)
    |
    +-- architect (review code)
    |       +-- OK ou corrections → retour dev
    |
    +-- performance-engineer (review perf)
    +-- security-auditor (audit)
    |
    +-- Main Claude : presente le resultat
```

### Migration fonction PostgreSQL

```
Utilisateur : "Migre la fonction f_get_proprietaires"
    |
Main Claude : taille = M, type = migration
    |
    +-- architect (design)
    +-- Main Claude : validation utilisateur
    +-- dev (skill migrate-function)
    +-- architect (review)
    +-- validator (equivalence comportementale) ← HARD GATE
    +-- performance-engineer (review perf)
    |
    +-- Main Claude : presente le resultat
```

### Bug fix

```
Utilisateur : "Bug sur GET /copros, retourne des doublons"
    |
Main Claude : taille = S, type = bug
    |
    +-- debugger (diagnostic + fix)
    +-- architect (review du fix)
    |
    +-- Main Claude : presente le resultat
```

### Migration complexe (domaine entier)

```
Utilisateur : "Migre tout le domaine copro"
    |
Main Claude : taille = L, type = migration
    |
    +-- architect (plan global + decoupe en taches)
    +-- Main Claude : validation utilisateur
    +-- TaskCreate (une tache par fonction a migrer)
    +-- Plusieurs dev en parallele
    +-- architect (review de chaque migration)
    +-- validator (chaque migration)
    +-- performance-engineer (review global)
    |
    +-- Main Claude : presente le resultat
```

## Comment deleguer

Inclure dans le prompt de l'agent :
1. La demande exacte de l'utilisateur
2. Le type de tache (migration / feature / modification / bug)
3. Les fichiers/tables/fonctions concernees si connus
4. La taille evaluee (S/M/L)
5. Le contexte pertinent (domaine, regles metier connues)
