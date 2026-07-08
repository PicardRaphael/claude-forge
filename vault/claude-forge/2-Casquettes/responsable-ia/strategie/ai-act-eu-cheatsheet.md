---
aliases:
  - ai-act
  - règlement IA UE
  - EU AI Act
  - 2024/1689
  - AI Act cheatsheet
  - règlement européen IA
resume: Cheatsheet AI Act UE 2024/1689 — timeline, classification 4 niveaux, Annexe III haut risque (focus scoring locataire III.5(a)), sanctions, obligations Provider vs Deployer pour Neoteem.
derniere-maj: 2026-05-25
tags:
  - "#type/cheatsheet"
  - "#domaine/conformite"
  - "#domaine/ia"
  - "#projet/neoteem"
  - "#casquette/responsable-ia"
---

# AI Act EU — Cheatsheet

## TL;DR

- Règlement UE **2024/1689** entré en vigueur **1er août 2024**, application progressive jusqu'à août 2027.
- **Date clé Neoteem : 2 août 2026** — obligations systèmes haut risque (Annexe III) entrent en vigueur.
- **Scoring locataire = Annexe III.5(a)** creditworthiness/credit score → haut risque par défaut, sauf exception profilage qui RECLASSE automatiquement en haut risque.
- Sanctions jusqu'à **35M€ ou 7% CA mondial**. PME = caps réduits mais EXISTENT.
- **Digital Omnibus AI (mai 2026)** : Commission propose report Annexe III à **décembre 2027** — surveiller, ne pas miser dessus.

## Timeline d'application

| Date | Ce qui s'applique | Impact Neoteem |
|---|---|---|
| **1 août 2024** | Entrée en vigueur | — |
| **2 février 2025** | Pratiques interdites (Art 5) + **AI literacy obligation** (Art 4) | Former équipe + utilisateurs Loji |
| **2 août 2025** | Règles GPAI (modèles fondation) + gouvernance + sanctions GPAI | Anthropic/Mistral = leur problème, mais doc requise |
| **2 août 2026** | **Systèmes haut risque Annexe III + transparence Art 50** | **Scoring locataire = DEADLINE DURE** |
| 2 août 2027 | Annexe I (haut risque "produits régulés" — jouets, machines, dispositifs médicaux) | Hors scope Neoteem |
| dec 2027 (potentiel) | Si Digital Omnibus AI adopté : report Annexe III | À surveiller mensuellement |

## Classification 4 niveaux

```
┌─────────────────────────────────────────────────────────┐
│ 1. RISQUE INACCEPTABLE (Art 5) — INTERDIT               │
│    Social scoring, manipulation, biométrie temps réel   │
├─────────────────────────────────────────────────────────┤
│ 2. HAUT RISQUE (Annexe I + III) — Conformité lourde     │
│    Scoring crédit, RH, éducation, justice, infra crit.  │
├─────────────────────────────────────────────────────────┤
│ 3. RISQUE LIMITÉ (Art 50) — Transparence                │
│    Chatbots, deepfakes, contenu généré → étiquetage     │
├─────────────────────────────────────────────────────────┤
│ 4. RISQUE MINIMAL — Aucune obligation                   │
│    Filtres spam, recommandation produits non sensibles  │
└─────────────────────────────────────────────────────────┘
```

## Annexe III — 8 catégories haut risque

| # | Catégorie | Exemples |
|---|---|---|
| III.1 | Biométrie | Identification à distance, catégorisation, reconnaissance émotion |
| III.2 | Infrastructures critiques | Eau, gaz, électricité, trafic |
| III.3 | Éducation/formation | Admission, notation, détection triche |
| III.4 | Emploi/RH | Tri CV, monitoring, évaluation perf |
| **III.5** | **Accès services essentiels** | **(a) Solvabilité/credit scoring**, (b) prestations publiques, (c) urgences, (d) assurance vie/santé |
| III.6 | Forces de l'ordre | Évaluation risque criminel, polygraphe |
| III.7 | Migration/asile | Évaluation risque sécurité, examen demandes |
| III.8 | Justice/démocratie | Aide juridictionnelle, élections |

### Focus Neoteem — III.5(a) creditworthiness

**Texte exact** : *"AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score, with the exception of AI systems used for the purpose of detecting financial fraud."*

→ **Scoring locataire dans Loji** = creditworthiness évaluation → **haut risque Annexe III.5(a)**.

→ Même si on argue "ce n'est pas du crédit bancaire", la clause **profilage** (Art 6.3 dernier alinéa) reclasse automatiquement TOUT système qui fait du profilage de personnes physiques en haut risque, même si on tente l'exception "tâche purement préparatoire".

## Obligations haut risque (Art 8-15)

