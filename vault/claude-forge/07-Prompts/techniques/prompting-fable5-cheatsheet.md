---
titre: "Prompting Claude Fable 5 — cheatsheet officielle Anthropic (copier-coller)"
resume: "Les 12 patterns officiels Anthropic pour prompter Fable 5 (classe Mythos) : goal-setting > micromanagement, effort high par défaut, negative prompting anti-refacto, verification loops, pause points, memory system, send_to_user tool. Templates verbatim depuis platform.claude.com."
aliases:
  - "Prompting Fable 5"
  - "Fable 5 cheatsheet"
  - "prompt engineering Fable 5"
  - "Fable 5 prompting guide"
  - "claude-fable-5 prompts"
  - "Mythos 5 prompting"
domaine: technique
type: technique
derniere-maj: 2026-07-02
auteur: claude
sources:
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5"
  - "[[Fable 5]]"
tags:
  - "#type/technique"
  - "#domaine/anthropic"
  - "#domaine/claude"
---

# Prompting Claude Fable 5

> ⚠️ **Disponibilité** : Fable 5 est **suspendu depuis le 12 juin 2026** (directive export-control US, cf [[Fable 5]]). Ces patterns restent valides pour le jour où il réactive, et beaucoup s'appliquent déjà à Opus 4.8 (même famille : adaptive thinking only, longs runs). Templates copier-coller extraits de la doc officielle Anthropic.

## Principe directeur : goal-setting, pas micromanagement

Fable 5 est fait pour le travail **long-horizon autonome** (heures/jours), pas pour être micro-managé. Sur-spécifier un prompt **dégrade** la sortie : on contraint un modèle qui aurait trouvé la bonne approche seul. Instruction-following assez fort pour **piloter un comportement en une phrase brève** plutôt qu'énumérer chaque cas.

## Les 12 patterns officiels (templates verbatim)

### 1. Anti-overplanning (tâche ambiguë)
```text
When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks.
```

### 2. Effort : `high` par défaut
`xhigh` = travail le plus capability-sensitive · `medium`/`low` = routine (dépasse souvent `xhigh` des modèles antérieurs). Baisser l'effort si la tâche aboutit mais traîne, ou pour un style plus interactif.

### 3. Anti-refacto / anti-tidying (haut effort)
```text
Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need surrounding cleanup and a one-shot operation usually doesn't need a helper. Don't design for hypothetical future requirements: do the simplest thing that works well. Avoid premature abstraction and half-finished implementations. Don't add error handling, fallbacks, or validation for scenarios that cannot happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs). Don't use feature flags or backwards-compatibility shims when you can just change the code.
```

### 4. Brièveté (une instruction suffit)
```text
Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail and reasoning come after. Being readable and being concise are different things, and readability matters more.

The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon.
```

### 5. Checkpoint / pause points
```text
Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise.
```

### 6. Grounding des claims de progression (anti-hallucination status)
```text
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.
```

### 7. Frontières d'action (anti-actions non demandées)
```text
When the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one. Before running a command that changes system state (restarts, deletes, config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

### 8. Subagents parallèles
```text
Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context.
```

### 9. Système de mémoire (fichier Markdown)
```text
Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong.
```
Bootstrap depuis l'historique :
```text
Reflect on the previous sessions we've had together. Use subagents to identify core themes and lessons, and store them in [X]. Make sure you know to reference [X] for future use.
```

### 10. Anti early-stopping (pipelines autonomes)
```text
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking "Want me to…?" or "Shall I…?" will block the work. For reversible actions that follow from the original request, proceed without asking. Offering follow-ups after the task is done is fine; asking permission after already discussing with the user before doing the work is not. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ("I'll…", "let me know when…"), do that work now with tool calls. End your turn only when the task is complete or you are blocked on input only the user can provide.
```

### 11. Rassurance context-budget (sessions très longues)
```text
You have ample context remaining. Do not stop, summarize, or suggest a new session on account of context limits. Continue the work.
```

### 12. Donner la raison, pas seulement la requête
```text
I'm working on [the larger task] for [who it's for]. They need [what the output enables]. With that in mind: [request].
```

## Scaffolding recommandé

- **Commencer en haut de sa gamme de difficulté** — tâche plus dure que ce qu'on donnait aux modèles antérieurs, lui faire scoper + poser des questions + exécuter.
- **Self-verification explicite** : `Establish a method for checking your own work at an interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the specification.` — les sous-agents vérificateurs à contexte frais battent l'auto-critique.
- **Refactorer les vieux prompts/skills** : trop prescriptifs pour Fable 5 = dégradation. Retirer les vieilles instructions si le défaut est meilleur.
- **NE PAS demander de reproduire son raisonnement** dans la réponse → déclenche la catégorie refusal `reasoning_extraction` → fallback vers Opus 4.8. Lire les blocs `thinking` de l'adaptive thinking à la place.
- **send_to_user tool** pour agents async longs (message verbatim sans finir le tour) — nécessite une instruction d'élicitation, sinon Fable 5 ne l'appelle presque jamais.

## Migration / gotchas

- **Ne pas réutiliser les vieux frameworks de prompt** (optimisés modèles antérieurs) → contre-productifs.
- **Longs tours par défaut** : requêtes de plusieurs minutes à haut effort. Ajuster timeouts client, streaming, indicateurs de progression ; envisager du check async (jobs planifiés) plutôt que bloquant.
- **Safety fallback** : classifiers cyber offensif / bio-sciences / extraction du thinking → `stop_reason: "refusal"`. Configurer fallback serveur/client vers Opus 4.8.

## Liens

- [[Fable 5]] — fiche modèle (caractéristiques, suspension export-control)
- [[prompting-opus47-cheatsheet]] — équivalent Opus 4.7 (16 prompts copier-coller)
- [[Effort Levels Guide]] — low/medium/high/xhigh/max
- [[Adaptive Thinking]] — thinking adaptatif (Fable = adaptive only)
- [[MOC-Prompts]]
- [[MOC-Techniques]]
