---
name: audit-departement
description: ALWAYS invoke when the user wants to interview a company department (Migration, Support, Commercial, RH, PO, Ops) to discover its processes and spot AI-automation candidates. Triggers "audit le département X", "interview le service Y", "/audit-departement Migration". Pilots a live discovery interview one question at a time. NOT for auditing your own daily workflow (cartographier-process-cma), NOT for turning a finished sheet into recommendations (reco-automatisation).
user-invocable: true
allowed-tools: Read, mcp__forge-brain__*, TaskCreate, TaskUpdate, TaskList
model: sonnet
effort: high
argument-hint: "<NomDuDépartement>"
---

# audit-departement — copilote d'entretien de découverte

Pilote en direct un entretien de découverte avec un département (`$ARGUMENTS`, ex : Migration) pour découvrir ses process et repérer les candidats à l'automatisation IA. **Toi (Raphael) mènes l'entretien face à l'interlocuteur ; cette skill te souffle quoi demander, une question à la fois, et décide de la suite selon les réponses que tu colles.** Sortie : une fiche process en markdown par process découvert.

C'est la PHASE 1 (interview). La PHASE 2 (analyse → reco) est la skill `reco-automatisation`, qui prend la fiche de sortie en entrée.

Méthode canonique (le socle — à NE PAS recopier ici) : `mcp__forge-brain__read_note(file="auditer-departements-pour-automatisation")`. La lire si un point de méthode est incertain.

## Comment ça marche — le mode pilote

