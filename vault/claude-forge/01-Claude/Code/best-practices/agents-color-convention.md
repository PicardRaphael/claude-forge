---
titre: "Convention couleurs agents Claude Code"
resume: "Standard cross-repo pour les couleurs agents — même rôle = même couleur sur tous les repos, identification visuelle instantanée dans Desktop et CLI."
aliases:
  - "convention couleurs agents"
  - "agent color convention"
  - "couleurs agents"
  - "agent colors"
  - "palette agents"
  - "color standard agents"
type: best-practice
derniere-maj: 2026-05-24
auteur: claude
tags:
  - "#type/best-practice"
  - "#domaine/claude-code"
  - "#domaine/agents"
---

# Convention couleurs agents Claude Code

Standard appliqué sur tous les repos Neoteem (claude-forge, ia_back, neo_ia).

## Règle fondamentale

**Même rôle = même couleur sur TOUS les repos.** Un agent `architect` est toujours bleu, qu'il soit dans ia_back ou neo_ia.

## Palette par catégorie

| Couleur | Catégorie | Exemples |
|---------|-----------|----------|
| **red** | Sécurité / Critique | security-auditor, security-reviewer, devils-advocate |
| **orange** | Review / Validation | code-reviewer, validator, sql-optimizer |
| **yellow** | Test / Évaluation / Debug | test-writer, outcomes-grader, debugger, build-error-resolver |
| **green** | Développement | dev, dev-neochat, dev-neodoc, dev-neomail, dev-shared-tools, python-dev, performance-engineer |
| **blue** | Architecture / Design | architect, api-designer, db-inspector |
| **purple** | Analyse / Stratégie | project-analyzer, project-auditor, schema-mapper, dev-lead, codebase-analyst |
| **cyan** | Infra / Maintenance | self-updater, vault-maintainer, refactor-pg-function, repo-functions-analyzer |
| **pink** | Meta-créateurs (forge) | agent-creator, skill-creator, hook-creator, claudemd-optimizer |

## Comment choisir la couleur d'un nouvel agent

1. Identifier la catégorie principale de l'agent
2. Appliquer la couleur correspondante
3. En cas de doute entre 2 catégories, choisir celle de l'action principale (un agent qui analyse puis corrige = vert dev, pas purple analyse)

## Contexte

Adopté le 2026-05-21 après constat que les couleurs étaient incohérentes entre repos (architect purple/blue, test-writer green/yellow). Le problème était visible dans [[Claude Desktop]] : les tâches en arrière-plan affichent un point coloré mais pas le nom de l'agent explicitement.

## Liens

- [[methode-analyser-repo]] — setup CC incluant les agents
- [[comment-creer-agent]] — patterns d'orchestration agents