| Obligation | Détail |
|---|---|
| Système de gestion des risques | Identifier, évaluer, atténuer risques sur durée vie |
| Gouvernance des données | Représentativité, qualité, biais, traçabilité datasets |
| Documentation technique | Avant mise sur marché (Annexe IV) |
| Logs automatiques | Conservation, traçabilité décisions |
| Transparence utilisateurs | Notice utilisation, capacités/limites |
| Supervision humaine | Art 14 — humain peut intervenir, override |
| Robustesse/précision/cybersécurité | Tests, monitoring, métriques |
| Système qualité (Provider) | Art 17 — politiques + procédures |
| Évaluation conformité | Avant mise sur marché (CE marking) |
| Enregistrement EU database | Avant mise sur marché |
| FRIA (Deployer public + privé sensible) | Art 27 — Fundamental Rights Impact Assessment |

## Provider vs Deployer

| Rôle | Définition | Neoteem |
|---|---|---|
| **Provider** | Développe le système IA ou le fait développer ET le met sur le marché sous son nom | **OUI si Neoteem construit scoring locataire en interne** → toutes obligations Art 8-15 |
| **Deployer** | Utilise un système IA sous son autorité (sauf usage perso non pro) | **OUI si Neoteem embarque un scoring tiers** → obligations Art 26 (supervision humaine, FRIA, logs, monitoring) |
| Importer / Distributor | Met sur marché UE un système d'un Provider non-UE / met à disposition | N/A |

**Piège** : si tu fine-tunes un modèle haut risque tiers et le commercialises sous "Loji Scoring", **tu deviens Provider** (Art 25). Cas typique de "fine-tune Mistral pour scoring" → Neoteem assume tout.

## Sanctions (Art 99)

| Infraction | Plafond entreprise | Plafond PME (le plus bas s'applique) |
|---|---|---|
| Pratiques interdites Art 5 | 35M€ ou 7% CA mondial | 7% CA mondial |
| Non-conformité haut risque, GPAI, transparence | 15M€ ou 3% CA mondial | 3% CA mondial |
| Info incorrecte autorités | 7,5M€ ou 1% CA mondial | 1% CA mondial |

**PME** = caps "le plus bas des deux" (Art 99.6) — protection mais pas immunité.

## Checklist conformité haut risque Neoteem (scoring locataire)

- [ ] Classification documentée : III.5(a) + clause profilage
- [ ] Provider ou Deployer ? (décidé + tracé)
- [ ] Système de gestion des risques formalisé (doc)
- [ ] Data governance : représentativité datasets, biais, sources légales
- [ ] Documentation technique Annexe IV à jour
- [ ] Logs automatiques (rétention min 6 mois, recommandé 12)
- [ ] Notice utilisateur (syndic/gérant) — capacités/limites
- [ ] Supervision humaine effective (pas rubber-stamping)
- [ ] FRIA réalisée AVANT mise en service (consolidée avec DPIA RGPD)
- [ ] Enregistrement EU database AI Act
- [ ] CE marking (auto-évaluation possible pour Annexe III, sauf biométrie III.1.a)
- [ ] Post-market monitoring + incident reporting
- [ ] Procédure réclamation usagers/locataires
- [ ] AI literacy équipe + utilisateurs Loji (depuis fév 2025)

## Anti-patterns

- "On est SaaS B2B, l'AI Act c'est pour le grand public" → **FAUX**. Le règlement s'applique au système, pas au modèle business.
- "On utilise Claude/Mistral, c'est leur problème" → **FAUX**. Tu es Deployer (min) ou Provider (si tu reconfigures).
- "Scoring locataire ≠ scoring bancaire" → **FAUX**. La Commission a clarifié : toute solvabilité personne physique compte.
- Attendre 2 août 2026 pour commencer → **FAUX**. La doc technique + datasets + FRIA prennent 6-12 mois.
- Confondre AI Act (produit) et RGPD (données personnelles) → cumul obligatoire. Voir [[rgpd-ia-cnil-article-22]].

## Sources

- Règlement UE 2024/1689 : <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>
- AI Act Explorer (Future of Life Institute) : <https://artificialintelligenceact.eu/>
- Annexe III détaillée : <https://artificialintelligenceact.eu/annex/3/>
- Commission EU AI Office : <https://digital-strategy.ec.europa.eu/en/policies/ai-office>
- CNIL — IA et RGPD : <https://www.cnil.fr/fr/intelligence-artificielle>

## Liens vault

- [[../index]] — casquette responsable-ia
- [[rgpd-ia-cnil-article-22]] — DPIA + Article 22
- ai-usage-policy-interne — politique interne usage IA
- ai-council-charter-composition — gouvernance interne
