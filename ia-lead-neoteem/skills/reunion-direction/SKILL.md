---
name: reunion-direction-neoteem
description: Aide Raphael (Responsable IA Neoteem) a preparer une reunion avec la direction sur la strategie IA. A declencher des qu'il mentionne "reunion direction", "comite de direction", "codir", "objectifs IA", "strategie IA", "budget IA", "OKR IA", "roadmap IA", ou demande des questions a poser au CEO/CTO/COO sur l'IA. Couvre cadrage strategique, ambition, budget, ROI, risques, gouvernance. Produit ordre du jour, questions a poser, points d'attention, livrables a apporter. Reunion cible 1h-1h30. Contexte : Loji (ERP SaaS pour syndics et gerance locative).
---

# Preparation reunion direction Neoteem - Strategie IA

Tu aides Raphael a preparer une reunion avec la direction de Neoteem sur la strategie IA. Cible : 1h-1h30, format dense.

## Contexte ancre

- Neoteem edite **Loji** (ERP AI-native pour syndics et gerance locative)
- Concurrents directs : Genius Immo, Reemia AI
- Briques IA existantes dans Loji : NeoChat, NeoDocs, integration GEMINI
- Outillage interne IA : Claude Code, Cowork, MCP Atlassian, neoteem-brain (Obsidian vault)
- Equipe transverse : dev, design, devops, redaction, support, QA, commercial

## Avant la reunion - questions a Raphael

Si Raphael n'a pas precise, demande-lui d'abord :

1. **Qui sera dans la salle ?** (CEO, CTO, COO, CFO, fondateurs, board ?)
2. **Sujet declencheur ?** (revue trimestrielle, budget annee N+1, reaction a un concurrent, levee, demande client ?)
3. **Niveau de maturite IA percu par la direction ?** (techno gadget / avantage competitif / pivot strategique ?)
4. **Decision attendue en sortie ?** (validation budget, arbitrage roadmap, recrutement, partenariat ?)

Si une seule de ces reponses est floue, prepare des **variantes** d'ordre du jour.

## Structure d'ordre du jour (a adapter)

```
1. Etat des lieux IA Neoteem - 10 min
   - Briques IA en production (NeoChat, NeoDocs, GEMINI)
   - Adoption interne et externe (chiffres)
   - Couts actuels (API, infra, RH)

2. Position concurrentielle - 10 min
   - Genius Immo, Reemia AI : ou sont-ils ?
   - Notre differenciation (AI-native, ancrage metier syndic)
   - Risque de retard / d'ecart

3. Strategie IA proposee (12-18 mois) - 25 min
   - 3 piliers : productivite interne / valeur produit Loji / nouveaux revenus
   - Roadmap macro (T+3, T+6, T+12 mois)
   - Make or buy par brique

4. Ressources et budget - 15 min
   - Equipe IA cible (recrutements, montee en competence)
   - Budget API et infra (scenarios bas/median/haut)
   - Investissements outillage (Claude Code, neoteem-brain, MCP)

5. Risques et gouvernance - 10 min
   - RGPD (donnees EU copropriete, locataires)
   - Dependance Anthropic / Google / OpenAI
   - Dette IA, hallucinations, biais
   - Comite IA propose

6. Decisions et arbitrages - 10 min
   - Ce qu'on lance / ce qu'on stoppe
   - Budget vote ou a re-arbitrer
   - Prochains jalons
```

## Questions a poser - par bloc

### Bloc 1 - Ambition strategique [CRITIQUE en premiere reunion]

- D'ici 18 mois, Loji est-il "un ERP avec de l'IA" ou "un produit qui ne peut pas exister sans IA" ?
- Acceptons-nous de degrader temporairement certaines fonctions metier pour accelerer l'IA ?
- Quelle part du CA 2027 doit venir de fonctions IA exclusives ?
- Sommes-nous prets a perdre des clients qui refusent l'IA dans leur ERP ?
- A quel moment l'IA devient-elle un argument de vente principal vs un confort ?

### Bloc 2 - Positionnement vs concurrence

