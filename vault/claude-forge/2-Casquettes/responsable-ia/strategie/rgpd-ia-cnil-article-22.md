---
aliases:
  - RGPD IA
  - Article 22 RGPD
  - CNIL IA
  - décision automatisée
  - DPIA IA
  - profilage RGPD
resume: RGPD + IA — Article 22 décision automatisée, DPIA Art 35, recommandations CNIL juillet 2025, projet PANAME, anonymisation, consolidation DPIA+FRIA pour scoring locataire Loji.
derniere-maj: 2026-05-25
tags:
  - "#type/cheatsheet"
  - "#domaine/conformité"
  - "#domaine/rgpd"
  - "#domaine/ia"
  - "#projet/neoteem"
  - "#casquette/responsable-ia"
---

# RGPD & IA — Article 22, DPIA, CNIL

## TL;DR

- **Article 22 RGPD** = droit à NE PAS faire l'objet d'une décision exclusivement automatisée produisant effets juridiques/significatifs.
- **Scoring locataire automatisé Loji = Article 22 frontal** → exceptions strictes + droit à intervention humaine + explication + contestation.
- **DPIA Art 35 obligatoire** dès profilage à grande échelle. À consolider avec FRIA AI Act en **1 document unique** pour Neoteem.
- **Recommandations CNIL juillet 2025** = grille pratique côté CNIL, complète CEPD déc 2024 (opinion modèles IA).
- **Projet PANAME (ANSSI + CNIL)** = framework évaluation anonymisation modèles IA, en cours 2026.

## Article 22 — Décision exclusivement automatisée

> *"La personne concernée a le droit de ne pas faire l'objet d'une décision fondée exclusivement sur un traitement automatisé, y compris le profilage, produisant des effets juridiques la concernant ou l'affectant de manière significative de façon similaire."*

### Conditions d'application

1. Décision **fondée exclusivement** sur traitement auto (humain rubber-stamping = compte comme auto)
2. **Effet juridique OU significatif similaire** (refus location = OUI significatif)
3. **Profilage** inclus explicitement

### 3 exceptions (Art 22.2)

| Exception | Détail | Applicable Neoteem ? |
|---|---|---|
| (a) **Nécessaire à un contrat** | Conclusion ou exécution contrat | Locataire candidat ≠ contrat conclu → fragile |
| (b) **Autorisée par droit UE/EM** | Avec mesures de protection | Pas de base légale spécifique scoring locataire FR |
| (c) **Consentement explicite** | Pas pré-coché, granulaire, retirable | Possible mais alourdit UX + droit de retrait |

**Verdict Neoteem** : exception (a) "exécution contrat" la plus défendable, MAIS jurisprudence CJUE SCHUFA (déc 2023) a restreint cette exception → **prudence + intervention humaine systématique recommandée**.

### Garanties obligatoires (Art 22.3)

Même si exception applicable :
- Droit à **intervention humaine** du responsable
- Droit d'**exprimer son point de vue**
- Droit de **contester la décision**
- Droit à une **explication** (logique sous-jacente, importance, conséquences — Art 13.2.f / 14.2.g / 15.1.h)

### Interdiction renforcée

Décisions Art 22 fondées sur **données sensibles Art 9** (santé, origine, opinions, etc.) → **interdites sauf consentement explicite OU intérêt public substantiel**.

## Arrêt CJUE SCHUFA (C-634/21, déc 2023)

- Le **scoring lui-même** est une "décision" Art 22 si la décision finale du tiers (banque, bailleur) **se fonde de manière déterminante** dessus.
- Conséquence : un score communiqué à un syndic qui s'en sert pour refuser = scoring lui-même soumis à Art 22.
- **Impact direct Loji** : ne pas se cacher derrière "c'est le syndic qui décide". Le scoring est attaquable.

## DPIA — Article 35 RGPD

### Obligatoire quand

| Cas | Détail |
|---|---|
| Évaluation systématique aspects personnels (profilage) | OUI scoring locataire |
| Traitement à grande échelle données sensibles | Si données financières/santé/historique judiciaire |
| Surveillance systématique zone accessible au public | N/A |
| **Liste CNIL** : profilage + décisions effets juridiques | OUI Neoteem |

### Contenu minimum DPIA (Art 35.7)

1. Description systématique du traitement (finalités, intérêts légitimes)
2. Évaluation nécessité + proportionnalité
3. Évaluation risques pour droits/libertés
4. Mesures envisagées pour atténuer

### Consolidation DPIA + FRIA (recommandé Neoteem)

Le FRIA (AI Act Art 27) ressemble fortement au DPIA. **CNIL et CEPD encouragent un document unique consolidé**.

Structure consolidée :
1. Description système IA + traitement données
2. Finalités + base légale RGPD + classification AI Act
3. Nature données + sources + qualité
4. Analyse nécessité/proportionnalité
5. Risques RGPD (droits personnes)
6. Risques droits fondamentaux (non-discrimination, dignité, recours)
7. Mesures techniques et organisationnelles
8. Consultation DPO + parties prenantes
9. Décision + signature responsable de traitement

