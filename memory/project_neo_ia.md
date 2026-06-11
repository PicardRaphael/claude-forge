---
name: neo-ia-project
description: Phase ephemere neo_ia — aligné sur le modèle neoteem-back-ts le 10 juin 2026 (/feature, Default-FAIL, memory/ compounding, workflow PR, CI Bitbucket réparée). Contexte stable dans vault/1-Projets/Neoteem/neo_ia/
type: project
originSessionId: be761cf9-3fd0-4016-adb8-3e189b4efb1f
---
## neo_ia — Phase actuelle

Contexte stable → voir `vault/claude-forge/1-Projets/Neoteem/neo_ia/neo_ia.md`

### Worktrees parallèles portés (2026-06-11, commit 0e0a696 develop)

Même système que neoteem-back-ts : `claude -w` + `/feature <ticket>` par terminal. `.worktreeinclude` (.env/.mcp.json/settings.local.json), skill feature worktree-aware (uv sync si .venv absent, étapes 2+9), section .claude/README, **fix config-guard** (chemin relatif au worktree, testé 5 chemins — sans lui les sous-agents étaient bloqués en écriture dans tout worktree). Commit fait DEPUIS un worktree temporaire (checkout principal alors occupé par us/N2-111316). Cf memory reference_worktree_natif_vs_convention_develop.

### Phase en cours (2026-06-10) — alignement modèle neoteem-back-ts LIVRÉ (commit ade18c2, develop)

12 agents · 36 skills · 18 rules · 18 hooks. Décisions Raphael (AskUserQuestion) : mémoire pattern back-ts complet + /feature complet + **workflow PR vers develop** (fin des commits directs).

- **`/feature`** : pipeline orchestré architect-sanity-check|architect-deep → test-writer → dev-{app}|dev-lead → reviewer (+ prompt-eval-runner/outcomes-test conditionnels) → /go → /ship → transition Jira après merge (découverte dynamique, workflow N2 partagé support).
- **Harness** : contrat Default-FAIL (reviewer + /go), anti-rationalisation (/feature), /go = miroir exact CI (mypy ajouté).
- **Mémoire** : `memory/` versionné + `@memory/MEMORY.md` dans CLAUDE.md + hooks learning-reminder (Stop) / memory-watcher (SessionStart, nettoie le marker). agent-memory/ par agent conservé.
- **Git PR** : rule git-pr-convention + hook git-guard.py (develop/master/main, exit 2, testé 6 adverses/5 légitimes) + /ship → push branche + URL PR Bitbucket.
- **⚠️ DÉCOUVERTE MAJEURE : la CI ne tournait PAS** — `.github/workflows/ci.yml` (GitHub Actions) sur un repo Bitbucket = config morte. `bitbucket-pipelines.yml` créé (miroir : ruff + format --check + mypy + pytest 4 dirs ; functional = pipeline custom).
- **Purge drift** : templates spec references/ TODO/ → docs/stories/s<N>/, tdd-guard/ supprimé, double Gotchas CLAUDE.md fusionné, MEMORY.md racine migré (pointeurs rules morts when-to-architect/agent-delegation → agent-routing/agent-limits corrigés).

**CI Bitbucket Pipelines ACTIVE (confirmé Raphael 11 juin 2026).** Escalade-detector corrigé (lit la queue du transcript, commit 3102a0c).

### Chantier « repo parfait » 11 juin 2026 (aligné neoteem-back-ts) — LIVRÉ develop

- **Alignement workflows** (3 vagues, gap analysis 26 manquants) : 5 hooks sécu portés (secrets-guard, config-guard, typecheck mypy Stop, guard-type-ignore, file-size-guard) · agents performance + security-auditor (adaptés stack LLM : N+1/latence LangGraph/tokens · 4 risques IA + OWASP) déclenchés /feature étape 7 · reviewer doté du bloc ESCALADE structuré · skills /test /notes /debugging-methodology · rules conventions-code/file-size-limit/recherche-avant-code/**reuse-first**.
- **reuse-first** (raison d'être monorepo) : classement RÉUTILISER/PACKAGES/LOCAL obligatoire au plan architecte + gate /feature « À TRANCHER » → AskUserQuestion + doublon = BLOQUANT review. refactor-scan v2 = audit conformité complet (archi/conventions/dérive docs/outils mécaniques), déclenché par « refacto ».
- **P0 outillage CI** (ratchet partout, recherches web sources primaires) : ruff étendu S/N/C90/ERA/ARG (286 noqa baseline legacy) · import-linter 3 contrats frontières (scripts/check_imports.py contourne AppLocker comme turbo.exe) · jscpd seuil 3 % (mesuré 1,93 %) · pip-audit (non bloquant) · gitleaks pipe natif · **CI conditionnelle par chemin** (neodoc/neomail testés seulement si touchés). docs/pipeline.md.
- **Refonte docs/ vivante** : architecture.md orienteur, 01-overview + 05-tools corrigés au réel (3 apps/6 agents/17 tools), conflit double 13 résolu, 8 fichiers périmés supprimés (ARCHITECTURE_REPORT, agent_devis, superpowers, notes mergées). neodoc/neomail = bandeau « à réécrire avec leur refacto ».
- **Décisions** : neomail/neodoc HORS PROD (refacto à venir) → exclus du strict ruff/import-linter + tests CI conditionnels, mais neochat (prod) ne peut jamais les importer (contrat import-linter). Rien de lourd en PostToolUse (« ruff pas H24 »). Story durcissement SQL shared_utils rédigée (5 S608 faux positifs à corriger sans noqa). Compteurs README : 14 agents / 39 skills / 23 hooks / 22 rules.
- **P1 différé** (couche agents IA, stories /spec) : promptfoo redteam · Presidio (AI Act deadline 2 août 2026) · DeepEval gating durci · budgets Langfuse. deptry + Semgrep différés (faux positifs workspace / couvert par ruff S). Détail : `neot-v2/neo_ia/docs/implementation-notes/harnais-repo-parfait.md`.

**Actions humaines restantes** : supprimer ou garder .github/workflows/ci.yml (mort) · prévenir l'équipe du workflow PR (git-guard actif à la prochaine session) · `.claude/settings.local.json.proposed` en attente d'application manuelle.

**Why:** ancien ci.yml jamais exécuté (org bloque GitHub, repo Bitbucket) — toujours vérifier l'hébergement réel avant de croire un fichier CI.
**How to apply:** dev neo_ia = `/feature <N°ticket>` → branche us/{N°} → PR develop, CI verte = condition de merge. Jamais de commit direct (git-guard bloque).