- Genius Immo et Reemia AI : on les copie, on les contourne, on les ignore ?
- Avons-nous une fenetre de tir (12-18 mois) ou est-on deja en retard ?
- Sur quelle brique IA acceptons-nous d'etre 2e ou 3e du marche ?
- Un client important nous a-t-il deja demande une fonction IA qu'on n'a pas ?

### Bloc 3 - Make or buy [IMPORTANT]

- Quelles briques DOIT-ON construire (differenciation metier) vs INTEGRER (Anthropic, Google) ?
- Acceptons-nous d'etre dependants d'un seul provider de LLM ?
- Faut-il investir dans du fine-tuning, ou les modeles generiques + RAG suffisent ?
- Combien de mois acceptons-nous d'investir avant ROI mesurable ?

### Bloc 4 - Equipe et organisation [IMPORTANT]

- L'IA est-elle une fonction transverse (mon poste actuel) ou une BU ?
- Mon equipe (dev/design/devops/redac) doit-elle 100% basculer IA ou rester mixte ?
- Recrutons-nous un AI Engineer dedie, ou montons-nous en competence en interne ?
- Le formateur IA en interne (moi) doit-il toucher 100% des collaborateurs ?

### Bloc 5 - Budget et ROI [CRITIQUE]

- Quelle enveloppe API / infra IA pour 2027 ? (scenarios bas/median/haut)
- Quels KPIs definissent un succes vs un echec d'investissement IA ?
- Acceptons-nous un retour sur investissement sous 18-24 mois ?
- A partir de quel cout par requete une fonction devient non rentable ?
- Comment refacturons-nous l'IA aux clients (forfait, conso, prix unique) ?

### Bloc 6 - Risques [rappel court systematique]

- RGPD : nos donnees clients (copropriete, locataires) peuvent-elles transiter par les USA ?
- Avons-nous une clause IA dans les contrats clients existants ?
- Que se passe-t-il si Anthropic / Google augmente ses prix de 3x ?
- Avons-nous un kill switch si une fonction IA derape (hallucination critique sur un compte syndic) ?

### Bloc 7 - Decisions concretes en sortie [CRITIQUE]

- Quelle est LA decision a prendre aujourd'hui ?
- Si on ne tranche pas, quelles sont les consequences a 3 mois ?
- Qui sponsorise officiellement le programme IA cote direction ?
- Quand est la prochaine revue strategique IA ?

## Pieges a eviter / signaux faibles a capter

- **Direction qui dit "fais ce que tu veux sur l'IA"** : c'est un piege, sans sponsor explicite, le programme s'enlisera
- **Demande de ROI a 3 mois** : signal d'un manque de comprehension de la maturite IA, recadrer
- **"On veut faire comme Genius Immo"** : verifier qu'ils savent ce que fait reellement Genius Immo
- **Silence sur le RGPD** : ce n'est jamais un non-sujet, c'est un sujet refoule
- **Enthousiasme massif sans question critique** : signal de bulle d'enthousiasme, prevoir un rappel a froid

## Livrables a apporter en reunion

- Tableau de bord 1 page : briques en prod, adoption, couts
- Carte concurrentielle (Genius Immo, Reemia AI) 1 slide
- Roadmap IA macro (T+3/6/12 mois) 1 slide
- Scenarios budget (bas/median/haut) 1 slide
- Matrice risques RGPD / techno / financier 1 slide

## Livrables a produire APRES la reunion

- Compte-rendu structure (decisions / actions / responsables / echeances)
- Mise a jour du document strategie IA dans neoteem-brain
- Tickets Jira pour les actions concretes (utiliser le skill `ticket-claude-code` si tickets pour devs)

## Rappel RGPD / risques (court systematique)

Loji manipule des donnees personnelles de copropriete et de locataires (donnees identifiantes, parfois bancaires). Toute fonction IA doit etre cadree RGPD avant production : base legale, minimisation, localisation des donnees, droit a l'oubli, registre des traitements. A challenger systematiquement en reunion direction.
