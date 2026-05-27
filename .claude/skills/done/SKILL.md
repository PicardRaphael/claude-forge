---
name: done
description: End-of-session metacognition -- extracts decisions, facts, preferences, and errors from the current conversation, updates vault and memory automatically. Use when the user types /done or at session end.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__forge-brain__*
user-invokable: true
---

# done -- Metacognition de fin de session

Analyse la conversation courante et capitalise les apprentissages en memoire projet et vault forge-brain.

**Usage** : `/done`

La conversation courante EST le contexte d'analyse. **Aucun fichier transcript externe n'existe** -- refleter uniquement sur ce qui vient de se passer dans cette session.

---

## Etape 1 -- Extraction brute

Analyser la conversation courante et remplir quatre listes.

> Ne rien inventer pour remplir une liste vide. Si une categorie est vide, l'indiquer honnetement.

### 1a -- Decisions
Choix explicites ou implicites pris pendant la session :
- Decisions techniques (architecture, stack, pattern choisi)
- Decisions de direction (priorisation, abandon, pivot)
- Decisions de configuration (settings, structure de fichiers)

### 1b -- Faits
Informations nouvelles apprises ou confirmees :
- Features Claude Code / outils (comportement observe, limitation decouverte)
- Patterns qui fonctionnent ou ne fonctionnent pas
- Resultats d'experimentations

### 1c -- Preferences
Signaux sur la facon dont l'utilisateur aime travailler :
- Validations sans contestation d'un choix non-evident -> preference confirmee
- Corrections apportees -> preference identifiee
- Tonalite, niveau de detail, format de reponse demande

### 1d -- Erreurs
Erreurs commises pendant la session (par Claude ou par l'utilisateur) :
- Mauvaise approche initiale corrigee
- Pattern a eviter
- Gotcha decouvert

### Garde anti-hallucination

Si la session etait courte (< 10 echanges substantifs) ou purement exploratoire (recherche, lecture sans decision) :
- Il est NORMAL que certaines listes soient vides
- Ne rien inventer pour les remplir
- "Rien a memoriser cette session" est une reponse valide -- ne pas forcer

### Filtre OBLIGATOIRE (avant d'aller plus loin)

Eliminer de chaque liste :
- Patterns de code, conventions de style -> dans les fichiers, pas en memoire
- Historique git, qui a change quoi -> `git log` est la source
- Recettes de fix de bugs -> le fix est dans le code, pas en memoire
- Tout ce qui est deja documente dans CLAUDE.md
- Details ephemeres de la session courante sans valeur future

Chaque item qui passe le filtre devient **candidat a un bloc de proposition** genere a l'etape 3.

---

## Etape 2 -- Verification de coherence

### 2a -- Verifier la memoire existante

Pour chaque item non-filtre, verifier si un feedback memoire couvre deja ce point.

Scoper au projet courant uniquement -- le wildcard `*/` lirait les feedbacks de TOUS les projets :
```bash
# Deriver le project-id du dossier courant
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
# Le project-id encode remplace / et espaces par -
PROJECT_ID=$(echo "$PROJECT_ROOT" | sed 's|[/:\\]|-|g; s| |-|g; s|^-||')
ls ~/.claude/projects/*${PROJECT_ID}*/memory/feedback_*.md 2>/dev/null | head -20
```

Si un feedback existant couvre deja l'item : **mettre a jour** le fichier existant, ne pas creer de doublon.

### 2b -- Verifier le vault pour les faits et erreurs

Utiliser le MCP forge-brain (auto-start, toujours disponible) :

```
forge-brain:search_brain  query="<mots-cles>"  limit=5
```

Si une note existante couvre l'item : **signaler le conflit** et proposer une mise a jour plutot qu'une creation.

---

## Etape 3 -- Generation des blocs de proposition

Pour chaque item qui a passe le filtre et n'est pas un doublon (verifie a l'etape 2), generer un **bloc pret-a-ecrire** selon son type.

