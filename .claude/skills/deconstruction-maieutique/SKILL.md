---
name: deconstruction-maieutique
description: ALWAYS invoke to deconstruct a book, podcast, article or talk into atomic concept-notes via maieutic questioning — 'déconstruis ce livre', 'décortique ce podcast'. Runs AFTER /watch. NOT for transcribing (watch) or searching sources (deep-research).
user-invocable: true
allowed-tools: Read, mcp__forge-brain__*
model: opus
effort: high
---

# Déconstruction maïeutique

Transforme un contenu déjà disponible (livre, podcast, article, talk — texte collé ou transcript `/watch`) en **notes-concepts atomiques** (1 concept = 1 note) via un questionnement maïeutique. Une seule transformation : contenu → notes-concepts `draft`.

Frontières : ≠ `watch` (qui transcrit une vidéo) — cette skill vit APRÈS, sur le contenu déjà en texte. ≠ `deep-research` / `web-search-canonical-source` (qui vont chercher dehors) — ici on travaille la matière fournie, on ne cherche pas.

## Étapes

1. **Extraire les concepts saillants** — parcourir le contenu, isoler les idées portantes (pas les anecdotes). 1 concept = 1 note potentielle. Viser l'atomicité : une note qui porte deux idées se scinde.
2. **Questionner chaque concept (maïeutique)** — pour chacun, poser et répondre :
   - Quelle est la **prémisse de l'auteur** (sur quoi repose l'idée) ?
   - Quelle est sa **valeur** (qu'apporte-t-elle, pour quoi) ?
   - **Qu'est-ce qui me challenge** / me semble discutable ?
   - **À quel projet / note existante ça se connecte** ?
3. **Suggérer les liens** — proposer les wikilinks vers les notes vault existantes (`search_brain` pour trouver les foyers). **Garde-fou Karpathy : l'IA SUGGÈRE, l'humain tranche.** Présenter les liens candidats pour validation, ne jamais promulguer la couche d'interconnexion d'office.
4. **Rendu en notes `draft`** — créer les notes-concepts via `mcp__forge-brain__create_note` avec `status: draft` (frontmatter standard : aliases, resume, tags, derniere-maj). Les liens suggérés restent marqués comme propositions tant que Raphael ne valide pas.

## Garde-fou interconnexion (Karpathy)

La valeur d'un vault vient de sa couche de liens, et c'est précisément ce que l'humain doit garder. La skill propose des wikilinks (candidats étayés par `search_brain`), elle ne les fige pas. Sortie : notes `draft` + liste de liens proposés à valider — jamais un graphe promulgué seul.

## Gotchas

- Atomicité d'abord : une note = un concept. Deux idées dans une note = scinder, sinon le vault devient illisible.
- Concept saillant ≠ citation marquante : on extrait l'IDÉE réutilisable, pas le bon mot.
- Liens = suggestions tant que non validés (garde-fou Karpathy). Pas de wikilinks « durs » non confirmés.
- Notes toujours en `status: draft` — la promotion vers canonique est une décision humaine.
- Ne pas chercher de sources externes pour « compléter » — c'est `deep-research`. Ici on travaille la matière fournie.

## Apprentissage

Après usage : si un type de questionnement maïeutique ou un pattern d'extraction se révèle particulièrement fécond pour un format donné (livre vs podcast vs article), le noter ici.
