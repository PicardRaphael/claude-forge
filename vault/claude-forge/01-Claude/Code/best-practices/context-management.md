---
titre: "Context Management Claude Code — /clear, /compact, compaction, subagents"
resume: "Gestion du contexte Claude Code — le context window est la contrainte fondamentale, patterns /clear et /compact, 3 primitives de compaction, subagents pour isolation"
aliases:
  - "context management CC"
  - "gestion contexte claude code"
  - "context engineering CC"
  - "/clear /compact guide"
  - "compaction claude code"
  - "session management claude code"
domaine: claude-code
type: technique
derniere-maj: 2026-05-24
auteur: claude
sources:
  - "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"
  - "https://code.claude.com/docs/en/best-practices"
  - "https://howborisusesclaudecode.com"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/context-engineering"
---
## Principe fondamental

> **"Good context engineering means finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."** — Anthropic Engineering

Cat Wu (docs officielles) : "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills."

### Context Rot

A mesure que le nombre de tokens augmente, la capacite du modele a rappeler l'information diminue. C'est une propriete de l'architecture transformer (relations n² pour n tokens). Plus le contexte est court, meilleure est la performance.

## Workflow Boris — Session hygiene

### /clear entre taches non liees

Sessions "fourre-tout" = piege #1. Commencer une tache, poser des questions sans rapport, revenir — le contexte est pollue.

### /compact proactif (sous 40-60%, pas 70%)

`/compact "garder le plan"` — ne pas attendre l'auto-compact (fire ~83.5%). Specifier ce qui doit etre preserve. Tips Thariq (howborisusesclaudecode.com) : shoot sous 40%, push 60% sur taches simples.

### Document & Clear

1. Dump le plan dans un .md
2. /clear
3. Nouvelle session qui lit le .md

### /btw

Questions rapides sans polluer le contexte. La reponse n'entre pas dans l'historique.

### Plan acceptance auto-clear

Boris : quand on accepte un plan, Claude clear automatiquement le contexte. Le plan demarre avec un context window frais → meilleure adherence.

## 3 primitives de compaction (API-level)

### 1. Tool clearing (cout zero)

Remplace les anciens `tool_result` blocks par des placeholders. Garde les `tool_use` blocks (le modele se souvient de l'appel). Zero cout d'inference.

### 2. Compaction (inference)

Compresse le dialogue en preservant les faits de haut niveau, decisions, etat architectural. Perd les details verbatim, statistiques specifiques, formulations exactes.

Benchmark : **58.6% reduction** de tokens sur un workflow de 37 tours.

### 3. Memory (persistant)

Notes ecrites par l'agent, persistantes cross-session. Complementaire aux 2 autres.

**Recommandation** : clearing d'abord (pas cher) → compaction ensuite (plus cher) → memory pour le cross-session.

## Subagents pour isolation de contexte

> "Since context is your fundamental constraint, subagents are one of the most powerful tools available."

- Un subagent explore dans un contexte separe, peut consommer des dizaines de milliers de tokens
- Ne retourne qu'un **resume condense** (1 000-2 000 tokens) au parent
- Le contexte de recherche detaille reste isole dans le subagent

### Pattern Writer/Reviewer (sessions paralleles)

- Session A (Writer) : implemente
- Session B (Reviewer) : review avec contexte frais (pas de biais vers son propre code)
- Session A incorpore le feedback

## Just-in-Time Context (Hybrid retrieval)

Le pattern dominant en 2026 :
- **Pre-charger** des identifiants legers (CLAUDE.md, chemins, queries)
- **Charger dynamiquement** le contenu complet a la demande via outils (glob, grep, read)

C'est exactement comment CC fonctionne : CLAUDE.md pre-charge + glob/grep pour navigation.

Boris : "Agentic search > RAG. Glob + grep pilotes par le modele surpassent un index RAG."

## 5 anti-patterns (Anthropic officiel)

1. **Kitchen sink session** — taches non liees dans une session → /clear
2. **Correcting over and over** — 2 corrections echouees → /clear et recrire le prompt
3. **Over-specified CLAUDE.md** — trop long, Claude ignore → pruner, convertir en hooks
4. **Trust-then-verify gap** — implementation plausible, pas de edge cases → verification
5. **Infinite exploration** — investigation non-scopee remplit le contexte → scoper ou subagents

## Liens

- [[comment-ecrire-claudemd]] — Compaction survie et taille
- [[comment-creer-skill]] — Budget contexte des skills
- [[comment-creer-hook]] — Hooks comme alternative au contexte advisory
- [[harness-engineering]] — Context management dans le harness
- [[Boris Cherny]] — Session hygiene
