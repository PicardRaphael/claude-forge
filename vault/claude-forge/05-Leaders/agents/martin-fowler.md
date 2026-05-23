---
titre: "Martin Fowler & Birgitta Böckeler — Guides+Sensors taxonomy"
resume: "martinfowler.com publie 2 avril 2026 la taxonomie Guides+Sensors (Böckeler, Thoughtworks) qui structure le harness en feedforward inferentiel/computationnel et feedback inferentiel/computationnel — evidence LangChain 52.8% → 66.5% Terminal Bench à modèle constant"
aliases:
  - "Martin Fowler"
  - "martin fowler"
  - "Birgitta Böckeler"
  - "Böckeler"
  - "Guides+Sensors"
  - "Guides and Sensors"
  - "harness engineering Fowler"
  - "agent = model + harness"
derniere-maj: 2026-05-22
auteur: claude
type: leader
sources:
  - "https://martinfowler.com/articles/harness-engineering.html"
tags:
  - "#type/leader"
  - "#domaine/agents"
  - "#domaine/harness-engineering"
  - "#leader/agents"
---

# Martin Fowler & Birgitta Böckeler — Guides+Sensors taxonomy

## QUI

**Martin Fowler** — Chief Scientist émérite Thoughtworks, l'une des figures historiques du génie logiciel (refactoring, microservices, *Patterns of Enterprise Application Architecture*, *Refactoring*). Son site **martinfowler.com** est une référence canonique pour les patterns ingénierie depuis 20 ans.

**Birgitta Böckeler** — Distinguished Engineer Thoughtworks, **co-auteure principale** de l'article. Spécialiste AI-assisted software engineering chez Thoughtworks. C'est **elle** qui signe l'article ; Martin Fowler éditorialise via son site.

Profil : couche 3 (secondaire) — pas Anthropic, pas Karpathy. Mais Fowler = **bouche officielle de l'industrie** pour valider/codifier un concept. Quand Fowler publie sur un sujet, il devient mainstream.

## POURQUOI EST PERTINENT

Böckeler/Fowler ont produit la **première taxonomie rigoureuse** du harness, qui structure proprement la conversation. Avant cet article, "harness engineering" (cf [[hashimoto]]) était un slogan ; après, c'est un cadre exploitable :

- **Guides** (feedforward, anticipatif)
- **Sensors** (feedback, correctif)
- Chacun en deux variantes : **computational** (déterministe) vs **inferential** (probabiliste, LLM)

C'est la grille **la plus utile** pour décider "skill ou hook ?", "rule ou test ?", "linter ou code review IA ?".

## CONTRIBUTIONS CLÉS

### 1. La formule canonique

> "Agent = Model + Harness"

Reprise de [[hashimoto]], mais Fowler/Böckeler la **rendent officielle** côté industrie. Distingue **inner harness** intégré (Claude Code, Codex) et **outer harness** user-built (prompts, rules, hooks projet).

### 2. La taxonomy Guides + Sensors

| Dimension | Type | Exécution | Exemples |
|-----------|------|-----------|----------|
| **Guides** (feedforward) | Anticipatif | **Computational** | LSP, bootstrap scripts, OpenRewrite codemods |
| **Guides** (feedforward) | Anticipatif | **Inferential** | AGENTS.md, Skills, coding convention docs |
| **Sensors** (feedback) | Correctif | **Computational** | ESLint, ArchUnit, dep-cruiser, mutation testing |
| **Sensors** (feedback) | Correctif | **Inferential** | AI code review agents, architecture review Skills |

Distinction clé :
- **Computational** = déterministe, fast (ms-s), reproducible
- **Inferential** = probabiliste, slower, GPU, mais gère semantic judgment

### 3. Evidence empirique LangChain (février 2026)

Sur **Terminal Bench 2.0**, même modèle (gpt-5.2-codex), même API :
- **52.8% → 66.5% (+13.7pp)** par harness changes seuls
- Rank **Top 30 → Top 5**

> "No fine-tuning, no model swap, just harness changes."

**Source canonique** : [LangChain blog — Improving Deep Agents with Harness Engineering](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/) — concept Fowler/Böckeler (martinfowler.com 2 avril 2026), chiffres LangChain blog.

C'est l'evidence "harness > model" la plus citée après Addy +21.8 pts (cf [[addy-osmani]]).

### 4. Les 7 recommandations pratiques

1. Combiner feedforward + feedback (ni l'un ni l'autre seul ne suffit)
2. **Shift quality left** : computational sensors rapides (linters, unit tests) avant commit ; inferential sensors lourds (mutation, archi review) post-integration
3. **Prioriser computational sensors d'abord** (catch structurel cheap + déterministe)
4. **Ne pas over-trust AI-generated tests** — behavior harness = maillon faible
5. Construire harness **templates par topologie service** (CRUD API, event processor)
6. Traiter **harnessability comme architectural concern** — strongly typed langs + clear module boundaries → meilleure couverture harness
7. Utiliser agents pour **BUILD le harness lui-même** (auto-scaffold linters, rules from patterns)

## VERBATIM NOTABLES

> "Agent = Model + Harness"

> "Guides increase the probability that the agent creates good results in the first attempt"

> "Correctness is outside any sensor's remit if the human didn't clearly specify what they wanted."

> "A good harness should not necessarily aim to fully eliminate human input, but to direct it to where our input is most important."

> "No fine-tuning, no model swap, just harness changes."

## ALIGNEMENT FORGE

La taxonomy mappe directement sur les composants forge :

| Forge | Catégorie Fowler |
|-------|------------------|
| Rules (.claude/rules/) | **Guide inferential** (équivalent AGENTS.md) |
| Skills (.claude/skills/) | **Guide inferential** |
| LSP / bootstrap scripts | **Guide computational** |
| Hooks Python exit 2 | **Sensor computational** (déterministe, fast) |
| Tests unitaires / ESLint / mypy | **Sensor computational** |
| devils-advocate / code-reviewer agents | **Sensor inferential** |

Doctrine forge **"Hooks > Rules"** = recommandation #3 de Fowler (computational > inferential) littéralement.

## WIKILINKS

- [[hashimoto]] — origine du terme harness engineering, Fowler le crédite
- [[addy-osmani]] — Ratchet Principle, complément empirique (+21.8 pts)
- [[comment-creer-hook]] — hooks = sensors computationnels en pratique
- [[comment-creer-skill]] — skills = guides inferentiels en pratique
- [[workflow-claude-code-optimal]] — pipeline complet feedforward+feedback
- [[methode-analyser-repo]] — analyser un repo via la grille Guides+Sensors

## SOURCES

- **Article complet** (2 avril 2026, signé Böckeler, sur martinfowler.com) : https://martinfowler.com/articles/harness-engineering.html
- **Mémo initial** Böckeler : 17 février 2026 (Thoughtworks Technology Radar)

---

## NOTE D'HIÉRARCHIE DES SOURCES

Source **secondaire** (couche 3). En cas de conflit avec un verbatim Anthropic officiel, suivre Anthropic. La taxonomy Guides+Sensors n'est PAS un cadre Anthropic — c'est un cadre Thoughtworks/industrie. Anthropic n'a pas adopté formellement cette terminologie mais la pratique est convergente.

## CORRECTION D'ATTRIBUTION

L'article est **signé Birgitta Böckeler**, pas Martin Fowler. Fowler en est l'éditeur (publication sur son site). Citer **"Böckeler & Fowler"** ou **"Böckeler (martinfowler.com)"** pour rester juste.
