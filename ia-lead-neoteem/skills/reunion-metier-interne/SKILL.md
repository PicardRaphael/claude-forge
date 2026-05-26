---
name: reunion-metier-interne-neoteem
description: Aide Raphael (Responsable IA Neoteem) a preparer une reunion avec un metier interne (dev, design, devops, support, QA, commercial, redaction) pour identifier comment l'IA peut les aider au quotidien. A declencher des qu'il mentionne "reunion equipe support", "reunion dev", "reunion QA", "reunion commercial", "atelier IA equipe", "decouverte besoin IA interne", "comment l'IA peut aider mon equipe", "audit IA equipe X". Methode en deux temps : capter d'abord les vrais besoins, suggerer ensuite des cas d'usage IA cibles. Reunion cible 1h-1h30. Produit ordre du jour, questions de decouverte, cas d'usage IA par metier, livrables.
---

# Preparation reunion metier interne Neoteem

Tu aides Raphael a preparer une reunion avec une equipe metier interne de Neoteem. **Methode obligatoire en deux temps** :

1. **Capter** d'abord les vrais besoins, douleurs, taches repetitives, frustrations
2. **Suggerer** ensuite, en fin de reunion, des cas d'usage IA cibles

Ne JAMAIS arriver avec une liste de solutions IA prete a vendre. C'est le meilleur moyen de faire echouer l'adoption.

## Avant la reunion - questions a Raphael

Si Raphael n'a pas precise, demande-lui :

1. **Quel metier ?** (dev / design / devops / support / QA / commercial / redaction)
2. **Combien de personnes** dans la salle ?
3. **Niveau de maturite IA** de l'equipe ? (jamais utilise / utilise ChatGPT perso / utilise Claude au taf / pratique avancee)
4. **Ambiance pressentie** ? (curieux / inquiet pour leur poste / sceptique / deja convaincu)
5. **C'est une premiere reunion** ou un suivi ?

Ces 5 reponses changent radicalement la structure.

## Structure d'ordre du jour - reunion DECOUVERTE (1er passage)

```
1. Cadrage et rassurance - 5 min
   - Pourquoi cette reunion (et pourquoi maintenant)
   - Ce qu'on cherche (les aider) / ce qu'on ne cherche PAS (les remplacer)
   - Format de la reunion

2. Tour de table express - 10 min
   - Chacun : son role, sa journee type
   - Pas de jugement, pas de notes ostentatoires

3. Cartographie des taches - 25 min
   - Taches recurrentes (quotidiennes / hebdo / mensuelles)
   - Taches a faible valeur ajoutee
   - Taches a forte cognitive (fatigue)
   - Taches bloquees ou ralenties par d'autres equipes

4. Frustrations et reves - 15 min
   - "Si j'avais un assistant magique, je lui demanderais..."
   - "Ce qui me fait perdre 1h par jour c'est..."
   - "Si je pouvais arreter une tache, ce serait..."

5. Suggestions IA (sans s'engager) - 10 min
   - Je vous propose 3-4 pistes basees sur ce que j'ai entendu
   - Vous me dites lesquelles vous parlent

6. Suite et engagement - 5 min
   - Prochaine etape
   - Volontaires pour un pilote ?
```

## Questions de decouverte - communes a tous les metiers

### Bloc 1 - Quotidien reel [CRITIQUE]

- Decris-moi ta journee type, heure par heure
- Quelles sont les 3 taches que tu fais TOUS les jours sans exception ?
- Quelle tache te prend le plus de temps mais te semble le moins valorisante ?
- Sur quelle tache es-tu le plus lent / le moins a l'aise ?
- Quelle tache demande une concentration enorme pour un resultat moyen ?

### Bloc 2 - Frictions et blocages

- Sur quoi attends-tu d'autres equipes plus de 30 min par semaine ?
- Quelle info te manque regulierement et que tu dois chercher ?
- Quelle question reviens systematiquement de la part des clients / collegues ?
- Quel outil utilises-tu en bricolant parce qu'il n'est pas adapte ?
- Quand tu rentres de vacances, qu'est-ce que tu redoutes le plus ?

### Bloc 3 - Volume et repetition

- Sur 100 demandes/tickets/cas que tu traites, combien se ressemblent ?
- Y a-t-il des modeles, des templates, des reponses-type que tu reutilises ?
- Quelle tache fais-tu en mode "pilote automatique" sans plaisir ?

### Bloc 4 - Connaissance et memoire

- Ou est documente ce que tu sais faire ? (nulle part, Confluence, ta tete, un fichier perso)
- Si tu partais demain, combien de temps faudrait-il pour te remplacer ?
- Quelle info reviens-tu chercher regulierement dans les memes documents ?

### Bloc 5 - Perception IA [IMPORTANT, manier avec precaution]

- Qu'est-ce que l'IA evoque pour toi dans ton metier ? (sans jugement)
- As-tu deja utilise ChatGPT / Claude / Gemini, meme perso ?
- Qu'est-ce qui te ferait peur si on introduisait de l'IA dans ton quotidien ?
- Qu'est-ce qui te ferait plaisir ?

### Bloc 6 - Volonte de tester

- Es-tu pret a tester un outil IA 2 semaines en pilote ?
- A quelle frequence accepterais-tu de me faire un retour ?
- Qu'est-ce qui te ferait dire "ok ca m'aide vraiment" vs "ca me fait perdre du temps" ?

## Questions specifiques par metier

### Dev

- Combien de % de ton temps en code vs en lecture / comprehension / debug ?
- Quelles parties du code te font perdre du temps a comprendre ? (legacy, doc absente)
- Les revues de PR : trop, pas assez, mal faites ?
- Sur Loji / back2.0 / Neo* : quelle partie tu eviterais de toucher si tu pouvais ?
- Le ticket Jira que tu recois : assez clair pour bosser, ou tu dois souvent re-demander ?
- Utilises-tu deja Claude Code ? Si oui, ou est-ce qu'il te lache ?

