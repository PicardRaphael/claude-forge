---
description: "Apply 8-color convention on all agents (red sec/orange review/yellow test/green dev/blue archi/purple analyse/cyan infra/pink meta). Same role = same color cross-repo."
---

# Convention couleurs agents — OBLIGATOIRE

Chaque agent DOIT avoir un champ `color` dans son frontmatter YAML. La couleur dépend de la catégorie :

| Couleur | Catégorie | Quand l'utiliser |
|---------|-----------|-----------------|
| **red** | Sécurité / Critique | Audits sécu, devil's advocate |
| **orange** | Review / Validation | Code review, validation, optimisation SQL |
| **yellow** | Test / Évaluation / Debug | Tests, grading, debugging, build errors |
| **green** | Développement | Implémentation features, dev par app |
| **blue** | Architecture / Design | Architect, API design, DB inspection |
| **purple** | Analyse / Stratégie | Analyse codebase, audit projet, schema mapping |
| **cyan** | Infra / Maintenance | Refactoring, maintenance, migration |
| **pink** | Meta-créateurs (forge only) | Création d'agents/skills/hooks/CLAUDE.md |

## Règle cross-repo

Même rôle = même couleur sur TOUS les repos. Un `architect` est toujours `blue`.

## Référence

Vault : `01-Claude/Code/best-practices/agents-color-convention.md`
