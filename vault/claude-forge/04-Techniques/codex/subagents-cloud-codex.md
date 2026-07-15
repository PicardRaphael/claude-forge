---
titre: "Subagents, cloud et automations Codex — délégation et parallélisme"
resume: "Note canonique forge — subagents Codex (fichiers TOML .codex/agents/, champs name/description/developer_instructions, built-ins default/worker/explorer, max_threads=6/max_depth=1, CSV batch), cloud tasks hébergées, automations planifiées (RRULE). Vérifié doc officielle au 15 juil. 2026."
aliases:
  - "subagents codex"
  - "codex agents toml"
  - "developer_instructions"
  - "max_threads max_depth codex"
  - "spawn_agents_on_csv"
  - "codex cloud tasks"
  - "automations codex scheduled"
  - "codex built-in agents explorer worker"
derniere-maj: 2026-07-15
auteur: claude
type: technique
sources:
  - "https://learn.chatgpt.com/docs/agent-configuration/subagents"
  - "https://learn.chatgpt.com/docs/cloud · /docs/automations"
  - "https://github.com/openai/codex"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#doctrine/2026"
---
# Subagents, cloud et automations Codex

> Note canonique forge — délégation parallèle Codex (subagents), exécution hébergée (cloud), planification récurrente (automations). Vérifié au **15 juil. 2026**. Les TOML de subagents sont lus en markdown brut (CERTAIN) ; cloud/automations via résumé (PROBABLE sauf mention).

---

## SUBAGENTS (CERTAIN, TOML lus en raw)

### Format — un fichier TOML = un agent

Emplacements : `~/.codex/agents/` (perso) ou `.codex/agents/` (projet). Champs **obligatoires** : `name`, `description`, **`developer_instructions`** (pas `instructions`). `name` = source de vérité (pas le nom de fichier). Champs optionnels (hérités du parent si omis) : `nickname_candidates`, `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`.

```toml
# .codex/agents/reviewer.toml
name = "reviewer"
description = "PR reviewer focused on correctness, security, and missing tests."
model = "gpt-5.4"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
developer_instructions = """
Review code like an owner.
Prioritize correctness, security, behavior regressions, and missing test coverage.
Lead with concrete findings; avoid style-only comments unless they hide a real bug.
"""
```

MCP et skills par agent :
```toml
[mcp_servers.chrome_devtools]
url = "http://localhost:3000/mcp"
startup_timeout_sec = 20

[[skills.config]]
path = "/Users/me/.agents/skills/docs-editor/SKILL.md"
enabled = false
```

**Effort — 8 valeurs** : `ultra | max | xhigh | high | medium | low | minimal | none`.

### Built-ins sans fichier

`default` (fallback généraliste), `worker` (exécution), `explorer` (read-heavy). Un custom du même nom prend le dessus.

### Délégation + parallélisme

- Déclenchement : **explicite** (« spawn two agents », « delegate this in parallel », « use one agent per point ») OU **implicite** (une instruction `AGENTS.md`/skill le demande).
- Codex **attend tous les subagents** puis renvoie une réponse consolidée (orchestration gérée par Codex, pas par un agent-leader — convergent avec la doctrine forge « la session principale orchestre », cf [[anti-reentrance-sub-agents-pattern-escalade]]).
- Plafonds (`[agents]` dans config.toml) :
```toml
[agents]
max_threads = 6      # défaut : threads d'agents concurrents
max_depth = 1        # défaut : root spawn enfants directs, PAS de petits-enfants
```
`job_max_runtime_seconds` (défaut 1800) pour les jobs CSV, `interrupt_message` (défaut true).

### CSV batch — `spawn_agents_on_csv` (EXPÉRIMENTAL)

1 worker subagent par ligne CSV, résultats ré-exportés en CSV. Chaque worker doit appeler `report_agent_job_result` **exactement une fois**. Params : `csv_path`, `instruction` (placeholders `{column}`), `id_column`, `output_schema`, `output_csv_path`, `max_concurrency`. État des jobs en SQLite (`sqlite_home`).

### vs Claude Code agent

| | Codex | Claude Code |
|--|-------|-------------|
| Format | **TOML** (1 fichier = 1 agent) | markdown + frontmatter YAML |
| Instructions | clé `developer_instructions` | corps markdown |
| Built-ins nommés | `default`/`worker`/`explorer` | aucun |
| Parallélisme déclaratif | `max_threads`/`max_depth` | pas d'équivalent |
| Skills liées | `[[skills.config]]` path+enabled | `skills:` frontmatter |

---

## CLOUD TASKS (PROBABLE)

Codex cloud exécute des tâches dans des **environnements hébergés isolés, en parallèle**, lançables depuis web/GitHub/Linear/Slack. Séquence : `chatgpt.com/codex` → connecter GitHub → créer un environnement (`.../settings/environments`) → décrire le résultat → laisser tourner en background → review summary+diff → PR. Pas de cap numérique de tâches parallèles documenté. Usage : background, comparer plusieurs tentatives, travail loin de sa machine.

---

## AUTOMATIONS / SCHEDULED TASKS (PROBABLE, sauf RRULE CERTAIN)

Cron-like pour workflows IA, gérées via **ChatGPT web ou desktop app** (⚠️ **PAS** la CLI/IDE — qui servent à préparer/tester le prompt). Vue latérale « Scheduled » (active/paused/completed).

- **Deux modes** : *standalone* (chaque run repart du prompt à zéro) vs *follow-up-in-thread* (retour dans la même conversation, contexte réutilisé = le « follow-up work »).
- **Cadence** : presets (daily/weekly/custom) + intervalles à la minute ; règle de récurrence **RFC 5545 (RRULE)** — `RRULE:FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=9;BYMINUTE=0`.
- Peut invoquer une skill : `Check my commits from the last 24h and submit a $recent-code-bugfix.`
- Web = cloud (pas d'accès aux dossiers locaux) ; Desktop = projet local ou **worktree Git dédié** en background (machine allumée + app ouverte).

Ces automations sont **l'équivalent natif du pattern Boris** (« une routine qui prompte l'agent ») et le socle du loop d'apprentissage — cf [[loops-codex]] et [[loop-apprentissage-codex]].

---

## ANTI-PATTERNS

- ❌ **Champ `instructions`** dans un TOML de subagent — c'est `developer_instructions`.
- ❌ **Attendre des petits-enfants d'agents** — `max_depth=1` par défaut (root → enfants directs seulement).
- ❌ **Gérer les Scheduled tasks depuis la CLI/IDE** — interface web/desktop only.
- ❌ **Croire un cap chiffré de tâches cloud //** — non documenté.
- ❌ **Un worker CSV qui n'appelle pas `report_agent_job_result` (ou 2×)** — contrat = exactement 1 appel.

---

## SOURCES

- `learn.chatgpt.com/docs/agent-configuration/subagents` (TOML lus en raw, CERTAIN).
- `learn.chatgpt.com/docs/cloud` · `/docs/automations` (PROBABLE, résumé).
- RRULE RFC 5545 : verbatim doc automations.

---

## WIKILINKS

- [[workflow-codex-optimal]] — note maître (délégation dans le workflow L/XL)
- [[config-toml-profils-codex]] — `[agents]`, sandbox par agent, MCP par agent
- [[loops-codex]] — automations comme loop
- [[loop-apprentissage-codex]] — scheduled task « scan sessions → update skills »
- [[comment-creer-skill-codex]] — `[[skills.config]]`
- [[anti-reentrance-sub-agents-pattern-escalade]] — orchestration par la session principale (doctrine forge)
