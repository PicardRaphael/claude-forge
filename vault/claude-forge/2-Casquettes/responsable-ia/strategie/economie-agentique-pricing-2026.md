---
titre: "Économie agentique & pricing IA 2026 — la fin du SaaS par siège"
resume: "L'économie agentique casse le modèle SaaS par siège : agents simples ~4× tokens d'un chat, multi-agents ~15×. Prix par token -98% depuis 2022 mais factures IA entreprise triplées. Réponses : métré, model routing, inférence maison, pricing à l'outcome. Cas Klarna (walk-back), Ramp (build-it-yourself), Harvey (moat data métier)."
aliases:
  - économie agentique
  - agentic economics
  - pricing IA outcome
  - fin du SaaS par siège
  - token economics entreprise
  - pricing à l'outcome
  - Klarna walk-back IA
  - Ramp Inspect agent
  - Harvey legal moat
domaine: ia
type: technique
derniere-maj: 2026-06-07
auteur: claude
sources:
  - "https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/ (Menlo Ventures, 9 déc 2025, ~500 décideurs US — estimation d'enquête)"
  - "https://www.langchain.com/state-of-agent-engineering (LangChain State of Agent Engineering 2025, 1340 réponses — estimation d'enquête)"
  - "Bloomberg interview Sebastian Siemiatkowski mai 2025 (Klarna walk-back)"
  - "Important/Stack IA.md (synthèse forge interne, 2026)"
tags:
  - "#type/technique"
  - "#casquette/responsable-ia"
  - "#domaine/strategie"
  - "#domaine/economie-ia"
---

# Économie agentique & pricing IA 2026 — la fin du SaaS par siège

> [!warning] Statut épistémique
> Cette note capitalise une synthèse forge dont **la majorité des chiffres sont des estimations d'enquête** (Menlo ~500 répondants, LangChain 1340) ou des **claims vendeurs non reproduits**. Chaque chiffre porte son marqueur de provenance. Les chiffres Menlo/LangChain ci-dessous ont été **vérifiés à la source primaire le 7 juin 2026**.

## TL;DR pour le Lead IA

1. **L'économie agentique casse le pricing SaaS par siège.** Un siège facturé à prix fixe ne reflète plus la consommation : un power-user agentique consomme 4× à 15× plus de tokens qu'un chat. Le flat-rate subventionne massivement les power-users.
2. **Prix par token en chute libre (~-98% depuis 2022) MAIS budgets IA entreprise triplés** — parce que le volume agentique explose plus vite que les prix ne baissent.
3. **Réponses de l'industrie** : métré (tiered metering), model routing/cascades, inférence maison (Cursor Composer), **pricing à l'outcome** (Intercom Fin 0,99 $/résolution, HubSpot 0,50 $/conversation résolue).
4. **Kill switches & spend ceilings = obligatoires.** Cas reporté d'une facture Claude ~500 M$ faute de limites (à vérifier, single source synthèse). Anthropic a divulgué (juillet 2025) un user consommant « tens of thousands » de dollars sur un plan à 200 $.

## Le coût agentique en chiffres

| Mesure | Valeur | Provenance |
|---|---|---|
| Tokens agent simple vs chat | **~4×** | Anthropic (blog multi-agent research) — vérifié existence déclaration |
| Tokens multi-agent vs chat | **~15×** | Anthropic — idem |
| Chute prix par token depuis 2022 | **~-98%** | Synthèse forge directionnelle, non audité |
| Évolution facture IA entreprise | **×3 (triplée)** | Cohérent Menlo : 1,7 Md$ (2023) → 37 Md$ (2025) |
| Abonnement 200 $ ↔ compute sous-jacent | **~5000 $** | **Estimation Cursor, non auditée** |
| Claude Code : users sous 30 $/jour | **90%** | Synthèse forge, donnée de consommation citée |
| Moyenne dev Claude Code | **~150-250 $/dev/mois** | idem |
| User Max 20x (200 $) ↔ équiv. API | **600-1500 $/mois** | idem |
| Seuil bascule flat→métré | **62-140 M tokens/dev/mois** | Repère forge, à calibrer empiriquement |

> [!note] Anthropic verbatim (existence vérifiée, pas véracité empirique)
> « agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats. »

## Le marché des modèles (Menlo Ventures, déc. 2025 — vérifié source primaire)

Rapport annuel Menlo Ventures, 3ᵉ édition, **~500 décideurs entreprise US** (estimation d'enquête, biais d'auto-sélection).

- **Dépense IA entreprise** : 1,7 Md$ (2023) → **37 Md$ (2025)**, triplée en un an. « the fastest enterprise category expansion in history » — un palier que le SaaS a mis 15 ans à atteindre.
- **Parts de marché LLM API entreprise** :
  - **Anthropic ~40%** (24% en 2024, 12% en 2023) — a dépassé OpenAI
  - **OpenAI ~27%** (de 50% en 2023)
  - **Google ~21%** (de 7% en 2023, ×3)
