---
titre: "Brad Abrams"
resume: "Product Management Lead Claude chez Anthropic, ex-Google/Microsoft. Créateur de l'Advisor Strategy (Code with Claude SF 2026, talk avec Mario Rodriguez GitHub CPO). Pattern executor+advisor pour cost reduction sans perte d'intelligence."
aliases:
  - "Brad Abrams"
  - "brad abrams anthropic"
  - "advisor strategy auteur"
  - "product lead claude"
  - "Bradley Abrams"
derniere-maj: 2026-05-23
auteur: claude
type: leader
sources:
  - "https://www.linkedin.com/in/brabrams/"
  - "https://x.com/brada"
  - "https://claude.com/code-with-claude/session/sf-caching-harnesses-and-advisors-building-on-claude-at-github-scale"
  - "https://www.infoq.com/news/2026/05/code-with-claude/"
tags:
  - "#type/leader"
  - "#domaine/claude-code"
  - "#projet/anthropic"
---

# Brad Abrams

> Product Management Lead Claude chez Anthropic — créateur de l'Advisor Strategy.

## QUI

Bradley Abrams — Product Manager Lead at Anthropic, working on Claude. Background : ex-Google, ex-Microsoft. LinkedIn : [brabrams](https://www.linkedin.com/in/brabrams/). X : [@brada](https://x.com/brada).

Spokesperson et demo presenter récurrent aux Anthropic developer events (Code with Claude SF 2026, webinaires, Computer Use launch, Skills launch).

## CE QU'IL APPORTE

### 1. Advisor Strategy — pattern majeur 2026

Pattern présenté à **Code with Claude SF 6 mai 2026** dans le talk *"Caching, harnesses, and advisors: Building on Claude at GitHub scale"* avec **Mario Rodriguez** (GitHub CPO).

**Le pattern** :
- **Executor model** : smaller (Haiku), exécute la majorité des appels
- **Advisor model** : larger (Opus), consulté ponctuellement quand l'executor demande conseil
- Goal : cost efficiency sans sacrifier l'intelligence

**Verbatim Abrams** :
> "We get close to Opus-level intelligence at much lower prices because we're being very conservative about the tokens that advisor actually sends"

Pattern utilisé chez **GitHub Copilot** à scale, avec Mario Rodriguez framing le **cache hit rate** comme métrique foundational ("kind of like high frequency trading — just 1% efficiency means millions overall"), target > 94% chez GitHub.

### 2. Skills (positions publiques)

Cité comme product lead sur les Skills :
> "The thing that's interesting to me about Skills is basically about agents."
> "It's not about hitting benchmark numbers — it's about getting real work done at your actual company."

Early enterprise customers Skills (selon Anthropic release) : Box, Canva, Rakuten.

### 3. Platform sessions CwC SF 2026

Session standalone "Claude Platform" — prompt caching, structured outputs, tool design patterns observés cross customers running large workloads.

## ⚠️ Coquille forge corrigée 23 mai 2026

**Avant 23 mai 2026** : le vault forge attribuait l'Advisor Strategy à "Angela Jiang 5× cost reduction".

**Source de la coquille** : live blog Simon Willison "Angela Kiang" → propagé comme "Angela Jiang" → forge a inventé "5× cost reduction" non sourcé.

**Source canonique** : Brad Abrams + Mario Rodriguez à CwC SF. Pas de chiffre "5×" verbatim, mais "close to Opus-level intelligence at much lower prices".

## SOURCES

- [LinkedIn profile](https://www.linkedin.com/in/brabrams/)
- [X/Twitter @brada](https://x.com/brada/status/1910709143289340102)
- [Code with Claude SF — Caching, harnesses, advisors session](https://claude.com/code-with-claude/session/sf-caching-harnesses-and-advisors-building-on-claude-at-github-scale)
- [InfoQ — Anthropic's Code with Claude](https://www.infoq.com/news/2026/05/code-with-claude/)
- LinkedIn posts : Computer Use launch, Building Blocks for Tomorrow's AI Agents, Amazon Bedrock AgentCore

## WIKILINKS

- [[comment-creer-agent]] — Advisor Strategy documentée
- [[workflow-claude-code-optimal]] — pattern intégré workflow
- [[mcp-vs-skills-doctrine]] — Skills doctrine
- [[Mario-Rodriguez]] — GitHub CPO, co-talk CwC SF
- [[Code with Claude 2026]] — événement
