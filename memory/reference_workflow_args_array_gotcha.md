---
name: workflow-args-array-gotcha
description: "Dynamic Workflow : passer un array/objet JSON complexe via le param `args` du tool Workflow échoue (args arrive undefined → pipeline() expects an array). Embarquer les données en constante JS dans le script, ou les faire lire par un 1er agent."
metadata:
  type: reference
---

Cf [[pattern-maintenance-hybride-corpus-accumulatif]] (contexte d'usage : workflows clean-memory).

**Cas empirique (2026-05-29)** : sur la skill /clean-memory, 2 workflows lancés avec une liste de slugs/objets passée via le param `args` de l'outil Workflow ont échoué immédiatement (`TypeError: pipeline() expects an array as the first argument`, duration ~20ms, 0 agent). Le global `args` du script était `undefined` malgré un array JSON valide passé dans le tool call.

**Solutions qui marchent** (validées la même session) :
- **Embarquer les données en constante JS** dans le corps du script (`const targets = [{...}, ...]`). Le 3e workflow (slim-pointeurs, 22 objets en dur) a tourné sans souci.
- **Faire lire un fichier par un 1er agent** : agent `Read` le fichier + retourne la liste via schema, puis `pipeline(listed.slugs, ...)`. Le 2e workflow (classify, 216 slugs lus depuis `.claude/_clean_slugs.txt`) a tourné.

**How to apply** : ne pas compter sur `args` pour des structures non-triviales dans un Dynamic Workflow. Mettre les données dans le script (Write/Edit le scriptPath puis re-Workflow) ou les charger via agent. Les chemins de fichiers en dur dans le script marchent bien (les agents ont accès FS, pas le script JS lui-même).
