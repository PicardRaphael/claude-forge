---
titre: "Takeshi Kojima"
resume: "Auteur principal de 'Large Language Models are Zero-Shot Reasoners' (NeurIPS 2022) — paper qui introduit 'Let's think step by step'. Matsuo-Iwasawa Lab, University of Tokyo"
aliases:
  - "Takeshi Kojima"
  - "takeshi kojima"
  - "Kojima"
  - "zero-shot CoT author"
  - "Let's think step by step"
  - "Matsuo Lab"
domaine: prompt-engineering
type: leader
affiliation: "Matsuo-Iwasawa Lab, University of Tokyo"
derniere-maj: 2026-05-24
auteur: claude
sources:
  - "https://arxiv.org/abs/2205.11916"
  - "https://weblab.t.u-tokyo.ac.jp/en/news/2022-09-16/"
  - "https://weblab.t.u-tokyo.ac.jp/en/news/20240611/"
tags:
  - "#type/leader"
  - "#domaine/prompt-engineering"
  - "#domaine/llm-reasoning"
---

## Profil

PhD student au **Matsuo-Iwasawa Lab** (University of Tokyo), depuis 2020. Yutaka Matsuo et Yusuke Iwasawa = directeurs de thèse.

## Contribution canonique

### "Large Language Models are Zero-Shot Reasoners" (NeurIPS 2022)

[arXiv 2205.11916](https://arxiv.org/abs/2205.11916). Auteurs : **Takeshi Kojima** (1er auteur), Shixiang Shane Gu et Machel Reid (Google Research, Brain Team), Yutaka Matsuo et Yusuke Iwasawa (UTokyo).

**Découverte fondatrice** : ajouter simplement *"Let's think step by step"* avant la réponse extrait un raisonnement complet du modèle — **sans aucun exemple**. Zero-shot CoT.

Process en 2 étapes :
1. Premier prompt : question + "Let's think step by step" → modèle produit raisonnement complet
2. Second prompt : extraire la réponse finale

> ⚠️ Distinction critique : Kojima 2022 = **zero-shot CoT**. Wei et al 2022 (arxiv 2201.11903) = **few-shot CoT** avec démonstrations. Les deux papers sont souvent confondus.

**Impact** : >2000 citations en moins de 2 ans (au 24 mai 2024). Une des techniques les plus citées du domaine.

### Inspiration

Kojima dit avoir tiré l'idée du paper de Google researchers de janvier 2022 (Wei et al CoT). Son intuition : appliquer ça en **zero-shot**.

### Test-time adaptation

Kojima et collègues appellent ces méthodes **"test-time adaptation"** — techniques qui aident les modèles à corriger leur output sans fine-tuning. Avant les LLM, ils avaient déjà expérimenté ça en computer vision.

## Pourquoi le citer

Source primaire **single source acceptable** sur :
- Zero-shot CoT et "Let's think step by step" (auteur original)
- Test-time adaptation framing

Pour des claims plus larges sur prompt engineering = 4+ sources.

## Pattern d'erreur fréquent

Beaucoup de notes attribuent "Let's think step by step" à Wei et al 2022 — c'est FAUX. Wei 2022 = CoT few-shot avec démonstrations. Kojima 2022 = zero-shot, et c'est lui qui introduit la phrase magique.

## Liens

- [[Jason Wei]] — paper CoT few-shot (à ne pas confondre)
- [[Denny Zhou]] — Reasoning Team Google DeepMind
- [[chain-of-thought]] — note technique vault
- [[MOC-Leaders]]