- **Coding spécifiquement** : **Anthropic 54%** vs OpenAI 21% — porté par Claude Code, 18 mois de domination depuis Sonnet 3.5 (juin 2024). Le coding est la 1ʳᵉ « killer use case » : **7,3 Md$** de dépense départementale.
- **76% des solutions IA entreprise sont achetées** (vs **53% l'année précédente**).

> [!important] Correction vs synthèse source
> La synthèse forge disait « 76% achetés vs 47% construits en interne en 2024 ». La source primaire Menlo dit **76% achetés en 2025, contre 53% l'an dernier**. Le « 47% » est en réalité le **taux de conversion pilote→production** des projets IA (~47% vs ~25% pour le SaaS classique) — deux métriques distinctes confondues dans la synthèse. Capitalisé ici corrigé.

## Build vs Buy — l'arbitrage 2026

Bascule décisive vers le **buy** (76%). Mais les acteurs **AI-native build leur tooling propre** : Ramp Inspect, Cursor Composer, Block Goose.

**Wrapper-vs-moat** — le moat n'est PAS le wrapper du modèle, mais :
1. Les **evals + golden data propriétaires**
2. Le **context engineering domaine-spécifique**
3. L'**intégration profonde au workflow**

→ Complète la matrice [[build-vs-buy-vs-finetune-rag]] (à créer) et la section « Build vs Buy — Neoteem » de [[../strategie/index]].

## Trois études de cas canoniques

### Klarna — l'échec emblématique du walk-back

- **Fév. 2024** : le chatbot (partenariat OpenAI) ferait « the work of 700 agents », 2,3 M chats/mois, résolution 11 min → < 2 min.
- **Mai 2025** : le CEO Siemiatkowski admet à Bloomberg que la sur-pondération du coût a produit une qualité moindre. Verbatim : « As cost unfortunately seems to have been a too predominant evaluation factor when organizing this, what you end up having is lower quality. »
- Klarna **ré-embauche des humains** (modèle « Uber-style ») pour les cas complexes.

> [!tip] Leçon Klarna pour Neoteem
> L'IA gère le **80% simple** ; les humains gardent le **20% complexe/empathique** ; **soigner le handoff** : intent classifié + contexte + tentative + score de confiance. Ne jamais sur-pondérer le coût comme facteur d'évaluation unique.

### Ramp — le succès build-it-yourself

- Agent de coding interne « **Inspect** » (Modal Sandboxes + OpenCode + Cloudflare Durable Objects ; câblé Sentry/Datadog/LaunchDarkly/Braintrust/GitHub/Slack/Buildkite).
- Écrit **~30-50% des PR mergées** (claim vendeur interne, non reproduit). 80%+ d'Inspect est écrit par Inspect.
- Chaque session = VM sandboxée avec environnement complet (Postgres, Redis, Temporal).
- Philosophie (Zach Bruggeman) : « The only way you're going to ensure that it is the best… is to build it yourself. »
- **Caveat Ramp** : viable seulement avec de fortes compétences infra ; la limite reste « model intelligence itself ».

### Harvey — le moat par les données métier

- Legal, valorisé **11 Md$**. 25 000+ agents custom (M&A, due diligence, contract review), avec des « embedded legal engineering teams ».
- **Moat = données métier + expertise embarquée, PAS le modèle.**

## Pricing à l'outcome — le nouveau modèle

Le pricing par siège ne survit pas à l'agentique. Modèles émergents :

| Modèle | Exemple | Unité |
|---|---|---|
| **Pricing à l'outcome** | Intercom Fin | **0,99 $/résolution** |
| **Pricing à l'outcome** | HubSpot | **0,50 $/conversation résolue** |
| **Tiered metering** | la plupart des labs | par palier de tokens |
| **Model routing** | Factory router | modèle choisi par tâche |
| **Inférence maison** | Cursor Composer | casse le coût retail par token |

**Product-led growth domine** : Cursor a atteint 200 M$ ARR avant d'embaucher un seul commercial entreprise. PLG = 27% de la dépense IA (~40% avec le shadow AI).

## Marges — le signal d'alarme

- Marges AI-native projetées **~52% en 2026** vs **75-85% SaaS mûr** (ICONIQ, estimation directionnelle).
- **Si la marge brute tombe sous ~50% à cause de l'inférence** → router vers des modèles moins chers ou internaliser.

## Implications pour Neoteem (Loji)

1. **Suivre le coût/token comme un KPI d'allocation de capital** (FinOps de tokens). Benchmark par tâche/outcome.
2. **Kill switches + spend ceilings** par agent/workflow/BU **dès le départ** — pas en rattrapage.
3. **Ne pas sur-pondérer le coût** dans l'arbitrage qualité (leçon Klarna) : NeoChat/NeoDocs doivent soigner le handoff humain sur le 20% complexe.
4. **Le moat Neoteem = données proptech (biens, baux, scoring) + evals propriétaires**, pas le wrapper LLM. Cohérent avec la matrice [[../strategie/index]] (RAG obligatoire proptech).
5. **Buy par défaut** (MVP), build seulement si compétences infra fortes ET volume le justifie (cf Ramp caveat).

## Liens

- [[../strategie/index]] — hub stratégie IA & gouvernance (matrice Build vs Buy Neoteem)
- [[build-vs-buy-vs-finetune-rag]] — note atomique build/buy/fine-tune/RAG (à créer)
- [[stack-ia-production-2026]] — synthèse transverse du stack IA en production
- [[roi-ia-mesure-mckinsey]] — ROI IA (75% des projets ratent leur ROI)
- [[hype-ia-cadrage-kozyrkov]] — cadrage anti-hype
- [[Cursor]] — fiche concurrent (Composer, inférence maison)
