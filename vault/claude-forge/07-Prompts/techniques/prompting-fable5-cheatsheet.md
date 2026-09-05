---
titre: "Prompting Claude Fable 5 / 5.1 — cheatsheet officielle Anthropic (copier-coller)"
resume: "Les 12 patterns officiels Anthropic pour prompter Fable 5 (classe Mythos) + les différences comportementales de Fable 5.1 (1er sept. 2026) : goal-setting > micromanagement, effort high par défaut, sweep d'effort à refaire par modèle, historique append-only obligatoire, retirer les règles anti-formatage. Templates verbatim depuis platform.claude.com."
aliases:
  - "Prompting Fable 5"
  - "Prompting Fable 5.1"
  - "Fable 5 cheatsheet"
  - "Fable 5.1 cheatsheet"
  - "prompt engineering Fable 5"
  - "Fable 5 prompting guide"
  - "claude-fable-5 prompts"
  - "claude-fable-5-1 prompts"
  - "Mythos 5 prompting"
domaine: technique
type: technique
derniere-maj: 2026-09-05
auteur: claude
sources:
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5"
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1"
  - "[[Fable 5]]"
  - "[[Fable 5.1]]"
tags:
  - "#type/technique"
  - "#domaine/anthropic"
  - "#domaine/claude"
---

# Prompting Claude Fable 5 / 5.1

> **Disponibilité (à jour 5 sept. 2026)** : Fable 5 a été redéployé le **1er juillet 2026** après la levée de l'export-control (cf [[Fable 5]]), et **[[Fable 5.1]] est sorti le 1er septembre 2026** — c'est désormais le modèle Fable par défaut. Les 12 patterns ci-dessous restent la base ; Anthropic confirme que *« your existing Claude Fable 5 prompts should perform well on Claude Fable 5.1 without changes »*. Les écarts propres à 5.1 sont regroupés en fin de note.

## Principe directeur : goal-setting, pas micromanagement

Fable est fait pour le travail **long-horizon autonome** (heures/jours), pas pour être micro-managé. Sur-spécifier un prompt **dégrade** la sortie : on contraint un modèle qui aurait trouvé la bonne approche seul. Instruction-following assez fort pour **piloter un comportement en une phrase brève** plutôt qu'énumérer chaque cas.

## Les 12 patterns officiels (templates verbatim)

### 1. Anti-overplanning (tâche ambiguë)
```text
When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks.
```

### 2. Effort : `high` par défaut
`xhigh` = travail le plus capability-sensitive · `medium`/`low` = routine (dépasse souvent `xhigh` des modèles antérieurs). Baisser l'effort si la tâche aboutit mais traîne, ou pour un style plus interactif. ⚠️ Sur 5.1, **refaire le sweep** — cf section dédiée.

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
- **Refactorer les vieux prompts/skills** : trop prescriptifs pour Fable = dégradation. Retirer les vieilles instructions si le défaut est meilleur.
- **NE PAS demander de reproduire son raisonnement** dans la réponse → déclenche la catégorie refusal `reasoning_extraction` → fallback vers Opus 4.8. Lire les blocs `thinking` de l'adaptive thinking à la place.
- **send_to_user tool** pour agents async longs (message verbatim sans finir le tour) — nécessite une instruction d'élicitation, sinon Fable ne l'appelle presque jamais.

## Migration / gotchas

- **Ne pas réutiliser les vieux frameworks de prompt** (optimisés modèles antérieurs) → contre-productifs.
- **Longs tours par défaut** : requêtes de plusieurs minutes à haut effort. Ajuster timeouts client, streaming, indicateurs de progression ; envisager du check async (jobs planifiés) plutôt que bloquant.
- **Safety fallback** : classifiers cyber offensif / bio-sciences / extraction du thinking → `stop_reason: "refusal"`. Configurer fallback serveur/client vers Opus 4.8.

---

## AJOUT 5 septembre 2026 — différences comportementales de Fable 5.1

Source primaire : [prompting-claude-fable-5-1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1). Les prompts Fable 5 fonctionnent tels quels ; ces écarts se traitent **au symptôme observé**.

