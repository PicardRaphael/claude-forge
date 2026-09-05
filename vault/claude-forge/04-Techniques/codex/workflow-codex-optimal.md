---
titre: "Workflow OpenAI Codex optimal (septembre 2026)"
resume: "Note maître forge — workflow optimal pour l'agent de code OpenAI Codex au 5 sept. 2026 : modèle défaut gpt-6-astra depuis la CLI 0.153.4, séquence par taille de tâche S/M/L/XL, 3 niveaux d'optimisation, Surface Map des 8 leviers (AGENTS.md → hooks), multitasking Sottiaux, codex exec pour loops. Miroir de workflow-claude-code-optimal, pas une recopie."
aliases:
  - "workflow codex optimal"
  - "workflow openai codex"
  - "codex cli workflow"
  - "comment utiliser codex"
  - "surface map codex"
  - "codex exec loop"
  - "multitasking codex sottiaux"
  - "codex agent-first"
derniere-maj: 2026-09-05
auteur: claude
type: technique
sources:
  - "https://learn.chatgpt.com/docs/ (doc officielle Codex, ex developers.openai.com/codex — redirect 308)"
  - "https://learn.chatgpt.com/docs/changelog (vérifié en primaire le 5 sept. 2026)"
  - "https://learn.chatgpt.com/docs/config-file/config-reference"
  - "https://newsletter.pragmaticengineer.com/p/how-codex-is-built (Gergely Orosz, ~17 fév 2026)"
  - "https://github.com/openai/codex (repo, releases, docs/config.md stub)"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#domaine/workflow"
  - "#doctrine/2026"
---
# Workflow OpenAI Codex optimal (septembre 2026)

