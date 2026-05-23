---
titre: "Fine-Tuning Evaluation — Benchmarks, LLM-as-Judge, Métriques"
resume: "Guide évaluation de modèles fine-tunés — 3 couches (benchmarks, LLM-as-judge, humain), outils (lm-eval-harness, Lighteval, DeepEval), métriques clés"
aliases:
  - "fine-tuning evaluation"
  - "évaluation LLM"
  - "LLM-as-judge"
  - "lm-evaluation-harness"
  - "Lighteval"
  - "DeepEval"
  - "benchmarks LLM"
type: technique
domaine: ia
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://github.com/EleutherAI/lm-evaluation-harness"
  - "https://github.com/huggingface/lighteval"
  - "https://arxiv.org/pdf/2410.12784"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/fine-tuning"
  - "#domaine/evaluation"
---

## Approche 3 couches

### 1. Benchmarks automatisés (baseline)

Avant/après fine-tuning. Rapide, reproductible, détecte les régressions.

| Outil | Stars | Forces |
|-------|-------|--------|
| **lm-evaluation-harness** (EleutherAI) | ~12.7K | 60+ benchmarks, backend HF Leaderboard |
| **Lighteval** (HuggingFace) | ~2.4K | 1000+ tasks, multi-backend (vLLM, SGLang) |
| **DeepEval** | ~15.6K | 40+ métriques (Agentic, RAG, Multi-Turn, MCP, Multimodal) |

### 2. LLM-as-Judge (calibration)

GPT-4/Claude juge les outputs sur : helpfulness, accuracy, harmlessness.

**Limitation :** sous-estime les erreurs edge cases. **Skywork-Critic-Llama-3.1-8B** atteint **57.43% accuracy** sur [JudgeBench](https://arxiv.org/abs/2410.12784). **JudgeBench** (Tan, Zhuang, Stoica et al., [arXiv 2410.12784](https://arxiv.org/abs/2410.12784), **ICLR 2025** — confirmé dans le PDF) est le standard pour évaluer les judges.

### 3. Évaluation humaine (ground truth)

10% spot check calibre sans nécessiter review complète. Indispensable pour : erreurs factuelles plausibles, problèmes de ton, inexactitudes domaine-spécifiques.

## Métriques Post Fine-Tuning

| Métrique | Ce qu'elle dit | Outil |
|----------|---------------|-------|
| Performance tâche cible | Le fine-tuning a-t-il marché ? | Eval spécifique (accuracy, F1, BLEU) |
| Rétention capacités base | Le modèle est-il cassé globalement ? | MMLU, HellaSwag avant/après |
| Taux d'hallucination | Le modèle invente-t-il plus qu'avant ? | TruthfulQA, DeepEval |
| Instruction following | Le modèle suit-il mieux les instructions ? | IFEval, MT-Bench |
| Safety | Le fine-tuning a-t-il supprimé les guardrails ? | HarmBench |

## Liens

- [[MOC-Techniques]]
- [[fine-tuning-datasets]] — qualité des données
- [[fine-tuning-techniques-peft]] — techniques à évaluer