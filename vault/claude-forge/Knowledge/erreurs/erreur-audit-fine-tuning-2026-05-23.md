---
titre: "Audit fine-tuning 2026-05-23 — 22 corrections sur 87 claims"
resume: "Audit thématique fine-tuning vault : 87 claims auditées via 7 sub-agents, 22 corrigées (Type 1/2/3). Pattern récurrent : venues de conférence inventées, stars GitHub périmées, claims chiffrés Lamini/TrueFoundry à scoper."
aliases:
  - "audit fine-tuning 23 mai"
  - "audit fine-tuning 2026"
  - "erreur fine-tuning"
  - "22 corrections fine-tuning"
  - "fine-tuning audit"
  - "stars-github-drift"
type: erreur
domaine: ia
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://arxiv.org/abs/2410.21228"
  - "https://arxiv.org/abs/2410.12784"
  - "https://github.com/pytorch/torchtune"
tags:
  - "#type/erreur"
  - "#domaine/ia"
  - "#domaine/fine-tuning"
  - "#domaine/audit"
---

## Contexte

Second audit thématique vault après l'audit Claude Code 23 mai (95 claims, 22 erreurs). Méthode validée : lecture parallèle notes, inventaire claims (checkpoint), 7 sub-agents parallèles WebFetch direct par cluster, self-verify avant correction, classement Type 1/2/3, application par vagues.

## Résultats

- **87 claims auditées** sur 10 notes (`MOC-Fine-Tuning` + 9 notes thématiques)
- **55 confirmées** (~63%)
- **22 corrigées** (~25%)
- **10 invérifiables/reformulées** (~12%)

## Erreurs typées

### Type 1 — Citations / sources / venues fausses (8 cas)

- **C1.13 "Insight NeurIPS 2025 intruder dimensions"** → paper réel = arXiv 2410.21228 (Shuttleworth et al, MIT, oct 2024), **aucune venue confirmée**. Pattern identique à l'audit RAG 23 mai (TOOLQP "ICLR 2025").
- **C2.6 / C2.7** : SimPO et KTO créateurs manquants → Yu Meng (Princeton) / Kawin Ethayarajh (Contextual AI, ICML 2024)
- **C5.5 Gemma 3** : "2B-31B Apache 2.0" FAUX → 1B/4B/12B/27B, **Gemma Terms of Use** (pas Apache)
- **C7.8 TrueFoundry** : "Medtronic" FAUX → ResMed ; "17M inférences cliniques/mois" non sourcé
- **C5.2 Llama 88.4% HumanEval** : modèle exact manquant → Llama 3.3 70B Instruct, 0-shot pass@1

### Type 2 — Chiffres inventés / drift (10 cas)

- **Stars GitHub drift majeur** :
  - Unsloth 54K → **65K**
  - MLX 4K → **26.4K** (×6 sous-estimé)
  - LLaMA-Factory 68K → **71.5K**
  - DeepEval 5K → **15.6K** (×3 sous-estimé)
  - Label Studio 20K → **27K**
- **Spectrum "-36% vs full FT"** : chiffre non sourcé → retiré
- **GRPO "-50% vs PPO"** : chiffre non dans paper DeepSeekMath → retiré
- **FSDP "5x plus rapide que DeepSpeed ZeRO-3"** : non sourcé → reformulé
- **Together AI "$29"** : confusion training/inference → précisé
- **AWS Bedrock "$80"** : unité floue → distinction training/inference/PT
- **Neoclouds "40-70%"** → **40-85%** (source Spheron)

### Type 3 — Doctrine fausse / obsolète (4 cas)

- **torchtune "PyTorch-native, Meta-backed"** OBSOLÈTE → **"no longer actively maintained, development wound down 2025"** (README officiel). Sorti des frameworks recommandés.
- **TGI "MAINTENANCE"** → confirmé empiriquement : **archivé GitHub 21 mars 2026**, HF redirige vers vLLM/SGLang/llama.cpp/MLX
- **EU AI Act "conformité complète août 2026"** OBSOLÈTE → accord politique mai 2026 reporte high-risk Annex III à déc 2027
- **Lamini "95% vs 50%"** : à scoper "case study Fortune 500 spécifique" partout (pas benchmark généralisé)

## Pattern récurrents (compounding)

1. **Venues inventées** : NeurIPS 2025, ICLR 2025 cités sans vérification PDF. Reproduit le pattern audit RAG 23 mai. **Règle** : si venue pas dans abstract arXiv → ne pas l'affirmer.
2. **Stars GitHub vieillissent vite** : drift x3-x6 sur DeepEval/MLX en 6 mois. **Règle** : re-vérifier stars > 6 mois.
3. **Chiffres marketing non vérifiés** : Lamini, TrueFoundry, claims clients. **Règle** : toujours scoper "case study X" vs "benchmark généralisé".
4. **Confusion training vs inference pricing** : $29, $80 sans unité. **Règle** : préciser systématiquement (training/inference/PT, $/M tokens vs $/hr).

## Action capitalisée

- Mise à jour 9 notes vault fine-tuning (toutes sauf MOC)
- Création de cette note erreur
- CHANGELOG.md + log.md à jour
- Pattern compounding documenté pour future audit thématique

## Liens

- [[methode-analyser-repo]] — méthode ABCDE
- [[erreur-22-claims-fausses-vault-claude-code-2026-05-23]] — audit Claude Code (cousin)
- [[fine-tuning-techniques-peft]] / [[fine-tuning-alignment]] / [[fine-tuning-frameworks]] / [[fine-tuning-infrastructure]] / [[fine-tuning-models]] / [[fine-tuning-privacy]] / [[fine-tuning-datasets]] / [[fine-tuning-evaluation]] / [[rag-vs-fine-tuning]]
