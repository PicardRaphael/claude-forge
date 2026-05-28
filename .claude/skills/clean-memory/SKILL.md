---
name: clean-memory
description: ALWAYS invoke when the user types /clean-memory. Detects duplicate and dormant feedbacks in memory/MEMORY.md, proposes merges and archives with human gate per item. DO NOT archive or merge any feedback without invoking first.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__forge-brain__*
user-invokable: true
---

# clean-memory — Nettoyage de la memoire projet

Detecte les feedbacks doublons, amendements successifs et dormants dans `memory/MEMORY.md`, propose des fusions/archives avec validation humaine obligatoire par item.

**Usage** : `/clean-memory`

---

## Etape 1 — Lecture et mesure initiale

Resoudre la racine du repo et mesurer l'etat initial :

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
MEMORY_DIR="$REPO_ROOT/memory"
wc -l "$MEMORY_DIR/MEMORY.md"
du -sh "$MEMORY_DIR/MEMORY.md"
ls "$MEMORY_DIR"/feedback_*.md 2>/dev/null | wc -l
```

Lire `memory/MEMORY.md` EN ENTIER.

Puis, pour chaque candidat detecte (etapes suivantes), lire les fichiers feedback individuels concernes pour confirmer le contenu reel — pas juste le resumé de l'index.

Etat initial a noter :
- Lignes MEMORY.md : N
- Taille MEMORY.md : X KB
- Feedbacks racine (hors `_archive/`) : N

---

## Etape 2 — Analyse LLM en 4 sections

Produire l'analyse complete avant tout gate. Aucune ecriture a cette etape.

### Section A — Doublons conceptuels (fusion)

2+ feedbacks qui disent essentiellement la **meme chose** meme formules differemment. Exemple : un feedback "verifier avant d'affirmer" et un autre "ne pas affirmer sans preuve empirique" couvrent le meme pattern.

Pour chaque cluster A :
- Liste des membres (slug + resume)
- Concept commun propose pour le meta-feedback
- Slug consolide propose (descriptif du concept fusionné)

**Classification tier du meta-feedback consolide** :
- Tier-1 (MEMORY.md visible) si : ≥1 citation entrante apres fusion OU sujet strategique (3 axes innovation forge : MCP decoratif sub-agent, agent vs skill densite MCP vault, living doctrine) OU pinned manuel
- Tier-2 (`memory/_index_archive.md`) sinon — reintegrable tier-1 des premiere citation

### Section B — Amendements successifs (fusion)

Feedbacks v1 + v2 + ... sur le meme sujet, ou le dernier remplace les precedents. Exemple : `feedback_opus47_workflow.md` marque "RÉVISÉ 22 mai" et `feedback_effort_level_v1.md` couvrant la meme doctrine.

Pour chaque cluster B :
- Liste des membres (slug + resume + date si visible)
- Quel membre est le plus recent / complet
- Slug consolide propose

### Section C — Candidats AMBIGUS (arbitrage requis)

Patterns proches mais conceptuellement DISTINCTS. Le LLM **rejette la fusion par defaut** et presente l'analyse de distinction pour arbitrage.

Exemple canonique a ne PAS fusionner :
- `verify-empirique-avant-affirmation-session` (scope : affirmations en session)
- `diagnostic-empirique-avant-affirmer-une-garde` (scope : artefacts doctrinaux type settings/CLAUDE.md)
→ Meme reflex "verifier empiriquement" mais contextes d'application distincts — fusionner efface la nuance.

Pour chaque candidat ambigu :
- Les 2+ membres avec leur contexte d'application respectif
- Distinction conceptuelle precise (pourquoi ils sont differents)
- **Proposition : NE PAS fusionner** + justification
- Options d'arbitrage : `[fusion]` / `[separer]` / `[reformuler-nuance]`

### Section D — Feedbacks DORMANTS (archive solo)

**Critere necessaire mais NON suffisant** : etre jamais cite (pas de `[[slug]]` entrant dans les fichiers `feedback_*.md`).

**Critere DECISIF** (obligatoire pour proposer en section D) : le concept est **obsolete**, **depreciee**, ou **absorbe par un autre feedback actif** — avec preuve explicite.

**Regle stricte** : Si tu n'as QUE "pas de citation entrante" sans preuve d'obsolescence ou d'absorption, NE PROPOSE PAS le feedback en section D. Il reste en place.

Note de calibrage : sur ce vault, ~57% des feedbacks ne sont pas wikilinkes entre eux. L'absence de citation entrante est la norme, pas un signal de dormance.

Methode de detection (2 etapes) :

Etape 1 — verifier l'absence de citation :
```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
# Pour chaque feedback_X.md, chercher si son slug est reference dans d'autres
grep -r "feedback_<slug>" "$REPO_ROOT/memory/feedback_*.md" 2>/dev/null
```

Etape 2 — verifier la preuve d'obsolescence/absorption (OBLIGATOIRE) :
- Lire le contenu du feedback
- Chercher un feedback actif qui couvre explicitement le meme concept
- Ou identifier une decision documentee qui rend ce feedback caduc

Pour chaque dormant retenu (critere DECISIF satisfait) :
- Slug + resume
- Preuve d'obsolescence/absorption : "concept absorbe par [[slug-actif]] qui couvre X" ou "obsolete depuis [decision precise]"

### Section E — Promotion / Retrogradation tier

Audit des feedbacks tier-1 (visibles dans MEMORY.md) : verifier qu'ils satisfont encore le critere tier-1.

**Critere mecanique tier-1** (un seul suffit) :
- Au moins 1 citation entrante (`[[slug]]` dans un autre `feedback_*.md`)
- Sujet strategique (3 axes innovation forge : MCP decoratif sub-agent, agent vs skill densite MCP vault, living doctrine)
- Pinned manuel (marqueur `pin: true` dans frontmatter)

Pour chaque tier-1 ne satisfaisant AUCUN critere :
- Proposer retrogradation vers tier-2 (`_index_archive.md`)
- Justifier : "0 citation entrante, hors 3 axes strategiques, pas pinned"

Pour chaque tier-2 (`_index_archive.md`) ayant gagne une citation depuis dernier clean :
- Proposer promotion vers tier-1
- Justifier : "desormais cite par [[<slug-citant>]]"

Format gate :

```
Retrogradation tier-1 → tier-2 : [slug]
Citations entrantes : 0
Sujet strategique : non
Pinned : non
---
[v]alider retrogradation  [p]inner (garder tier-1)  [i]gnorer
```

```
Promotion tier-2 → tier-1 : [slug]
Cite par : [[<slug-citant>]]
---
[v]alider promotion  [i]gnorer
```

### Section "tout va bien"

Feedbacks qui restent en place : compte uniquement. Pas de detail.

---

## Etape 3 — Gate humain par section

Presenter chaque section et attendre la validation avant de passer a la suivante.

### Gate section A/B (clusters de fusion)

Pour chaque cluster :

```
Cluster [A/B] : <concept commun>
Membres :
  - [slug-1] : <resume>
  - [slug-2] : <resume>
  - (+ slug-3 si applicable)
