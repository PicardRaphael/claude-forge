---
titre: "Loops de travail avec Codex — codex exec, automations, CI"
resume: "Note canonique forge — comment tourner des loops avec Codex : exécution non-interactive codex exec (flags, JSONL, pipe shell), automations planifiées (équivalent natif du pattern Boris), intégration CI (openai/codex-action, review PR automatique). Vérifié doc officielle au 15 juil. 2026."
aliases:
  - "loops codex"
  - "codex exec"
  - "codex headless"
  - "codex ci github action"
  - "automations codex loop"
  - "codex exec json output-schema"
  - "codex pattern boris routine"
derniere-maj: 2026-07-15
auteur: claude
type: technique
sources:
  - "https://learn.chatgpt.com/docs/non-interactive-mode"
  - "https://learn.chatgpt.com/docs/automations · /docs/github-action · /docs/third-party/github"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#domaine/workflow"
  - "#doctrine/2026"
---
# Loops de travail avec Codex

> Note canonique forge — les mécanismes pour faire tourner Codex en boucle sans le re-prompter à la main : `codex exec` (headless), automations (planifié), CI. La méthode universelle de conception d'un loop (4 briques, vérification, idempotence, garde-fous) vit dans [[concevoir-loops-travail]] — cette note donne les **outils Codex** qui l'instancient. Vérifié au **15 juil. 2026**.

---

## 1. `codex exec` — exécution non-interactive (CERTAIN)

`codex exec "<prompt>"` (alias `codex e`) lance Codex en headless. « Progress goes to `stderr`; only the final agent message goes to `stdout`. » Exit non-zero en cas d'échec.

**Flags clés** :
- `--sandbox <mode>` — défaut `read-only` ; `workspace-write` pour éditer ; `danger-full-access` env contrôlé.
- `--json` — stdout devient un flux JSONL (`thread.started`, `turn.started/completed/failed`, `item.*`, `error`).
- `--output-schema ./schema.json` — force une sortie finale conforme à un JSON Schema.
- `-o <path>` / `--output-last-message <path>` — écrit le message final dans un fichier.
- `--ephemeral` — ne persiste pas la session sur disque.
- `--ignore-user-config`, `--ignore-rules`, `--skip-git-repo-check`.
- `--dangerously-bypass-approvals-and-sandbox` (alias `--yolo`) — bypass total (dangereux).
- `--full-auto` — **DÉPRÉCIÉ**, préférer `--sandbox workspace-write`.
- `-` — force la lecture du prompt depuis stdin.
- Reprise : `codex exec resume --last "<suite>"` ou `codex exec resume <SESSION_ID>`.

**Patterns loop shell** (le « loop » minimal) :
```bash
npm test 2>&1 | codex exec "summarize the failing tests and propose the smallest likely fix"
cat prompt.txt | codex exec -
generate_prompt.sh | codex exec - --json > result.jsonl
codex exec "Extract project metadata" --output-schema ./schema.json -o ./project-metadata.json
```

**Auth automatisation** : `CODEX_API_KEY` supporté **uniquement dans `codex exec`** :
```bash
CODEX_API_KEY=<api-key> codex exec --json "triage open bug reports"
```

---

## 2. Automations planifiées — l'équivalent natif du pattern Boris (CERTAIN pour l'existence)

Le pattern Boris « écrire une routine qui prompte l'agent sur un calendrier » (cf [[concevoir-loops-travail]], [[pre-compute-vs-inference-loops-boris]]) a un **équivalent natif documenté** : les **automations / scheduled tasks** Codex.

- Récurrence RFC 5545 (RRULE), presets + intervalles minute.
- Deux modes : standalone vs follow-up-in-thread.
- Gérées via web/desktop (pas CLI/IDE). Détail complet : [[subagents-cloud-codex]] § Automations.
- Une tâche planifiée peut invoquer une skill (`$skill`) et tourner dans un worktree Git dédié.

C'est le socle du **loop d'apprentissage** (cf [[loop-apprentissage-codex]]).

---

## 3. Intégration CI (CERTAIN)

**Action officielle `openai/codex-action@v1`** : installe le CLI, lance un proxy Responses API (limite l'exposition de la clé), exécute `codex exec`, poste la réponse sur la PR.
```yaml
- uses: actions/checkout@v5
- name: Run Codex
  uses: openai/codex-action@v1
  with:
    openai-api-key: ${{ secrets.OPENAI_API_KEY }}
    prompt-file: .github/codex/prompts/review.md
    output-file: codex-output.md
```
**Sécurité CI** : ne pas exposer la clé en variable job-level si du code du repo tourne dans le même job → job `generate_fix` en `contents: read` seul, job `open_pr` séparé avec droits d'écriture (verbatim doc).

**Review PR automatique** : activable dans `chatgpt.com/codex/settings/code-review` (review chaque nouvelle PR sans `@codex review`). Commandes : `@codex review`, `@codex review for security regressions`, `@codex fix the CI failures`. Un `@codex fix`/mention **démarre une cloud task** avec la PR en contexte. Guidelines lues depuis `## Review guidelines` de l'`AGENTS.md` le plus proche ; flag P0/P1 seulement.

> « OpenAI review 100 % de ses PRs avec Codex » : formule *à vérifier* — introuvable verbatim sur les docs OpenAI actuelles (source tierce Level Up Coding ; Greg Brockman la décrit comme un « safety net »). Ne pas la citer comme fait officiel.

---

## Vérification, idempotence, garde-fous

Non répété ici : le **tip #1 de Boris** (« give the agent a way to verify its work → 2-3× quality »), l'idempotence et les 4 garde-fous d'un loop autonome sont dans [[concevoir-loops-travail]]. Ils s'appliquent intégralement à un loop Codex : un `codex exec` en CI doit avoir sa condition de vérif (tests verts, `--output-schema`), une automation doit être idempotente (ne pas re-poster/re-créer), avec kill-switch et log.

---

## ANTI-PATTERNS

- ❌ **`--full-auto`** — déprécié.
- ❌ **`--yolo` hors env contrôlé** — bypass total sandbox + approbations.
- ❌ **Clé API en variable job-level** avec code repo dans le même job — séparer les jobs.
- ❌ **Loop `codex exec` sans vérification** — cf tip #1.
- ❌ **Citer « 100 % des PRs OpenAI » comme fait** — non confirmé en primaire.
- ❌ **Gérer les automations depuis la CLI** — web/desktop only.

---

## SOURCES

- `learn.chatgpt.com/docs/non-interactive-mode` (flags `codex exec`, CERTAIN verbatim).
- `learn.chatgpt.com/docs/github-action` · `/docs/third-party/github` (CI + review PR).
- `learn.chatgpt.com/docs/automations` (planification).

---

## WIKILINKS

- [[workflow-codex-optimal]] — note maître (loops dans le workflow XL)
- [[concevoir-loops-travail]] — méthode universelle (4 briques, vérif, idempotence, garde-fous)
- [[pre-compute-vs-inference-loops-boris]] — le pourquoi (pre-compute > inference)
- [[loop-apprentissage-codex]] — le loop de compounding spécifique
- [[subagents-cloud-codex]] — automations + cloud en détail
- [[Thibault Sottiaux]] — multitasking
