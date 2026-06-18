---
titre: "Zach Lloyd — Warp, le terminal comme workbench de l'IA"
resume: "Fondateur & CEO de Warp (ex-Principal Eng Google Docs). Thèse : le terminal est le poste de travail naturel de l'IA pour orchestrer des agents ; 'coding will be solved', le prochain goulot est l'expression de l'intention humaine. 3 stades du coding IA (inline → agentique → event-triggered)."
aliases:
  - "Zach Lloyd"
  - "zachlloyd"
  - "zachlloydtweets"
  - "Warp founder"
  - "Warp CEO"
  - "terminal as AI workbench"
role: "Fondateur & CEO"
affiliation: "Warp"
derniere-maj: 2026-06-18
auteur: claude
sources:
  - "https://x.com/zachlloydtweets/status/2066908445425496348"
  - "https://sequoiacap.com/podcast/making-the-case-for-the-terminal-as-ais-workbench-warps-zach-lloyd/"
  - "https://thenewstack.io/how-warp-went-from-terminal-to-agentic-development-environment/"
  - "https://www.gv.com/news/ai-agent-warp"
tags:
  - "#type/leader"
  - "#domaine/warp"
  - "#leader/claude-code"
---

## Profil

Fondateur et CEO de [[Warp]] (terminal Rust → ADE). Ancien **Principal Engineer sur Google Docs** avant de lancer Warp en 2022. Auteur d'un livre (thezbook.com). Twitter `@zachlloydtweets`.

Profil : ingénieur produit devenu fondateur d'infra développeur. Sa pertinence vient de sa thèse contrarian sur **le terminal comme surface centrale de l'IA** — à un moment où l'attention va aux IDE (Cursor) et au web (Claude Code on the web).

## Contributions clés

### 1. Le terminal comme workbench de l'IA

> *« You can multitask agents in the terminal really easily, and so I think it's been like actually a great stroke of luck for us that the terminal has become the center of agentic development. »*

L'interface texte + temporelle du terminal est, selon lui, structurellement adaptée à l'orchestration d'agents, au multitâche et au logging — mieux qu'un IDE graphique. C'est le pari produit de Warp 2.0 (ADE).

### 2. Les 3 stades du coding IA

1. **Complétions inline** (Copilot, premier Cursor)
2. **Coding agentique** (la transition « des derniers mois »)
3. **Déclenché par événements système** — l'agent s'auto-invoque sur un crash report, un ticket utilisateur, etc.

### 3. « Coding will be solved » — l'intention humaine devient le goulot

Sa thèse la plus citée : la capacité technique à générer du code fonctionnel deviendra ubiquitaire (« coding will be solved » d'ici quelques années). Le vrai goulot devient alors **l'expression claire de l'intention humaine** et le guidage des agents. Horizon 2030 : pas moins d'ingénieurs, mais **beaucoup plus de logiciel**, produit à un niveau d'abstraction supérieur.

## Positions récentes

- Lancement de **Warp Code** puis **Warp 2.0 / ADE** (4 piliers Code/Agents/Terminal/Drive) — voir [[Warp]]
- **Oz** : plateforme cloud d'orchestration qui pilote *aussi* Claude Code et Codex — Warp se place en couche méta sur les CLI concurrentes
- Interview podcast **Sequoia** « Making the Case for the Terminal as AI's Workbench » (2026)

## Alignement / résonance forge

Sa thèse « l'intention humaine = prochain goulot » converge avec :
- [[Boris Cherny]] — *« engineer's value shifts to the decisions above the code »* (quoi/pourquoi/comment ça s'assemble)
- [[addy-osmani]] — *« the bottleneck was always judgment, taste, and systems thinking »*
- [[concevoir-loops-travail]] — son stade 3 (event-triggered) = un loop déclenché par événement plutôt que par horaire

## Note d'hiérarchie des sources

Lloyd = source **secondaire** (fondateur d'un outil concurrent, discours en partie marketing). Excellent en **framing stratégique** (3 stades, intention-as-bottleneck) ; les chiffres produits Warp (benchmarks, productivité) sont auto-déclarés → vérifier en source primaire avant de les citer comme faits. En cas de conflit doctrinal, suivre les sources primaires Anthropic (couche 1).

## Liens

- [[Warp]] — son produit
- [[Boris Cherny]] · [[addy-osmani]] — convergence sur le déplacement de la valeur ingénieur
- [[harness-engineering]] — l'ADE comme harness produit
- [[Gemini CLI]] · [[Cursor]] — autres acteurs du dev IA
