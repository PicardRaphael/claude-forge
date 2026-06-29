---
titre: "Auditer un département tiers pour identifier ses process automatisables par l'IA"
resume: "Méthode pour interviewer un département (Support, RH, Migration, PO, Commercial) et en tirer des recommandations d'automatisation IA : entretien de découverte story-based (Torres/Portigal/Moesta) → repérage des signaux d'automatisabilité → fiche process → workflow de qualification (équation qualité + bottleneck + gradation chatbot/workflow/agent, Eliott Meunier). Découpe en 2 phases : INTERVIEW puis RECO."
aliases:
  - "auditer un département pour l'IA"
  - "interview de découverte automatisation"
  - "discovery process automatisable"
  - "audit besoins automatisation entreprise"
  - "interviewer un service pour proposer des agents"
  - "process automation discovery interview"
type: technique
domaine: patterns
status: active
derniere-maj: 2026-06-29
auteur: claude
sources:
  - "https://www.youtube.com/watch?v=pjRKfnlsTfk (podcast intégration IA entreprise — Elliot & Rémy)"
  - "https://www.producttalk.org/2022/04/best-customer-interview-questions/ (Teresa Torres — Continuous Discovery)"
  - "https://www.nngroup.com/articles/user-interviews/ (Nielsen Norman Group)"
  - "https://commoncog.com/putting-jtbd-interview-to-practice/ (Bob Moesta — JTBD switch interview)"
  - "https://www.userinterviews.com/blog/interviewing-users-steve-portigal-applied-to-remote-research (Steve Portigal — 7 étapes)"
  - "https://docs.uipath.com/automation-hub/automation-cloud/latest/user-guide/automation-pipeline (UiPath — grille Automation Potential)"
tags:
  - "#type/technique"
  - "#domaine/patterns"
  - "#domaine/ia"
  - "#casquette/responsable-ia"
---

## Quand utiliser cette note

Déclencheur : **« je veux aller voir un département de mon entreprise (Support, RH, Migration, PO, Commercial…) pour comprendre son travail et lui proposer des agents / automatisations IA »**. Tu interviewes un **tiers** sur SON métier, tu n'audites pas ton propre quotidien.

Frontière nette avec les notes sœurs :
- [[cartographier-process-cma]] = auditer **MON propre** quotidien (CMA : Clarifier · Mapper · Amplifier), un portfolio de mes process.
- [[methode-monter-systeme-workflow]] = pour CE besoin précis, **quelle brique** (skill/agent/hook/MCP) construire.
- **Cette note** = interviewer **quelqu'un d'autre** pour découvrir SES process, puis qualifier lesquels valent une automatisation. La couche manquante : la **technique d'entretien** (le QUOI demander + le COMMENT mener).

Une fois les process découverts et qualifiés, on route vers [[methode-monter-systeme-workflow]] (quelle brique) puis vers les créateurs forge.

## Les 2 phases (à ne pas mélanger)

```
PHASE 1 — INTERVIEW (interactif, humain)       PHASE 2 — RECO (transformation)
interviewer le département                     analyser la/les fiche(s) process
→ cadrage anti-politique                       → équation qualité
→ questions story-based                        → diagnostic bottleneck
→ creusage (silence, 5 whys, laddering)        → gradation chatbot/workflow/agent
→ repérer signaux d'automatisabilité           → priorisation impact × effort
OUTPUT : fiche process (Interview Snapshot)    OUTPUT : reco priorisée + OST
```

La phase 1 est **interactive et pilotée** (output variable, l'humain mène l'entretien) ; la phase 2 est une **transformation** (fiche → reco). Deux responsabilités distinctes = deux skills.

## Phase 1 — L'entretien de découverte

### Principe cardinal (corroboré Torres + NN/g + Moesta)
**Comportement passé > opinions > futur hypothétique.** Faire raconter du vécu, jamais demander des opinions ni du « il faudrait ». Les gens décrivent mal leur process en théorie ; précisément quand ils racontent la dernière fois qu'ils l'ont fait. Distinguer **question de recherche** (ce que tu veux apprendre) de **question d'entretien** (ce que tu demandes) — ne jamais poser la première directement.