## Recommandations CNIL — juillet 2025

Complète et finalise les guides "IA et RGPD" CNIL (premières versions 2023-2024). Couvre :

| Recommandation | Apport |
|---|---|
| Base légale développement IA | Intérêt légitime souvent défendable si tests 3-volets sérieux |
| Constitution datasets | Sources licites, minimisation, suppression données inutiles |
| Annotation/labellisation | Sous-traitance = Art 28 DPA obligatoire |
| Sécurité dev IA | OWASP LLM Top 10 référencé (cf [[../gouvernance/securite-llm-owasp]]) |
| Information personnes | Art 13/14 adaptés au cycle de vie IA |
| Modèles open-source / mise à disposition | Documentation type "model card" |
| Droits personnes (Art 15-22) | Modalités exercice + délais |

## CEPD — Opinion 28/2024 (déc 2024) sur modèles IA

3 questions traitées :
1. **Modèle IA = données personnelles ?** Pas toujours, mais souvent : risque d'identification résiduel → analyser cas par cas
2. **Intérêt légitime base légale développement ?** Possible, test 3-volets (intérêt / nécessité / balance)
3. **Conséquence si dev illicite ?** Le déploiement aval peut être contaminé

**Impact Neoteem** : si on fine-tune Mistral/Claude avec données locataires, faire un test 3-volets documenté + minimisation + opt-out.

## Projet PANAME (ANSSI + CNIL, 2025-2026)

Framework conjoint ANSSI/CNIL pour **évaluer le risque de ré-identification depuis un modèle IA**. Référence en cours de finalisation, à surveiller pour benchmarker l'anonymisation Loji.

## Anonymisation vs Pseudonymisation

| Critère | Anonymisation | Pseudonymisation |
|---|---|---|
| Définition | Données plus rattachables à personne | Données rattachables via info séparée (clé) |
| Statut RGPD | **Hors scope** | **Dans scope** (toujours données perso) |
| Critères CNIL/CEPD (3 cumulatifs) | Individualisation IMPOSSIBLE + corrélation + inférence | — |
| Pratique Neoteem | Très dur à prouver, presque jamais atteint | Standard recommandé (hash + sel + KMS) |

## Checklist conformité RGPD scoring locataire Loji

- [ ] Base légale identifiée (Art 6) + documentée
- [ ] Si Art 22 : exception identifiée + garanties (intervention humaine, explication, contestation)
- [ ] Information personnes Art 13/14 mise à jour (logique, importance, conséquences)
- [ ] DPIA + FRIA consolidées rédigées, signées DPO + Lead IA
- [ ] Registre des activités de traitement Art 30 à jour
- [ ] Sous-traitants (Anthropic, Mistral, GCP) DPA Art 28 + SCCs si transfert hors UE
- [ ] Durée conservation définie + purge automatisée
- [ ] Mécanisme exercice droits (Art 15-22) opérationnel <1 mois
- [ ] Procédure violation données (Art 33/34) — notification CNIL <72h
- [ ] Pseudonymisation appliquée par défaut (sel + KMS)
- [ ] AI literacy équipe (recoupement AI Act Art 4)

## Anti-patterns

- "On a un humain dans la boucle" → si rubber-stamping = considéré comme auto (CJUE SCHUFA)
- DPIA cosmétique sans consultation DPO → Art 35.2 exige consultation DPO
- "C'est du B2B, le RGPD c'est B2C" → **FAUX**, RGPD = personne physique, indépendamment du contexte business
- Conserver datasets training "au cas où" → minimisation Art 5.1.c
- Anonymisation = "j'ai enlevé le nom" → tests CNIL beaucoup plus stricts
- Confondre DPIA et FRIA et les faire 2 fois → consolider

## Sources

- RGPD texte : <https://eur-lex.europa.eu/eli/reg/2016/679/oj>
- CNIL — IA : <https://www.cnil.fr/fr/intelligence-artificielle>
- CNIL — recos IA 2025 : <https://www.cnil.fr/fr/intelligence-artificielle/lia-et-vous>
- CEPD Opinion 28/2024 : <https://www.edpb.europa.eu/our-work-tools/our-documents/opinion-board-art-64/opinion-282024-certain-data-protection-aspects_en>
- CJUE C-634/21 SCHUFA : <https://curia.europa.eu/juris/liste.jsf?num=C-634/21>
- PANAME ANSSI/CNIL : <https://www.cnil.fr/fr/projets-de-recherche/paname>

## Liens vault

- [[../index]] — casquette responsable-ia
- [[ai-act-eu-cheatsheet]] — règlement UE 2024/1689
- [[../gouvernance/ai-usage-policy-interne]] — politique interne
- [[../gouvernance/vendor-management-llm-dpa]] — DPA vendor LLM