Slug consolide propose : feedback_<slug-consolide>.md
---
[v]alider la fusion  [m]odifier les membres du cluster  [i]ignorer ce cluster
```

Option `[m]` — ajuster la composition du cluster AVANT fusion :
> Indiquer quel(s) membre(s) retirer (faux positifs) ou ajouter. Crucial pour eviter "tout ou rien" sur un cluster mixte (ex : 3 vrais doublons + 1 faux positif).

### Gate section D (dormants)

Pour chaque dormant :

```
Dormant : [slug]
Resume : <resume>
Raison : <pourquoi archive>
---
[v]alider l'archive  [i]ignorer
```

### Gate section C (ambigus)

Pour chaque candidat ambigu :

```
Candidat ambigu : [slug-1] vs [slug-2]
Distinction : <pourquoi ils sont conceptuellement distincts>
Recommandation : NE PAS fusionner — <justification>
---
[fusion]  [separer]  [reformuler-nuance]
```

`[reformuler-nuance]` = ajuster le resume de l'un ou des deux pour clarifier la distinction, sans fusion ni archive.

---

## Etape 4 — Execution selon arbitrages

**Principe : aucune modification sans validation explicite obtenue a l'etape 3.**

### Option α — Fusion validee (clusters A/B)

1. Lire les fichiers membres pour extraire le contenu complet.

2. Creer le meta-feedback consolide :

```markdown
---
name: <slug-consolide>
description: "<1 ligne specifique, concept fusionné>"
metadata:
  type: feedback
