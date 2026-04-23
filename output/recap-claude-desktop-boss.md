# Ce que Claude peut faire pour toi — Recap

> 3 plugins installes : neoteem-brain-support, neoteem-brain-dev, neoteem-backlog-hub

---

## 0. Brief du matin

Tu ouvres Claude, tu dis "bonjour". Il te fait un point flash.

**Exemple :**
> "Bonjour"
>
> → "3 tickets N2 ont avance hier (N2-8734 passe en test, N2-8801 livre, N2-8756 bloque par l'equipe front). 1 ticket AML en attente de ta decision (AML-4521, demande de modification des charges). 2 nouvelles demandes clients a trier."

30 secondes, actionnable, chaque matin.

---

## 1. Poser une question metier

Tu demandes, Claude cherche dans le vault (682+ notes de documentation Neoteem) avant de repondre.

**Exemples :**
- "Comment fonctionne le rappel de charges en copropriete ?"
- "C'est quoi la regle pour les cles de repartition ?"
- "Explique-moi le processus de vote en AG"

→ Reponse en langage metier, pas de code, pas de jargon technique.

---

## 2. Poser une question technique

Meme chose, mais Claude te donne le detail technique quand tu le demandes.

**Exemples :**
- "C'est quoi la fonction f_calc_charges ?"
- "Comment est structuree la base de donnees pour la compta ?"
- "Quel endpoint gere la creation de lots ?"

→ Reponse avec le detail technique complet (tables, fonctions, code).

---

## 3. Avoir un point d'avancement

Claude croise le vault (contexte fonctionnel) et Jira (etat reel des tickets).

**Exemples :**
- "Ou en est le module syndic ?"
- "Quels tickets sont bloques cette semaine ?"
- "Fais-moi un point sur le projet gerance"
- "Combien de tickets N2 ouverts sur la compta ?"

→ Reponse structuree : fait / en cours / bloque / prochaines etapes.

---

## 4. Trier une demande client (mail, texte, message)

Tu colles un mail ou un texte, Claude le transforme en spec structuree et cree le ticket N2.

**Exemples :**
- *Tu colles un mail :* "De : Mme Dupont. Objet : Probleme charges. Bonjour, nous avons remarque que les charges du T2 ne sont pas correctes depuis janvier..."
  → Claude reformule, cherche si un ticket similaire existe, propose une spec, attend ta validation, cree le ticket N2.

- "Un client a appele pour demander un export PDF des appels de fonds"
  → Meme workflow : reformulation, dedup, spec, ticket.

---

## 5. Analyser un ticket Jira existant

Tu donnes un numero de ticket, Claude le lit, l'enrichit avec le vault, et te fait une synthese.

**Exemples :**
- "Analyse le ticket AML-4521"
- "C'est quoi le ticket N2-8734 ? On a deja quelque chose de similaire ?"

→ Claude lit le ticket, cherche le contexte dans le vault, detecte les doublons.

---

## 6. Trier un lot de tickets d'un coup

Tu demandes d'analyser un ensemble de tickets, Claude les liste, les trie un par un, et fait un resume croise.

**Exemples :**
- "Trie tous les tickets AML ouverts"
- "Analyse les N2 sans spec crees cette semaine"
- "Y a des doublons dans les tickets AML du mois ?"

→ Claude liste les tickets, te demande lesquels traiter, trie chacun, puis resume : doublons detectes, regroupements suggeres.

---

## 7. Evaluer une proposition technique

Un dev ou un PO propose quelque chose. Claude traduit en impact business et donne un avis.

**Exemples :**
- "Raphael me dit qu'il faut migrer PostgreSQL, t'en penses quoi ?" → Claude explique le risque en termes business, recommande un planning, et formule ce que tu peux repondre au dev
- "On hesite entre refaire le module compta ou ameliorer le syndic" → Tableau comparatif impact/cout/risque + recommandation tranchee
- "C'est quoi le risque si on change le calcul des charges ?" → Liste des risques concrets + mitigation

---

## 8. Se faire proposer des evolutions

Claude connait ton logiciel via le vault. Il peut croiser avec les tickets Jira pour te proposer des ameliorations.

**Exemples :**
- "Qu'est-ce qu'on devrait ameliorer dans le module gerance ?" → Analyse vault + tickets Jira, 3 propositions classees par impact/effort
- "J'aimerais qu'on cree un portail client" → Claude cherche ce qui existe deja, evalue la faisabilite, propose une approche par etapes
- "On a le budget pour un seul projet ce trimestre, lequel ?" → Matrice impact/effort, recommandation argumentee

---

## 9. Booster ses demandes

Tu as une idee complexe mais tu sais pas comment la formuler. Claude te la reformule pour que le resultat soit top.

**Exemples :**
- "J'aimerais un truc qui compare nos modules avec les concurrents" → Claude te pose 2 questions, puis te propose une demande structuree prete a envoyer
- "Je voudrais savoir si on devrait faire un truc avec l'IA pour les AG" → Claude transforme ca en analyse structuree avec 3 cas d'usage concrets
- "Aide-moi a formuler une demande pour analyser notre churn" → Claude reformule, tu valides, il execute

---

## 10. Avoir un avis franc (pas un yes-man)

Claude est configure pour etre ton bras droit, pas un yes-man. Il te dit quand une idee est mauvaise.

**Exemples :**
- "Je pense qu'on devrait tout recoder en Java" → "Non. Voici pourquoi c'est une mauvaise idee, et voici ce qu'on devrait faire a la place."
- "On devrait supprimer la compta du logiciel" → "C'est un risque majeur parce que [raisons]. Alternative : [proposition]."
- "Je veux lancer 3 projets en meme temps" → "Avec l'equipe actuelle, c'est pas tenable. Voici comment prioriser."

---

## 11. Se souvenir de tes preferences

Claude retient tes corrections, tes preferences et le contexte de tes projets d'une conversation a l'autre.

**Exemples :**
- Tu dis "je prefere les recaps en bullet points" → il le retient pour toutes les prochaines conversations
- Tu corriges "non, le module s'appelle Gerance pas Gestion" → il ne refera plus l'erreur
- Tu travailles sur un sujet depuis 3 conversations → il se souvient du contexte

---

## En resume

| Tu dis... | Claude fait... |
|-----------|---------------|
| Question metier | Vault → reponse vulgarisee |
| Question technique | Vault → reponse detaillee |
| "Ou en est X ?" | Vault + Jira → point structure |
| *colle un mail client* | Triage → spec → ticket N2 |
| "Analyse le ticket X" | Jira + vault → synthese enrichie |
| "Trie les tickets AML" | Lot → dedup → regroupements |
| "Mon dev propose X" | Traduit en business → avis tranche |
| "On hesite entre A et B" | Comparatif → recommandation |
| "Qu'est-ce qu'on devrait ameliorer ?" | Vault + Jira → 3 propositions |
| "J'aimerais creer X" | Verifie l'existant → faisabilite → approche |
| "Aide-moi a formuler ca" | Reformule ta demande → tu valides → il execute |
| Mauvaise idee | Te le dit franchement |
| Demande floue | Te pose des questions |