Mapping des items vers les 3 types de blocs : erreur technique → feedback ; bug non fixe → feedback ; preference detectee → feedback ; decision structurante / pivot / trade-off → ADR ; fait technique non documente → note vault.

### Type 1 -- Bloc feedback memoire

```markdown
---
name: <slug-kebab>
description: "<1 ligne specifique>"
metadata:
  type: feedback
---

<fait ou regle>

**Why:** <raison -- incident passe, preference forte, contrainte>
**How to apply:** <quand cette regle s'applique>
```

Chemin cible : `~/.claude/projects/<project-id>/memory/feedback_<slug>.md`
Ligne MEMORY.md a ajouter : `- [Titre lisible](feedback_<slug>.md) -- description (~150 chars)`

### Type 2 -- Bloc note vault

Utiliser la syntaxe Obsidian (wikilinks `[[Note]]`, frontmatter complet, aliases 4-6, tags 2+).

```markdown
---
titre: "<Titre lisible>"
resume: "<1 phrase specifique>"
aliases: ["<alias1>", "<alias2>", "<alias3>", "<alias4>"]
type: erreur | technique | knowledge
derniere-maj: YYYY-MM-DD
auteur: claude
tags: ["#type/<type>", "#domaine/<domaine>"]
---

<body avec wikilinks vers notes liees>
```

Chemin cible selon le contenu : erreur → `vault/claude-forge/Knowledge/erreurs/<slug>.md` ; fait technique → `vault/claude-forge/04-Techniques/<sous-dossier>/<slug>.md` ; synthese → `vault/claude-forge/Knowledge/syntheses/<slug>.md`.

