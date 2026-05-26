---
name: formation-ia-neoteem
description: Aide Raphael (Responsable IA et formateur) a concevoir et animer des formations IA pour les collaborateurs de Neoteem. A declencher des qu'il mentionne "formation IA", "session de formation", "atelier IA", "onboarding IA", "montee en competence IA", "support de formation", "syllabus IA", "evaluation formation", "tuto interne", "academie IA Neoteem", "former l'equipe a Claude Code", "former le support a l'IA". Couvre conception de cursus, design d'atelier, supports, exercices pratiques, evaluation, evolution dans le temps. Adapte au public Neoteem (dev, design, devops, support, QA, commercial, redaction, direction).
---

# Formation IA interne Neoteem

Tu aides Raphael a concevoir et animer des formations IA pour les collaborateurs Neoteem. Raphael est le formateur, pas un prestataire externe.

## Detection du besoin

Identifie d'abord lequel des contextes est le sien :

1. **Concevoir un cursus complet** (ex : academie IA Neoteem 2026)
2. **Concevoir une session ponctuelle** (ex : atelier prompt engineering, 2h)
3. **Onboarder un nouveau collaborateur** sur l'IA
4. **Mettre a jour un support** existant
5. **Evaluer l'efficacite** d'une formation passee
6. **Diffuser une bonne pratique** decouverte

## Avant de concevoir - questions a Raphael

1. **Public cible** : un metier specifique ou mixte ? Niveau de depart ?
2. **Format** : presentiel, distanciel, hybride, autonomie ?
3. **Duree** : session unique, parcours sur N semaines ?
4. **Objectif declare** : sensibilisation, mise en pratique, maitrise avancee ?
5. **Contraintes** : budget, planning, outils disponibles (claude.ai, Claude Code, API)
6. **Mesure du succes** : satisfaction, mise en pratique reelle, KPI metier ?

## Cursus type - "Academie IA Neoteem" (modulaire)

```
Module 1 - Fondamentaux IA (2h, tous publics)
- Comprendre ce qu'est un LLM (sans entrer dans la tech)
- Forces et limites (hallucinations, contexte, biais)
- Cas d'usage concrets vus chez Neoteem
- Exo : 3 prompts a essayer en live

Module 2 - Prompt engineering basique (2h, tous publics)
- Anatomie d'un bon prompt (contexte, tache, format, exemples)
- Quand structurer, quand laisser libre
- Iteration et amelioration
- Exo : transformer une demande floue en prompt qui marche

Module 3 - Outils Anthropic et Neoteem (1h30, tous publics)
- claude.ai : usages quotidiens
- Claude Code : pour qui, quand
- MCP, agents, artifacts : a quoi ca sert
- neoteem-brain : notre base de connaissance IA
- Exo : utiliser neoteem-brain en live

Module 4 - Specifique metier (2h, par metier)
- Voir liste par metier ci-dessous

Module 5 - RGPD, securite, ethique (1h, tous publics)
- Quelles donnees on peut / ne peut pas mettre dans un LLM
- Localisation des traitements
- Anonymisation, pseudo, masquage
- Que faire en cas d'erreur IA (process Neoteem)
- Exo : QCM situations a risque

Module 6 - Aller plus loin (auto-formation, ressources)
- Lectures conseillees
- Ressources internes (neoteem-brain, Confluence)
- Communaute IA en interne (canal Slack, weekly partage)
```

## Variantes par metier - Module 4

### Devs

- Claude Code en profondeur (config, hooks, agents, MCP)
- back2.0 + Claude Code : workflow type
- Generation de tests, refacto, doc, review
- Limites : ne pas laisser Claude decider, le dev reste responsable

### Design

- Generation et iteration visuelle avec IA
- Specs vers code via Claude
- Audit accessibilite assistee
- Microcopy / UX writing avec LLM

### DevOps

- Analyse de logs avec LLM
- Generation de runbooks
- Optimisation infra Cloud Run / GCP avec assistance
- Securite : sensibilite des configs et secrets

### Support

- Reponses-type assistees (et leur revue humaine)
- Resumes de conversations longues
- Classification ticket
- Recherche dans neoteem-brain

### QA

- Generation de cas de test a partir de specs
- Generation de tests automatises
- Detection d'anomalies
- Limites : pas de remplacement du jugement humain

### Commercial

- Brief de prospect (recherche web + LLM)
- Propositions personnalisees
- Battle cards Genius Immo / Reemia AI
- Reponse aux objections

### Redaction

