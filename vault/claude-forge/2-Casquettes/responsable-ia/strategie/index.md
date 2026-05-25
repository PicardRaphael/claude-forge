---
aliases:
  - strategie-ia
  - ai-strategy
  - hub-strategie
  - strategy-ia-neoteem
  - ai-governance
resume: Hub stratégie IA & gouvernance — AI Act EU, NIST AI RMF, ISO 42001, RGPD, AI Usage Policy, Build vs Buy, ROI IA, AI Council, sécurité OWASP LLM.
derniere-maj: 2026-05-25
tags:
  - "#type/index"
  - "#casquette/responsable-ia"
  - "#domaine/strategie"
  - "#domaine/gouvernance"
---

# Stratégie IA & gouvernance — hub

## TL;DR pour Neoteem (proptech FR scale-up)

1. **Vous êtes très probablement en haut risque AI Act** (Annexe III.5(a) — scoring locataire). Date clé : **2 août 2026** (potentiellement reportée à dec 2027 via Digital Omnibus AI).
2. **AI literacy obligatoire depuis février 2025** — vous êtes déjà en retard si pas formalisée.
3. **FRIA + DPIA consolidée obligatoire** pour scoring locataire. Sanction : 15 M€ ou 3% CA.
4. **75% des projets IA n'atteignent pas leur ROI attendu** (IBM). Seulement 5,5% des orgas tirent >5% EBIT de l'IA (McKinsey).
5. **Politique IA interne (AI AUP) URGENT** — Shadow AI est partout, cas Samsung 2023.

## Les 14 sujets canoniques

| Sujet | Note atomique | Source |
|---|---|---|
| AI Act EU (cheatsheet) | [[ai-act-eu-cheatsheet]] | EU Reg 2024/1689 |
| NIST AI RMF 1.0 | [[nist-ai-rmf-govern-map-measure-manage]] | NIST |
| ISO/IEC 42001:2023 | [[iso-42001-aims]] | ISO |
| RGPD & IA — CNIL | [[rgpd-ia-cnil-article-22]] | CNIL juillet 2025 |
| AI Usage Policy interne | [[ai-usage-policy-interne]] | Samsung 2023 lesson |
| Build vs Buy vs Fine-tune vs RAG | [[build-vs-buy-vs-finetune-rag]] | Menlo, TCO 2026 |
| ROI IA — mesure honnête | [[roi-ia-mesure-mckinsey]] | McKinsey State of AI |
| Roadmap IA & maturity | [[roadmap-ia-gartner-maturity]] | Gartner, Andrew Ng |
| Mistral & souveraineté FR | [[mistral-souverainete-francaise]] | Introl, Maddyness |
| Éthique IA (biais, explainability) | [[ethique-ia-fairness-model-cards]] | Mitchell, Gebru |
| Sécurité OWASP LLM | [[securite-llm-owasp-mitre-atlas]] | OWASP, MITRE |
| Vendor management LLM | [[vendor-management-llm-dpa]] | TrueFoundry |
| AI Council interne | [[ai-council-charter-composition]] | OneTrust, Deloitte |
| Communication CODIR IA | [[../communication/index]] | Cassie Kozyrkov, Mollick |

## AI Act EU — timeline critique

| Date | Obligation |
|---|---|
| 2 février 2025 | Interdictions (8 pratiques) + **AI literacy salariés OBLIGATOIRE** |
| 2 août 2025 | GPAI + autorités nationales + sanctions actives |
| **2 août 2026** | **Systèmes haut risque Annexe III — date clé Neoteem** |
| 2 août 2027 | GPAI pré-2025 + systèmes Annexe I |

⚠️ Digital Omnibus AI (accord politique 7 mai 2026) : potentiel report Annexe III à 2 décembre 2027.

### Classification 4 niveaux
1. **Inacceptable** : social scoring, manipulation subliminale (interdits)
2. **Haut risque** : Annexe III (8 catégories) — **scoring locataire = III.5(a)**
3. **Risque limité** : chatbots, deepfakes (transparence)
4. **Risque minimal** : pas d'obligation

### Sanctions
- Pratiques interdites : **35 M€ ou 7% CA mondial**
- Haut risque : 15 M€ ou 3%
- Info trompeuse : 7,5 M€ ou 1%
- Caps proportionnés PME/startups

### Obligations Deployer Neoteem (si haut risque)
- **FRIA** (Fundamental Rights Impact Assessment) — peut consolider avec DPIA RGPD
- Logs automatiques minimum 6 mois
- Oversight humain documenté
- Information des personnes affectées

## NIST AI RMF 1.0 — la grammaire

**4 fonctions** : GOVERN (transverse, culture, politiques) / MAP (contextualiser) / MEASURE (métriques) / MANAGE (mitiger, accepter risque résiduel).