Si une note similaire existe (detectee a l'etape 2b), le bloc propose est un **amendement** : lire la note existante via `read_note`, proposer uniquement le passage a ajouter.

### Type 3 -- Bloc ADR (arbitrage / pivot / decision structurante)

```markdown
## Statut : accepte | <date>

## Contexte
<situation qui a force la decision>

## Options envisagees
<liste des alternatives>

## Decision
<choix retenu>

## Consequences
<impacts previsibles>

## Declencheur de reactivation
<conditions qui justifieraient de revoir cette decision>
```

Chemin cible : `vault/claude-forge/Knowledge/decisions/decision-<slug>.md` (ou `Knowledge/raisonnements/` si c'est un raisonnement multi-etapes plutot qu'une decision tranchee).

---

## Etape 4 -- Boucle de validation item par item

Presenter chaque bloc **un par un**. Ne rien ecrire avant validation explicite.

Pour chaque bloc :

```
Type : [feedback / note vault / ADR]
Chemin cible : [chemin complet]
---
[contenu du bloc]
---
[v]alider tel quel  [m]odifier puis valider  [i]gnorer
```

- `v` --> ecrire immediatement, passer au suivant
- `m` --> attendre la version modifiee par l'utilisateur, puis ecrire, passer au suivant
- `i` --> ne rien ecrire, passer au suivant

**Ecriture memoire** (apres `v` ou `m`) :
- `Write` le fichier `feedback_<slug>.md` (jamais obsidian create)
- Lire MEMORY.md, verifier absence de doublon, puis ajouter la ligne index en section appropriee

**Ecriture vault** (apres `v` ou `m`) :
- `Write` la note vault (jamais CLI Obsidian -- colons YAML cassent le parser)
- `forge-brain:update_property  file="<nom-note>"  name="derniere-maj"  value="YYYY-MM-DD"`
- Lier au MOC correspondant si note creee

---

## Etape 5 -- Rapport final

Afficher un resume structure :

```
## Session Done -- [date du jour]

### Blocs proposes : N
- Valides : N  |  Modifies : N  |  Ignores : N

### Memoire
- Crees : [liste fichiers]
- Mis a jour : [liste fichiers]
- Ignores (doublons ou [i]) : [N items]

### Vault
- Crees : [liste notes]
- Mis a jour : [liste notes]
- Rien a creer (info ephemere ou deja couverte) : [si applicable]

### Conflits detectes
- [conflit] : [description + action prise/proposee]
```

Terminer par une **ligne de suggestion** : ce que la prochaine session pourrait commencer a faire.

---

## Etape 6 -- Mise a jour Context Note

Reecrire `vault/claude-forge/0-Inbox/context-actuel.md` avec l'etat actuel :

```markdown
---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: YYYY-MM-DD
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
[resume en 1 phrase de ce sur quoi on travaille]

## Derniere session (YYYY-MM-DD)
### Decisions prises
[lister les decisions de cette session]
### En cours
[ce qui est en cours de realisation]
### Prochaines etapes
[suggestions pour la prochaine session]

## Fils ouverts
[sujets mentionnes mais pas traites, a reprendre plus tard]

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
```

Cette note est la **working memory** -- ce que Jarvis doit savoir au reveil. `/recap` la lit en debut de session.

---

## Gotchas

- **Aucun fichier transcript** -- la conversation est dans le contexte courant. Ne pas chercher de `conversation.txt` ou equivalent.
- **Filtre OBLIGATOIRE** -- code patterns, git history, fix recipes sont hors scope memoire. Les inclure pollue le signal.
- **Ne rien inventer** -- si la session etait courte, il peut n'y avoir aucun item. "Rien a memoriser cette session" est une reponse valide.
- **Chemins memoire non hardcodes** -- utiliser `git rev-parse --show-toplevel` pour deduire le project-id, jamais un chemin Windows en dur.
- **`Write` pour les notes vault, jamais `obsidian create`** -- les deux-points dans le frontmatter YAML cassent le parser CLI (exit 127).
- **MEMORY.md < 200 lignes** -- si l'index approche la limite, mentionner dans le rapport.
- **Conflit = proposition, pas action unilaterale** -- si un item contredit une note existante, proposer la mise a jour plutot qu'ecraser.
- **Separation memoire/vault** -- memoire = feedback specifique relation utilisateur. Vault = savoir reutilisable par n'importe qui.
- **MCP forge-brain auto-start** -- le MCP est lance par hook SessionStart. Utiliser les outils MCP (search_brain, read_note, create_note...) pour tout acces vault. Jamais de CLI.
- **Auto-trigger inexistant** -- cette skill ne s'auto-declenche pas en fin de session. Un Stop hook separe serait necessaire (hors scope).
- **`/done` != `/recap`** -- `/recap` = snapshot etat du projet en DEBUT de session (git, vault, memoire). `/done` = metacognition en FIN de session (extraction et capitalisation de ce qui s'est passe). Les deux sont complementaires, pas redondants.
- **Deduplication avant ecriture** -- toujours lire MEMORY.md et les feedbacks existants avant de creer un nouveau fichier memoire.
- **Sur-generalisation** -- 1 seule occurrence = feedback ponctuel. Ne jamais formuler une regle a partir d'un seul evenement.
- **Doublon detecte = amendement, pas creation** -- si search_brain retourne une note similaire, lire la note via `read_note`, proposer un ajout, pas un nouveau fichier.
- **"Rien a proposer" est valide** -- si la session n'a rien produit de capitalisable, le dire honnetement. Ne pas forcer des blocs.
- **Jamais d'ecriture sans validation explicite** -- la gate [v]/[m]/[i] est obligatoire pour chaque bloc. L'humain est dans la boucle.

---

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

Apres avoir utilise `/done`, noter en memoire si :
- Un type d'item revient systematiquement (signifie que ce type merite une section dediee dans le rapport)
- Le filtre elimine trop ou trop peu (calibrer les criteres)
- Les conflits vault sont frequents sur un theme precis (note vault sous-maintenue)

Sauvegarder ces observations dans `project_done_patterns.md` si un pattern emerge sur plusieurs sessions.
