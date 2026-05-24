---
name: done
description: End-of-session metacognition -- extracts decisions, facts, preferences, and errors from the current conversation, updates vault and memory automatically. Use when the user types /done or at session end.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__create_note, mcp__forge-brain__append_note, mcp__forge-brain__update_property
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

## Etape 3 -- Mise a jour memoire

### 3a -- Localiser le dossier memoire

```bash
git rev-parse --show-toplevel 2>/dev/null
```

Le dossier memoire est a :
`~/.claude/projects/<project-id-encode>/memory/`

Ou `<project-id-encode>` = chemin du projet avec `/` et espaces replaces par `-`
(ex : `C--Users-raphael-picard-neote-Documents-claude-forge`).

Si le chemin n'est pas accessible : noter "memoire non accessible" et continuer avec le vault.

### 3b -- Creer ou mettre a jour les fichiers memoire

Pour chaque item retenu :

**Feedback** (preferences, erreurs a eviter) -> `feedback_<sujet>.md`
**Projet** (decisions, contexte en cours) -> `project_<sujet>.md`
**Reference** (faits techniques reutilisables) -> `reference_<sujet>.md`

Format obligatoire :
```markdown
---
name: <nom court>
description: <une ligne -- ce que ce fichier contient>
type: feedback | project | reference
---

<contenu>

**Why:** <raison -- incident passe, preference forte, contrainte>
**How to apply:** <quand cette regle s'applique>
```

Regle dedoublonnage : avant de creer un nouveau fichier, verifier qu'aucun fichier existant ne couvre deja ce sujet.

### 3c -- Mettre a jour MEMORY.md

Si un nouveau fichier a ete cree, ajouter **une seule ligne** dans la section appropriee de MEMORY.md :
```
- [nom-lisible](nom-fichier.md) -- description courte en une ligne (~150 chars max)
```

Lire MEMORY.md avant de modifier pour verifier qu'aucun doublon n'existe.

---

## Etape 4 -- Mise a jour vault (si applicable)

Vault a mettre a jour seulement si les faits ou erreurs sont **reutilisables au-dela de cette session** et **non couverts par une note existante**.

### Seuil pour creer une note vault

Creer une note vault si :
- Une erreur est susceptible de se reproduire dans d'autres projets
- Un fait technique est une decouverte non-documentee (feature, limitation, pattern)
- Une exploration a produit un resultat non-evident

Ne pas creer de note vault si :
- L'info est specifique a une decision ponctuelle
- Elle sera obsolete en < 7 jours
- Elle est deja dans MEMORY.md

### Creer une note vault

Lire le template approprie avant de creer :
```bash
cat vault/claude-forge/Templates/knowledge.md 2>/dev/null
```

Chemin selon le type :
- Erreur -> `vault/claude-forge/Knowledge/erreurs/<slug>.md`
- Fait technique -> `vault/claude-forge/04-Techniques/<sous-dossier>/<slug>.md`
- Synthese -> `vault/claude-forge/Knowledge/syntheses/<slug>.md`
- Contexte projet (decision, etat) -> `vault/claude-forge/1-Projets/<nom-projet>/<slug>.md` (template `context-projet`)
- Contexte casquette (preference vie) -> `vault/claude-forge/2-Casquettes/<slug>.md` (template `context-casquette`)
- Capture rapide (a trier) -> `vault/claude-forge/0-Inbox/<slug>.md`

**Creer avec `Write`** (jamais `obsidian create` -- les colons YAML cassent le parser CLI).

Mettre a jour `derniere-maj` apres creation :
```
forge-brain:update_property  file="<nom-note>"  name="derniere-maj"  value="YYYY-MM-DD"
```

Lier au MOC correspondant si une note vault est creee.

---

## Etape 5 -- Rapport final

Afficher un resume structure :

```
## Session Done -- [date du jour]

### Decisions (N)
- [decision] --> memorisee dans [feedback_xxx.md] / non memorisee (specifique)

### Faits appris (N)
- [fait] --> vault [note] / memoire [reference_xxx.md] / deja documente

### Preferences detectees (N)
- [preference] --> [feedback_xxx.md] mis a jour / cree

### Erreurs (N)
- [erreur] --> [feedback_xxx.md] + vault [Knowledge/erreurs/xxx.md]

### Memoire
- Crees : [liste fichiers]
- Mis a jour : [liste fichiers]
- Ignores (doublons) : [N items]

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

---

## Apprentissage

Apres avoir utilise `/done`, noter en memoire si :
- Un type d'item revient systematiquement (signifie que ce type merite une section dediee dans le rapport)
- Le filtre elimine trop ou trop peu (calibrer les criteres)
- Les conflits vault sont frequents sur un theme precis (note vault sous-maintenue)

Sauvegarder ces observations dans `project_done_patterns.md` si un pattern emerge sur plusieurs sessions.
