---
aliases:
  - gouvernance-ia
  - hub-gouvernance
  - ai-governance-neoteem
  - compliance-ia
  - regulatory-ia
resume: Hub gouvernance IA — conformité AI Act EU, NIST RMF, RGPD/CNIL, sécurité OWASP LLM Top 10, MITRE ATLAS, red teaming, vendor management, AI Council.
derniere-maj: 2026-05-25
tags:
  - "#type/index"
  - "#casquette/responsable-ia"
  - "#domaine/gouvernance"
  - "#domaine/securite"
---

# Gouvernance IA — hub

Cette section recouvre la **dimension réglementaire et sécurité** de la stratégie IA. Le hub stratégique général est dans [[../strategie/index]].

## Les piliers

| Pilier | Détails dans | Source |
|---|---|---|
| AI Act EU (classification, FRIA) | [[../strategie/index]] | EU Reg 2024/1689 |
| RGPD & IA (art. 22, DPIA) | [[../strategie/index]] | CNIL juillet 2025 |
| NIST AI RMF 1.0 | [[../strategie/index]] | NIST |
| ISO/IEC 42001:2023 | [[../strategie/index]] | ISO |
| **Sécurité OWASP LLM Top 10** | [[securite-llm-owasp]] | OWASP |
| **MITRE ATLAS** | [[mitre-atlas-ml-threat]] | MITRE |
| **Red teaming LLM** | [[red-teaming-llm-promptfoo]] | Promptfoo, Garak |
| **Vendor management LLM** | [[vendor-management-llm-dpa]] | TrueFoundry |
| **AI Council interne** | [[../strategie/index]] | OneTrust, Deloitte |
| **AI Acceptable Use Policy** | [[ai-usage-policy-interne]] | Strac, Samsung 2023 |

## OWASP Top 10 for LLM Applications (2025)

Risques majeurs en production :

| # | Risque | Description |
|---|---|---|
| LLM01 | **Prompt Injection** (direct + indirect) | #1 attaque |
| LLM02 | **Sensitive Information Disclosure** | PII leak, secrets |
| LLM03 | **Supply Chain** | Modèles ou datasets compromis |
| LLM04 | **Data and Model Poisoning** | Training data corrompue |
| LLM05 | **Improper Output Handling** | XSS, SSRF via output LLM |
| LLM06 | **Excessive Agency** | Agents avec trop de permissions |
| LLM07 | **System Prompt Leakage** | Exposition prompt système |
| LLM08 | **Vector and Embedding Weaknesses** | Attaques sur vector store |
| LLM09 | **Misinformation** | Hallucinations |
| LLM10 | **Unbounded Consumption** | DoS, cost runaway |

## MITRE ATLAS

Framework ATT&CK pour ML/IA. OWASP map les attaques à ATLAS :
- AML.T0051 pour prompt injection
- AML.T0054 pour jailbreak

Utiliser pour modéliser les menaces sur tes systèmes Neoteem.

## Red teaming — outils

| Outil | Usage |
|---|---|
| **Promptfoo** | Open source, listé par OWASP |
| **DeepTeam** | Confident AI |
| **Garak** | NVIDIA, scan vulnérabilités LLM |

**Cadence** : tests réguliers + régression après chaque changement de system prompt.

## Vendor management LLM — checklist achat

| Critère | Question à poser |
|---|---|
| **DPA Art. 28 RGPD** | Signé, avec SCCs si transfert hors EU |
| **Training opt-out** | Off by default ? (Anthropic ✅, OpenAI = opt-out, Mistral ✅) |
| **Data residency** | EU only ? Zero Data Retention dispo ? |
| **Retention** | Combien de jours ? (Anthropic 7j depuis sept 2025) |
| **Certifs** | SOC 2 Type II + ISO 27001 minimum. ISO 42001 = bonus 2026 |
| **Audit logs** | API access logs + admin actions |
| **Incident SLA** | Notification breach < 72h (RGPD) |
| **Sub-processors** | Liste exhaustive + droit de veto |
| **Exit clauses** | Récupération données + suppression certifiée |

