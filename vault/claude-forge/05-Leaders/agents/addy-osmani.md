---
titre: "Addy Osmani — Agent Harness Engineering & Ratchet Principle"
resume: "Engineering lead Google Chrome, formalise le concept d'Agent Harness Engineering : la valeur d'un agent vient du scaffolding (prompts, hooks, sandboxes), pas du modèle — démontré par +21.8 pts Terminal Bench à modèle constant"
aliases:
  - "Addy Osmani"
  - "addy osmani"
  - "addyosmani"
  - "Agent Harness Engineering"
  - "Ratchet Principle"
  - "harness engineering Addy"
derniere-maj: 2026-05-22
auteur: claude
type: leader
sources:
  - "https://addyosmani.com/blog/agent-harness-engineering/"
  - "https://www.oreilly.com/radar/agent-harness-engineering/"
  - "https://x.com/addyosmani/status/2022822356050399673"
  - "https://addyosmani.com/blog/agent-skills/"
tags:
  - "#type/leader"
  - "#domaine/agents"
  - "#domaine/harness-engineering"
  - "#leader/agents"
---

# Addy Osmani — Agent Harness Engineering & Ratchet Principle

## QUI

Engineering lead sur Google Chrome (DevTools, performance, dev experience). Auteur prolifique (livres *Learning JavaScript Design Patterns*, *Image Optimization*, et plus récemment **Harness Engineering**, focalisé agents IA). Twitter `@addyosmani`. Blog `addyosmani.com`.

Profil : ingénieur produit + écrivain technique. N'est PAS chez Anthropic. Ses contributions sont **observationnelles** (synthèse de patterns convergents Claude Code / Cursor / Codex / Aider / Cline) plutôt que doctrinales.

## POURQUOI EST PERTINENT

Addy a **formalisé** ce que Hashimoto a nommé *"harness engineering"* (cf [[hashimoto]]) et que Fowler/Böckeler ont taxonomisé en Guides+Sensors (cf [[martin-fowler]]). Sa contribution propre : le **Ratchet Principle** et la métrique **+21.8 pts harness > model** qui sert d'argument empirique massif partout.

Son framing est devenu la **référence de vulgarisation** pour expliquer "pourquoi config Claude Code matter". Boris Cherny l'a recommandé publiquement.

## CONTRIBUTIONS CLÉS

### 1. Définition canonique "harness"

> "A coding agent is the model plus everything you build around it. Harness engineering treats that scaffolding as a real artifact, and it tightens every time the agent slips."

Le harness = **prompts + tools + context policies + hooks + sandboxes + subagents + feedback loops + recovery paths**. Tout sauf le modèle.

### 2. Le Ratchet Principle

> "the harness only tightens, never loosens"

Chaque erreur d'agent = signal permanent qui tighten le harness. **L'erreur n'est jamais "le modèle est nul"** — c'est un bug du harness qui doit être codifié en règle/hook/skill pour ne plus jamais arriver.

> "the agent does something dumb, the engineer blames the model, and the blame gets filed under 'wait for the next version'. The harness-engineering mindset rejects that default. The failure is usually legible — the agent didn't know about a convention, so you add it to AGENTS.md; the agent ran a destructive command, so you add a hook that blocks it."

### 3. Stat chocs harness > model (Terminal Bench 2.0)

- Claude Opus 4.6 dans **Claude Code** : **58.0%**
- **Même modèle** dans **ForgeCode** (harness différent) : **79.8%**
- Delta : **+21.8 points par architecture harness seule** (modèle identique)
- Une équipe est passée de **top 40 à top 5** en changeant uniquement le harness

C'est l'argument empirique le plus cité en 2026 pour justifier l'investissement dans la configuration Claude Code plutôt que d'attendre Opus 5.

### 4. Primitives harness convergentes

Claude Code, Cursor, Codex, Aider, Cline convergent sur les mêmes primitives malgré modèles/équipes différents :

- Filesystem / Git pour durable state
- Bash execution + sandboxes
- Memory / search
- Context compaction strategies
- **Hooks for enforcement** (déterministes)
- Planner / evaluator splits
- *"Harness-as-a-Service"* émergent

→ Signal de **"load-bearing scaffolding principles"** indépendants du modèle.

### 5. Engineer's value shifts (commentaire sur Boris)

> "Boris created Claude Code. His point here is important — when AI handles the code generation, the engineer's value shifts to the decisions above the code: 1. what do we build? 2. why? for whom? 3. and how it all fits together. The bottleneck was always judgment, taste, and systems thinking — AI just made that more obvious."

Convergent avec Erik Schluntz (vibe coding responsibly, [[erik-schluntz]] si fiche créée) et Karpathy (agentic engineering).

## VERBATIM NOTABLES

> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."
> *(Addy reprend ici la formulation de Hashimoto, qu'il crédite)*

> "the harness only tightens, never loosens"

> "+21.8 points by architecture alone"

## ALIGNEMENT FORGE

La doctrine forge **Hooks > Rules** ([[comment-creer-hook]]) **EST** le Ratchet Principle appliqué. Chaque erreur comportementale capitalisée dans CLAUDE.md ou un hook bloquant = tighten du harness. Compounding error-driven.

Addy formalise mieux que la doctrine forge la **discipline systémique** : pas juste "documenter l'erreur" mais "transformer l'erreur en règle déterministe permanente".

## WIKILINKS

- [[hashimoto]] — origine du terme "harness engineering" (Addy le crédite)
- [[martin-fowler]] — taxonomy Guides+Sensors complémentaire
- [[comment-creer-agent]] — Agent = Model + Harness en pratique
- [[comment-creer-hook]] — hooks = sensors computationnels (tighten via enforcement)
- [[workflow-claude-code-optimal]] — harness pipeline complet
- [[methode-analyser-repo]] — analyser un repo = identifier les trous du harness

## SOURCES

- **Blog principal harness** : https://addyosmani.com/blog/agent-harness-engineering/
- **O'Reilly Radar** : https://www.oreilly.com/radar/agent-harness-engineering/
- **Tweet sur Boris** (engineer's value shifts) : https://x.com/addyosmani/status/2022822356050399673
- **Blog Agent Skills** : https://addyosmani.com/blog/agent-skills/
- **Blog Claude Code Swarms** : https://addyosmani.com/blog/claude-code-agent-teams/

---

## NOTE D'HIÉRARCHIE DES SOURCES

Addy = source **secondaire** (couche 3 de la hiérarchie forge : équipe CC Anthropic > Karpathy > autres). En cas de conflit avec un verbatim Boris/Cat/Erik ou avec Karpathy, suivre la source primaire. Addy excelle en **synthèse et framing pédagogique**, pas en doctrine officielle.