---

<Corps consolide : prend le meilleur de chaque membre, sans repetition>

**Why:** <raison originelle — cite les membres fusionnes>
**How to apply:** <quand cette regle s'applique>

Consolide depuis : [[feedback_<slug-1>]], [[feedback_<slug-2>]]
```

Chemin : `memory/feedback_<slug-consolide>.md`

3. Archiver les originaux (un par un) :
```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
ARCHIVE_DIR="$REPO_ROOT/memory/_archive/$(date +%Y-%m)"
mkdir -p "$ARCHIVE_DIR"
git -C "$REPO_ROOT" mv memory/feedback_<slug-original>.md memory/_archive/$(date +%Y-%m)/feedback_<slug-original>.md
```

4. Mettre a jour `memory/MEMORY.md` :
   - Retirer les lignes des originaux archives
   - Ajouter la ligne du meta-feedback en section appropriee

5. Ajouter l'entree au journal `memory/_archive/MEMORY-archive-log.md` :

```
## [YYYY-MM-DD] fusion — <concept consolide>
- **Fichiers** : feedback_<slug-1> → memory/_archive/YYYY-MM/feedback_<slug-1>.md, feedback_<slug-2> → memory/_archive/YYYY-MM/feedback_<slug-2>.md
- **Raison** : doublons conceptuels — meme pattern formule differemment
- **Meta-feedback** : feedback_<slug-consolide>.md
- **Index MEMORY.md** : entrees <slug-1>, <slug-2> retirees / entree <slug-consolide> ajoutee
- **Rollback** : git mv memory/_archive/YYYY-MM/feedback_<slug>.md memory/feedback_<slug>.md pour chaque archive, retirer le meta-feedback, restaurer les lignes index
```

### Option β — Archive solo dormant validee

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
git -C "$REPO_ROOT" mv memory/feedback_<slug>.md memory/_archive/$(date +%Y-%m)/feedback_<slug>.md
```

Puis retirer l'entree index dans MEMORY.md et ajouter l'entree journal :

```
## [YYYY-MM-DD] archive — <slug>
- **Fichiers** : feedback_<slug> → memory/_archive/YYYY-MM/feedback_<slug>.md
- **Raison** : dormant — jamais cite, concept absorbe par [[<slug-actif>]]
- **Rollback** : git mv memory/_archive/YYYY-MM/feedback_<slug>.md memory/feedback_<slug>.md, restaurer ligne index
```

### Regles d'ecriture (OBLIGATOIRES)

- Toujours `git mv` (jamais `mv` simple) — preserve l'historique.
- Commits multi-lignes via `-m` repetes, jamais here-string `@'...'@` (injecte un `@` littéral sur Windows).
- Ne jamais modifier un fichier une fois archive (`_archive/` est append-only sacre).
- Creer le dossier d'archive avec `mkdir -p` si inexistant.

---

## Etape 5 — Mesure d'impact et rapport final

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
MEMORY_DIR="$REPO_ROOT/memory"
wc -l "$MEMORY_DIR/MEMORY.md"
du -sh "$MEMORY_DIR/MEMORY.md"
ls "$MEMORY_DIR"/feedback_*.md 2>/dev/null | wc -l
```

Afficher le rapport :

```
## Clean-Memory — [date du jour]