### Structure (Portigal, simplifiée)
1. **Ouverture facile** — mettre à l'aise, questions sans jugement.
2. **Cadrage anti-politique** (essentiel en interne) — *« Je ne viens pas évaluer ton travail. Je veux comprendre comment ça se passe vraiment, pour voir ce qu'on pourrait t'enlever des mains. Rien ne te sera attribué. »* Et **ne pas révéler l'intention précise trop tôt** (sinon l'interviewé reverse-engineere ce qu'il croit que tu veux entendre, et masque le reste).
3. **Corps chronologique** — suivre l'ordre du process (découvrir → faire → vérifier → transmettre), pas par thème.
4. **Tipping point** — le passage des réponses courtes/prudentes au mode récit. C'est là que naît la vraie donnée ; tout ce qui précède est du setup.
5. **Soft close** — *« Si tu avais une baguette magique, qu'est-ce que tu changerais ? »* Garder l'attention active jusqu'au bout (les meilleures infos sortent quand la garde tombe).

Solo en découverte (la politique fausse les groupes) ; atelier de groupe **après**, pour synthétiser. ~45-60 min réaliste pour couvrir un process complet + creusage.

### Questions story-based (formulations réutilisables)
- *« Raconte-moi la dernière fois que tu as [traité un ticket / fait un recrutement / migré un client]. Pars du tout début. »*
- *« Déroule-moi une journée type sur cette tâche. »*
- *« Raconte-moi une fois où ça a mal tourné. »*
- Ancrage sensoriel (réveille la mémoire) : *« C'était quel jour ? Tu utilisais quel outil ? Qui d'autre était impliqué ? »*
- Calibrer la largeur : de *« la dernière fois que tu as fait quelque chose de répétitif »* (large) à *« la dernière fois que tu as relancé un client en retard »* (étroit).

