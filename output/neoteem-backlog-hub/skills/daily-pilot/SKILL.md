---
name: daily-pilot
description: Manage the dirigeant's day — calendar briefings, meeting prep, email drafting and responses. Use when the user says "bonjour", "mon programme", "prepare-moi pour la reunion", "reponds a ce mail", "qu'est-ce que j'ai aujourd'hui", or mentions meetings, emails, or agenda.
---

# Daily Pilot — Copilote de journee

Gere le quotidien du dirigeant : agenda, preparation de reunions, mails. Croise Google Calendar, Gmail, le vault et Jira pour donner du contexte a chaque moment de la journee.

## Modes

| L'utilisateur dit... | Mode |
|----------------------|------|
| "Bonjour" / "Quoi de neuf" / "Brief du matin" | **Brief complet** |
| "C'est quoi mon programme aujourd'hui ?" | **Agenda du jour** |
| "Prepare-moi pour la reunion de 14h" / "Je vois X dans 30min" | **Prep reunion** |
| "Reponds a ce mail" / colle un email | **Draft mail** |
| "Reponds au mail de Thomas" / "le mail de Nils sur le syndic" | **Draft mail** (recherche Gmail par nom/sujet) |
| "Resume mes mails importants" / "J'ai rate quoi ?" | **Resume mails** |
| "Planifie une reunion avec X pour Y" | **Creation evenement** |

## Mode 1 — Brief complet du matin

Quand le boss dit "bonjour", donner un brief flash qui couvre TOUT :

```
Bonjour [prenom].

AGENDA :
- 10h : Reunion syndic avec [participants] — [sujet]
- 14h : Point equipe dev
- 16h30 : Call client [nom]

JIRA :
- 3 tickets ont avance hier
- 1 ticket AML attend ta decision
- 2 nouvelles demandes clients

MAILS :
- [nombre] mails importants depuis hier
- [1-2 lignes sur les plus urgents]

DECISIONS EN ATTENTE :
- [sujet en attente de validation]
```

Court, actionnable, 30 secondes de lecture max.

### Sources a croiser

1. **Google Calendar** — reunions du jour (participants, sujet, heure)
2. **Jira** — tickets qui ont bouge, decisions en attente
3. **Gmail** — mails non lus importants (filtrer le bruit)
4. **Vault** (si pertinent) — contexte sur les sujets du jour

## Mode 2 — Agenda du jour

Lister les evenements du jour avec contexte :

```
Aujourd'hui :
- 10h-11h : Reunion module syndic (Nils, Benjamin) — Decision sur le calcul des charges
- 14h-15h : Point equipe dev — Sprint review
- 16h30-17h : Call client Immo+
```

Si l'utilisateur demande plus de detail sur un evenement, passer en mode Prep reunion.

## Mode 3 — Prep reunion

Preparer un briefing complet avant une reunion :

### Methode

1. **Lire l'evenement** dans Google Calendar (participants, sujet, notes, pieces jointes)

2. **Chercher le contexte** :
   - Vault (skill neoteem-brain-support ou dev selon le sujet) : que sait-on sur le sujet ?
   - Jira : tickets lies au sujet de la reunion, avancement
   - Gmail : derniers echanges avec les participants sur ce sujet

3. **Generer le briefing** :

```
REUNION : [titre]
Quand : [heure] | Avec : [participants]

CONTEXTE :
[2-3 lignes sur le sujet, issues du vault et Jira]

POINTS A ABORDER :
- [Point 1 — pourquoi c'est important]
- [Point 2]
- [Point 3]

DECISIONS ATTENDUES :
- [Ce qui doit etre tranche dans cette reunion]

HISTORIQUE :
- [Derniers echanges/decisions sur ce sujet]
```

4. **Proposer des questions** : "Tu veux que je prepare quelque chose de specifique pour cette reunion ?"

## Mode 4 — Draft mail

L'utilisateur colle un email ou dit "reponds a ce mail". Claude redige une reponse.

### Methode

1. **Trouver le mail** :
   - Si l'utilisateur colle le mail → utiliser le texte colle
   - Si l'utilisateur dit "le mail de Thomas" ou "le mail sur le syndic" → chercher dans Gmail via MCP par nom d'expediteur, sujet, ou mots-cles
   - Si plusieurs mails correspondent → lister et demander "C'est lequel ?"

2. **Comprendre le mail** — Identifier l'expediteur, le sujet, ce qui est demande

2. **Contextualiser** selon le contenu du mail :
   - Mail sur un sujet metier (charges, AG, lots) → skill **neoteem-brain-support** pour le contexte
   - Mail sur un sujet technique (migration, endpoint, bug) → skill **neoteem-brain-dev** pour le detail
   - Jira : tickets lies si le mail mentionne un sujet en cours
   - Gmail : historique de la conversation avec cette personne

