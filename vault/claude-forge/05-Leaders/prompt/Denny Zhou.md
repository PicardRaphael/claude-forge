---
titre: "Denny Zhou"
resume: "Research Scientist Google DeepMind, fondateur Reasoning Team Google Brain (intégrée dans Gemini). Co-auteur CoT, Self-Consistency, Least-to-Most, ToT. Surnommé 'the king of reasoning'"
aliases:
  - "Denny Zhou"
  - "denny zhou"
  - "Zhou"
  - "king of reasoning"
  - "Google Brain Reasoning Team founder"
domaine: prompt-engineering
type: leader
affiliation: "Google DeepMind"
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://dennyzhou.github.io/"
  - "https://scholar.google.com/citations?user=UwLsYw8AAAAJ"
  - "https://www.linkedin.com/in/denny-zhou-7695487"
  - "https://arxiv.org/abs/2201.11903"
  - "https://arxiv.org/abs/2203.11171"
tags:
  - "#type/leader"
  - "#domaine/prompt-engineering"
  - "#domaine/llm-reasoning"
---

## Profil

Research Scientist à **Google DeepMind**. A fondé la **Reasoning Team chez Google Brain**, désormais intégrée à l'équipe Gemini de Google DeepMind. Objectif déclaré : aider à résoudre l'AGI en construisant des LLM capables de raisonner et atteindre la generalization parfaite.

Surnommé **"the king of reasoning"** par ses pairs.

## Contributions canoniques

Approche structurée du raisonnement LLM autour de 4 piliers :

### 1. Chain-of-Thought (2022)

Co-auteur du paper CoT avec Jason Wei et al — [arXiv 2201.11903](https://arxiv.org/abs/2201.11903). Ajouter des étapes intermédiaires avant la réponse finale.

### 2. Self-Consistency (2022)

Co-auteur **senior** — [arXiv 2203.11171](https://arxiv.org/abs/2203.11171) "Self-Consistency Improves Chain of Thought Reasoning **in Language Models**". **Premier auteur = Xuezhi Wang**, Zhou = senior. Sampler plusieurs réponses, choisir la plus fréquente. Améliore CoT.

### 3. Least-to-Most Prompting

Décomposer un problème en sous-parties et les résoudre individuellement.

### 4. Instruction following

Recherches sur la capacité des LLM à suivre des instructions naturelles.

### Théorème transformer ↔ raisonnement

Avec son équipe, a **mathématiquement prouvé que les transformers peuvent résoudre n'importe quel problème** s'ils peuvent générer autant de tokens de raisonnement intermédiaires que nécessaire.

### Autres publications majeures

- *"Large Language Models as Optimizers"* (arXiv 2023)
- *"Large Language Models as Tool Makers"* (arXiv 2023)
- *"Language Models are Multilingual Chain-of-Thought Reasoners"* (ICLR 2023)
- *"Teaching Large Language Models to Self-Debug"*

## Awards

- Google Research Tech Impact Award 2022
- WSDM Test of Time Award 2022
- General Chair de la 1ère Conference on Language Modeling (COLM) 2024

## Citation utile

> *"Always keep in mind that LLMs are probabilistic models of generating next tokens. They are not humans."*
> — Denny Zhou

> *"Reasoning in LLMs = simply generating a sequence of intermediate tokens before producing the final answer."*

Définition opérationnelle (vs philosophique) du reasoning en LLM.

## Pourquoi le citer

Source primaire **single source acceptable** sur :
- CoT, Self-Consistency, Least-to-Most (co-auteur)
- Reasoning research chez Google DeepMind
- Définition opérationnelle du reasoning LLM
- Théorème transformer/reasoning

## Liens

- [[Jason Wei]] — co-auteur CoT et Self-Consistency
- [[Takeshi Kojima]] — zero-shot CoT
- [[Shunyu Yao]] — ToT, ReAct
- [[MOC-Leaders-Prompt]]
