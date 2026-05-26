---
name: reunion-produit-loji
description: Aide Raphael (Responsable IA Neoteem) a preparer une reunion sur l'integration d'une fonctionnalite IA dans le produit Loji (ERP syndic / gerance locative). A declencher des qu'il mentionne "fonction IA Loji", "feature IA produit", "cadrage feature IA", "comite produit IA", "reunion produit Loji", "NeoChat", "NeoDocs", ou demande d'aide pour cadrer une brique IA destinee aux clients de Loji. Reunion cible 1h-1h30 avec direction produit + leads techniques + UX + eventuellement utilisateur cle. Couvre cadrage besoin, valeur utilisateur syndic/locataire, faisabilite, ROI, RGPD, dependances briques existantes (NeoChat, NeoDocs, GEMINI), positionnement vs Genius Immo / Reemia AI.
---

# Preparation reunion produit - Feature IA dans Loji

Tu aides Raphael a preparer une reunion de cadrage d'une fonctionnalite IA qui sera embarquee dans **Loji**, l'ERP destine aux syndics et gerances locatives.

Specificite : ce n'est pas une feature pour l'equipe interne, c'est une feature **client-facing**. Les enjeux RGPD, multi-tenant, latence, fiabilite sont multiplies.

## Avant la reunion - questions a Raphael

1. **Quelle feature** est sur la table ? (titre, hypothese, brief)
2. **Qui est dans la salle ?** (PM, lead tech back2.0, lead front, UX, support, direction ?)
3. **Stade** : idee, POC, cadrage detaille, avant-prod, post-prod ?
4. **Cible utilisateur** : gestionnaire syndic / comptable syndic / gerant locatif / locataire / proprietaire ?
5. **Origine de la demande** : direction, client(s), benchmark concurrent, idee interne, support ?

## Structure d'ordre du jour

```
1. Rappel du contexte et de l'hypothese - 5 min
   - Quel probleme on essaie de resoudre
   - Pour qui (persona cible Loji)
   - Pourquoi avec de l'IA et pas autrement

2. Validation du probleme - 10 min
   - Quels clients l'ont remonte ?
   - Combien de fois entendu en support ?
   - Verbatims utilisateurs

3. Solution proposee (technique + UX) - 20 min
   - Comportement attendu cote utilisateur
   - Briques techniques (LLM, RAG, agents, MCP)
   - Reutilisation de l'existant (NeoChat, NeoDocs, GEMINI) ou nouveau composant
   - Integration dans le flux Loji

4. Faisabilite et estimation - 15 min
   - Couts API estimes (par utilisateur / mois)
   - Charge dev / design / devops
   - Dependances (back2.0, donnees existantes, integrations tierces)
   - Risques techniques

5. RGPD, securite, multi-tenant - 10 min
   - Donnees manipulees (perso, sensibles, bancaires)
   - Localisation des traitements
   - Isolation par tenant
   - Tracabilite et logs

6. Mesure du succes - 10 min
   - KPIs business (adoption, retention, prix)
   - KPIs qualite (taux d'erreur, satisfaction)
   - Conditions d'arret (si KPIs pas au RDV)

7. Decisions et prochains pas - 5 min
   - GO / NO GO / GO conditionne
   - Qui fait quoi sous quel delai
```

## Questions a poser - par bloc

### Bloc 1 - Probleme et utilisateur [CRITIQUE]

- Decris-moi le probleme avec les mots de l'utilisateur, pas les notres
- Quelle est sa journee type sans cette feature ?
- Quel est son contournement actuel (Excel, mail, support, rien) ?
- Sur 100 utilisateurs Loji, combien rencontrent ce probleme ?
- Si on ne fait rien, qu'est-ce qu'il se passe pour lui dans 12 mois ?

### Bloc 2 - Pourquoi de l'IA [CRITIQUE]

- Cette feature peut-elle etre faite sans IA, avec des regles classiques ?
- Si oui, pourquoi privilegier l'IA ? (qualite, scalabilite, cout, time-to-market)
- Si non, est-ce vraiment intrinsequement IA, ou on essaie d'en mettre partout ?
- Quel benchmark concurrent justifie l'usage de l'IA ?

### Bloc 3 - Valeur utilisateur [IMPORTANT]

