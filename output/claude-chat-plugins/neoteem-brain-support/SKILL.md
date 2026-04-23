---
name: neo-brain-support
description: Search the neoteem-brain vault and answer in non-technical language for support teams. Reformulates technical content without tables, IDs, SQL, or PG functions. Works via Bash CLI or MCP obsidian-brain.
---

# neo-brain-support

Skill de consultation du vault neoteem-brain avec **reformulation non-technique** pour les equipes support.

## Acces au vault — Detection automatique

Cette skill detecte automatiquement le meilleur mode d'acces au vault :

### Mode 1 : Bash CLI (prioritaire — Claude Code)

Si l'outil `Bash` est disponible, utiliser la CLI Obsidian directement via le wrapper :

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-cli.sh vault="neoteem-brain" [commande]
```

| Commande CLI | Usage |
|-------------|-------|
| `search:context query="..." limit=N` | Recherche avec snippets |
| `search query="..." limit=N` | Recherche simple |
| `read file="nom-note"` | Lire une note (resolution wikilink) |
| `read path="chemin/exact.md"` | Lire par chemin exact |
| `backlinks file="nom-note" counts` | Notes qui pointent vers celle-ci |
| `tags sort=count counts` | Tous les tags du vault |
| `create path="..." content="..." silent` | Creer une note |
| `append file="..." content="..."` | Ajouter a une note |
| `property:set name="..." value="..." file="..."` | Modifier une propriete |

Les exemples ci-dessous utilisent `obsidian` par concision, mais **remplacer par le wrapper dans chaque appel Bash**.

Voir `references/obsidian-cli-commands.md` pour la reference complete.

### Mode 2 : MCP obsidian-brain (fallback — Claude Chat / Cowork)

Si Bash n'est pas disponible (Claude Chat, Cowork), utiliser les tools MCP :

| Tool MCP | Equivalent CLI |
|----------|---------------|
| `search_brain(query, limit, context)` | `search:context` / `search` |
| `read_note(file)` | `read file=` |
| `read_note_by_path(path)` | `read path=` |
| `get_backlinks(file)` | `backlinks file= counts` |
| `get_tags()` | `tags sort=count counts` |

**Ecriture non disponible en MCP** — signaler a l'equipe technique si une note doit etre creee/corrigee.

### Comment detecter le mode

1. Essayer un appel Bash : `bash ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-cli.sh vault="neoteem-brain" search query="test" limit=1`
2. Si ca marche → **Mode CLI** pour toute la session (lecture + ecriture)
3. Si ca echoue ou si Bash n'est pas disponible → **Mode MCP** (lecture seule)

## Strategie de recherche et auto-enrichissement

### Classifier la question AVANT de chercher

| Signal dans la question | Type | Strategie |
|------------------------|------|-----------|
| "Comment faire X ?", "Pourquoi Y ?" | **Simple** | Flux standard (1 search + 1-2 reads) |
| "Tous les X", "liste complete", "recap de chaque", "exhaustif" | **Exhaustive** | Flux exhaustif (voir ci-dessous) |

**Choisir le bon flux AVANT la premiere recherche.** Ne pas decouvrir apres 8 searches que la question etait exhaustive.

### Flux standard (question simple)

```
Question support
    ↓
1. Chercher dans 07-Support/ (notes deja reformulees pour le support)
    ↓
  Trouvee? → Repondre directement
    ↓ non
2. Knowledge/ (reponses deja traitees, focalisees)
    ↓
  Trouvee? → Reformuler + repondre + auto-creer note 07-Support/ (CLI) ou signaler (MCP)
    ↓ non
3. Vault structure (01-Domaines/, 02-BDD/, 03-Apps/, 06-Regles/)
    ↓
  Trouvee? → Reformuler + repondre + auto-creer note 07-Support/ (CLI) ou signaler (MCP)
    ↓ non
4. Escalade → Repondre "investigation necessaire, transmettre a l'equipe technique"
```

**Knowledge/ avant le vault structure** — les reponses y sont deja synthetisees, ca economise des tokens.

> **Budget standard** : 1 search + 1-2 reads. Pas 10.

### Flux exhaustif (question "tous les X")

Les questions "liste-moi tous les X" ne se resolvent pas par des recherches vault successives. Le vault n'a pas forcement une note unique avec la liste complete. Il faut aller a la source de verite.

```
Question exhaustive ("tous les roles", "chaque type de X")
    ↓
