---
titre: "Pattern déploiement skill /spec sur un nouveau repo"
resume: "Guide complet pour déployer la skill /spec (interview → exploration → architecture → génération) sur n'importe quel repo Claude Code. Structure, adaptations, agents requis"
aliases:
  - deployer spec
  - spec deployment
  - spec nouveau repo
  - skill spec template
  - installer spec
domaine: claude-code
type: technique
derniere-maj: 2026-05-12
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/workflow"
auteur: claude
---

## Prérequis du repo cible

- Agent `architect` (obligatoire — phase 3)
- Agent `codebase-analyst` ou équivalent read-only (obligatoire — phase 2)
- Agent `code-reviewer` (optionnel — contradiction check)
- `AskUserQuestion` dans les allowed-tools

## Structure à copier

```
.claude/skills/spec/
  SKILL.md                          ← < 500 lignes
  references/
    output-templates.md             ← templates M/L/XL adaptés au stack
    interview-bank.md               ← banque de questions par type
    contradiction-prompt.md         ← prompt inline + exemples
```

## Adaptations obligatoires

### 1. Phase 2 — Exploration

Remplacer les agents par ceux du repo local :

| Stack | Agents phase 2 |
|-------|----------------|
| TypeScript/Bun hexagonal (ia_back) | `codebase-analyst` + `db-inspector` + MCP postgres |
| Python/FastAPI monorepo (neo_ia) | `codebase-analyst` + skill `neo-brain-dev-ia` |
| Frontend Vue/React | `codebase-analyst` seul |
| Nouveau repo sans agents | Glob/Read direct (pas d'agents dispo) |

### 2. Phase 3 — Architecture

- Si le repo a `api-designer` → l'ajouter pour le design d'endpoints
- Si le repo a un pipeline architect-first → le mentionner dans le handoff

### 3. Output templates

Adapter `references/output-templates.md` au stack :
- Hexagonal (ia_back) : entity, port, repository, use-case, route
- Monorepo Python (neo_ia) : tool, schemas, prompts, routing, config.yaml
- MVC : controller, service, model, migration
- Frontend : composant, store, route, test

### 4. Skills disponibles

Dans le template BRIEF, lister les skills du repo pour l'implémentation :
- ia_back : `/add-endpoint`, `/connect-table`, `/go`
- neo_ia : `/create-tool`, `/create-agent`, `/go`
- Autre : adapter

### 5. MCP et contexte BDD

- Si accès vault neoteem-brain → `skills: neo-brain-dev-ia` dans frontmatter
- Si MCP postgres disponible → requêtes SQL directes en phase 2
- Si aucun MCP → Glob/Read sur les fichiers de schéma/migration

## Calibration gate

Toujours le même, indépendant du stack :

| Taille | Critères (déterminés APRÈS phase 2) |
|--------|-------------------------------------|
| M | 1 repo, < 5 fichiers à toucher |
| L | 2+ repos OU < 15 fichiers |
| XL | 2+ repos, 15+ fichiers, multi-sprint |

Pas de taille S — un bug trivial ne justifie pas /spec.

## Cross-BRIEF contradiction detection

Applicable uniquement si multi-BRIEF (taille L/XL). Le prompt dans `references/contradiction-prompt.md` est générique — adapter les exemples aux contrats d'interface du projet.

Exemples à adapter :
- Format réponse API (champs, nommage)
- Responsabilité de création (qui crée la ressource)
- Pagination vs liste complète
- Auth (JWT vs body vs query param)

## Pipeline complet

```
/spec → TODO/feature-<nom>/ → /decompose-ticket [optionnel XL] → /go
```

Si le repo n'a pas `/decompose-ticket`, `/spec` suffit — le BRIEF est assez clair pour exécuter directement via `/go` ou manuellement.

## Liens

- [[MOC-Techniques]]
- [[pattern-spec-driven-development]] — Recherche complète SDD
- [[feature-dev-plugin]] — Plugin Anthropic complémentaire
- [[pattern-architect-first-pipeline]] — Pipeline d'exécution en aval