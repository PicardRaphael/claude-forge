---
titre: "Justin Young"
resume: "MTS Anthropic — auteur de 'Effective harnesses for long-running agents' (26 nov 2025). Pose la doctrine canonique two-agent architecture (Initializer + Coding Agent) et clean-state pour agents long-running."
aliases:
  - "justin young"
  - "Justin Young"
  - "young justin"
  - "MTS Anthropic Justin"
  - "effective harnesses"
  - "two-agent architecture"
  - "init agent coding agent"
  - "long-running agents Anthropic"
derniere-maj: 2026-05-22
auteur: claude
role: "Member of Technical Staff (MTS)"
affiliation: "Anthropic"
sources:
  - "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents"
  - "https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding"
  - "https://platform.claude.com/docs/en/agent-sdk/overview"
type: "leader"
tags:
  - "#type/leader"
  - "#domaine/claude-code"
  - "#domaine/agents"
  - "#org/anthropic"
---

## QUI

- **Rôle** : Member of Technical Staff (MTS), Anthropic
- **Équipe** : Claude Code / Agent Engineering
- **Article référence** : *Effective harnesses for long-running agents* — publié sur anthropic.com/engineering, **26 novembre 2025**
- **Profil public** : auteur unique de l'article qui pose la doctrine officielle Anthropic pour les agents qui durent au-delà d'une seule fenêtre de contexte

## POURQUOI IL EST PERTINENT

Justin Young est la **source canonique** Anthropic pour la doctrine **two-agent architecture**. Son article est cité dans la hiérarchie de vérité du chantier 22 mai (section "Équipe Claude Code / Anthropic officiel = dernier mot").

Trois raisons :

1. **Two-agent architecture** (Initializer + Coding Agent) — pattern central pour tout agent long-running. Réutilisé directement dans la note canonique forge [[comment-creer-agent]].
2. **Failure modes officiels** nommés et documentés — "agent attempts to one-shot" et "declares the job done" prématurément.
3. **Clean state doctrine** — via commits git descriptifs, JSON > Markdown pour artefacts, tests immuables.

Pertinence forge : son article structure la section "agents long-running" de [[comment-creer-agent]] et alimente la doctrine async dans [[workflow-claude-code-optimal]].

## CONTRIBUTIONS CLÉS

### Two-agent architecture (verbatim doctrine)

Article Anthropic, source : `anthropic.com/engineering/effective-harnesses-for-long-running-agents` (26 nov 2025).

**Architecture officielle** :

| Agent | Rôle |
|---|---|
| **Initializer Agent** (1ère session) | Scaffold env : `init.sh`, `claude-progress.txt`, `feature_list.json`, git baseline |
| **Coding Agent** (sessions suivantes) | Exécution incrémentale, clean state à la fin de chaque session |

**Distinction explicite** (verbatim du chantier `recherche-blog-docs-anthropic.md`) :

> "Distinction : uniquement par leur user prompt initial. System prompt et tools identiques."

Ce point est crucial : les deux agents partagent **le même system prompt** et **les mêmes outils**. Seul le prompt utilisateur d'amorçage diffère. C'est l'antidote au pattern anti "split by problem type" (planner / impl / tester / reviewer en téléphone arabe) — pattern critiqué dans `audit-notes-existantes-vs-fraiches.md`.

### Failure modes officiels (à éviter)

Verbatim Justin Young (cf. `recherche-blog-docs-anthropic.md`) :

1. **One-shot exhaustion** : "Agent attempts to one-shot, exhausts context mid-implementation."
2. **Premature done** : "Later agent instance surveys partial progress and declares the job done."

Le second est le plus pernicieux : un agent qui reprend trouve l'env partiellement avancé et déclare la tâche terminée parce qu'il ne reconnaît pas son propre état initial.

### Artefacts d'environnement obligatoires

| Artefact | Rôle |
|---|---|
| `init.sh` | Démarrer dev server fiablement, idempotent |
| `claude-progress.txt` | Log des features done (lecture par agent suivant) |
| `feature_list.json` | JSON breakdown, `"passes": false` au départ |
| Commit git initial | Baseline recoverable, état zéro reconnaissable |

**Doctrine JSON > Markdown** (verbatim) :

> "the model is less likely to inappropriately overwrite it."

**Doctrine tests immuables** (verbatim) :

> "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

### Clean state via git commits

Verbatim canonique :

> "the best way to elicit this behavior was to ask the model to commit its progress to git with descriptive commit messages"

Le commit git devient le mécanisme de mémoire externe entre sessions — équivalent harness du "engineer one time, agent runs forever" (Hashimoto).

### Question multi-agent ouverte (intellectuelle honnêteté)

Verbatim Justin Young, fin d'article :

> "it's still unclear whether a single, general-purpose coding agent performs best across contexts, or if better performance can be achieved through a multi-agent architecture"

C'est la phrase qui ferme l'article — Anthropic ne tranche pas. Cela cadre la nuance forge : two-agent = pattern documenté, pas dogme. Single-agent reste valide pour beaucoup de cas.

## VERBATIM NOTABLES

> "Distinction : uniquement par leur user prompt initial. System prompt et tools identiques." — Justin Young, *Effective harnesses for long-running agents*

> "the model is less likely to inappropriately overwrite it." (à propos de JSON > Markdown)

> "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

> "the best way to elicit this behavior was to ask the model to commit its progress to git with descriptive commit messages"

> "it's still unclear whether a single, general-purpose coding agent performs best across contexts, or if better performance can be achieved through a multi-agent architecture"

## STATUT D'INFORMATION

- **Confirmé** : auteur unique de l'article *Effective harnesses for long-running agents* (26 nov 2025), MTS Anthropic, doctrine two-agent + clean state + JSON > MD + tests immuables
- **À confirmer** : autres publications, talks publics (présence Code with Claude SF / London non confirmée dans les rapports du chantier)
- **Information non confirmée à date du chantier** : handle Twitter/X public, bio pré-Anthropic détaillée, contributions GitHub publiques sous identité Anthropic

## ÉQUIVALENT FORGE

La two-agent architecture est intégrée comme **doctrine canonique** dans la note forge [[comment-creer-agent]] (chantier 22 mai 2026). Elle remplace l'anti-pattern "agent CTO orchestrateur" et "split by role" précédemment toléré dans certains repos.

## WIKILINKS

- [[comment-creer-agent]] — référence directe à la two-agent architecture
- [[workflow-claude-code-optimal]] — agents long-running, async, clean-state
- [[methode-analyser-repo]] — pattern Initializer Agent appliqué à l'analyse repo
- [[Erik Schluntz]] — co-auteur du paper fondateur *Building Effective Agents* (2024), complémentaire
- [[Boris Cherny]] — Routines async, compounding, complémentarité
- [[Jeremy Hadfield]] — Dreaming, agents async cross-session
- [[Daisy Hollman]] — "agents overnight" — opérationnalisation

## SOURCES

- [Effective harnesses for long-running agents — Justin Young, Anthropic, 26 nov 2025](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Claude Quickstarts — autonomous-coding (référencé dans l'article)](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview)
- Rapport chantier interne : `0-Inbox/_chantier-22mai/recherche-blog-docs-anthropic.md` (§4)
