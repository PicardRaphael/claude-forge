---
name: reasoning-cache
description: Captures a successful multi-step reasoning chain as a vault note for future reuse. Use PROACTIVELY after solving a complex problem where the path reversed direction at least once, or where a non-obvious approach was chosen over an obvious one. ALWAYS invoke when the user says save this reasoning, cache this, or after a multi-step debug that changed direction.
argument-hint: "[problem description] [-- steps]"
allowed-tools: Bash, Read, Write, Glob, mcp__forge-brain__*
user-invokable: true
effort: high
memory: project
---

Caches the reasoning PATH (not the solution) that led to a validated outcome, as a vault note in `Knowledge/raisonnements/`. Next time a similar problem surfaces, reasoning starts from the working chain — not from zero.

## Usage

```
/reasoning-cache                          — prompt guided (interactive)
/reasoning-cache "problem description"   — quick cache with description
```

The note captures: problem type, context, numbered reasoning steps, the key non-obvious insight, outcome, and a reuse signal pattern.

## Etapes

### 0. Utiliser $ARGUMENTS comme point de depart

Si la skill est invoquee avec des arguments (`/reasoning-cache "mon probleme"`), utiliser ce texte comme description initiale du probleme a l'etape 2. Les etapes du raisonnement viennent du contexte de la conversation courante.

### 1. Determiner si le raisonnement merite d'etre cache

Un raisonnement est cache-worthy quand :
- Il a inverse de direction au moins une fois (premier instinct wrong)
- L'approche choisie n'est pas celle qu'on aurait naturellement prise
- Le probleme est susceptible de revenir (type recurrent : architecture, debug, selection de technique)
- L'insight cle serait difficile a reconstruire sans relire toute la session

Si aucune de ces conditions n'est satisfaite, ne pas cacher — c'est du bruit.

### 2. Preparer le contenu

Identifier et formaliser :
- **Type de probleme** : `architecture-decision`, `bug-investigation`, `technique-selection`, `optimization`, `debugging`, `refactoring`
- **Domaine** : projet concerne ou `general`
- **Chaine de raisonnement** : etapes numerotees — la LOGIQUE, pas le code ni les commandes
- **Insight cle** : quelle etape etait la non-evidente, pourquoi ca a marche
- **Signal de reutilisation** : le pattern qui devrait declencher ce raisonnement

### 3. Rechercher des raisonnements similaires existants

```
forge-brain:search_brain query="<mots-cles du probleme>" limit=10
```

Si un raisonnement similaire existe : verifier si une mise a jour vaut mieux qu'une nouvelle note.

### 4. Identifier les notes liees

```
forge-brain:search_brain query="<technique ou erreur associee>" limit=5
```

Collecter 2-3 wikilinks pertinents pour la section `## Liens`.

### 5. Creer la note vault

**IMPORTANT — creation avec MCP `create_note(path, content)`**. Le MCP gere le YAML sans probleme.

Chemin : `vault/claude-forge/Knowledge/raisonnements/<slug>.md`

Format du slug : `<type>-<3-mots-cles>.md` (ex : `architecture-decision-hooks-vs-rules.md`)

Lire le template avant de creer :
```bash
# Reference : vault/claude-forge/Templates/raisonnement.md
```

Structure obligatoire (voir section **Template** ci-dessous).

### 6. Mettre a jour la date

```
forge-brain:update_property file="<nom-note>" name="derniere-maj" value="YYYY-MM-DD"
```

### 7. Lier au MOC-Techniques

Ajouter le wikilink dans `vault/claude-forge/00-Hub/MOC-Techniques.md` sous la section la plus pertinente.

Format : `- [[<nom-note>]] — <une ligne de description>`

## Template note raisonnement

