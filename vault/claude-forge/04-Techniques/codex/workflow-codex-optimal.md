---
titre: "Workflow OpenAI Codex optimal (juillet 2026)"
resume: "Note maître forge — workflow optimal pour l'agent de code OpenAI Codex au 15 juil. 2026 : modèle défaut gpt-5.6-sol, séquence par taille de tâche S/M/L/XL, 3 niveaux d'optimisation, Surface Map des 8 leviers (AGENTS.md → hooks), multitasking Sottiaux, codex exec pour loops. Miroir de workflow-claude-code-optimal, pas une recopie."
aliases:
  - "workflow codex optimal"
  - "workflow openai codex"
  - "codex cli workflow"
  - "comment utiliser codex"
  - "surface map codex"
  - "codex exec loop"
  - "multitasking codex sottiaux"
  - "codex agent-first"
derniere-maj: 2026-07-15
auteur: claude
type: technique
sources:
  - "https://learn.chatgpt.com/docs/ (doc officielle Codex, ex developers.openai.com/codex — redirect 308)"
  - "https://newsletter.pragmaticengineer.com/p/how-codex-is-built (Gergely Orosz, ~17 fév 2026)"
  - "https://github.com/openai/codex (repo, releases, docs/config.md stub)"
  - "https://learn.chatgpt.com/docs/models · /docs/changelog · /docs/non-interactive-mode"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#domaine/workflow"
  - "#doctrine/2026"
---
# Workflow OpenAI Codex optimal (juillet 2026)

