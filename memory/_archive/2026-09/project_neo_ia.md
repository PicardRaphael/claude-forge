---
name: neo-ia-project
description: Phase ephemere neo_ia — aligné sur le modèle neoteem-back-ts le 10 juin 2026 (/feature, Default-FAIL, memory/ compounding, workflow PR, CI Bitbucket réparée). Contexte stable dans vault/1-Projets/Neoteem/neo_ia/
type: project
status: review-required
expires: 2026-09-15
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

### Jira IA — hiérarchie réelle (vérifiée 11 juin 2026)
- **6 epics permanents** (pas 5) : Chatbots N2-68082 (+socle backend partagé qui sert les assistants), Agents N2-106433, Mail N2-111277, MCP N2-111230, Outils internes N2-111276, NeoDoc N2-103047.
- **Création N2 via MCP `plugin:atlassian:atlassian`** (OAuth), cloudId `neoteem.atlassian.net`, `createJiraIssue` accepte `issueTypeName`. `MCP JIRA - NEOTEEM` = Service-Desk-only (pas de création N2).
- **Types** : `[IA] FEATURE` (10653), `[IA] BUG` (10652), `[IA] A CLASSER` (10654). `[IA] Optimisation` créé par le PO (en attente — mapping skills prêt par nom).
- /spec ×3 + skill forge neoteem-back-ts portent la classification FEATURE/BUG/OPTIMISATION + routage 6 epics (commits neo_ia 55cd899 / back-ts 4653f40 / forge 96e2b37). Cf [[classification-type-ticket-jira]].
- Story durcissement SQL = N2-111316 (`[IA] BUG`, parent N2-68082), à rebasculer en `[IA] Optimisation` quand le type existera.

### Audit plugins neo_ia (12 juin 2026) — DÉSINSTALLATION FAITE par Raphael

superpowers + feature-dev désinstallés (registre + enabledPlugins propres). **Portage zéro-régression** : la substance d'executing-plans condensée dans les 3 agents dev (review critique du plan avant exécution, batch de 3 + checkpoint, STOP sur blocker) — exigence Raphael « on va pas régresser », jamais supprimer une réf plugin sans porter sa valeur. claude-hud installé+disabled = état correct (statusline, cf [[plugin-vs-skill-anatomie]]). **Restes machine** : plugin-dev rétrogradé local (override false PERDU lors du remaniement settings → va se recharger, désinstaller pour de bon) · frontend-design fantôme (pointe Documents\neo_ia inexistant) + entrée projects Documents/neo_ia fantôme dans ~/.claude.json (langfuse) · caches orphelins superpowers 1,8M + feature-dev 56K · figma toujours enabled (à trancher). Modifs agents en working tree develop, NON committées.

**MCP Langfuse neo_ia (DESIGN FINAL v2, 12 juin)** : UN SEUL serveur `langfuse-neochat`, transport stdio via **wrapper `scripts/mcp_langfuse.py`** (zéro secret : lit `.env` → token base64 → `uvx mcp-proxy --transport streamablehttp --headers Authorization "Basic <tok>" <url>`). Exigences Raphael : un seul MCP + pas de credentials en dur + **pas d'env var Windows (impartageable)** — le `.env` est LA source. Testé LIVE 200 OK + négo protocole MCP. `.mcp.json` ne contient plus AUCUN secret → candidat dé-gitignore (décision équipe, .gitignore L82) ; script à committer. Onboarding collègue = clone + .env, ZÉRO config. Env vars LANGFUSE_MCP_TOKEN_* du registre Windows devenues inutiles (posées plus tôt ce jour, supprimables). Rappel doc : ${VAR} de .mcp.json résolu depuis l'env du process CC uniquement, AUCUN champ envFile n'existe → wrapper stdio = LE pattern pour .env. Décision produit liée : consolidation Langfuse 1 projet + tags par app (neochat/neomail/neodoc) à venir — story [IA] OPTIMISATION, vault confirme « tracing only, pas de prompt management runtime » (neochat-architecture) → consolidation quasi gratuite. Justification : neodoc/neomail HORS PROD → leurs MCP retirés de .mcp.json + enabledMcpjsonServers (settings.json versionné, non committé). FAITS VÉRIFIÉS (sources primaires) : MCP officiel Langfuse = project-scoped keys ONLY, clés org explicitement rejetées → 1 MCP par projet incompressible ; alternative avivsinai/langfuse-mcp (96⭐, Python, uvx) = multi-projets via HTTP partagé MAIS toujours 1 entrée MCP par projet côté client (l'« argument project par tool » de DeepWiki = hallucination, absent du README). Si besoin multi-apps revient (neodoc/neomail en prod) : option MCP FastMCP maison wrappant l'API REST avec param app (clés .env), ou réévaluer l'issue langfuse#12738 (OAuth/OIDC). Onboarding collègue : copier .mcp.json (zéro secret dedans) + poser SA var LANGFUSE_MCP_TOKEN_NEOCHAT. Historique session : .mcp.json avait disparu chez Raphael (restauré de ac544d5), tokens jamais générés nulle part (cause racine), épisode tokens en dur écrit puis ANNULÉ sur refus Raphael, fausse alerte rotation corrigée (${VAR} dans l'historique git, pas de clés). context7/docs-langchain = user-scope ~/.claude.json Raphael, PAS partagés équipe.

**Actions humaines restantes** : supprimer ou garder .github/workflows/ci.yml (mort) · prévenir l'équipe du workflow PR (git-guard actif à la prochaine session) · `.claude/settings.local.json.proposed` en attente d'application manuelle · **PM crée le type Jira `[IA] Optimisation`**.

**Why:** ancien ci.yml jamais exécuté (org bloque GitHub, repo Bitbucket) — toujours vérifier l'hébergement réel avant de croire un fichier CI.
**How to apply:** dev neo_ia = `/feature <N°ticket>` → branche us/{N°} → PR develop, CI verte = condition de merge. Jamais de commit direct (git-guard bloque).