Le principe : **la skill donne UNE question à la fois**, formulée prête à dire ("Pose ça : « ... »"), tu la poses à l'interlocuteur, tu **colles sa réponse** dans la conversation, et la skill décide :
- **creuser** (la réponse contient un fil à tirer ou un signal d'automatisation), ou
- **passer** à la question/phase suivante, ou
- **noter** un process candidat et continuer.

Tu suis, la skill mène. Jamais de questionnaire entier balancé d'un coup — une question, une réponse, une décision.

## Étapes

### 1. Initialiser

- Le département cible = `$ARGUMENTS`. Si absent, demander lequel.
- Lire `mcp__forge-brain__read_note(file="auditer-departements-pour-automatisation")` une fois pour avoir la méthode fraîche (questions story-based, signaux, format de fiche).
- Créer les tâches de pilotage (1 par phase d'entretien) avec `TaskCreate` :
  1. Ouverture & cadrage anti-politique
  2. Cartographie du quotidien (quels process)
  3. Récit chronologique du process le plus chronophage
  4. Creusage & signaux d'automatisation
  5. Soft close (baguette magique)
  6. Fiche(s) process de sortie
- `TaskUpdate` chaque phase en `in_progress` à son début, `completed` AVANT de passer à la suivante. Ne jamais sauter une phase.

### 2. Phase ouverture & cadrage (Task 1)

Souffler à Raphael, dans l'ordre, une question à la fois :
- Mise à l'aise : *« Raconte-moi ton rôle, une journée type chez toi. »*
- **Cadrage anti-politique** (le dire tel quel) : *« Je ne viens pas évaluer ton travail. Je veux comprendre comment ça se passe vraiment, pour voir ce qu'on pourrait t'enlever des mains. Rien ne te sera attribué. »*
- Ne PAS révéler l'intention précise (« on cherche à automatiser X ») — sinon l'interlocuteur oriente ses réponses. Rester large.

### 3. Phase cartographie (Task 2)

- *« Qu'est-ce qui occupe le plus ton temps en ce moment ? »*
- *« Quel process te fait perdre le plus de temps ? »*
- Lister mentalement les process cités. Choisir avec Raphael le plus chronophage/contraignant pour le récit détaillé (les autres seront notés pour des entretiens futurs).

### 4. Phase récit chronologique (Task 3)

Faire raconter du **vécu passé**, jamais des opinions. Transposer la formulation au département (`$ARGUMENTS`) :
- *« Raconte-moi la dernière fois que tu as [fait ce process — ex pour Migration : migré un client / repris des données d'un ancien outil]. Pars du tout début. »*
- Suivre l'ordre chronologique (découvrir → faire → vérifier → transmettre), pas par thème.
- Ancrer : *« C'était quel jour ? Tu utilisais quel outil ? Qui d'autre était impliqué ? »*

### 5. Phase creusage & signaux (Task 4)

Quand une réponse contient un fil, souffler un probe de creusage :
- Silence (rappeler à Raphael : *laisse 3-5 s de blanc avant de relancer*).
- *« Raconte-moi en plus. » / « Concrètement, ça donne quoi ? »*
- 5 Whys quand un symptôme cache une cause (*« ça prend trop de temps »* → pourquoi ? → pourquoi ?).
- Clarifier le vague : *« Tu dis 'compliqué' — qu'est-ce qui le rend compliqué ? »*

**Signaux d'automatisation à écouter** (quand l'un apparaît, le signaler à Raphael : « 🔎 signal — creuse ça ») :
| Signal | Question de creusage à souffler |
|---|---|
| Répétitivité + volume | *« Tu fais ça combien de fois par semaine ? Vous êtes combien dessus ? »* |
| Règles explicites vs jugement tacite (LE discriminant) | *« Comment tu décides quoi faire ? C'est une règle claire, ou ça dépend de ton expérience ? »* |
| Données structurées vs non | *« Les infos d'entrée, c'est dans un tableur / un formulaire, ou c'est des mails / des conversations ? »* |
| Savoir explicitable vs implicite | *« Si tu devais l'expliquer à un nouveau, ça tient dans une procédure, ou il faut du flair ? »* |
| Temps perdu / ressaisie | *« Tu recopies des infos d'un outil à un autre ? »* |

### 6. Phase soft close (Task 5)

- *« Si tu avais une baguette magique, qu'est-ce que tu changerais dans ce process ? »*
- Garder l'attention active : les meilleures infos sortent quand la garde tombe.

### 7. Fiche process de sortie (Task 6)

Pour chaque process traité, produire en **markdown propre dans la conversation** (Raphael colle où il veut — pas d'écriture automatique) :

```markdown
## Fiche process — [département] · [nom du process]

- **Qui / contexte** : [rôle, équipe]
- **Citation marquante** : « ... »
- **Étapes (carte d'expérience)** : 1. ... 2. ... 3. ...
- **Opportunités (douleurs actionnables)** : [ce qui fait mal, racontable]
- **Insights (notable, pas encore actionnable)** : [observations]
- **Fréquence / volume** : [quotidien/hebdo, nb de personnes]
- **Règles explicites ou jugement tacite** : [le discriminant]
- **Données** : [structurées (tableur/formulaire) / non structurées (mail/conv)]
- **Savoir** : [explicitable / implicite]
- **Candidat automatisation** : [oui/non + IA vs règles déterministes]
- **Niveau de solution pressenti** : [chatbot assisté / workflow contextualisé / agent autonome]
```

Ce format = Interview Snapshot (Torres) + grille de qualification. Il alimente directement la skill `reco-automatisation`.

## Gotchas

- **Une question à la fois, jamais le questionnaire entier.** Si tu balances tout d'un coup, Raphael perd le mode pilote interactif voulu — il ne peut plus coller une réponse et te laisser décider la suite.
- **Comportement passé > opinions > futur.** Bannir *« est-ce que tu utiliserais... »* et *« c'est important pour toi... »* — faire raconter la dernière fois réelle.
- **Ne pas souffler de question suggestive** : pas *« c'est pénible de ressaisir, non ? »* mais *« raconte-moi cette étape. »*
- **Ne pas sauter à la solution.** Si l'interlocuteur dit « il me faudrait un bouton qui... », souffler *« ça te permettrait de régler quoi ? »* — on cherche les douleurs, pas les specs.
- **Migration / Support / RH / PO ne sont pas couverts par les sources d'origine** (qui parlent Sales/Marketing/Delivery) : transposer les questions story-based au département, ne pas inventer un jargon métier qu'on n'a pas.
- **Déclaratif ≠ comportement** : pour les volumes/fréquences durs, rappeler à Raphael que les chiffres se confirment sur les logs réels, pas juste sur le ressenti de l'interviewé.
- **Sortie = markdown à coller, aucun écrit vault automatique** (décision verrouillée). Ne pas tenter d'écrire la fiche via MCP sans demande explicite.

## Apprentissage

Après un entretien réel mené avec cette skill, noter ici :
- Les questions transposées qui ont bien marché pour un département donné (ex : formulations Migration efficaces) → enrichir la table de questions.
- Un signal d'automatisation récurrent non listé → l'ajouter à la table des signaux.
- Si un département révèle un schéma de process type → le capitaliser dans la note canonique `[[auditer-departements-pour-automatisation]]` (enrichir, pas dupliquer).