| Symptôme observé | Cause 5.1 | Correctif officiel |
|---|---|---|
| Doute sur le niveau d'effort, coût/latence trop élevés | Les noms d'effort ne couvrent pas le même volume de pensée d'un modèle à l'autre | **Refaire le sweep**, même si fait sur Fable 5 |
| Peu ou pas de texte entre les tool calls | 5.1 écrit moins d'updates que Fable 5, surtout à haut effort | Activer `thinking.display: "updates"` (beta `thinking-display-updates-2026-08-18`) puis, si besoin, demander explicitement les updates |
| Un seul tool call par tour en boucle agentique | Défaut dans les harnesses coding/computer-use quand les appels suivants sont implicites | Nudge : *« First privately list what you need next; then request every item that doesn't depend on another's result in this one response. »* |
| Erreur `bound to a different conversation` | **Les thinking blocks ne sont valides que dans la conversation exacte qui les a produits** (comptes créés depuis le 31 août 2026) | Historique **strictement append-only** — cf ci-dessous |
| Prose longue et dense | 5.1 écrit plus dense que Fable 5 | Instruction anti-*mannered prose* (ou simplement « Please remove all mannered prose. ») |
| Réponses de chat sous-structurées | 5.1 utilise **moins** de gras/listes que les modèles antérieurs | **Retirer les règles anti-formatage** héritées, les remplacer par une règle disant quand formater |
| Citations non marquées | 5.1 reproduit plus souvent le texte source sans le marquer | Ajouter un exemple complet de réponse correcte au system prompt |
| Le tour s'arrête avant la fin / demande une permission déjà donnée | — | Bloc « operating autonomously » + bloc « Delivering work » (les deux) |
| Corrections ou tests non demandés | 5.1 en fait parfois plus que demandé | Instruction explicite de ne pas étendre ; tests dimensionnés comme le voisinage |
| Répond de mémoire au lieu de chercher, à effort `low` | 5.1 déclenche moins les outils de recherche à `low` | Monter l'effort sur les tours concernés, ou nudge « vérifier le nom lui-même » |
| Fichiers entiers réécrits pour un petit changement | 5.1 réécrit plus volontiers que Fable 5 | *« try to surgically edit a file rather than rewrite the entire thing »* |
| Longs livrables lents ou coupés à `xhigh`/`max` | 5.1 peut rédiger le livrable dans son thinking puis le réécrire | Rester à `high`, ou prévenir que thinking + réponse partagent un seul budget |
| Le lead agent attend ses sous-agents | — | Tool de spawn qui rend la main immédiatement + tool d'attente séparé |
| Détail manqué sur graphiques denses | — | Donner un outil de crop/zoom (recette officielle *crop tool*) |

### Les trois points qui comptent le plus

1. **Historique append-only, non négociable.** Rejouer un thinking block après modification du préfixe (system prompt, liste d'outils, message antérieur) renvoie **400**. Anthropic prévient : *« Future models are expected to enforce this check for all accounts, so adopt the pattern now even if yours isn't enforced today. »* Les édits fautifs sont exactement ceux qui cassent le prompt cache — injection/retrait de rappels par tour, résumé en place, changement de system prompt en cours de session. Utiliser les turn-scoped system messages plutôt que réécrire `system`.

2. **Le sweep d'effort n'est pas transférable.** *« Effort level names don't correspond to the same amount of thinking across models. »* À `medium`, 5.1 égale Fable 5 pour moins cher ; à `low`, il est *« often competitive with Claude Opus and Claude Sonnet models on cost per task while scoring higher »*. C'est un argument direct pour tester `low`/`medium` là où forge met `high` par réflexe.

3. **Safeguards assouplis mais présents.** *« Finding vulnerabilities in source code is permitted. »* Trois déclencheurs de faux positifs subsistent : phrasé de type « est-ce que ça compile sans erreur » (préférer « y a-t-il des bugs »), langages peu connus (fournir la doc), et **base64 en sortie d'outil** (à retirer).

## Liens

- [[Fable 5.1]] — fiche modèle 5.1 (specs, pricing, Mythos 5.1)
- [[Fable 5]] — fiche modèle (caractéristiques, cycle suspension/redéploiement)
- [[doctrine-par-modele-opus5-fable5]] — quel modèle pour quel agent, et ce qui change dans les prompts
- [[prompting-opus47-cheatsheet]] — équivalent Opus 4.7 (16 prompts copier-coller)
- [[Effort Levels Guide]] — low/medium/high/xhigh/max
- [[Adaptive Thinking]] — thinking adaptatif (Fable = adaptive only)
- [[MOC-Prompts]]
- [[MOC-Techniques]]
