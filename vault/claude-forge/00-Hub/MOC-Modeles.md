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
derniere-maj: 2026-09-25
auteur: claude
sources: []
tags:
  - "#type/index"
  - "#domaine/modeles"
---
# Modèles IA

## Anthropic

> Lineup vérifié le 25 sept. 2026 sur `platform.claude.com/docs/en/models/overview` : Fable 5.1 · Opus 5.5 · Sonnet 5 · Haiku 4.5. Legacy toujours disponibles : Fable 5, Opus 5, Opus 4.8, 4.7, 4.6, 4.5, Sonnet 4.6, 4.5.

- [[Opus 5.5]] (`claude-opus-5-5`, 22 sept. 2026) — **défaut Opus de Claude Code depuis v2.1.280** et **point de départ recommandé par Anthropic pour la plupart des workloads**. $4/$20, cache read $0,20/MTok, 1M ctx / 128K output, cutoff juin 2026, thinking adaptatif toujours actif. ⚠️ **Effort API par défaut `medium`** (et non `high`) ; `thinking: disabled`, `budget_tokens`, `tool_choice` any/tool, sampling non défaut et prefill → 400
- [[Fable 5.1]] — **modèle Fable par défaut depuis le 1er sept. 2026** ; classe Mythos, 1M ctx / 128k output, $10/$50, cache read $0,25/MTok, effort défaut `high`. Step-up quand Opus 5.5 à effort élevé ne suffit pas. Mythos 5.1 = même modèle, safeguards renforcés (Project Glasswing)
- [[Opus 5]] — flagship Opus du 24 juil. 2026, $5/$25, 1M ctx, effort défaut `high`. Défaut Opus CC jusqu'à v2.1.279 ; **legacy depuis le 22 sept. 2026**
- [[Fable 5]] — génération Fable précédente, annoncée 9 juin 2026, redéployée 1er juillet (export controls levés 30 juin) ; recadrée 20 juillet (50 % des limites hebdo Max/Team Premium) ; legacy
- [[Sonnet 5]] — near-Opus agentic, 1M ctx natif, $2/$10. A été le défaut Free/Pro du 30 juin 2026 à CC v2.1.280, qui fait passer Pro et Team Standard sur Opus
- [[Opus 4.7]] — SWE-bench 87.6%, adaptive thinking — retiré du fast mode (24 juil. 2026)
- [[Sonnet 4.6]] — Exécution forge, effort high obligatoire
- [[Haiku 4.5]] — Rapide, léger, faible coût ; retrait « not sooner than October 15, 2026 » (aucun signal Haiku 5)
- [[claude-mythos-preview]] — SWE-bench 93.9%, zero-day autonome, Project Glasswing only — **retiré 21 juillet 2026**

## OpenAI

- [[GPT-6 Astra]] — flagship (3 sept. 2026), *« our most capable model, built for the hardest end-to-end work »*. $10 / $1 cache / $50, 1,05M ctx, 128K output — confirmé en primaire le 25 sept. ; ×2 input / ×1,5 output sur toute la requête au-delà de 272K tokens d'entrée. Pas de reasoning effort `none`, pas de temperature/top_p custom, pas de logprobs ; **tool calling via Responses API uniquement**
- [[GPT-6 Sol et Luna]] (22 sept. 2026) — modèles de raisonnement, Responses **et** Chat Completions. Sol $2 / $0,20 / $10, 1,05M ctx, effort `none`→`max` (défaut `medium`), recommandé par Codex pour le coding agentique ; Luna $0,10 / $0,01 / $0,50 (changelog API) pour le volume
- [[GPT-5.6]] — Famille Sol/Terra/Luna (GA 9 juil. 2026), SOTA coding agent, Programmatic Tool Calling
- [[GPT-5.5]] — Flagship printemps 2026, Terminal-Bench 82.7%, variantes Instant/Pro/Cyber ; **retiré de ChatGPT et Codex le 14 oct. 2026**

## Google

> Catalogue vérifié le 5 sept. 2026 sur `ai.google.dev/gemini-api/docs/models` et `deepmind.google/models/gemini/` ; revu le 25 sept. (3.8 Flash toujours « New Stable », 3.1 Pro toujours preview).

- Série 3 **stable** : Gemini 3.8 Flash (*« engineered for long-horizon software engineering, autonomous agents »*), 3.7 Flash, 3.6 Flash, 3.5 Flash, 3.5 Flash-Lite, 3.1 Flash-Lite
- **Gemini 3.1 Pro** — statut **preview** (`gemini-3.1-pro-preview`), pas GA
- **Gemini 3.5 Pro** — « Coming soon » au 5 sept. 2026 ; le libellé n'apparaît plus sur la page modèles servie le 25 sept., sans annonce d'abandon ni de sortie (statut à reconfirmer)
- **Gemini 4.0** — **aucune date de sortie annoncée**. Le pré-entraînement aurait démarré fin juillet 2026 (call résultats Q2, source tierce à reconfirmer)
- Modèles image : Nano Banana 2 (`gemini-3.1-flash-image`), Nano Banana Pro (`gemini-3-pro-image`)
- [[Gemma 4]] — Open-source, 26b-a4b-it et 31b-it

## xAI

- **Grok 4.7** — présenté comme le modèle le plus capable sur `docs.x.ai` ; disponible dans GitHub Copilot depuis le 21 sept. 2026 (changelog GitHub). Fiche non créée
- [[Grok 4.5]] — SpaceXAI (8 juil. 2026), 1.5T V9, token efficiency 4.2x vs Opus 4.8, 500K ctx ; retiré de Copilot le 19 oct. 2026
- [[grok-code-fast-1]] — MoE 314B, 70.8% SWE-Bench, 15x moins cher que Sonnet

## Deprecations

### Anthropic
- Opus 5, Fable 5 — **legacy** (toujours disponibles) depuis le 22 sept. 2026
- [[claude-mythos-preview]] — retrait 21 juillet 2026 (effectif)
- Opus 4.1 — retrait 5 août 2026
- Opus 4.7 — retiré du fast mode 24 juillet 2026 (`speed: "fast"` → erreur ; standard toujours dispo)
- [[Deprecation Sonnet 4 Opus 4]] — retirement 15 juin 2026
- [[Deprecation Haiku 3]] — retirement 19 avril 2026
- [[Deprecation 1M Context Beta]]

### OpenAI
- GPT-5.5 — retiré de ChatGPT, ChatGPT Work et Codex le 14 oct. 2026 (remplacement conseillé : `gpt-6-sol`)

### Google (vérifié 5 sept. 2026)
- Gemini 2.0 Flash, Gemini 2.0 Flash-Lite — **shut down**
- Gemini 3.1 Flash-Lite Preview, Gemini 3 Pro Preview — **shut down**
- Imagen 4 — déprécié
- Modèles 2.5 : accès réservé aux utilisateurs actifs depuis le 18 sept. 2026 (non dépréciés)
- `antigravity-preview-05-2026` — arrêt le 5 oct. 2026, remplacé par `antigravity-preview-09-2026` (paramètres d'outils passés en PascalCase)
- Préavis annoncé : au moins 2 semaines avant retrait

## Liens

- [[Home]]
- [[MOC-Claude-Code]]
- [[doctrine-par-modele-opus5-fable5]] — quel modèle pour quel agent
- [[parametres-echantillonnage-llm]] — boutons de raisonnement et sampling par fournisseur
