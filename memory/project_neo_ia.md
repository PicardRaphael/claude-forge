---
name: neo-ia-project
description: Phase ephemere neo_ia — aligné sur le modèle neoteem-back-ts le 10 juin 2026 (/feature, Default-FAIL, memory/ compounding, workflow PR, CI Bitbucket réparée). Contexte stable dans vault/1-Projets/Neoteem/neo_ia/
type: project
originSessionId: be761cf9-3fd0-4016-adb8-3e189b4efb1f
---
## neo_ia — Phase actuelle

Contexte stable → voir `vault/claude-forge/1-Projets/Neoteem/neo_ia/neo_ia.md`

### Phase en cours (2026-06-10) — alignement modèle neoteem-back-ts LIVRÉ (commit ade18c2, develop)

12 agents · 36 skills · 18 rules · 18 hooks. Décisions Raphael (AskUserQuestion) : mémoire pattern back-ts complet + /feature complet + **workflow PR vers develop** (fin des commits directs).

- **`/feature`** : pipeline orchestré architect-sanity-check|architect-deep → test-writer → dev-{app}|dev-lead → reviewer (+ prompt-eval-runner/outcomes-test conditionnels) → /go → /ship → transition Jira après merge (découverte dynamique, workflow N2 partagé support).
- **Harness** : contrat Default-FAIL (reviewer + /go), anti-rationalisation (/feature), /go = miroir exact CI (mypy ajouté).
- **Mémoire** : `memory/` versionné + `@memory/MEMORY.md` dans CLAUDE.md + hooks learning-reminder (Stop) / memory-watcher (SessionStart, nettoie le marker). agent-memory/ par agent conservé.
- **Git PR** : rule git-pr-convention + hook git-guard.py (develop/master/main, exit 2, testé 6 adverses/5 légitimes) + /ship → push branche + URL PR Bitbucket.
- **⚠️ DÉCOUVERTE MAJEURE : la CI ne tournait PAS** — `.github/workflows/ci.yml` (GitHub Actions) sur un repo Bitbucket = config morte. `bitbucket-pipelines.yml` créé (miroir : ruff + format --check + mypy + pytest 4 dirs ; functional = pipeline custom).
- **Purge drift** : templates spec references/ TODO/ → docs/stories/s<N>/, tdd-guard/ supprimé, double Gotchas CLAUDE.md fusionné, MEMORY.md racine migré (pointeurs rules morts when-to-architect/agent-delegation → agent-routing/agent-limits corrigés).

**Actions humaines restantes** : activer Bitbucket Pipelines (settings repo) · supprimer ou garder .github/workflows/ci.yml (mort) · prévenir l'équipe du workflow PR (git-guard actif à la prochaine session) · `.claude/settings.local.json.proposed` en attente d'application manuelle.

**Why:** ancien ci.yml jamais exécuté (org bloque GitHub, repo Bitbucket) — toujours vérifier l'hébergement réel avant de croire un fichier CI.
**How to apply:** dev neo_ia = `/feature <N°ticket>` → branche us/{N°} → PR develop, CI verte = condition de merge. Jamais de commit direct (git-guard bloque).
