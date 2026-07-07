---
titre: "Techniques de prompting dépréciées 2026"
resume: "Inventaire des techniques de prompting devenues contre-productives en 2026 sur les modèles frontier : chain-of-thought, few-shot, self-consistency, sur-spécification et autres patterns 2023-2025"
aliases:
  - "deprecated prompting 2026"
  - "techniques dépréciées prompting"
  - "anti-patterns prompting frontier"
  - "prompting obsolete 2026"
  - "techniques a eviter LLM"
  - "prompting patterns broken"
domaine: technique
type: deprecation
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://developers.openai.com/api/docs/guides/prompt-guidance"
  - "https://www.anthropic.com/docs"
  - "https://arxiv.org/abs/2601.00880"
tags:
  - "#type/technique"
  - "#type/deprecation"
  - "#domaine/prompt-engineering"
---

## Contexte

En 2026, les modèles frontier (Claude Opus 4.7, GPT-5.x, Gemini 2.5 Deep Think) ont des capacités de raisonnement interne qui rendent certaines techniques 2023-2025 non seulement inutiles, mais **activement dégradantes**.

> "Legacy prompts often over-specify the process because earlier models needed more help staying on track. With GPT-5.5, that can add noise, narrow the model's search space, or lead to overly mechanical answers."
> — [OpenAI GPT-5.5 Prompting Guide](https://developers.openai.com/api/docs/guides/prompt-guidance), avril 2026 (verbatim canonique — version forge précédente "patterns you spent months perfecting" était fabriquée, corrigée 2026-05-23)

## Techniques désormais contre-productives

### 1. "Let's think step by step"

**Origine :** Zero-shot CoT — **Kojima et al 2022** ([arXiv 2205.11916](https://arxiv.org/abs/2205.11916)), distinct du paper CoT (Wei et al 2022 arxiv 2201.11903 = few-shot CoT avec démonstrations).
**Statut :** Inutile à nuisible sur reasoning models  
**Pourquoi :** Claude Opus 4.7, GPT-5.x, Gemini Deep Think font le raisonnement internement (extended thinking). Ajouter cette instruction perturbe le flux de raisonnement natif.  
**Alternative :** Rien — laisser le modèle raisonner. Ou utiliser `effort: xhigh` via API.

### 2. Few-shot sur reasoning models

**Statut :** Contre-productif (heuristique post-2022)
**Pourquoi :** Sur reasoning models (o1/o3, Claude extended thinking), les exemples consomment le contexte de raisonnement interne sans bénéfice. Heuristique synthétisée depuis docs OpenAI o1 + Anthropic extended thinking.
**Alternative :** Zéro-shot + description claire de l'outcome attendu.

### 3. Self-consistency prompting

**Statut :** Redondant (heuristique post-2022)
**Pourquoi :** Self-consistency (Wang et al 2022, arxiv 2203.11171) a été construit pour les LLM standard qui varient leurs sorties. Les reasoning models internalisent un raisonnement avant de répondre — heuristique forge à confirmer empiriquement par modèle.
**Alternative :** Confiance dans le raisonnement natif + verification post-réponse si critique.

### 4. Least-to-most prompting

**Statut :** Contre-productif (heuristique post-2022)
**Pourquoi :** Prescrit une décomposition que le modèle fait mieux seul. Crée de l'hyper-literalism documenté par paper Sculpting (Khan 2025, arxiv 2510.22251) sur GSM8K — Sculpting NUIT gpt-5 (-2.4 points vs baseline).
**Alternative :** [[outcome-first-prompting]] — définir l'outcome, pas le process.

### 5. Process-first / step-by-step instructions (GPT-5.5)

**Statut :** Activement dégradant sur GPT-5.5
**Pourquoi :** Verbatim OpenAI GPT-5.5 Prompting Guide : *"For many tasks, describe the destination rather than every step."* + *"Avoid carrying over every instruction from an older prompt stack."*
**Alternative :** Instructions orientées outcome + critères de succès.

### 6. Prefilled responses (Claude 4.6+)

**Statut :** No longer supported (docs Anthropic officielles)
**Pourquoi :** Verbatim Anthropic migration guide : *"Prefilled responses on the last assistant turn are no longer supported starting with Claude 4.6 models."*
**Alternative :** XML output tags ou format instructions dans le prompt. Voir migration guide Anthropic pour détail.
**Note correction 2026-05-23 :** précédente formulation "erreur 400" n'était pas verbatim documenté — Anthropic dit "no longer supported", le comportement exact (erreur vs ignore) varie.

### 7. Sur-spécification au-delà de S*=0.509

**Statut :** Dégradation quadratique  
**Pourquoi :** Prouvé par UCL (arXiv 2601.00880) — au-delà du seuil optimal, chaque contrainte supplémentaire nuit.  
**Alternative :** Pruner les contraintes. 29.8% de tokens en moins = meilleure performance.

### 8. ALL-CAPS / ALWAYS / NEVER pour les jugements

**Statut :** Contre-productif sur Claude 4.6+ (verbatim Anthropic)
**Pourquoi :** Verbatim Anthropic prompting best practices : *"The fix is to dial back any aggressive language. Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'."* Les modèles 4.6+ sont plus responsifs au system prompt — les ALL-CAPS créent de l'overtriggering.
**Alternative :** Formuler "Use X when Y" plutôt que "CRITICAL: You MUST use X". Expliquer le POURQUOI > imposer en majuscules.
**Note correction 2026-05-23 :** précédente "exception sécu absolue" était l'INVERSE de la recommandation Anthropic. Pour les vraies contraintes de sécurité, formuler factuellement reste plus efficace que des majuscules.

### 9. Formatage markdown excessif

**Statut :** Dégradant sur GPT-5.5
**Pourquoi :** Verbatim OpenAI GPT-5.5 Guide : *"Use plain paragraphs as the default format for normal conversation, explanations, reports, documentation, and technical writeups."* Trop de headers/bullets fragmente la cohérence de sortie.
**Alternative :** Prose structurée pour les tâches analytiques. Markdown uniquement si la sortie est un document.

### 10. `budget_tokens` comme levier de contrôle du raisonnement

**Statut :** Deprecated → remplacé par `effort` parameter  
**Pourquoi :** `budget_tokens` (Claude 3.x) est remplacé par `effort: low|medium|high|xhigh` sur les modèles 4.x.  
**Pitfall Adaptive Thinking :** Le remplacement peut allouer **ZERO tokens de réflexion** → hallucinations précises (faux SHA, packages inexistants). Garde-fous si comportement non déterministe observé : `CLAUDE_CODE_EFFORT_LEVEL=max` + `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`.  
**Sweet spot prompts :** 150-300 mots (~3000 tokens max) — au-delà, voir [[over-specification-paradox]].

## Ce qui reste valide

- **XML pour zones sémantiques** (system prompts longs, tools API) — toujours efficace
- **Instructions négatives absolues** — "Ne JAMAIS X car Y" (avec le pourquoi)
- **Format de sortie explicite** — schema + exemple reste utile
- **Anti-hallucination** — "si tu ne sais pas, dis-le" reste nécessaire
- **TDD prompts** (Amanda Askell) — écrire les tests avant le prompt, toujours valide

## Liens

- [[over-specification-paradox]] — Preuve mathématique du seuil S*=0.509
- [[outcome-first-prompting]] — L'alternative : définir l'outcome, pas le process
- [[amanda-askell-prompt-engineering]] — Techniques Anthropic encore valides
- [[Context Engineering]] — Paradigme dominant 2026
- [[MOC-Techniques]]


## AJOUT 2026-06-26 — Gemini 3.x / 3.5 Flash (vérifié source primaire Google)

Vérifié à la source primaire le 26 juin 2026 (ai.google.dev/gemini-api/docs/whats-new-gemini-3.5 + blog.google + docs.cloud.google.com gemini-3-prompting-guide), chantier prompting neo_ia. Faits DATÉS — re-vérifier avant de citer.

- **`gemini-3.5-flash` GA depuis le 19 mai 2026**, devenu défaut de l'app Gemini (remplace 2.5 Flash). « Gemini 3 Flash/Pro » = génération précédente ; `gemini-3-flash-preview` était la preview.
- **`temperature` / `top_p` / `top_k` ne sont plus recommandés sur TOUS les modèles Gemini 3.x** — verbatim : *« temperature, top_p, and top_k are no longer recommended for all Gemini 3.x models »*. Reco Google = **retirer ces paramètres** (modèle optimisé pour ses défauts). Conséquence migration : tout mapping `task_type → temperature` (ex : ROUTING/EXTRACTION à temp=0.0 pour le déterminisme) devient caduc → déterminisme via **règles explicites en system instruction**, pas via la température. Cohérent avec [[parametres-echantillonnage-llm]] et [[opus-47-design-defaults]] (contrôle par le prompt, pas le sampling).
- **CoT forcé → `thinking_level`** (`minimal` / `low` / `medium` (défaut) / `high`), qui remplace `thinking_budget`. Verbatim : *« If you used chain-of-thought prompt engineering to force reasoning, try thinking_level… with simpler prompts instead. »*
- **Concis par défaut** : *« verbose or complex prompt engineering techniques designed for older models may cause the model to over-analyze »* → validation directe de [[over-specification-paradox]].
- **« do not infer » / négations larges** font over-indexer → préférer « use the provided context for deductions ».
- **Seuil cache implicite par modèle** : 2.5 Flash = **1024 tokens**, 2.5 Pro = **2048 tokens** (doc Google). Seuil 3.5 Flash non documenté publiquement (valider via `cached_content_token_count`). Gotcha neo_ia : code force `GEMINI_CACHE_MIN_TOKENS = 2048` (valeur Pro) → monitoring `calculate_cache_eligible_tokens` **sous-rapporte** sur Flash. Bug de monitoring, pas de coût. Cf [[neochat-adaptive-prompt]] (note « seuil 1024 » à préciser par modèle).