### Etat initial
- MEMORY.md : N lignes / X KB
- Feedbacks racine : N

### Etat final
- MEMORY.md : N lignes / X KB  (delta : -N lignes)
- Feedbacks racine : N  (delta : -N)
- Feedbacks archives : N

### Operations effectuees
- Fusions (A/B) validees : N clusters → N meta-feedbacks crees, N originaux archives
- Archives solo (D) validees : N feedbacks
- Ambigus (C) : N analyses — N fusionnes / N separes / N reformules
- Ignores : N items

### Rollback disponible
Toute operation est reversible via `memory/_archive/` + `memory/_archive/MEMORY-archive-log.md`.
Procédure : git mv depuis _archive/ vers memory/, restaurer ligne index, ajouter entree "rollback" au journal.
```

---

## Gotchas

- **Append-only sacre sur `_archive/`** : ne jamais modifier un fichier apres ecriture dans `_archive/`. Seul le journal MEMORY-archive-log.md recoit des ajouts.
- **`git mv` obligatoire** (pas `mv` simple) — preserve l'historique git des fichiers archives.
- **Quoting Windows** : commits multi-lignes via `-m` repetes, jamais `@'...'@` (here-string PowerShell injecte un `@` en tete du titre).
- **Gate humain OBLIGATOIRE par item** : aucune fusion ni archive automatique. Meme si le doublon est evident.
- **Section C = rejeter la fusion par defaut** : ne JAMAIS fusionner deux feedbacks sur la seule base de proximite lexicale. Chercher la distinction de contexte d'application.
- **Path via `git rev-parse --show-toplevel`** : jamais `${CLAUDE_PROJECT_DIR}` (vide dans le shell d'une skill).
- **Lire les fichiers individuels** avant de proposer une fusion — pas juste les resumes de l'index (le resume peut etre tronque ou imprécis).
- **Un dormant ≠ un doublon** : dormant = pas cite = potentiellement obsolete. Doublon = meme concept = fusion. Les deux sections sont distinctes et separees.
- **Option [m] sur cluster** : permettre le retrait d'un faux positif AVANT de valider la fusion. Un cluster de 4 avec 1 faux positif ne doit pas etre abandonne mais ajuste.
- **MEMORY.md < 200 lignes** : si l'index approche la limite apres nettoyage, le signaler dans le rapport.
- **Declencheur re-clean** : MEMORY.md > 38k chars = signal a traiter dans session courte dediee. Marge 2k sous seuil systeme 40k pour maintenance anticipee.
- **Tier-1 = critere mecanique** : citation ≥1 OU 3 axes strategiques OU pinned. Pas d'"intuition tier-1" — sinon derive vers MEMORY.md obese.

---

## MCP — acces direct (filet de securite)

Tu recois normalement un brief enrichi de la session principale. Si pendant l'execution un element manque (terme inconnu, pattern incertain), tu peux re-consulter via `mcp__forge-brain__*`.

**Pas systematique** — filet de securite uniquement, pas exploration parallele.

**Quand l'utiliser** :
- Terme/acronyme non defini dans le brief
- Conflit entre 2 approches mentionnees
- Valeur precise necessaire
- Ne PAS re-verifier ce que le brief dit clairement

---

## Apprentissage

Apres avoir utilise `/clean-memory`, noter en memoire si :
- Un type de doublon revient systematiquement (signifie un pattern d'ecriture a corriger a la source dans `/done`)
- La section C produit souvent des fusions non souhaitees (calibrer les criteres de proximite)
- Le journal MEMORY-archive-log.md devient difficile a lire (refactorer en sections mensuelles)

Sauvegarder ces observations dans `project_clean_memory_patterns.md` si un pattern emerge sur plusieurs sessions.
