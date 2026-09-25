---
aliases:
  - comprendre-neoteem
  - neoteem-vue-responsable-ia
  - neoteem-strategie-produit
  - moat-neoteem-base-donnees
  - neoteem-ou-l-ia-cree-valeur
  - synthese-neoteem-loji
resume: Synthèse stratégique de Neoteem/Loji vue Responsable IA — architecture, domaines métier, le moat (base de données Loji), et où l'IA crée de la valeur. Source pour toute décision produit/roadmap IA.
derniere-maj: 2026-09-25
tags:
  - "#type/knowledge"
  - "#projet/neoteem"
  - "#casquette/responsable-ia"
  - "#domaine/strategie"
---
# Comprendre Neoteem — vue Responsable IA

> Synthèse construite depuis le vault neoteem-brain (MCP obsidian-brain, 29 mai 2026) pour outiller les décisions stratégiques IA. Le vault technique reste la source de vérité détaillée ; cette note est la lecture **stratégique** (où est la valeur, où brancher l'IA).

## Ce qu'est Neoteem en une phrase

Éditeur français d'un **ERP de gestion immobilière** (Loji) couvrant **syndic de copropriété + gérance locative + comptabilité**, en migration d'un legacy WinDev vers une stack full web. Direction : famille Trevisiol + Benjamin Mangani (repreneurs). ~20+ personnes, 3 îlots dev (Syndic / Gérance / Technique). Narjis Trevisiol = Support + Formation (consultants).

## Architecture (la chaîne)

```
lojii (Vue 3/Vuetify)  →  ws (Go)  →  PostgreSQL (toute la logique métier)
neo_ia (Python/LangGraph) → ia_back (TS/Bun/Hono) → mêmes fonctions PG
notification-proxy (Go, LISTEN/NOTIFY) → GED / mail / OCR / éditions
```

**Point capital** : **toute la logique métier vit dans PostgreSQL** (fonctions PG). 12 schémas : `web_service, ag, banque, comptabilite, proprietaire, suividossier, relance, dashboard, fournisseur, suivicopro, transco, ia`. Les apps ne font que router/formater. → L'IA (via ia_back, schéma `ia.`) a un accès structuré à cette logique.

## ⭐ LE MOAT — la base de données Loji (validé par Raphael 29 mai)

**L'IA est une commodité** (même Claude/GPT pour tous les concurrents). L'avantage inimitable de Neoteem = **les données réelles, vivantes, structurées** de la gestion immobilière de ses clients. Personne (Bellman, Genius, Gemini) ne peut les reproduire.

Cœur du modèle de données : **acteur universel + rôle** (`t_acteur` + `t_role`, **27 type_role × 98 type_fonction**). Un même contact porte plusieurs rôles (copropriétaire, locataire, propriétaire, fournisseur, garant, CAF, notaire, conseil syndical…). C'est ce graphe relationnel riche qui rend l'IA Neoteem non-générique.

Distinction importante (Raphael) : la **base de données Loji = le moat** (va aux clients, inimitable). Le **vault neoteem-brain 682 notes = accélérateur INTERNE** (aide l'équipe à construire, ne va PAS aux clients). Ne pas confondre les deux.

## Les domaines métier (où sont les douleurs = où l'IA crée de la valeur)

### Syndic de copropriété
Cycles lourds et répétitifs, candidats naturels à l'assistance IA :
- **ADF** (appels de fonds) — calcul QP 4 phases, validation 6 phases, SEPA, fonds travaux ALUR
- **Régularisation des charges** — 8 phases, rompus, solde 471 (douleur support récurrente)
- **AG** — convocation multi-canal, vote par correspondance, tenue VoRio, PV, **84 fonctions** — LA tâche chronophage du syndic
- **Mutations / état daté**, relances copropriétaires (5 niveaux amiable→contentieux), honoraires (3 modes), immatriculation (API gouv), sinistres MRI, OS mobilité

### Gérance locative
- **Quittancement / ADL** (9 étapes), **révision loyers** (IRL/ICC/ILAT + 7 plafonnements DPE/Pinel)
- **CRG** (compte rendu de gestion, fiscal 2044), **régularisation charges locatives**
- **Relance impayés** (lien GLI garantie loyers impayés) — touche à l'argent du client = argument de vente fort
- Commercialisation lots vacants (scoring candidats, signature Yousign), sortie locataire (EDL, décompte DG)

### Comptabilité
Lettrage (10 types), encaissement SEPA (pain.001/008), rapprochement bancaire auto (3 passes), TVA, clôture exercice, export Sage/CEGID/LDCOMPTA, OCR factures (Cloud Vision).

### Transversal — points de greffe IA directs
- **Module suivi-dossier** (`suividossier`, ~50 PS) : dossiers/tâches thématiques (AG, Travaux, Sortie locataire) avec **workflows, création auto d'actions, association mail↔tâche, publication extranet ciblée** (copro / locataire / propriétaire / CS). Lojii a déjà une structure de tâches → un agent IA peut s'y brancher.
- **Module mail** (messagerie intégrée, lien mail↔facture, module G-Suite/Gmail Lojii `extranet-neoteem.dendreo.com` pour la formation).
- **GED** (Google Drive, labellisation, Yousign), **OCR** (factures, scan chèques CMC7), **correspondance multi-canal**.

## Les apps IA existantes (neo_ia)

| App | Rôle | État |
|---|---|---|
| **NeoChat** | Chatbot multi-agents SSE : Universal, Support (RAG Confluence VERBATIM anti-hallucination + LLM-as-Judge), Web, Devis (BODACC/DTU/NF/RGE), Annonce (8 styles), Reformulation (4 types) | Pilote, **parké** en l'état (doublon barre recherche Loji) |
| **NeoMail** | Pipeline Gmail Pub/Sub → classif → brouillon. Règle **BROUILLON ONLY 5 niveaux** (oversight humain by design). 21 outils | Back OK, pas de front |
| **NeoDoc** | RAG documentaire (Vertex AI), tests DeepEval faithfulness ≥ 0.8 | Back OK, pas en prod |

Stack IA : LangGraph + Declarative ReAct Engine (AgentBlueprint), 2 bases PG (dbUsers checkpoints + dbVector pgvector), schémas isolés neochat/neodoc/neomail.

**Crédit IA responsable déjà en place** : BROUILLON ONLY (NeoMail) + extraction VERBATIM anti-hallucination (Support) + tests DeepEval (NeoDoc) = posture qualité/eval réelle, à valoriser face aux clients.

## Concurrents (benchmark mai 2026)

- **Bellman (Septeo)** : 70% emails 1 clic, groupe 3000 pers, Bpifrance, OpenAI
- **Genius Immo** : ~10 pers, chatbot + agent mail en prod, OpenAI, prix non public (≈49€/user annoncé). Insight Coprolab : « la connexion à une couche d'automatisation IA = critère de survie 2026 » → valide le moat Loji
- **Reemia (Foncia)** : Orion IDP 12M+ docs
- **Gemini dans Gmail** : menace gratuite, mais générique (pas d'accès données Loji)

## Implication stratégique (le fil rouge)

Prioriser les produits qui **exploitent la donnée Loji** (NeoMail contextualisé, agents métier branchés sur comptes/interventions/AG) plutôt que les produits génériques (chatbot qui double la recherche). La fenêtre est réelle mais temporaire : avantage tant que les éditeurs traditionnels n'ont pas rattrapé l'IA.

## Dossier stratégique IA — trilogie CODIR (livrée le 30 mai 2026)

Trois PDF dans `output/neoteem/`, générés avec la charte et la chaîne [[pdf-chrome-headless]] :

1. **Neoteem_Dossier_Strategique_IA_v2.pdf** — le *pourquoi* : diagnostic, benchmark, choix A/B, équipe valorisée sans chiffrage salarial.
2. **Neoteem_Roadmap_IA_v2.pdf** — le *quoi/quand* : catalogue d'idées, roadmap en deux colonnes (« à 2 » / « renforcé »), coût caché, NeoChat parqué. Rien qui mette Raphaël personnellement en avant.
3. **Neoteem_Modele_Economique_IA.pdf** — le *combien* : quatre modèles (usage, forfait, crédits, inclus), fourchettes à valider, revenus clients uniquement.

**Verdict tranché le 30 mai : choix binaire A ou B.** La séquence « B finance A » est abandonnée (risque de cannibalisation ; les clients ont déjà ChatGPT et des MCP moins chers). Le dossier recommande B, en le disant, et écrit trois dangers noir sur blanc :

- les clients ont déjà ChatGPT : un agent qui n'est pas meilleur décrédibilise Neoteem, donc uniquement de l'IA branchée sur Loji ;
- un MCP ouvert tue les produits ;
- le retard concurrentiel.

Avis de fond, dans l'encadré « sans filtre » du mot de la fin : le facteur décisif n'est ni A ni B, c'est la vitesse de décision et le changement d'organisation. La roadmap correspond au scénario A ; les usages internes valent pour A comme pour B.

**Trous identifiés le 29 mai** (niveau « grand Responsable IA ») :
1. aucun chiffre de valeur client réel ;
2. gouvernance des données et RGPD ;
3. vélocité de la concurrence non datée ;
4. pas de KPI de succès ni de condition de pivot ;
5. moat pas assez central.

Les sections KPI de succès, IA responsable / données et moat étaient en cours d'ajout le 29 mai (trous 2, 4 et 5). Le trou n°1 reste ouvert.

**TODO (reporté par Raphaël)** : trame d'interview client, 5-6 questions posées à 2-3 syndics, pour obtenir la vraie donnée de valeur (trou n°1). Canal privilégié : le Club Utilisateurs (voir plus bas).

## Liens

- [[lojii]] — frontend, architecture full web
- [[ai-act-eu-cheatsheet]] — si « Loji Scoring » commercialisé → Neoteem devient Provider AI Act
- [[strategie-ia]] — hub stratégie/gouvernance Responsable IA
- [[reunion-kit-de-decision-autonome]] — format de présentation de la trilogie à la direction
- [[pdf-chrome-headless]] — chaîne PDF + charte Neoteem


## Découvertes web (29 mai 2026) — marché & utilisateurs Loji

### Image & positionnement Loji (sources : ANGC, monimmeuble, comparatifs)
- **8M€ CA**, **4,17/5 ergonomie** (top 3 ANGC 2024), « solution à la mode », candidat **leader cabinets moyens/grands** (vs ICS Spirit, Immopen, TIMCI).
- Forces reconnues : migration de données (équipe dédiée, cas complexes avec historique), **30+ API**, comptabilité d'engagement solide.
- **Club Utilisateurs Neoteem** (échange annuel client↔Neoteem, propositions d'évolutions) = **canal idéal pour cadrer les besoins IA et obtenir la donnée client réelle** (au lieu d'interviews à monter de zéro).
- ⚠️ Critique négative historique : « commercialisé en cours de dev, modules KO (AG, correspondance, compta), 20-30s/clic ». = même pattern que le dossier dénonce (sortir trop tôt). Argument : l'IA ne doit pas répéter ça → preuve avant déploiement large.

### Tâches chronophages syndic (marché 2026, sources : Facilogi, monimmeuble, ESPI2R)
Confirment les priorités produit, avec chiffres citables :
1. **Mails entrants** (dizaines-centaines/jour) — tri par typologie (sinistre, travaux, compta, conflit)
2. **Admin répétitif** — rédaction emails, CR de visite, ordres du jour AG
3. **Financier** — appels de charges, suivi paiements
4. **Sinistres** — déclarations, échanges assurances (cauchemar admin)
5. **Documents** — factures, devis, contrats (OCR)

Gains marché mesurés (citables, sourcés) : prélèvements « matinée → <15 min » ; factures « **−75%** temps » ; charge admin « **−40%** ». 

### Concurrents IA spécialisés émergents (fenêtre datée)
- **Keyzia, SyndicInboxAI** (dédié tri mails !), **Bellman** — l'IA syndic se spécialise vite. SyndicInboxAI sur le créneau mail = concurrent direct de NeoMail. La fenêtre se referme.

### Implications roadmap (29 mai)
- **NeoMail** : statut réel = **en cadrage** (pas back-OK-simple). Vraie question à trancher avec clients : veulent-ils leur base SQL branchée, ou Gemini natif suffit ? Beaucoup de dev passé fait « parce qu'on a dit de développer » sans valider le besoin (comme NeoChat). → Cadrage client AVANT d'investir.
- **Chatbot support** : existe déjà MAIS (a) ne crée pas de tickets, (b) documentation incomplète. Chantier réel = ajouter création de tickets + optimiser rédaction/structuration de la doc support.
- **Skills par équipe** : plus complexe que « 1-2 pilotes » — skills par développeur, par syndic, par métier. À reformuler.
- **Skill PO tickets** : angle = générer épiques/tickets structurés → exploitables par Claude → docs auto derrière (PAS un outil perso Raphael).
- **Agents** = type NeoIA existant : comparateur de devis, rédaction annonces immobilières. C'est ce gabarit d'agent à mettre dans Loji.
