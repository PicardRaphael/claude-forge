---
name: backlog-triage
description: Triage a raw demand (mail, text, ticket) into a structured spec and Jira N2 ticket. Use when the user pastes a client request, a mail, or any feature demand to process. Deduplicates against existing Jira tickets, enriches with vault context, proposes a spec, and creates the N2 ticket on validation.
---

# Backlog Triage — Intelligence Hub Neoteem

Transforme une demande en specification structuree et ticket Jira N2. Accepte 3 modes d'entree.

## Modes d'entree

| Mode | Declencheur | Exemple |
|------|------------|---------|
| **Texte colle** | L'utilisateur colle un mail, un message client, un texte libre | "Voici un mail de Mme Dupont : ..." |
| **Ticket unique** | L'utilisateur reference un ticket par son ID | "Analyse le ticket AML-4521" |
| **Lot de tickets** | L'utilisateur demande d'analyser un projet, un filtre, ou un ensemble | "Trie tous les tickets AML ouverts", "Analyse les N2 sans spec" |

### Mode texte colle
Passer directement a l'etape 1 avec le texte brut.

### Mode ticket unique
Lire le ticket dans Jira (titre, description, commentaires, pieces jointes textuelles), puis traiter comme un texte brut a l'etape 1.

### Mode lot de tickets
1. Chercher les tickets correspondants dans Jira (JQL)
2. Lister les resultats avec un resume : ID, titre, statut, date
3. Demander a l'utilisateur : "J'ai trouve X tickets. Tu veux que je les trie tous ou tu veux en selectionner ?"
4. Pour chaque ticket selectionne, executer le workflow complet (etapes 1-5)
5. A la fin, proposer un resume croise : doublons detectes, regroupements suggeres, specs a creer

## Workflow (par demande)

```
Entree (texte / ticket / lot)
    |
    v
1. COMPRENDRE — Reformuler la demande en langage clair
    |
    v
2. CONTEXTUALISER — Chercher dans le vault si le sujet est deja
   documente. Question metier → skill neoteem-brain-support.
   Question technique → skill neoteem-brain-dev.
    |
    v
3. DEDOUBLONNER — Chercher dans Jira N2 et AML si un ticket
   similaire existe deja
    |
    v
4. CLASSIFIER — Rattacher a un regroupement fonctionnel existant
   ou en suggerer un nouveau
    |
    v
5. PROPOSER — Generer une specification structuree
    |
    v
6. VALIDER — L'utilisateur valide, ajuste ou rejette
    |
    v
7. CREER — Ticket N2 dans Jira avec la spec validee
```

## Etape 1 — Comprendre

Reformuler la demande brute en une description claire :
- Supprimer le bruit (formules de politesse, contexte inutile)
- Identifier le besoin fonctionnel concret
- Extraire : qui demande, quel module concerne, quelle action attendue

Si la demande est floue, ambigue, ou manque d'info critique, poser des questions AVANT de continuer :
- "C'est pour quel module ? Syndic, gerance, compta ?"
- "Le client veut modifier le comportement existant ou ajouter quelque chose de nouveau ?"
- "Ca concerne un cas precis ou c'est une demande generale ?"

Ne jamais deviner quand on peut demander. Un ticket bien cadre vaut mieux qu'une spec a cote.

Presenter la reformulation a l'utilisateur : "Voici ce que je comprends : [reformulation]. C'est bien ca ?"

## Etape 2 — Contextualiser via le vault

Chercher le contexte dans le vault en choisissant la bonne skill selon la nature de la demande :

| Nature de la demande | Skill a utiliser |
|---------------------|-----------------|
| Fonctionnelle (processus, regles metier, utilisateur) | **neoteem-brain-support** (langage metier) |
| Technique (BDD, fonctions PG, endpoints, architecture) | **neoteem-brain-dev** (detail technique) |
| Mixte ou pas clair | Commencer par **support**, basculer vers **dev** si besoin de precision technique |

```
Chercher dans le vault : [sujet de la demande]
- Existe-t-il des regles metier liees ?
- Des tables/fonctions PG concernees ? (si technique)
- Des decisions passees sur ce sujet ?
```

Presenter le contexte trouve : "Le vault indique que [contexte]. Ca impacte la demande parce que [lien]."