> Note maître forge — workflow optimal pour utiliser **OpenAI Codex** (l'agent de code, CLI/IDE/cloud) selon la doc officielle au **5 septembre 2026**. Miroir structurel de [[workflow-claude-code-optimal]] ; **la doctrine Claude Code n'y est pas recopiée** — Codex a ses propres mécanismes, vérifiés en source primaire. Chaque affirmation datée + niveau de confiance (Codex bouge chaque semaine).

---

## ⚠️ Fraîcheur — vérité datée au 05/09/2026

Codex publie plusieurs releases CLI par semaine. Les faits ci-dessous sont datés ; toute donnée volatile (modèle, prix, cap) est marquée `à vérifier` avec sa date. État verrouillé :

- **Modèle par défaut CLI** : **`gpt-6-astra`** depuis la CLI **0.153.4 (4 sept. 2026)**, verbatim changelog : *« Fixed Astra's visibility in the bundled model picker and made it the bundled default when no model is explicitly configured »*. C'est un **défaut de bundle** : il s'applique quand aucun modèle n'est configuré explicitement. Épingler `gpt-5.6-sol` dans `config.toml` reste possible et devient un choix délibéré. ⚠️ L'accès à Astra dépend du déploiement, de la méthode de connexion et du client (doc modèles) — sur un compte non éligible, le modèle servi peut différer.
- **Défaut précédent** : `gpt-5.6-sol` (alias `gpt-5.6`, préréglage « Power » effort medium), du **9 juil.** au **3 sept. 2026**. Toute doctrine antérieure au 4 sept. qui affirme « le défaut est `gpt-5.6-sol` » est périmée.
- **Modèles listés dans le CLI** : `gpt-6-astra`, `gpt-5.6-sol` (flagship), `gpt-5.6-terra` (balanced), `gpt-5.6-luna` (fast/cheap), `gpt-5.3-codex-spark`, `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`. **Dépréciés** : `gpt-5.2`, `gpt-5.3-codex` (sunset legacy 23 juil. 2026). `gpt-5.4` et `gpt-5.4-mini` sont retirés pour la connexion ChatGPT depuis le **31 août 2026** — remplacements conseillés par OpenAI : `gpt-5.6-terra` / `gpt-5.6-luna`.
- **CLI** : `0.153.4` (4 sept.). Minimum pour voir GPT-5.6 = `0.144.0` (9 juil.).
- **Doc officielle a MIGRÉ** : `developers.openai.com/codex/*` → **redirige 308 vers `learn.chatgpt.com/docs/*`**. Le `docs/config.md` du repo GitHub `openai/codex` est devenu un **stub**. Source primaire actuelle = `learn.chatgpt.com/docs/`.

### Changements de comportement à connaître (août-septembre 2026)

Quatre évolutions récentes invalident des réflexes acquis plus tôt dans l'année :

| Depuis | Changement | Conséquence pratique |
|---|---|---|
| 0.150.0 (26 août) | *« Untrusted projects no longer supply project-level `AGENTS.md` instructions »* | Un repo non *trusted* n'injecte plus ses conventions. Un `AGENTS.md` qui « ne fait rien » se diagnostique d'abord par le niveau de confiance du projet. |
| 0.150.0 (26 août) | Hooks **Interrupt** — exécutés quand un tour top-level est interrompu | Nouveau point d'accroche pour le nettoyage ; cf [[comment-creer-hook-codex]]. |
| 0.152.0 (1er sept.) | *« The planning tool is disabled by default; enable it with `tools.update_plan.enabled = true` »* | Toute doctrine qui suppose un plan actif par défaut est fausse. À activer explicitement pour les tâches L/XL. |
| 0.153.0 (3 sept.) | Marketplace de plugins en CLI (list/install/remove depuis des marketplaces distantes) | Un 9ᵉ levier émerge à côté des 8 de la Surface Map ; à surveiller avant de l'inscrire en doctrine. |

---

## QUOI — Codex en une carte

Codex = agent de code agentique d'OpenAI, décliné en surfaces : **CLI** (terminal, Rust ~95 %), **IDE extension** (VS Code / Cursor / Windsurf), **desktop app** (macOS/Windows, devenue la nouvelle app ChatGPT le 9 juil.), **cloud/web** (tâches hébergées parallèles), **Chrome extension / Computer Use**.

Les **8 leviers de configuration** — hiérarchie d'application (« Surface Map », ordre issu de la skill officielle `openai-docs`, *probable*, pas règle canonique) :

```
prompt/thread → AGENTS.md → config.toml → skills → plugins → MCP servers → automations → hooks
```

| Levier | Rôle | Note dédiée |
|--------|------|-------------|
| **AGENTS.md** | conventions durables du repo (≈ CLAUDE.md) | [[agents-md-codex]] |
| **config.toml + profils** | réglages machine/projet, profils nommés | [[config-toml-profils-codex]] |
| **Skills** (`SKILL.md`) | savoir-faire réutilisable | [[comment-creer-skill-codex]] |
| **Subagents** (`.codex/agents/*.toml`) | délégation parallèle | [[subagents-cloud-codex]] |
| **MCP servers** | accès données externes | [[mcp-vs-skills-doctrine]] (doctrine commune) |
| **Automations / cloud tasks** | loops planifiés, exécution hébergée | [[loops-codex]] |
| **Hooks** | enforcement déterministe | [[comment-creer-hook-codex]] |
| **Mémoire `[memories]`** | compounding auto | [[loop-apprentissage-codex]] |

**Doctrine « agent-first »** (Thibault Sottiaux, Head of Codex) : construire un agent général avant de figer les surfaces produit. Le pari produit : *« the same feature set would have failed in November 2025 »* — seul l'écart de 3 mois d'intelligence du modèle explique l'adoption (Andrew Ambrosino, Lenny's Podcast 28 juin 2026).

---

## POURQUOI — Le problème résolu

