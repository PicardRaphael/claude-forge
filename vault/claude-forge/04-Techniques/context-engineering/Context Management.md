---
titre: "Context Management — Gestion contexte LLM Claude Code"
resume: "Techniques de gestion du contexte Claude Code : /clear, /compact, Document & Clear, délégation subagents, prompt caching"
aliases:
  - "Context Management"
  - "context management"
  - "gestion contexte"
  - "gestion contexte LLM"
  - "compaction sessions longues"
  - "document and clear"
  - "document clear pattern"
  - "session longue claude code"
  - "context saturation"
  - "context window management"
type: technique
domaine: context-engineering
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://www.anthropic.com/engineering/claude-code-best-practices"
  - "https://howborisusesclaudecode.com/"
  - "https://blog.sshh.io/p/how-i-use-every-claude-code-feature"
tags:
  - "#type/technique"
  - "#domaine/context-engineering"
---

## Description

Techniques canoniques de gestion du contexte Claude Code dans les sessions longues. Compose Anthropic docs (co-rédigées par Boris Cherny, créateur Claude Code) + tips Thariq Shihipar + patterns communauté.

## Patterns clés

### `/clear` entre tâches non liées

Doc Anthropic (verbatim) : *"Use /clear frequently between tasks to reset the context window entirely."*

Anti-pattern à éviter : sessions fourre-tout où des tâches non liées s'empilent et polluent le contexte. Lancer `/clear` avant chaque nouvelle tâche substantielle.

### Compaction proactive

Tips attribués à **Thariq Shihipar** (Eng Manager Claude Code) via [howborisusesclaudecode.com](https://howborisusesclaudecode.com/) :

- **Sous 40%** : zone confortable, contexte propre
- **40-60%** : push vers compaction sur tâches simples
- **>60%** : forcer wrap-up
- **Auto-compact fire ~83.5%** (seuil système)

Le seuil "70%" parfois cité n'est pas attesté dans les sources canoniques — utiliser la fourchette 40-60% officielle.

### Document & Clear

Pattern documenté par la communauté (sshh.io, Manus AI, planning-with-files GitHub) :

> Manus AI verbatim (via sshh) : *"Markdown is my working memory on disk."*

Mécanique : dumper le plan/état courant dans un fichier `.md` → `/clear` → nouvelle session qui lit le fichier comme contexte. Attribution communauté/Manus AI/sshh — **pas attribué à Boris Cherny** dans les sources primaires.

### Délégation subagents

Doc Anthropic : *"a subagent is an isolated Claude instance with its own context window that takes a task, does the work, and returns only the final result to the parent."* — utile pour exploration read-only sans polluer le contexte principal.

### Prompt caching

Anthropic : cache read tokens = 0.1× base = **-90% sur les portions cachées** (system prompt statique, tools définitions). Activation automatique au-delà des seuils de longueur.

## Liens

- [[Context Engineering]]
- [[workflow-claude-code-optimal]]
- [[Boris Cherny]]
- [[Thariq Shihipar]]
- [[MOC-Techniques]]
