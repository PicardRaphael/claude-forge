---
titre: neo_ia
resume: Monorepo Python NeoChat/NeoDoc/NeoMail — agents conversationnels et documentaires Neoteem
aliases:
  - neo_ia
  - neo ia
  - neoia
  - neochat
  - neodoc
  - neomail
type: context
status: active
derniere-maj: 2026-09-25
auteur: claude
tags:
  - "#type/context"
  - "#type/projet"
  - "#projet/neo_ia"
---
## Description

Monorepo LLM assistants B2B de [[Neoteem|Neoteem]]. 3 apps : NeoChat (agents ReAct), NeoDoc (RAG Vertex AI Search), NeoMail (classification + draft). Projet principal de Raphael.

## Stack

- Python 3.13, uv, ruff, pytest, FastAPI, LangGraph, LangChain, Gemini 2.5 Flash
- Emplacement : `neot-v2/neo_ia` (Bitbucket, branche `develop`)

## Composants Claude Code (audit 2026-05-08)

- **11 agents opus** : architect, codebase-analyst, security-reviewer (high) + dev-neochat, dev-neodoc, dev-neomail, dev-shared-tools, test-writer... (medium)
- **27 skills** : 2 slash, 4 scaffolding, 6 dev, 6 référence métier, 3 qualité, 2 analyse, 1 recap
- **14 rules** : agent-delegation, check-before-create, quality-gates, decompose-ticket-vault-mandatory...
- **9 hooks** Python : architect-guard, commit-guard, ruff, GChat webhook...
- **7 CLAUDE.md** : 1 racine (106L) + 3 apps + 3 packages

## Points à surveiller

- neomail-architecture = 60L (déséquilibre vs neochat 297L, neodoc 363L)
- neodoc-architecture = 363L sans references/ (approche limite 500L)
- pipeline-reset.py présent dans hooks/ mais pas branché dans settings.json

## Liens

- [[Neoteem|Neoteem]]
- [[ia_back|ia_back]]


## Alignement sur neoteem-back-ts (10-12 juin 2026)

État au 12 juin 2026, promu depuis la mémoire projet forge le 25 sept. 2026. Les compteurs de composants ci-dessus (audit 8 mai) sont antérieurs à cet alignement ; compteurs README au 11 juin : 14 agents, 39 skills, 23 hooks, 22 rules.