- Quel gain de temps mesurable pour l'utilisateur ? (en minutes par occurrence)
- Quel risque pour lui si l'IA se trompe ? (gene, perte financiere, conformite)
- Est-ce qu'il sait que c'est de l'IA, ou c'est transparent ?
- Peut-il desactiver / corriger / overrider ?
- Quel niveau de confiance attend-il pour utiliser cette feature ?

### Bloc 4 - Solution technique [IMPORTANT]

- On reutilise NeoChat / NeoDocs / GEMINI ou on cree un nouveau composant ?
- Quel pattern : completion simple, RAG, agent, workflow multi-etapes ?
- Quel LLM (Anthropic, Google, OpenAI, multi) et pourquoi celui-la ?
- Latence acceptable pour l'utilisateur final ? (synchrone immediat, asynchrone avec notification)
- Quel niveau de personnalisation par tenant (syndic) ?
- Architecture cote back2.0 : ou ca s'integre (hexagonal, port, adapter) ?

### Bloc 5 - Donnees [CRITIQUE]

- Quelles donnees alimentent l'IA en entree ?
- Sont-elles dans les bases Loji actuelles ou il faut les extraire ?
- Y a-t-il des donnees personnelles, sensibles, bancaires ?
- Le client a-t-il consenti a leur usage IA dans le contrat ?
- Faut-il un opt-in tenant par tenant ?
- Quel volume de donnees traite par mois ?

### Bloc 6 - Cout et ROI [IMPORTANT]

- Cout API estime par utilisateur actif / mois ?
- Cout total mensuel a iso-adoption / x10 adoption ?
- Refacture au client (forfait, surcout, gratuit) ?
- Quel ROI attendu (retention, churn evite, upsell, prix premium) ?
- Combien de temps avant break-even ?

### Bloc 7 - Risques [rappel court systematique]

- Que se passe-t-il si l'IA hallucine sur un cas critique (montants compta, droits locataires) ?
- Quel garde-fou (revue humaine, seuil de confiance, blocage) ?
- Quel kill switch pour desactiver la feature globalement en cas de derive ?
- Quel plan de communication si bug visible cote client ?
- RGPD : DPIA requise ?

### Bloc 8 - Mesure et arret [IMPORTANT]

- Quels KPIs surveille-t-on en pilote ? (utilisation, satisfaction, taux d'erreur, NPS)
- A partir de quelle valeur on continue / on arrete / on pivote ?
- Pendant combien de temps tient le pilote avant decision ?
- A-t-on un comparable interne / externe pour benchmarker ?

### Bloc 9 - Positionnement marche

- Genius Immo / Reemia AI ont-ils une feature equivalente ?
- En quoi notre version est differente ? (mieux integree au metier syndic, plus precise, plus ouverte)
- Est-ce un must-have de marche ou un differenciateur ?

## Pieges a eviter / signaux faibles a capter

- **"On lance, on verra apres"** : pas de criteres d'arret = derive budgetaire garantie
- **PM enthousiaste sans avoir parle a un seul utilisateur** : creuser la realite du besoin
- **"L'IA va remplacer le support"** : surevaluation classique, raisonner en assistance, pas remplacement
- **"On utilise GEMINI parce que c'est gratuit"** : verifier que ce n'est pas faux et que les CGU sont compatibles avec donnees client
- **Pas de DPIA evoquee sur donnees sensibles** : signal RGPD critique
- **Pas de mention du multi-tenant** : risque que le POC ne passe pas en prod
- **Latence non discutee** : sous-estimee, casse l'UX

## Livrables a produire APRES la reunion

Pour Raphael :
- Note de cadrage produit IA (modele Confluence)
- Matrice impact x faisabilite des options techniques
- Tableau de bord KPIs proposes
- Liste d'actions et responsables

Pour devs :
- Ticket Jira Epic + Stories (utiliser le skill `ticket-claude-code` pour les stories)
- Schema d'architecture (port hexagonal, adapter, dependances)

Pour direction :
- Synthese GO/NO GO 1 page (probleme, solution, cout, risque, KPIs, decision)

## Rappel RGPD / risques (court systematique)

Toute feature IA dans Loji touche potentiellement des donnees personnelles de copropriete / locataires. Reflexes obligatoires : base legale, minimisation, localisation des traitements (UE preferable), DPIA si donnees sensibles, registre des traitements a jour, mention dans CGU clients. Si LLM hors UE, prevoir clauses contractuelles types et information utilisateurs. Anthropic Claude EU : a verifier disponibilite et conditions au moment du cadrage.