### Creusage
- **Silence 3-5 s** après une réponse — la 2e couche (plus honnête) sort dans le vide.
- *« Raconte-moi en plus » / « Concrètement, ça donne quoi ? »*
- **5 Whys** — séparer le symptôme (« ça prend trop de temps ») de la cause racine (« je ne fais pas confiance aux données, donc je revérifie tout »).
- **Laddering** — *« Ça te permet de faire quoi ? »* pour remonter à la motivation.
- Clarifier le vague — *« Tu dis 'compliqué' : qu'est-ce qui le rend compliqué ? »*
- **JTBD / 4 forces** (Moesta) pour comprendre pourquoi un process existe sous sa forme actuelle : Push (frustration de l'existant) · Pull (attrait du nouveau) · Anxiety (peur du changement, force la plus sous-estimée) · Habit (inertie). Cadre **What/How** plutôt que Why (le pourquoi pousse à rationaliser).

### Repérer un candidat à l'automatisation (signaux à écouter, pas questions séparées)
- **Répétitivité + volume** : ≥ quotidien/hebdo, plusieurs personnes.
- **Règles explicites vs jugement tacite = LE discriminant** : *« Comment tu décides quoi faire ? C'est une règle claire, ou ça dépend de ton expérience ? »* Règles claires → automatisation déterministe ; ambiguïté/langage/jugement → terrain IA.
- **Données** : structurées (Excel/formulaire/PDF exploitable) = facile ; non structurées (mail/conversation) = terrain IA.
- **Savoir explicitable vs implicite** (Eliott Meunier) : un process est automatisable proportionnellement à son savoir documentable ; le savoir tacite (« il n'y a que Jérôme qui sait ») est le frein principal.
- Temps perdu, ressaisie multi-systèmes, copier-coller entre outils.
- **Stabiliser AVANT d'automatiser** : automatiser un process bancal crée de la dette ; corriger d'abord.

### Pièges
- Parler trop (viser ~80 % de temps de parole pour l'interviewé).
- Questions suggestives (*« c'est pénible de ressaisir, non ? »* → *« raconte-moi cette étape »*).
- Biais de confirmation (réaction neutre et constante ; ne pas noter seulement ce qui confirme).
- Sauter à la solution / demander des specs (*« il me faudrait un bouton »* → *« ça te permettrait de régler quoi ? »*).
- Confondre déclaratif et comportement (pour les volumes/fréquences réels, compléter par logs/observation).

## Phase 2 — La reco d'automatisation (workflow Eliott Meunier, vidéo 1)

### Équation de qualité (reframe)
**Qualité output = Puissance du modèle × Outils connectés × Contexte.** Ne pas overthinker le modèle ; la valeur est dans le **contexte** (process + méthode + données client documentés).

### Diagnostic du goulot d'étranglement
*« Où le département est-il bloqué ? »* Trois zones : **Acquisition / Production-Delivery / Rétention**. Commencer par le process **le plus contraignant** maintenant, croisé avec **l'équipe la plus motivée** (adhésion).

### Séquence 3 layers (NE PAS inverser)
1. **Contexte holistique** (world model : statique = offres/orga/OKR + dynamique = données qui évoluent).
2. **Mapping horizontal** de tous les process du département.
3. **SEULEMENT ensuite** : agents/skills/automatisations.
> Anti-pattern central : partir du layer 3 (les agents d'abord) → « ça casse en 2-6 semaines, personne derrière pour gérer ».

### Gradation — qualifier le bon niveau de solution
| Niveau | Quoi | Quand |
|---|---|---|
| **1 — Chatbot assisté** | L'humain fait la plomberie (copier-coller) | 95 % des usages aujourd'hui |
| **2 — Workflow contextualisé** | L'IA va chercher les données, a la méthode + le format, produit ; déclenché par un humain | Le sweet spot de la plupart des process |
| **3 — Agent autonome** | Trigger événementiel, sans humain dans la boucle | La DERNIÈRE phase, jamais la première |
> « Ce qui est vendu comme agent IA est en réalité plus un workflow. » L'autonomie se mérite après avoir prouvé la valeur sur les niveaux 1-2.

### Top-down vs bottom-up (curseur, pas binaire)
- **Top-down** (petite boîte / dirigeant pro-IA) : interviews → reco → atelier de restitution → tuyauterie → formation.
- **Bottom-up** (grande boîte / résistance) : ateliers de 3-7 personnes, chaque équipe fait son 1er use case, contagion organique.

## Restitution

- **Fiche par process** (Interview Snapshot, Torres — remplie 15-20 min après l'entretien) : Qui · citation mémorable · **Opportunités** (douleurs actionnables) · **Insights** (notables mais pas encore actionnables, section séparée) · carte d'expérience (étapes du process). Pour un audit d'automatisation, ajouter : Fréquence/volume · Règles explicites ou jugement tacite · Données structurées ? · Candidat IA vs règles · niveau de solution proposé.
- **Opportunity Solution Tree** ([[Continuous Discovery]] Torres) comme synthèse transverse : Outcome → Opportunités (douleurs) → Solutions (agents candidats) → Tests. Construire après 3-4 entretiens, réviser tous les 3-4. Sizing sans analytics = compter combien de fiches mentionnent la même opportunité.
- **Straw model** pour l'atelier de groupe : arriver avec un brouillon de cartographie issu des 1:1, les participants corrigent (résout les perceptions contradictoires plus vite qu'une page blanche).

## Mises en garde de sourcing (vérifié, à ne PAS citer comme canon)

- Milkshake JTBD = *« environ la moitié »*, pas « >50 % » (mot de Christensen).
- « McKinsey 70-80 % du volume par règles » = **attribution fausse**, ne pas l'attribuer à McKinsey.
- « Push + Pull > Anxiety + Habit » = dispositif pédagogique, **pas** une équation de Moesta (basculement dynamique, pas seuil algébrique).
- Seuil « 2 FTE », délais « 6-8 / 12-16 semaines », taxonomie « 5 patterns » = directionnels seulement. Seule grille adossée à une source primaire = **UiPath Automation Hub** (Automation Potential % + Ease of Implementation 0-100 %).

## Liens

- [[cartographier-process-cma]] — méthode sœur : auditer MON propre quotidien (vs un tiers ici)
- [[methode-monter-systeme-workflow]] — l'étape d'après : pour le process retenu, quelle brique construire
- [[Continuous Discovery]] — Teresa Torres, OST et Interview Snapshot (le squelette de restitution)
- [[architecture-cerveau-obsidian-mcp]] — la couche contexte (world model) sur laquelle la phase 2 s'appuie
- [[n8n-self-host-mcp-claude]] — cible si le verdict est une automatisation externe