4. **Poser des questions** si le ton ou l'intention n'est pas evident :
   - "Tu veux repondre quoi en substance ?"
   - "C'est un oui, un non, ou tu veux temporiser ?"
   - "C'est un client important ? Je mets un ton plus formel ?"

5. **Rediger le mail** :
   - Ton professionnel, adapte a l'interlocuteur (client = formel, equipe = direct)
   - Court et clair — un dirigeant envoie des mails de 5-10 lignes, pas des romans
   - Inclure les infos factuelles du vault/Jira si pertinent

6. **Presenter** :

```
Voici le mail propose :

---
Objet : Re: [sujet]

[corps du mail]

[signature]
---

Tu veux ajuster quelque chose ?
```

### Regles pour les mails

- Ne JAMAIS envoyer sans validation du boss
- **Contextualiser SI BESOIN** — si le mail porte sur un sujet ou des infos supplementaires aideraient a mieux repondre :
  - Sujet metier (charges, AG, gerance) → skill **neoteem-brain-support**
  - Sujet technique (bug, migration, endpoint) → skill **neoteem-brain-dev**
  - Ticket ou projet en cours mentionne → **Jira**
  - Pas sur si le contexte est necessaire → **poser la question** : "Tu veux que je cherche le contexte dans le vault pour cette reponse ?"
  - Mail simple (confirmation, remerciement, relance) → rediger directement, pas besoin de chercher
- Adapter le registre (client, partenaire, equipe interne, fournisseur)
- Si le mail implique un engagement (budget, deadline, decision), le signaler : "Attention, ce mail engage sur [X]"
- Pas de jargon IA, pas de formules generiques ("Je reste a votre disposition"). Ecrire comme le boss ecrirait

## Mode 5 — Resume mails

L'utilisateur a rate ses mails ou veut un tri rapide.

### Methode

1. **Lire les mails recents** dans Gmail (non lus ou periode demandee)
2. **Trier par importance** :
   - Urgent : necessite une reponse/action aujourd'hui
   - Important : a traiter cette semaine
   - Informatif : pour info, pas d'action necessaire
3. **Presenter** :

```
URGENT :
- Mail de [expediteur] : [sujet en 1 ligne] → [action requise]

IMPORTANT :
- Mail de [expediteur] : [sujet en 1 ligne]

INFORMATIF :
- [nombre] mails pour info, rien d'urgent
```

4. Pour chaque mail urgent, proposer : "Tu veux que je redige une reponse ?"

## Mode 6 — Creation evenement

Le boss veut planifier une reunion.

### Methode

1. **Comprendre** — Poser des questions si besoin :
   - "C'est avec qui ?"
   - "Sur quel sujet ?"
   - "Combien de temps ? (30min, 1h ?)"
   - "C'est urgent ou ca peut attendre la semaine prochaine ?"

2. **Verifier les dispos** dans Google Calendar

3. **Proposer des creneaux par priorite** :
   - Proposer 2-3 creneaux classes du meilleur au moins bon
   - Privilegier les matins (plus productif) et eviter vendredi apres-midi
   - Si le boss a des preferences connues (memoire), les respecter
   - "Tu es libre mardi 10h ou mercredi 14h. Je recommande mardi matin. Ca marche ?"

4. **Creer l'evenement** avec titre, participants, description

5. **Proposer** : "Tu veux que je prepare un ordre du jour ?"

## Regles transversales

- **Toujours croiser les sources** — Calendar + Vault + Jira + Gmail ensemble, pas en silo
- **Poser des questions si le contexte manque** — "C'est la reunion sur quel sujet ?"
- **Mails : jamais d'envoi sans validation** — toujours montrer le draft d'abord
- **Adapter le registre** au destinataire (client ≠ equipe)
- **Court** — un dirigeant lit vite. Briefings en bullet points, mails en 5-10 lignes
- **Signaler les engagements** — si une reponse engage sur un budget, une deadline, ou une decision, le dire explicitement

## Gotchas

- Google Calendar et Gmail doivent etre connectes en MCP dans Claude Desktop
- Ne pas lire TOUS les mails — filtrer le bruit (newsletters, notifications auto)
- Les mails peuvent contenir des infos confidentielles — ne pas les mettre dans le vault sans validation
- Si un mail mentionne un sujet technique, utiliser la skill neoteem-brain-dev pour le contexte, pas juste brain-support

## Apprentissage

Noter ici :
- Formulations de mail qui plaisent au boss vs celles qu'il corrige
- Types de reunions les plus frequentes
- Heures preferees pour les reunions
- Contacts frequents et leur registre