Sans workflow structuré autour de Codex :
- Config dispersée entre AGENTS.md, config.toml, skills → duplication et dérive.
- Tout en interactif → pas d'automatisation (pas de loops, pas de CI).
- Pas de vérification → qualité aléatoire (le tip #1 de Boris vaut pour tout agent, cf [[concevoir-loops-travail]]).
- Modèle mal choisi → coût ×N.

Avec le workflow optimal : les 8 leviers occupent chacun leur rôle, `codex exec` alimente les loops, la mémoire auto capitalise, le multitasking parallélise.

---

## COMMENT — Multitasking (le cœur de la doctrine Codex)

**Verbatim Sottiaux** (Pragmatic Engineer « How Codex is built », ~17 fév. 2026 — *date de publication à vérifier*) :

> "Codex is really built for multitasking. There's this understanding that most tasks will just get done to completion. People on our team have figured out what Codex is and isn't capable of. There is a tricky thing in all of this, though: we have to relearn these capabilities with every model."

Pratique de l'équipe Codex : **4–8 agents en parallèle**, runs autonomes 20–30 min à ~1 h, runs nocturnes qui scannent le code (fixes en attente le matin). Codex écrit **> 90 %** du code de sa propre app ; l'AI code review flag ~90 % de commentaires valides.

La dernière phrase est la doctrine maîtresse (convergente avec Anthropic, cf [[workflow-claude-code-optimal]] « re-tester les hypothèses du harness à chaque modèle ») : **les capacités se ré-apprennent à chaque modèle**. Ne pas figer un harness sur les limites du modèle d'hier.

⚠️ Cette phrase vient de se vérifier deux fois en une semaine : Anthropic écrit noir sur blanc que les niveaux d'effort *« don't correspond to the same amount of thinking across models »* (cf [[Fable 5.1]]), et le défaut Codex a changé de modèle en 24 h. Le sweep de calibration se refait à chaque bascule, pas une fois pour toutes.

---

## Effort de raisonnement — le champ exact

**`model_reasoning_effort`**, dans `config.toml`. Valeurs acceptées, verbatim de la référence officielle : `minimal | low | medium | high | xhigh`, avec la mention *« Responses API only; `xhigh` is model-dependent »*. Aucun défaut n'est déclaré dans la référence — non défini, le modèle applique le sien.

⚠️ **`ultra`, `max` et `none` ne sont PAS des valeurs valides de ce champ** (vérifié en primaire le 5 sept. 2026). Les libellés de préréglage vus dans l'UI (« Power », « Ultra ») ne sont pas des valeurs de configuration : leur correspondance exacte avec `model_reasoning_effort` n'est pas documentée, ne pas la supposer.

Guidance officielle (*best practices*) : *« Choose a reasoning level based on how hard the task is »* — `low` pour les tâches courtes et bien cadrées, `medium`/`high` pour les changements complexes et le debugging, `xhigh` pour les tâches longues, agentiques, à forte charge de raisonnement.

Champ associé : `model_reasoning_summary` = `auto | concise | detailed | none`.

---

## WORKFLOW — Séquence par taille de tâche

### S (small, < 30 min)
```
codex "<tâche>"        # interactif, sandbox workspace-write, approval on-request
→ vérifier le diff → commit
```
Pas de skill, pas de subagent. Modèle par défaut suffit.

### M (medium, 30 min – 4 h)
```
1. AGENTS.md à jour (conventions repo) — cf [[agents-md-codex]]
2. codex avec un profil adapté si besoin (--profile) — cf [[config-toml-profils-codex]]
3. Skill invoquée si procédure réutilisable ($skill ou implicite)
4. Review : @codex review sur la PR (guidelines depuis AGENTS.md § Review guidelines)
5. commit
```

### L (large, > 4 h ou cross-files)
```
1. AGENTS.md + skills en place
2. Outil de planning ACTIVÉ (tools.update_plan.enabled = true) — off par défaut depuis 0.152.0
3. Délégation subagents (max_threads=6) : "spawn N agents", 1 par sous-tâche
4. model_reasoning_effort = "high" ou "xhigh"
5. Review automatique (settings/code-review) — flag P0/P1
6. commit groupé
```

### XL (multi-jours / récurrent)
```
1. Planning + AGENTS.md exhaustif
2. codex exec en CI/headless sur tâches scriptables (--json, --output-schema)
3. Scheduled tasks (automations) pour le récurrent — cf [[loops-codex]]
4. Loop d'apprentissage : scan sessions → update skills — cf [[loop-apprentissage-codex]]
5. Mémoire auto [memories] active pour le compounding
```

---

## OPTIMISATION — 3 niveaux

### Niveau basique
- AGENTS.md racine + modèle par défaut
- Sandbox `workspace-write` + approval `on-request`
- Pas de skills, pas de hooks, sessions interactives

### Niveau avancé
- AGENTS.md nesté (racine + sous-arbres) + profils config.toml
- 3–10 skills (`.agents/skills`) + quelques subagents (`.codex/agents/*.toml`)
- MCP pour les données ; review automatique des PR
- `codex exec` en CI (action `openai/codex-action@v1`)

### Niveau expert
- Les 8 leviers alignés sur la Surface Map
- Multitasking 4–8 agents ; `model_reasoning_effort` calibré par taille de tâche
- Automations récurrentes + loop d'apprentissage (sessions → skills)
- Mémoire auto `[memories]` + hooks d'enforcement (trust model par hash)
- Enterprise : `requirements.toml` (managed hooks, sandbox/approval imposés)

---

## QUAND — Codex vs autre outil

- **Codex CLI/IDE** : dev interactif local, contrôle fin du sandbox.
- **Codex cloud** : tâches parallèles offloadées, démarrées depuis GitHub/Linear/Slack.
- **ChatGPT seul** (app) : PAS de code agentique — leviers = custom instructions, Projects, mémoire native. Cf [[personnalisation-chatgpt-app]] et l'arbitrage [[codex-vs-chatgpt-seul]].

---

## ANTI-PATTERNS

- ❌ **Figer le harness sur les limites du modèle d'hier** — Sottiaux : les capacités se ré-apprennent à chaque modèle.
- ❌ **Tout mettre dans AGENTS.md** — cap 32 KiB (`project_doc_max_bytes`, *à re-tester*) ; sortir le how-to en skills, l'enforcement en hooks (cf Surface Map).
- ❌ **Présumer un modèle par défaut sans vérifier la version du CLI** — le défaut a changé deux fois en deux mois (`gpt-5.6-sol` le 9 juil., `gpt-6-astra` le 4 sept.). Un anti-pattern daté vaut mieux qu'un nom de modèle gravé : `codex --version` puis le changelog.
- ❌ **Supposer l'outil de planning actif** — désactivé par défaut depuis 0.152.0.
- ❌ **Écrire `ultra`, `max` ou `none` dans `model_reasoning_effort`** — valeurs invalides ; ce sont au mieux des libellés d'UI.
- ❌ **`--full-auto`** — déprécié, préférer `--sandbox workspace-write`.
- ❌ **`--dangerously-bypass-approvals-and-sandbox` (`--yolo`) hors env contrôlé** — bypass total sandbox + approbations.
- ❌ **`approval_policy = "on-failure"`** — déprécié ; utiliser `on-request` (interactif) ou `never` (non-interactif).
- ❌ **Chasser `docs/config.md` du repo** — c'est un stub ; la doc vit sur `learn.chatgpt.com/docs/`.
- ❌ **Recopier la doctrine Claude Code** — Codex a ses propres mécanismes (TOML vs markdown, `.agents/skills` vs `.claude/skills`, trust model par hash).

---

## SOURCES

### Doc officielle OpenAI (source primaire, vérifiée au 05/09/2026)
- `learn.chatgpt.com/docs/` — doc Codex canonique (les URLs `developers.openai.com/codex/*` redirigent 308 ici).
- `learn.chatgpt.com/docs/models` · `/docs/changelog` · `/docs/config-file/config-reference` · `/docs/learn/best-practices` · `/docs/non-interactive-mode` · `/docs/automations` · `/docs/hooks` · `/docs/customization/memories`
- `github.com/openai/codex` — repo (releases `rust-v0.XXX.0`, `docs/config.md` = stub de redirection).

⚠️ **Trou de couverture connu** : le changelog Codex de **mars à juillet 2026** n'a pas été récupéré en source primaire lors de la vérification du 5 sept. (la page ne remonte qu'à fin août, le CHANGELOG brut GitHub ne sert qu'un pointeur). Les faits de cette période proviennent des vérifications de juillet et n'ont pas été recroisés depuis.

### Praticiens / analyses
- **Pragmatic Engineer** « How Codex is built » (Gergely Orosz, ~17 fév. 2026) — multitasking Sottiaux, 100+ skills internes.
- **Lenny's Podcast** « OpenAI Codex lead on the new shape of product work » (Andrew Ambrosino, 28 juin 2026) — taste > implementation, timing modèle.
- **Simon Willison** [tags/codex](https://simonwillison.net/tags/codex/) — reverse-engineering CLI, skills cross-LLM, lethal trifecta appliqué à Codex.

---

## WIKILINKS

### Notes canoniques Codex (corpus 04-Techniques/codex)
- [[agents-md-codex]] · [[config-toml-profils-codex]] · [[comment-creer-skill-codex]] · [[comment-creer-hook-codex]] · [[subagents-cloud-codex]] · [[loops-codex]] · [[loop-apprentissage-codex]] · [[memoire-optimale-codex-chatgpt]] · [[codex-vs-chatgpt-seul]]

### Doctrine commune (ne PAS dupliquer)
- [[mcp-vs-skills-doctrine]] — MCP/Skills/CLI (standard cross-LLM)
- [[Agent Skills Spec]] — spec ouverte adoptée par Codex
- [[concevoir-loops-travail]] — méthode loop universelle (tip #1 vérification)
- [[workflow-claude-code-optimal]] — le miroir Claude Code

### Modèles
- [[GPT-6 Astra]] — défaut CLI depuis le 4 sept. 2026
- [[GPT-5.6]] — famille Sol/Terra/Luna

### Fiches leaders
- [[Thibault Sottiaux]] · [[Michael Bolin]] · [[Fouad Matin]] · [[Andrew Ambrosino]] · [[Gabriel Peal]] · [[Josh McKinney]] · [[Shao-Qian Mah]] · [[Simon Willison]]

### Industrie
- [[OpenAI Codex]] — fiche produit (06-Industrie)
