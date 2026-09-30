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
derniere-maj: 2026-09-30
auteur: claude
sources: []
tags:
  - "#type/index"
  - "#domaine/modeles"
---
# Modèles IA

## Anthropic

> Lineup vérifié le 30 sept. 2026 sur `platform.claude.com/docs/en/models/overview` : Fable 5.1 · Opus 5.5 · Sonnet 5.5 · Haiku 4.5. Legacy toujours disponibles : Fable 5, Opus 5, Opus 4.8, 4.7, 4.6, 4.5, Sonnet 5, 4.6, 4.5.

- [[Opus 5.5]] (`claude-opus-5-5`, 22 sept. 2026) — **défaut Opus de Claude Code depuis v2.1.280** et **point de départ recommandé par Anthropic pour la plupart des workloads**. $4/$20, cache read $0,20/MTok, 1M ctx / 128K output, cutoff juin 2026, thinking adaptatif toujours actif. ⚠️ **Effort API par défaut `medium`** (et non `high`) ; `thinking: disabled`, `budget_tokens`, `tool_choice` any/tool, sampling non défaut et prefill → 400
- **Sonnet 5.5** (`claude-sonnet-5-5`, 28 sept. 2026, fiche non créée) — *« The best combination of speed and intelligence »* ; **Sonnet par défaut sur l'API Anthropic dans Claude Code depuis v2.1.284** (alias `sonnet` → Sonnet 5.5, table de `code.claude.com/docs/en/model-config`). $2/$10, cache read $0,20, cache minimum 512 tokens, 1M ctx / 128K output, cutoff juin 2026, thinking adaptatif. ⚠️ **Effort par défaut `high` sur l'API mais `medium` dans Claude Code** ; niveaux recalibrés (refaire le sweep ; départ officiel `medium` pour l'agentique bien spécifiée, `high` sinon). Cinq breaking changes vs Sonnet 5 : `thinking: disabled` → 400 (utiliser `between_tools`, effort ≤ `high`), `tool_choice` any/tool → 400, thinking blocks liés au modèle, à la conversation et au compte, `computer_20251124` refusé sur API Claude et Google Cloud (toolset `computer_toolset_20260801`), advisor tool refusant Opus 4.8, Opus 4.7 et Sonnet 5 comme conseillers. Retrait pas avant le 28 sept. 2027
- [[Fable 5.1]] — **modèle Fable par défaut depuis le 1er sept. 2026** ; classe Mythos, 1M ctx / 128k output, $10/$50, cache read $0,25/MTok, effort défaut `high`. Step-up quand Opus 5.5 à effort élevé ne suffit pas. Mythos 5.1 = même modèle, safeguards renforcés (Project Glasswing)
- [[Opus 5]] — flagship Opus du 24 juil. 2026, $5/$25, 1M ctx, effort défaut `high`. Défaut Opus CC jusqu'à v2.1.279 ; **legacy depuis le 22 sept. 2026**
- [[Fable 5]] — génération Fable précédente, annoncée 9 juin 2026, redéployée 1er juillet (export controls levés 30 juin) ; recadrée 20 juillet (50 % des limites hebdo Max/Team Premium) ; legacy
- [[Sonnet 5]] — near-Opus agentic, 1M ctx natif, $2/$10 devenu **prix standard** (la hausse à $3/$15 prévue le 1er sept. 2026 a été annulée). Défaut Free/Pro du 30 juin 2026 à CC v2.1.280, qui fait passer Pro et Team Standard sur Opus ; **legacy depuis le 28 sept. 2026**
- [[Opus 4.7]] — SWE-bench 87.6%, adaptive thinking — retiré du fast mode (24 juil. 2026)
- [[Sonnet 4.6]] — Exécution forge, effort high obligatoire
- [[Haiku 4.5]] — Rapide, léger, faible coût ; retrait « not sooner than October 15, 2026 » (aucun signal Haiku 5 au 30 sept.)
- [[claude-mythos-preview]] — SWE-bench 93.9%, zero-day autonome, Project Glasswing only — **déprécié le 9 juin 2026, retrait « To be announced »** (page deprecations au 30 sept. 2026)

## OpenAI

- [[GPT-6 Astra]] — flagship (3 sept. 2026), *« our most capable model, built for the hardest end-to-end work »*. $10 / $1 cache / $50, 1,05M ctx, 128K output — confirmé en primaire le 25 sept. ; ×2 input / ×1,5 output sur toute la requête au-delà de 272K tokens d'entrée. Pas de reasoning effort `none`, pas de temperature/top_p custom, pas de logprobs ; **tool calling via Responses API uniquement**. Mode **Ultrafast** (`service_tier: "ultrafast"`, résidence US uniquement) depuis le 29 sept.
- **GPT-6.1 Sol** (`gpt-6.1-sol`, 29 sept. 2026, fiche non créée) — *« near-Astra performance for complex work at a lower cost than Astra »* ; $2 / $0,10 cache / $10, 1,05M ctx, 128K output ; **défaut du catalogue Codex CLI depuis 0.159.1**. Détail dans [[GPT-6 Sol et Luna]]
- [[GPT-6 Sol et Luna]] (22 sept. 2026) — modèles de raisonnement, Responses **et** Chat Completions. Sol $2 / $0,20 / $10, 1,05M ctx, effort `none`→`max` (défaut `medium`) ; Luna $0,10 / $0,01 / $0,50, 1,05M ctx (fiche confirmée le 30 sept.) pour le volume
- [[GPT-5.6]] — Famille Sol/Terra/Luna (GA 9 juil. 2026), SOTA coding agent, Programmatic Tool Calling
- [[GPT-5.5]] — Flagship printemps 2026, Terminal-Bench 82.7%, variantes Instant/Pro/Cyber ; **retiré de ChatGPT et Codex le 14 oct. 2026**

## Google

> Catalogue vérifié le 5 sept. 2026 sur `ai.google.dev/gemini-api/docs/models` et `deepmind.google/models/gemini/` ; revu le 30 sept. (page modèles mise à jour le 24 sept. : 3.8 Flash toujours dernier stable texte, 3.1 Pro toujours preview, aucun 3.8 Pro).

- Série 3 **stable** : Gemini 3.8 Flash (*« engineered for long-horizon software engineering, autonomous agents »*), 3.7 Flash, 3.6 Flash, 3.5 Flash, 3.5 Flash-Lite, 3.1 Flash-Lite
- Audio / temps réel (changelog Gemini API) : **Gemini 3.8 Live** et **Live Extended Thinking** GA (15 sept.) ; **Gemini 3.8 Flash TTS** et **Flash-Lite TTS** GA, bibliothèque de 150+ voix (22 sept.)
- **Gemini 3.1 Pro** — statut **preview** (`gemini-3.1-pro-preview`), pas GA
- **Gemini 3.5 Pro** — absent de `ai.google.dev` au 24 sept. ; `deepmind.google/models/gemini/` (page non datée) l'affiche toujours « coming soon » au 30 sept. Aucune sortie ni abandon annoncé
- **Gemini 3.8 Flash Cyber** (détection de vulnérabilités) — listé sur `deepmind.google/models/gemini/` au 30 sept., à confirmer par une source primaire dédiée
- **Gemini 4.0** — **aucune date de sortie annoncée**. Le pré-entraînement aurait démarré fin juillet 2026 (call résultats Q2, source tierce à reconfirmer)
- Modèles image : Nano Banana 2 (`gemini-3.1-flash-image`), Nano Banana Pro (`gemini-3-pro-image`)
- [[Gemma 4]] — Open-source, 26b-a4b-it et 31b-it

## xAI

- **Grok 4.7** — présenté comme le modèle le plus capable sur `docs.x.ai` (release notes « September 2026 », jour non précisé) : 500K ctx, entrée texte + image, reasoning effort `low`→`xhigh` ; variante **Fast** réservée à Cursor et Grok Build. Disponible dans GitHub Copilot depuis le 21 sept. 2026 (changelog GitHub). Fiche non créée
- [[Grok 4.5]] — SpaceXAI (8 juil. 2026), 1.5T V9, token efficiency 4.2x vs Opus 4.8, 500K ctx ; retiré de Copilot le 19 oct. 2026
- [[grok-code-fast-1]] — MoE 314B, 70.8% SWE-Bench, 15x moins cher que Sonnet

## Deprecations

### Anthropic
- Sonnet 5 — **legacy** (toujours disponible, retrait pas avant le 30 juin 2027) depuis la sortie de Sonnet 5.5, le 28 sept. 2026
- Opus 5, Fable 5 — **legacy** (toujours disponibles) depuis le 22 sept. 2026
- [[claude-mythos-preview]] — déprécié le 9 juin 2026, retrait « To be announced » (une date du 21 juillet 2026 inscrite ici auparavant n'a pas de source primaire)
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