Cas d'usage IA a suggerer si pertinent :
- Generation et review de tickets Jira
- Generation tests unitaires / d'integration
- Documentation automatique du legacy
- Pair programming via Claude Code sur back2.0
- Recap de PR / changelogs auto

### Design

- Combien de versions / iterations sur un meme ecran avant validation ?
- Quelles taches "techniques" prennent du temps (export, declinaisons, specs) ?
- Les retours metier sont-ils clairs ou il faut deviner ?
- La design system Loji est-elle a jour, documentee, applicable ?

Cas d'usage IA a suggerer si pertinent :
- Generation de variantes / declinaisons rapides
- Generation de specs Figma vers code
- Audit accessibilite automatise
- Generation de microcopy / textes UI

### DevOps

- Combien d'alertes par semaine, dont combien de faux positifs ?
- Quelle proportion d'incidents est repetitive (memes causes, memes solutions) ?
- Le runbook / documentation incident est-il a jour ?
- Combien de temps a creuser les logs vs reparer ?
- Le scaling Cloud Run / GCP : maitrise ou tatonnement ?

Cas d'usage IA a suggerer si pertinent :
- Triage / categorisation d'alertes
- Analyse de logs et root cause assistee
- Generation de runbooks a partir de l'historique d'incidents
- Predictif sur les couts cloud

### Support

- Combien de tickets par jour ? Combien de % similaires entre eux ?
- Quel est le top 10 des questions clients recurrentes ?
- Quels tickets demandent le plus de recherche dans la doc / le code / l'historique ?
- Quelles donnees client te manquent au moment de repondre ?
- La base de connaissance / Confluence est-elle utilisable en lecture rapide ?

Cas d'usage IA a suggerer si pertinent :
- Reponses-type suggerees (avec validation humaine)
- Classification automatique de tickets
- Resume des fils de conversation longs
- Assistant interne avec acces neoteem-brain
- Detection de tickets a risque (client mecontent, escalade)

### QA

- Quel est ton ratio test manuel vs test automatique aujourd'hui ?
- Sur quelles fonctionnalites les bugs reviennent le plus ?
- Combien de temps a rediger / mettre a jour des plans de test ?
- Les specs que tu recois sont-elles testables (criteres clairs) ?
- Combien de regressions detectees en prod vs en QA ?

Cas d'usage IA a suggerer si pertinent :
- Generation de cas de tests a partir de specs
- Generation de tests automatises (Playwright, etc.)
- Detection d'anomalies dans les logs prod
- Resume executif des campagnes de test

### Commercial

- Combien de temps en demo / RDV vs en prep / suivi / CRM ?
- Les objections clients : recurrentes ou variees ?
- Combien de temps a chercher des infos sur un prospect / un compte ?
- La base concurrentielle (Genius Immo, Reemia AI) est-elle a jour ?
- Les propositions commerciales : faites a la main ou templates ?

Cas d'usage IA a suggerer si pertinent :
- Generation de propositions / devis personnalises
- Brief client en amont de RDV (recherche web + historique)
- Suivi CRM assiste (recap d'appels, prochaines actions)
- Battle cards concurrentielles a jour
- Reponses aux objections personnalisees

### Redaction

- Quel est ton volume par semaine (articles, docs, emails, releases) ?
- Combien de temps en recherche vs en redaction vs en correction ?
- Les briefs que tu recois sont-ils utilisables ou tu dois inventer ?
- Quels formats reviennent souvent (release notes, doc fonctionnelle, comm interne) ?
- Le ton / vocabulaire Neoteem est-il documente ?

Cas d'usage IA a suggerer si pertinent :
- Generation de premieres versions a iterer
- Adaptation d'un texte selon canal (release note vs comm client vs LinkedIn)
- Traduction maintenue (FR / EN)
- Recherche augmentee (web + neoteem-brain)
- Charte editoriale assistee

## Pieges a eviter / signaux faibles a capter

- **L'enthousiaste qui dit "remplacons tout par l'IA"** : signal d'inexperience, recadrer
- **Le silencieux qui croise les bras** : peur du remplacement, lui parler en 1-1 apres
- **"On a deja essaye un chatbot ca marche pas"** : creuser le contexte, ce n'est pas un argument
- **Les douleurs verbalisees mais minimisees** ("c'est rien, j'ai l'habitude") : ce sont souvent les meilleurs cas d'usage
- **Les "petites choses" repetees 10 fois par jour** : meilleur ROI IA generalement
- **L'absence de manager dans la salle** : risque que les decisions ne soient pas validees apres

## Livrables a produire APRES la reunion

Pour Raphael (notes internes) :
- Cartographie des taches par personne
- Top 5 frustrations consolide
- 3-5 cas d'usage IA prioritaires (impact x faisabilite)
- Liste des volontaires pour pilote

Pour l'equipe (compte-rendu envoye) :
- Ce qu'on a entendu (sans nom)
- Les 3-5 pistes IA proposees
- Le calendrier propose (pilote ? sur quoi ? quand ?)
- Le point de contact (Raphael)

Pour la direction (synthese) :
- Maturite IA percue de l'equipe (echelle 1-5)
- Adherence (echelle 1-5)
- Investissement requis (temps / outil / formation)
- Risques d'adoption identifies

## Rappel RGPD / risques (court systematique)

Memes pour des outils internes, attention aux donnees personnelles que l'equipe manipule (clients, collegues). Verifier qu'aucun POC ne fuite de donnees clients vers des LLM hors EU sans cadrage. Reflexes : tenant local / proxy / anonymisation avant tout pilote.
