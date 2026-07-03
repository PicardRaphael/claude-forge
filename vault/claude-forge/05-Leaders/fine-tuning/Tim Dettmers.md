---
titre: "Tim Dettmers"
resume: "Créateur de QLoRA et bitsandbytes, Assistant Professor CMU, Research Scientist AI2, démocratisation du fine-tuning consumer GPU"
aliases:
  - "tim dettmers"
  - "Tim Dettmers"
  - "Tim_Dettmers"
  - "QLoRA creator"
  - "bitsandbytes"
  - "créateur QLoRA"
  - "expert QLoRA"
  - "consumer GPU training"
  - "quantization research"
role: "Assistant Professor CMU / Research Scientist AI2"
domaine: ia
type: leader
derniere-maj: 2026-07-02
auteur: claude
sources:
  - "https://timdettmers.com/about/"
  - "https://github.com/bitsandbytes-foundation/bitsandbytes"
tags:
  - "#type/leader"
  - "#domaine/ia"
  - "#domaine/fine-tuning"
  - "#domaine/quantization"
---

## Profil

Créateur de **QLoRA** et **bitsandbytes** (millions de downloads mensuels). Assistant Professor à CMU et Research Scientist à l'Allen Institute for AI (AI2).

## Contributions clés

- **QLoRA** — fine-tune un modèle 65B sur un seul GPU 48GB. Démocratisation du fine-tuning
- **bitsandbytes** — librairie de quantization 4-bit, intégrée au stack HuggingFace
- **k-bit inference scaling laws** — lois d'échelle pour l'inférence quantizée

## Travaux récents (2025-2026)

Pivot de la quantization (rendements décroissants) vers les **coding agents**. _Note : claim "pause santé depuis février 2025" présent antérieurement retiré car non vérifiable publiquement._

### SERA (jan 2026) — attribution AI2, Dettmers senior author

**SERA (Soft-Verified Efficient Repository Agents)** — méthode **SFT-only** (Soft Verified Generation, sans unit tests) pour entraîner des coding agents spécialisés sur codebases privées. ⚠️ **PAS un travail solo de Dettmers** : papier **Allen Institute for AI (AI2)**, auteurs **Ethan Shen, Daniel Tormoen, Saurabh Shah, Ali Farhadi, Tim Dettmers** (Dettmers = **senior author**).

Claims (vérifiés source primaire — vivent dans l'**arXiv abstract / blog AI2**, PAS le blog perso Dettmers) :
- **26× moins cher que le RL** (match SkyRL à 26× lower cost)
- **57× moins cher que les méthodes synthetic data** précédentes (match SWE-smith à 57× lower cost)
- **Égale Devstral-Small-2** : SERA-32B **49.5 % ±1.9 %** vs Devstral Small 2 **50.0 % ±1.3 %** sur SWE-Bench Verified (32K) ; 54.2 % ±1.4 % à 64K
- Teacher GLM-4.5-Air, 200 000+ trajectoires synthétiques

Sources : arXiv **2601.20789** · blog AI2 [open-coding-agents](https://allenai.org/blog/open-coding-agents) · récit compagnon (autre cadrage/chiffres) [timdettmers.com/2026/01/27/building-open-coding-agent-sera](https://timdettmers.com/2026/01/27/building-open-coding-agent-sera/). **Citer les chiffres 26×/57×/Devstral → sourcer arXiv/AI2, jamais le blog perso.**

## Liens

- [[MOC-Leaders]]
- X : [@Tim_Dettmers](https://x.com/Tim_Dettmers)
- Blog : [timdettmers.com](https://timdettmers.com/)
- [[fine-tuning-techniques-peft]] — QLoRA en détail
- [[Edward Hu]] — LoRA, base de QLoRA