Volontaire, US, mais **standard de facto** mondial. S'aligne ISO 42001 et AI Act sans conflit.

## Build vs Buy — matrice décision Neoteem

| Approche | Cas idéal | Verdict Neoteem |
|---|---|---|
| **Build from scratch** | Hyperscaler | NON. Hors capacité scale-up |
| **Buy (API/SaaS)** | Time-to-market | DEFAULT pour MVP |
| **Fine-tune** | Style, tone | Si volumétrie 100k+ req/mois |
| **RAG** | Connaissance dynamique | **OBLIGATOIRE proptech** (bases biens, baux) |
| **Hybride RAG + Fine-tune** | Production scale | **Cible 12-24 mois** |

Menlo Ventures 2024 : 51% déploiements enterprise utilisent RAG, 9% fine-tuning seul.

## Souveraineté française — angle Mistral

Pour proptech FR :
- Hébergeable on-prem ou OVHcloud/Scaleway **SecNumCloud**
- Immunité Cloud Act (vs OpenAI/Anthropic/Google)
- Bpifrance dans capital (clause 20% max)
- Trade-off : Mistral derrière GPT-5/Claude 4.7 sur benchmarks complexes mais OK pour RAG/scoring

## ROI IA — chiffres clés à connaître

- **88%** des orgas utilisent l'IA dans au moins une fonction
- **39%** rapportent un impact EBIT mesurable
- **5,5%** seulement ("High Performers") tirent >5% EBIT
- **75%** des projets IA n'atteignent pas leur ROI (IBM)

### Patterns des High Performers (3)
1. **Transformation > efficacité** (3,6× plus susceptibles)
2. **Sponsorship CEO** (3× plus de leadership senior engagé)
3. **Re-design de workflows** (55% redessinent fondamentalement)

## AI Council Neoteem (composition recommandée)

Pour scale-up 5-50 personnes :
- **Sponsor exec** : CEO ou COO
- **Lead IA** : Raphael (toi)
- **Legal/DPO** : conformité RGPD + AI Act
- **Security/CISO** : OWASP LLM
- **Business owner** : représentant produit/ops par rotation

À 5 pers Neoteem : **3 personnes core** suffit + consultants externes ponctuels.

### Mandat (charter à formaliser)
1. Valider cas d'usage IA avant lancement (go/no-go)
2. Approuver classification risque AI Act
3. Réviser KPIs et incidents mensuellement
4. Approuver nouveaux vendors LLM
5. Escalader CODIR décisions structurantes (>50k€, haut risque)
6. Maintenir inventaire AI + DPIA/FRIA

**Cadence** : bi-mensuelle 30 min opérationnel + trimestriel 1h stratégique.

## Synthèse opérationnelle — 6 prochains mois pour Raphael

| Mois | Livrable |
|---|---|
| M1 | Inventaire AI + classification AI Act + AI Acceptable Use Policy v1 |
| M2 | AI Council charter + 1ère réunion + DPIA/FRIA scoring locataire |
| M3 | Vendor due diligence (Mistral vs Anthropic vs OpenAI) + Model Cards prio 1 |
| M4 | Roadmap IA priorisée (matrice valeur/risque) + dashboard CODIR v1 |
| M5 | Red team OWASP sur cas d'usage haut risque + plan AI literacy salariés |
| M6 | Bilan KPIs Q1-Q2 + arbitrage build/buy/RAG + budget 2027 |

## 3 pièges à éviter immédiatement

1. **Sous-estimer AI literacy** — obligation février 2025
2. **Lancer scoring locataire sans FRIA + DPIA** — risque 15 M€ ou 3% CA
3. **Promettre ROI EBIT au CODIR avant 12 mois** — seuls 5,5% y arrivent

## Sources clés

- [EU AI Act Service Desk — Annex III](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3)
- [Trilateral Research — Timeline 2025-2027](https://trilateralresearch.com/responsible-ai/eu-ai-act-implementation-timeline-mapping-your-models-to-the-new-risk-tiers)
- [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/)
- [ISO/IEC 42001:2023](https://www.iso.org/standard/42001)
- [CNIL — Recommandations IA juillet 2025](https://www.cnil.fr/fr/ia-finalisation-recommandations-developpement-des-systemes-ia)
- [OWASP Top 10 LLM v2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [McKinsey State of AI 2025](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)
- [Stanford HAI AI Index 2025](https://hai.stanford.edu/ai-index/2025-ai-index-report)
- [Andrew Ng — AI Transformation Playbook](https://medium.com/@andrewng/introducing-the-ai-transformation-playbook-58ccad4393e9)
- [Strac — AI AUP Template 2026](https://www.strac.io/blog/ai-acceptable-use-policy-template)