> Note maître forge — workflow optimal pour utiliser **OpenAI Codex** (l'agent de code, CLI/IDE/cloud) selon la doc officielle au **15 juillet 2026**. Miroir structurel de [[workflow-claude-code-optimal]] ; **la doctrine Claude Code n'y est pas recopiée** — Codex a ses propres mécanismes, vérifiés en source primaire. Chaque affirmation datée + niveau de confiance (Codex bouge chaque semaine).

---

## ⚠️ Fraîcheur — vérité datée au 15/07/2026

Codex publie plusieurs releases CLI par semaine. Les faits ci-dessous sont datés ; toute donnée volatile (modèle, prix, cap) est marquée `à vérifier` avec sa date. État verrouillé :

- **Modèle par défaut CLI** : `gpt-5.6-sol` (alias `gpt-5.6`, préréglage « Power » effort medium) depuis la GA de GPT-5.6 le **9 juil. 2026**. *Probable* — la doc ne déclare pas de « default = X » verbatim, c'est le préréglage Power. **N'est PAS** GPT-5-Codex (qui reste dispo, orienté API).
- **Famille GPT-5.6** : `sol` (flagship), `terra` (balanced), `luna` (fast/cheap). + `gpt-5.5`, `gpt-5.3-codex-spark`. **Dépréciés** : `gpt-5.2`, `gpt-5.3-codex`. Sunset legacy **23 juil. 2026**.
- **CLI** : `0.144.4` (14 juil.). Minimum pour voir GPT-5.6 = `0.144.0` (9 juil.).
- **Doc officielle a MIGRÉ** : `developers.openai.com/codex/*` → **redirige 308 vers `learn.chatgpt.com/docs/*`**. Le `docs/config.md` du repo GitHub `openai/codex` est devenu un **stub**. Source primaire actuelle = `learn.chatgpt.com/docs/`.

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
- Modèle mal choisi → coût ×N (Sol à $5/$30 vs Luna à $1/$6 par M tokens).

Avec le workflow optimal : les 8 leviers occupent chacun leur rôle, `codex exec` alimente les loops, la mémoire auto capitalise, le multitasking parallélise.

---

## COMMENT — Multitasking (le cœur de la doctrine Codex)

**Verbatim Sottiaux** (Pragmatic Engineer « How Codex is built », ~17 fév. 2026 — *date de publication à vérifier*) :

> "Codex is really built for multitasking. There's this understanding that most tasks will just get done to completion. People on our team have figured out what Codex is and isn't capable of. There is a tricky thing in all of this, though: we have to relearn these capabilities with every model."

Pratique de l'équipe Codex : **4–8 agents en parallèle**, runs autonomes 20–30 min à ~1 h, runs nocturnes qui scannent le code (fixes en attente le matin). Codex écrit **> 90 %** du code de sa propre app ; l'AI code review flag ~90 % de commentaires valides.

La dernière phrase est la doctrine maîtresse (convergente avec Anthropic, cf [[workflow-claude-code-optimal]] « re-tester les hypothèses du harness à chaque modèle ») : **les capacités se ré-apprennent à chaque modèle**. Ne pas figer un harness sur les limites du modèle d'hier.

---

## WORKFLOW — Séquence par taille de tâche

### S (small, < 30 min)
```
codex "<tâche>"        # interactif, sandbox workspace-write, approval on-request
→ vérifier le diff → commit
```
Pas de skill, pas de subagent. Modèle défaut (`gpt-5.6-sol` medium) suffit.

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
2. Délégation subagents (max_threads=6) : "spawn N agents", 1 par sous-tâche
3. Effort élevé (high/xhigh, ou Ultra en UI = active des subagents)
4. Review automatique (settings/code-review) — flag P0/P1
5. commit groupé
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
- AGENTS.md racine + modèle défaut (`gpt-5.6-sol`)
- Sandbox `workspace-write` + approval `on-request`
- Pas de skills, pas de hooks, sessions interactives

### Niveau avancé
- AGENTS.md nesté (racine + sous-arbres) + profils config.toml
- 3–10 skills (`.agents/skills`) + quelques subagents (`.codex/agents/*.toml`)
- MCP pour les données ; review automatique des PR
- `codex exec` en CI (action `openai/codex-action@v1`)

### Niveau expert
- Les 8 leviers alignés sur la Surface Map
- Multitasking 4–8 agents ; effort calibré (Ultra pour le lourd)
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
- ❌ **Tout mettre dans AGENTS.md** — cap 32 KiB (`project_doc_max_bytes`) ; sortir le how-to en skills, l'enforcement en hooks (cf Surface Map).
- ❌ **Présumer que GPT-5-Codex est le défaut** — c'est `gpt-5.6-sol` depuis le 9 juil.
- ❌ **`--full-auto`** — déprécié, préférer `--sandbox workspace-write`.
- ❌ **`--dangerously-bypass-approvals-and-sandbox` (`--yolo`) hors env contrôlé** — bypass total sandbox + approbations.
- ❌ **Chasser `docs/config.md` du repo** — c'est un stub ; la doc vit sur `learn.chatgpt.com/docs/`.
- ❌ **Recopier la doctrine Claude Code** — Codex a ses propres mécanismes (TOML vs markdown, `.agents/skills` vs `.claude/skills`, trust model par hash).

---

## SOURCES

### Doc officielle OpenAI (source primaire, au 15/07/2026)
- `learn.chatgpt.com/docs/` — doc Codex canonique (les URLs `developers.openai.com/codex/*` redirigent 308 ici).
- `learn.chatgpt.com/docs/models` · `/docs/changelog` · `/docs/non-interactive-mode` · `/docs/automations` · `/docs/hooks` · `/docs/customization/memories`
- `github.com/openai/codex` — repo (releases `rust-v0.XXX.0`, `docs/config.md` = stub de redirection).

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

### Fiches leaders
- [[Thibault Sottiaux]] · [[Michael Bolin]] · [[Fouad Matin]] · [[Andrew Ambrosino]] · [[Gabriel Peal]] · [[Josh McKinney]] · [[Shao-Qian Mah]] · [[Simon Willison]]

### Industrie
- [[OpenAI Codex]] — fiche produit (06-Industrie)
