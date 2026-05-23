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