1. 1 search dans 07-Support/ ou Knowledge/ → FAQ/synthese existante?
    ↓ trouvee → Repondre
    ↓ non
2. Identifier la SOURCE DE VERITE (pas le vault, la source primaire) :
   - Donnees BDD → notes 02-BDD/ (tables, constantes, enums)
   - Regles metier → notes 01-Domaines/
   - Config/parametrage → notes 03-Apps/
    ↓
3. Lire la/les MOC pour trouver les notes sources exactes :
   obsidian vault="neoteem-brain" read file="MOC-BDD"
    ↓
4. Lire les 2-4 notes sources identifiees (pas de search supplementaire)
    ↓
5. Synthetiser → Repondre → Creer FAQ dans 07-Support/ pour la prochaine fois
```

> **Budget exhaustif** : 1 search + 1 MOC + 2-4 reads sources. Max 6 appels total.
>
> **Anti-pattern** : enchaîner des `search:context` avec des variantes de mots-cles ("role tiers", "type acteur", "acteur role bail"...) en esperant tomber sur la bonne note. Si le 1er search ne donne pas de FAQ prete, passer directement a l'etape 2 (MOC → notes sources).

### Hints de recherche — termes techniques vault

Le vault est indexe par noms techniques. Les recherches en langage naturel generent du bruit. Privilegier les termes vault :

| Le support demande... | Chercher avec... |
|----------------------|-----------------|
| Roles / types de tiers | `t_acteur role type_role` ou MOC-BDD |
| Charges / appels de fonds | `charges copropriete appel-fonds` |
| Baux / locataires | `t_bail locataire statut` |
| Comptabilite | `ecriture compta rapprochement` |
| Documents / courriers | `correspondance document drive` |
| Extranet / portail | `extranet portail acces` |

Quand le 1er search ne renvoie que du bruit, **ne pas re-chercher avec d'autres mots**. Lire le MOC du domaine concerne a la place.

### 1. Chercher (search)

```bash
# Mode CLI
obsidian vault="neoteem-brain" search:context query="charges copropriete" limit=5
```
```
# Mode MCP
search_brain(query="charges copropriete", limit=5, context=true)
```

Si des notes avec `public: support` apparaissent → les utiliser en priorite.

### 2. Lire si besoin (read)

```bash
# Mode CLI
obsidian vault="neoteem-brain" read file="faq-charges-copro"
```
```
# Mode MCP
read_note(file="faq-charges-copro")
```

Seulement si le snippet ne suffit pas. Lire les 1-3 notes les plus pertinentes, pas plus.

### 3. Suivre les connexions si incomplet

Utiliser backlinks pour trouver les notes liees. Stopper des que la reponse est complete.

### 4. Reformuler AVANT de repondre

Appliquer systematiquement les regles de `references/reformulation-rules.md`.

## Regles de reformulation (resume)

| Interdit | Remplacer par |
|----------|--------------|
| Nom de table (`t_bail`, `t_acteur`) | Terme metier ("le bail", "le contact") |
| Nom de fonction PG (`f_calc_charges`) | Action ("le calcul des charges") |
| Nom de schema (`schema_compta`) | Module ("module comptabilite") |
| Colonne/champ (`bail.statut`, `psbyid`) | Etat ou valeur ("statut du bail", "identifiant") |
| SQL / requete | Description du resultat |
| ID technique / UUID | Jamais mentionne |
| Architecture (API, endpoint, service) | Navigation ecran ("Menu > Onglet > Bouton") |

Voir `references/reformulation-rules.md` pour les regles detaillees.

## Format de reponse

### Question simple (FAQ)

```
**Reponse** : [1-2 phrases simples]

**Pour le faire** :
1. Aller dans [Menu > Onglet]
2. [Action]
3. [Verification]
```

### Probleme / incident

```
**Cause probable** : [explication simple]

**Solution** :
1. Verifier que [condition]
2. [Action corrective]
3. Si ca ne marche pas : [escalade]

**Bon a savoir** : [contexte utile]
```

### Question complexe (necessite investigation)

```
**Ce qu'on sait** : [resume]

