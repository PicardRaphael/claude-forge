---
titre: "Jason Wei"
resume: "Inventeur de Chain-of-Thought prompting (NeurIPS 2022), instruction tuning (FLAN), emergent abilities. Carrière Google Brain → OpenAI (o1, deep research) → Meta Superintelligence Labs"
aliases:
  - "Jason Wei"
  - "jason wei"
  - "Wei"
  - "CoT auteur"
  - "FLAN author"
  - "emergent abilities author"
domaine: prompt-engineering
type: leader
affiliation: "Meta Superintelligence Labs (ex-OpenAI, ex-Google Brain)"
derniere-maj: 2026-05-24
auteur: claude
sources:
  - "https://www.jasonwei.net/"
  - "https://arxiv.org/abs/2201.11903"
  - "https://arxiv.org/abs/2206.07682"
tags:
  - "#type/leader"
  - "#domaine/prompt-engineering"
  - "#domaine/llm-reasoning"
---

## Profil

Bachelor CS Dartmouth College (2016-2020, advisor Lorenzo Torresani). Thomas Jefferson High School for Science and Technology.

Carrière :
- 2020 : Google AI Residency
- 2020-2023 : Research engineer/scientist Google Brain
- 2023-2025 : OpenAI (research reasoning + agents, o1 et deep research)
- 2025+ : Meta Superintelligence Labs

## Contributions canoniques

### Chain-of-Thought Prompting (2022)

[arXiv 2201.11903](https://arxiv.org/abs/2201.11903) — *"Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"* (NeurIPS 2022). Auteurs : Wei, Wang, Schuurmans, Bosma, Xia, Chi, Le, Zhou.

Technique fondamentale : générer une chaîne d'étapes de raisonnement intermédiaires améliore drastiquement les performances LLM sur tâches arithmétiques, commonsense, symboliques. Émerge naturellement chez les modèles suffisamment grands.

> Note distinction : Wei 2022 = **few-shot CoT** (avec démonstrations). "Let's think step by step" zero-shot = [[Takeshi Kojima]] 2022.

### Instruction Tuning & FLAN

Lead du développement FLAN (Finetuned Language Net). Fine-tuning LLM sur mélange d'instructions naturelles → amélioration drastique zero-shot et few-shot performance.

FLAN-T5, FLAN-PaLM : techniques fondationnelles du deployment LLM moderne.

### Emergent Abilities (2022)

Paper concept fondateur — capacités LLM qui apparaissent abruptement avec le scale. Pionnier de l'idée des "thresholds émergents" largement discutée depuis ChatGPT.

### OpenAI o1 & Deep Research (2023-2025)

Participation à la recherche et développement des modèles o1 et deep research — cœur = reasoning ability. Modèles qui ont popularisé le "thinking mode" adopté ensuite par Anthropic (Claude extended thinking), Google (Gemini Deep Think), DeepSeek R1.

## Impact

CoT donne aux modèles une capacité de raisonnement type "System 2" (Kahneman) vs "System 1" intuitive. Idée adoptée par les thinking modes de toutes les frontier models depuis 2024.

> *"His departure from OpenAI meant losing not just a researcher capable of executing complex projects, but also a 'visionary' with the ability to change the entire field's landscape."* — 36kr profile

## Pourquoi le citer

Source primaire **single source acceptable** sur :
- Chain-of-Thought (auteur original)
- FLAN instruction tuning
- Emergent abilities concept

Pour ses propres papers et travaux = single source. Pour des claims génériques prompt engineering hors de son scope = 4+ sources.

## Liens

- [[Denny Zhou]] — co-auteur CoT, Self-Consistency, ToT
- [[Takeshi Kojima]] — zero-shot CoT (distinction)
- [[Shunyu Yao]] — Tree of Thoughts, ReAct
- [[MOC-Leaders]]