## Comparatif providers (mai 2026)

| Critère | OpenAI | Anthropic | Mistral |
|---|---|---|---|
| DPA + SCCs | ✅ | ✅ (Irish law) | ✅ |
| Training opt-out | Opt-out | **Off by default** | EU-based |
| Retention API | 30j | **7j** | EU-based |
| ZDR | ✅ (qualif) | ✅ (addendum) | Varies |
| EU residency | Enterprise | Enterprise | **Native** |
| SOC 2 Type II | ✅ | ✅ | À vérifier |
| ISO 42001 | En cours | ✅ (jan 2025) | À vérifier |
| **SecNumCloud** | ❌ | ❌ | **Via OVH/Scaleway** |

⚠️ **Une fois entraîné, pas de "unlearning" possible**. Si vos données partent dans le training set, elles y sont. D'où importance opt-out **contractuel + par défaut**.

## AI Acceptable Use Policy — URGENT

### Pourquoi (Shadow AI)
Mid-market moyen : **3-5× plus d'outils IA en usage que ce que l'IT a sanctionné**.

Cas Samsung 2023 : ingénieurs ont fuité code semi-conducteurs sur ChatGPT public → ban global. Neoteem n'a pas la capacité juridique de gérer un tel incident.

### Composants minimaux

1. **Scope** : salariés, prestataires, BYOD inclus
2. **Liste outils sanctionnés** : ChatGPT Team/Enterprise, Claude for Work, Gemini Workspace, Copilot — **pas les versions gratuites**
3. **Classification data 3-tiers** :
   - Public : libre sur tout outil approuvé
   - Interne : enterprise tiers uniquement
   - **Confidentiel/PII clients : interdit sur tout LLM externe**
4. **Interdictions explicites** : noms clients, données financières, scoring, baux, identités locataires
5. **Output review obligatoire** : tout contenu généré → revue humaine avant usage externe
6. **Sanctions progressives** : retraining > avertissement > sanction. Pas de licenciement au premier cas.

### Stratégie "Restrict & Replace"
Plus efficace que l'interdiction pure : bloquer outils risqués + **offrir alternative enterprise**. Sans alternative, les gens contournent.

## Documents à produire chez Neoteem (priorité)

1. **Inventaire AI** (registre interne)
2. **Classification risque par cas d'usage** (fiche par modèle)
3. **FRIA + DPIA consolidée** pour scoring locataire
4. **Documentation technique Annexe IV** pour chaque modèle haut risque
5. **Charte AI literacy + plan de formation** salariés (obligation depuis février 2025)
6. **AI Acceptable Use Policy v1**
7. **AI Council charter** + cadence réunions
8. **Vendor due diligence** par provider LLM
9. **Model cards** par modèle prod
10. **Incident response plan IA**

## Sources

- [OWASP Top 10 LLM v2025 PDF](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf)
- [Giskard — OWASP MITRE ATLAS NIST RMF](https://www.giskard.ai/knowledge/risk-assessment-for-llms-and-ai-agents-owasp-mitre-atlas-and-nist-ai-rmf-explained)
- [TrueFoundry — LLM Deployment Regulated 2026](https://www.truefoundry.com/blog/llm-deployment-in-regulated-industries-hipaa-soc2-and-gdpr-playbook-for-2026)
- [Factually — Prompt retention OpenAI Anthropic Mistral](https://factually.co/fact-checks/technology/ai-model-providers-prompt-retention-deletion-contract-commitments-432c7b)
- [Strac — AI AUP Template 2026](https://www.strac.io/blog/ai-acceptable-use-policy-template)
- [Prompt.security — AI AUP](https://prompt.security/blog/ai-acceptable-use-policy-what-it-is-why-it-matters-and-how-to-create-one)
- [OneTrust — AI Governance Committee](https://www.onetrust.com/blog/establishing-an-ai-governance-committee-an-inside-look-at-onetrusts-process/)
- [Deloitte — AI Board Governance Roadmap](https://www.deloitte.com/us/en/programs/center-for-board-effectiveness/articles/board-of-directors-governance-framework-artificial-intelligence.html)
