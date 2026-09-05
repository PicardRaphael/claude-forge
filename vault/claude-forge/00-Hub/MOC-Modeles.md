---
titre: "MOC — Modèles IA"
resume: "Index des modèles IA : Claude, GPT, Gemini, Grok — specs, benchmarks, migrations"
aliases:
  - "MOC Modeles"
  - "index modèles"
  - "modèles LLM"
  - "comparatif modèles IA"
  - "Claude Opus Sonnet Haiku"
type: index
derniere-maj: 2026-09-05
auteur: claude
sources: []
tags:
  - "#type/index"
  - "#domaine/modeles"
---
# Modèles IA

## Anthropic

- [[Fable 5.1]] — **modèle Fable par défaut depuis le 1er sept. 2026** ; classe Mythos, 1M ctx / 128k output, $10/$50, cache read $0,25/MTok, effort défaut `high`. Mythos 5.1 = même modèle, safeguards renforcés (Project Glasswing)
- [[Opus 5]] — flagship Opus (24 juil. 2026), $5/$25, 1M ctx, thinking ON par défaut, défaut Claude Max + défaut Opus CC. **Point de départ recommandé par Anthropic pour la plupart des workloads**
- [[Fable 5]] — génération Fable précédente, annoncée 9 juin 2026, redéployée 1er juillet (export controls levés 30 juin) ; recadrée 20 juillet (50 % des limites hebdo Max/Team Premium)
- [[Sonnet 5]] — near-Opus agentic, 1M ctx natif, défaut Free/Pro depuis 30 juin 2026
- [[Opus 4.7]] — SWE-bench 87.6%, adaptive thinking — retiré du fast mode (24 juil. 2026)
- [[Sonnet 4.6]] — Exécution forge, effort high obligatoire
- [[Haiku 4.5]] — Rapide, léger, faible coût (aucun signal Haiku 5)
- [[claude-mythos-preview]] — SWE-bench 93.9%, zero-day autonome, Project Glasswing only — **retiré 21 juillet 2026**

## OpenAI

- **GPT-6 Astra** — nouveau flagship (3 sept. 2026), *« our most capable model, built for the hardest end-to-end work »*. Pas de reasoning effort `none`, pas de temperature/top_p custom, pas de logprobs ; **tool calling via Responses API uniquement**. Pricing et benchmarks encore non confirmés en source primaire (à documenter)
- [[GPT-5.6]] — Famille Sol/Terra/Luna (GA 9 juil. 2026), SOTA coding agent, Programmatic Tool Calling
- [[GPT-5.5]] — Flagship printemps 2026, Terminal-Bench 82.7%, variantes Instant/Pro/Cyber

## Google

> Catalogue vérifié le 5 sept. 2026 sur `ai.google.dev/gemini-api/docs/models` et `deepmind.google/models/gemini/`.

- Série 3 **stable** : Gemini 3.8 Flash (*« engineered for long-horizon software engineering, autonomous agents »*), 3.7 Flash, 3.6 Flash, 3.5 Flash, 3.5 Flash-Lite, 3.1 Flash-Lite
- **Gemini 3.1 Pro** — statut **preview** (`gemini-3.1-pro-preview`), pas GA
- **Gemini 3.5 Pro** — toujours **« Coming soon »** au 5 sept. 2026 (le report vers ~17 juillet a de nouveau glissé)
- **Gemini 4.0** — **aucune date de sortie annoncée**. Le pré-entraînement aurait démarré fin juillet 2026 (call résultats Q2, source tierce à reconfirmer)
- Modèles image : Nano Banana 2 (`gemini-3.1-flash-image`), Nano Banana Pro (`gemini-3-pro-image`)
- [[Gemma 4]] — Open-source, 26b-a4b-it et 31b-it

## xAI

- [[Grok 4.5]] — SpaceXAI (8 juil. 2026), 1.5T V9, token efficiency 4.2x vs Opus 4.8, 500K ctx
- [[grok-code-fast-1]] — MoE 314B, 70.8% SWE-Bench, 15x moins cher que Sonnet

## Deprecations

### Anthropic
- [[claude-mythos-preview]] — retrait 21 juillet 2026 (effectif)
- Opus 4.1 — retrait 5 août 2026
- Opus 4.7 — retiré du fast mode 24 juillet 2026 (`speed: "fast"` → erreur ; standard toujours dispo)
- [[Deprecation Sonnet 4 Opus 4]] — retirement 15 juin 2026
- [[Deprecation Haiku 3]] — retirement 19 avril 2026
- [[Deprecation 1M Context Beta]]

### Google (vérifié 5 sept. 2026)
- Gemini 2.0 Flash, Gemini 2.0 Flash-Lite — **shut down**
- Gemini 3.1 Flash-Lite Preview, Gemini 3 Pro Preview — **shut down**
- Imagen 4 — déprécié
- Préavis annoncé : au moins 2 semaines avant retrait

## Liens

- [[Home]]
- [[MOC-Claude-Code]]
- [[doctrine-par-modele-opus5-fable5]] — quel modèle pour quel agent
- [[parametres-echantillonnage-llm]] — boutons de raisonnement et sampling par fournisseur
