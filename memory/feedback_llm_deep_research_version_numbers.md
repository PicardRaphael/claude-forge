---
name: llm-deep-research-version-numbers-hallucinated
description: Claims numériques précis (versions, dates, étoiles) de Gemini/ChatGPT deep research = hallucinations fréquentes. WebFetch systématique avant d'agir.
metadata:
  type: feedback
---

Quand un LLM tiers (Gemini deep research, ChatGPT) cite des **numéros de version, dates, ou stats précises**, vérifier empiriquement AVANT toute action structurelle.

**Why** : 28 mai 2026, Gemini deep research affirmait "bug #60237 fixé dans Claude Code v1.21.1 et v1.22". Vérification WebFetch CHANGELOG officiel : ces versions n'existent pas (CC versionné v2.1.x). Fix réel = v2.1.147. Numéros hallucinés mais le fait sous-jacent (bug existe, fix existe) était correct. Pattern : LLM mélange knowledge cutoff + invention plausible pour combler les trous.

**How to apply** :
- Claim type "version X.Y.Z fixe le bug" → WebFetch raw CHANGELOG avant de croire/citer
- Claim type "repo X a N étoiles, créé en YYYY" → WebFetch GitHub direct
- Claim type "Boris fait N sessions parallèles" → vérifier source primaire (site Boris, talk Anthropic)
- Symétrique de [[feedback_tweet_hype_paraphrase_pattern]] mais pour deep research LLM, pas tweets
- Le **fait qualitatif** peut être vrai même quand les **chiffres sont faux** — distinguer les deux dans le verdict

Voir aussi [[feedback_arxiv_url_swap_papers_similaires]] (LLM swap URLs papers similaires) et [[feedback_anthropic_single_source_suffit]] (canonical source > paraphrase).