**Ce qu'il faut verifier** :
- [Point 1 — qui peut verifier]
- [Point 2]

**Escalade** : [a qui transmettre si besoin]
```

## Exemples

### Mauvaise reponse (mode technique)

> Le locataire n'est pas affiche car `t_bail.statut = 'RESILIE'` dans la table `t_bail` (schema `gerance`). La fonction `f_get_locataires_actifs` filtre sur `statut IN ('ACTIF', 'PREAVIS')`. Verifier via `SELECT * FROM gerance.t_bail WHERE psbyid = '...'`.

### Bonne reponse (mode support)

> **Cause probable** : Le bail du locataire est resilie dans le systeme.
>
> **Solution** :
> 1. Aller dans **Gerance > Baux**
> 2. Rechercher le locataire par nom
> 3. Verifier la colonne "Statut" — si elle indique "Resilie", le locataire n'apparait plus dans les listes actives
> 4. Si le bail devrait etre actif, contacter l'equipe de gestion pour corriger le statut
>
> **Bon a savoir** : Seuls les baux "Actif" et "En preavis" apparaissent dans les ecrans courants.

## Auto-creation de notes support (Mode CLI uniquement)

En mode CLI, apres avoir repondu a partir du vault technique, **creer la note support** :

### Verification prealable OBLIGATOIRE

```bash
obsidian vault="neoteem-brain" search:context query="{sujet}" limit=5
```

| Resultat | Action |
|---|---|
| FAQ existante couvre le sujet | Ne rien creer. Repondre depuis la FAQ |
| FAQ existante mais incomplete | `append` sur la note existante |
| Aucune FAQ | Creer la note support |

### Ou creer

| Type de question | Dossier | Prefix |
|-----------------|---------|--------|
| "Comment faire X ?" | `07-Support/faq/` | `faq-` |
| "Comment realiser X etape par etape ?" | `07-Support/procedures/` | `proc-` |
| "X ne marche pas" | `07-Support/problemes-connus/` | `pb-` |

### Comment creer

```bash
obsidian vault="neoteem-brain" create path="07-Support/faq/faq-{sujet}.md" content="---
titre: \"Question — {question reformulee}\"
resume: \"{reponse courte en 1 ligne}\"
aliases:
  - \"{formulations alternatives}\"
domaine: {syndic|gerance|compta|transversal}
public: support
derniere-maj: {YYYY-MM-DD}
auteur: claude
sources:
  - \"[[{note-technique-source}]]\"
tags:
  - \"#type/support-faq\"
  - \"#domaine/{xxx}\"
---

## Reponse courte

{reponse reformulee sans jargon}

## Etapes

1. {navigation ecran + action}

## Points de vigilance

- {cas particuliers}

## Voir aussi

- [[{notes-liees}]]
" silent
```

## Sauvegarder une information (demande utilisateur)

1. **Comprendre** ce qu'il veut sauvegarder — reformuler pour confirmer
2. **Chercher** si une note support existe deja
3. **Mode CLI** → creer ou append directement dans `07-Support/`
4. **Mode MCP** → "Cette info est notee. Je transmets a l'equipe technique pour ajout au vault."

**Ne JAMAIS refuser de sauvegarder.**

## Corriger une note (info obsolete ou fausse)

1. Chercher la note support
2. **Mode CLI** → corriger avec `append` + `property:set derniere-maj`
3. **Mode MCP** → "Je note que cette info est obsolete. Transmis pour correction."

## Gotchas

- Obsidian doit etre ouvert — CLI et MCP en dependent
- `file=` / `read_note(file=)` resout comme un wikilink (nom seul), `path=` est le chemin exact
- Ne jamais modifier les notes dans `01-Domaines/`, `02-BDD/`, `03-Apps/` — lecture seule
- Ne jamais exposer les noms techniques dans les reponses — toujours reformuler
- Mode MCP = lecture seule, signaler les ecritures necessaires

## Apprentissage

A chaque session :
- Verifier que chaque reponse technique a genere sa note support (mode CLI)
- Reformulations qui fonctionnent bien → enrichir le glossaire support
- Termes metier mal compris → ajouter au [[glossaire-support]]
- Si un sujet genere plusieurs FAQ proches → envisager une procedure unifiee
