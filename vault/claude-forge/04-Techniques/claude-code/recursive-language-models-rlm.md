---
titre: "Recursive Language Models (RLMs) — le prompt comme variable externe dans un REPL"
resume: "Paradigme d'inférence (MIT CSAIL, Khattab) : le modèle traite le long prompt comme une variable externe dans un REPL Python et écrit du code pour l'inspecter/chunker/s'auto-appeler récursivement. Gère des inputs ~2 ordres de grandeur au-delà du contexte, bat les LLM frontière sur long-contexte. Nouvel axe de test-time compute."
aliases:
  - "recursive language models"
  - "RLM"
  - "modèles de langage récursifs"
  - "prompt as external variable REPL"
  - "context folding RLM"
  - "arxiv 2512.24601"
derniere-maj: 2026-06-16
auteur: claude
type: technique
sources:
  - "https://arxiv.org/abs/2512.24601"
  - "https://github.com/alexzhang13/rlm"
  - "https://www.primeintellect.ai/blog/rlm"
tags:
  - "#type/technique"
  - "#domaine/agents"
  - "#domaine/prompt-engineering"
  - "#domaine/llm-reasoning"
---

# Recursive Language Models (RLMs)

> arXiv 2512.24601 — Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL). Soumis 31 déc 2025, v3 révisée 11 mai 2026.

## Le concept

Au lieu de charger tout le long prompt dans le contexte, le modèle le **traite comme une variable externe dans un REPL Python**. Le modèle écrit du **code** pour inspecter, chunker, et **s'appeler lui-même récursivement** sur des segments. Seuls les résultats pertinents remontent.

Conséquence : gère des inputs **~2 ordres de grandeur au-delà de la fenêtre de contexte**, et bat les LLM frontière vanille sur les tâches long-contexte — vs GPT-5 : +26% over compaction, +130% over CodeAct sub-calls ; **+13% over Claude Code** (chiffres du paper/blog, à confirmer en lisant le PDF primaire avant de les citer comme définitifs).

## Pourquoi c'est stratégique pour forge

RLM est un **nouvel axe de test-time compute scaling** (orthogonal au « penser plus longtemps ») et il **intersecte directement la doctrine context-engineering / leaf-node de forge** :
- Le pattern « la session principale orchestre, les sous-agents isolent le contexte » est une version manuelle de ce que RLM automatise (récursion + isolation de contexte).
- Converge avec les sous-agents imbriqués CC v2.1.172 (récursion native) et le pattern reviewer→verifier (cf [[anti-reentrance-sub-agents-pattern-escalade]] § AJOUT 16 juin).
- RL-tunable : des modèles 4B entraînés comme RLM natifs. Prime Intellect le qualifie de « best method for context folding ».

## À surveiller

Paradigme de recherche récent (pas encore un outil grand public). Vérifier le PDF arXiv primaire avant de capitaliser les chiffres exacts (gains %, tailles) — pattern hallucination chiffrée des résumés deep-research.

## Wikilinks

- [[anti-reentrance-sub-agents-pattern-escalade]] — orchestration / isolation de contexte (version manuelle)
- [[Andrej Karpathy]] — context window = RAM, ton job = l'OS (Software 3.0)
- [[Omar Khattab]] — co-auteur (DSPy, late interaction)
- [[MOC-Techniques]]
