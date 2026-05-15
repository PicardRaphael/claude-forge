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
derniere-maj: 2026-05-09
auteur: claude
tags:
  - "#type/context"
  - "#type/projet"
  - "#projet/neo-ia"
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
