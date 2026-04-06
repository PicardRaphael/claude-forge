# Agent Delegation Rules - MANDATORY

## TOUJOURS deleguer. Ne JAMAIS explorer ou coder directement.

### Evaluation de la complexite

| Taille | Criteres | Action |
|--------|----------|--------|
| **S** | Bug fix, <3 fichiers | Agent direct |
| **M** | Nouveau endpoint, 3-5 fichiers | Architect (plan) → Dev |
| **L** | Migration domaine, >5 fichiers | Architect → TaskCreate → multi-Dev |

### Triage — Qui appeler quand

| L'utilisateur dit... | Agents |
|---------------------|--------|
| "J'ai besoin d'un endpoint pour X" | `api-designer` (design) → user valide → `dev` (skill add-endpoint) → `code-reviewer` → `performance-engineer` → `security-auditor` |
| "Migre la fonction f_xxx" | `refactor-pg-function` → `code-reviewer` → `validator` → `performance-engineer` |
| "Connecte la table X" | `dev` (skill connect-table) → `code-reviewer` |
| "Modifie l'endpoint, ajoute X" | `architect` (design) → `dev` → `code-reviewer` → `performance-engineer` |
| "Bug / erreur / ça marche pas" | `debugger` → `code-reviewer` |
| "C'est lent / performance" | `performance-engineer` → `dev` si fix → `code-reviewer` |
| "Audit sécurité / on release" | `security-auditor` → `dev` si fix → `security-auditor` (re-audit) |
| "Ajoute des tests" | `test-writer` |
| "Review mon code" | `code-reviewer` |
| "Explore cette table / montre les colonnes / FK" | `db-inspector` (exploration ad-hoc, questions ponctuelles) |
| "Analyse toute la BDD / génère la doc des domaines" | `schema-mapper` (génération doc/schemas/, clustering) |
| "Analyse les fonctions PG / le source de f_xxx" | `db-inspector` (peut lire le source via MCP) |
| "Où en est la migration ?" | Lire doc/migration-tracker.md directement |
| Ticket complexe | Découper → TaskCreate → router chaque tâche |

### Workflows types

**Nouvel endpoint :**
```
api-designer (design) → user valide → dev (skill add-endpoint)
  → code-reviewer → performance-engineer → security-auditor
```

**Migration fonction PostgreSQL :**
```
refactor-pg-function (analyse SQL + implémente)
  → code-reviewer → validator (équivalence) → performance-engineer
```

**Bug fix :**
```
debugger (diagnostic + fix) → code-reviewer
```

**Migration domaine entier (taille L) :**
```
architect (plan global) → user valide → TaskCreate
  → plusieurs refactor-pg-function en parallèle
  → code-reviewer (chaque migration) → validator (chaque migration)
  → performance-engineer (review global)
```

### Gates après implémentation

| Gate | Systématique | Conditionnel |
|------|-------------|-------------|
| `code-reviewer` | TOUJOURS | — |
| `validator` | Migrations PG | — |
| `performance-engineer` | Features + Migrations | "C'est lent" |
| `security-auditor` | Nouveaux endpoints | Avant release |

### Comment déléguer

Inclure dans le prompt de l'agent :
1. Demande exacte de l'utilisateur
2. Type de tâche (migration / feature / modification / bug)
3. Fichiers/tables/fonctions concernées
4. Taille évaluée (S/M/L)
5. Contexte pertinent (domaine, règles métier)

### Main Claude directement (PAS de delegation)

- Questions sur le projet
- Statut migration → lire doc/migration-tracker.md
- Git (commit, push, status)
- Configuration .claude/