- Generation et iteration d'articles, release notes, doc
- Adaptation par canal
- Maintien du ton / vocabulaire Neoteem
- Bonnes pratiques : iterer, ne pas publier brut

## Design d'un atelier 2h - canevas

```
0-10 min : Accueil et niveau de connaissance
- Sondage rapide (5 questions, "main levee")
- Adapter le niveau de la session

10-30 min : Theorie courte et claire
- Slides max, exemples concrets
- Pas plus de 3 concepts cles

30-90 min : Pratique guidee (le coeur)
- 3-5 exercices progressifs
- Chacun avec un livrable visible
- Co-animation : Raphael + un volontaire qui montre son ecran

90-105 min : Retour collectif
- Tour de table : ce que chacun a essaye
- Difficultes rencontrees
- Astuces decouvertes

105-120 min : Suite et engagement
- 1 chose a essayer cette semaine
- Ou trouver de l'aide
- Prochain atelier annonce
```

## Questions pour evaluer un atelier ou cursus

### Pendant (a chaud)

- Sur une echelle de 1 a 10, comment vous notez la session ?
- Qu'avez-vous appris que vous ne saviez pas ?
- Qu'est-ce que vous allez essayer cette semaine ?
- Qu'est-ce qui aurait pu etre mieux ?
- Recommanderez-vous cet atelier a un collegue ?

### A froid (2-4 semaines apres)

- Avez-vous utilise ce qu'on a vu ensemble ? Combien de fois ?
- Sur quoi precisement avez-vous gagne du temps ?
- Qu'est-ce qui vous a freine pour mettre en pratique ?
- De quoi auriez-vous besoin maintenant pour aller plus loin ?

## Bonnes pratiques pedagogiques

- **Toujours montrer avant de faire faire** : 1 demo live > 10 slides
- **Eviter le jargon** : LLM, RAG, prompt = a expliquer une fois, pas a tartiner
- **Pratique > theorie** : 70% pratique minimum sur le temps total
- **Petits groupes** : max 8-10 personnes par atelier pratique
- **Outils prets** : verifier acces et licences avant d'arriver
- **Cas concret Neoteem** : exemples tires du quotidien Loji / equipe
- **Pas de jugement** : un dev senior peut ne rien connaitre a l'IA, c'est normal
- **Mesurer la mise en pratique** : satisfaction post-atelier n'est PAS le bon KPI

## Pieges a eviter

- **Formation theorique sans pratique** : tout le monde oublie sous 7 jours
- **Trop ambitieux pour le temps** : reduire le contenu, garder la pratique
- **Public trop heterogene** : separer les niveaux quand possible
- **Demos qui plantent** : tester l'environnement avant, prevoir un plan B (video, screenshots)
- **"Vous verrez en autonomie"** : taux de mise en pratique tombe a 5%
- **Pas de suivi a J+30** : la formation est oubliee sans rappel
- **Top-down impose** : participation chute, ressentiment monte

## Livrables a produire

Pour chaque atelier / module :
- Plan de session (timing, contenu, exercices)
- Supports visuels (slides ou markdown) - rester sobre
- Exercices avec solutions
- Quiz / QCM eventuel (RGPD utile)
- Document "Pour aller plus loin"
- Survey post-atelier (5 questions max)

Pour un cursus complet :
- Page Confluence "Academie IA Neoteem"
- Calendrier modules + inscrits
- Suivi assiduite et progression
- Bilan trimestriel partage en weekly

## Sujets specifiques formation Claude Code (pour devs)

Niveau 1 - Decouverte (1h)
- Installation, premiers prompts
- Lecture, edition, multi-fichier
- Bonnes pratiques de prompt

Niveau 2 - Maitrise (2h)
- Configuration .claude/ (settings, hooks, allowed-tools)
- MCP : ajouter un serveur (ex : MCP Atlassian)
- Agents specialises
- Workflow type sur back2.0

Niveau 3 - Avance (3h)
- Skills custom
- Hooks complexes
- Multi-agents et orchestration
- Integration en CI / pre-commit

## Rappel RGPD / risques (court systematique)

Une formation IA doit toujours inclure un volet "ce qu'on ne met pas dans un LLM" : donnees client identifiantes, donnees bancaires, donnees RH sensibles, secrets / credentials, contenus confidentiels d'autres clients. Donner aux participants un reflexe simple : "si je ne le mettrais pas sur un post-it sur mon bureau ouvert, je ne le mets pas dans un LLM grand public". Pour les besoins pro reels, utiliser claude.ai entreprise ou l'API avec ZDR.
