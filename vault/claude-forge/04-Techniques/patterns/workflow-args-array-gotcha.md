---
titre: "Gotcha Dynamic Workflow — args array/objet arrive undefined"
resume: "Passer un array/objet JSON via le param args du tool Workflow échoue (args undefined → pipeline() expects an array). Solutions validées : embarquer les données en constante JS dans le script, ou faire lire un fichier par un 1er agent qui retourne la liste via schema. Chemins de fichiers en dur OK."
aliases:
  - "workflow args array gotcha"
  - "args undefined dynamic workflow"
  - "pipeline expects an array"
  - "passer données à un workflow"
  - "const JS vs args workflow"
derniere-maj: 2026-06-07
auteur: claude
type: pattern
tags:
  - "#type/pattern"
  - "#domaine/claude-code"
  - "#domaine/workflow"
---

# Gotcha Dynamic Workflow — args array/objet arrive undefined

> Passer une structure JSON non-triviale via le paramètre `args` du tool Workflow échoue silencieusement : le global `args` du script arrive `undefined`.

## Cas empirique (2026-05-29, skill /clean-memory)

Deux workflows lancés avec une liste de slugs/objets passée via `args` ont échoué immédiatement : `TypeError: pipeline() expects an array as the first argument`, durée ~20ms, 0 agent. Le global `args` était `undefined` malgré un array JSON valide passé dans le tool call.

## Solutions validées (même session)

- **Embarquer les données en constante JS** dans le corps du script : `const targets = [{...}, ...]`. Le workflow slim-pointeurs (22 objets en dur) a tourné sans souci. Pour itérer : `Write`/`Edit` le `scriptPath` puis re-`Workflow`.
- **Faire lire un fichier par un 1er agent** : agent `Read` le fichier + retourne la liste via `schema`, puis `pipeline(listed.slugs, ...)`. Le workflow classify (216 slugs lus depuis `.claude/_clean_slugs.txt`) a tourné.

## Règle

Ne pas compter sur `args` pour des structures non-triviales dans un Dynamic Workflow. Les **chemins de fichiers en dur** dans le script marchent bien (les agents ont accès au FS ; le script JS lui-même non).

## Wikilinks

- [[mcp-vault-llm-design]] — outillage MCP/vault pour LLM
- [[pattern-maintenance-hybride-corpus-accumulatif]] — contexte d'usage (workflows clean-memory)