```markdown
---
titre: "[type] — [description du probleme en une ligne]"
resume: "[ce que ce raisonnement apporte]"
aliases:
  - "alias-fr-1"
  - "alias-fr-2"
  - "alias-en-1"
  - "alias-en-2"
  - "alias-technique-1"
  - "alias-technique-2"
type: raisonnement
domaine: [projet ou general]
derniere-maj: YYYY-MM-DD
auteur: claude
tags:
  - "#type/raisonnement"
  - "#domaine/[domaine]"
---

## Probleme

[Ce qu'on cherchait a resoudre — 2-3 phrases max]

## Contexte

[Projet, contraintes, ce qui avait deja ete essaye]

## Chaine de raisonnement

1. [Etape 1 — premiere approche ou hypothese initiale]
2. [Etape 2 — ce que ca a revele / pourquoi ca n'a pas marche]
3. [Etape 3 — le pivot ou la decouverte]
4. [Etape 4 — validation de la nouvelle approche]
...

## Insight cle

**[L'etape non-evidente]** — [Pourquoi ca a marche quand les approches simples n'ont pas marche. C'est la partie qui se perd entre sessions.]

## Resultat

[Outcome concret + validation (tests passes, solution deployee, decision prise)]

## Reutilisation

Utiliser ce raisonnement quand : [description precise du pattern de declenchement]

## Liens

- [[note-liee-1]]
- [[note-liee-2]]
```

## Aliases — standard 4-6 minimum

Inclure obligatoirement :
- 2 synonymes FR (ex : "cacher raisonnement", "trace de pensee")
- 2 synonymes EN (ex : "reasoning chain", "thought process cache")
- 1-2 variantes techniques (ex : "chain-of-thought cache", type de probleme specifique)

## Gotchas

- **Ne pas cacher la solution, cacher le chemin** : le code/commit contient la solution. Ce qu'on veut conserver c'est le fork pris et pourquoi.
- **MCP forge-brain pour tout** — search, create, append, update_property. Plus de distinction Write vs CLI.
- **Insight cle = critere de validation** : si on ne peut pas remplir cette section avec quelque chose de non-evident, le raisonnement ne vaut pas la peine d'etre cache.
- **Slug unique** : verifier qu'un fichier du meme nom n'existe pas avant de creer. Format `<type>-<3-mots-cles>.md`.
- **MOC obligatoire** : chaque note cree DOIT etre linkee dans MOC-Techniques. Oublier le MOC = note orpheline.
- **$ARGUMENTS jamais dans des backtick shell** : passer le contenu comme texte au prompt, utiliser les outils agent (Read, Bash) pour les operations sur fichiers.
- **Aliases minimum 4-6** : standard vault forge-brain. Moins = note non trouvable par search.
- **Fallback si CLI indisponible** : pre-check `version` avant tout appel CLI. Si echec → utiliser Read/Glob/Grep directement sur les fichiers du vault.

## MCP — accès direct (filet de sécurité)

Tu reçois normalement un brief enrichi de la session principale avec les éléments MCP pertinents déjà extraits (vault, DB, docs). Si pendant l'exécution tu rencontres un doute non couvert par ton brief (terme inconnu, décision technique conflictuelle, pattern incertain, valeur précise non fournie), tu peux re-consulter directement le MCP via `mcp__forge-brain__*`.

**Pas systématique** — la session principale t'a déjà briefé. C'est un filet de sécurité, pas une exploration parallèle. Anti-pattern : scanner par réflexe (coût tokens × N agents).

**Quand l'utiliser** :
- ✅ Terme/acronyme non défini dans le brief
- ✅ Conflit entre 2 approches mentionnées
- ✅ Valeur précise nécessaire (note canonique exacte)
- ❌ Re-vérifier ce que le brief dit clairement
- ❌ "Au cas où" sans déclencheur précis

Source canonique : [[pattern-mcp-brief-then-direct]] vault forge.

## Apprentissage

Apres avoir utilise cette skill, si un pattern emerge :
- Quel type de probleme revient le plus souvent dans les raisonnements caches ?
- Les aliases generes sont-ils suffisamment precis pour que les searches futures trouvent la note ?
- Y a-t-il des domaines sous-representes dans Knowledge/raisonnements/ ?

Sauvegarder ces observations dans la memoire projet via un fichier `project_reasoning_cache_patterns.md`.
