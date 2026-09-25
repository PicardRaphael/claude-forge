---
titre: "Claude Opus 5.5 — défaut Opus depuis le 22 septembre 2026, effort par défaut medium"
resume: "Sorti le 22 sept. 2026 : claude-opus-5-5, $4/$20 par MTok, cache read $0,20 (5 % de l'input), 1M contexte / 128K output, cutoff juin 2026, thinking adaptatif toujours actif. Défaut Opus de Claude Code depuis v2.1.280 et point de départ officiel Anthropic. Piège principal : effort API par défaut medium (Opus 5 = high) et aucun niveau de départ recommandé. Cinq réglages renvoient 400 : thinking disabled, budget_tokens, tool_choice any/tool, sampling non défaut, prefill."
aliases:
  - "Claude Opus 5.5"
  - "Opus 5.5"
  - "claude-opus-5-5"
  - "opus-5-5"
  - "opus5.5"
derniere-maj: 2026-09-25
auteur: claude
type: modele
sources:
  - "https://platform.claude.com/docs/en/models/overview"
  - "https://platform.claude.com/docs/en/models/opus-5-5/migration-guide"
  - "https://platform.claude.com/docs/en/build-with-claude/effort"
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
tags:
  - "#type/modele"
  - "#domaine/anthropic"
  - "#domaine/claude"
---

# Claude Opus 5.5

> Sorti le **22 septembre 2026**. Ajouté dans Claude Code en **v2.1.280**, verbatim : *« Added Claude Opus 5.5 (`claude-opus-5-5`), now the default Opus model — 1M context, $4/$20 per Mtok with $0.20/Mtok cache reads »*. Successeur d'[[Opus 5]], qui passe en legacy (toujours disponible).

## Specs — source primaire (25 sept. 2026)

| Item | Valeur |
|---|---|
| ID modèle | `claude-opus-5-5` (Bedrock `anthropic.claude-opus-5-5`, même ID sur Vertex, Foundry, Claude Platform on AWS) |
| Prix | **$4 / M input · $20 / M output** — moins cher qu'Opus 5 ($5/$25) |
| Cache read | **$0,20 / MTok** = 5 % de l'input (10 % sur la plupart des modèles, 2,5 % sur [[Fable 5.1]]) |
| Contexte | **1M tokens** par défaut, sans header / 128K output (300K en Batch avec `output-300k-2026-03-24`) |
| Thinking | **Adaptatif, toujours actif** — non désactivable |
| Effort | 5 niveaux, **défaut `medium`** |
| Cutoff | juin 2026 (fiable et entraînement) |
| Retrait | pas avant le 22 septembre 2027 |

## Positionnement officiel

Verbatim *Models overview* : *« If you're unsure which model to use, start with Claude Opus 5.5 for most workloads. Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still fall short. »* Description du tableau : *« For long-running agentic coding and knowledge work »*.

## ⚠️ Le piège de l'effort

Verbatim page [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) : *« `medium` is the default (Claude Opus 5 and earlier Opus models default to `high`, so a request that omits `effort` runs one level lower than it did on Claude Opus 5) … Run an effort sweep on your own evals rather than carrying settings over from an earlier model »*.

Trois conséquences :

1. Un appel ou un composant **sans `effort:`** tourne en `medium` — un cran plus bas qu'hier, sans rien signaler.
2. Anthropic ne donne **aucun point de départ** pour ce modèle, contrairement à Opus 5 et Fable 5.1 (« Start with `high` »). Le `high` d'un frontmatter devient un **choix**, plus un alignement sur le défaut.
3. Côté Claude Code (v2.1.280) : un effort sauvegardé avant que `/effort` devienne par modèle **ne s'applique pas** aux nouveaux modèles ; Opus 5.5 démarre à son défaut tant qu'on ne choisit pas.

Changer l'effort au niveau global entre deux requêtes invalide le cache ; l'effort **par message** (beta `mid-conversation-output-config-2026-07-01`) le préserve.

## Breaking changes (guide de migration)

Toutes renvoient **400** :

- `thinking: {"type": "disabled"}` et `thinking: {"type": "enabled", "budget_tokens": N}` — remplacer par un niveau d'effort.
- `tool_choice` `{"type": "any"}` ou `{"type": "tool", …}` — y compris sur le comptage de tokens. Passer par `auto` + strict tool use ou structured outputs.
- `temperature`, `top_p`, `top_k` différents du défaut.
- Prefill d'un tour assistant.

Autres points :

- `max_tokens` couvre thinking + texte : les workloads qui tournaient sans thinking produisent plus de tokens de sortie facturés. À `xhigh`/`max`, partir de 64k.
- Les réponses commencent par des blocs `thinking` : sélectionner les blocs par `type` et les renvoyer inchangés avec les résultats d'outils.
- Thinking blocks : Opus 5.5 lit ceux d'Opus 5 et des Opus/Sonnet/Haiku antérieurs, pas ceux de Fable/Mythos. Un routeur qui fait redescendre une conversation d'Opus 5.5 vers un autre modèle perd le raisonnement, sauf vers Fable 5.1 / Mythos 5.1 sur l'API Claude.
- Claude Managed Agents : seul le nom du modèle change.
- Outil de migration : `/claude-api migrate this project to claude-opus-5-5` dans Claude Code.

## Pertinence forge

- L'alias `opus` des frontmatters résout vers Opus 5.5 depuis v2.1.280. Tous les agents forge `opus` y sont passés sans modification de fichier.
- Doctrine effort pivotée le 25 sept. 2026 : `high` reste posé explicitement, sweep Opus 5.5 (n=3 par niveau) avant de toucher un frontmatter. Voir [[raisonnement-2026-09-25-effort-opus-5-5]] et [[effort-opus-47-doctrine-anthropic-2026]].
- Ordre de repli : Opus 5 → Opus 4.8, jamais 4.7 (préférence Raphaël).

## Liens

- [[Opus 5]] — prédécesseur, legacy depuis le 22 sept. 2026
- [[Fable 5.1]] — step-up mesuré
- [[CC septembre 2026 - Opus 5.5 + v2.1.263-282]] — versions Claude Code liées
- [[doctrine-par-modele-opus5-fable5]] — quel modèle pour quel agent
- [[MOC-Modeles]]
