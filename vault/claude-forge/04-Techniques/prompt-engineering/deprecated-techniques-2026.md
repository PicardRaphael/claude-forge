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
derniere-maj: 2026-05-10
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

> "The prompt patterns you spent months perfecting for GPT-5.2 may be actively making GPT-5.5 worse."
> — OpenAI GPT-5.5 Prompting Guide, avril 2026

## Techniques désormais contre-productives

### 1. "Let's think step by step"

**Statut :** Inutile à nuisible sur reasoning models  
**Pourquoi :** Claude Opus 4.7, GPT-5.x, Gemini Deep Think font le raisonnement internement (extended thinking). Ajouter cette instruction perturbe le flux de raisonnement natif.  
**Alternative :** Rien — laisser le modèle raisonner. Ou utiliser `effort: xhigh` via API.

### 2. Few-shot sur reasoning models

**Statut :** Contre-productif  
**Pourquoi :** Les exemples "overwhelment" le raisonnement interne. Les reasoning models généralisent sans avoir besoin d'ancrage par exemples.  
**Alternative :** Zéro-shot + description claire de l'outcome attendu.

### 3. Self-consistency prompting

**Statut :** Redondant  
**Pourquoi :** Construit pour les LLM standard qui varient leurs sorties. Les reasoning models sont intrinsèquement cohérents — ils raisonnent avant de répondre.  
**Alternative :** Confiance dans le raisonnement natif.

### 4. Least-to-most prompting

**Statut :** Contre-productif  
**Pourquoi :** Prescrit une décomposition que le modèle fait mieux seul. Crée de l'hyper-littéralisme.  
**Alternative :** [[outcome-first-prompting]] — définir l'outcome, pas le process.

### 5. Process-first / step-by-step instructions (GPT-5.5)

**Statut :** Activement dégradant sur GPT-5.5  
**Pourquoi :** Même chose que least-to-most. Le modèle suit les steps même quand une meilleure approche existe.  
**Alternative :** Instructions orientées outcome + critères de succès.

### 6. Prefilled responses (Claude 4.6+)

**Statut :** Erreur 400  
**Pourquoi :** Anthropic a retiré le support des "assistant prefills" sur Claude 4.6+. La feature retournait des comportements imprévisibles.  
**Alternative :** XML output tags ou format instructions dans le prompt.

### 7. Sur-spécification au-delà de S*=0.509

**Statut :** Dégradation quadratique  
**Pourquoi :** Prouvé par UCL (arXiv 2601.00880) — au-delà du seuil optimal, chaque contrainte supplémentaire nuit.  
**Alternative :** Pruner les contraintes. 29.8% de tokens en moins = meilleure performance.

### 8. ALL-CAPS / ALWAYS / NEVER pour les jugements

**Statut :** Coupe le raisonnement du modèle  
**Pourquoi :** Sur les modèles frontier, les instructions en majuscules empêchent le modèle de trouver de meilleures solutions dans les cas limites.  
**Exception :** Contraintes de sécurité absolues (pas de données perso, etc.) — là les majuscules restent justifiées.  
**Alternative :** Expliquer le POURQUOI de la règle. "Ne pas X car Y" > "NEVER X".

### 9. Formatage markdown excessif

**Statut :** Dégradant sur GPT-5.5  
**Pourquoi :** Le GPT-5.5 guide recommande "plain paragraphs by default". Trop de headers/bullets fragmente la cohérence de sortie.  
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
