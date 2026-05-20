---
titre: "Codebase Maps — Markdown table of contents pour navigation Claude"
resume: "Fichier markdown léger à la racine listant chaque dossier top-level avec une description une-ligne — donne à Claude une table des matières scannable avant d'ouvrir des fichiers"
aliases:
  - "codebase map"
  - "codebase maps pattern"
  - "table of contents codebase"
  - "claude code map directory"
  - "monorepo map"
  - "structure markdown claude"
domaine: claude-code
type: technique
derniere-maj: 2026-05-20
auteur: claude
sources:
  - "https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#pattern/navigation"
---

## Le problème

Sur une codebase grosse ou non-conventionnelle (structure historique, monorepo avec 100+ dossiers top-level, naming non-standard), Claude perd du temps à ouvrir des fichiers pour comprendre où il est. Résultat : contexte saturé avant que le vrai travail commence.

## La solution

> "A lightweight markdown file at the repo root listing each top-level folder with a one-line description of what lives there gives Claude a table of contents it can scan before opening files." — Anthropic blog 14 mai 2026

Un fichier `CODEBASE-MAP.md` (ou inclus dans `CLAUDE.md`) à la racine avec UN dossier par ligne et UNE description par dossier.

## Format minimal

```markdown
# Codebase Map

| Dossier | Contenu |
|---------|---------|
| `apps/api` | API REST FastAPI principale |
| `apps/worker` | Workers Celery (jobs async) |
| `libs/auth` | Auth shared (JWT, OAuth) |
| `libs/db` | Modèles SQLAlchemy partagés |
| `tools/migrations` | Scripts Alembic |
| `infra/terraform` | IaC AWS |
```

## Approche layered (pour très grosses codebases)

Pour codebases avec hundreds of top-level folders : un seul fichier au root devient illisible. Stratégie en couches :

1. **Root** : décrit uniquement les **groupes** de top-level folders (ex: `apps/`, `libs/`, `tools/`, `infra/`)
2. **Subdirectory CLAUDE.md** : décrit le détail des dossiers de cette section
3. **Chargement on-demand** : Claude lit le root, puis charge la section relevante quand il y descend

Exemple structure :

```
/CLAUDE.md              ← description groupes top-level
/apps/CLAUDE.md         ← description détaillée des apps
/apps/api/CLAUDE.md     ← conventions API spécifiques
/libs/CLAUDE.md         ← description détaillée des libs
```

## Quand utiliser

- ✅ Codebase avec > 20 dossiers top-level
- ✅ Naming non-évident (ex: dossiers historiques, projet-codename internes)
- ✅ Structure non-conventionnelle (pas standard Maven/npm/Cargo)
- ✅ Monorepo avec services hétérogènes
- ❌ Petit projet avec structure standard → ratio coût/bénéfice faible

## Variante — @-mention pour cas simples

> "For simpler cases, @-mentioning the specific files or directories Claude should reference can do the same job."

Sur une codebase de taille moyenne, plutôt qu'un fichier dédié, simplement dans le CLAUDE.md ou le prompt :

```
Le code de l'auth se trouve dans @libs/auth/
Les migrations sont gérées dans @tools/migrations/
```

## Pièges

- ❌ Map trop verbeuse — au-delà d'une ligne par dossier, ça devient du noise
- ❌ Map qui se désynchronise — ajouter au [[changelog-vault]] et l'update à chaque restructure
- ❌ Dupliquer dans CLAUDE.md ET CODEBASE-MAP.md → pollute le contexte. Choisir un seul endroit.
- ❌ Décrire le **comment** plutôt que le **quoi** — la map dit où, pas comment le code fonctionne

## Application aux repos Neoteem

| Repo | Map nécessaire ? | Justification |
|------|------------------|---------------|
| ia_back | ⚠️ peut-être | Structure FastAPI standard, mais > 30 modules — utile pour discovery |
| neo_ia | ✅ recommandé | Monorepo NeoChat/NeoDoc/NeoMail, structure non-évidente |
| bdd | ✅ recommandé | 2779 fichiers, structure PG/PL-pgSQL atypique |
| lojii | ⚠️ peut-être | 634 composants Vue, hiérarchie composants à documenter |
| neoteem-brain | ❌ non | Structure vault Obsidian déjà self-documenting |

## Liens

- [[claudemd-guide]] — Layered CLAUDE.md (concept parent)
- [[setup-project-complet]] — Setup global d'un repo
- [[harness-engineering]] — Codebase navigation est partie du harness
- [[best-practices-claude-code-leaders]] — Synthèse leaders