Si le vault ne contient rien sur le sujet, le dire.

## Etape 3 — Dedoublonner dans Jira

Chercher dans les projets Jira N2 et AML :

```
Rechercher les tickets existants qui traitent du meme sujet :
- Projet N2 : tickets ouverts avec des mots-cles similaires
- Projet AML : tickets clients qui remontent le meme besoin
```

| Resultat | Action |
|----------|--------|
| Ticket identique existe | Signaler le doublon, proposer de completer le ticket existant |
| Ticket similaire existe | Signaler la proximite, demander si c'est le meme besoin ou un besoin distinct |
| Rien trouve | Continuer vers la spec |

## Etape 4 — Classifier

Rattacher la demande a un regroupement fonctionnel :

```
Regroupements = epics ou categories existantes dans Jira N2.
Chercher l'epic la plus proche du sujet de la demande.
```

| Resultat | Action |
|----------|--------|
| Epic existante correspond | Rattacher et indiquer laquelle |
| Aucune epic ne correspond | Suggerer un nouveau regroupement, soumis a validation |

## Etape 5 — Proposer la specification

Generer une spec structuree :

```
## Specification : [Titre court]

**Origine :** [source — mail de X, ticket AML-xxx, texte libre]
**Module :** [syndic / gerance / comptabilite / technique / transverse]
**Regroupement :** [epic existante ou suggestion]

### Besoin
[Description fonctionnelle claire, 3-5 lignes]

### Comportement attendu
[Ce que l'utilisateur doit pouvoir faire, etape par etape]

### Cas limites
- [Cas 1]
- [Cas 2]

### Criteres d'acceptance
- [ ] [Critere 1]
- [ ] [Critere 2]

### Description publique (version client)
[Version simplifiee, anonymisee, sans jargon interne — pour la vue client]

### Contexte vault
[Resume du contexte trouve dans neoteem-brain, si pertinent]
```

Presenter la spec et attendre la validation : "Voici la spec proposee. Tu valides, tu ajustes, ou tu rejettes ?"

## Etape 6 — Validation

3 options :
- **Valide** → passer a la creation du ticket
- **Ajuste** → modifier la spec selon les retours, reproposer
- **Rejette** → archiver avec le motif

## Etape 7 — Creer le ticket N2

Sur validation, creer le ticket dans Jira projet N2 :

| Champ Jira | Contenu |
|-----------|---------|
| Projet | N2 |
| Type | Story (ou type valide par l'utilisateur) |
| Titre | Titre de la spec |
| Description | Spec complete (besoin + comportement + criteres) |
| Epic | Regroupement identifie a l'etape 4 |
| Labels | `backlog-hub`, `ia-triage` |

Confirmer la creation : "Ticket [N2-XXXXX] cree. [lien]"

## Raccourcis

L'utilisateur peut declencher des etapes specifiques :

| Commande | Action |
|----------|--------|
| "trie cette demande" / coller un texte | Workflow complet (etapes 1-7) |
| "analyse le ticket AML-1234" | Lire le ticket Jira puis workflow complet |
| "trie tous les tickets AML ouverts" | Mode lot : lister, selectionner, trier chacun |
| "analyse les N2 sans spec cette semaine" | Mode lot avec filtre JQL |
| "est-ce qu'on a deja un ticket sur X ?" | Etapes 2-3 seulement (contexte + dedup) |
| "fais une spec pour X" | Etapes 1-5 seulement (sans creation Jira) |
| "cree le ticket" | Etape 7 seulement (si spec deja validee dans la conversation) |

## Gotchas

- Toujours attendre la validation avant de creer le ticket Jira — jamais de creation automatique
- Le projet AML est en lecture seule — on cherche dedans mais on ne cree jamais de ticket AML
- Si plusieurs demandes sont collees d'un coup, les traiter une par une
- Le contexte vault enrichit la spec mais ne la remplace pas — la spec reste fonctionnelle, pas technique
- Adapter le langage au niveau de l'utilisateur (dirigeant = metier, dev = technique)

## Apprentissage

Noter ici les patterns recurrents :
- Types de demandes les plus frequentes
- Regroupements souvent suggeres
- Formulations de spec qui passent bien vs celles qui sont toujours ajustees