- **Workflow dev** : `/feature <ticket>` → branche `us/<N°>` → PR vers `develop`, CI verte = condition de merge. Commit direct sur develop/master/main bloqué par `git-guard.py`. Pipeline `/feature` : architect → test-writer → dev → reviewer (contrat Default-FAIL) → `/go` (miroir exact de la CI) → `/ship` → transition Jira après merge. Worktrees parallèles via `claude -w` + `.worktreeinclude`.
- **CI** : `bitbucket-pipelines.yml` est la CI réelle depuis le 11 juin (le repo est sur Bitbucket, GitHub est bloqué par l'org) : ruff + format + mypy + pytest, gates en ratchet sur le legacy (ruff S/N/C90/ERA/ARG, import-linter 3 contrats, jscpd 3 %, gitleaks), tests neodoc/neomail conditionnels par chemin. `.github/workflows/ci.yml` ne s'exécute pas mais reste dans le repo et continue d'être modifié en parallèle (encore le 17 juin, commit `f18d9c4d`, contract test ia_back_client ajouté aux deux fichiers). Leçon : vérifier l'hébergement réel avant de croire un fichier CI.
- **Périmètre prod** : neochat seul en prod ; neodoc/neomail hors prod (refacto à venir), exclus du strict mais interdits à l'import depuis neochat (contrat import-linter).
- **reuse-first** : classement RÉUTILISER/PACKAGES/LOCAL obligatoire au plan architecte ; un doublon est BLOQUANT en review.
- **MCP Langfuse (design v2)** : un seul serveur `langfuse-neochat`, stdio via le wrapper `scripts/mcp_langfuse.py` qui lit `.env` et lance `uvx mcp-proxy` avec l'en-tête Basic. `.mcp.json` sans aucun secret, pas de variable d'environnement Windows ; onboarding = clone + `.env`. Fait vérifié : le MCP officiel Langfuse n'accepte que des clés projet, donc un MCP par projet Langfuse.
- **Jira IA** : 6 epics permanents — Chatbots N2-68082, Agents N2-106433, Mail N2-111277, MCP N2-111230, Outils internes N2-111276, NeoDoc N2-103047. Types `[IA] FEATURE` / `[IA] BUG` / `[IA] A CLASSER` ; création N2 via le MCP `plugin:atlassian` (le MCP JIRA - NEOTEEM est Service-Desk-only). Classement par nature du ticket : feedback forge `memory/feedback_classification_type_ticket_jira.md`.
- **Différé (P1)** : promptfoo redteam, Presidio (AI Act), DeepEval gating, budgets Langfuse. Détail : `neo_ia/docs/implementation-notes/harnais-repo-parfait.md`.
- **Actions humaines** (revérifié le 25 sept. 2026 sur `develop`) :
  - `.claude/settings.local.json.proposed` n'existe plus : appliqué ou retiré.
  - `.github/workflows/ci.yml` est toujours présent. Le supprimer est une décision d'équipe, tant qu'il est maintenu en miroir.
  - Type Jira `[IA] Optimisation` (N2-111316 à rebasculer) : non revérifié.

## Architecture détaillée par app

### NeoChat (documentation profonde)
- [[neochat-architecture]] — Vue d'ensemble : 7 agents, 26 tools, 6 interrupt handlers
- [[neochat-react-engine]] — Declarative ReAct Engine 7 phases (AgentBlueprint)
- [[neochat-adaptive-prompt]] — Prompt Builder V2 4 layers (cache Gemini)
- [[neochat-tool-rag]] — HybridToolSelector pgvector (full-text + semantic + RRF)

### NeoDoc (documentation profonde)
- [[neodoc-architecture]] — Vue d'ensemble : RAG Vertex AI Discovery Engine, workspaces multi-tenant, notes indexables
- [[neodoc-research-agent]] — Agent Research LangGraph 5 nœuds (decompose → retrieve → generate → respond)
- [[neodoc-ingestion-pipeline]] — Pipeline 7 étapes : Drive/upload → GCS → Vertex AI Discovery Engine

### NeoMail (documentation profonde)
- [[neomail-architecture]] — Vue d'ensemble : webhook Pub/Sub, classification LLM, 21 tools, BROUILLON ONLY
- [[neomail-webhook-pipeline]] — Pipeline 10 étapes : Pub/Sub → classify → label → auto-reply draft


## Refonte hooks 22 mai 2026

Suppression de 7 hooks workflow (architect-guard, commit-guard, dispatch-guard, marker-protect, agent-marker-writer, pipeline-reset, session-reset-markers) suite à friction 6×. Doctrine encodée dans `rules/quality-gates.md` + `rules/when-to-architect.md`. Architect split en `architect-quick` (sonnet) + `architect-deep` (opus xhigh).

Hooks restants (8) : `repo-scope-guard`, `guard-pytest-scope`, `auth-detector`, `auth-cleanup`, `on-push-notify`, `session-health`, `spec-brief-boundary-guard`, + ruff format/check inline. Tous = lint/test/security/observabilité légitimes selon doctrine Anthropic.

Voir [[raisonnement-22mai-doctrine-vs-enforcement]].


## Critiques

- [[critique-2026-05-22-audit-neo_ia]] — DA audit consolidé neo_ia. 3 bloquants manqués dont 1 sécurité critique (password Postgres en clair commit ffb5963). VERDICT REVISE.

## Explorations

- [[neo-ia-tests-lenteur-diagnostic]] — Diagnostic root cause de la lenteur des tests neo_ia : clean_caches autouse + log_cli + absence de pytest-xdist + pytest 9 incompatible options.
