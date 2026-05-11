---
titre: "NeoMail Architecture — Vue d'ensemble"
resume: "App autonome de traitement mail Gmail : webhook Pub/Sub, classification LLM, auto-reply brouillon, Declarative ReAct Engine partagé avec NeoChat, 21 tools (17 Gmail + 4 Lojii), règle BROUILLON ONLY"
aliases:
  - "neomail architecture"
  - "architecture neomail"
  - "neomail overview"
  - "neomail archi"
  - "pipeline webhook gmail"
type: context
status: active
derniere-maj: 2026-05-11
auteur: claude
tags:
  - "#type/context"
  - "#projet/neo-ia"
  - "#domaine/agents"
  - "#domaine/ia"
---

## Vue d'ensemble

NeoMail est une app FastAPI autonome dans le monorepo [[neo_ia]], dédiée au traitement automatique des mails Gmail. Elle combine deux modes :

1. **Pipeline automatique (webhook)** : réception Pub/Sub → classification LLM → labelling → brouillon auto-reply
2. **Agent conversationnel (chat)** : même Declarative ReAct Engine que [[neochat-architecture]], pour les interactions manuelles

**Différence clé avec NeoChat** : NeoMail est simplifié — pas d'historique de conversation, pas de suggestions, pas de résumé. Mais même engine, même prompt builder, même tool selector.

## Architecture en couches

```
┌──────────────────────────────────────────────────┐
│  Gmail Push Notifications (Pub/Sub)              │
│  Topic GCP → Cloud Run webhook                   │
├──────────────────────────────────────────────────┤
│  Webhook Pipeline (services/)                    │
│  decode → history API → classify → label → draft │
│  → voir [[neomail-webhook-pipeline]]             │
├──────────────────────────────────────────────────┤
│  Agent NeoMail (1 seul, déclaratif)              │
│  NEOMAIL_BLUEPRINT = AgentBlueprint              │
│  Même engine que NeoChat                         │
├──────────────────────────────────────────────────┤
│  Infrastructure partagée                         │
│  shared_utils (engine, prompts, tools, auth)     │
│  shared_tools (21 tools via config.yaml)         │
├──────────────────────────────────────────────────┤
│  BDD PostgreSQL (schema neomail)                 │
│  t_neomail_label, t_neomail_mail_processed       │
└──────────────────────────────────────────────────┘
```

## L'agent NeoMail — Blueprint déclaratif

```python
NEOMAIL_BLUEPRINT = AgentBlueprint(
    name="neomail",
    state_class=InterruptCapableState,  # alias pur, pas de state custom
    prompt_builder=neomail_adaptive_builder,
    tool_selector=select_tools_for_query,
    interrupt_handlers=[
        ActorSelectionHandler(),
        PendingRolesHandler(),
        MailPreviewHandler(),
        ComposeInterruptHandler(),
        DeleteConfirmHandler(),
    ],
    config=EngineConfig(
        max_iterations=5,
        enable_cache_first=True,
        enable_draft_context=True,
        enable_pending_action=True,
    ),
)
```

Utilise `create_react_graph(NEOMAIL_BLUEPRINT)` — même factory que NeoChat.

## Prompt Architecture

AdaptivePromptBuilderV2 avec 4 layers identiques à NeoChat :

| Layer | Contenu NeoMail |
|-------|----------------|
| L1 Core | "Je suis NeoMail, assistant mail professionnel" — 21 tools (17 Gmail + 4 Lojii) |
| L2 Task Rules | workflow (BROUILLON ONLY), generation, classification (5 types) |
| L3a Tools | Chargés dynamiquement via `ToolPromptLoader.get_tools_for_agent("neomail")` |
| L3b Templates | Par response_type, idem NeoChat |

**Classification types** : mail_read, mail_write, mail_search, contact_lookup, document_lookup.

## Tools disponibles (21)

**Gmail (17)** : recherche_mail, lire_mail, lire_thread, repondre_mail, creer_brouillon, modifier_brouillon, envoyer_mail, transferer_mail, archiver_mail, archiver_thread, supprimer_mail, supprimer_brouillon, lister_brouillons, marquer_lu, appliquer_label, lister_labels, creer_label

**Lojii (4)** : recherche_acteur, acteur_detail, recherche_document, analyze_drive_document

Sélection dynamique via `HybridToolSelector(agent_name="neomail", use_llm_rerank=False)` avec `min_score_ratio=0.90` et core tools en fallback.

## Règle BROUILLON ONLY — Défense en profondeur

La règle "pipeline auto = brouillon uniquement, JAMAIS envoyer_mail" est appliquée à **5 niveaux** :

1. **CLAUDE.md** (gotchas) — documentation développeur
2. **NEOMAIL_TASK_RULES["workflow"]** — `<must>` dans le system prompt
3. **Docstring webhook_handler.py** — rappel en tête de module
4. **Message agent dans `_create_auto_reply_draft()`** — instruction explicite
5. **Commentaire inline** — dernière ligne de défense

Si l'utilisateur demande explicitement d'envoyer : confirmation AVANT `envoyer_mail`.

## Différences NeoChat vs NeoMail

| Aspect | NeoChat | NeoMail |
|--------|---------|---------|
| Engine | Declarative ReAct | Declarative ReAct (identique) |
| Historique conversations | Oui (t_neochat_historique) | Non |
| Résumé de conversation | Oui (summarizer) | Non |
| Suggestions | Oui (generator) | Non |
| Webhook pipeline | Non | Oui (Gmail Pub/Sub) |
| Labels CRUD | Non | Oui (BDD + Gmail sync) |
| Classification | Via ReAct graph | Service LLM séparé |
| Quota | Implémenté | Passthrough V1 |
| Usage tracking | shared_utils.billing | Propre service → t_neomail_usage |
| Gmail Watch | Non | setup_watch/stop_watch |

## Schéma BDD (schema `neomail`)

| Table | Rôle |
|-------|------|
| `t_neomail_label` | Labels utilisateur (name, description, gmail_id, auto_reply, auto_reply_instructions, is_default, color) |
| `t_neomail_mail_processed` | Historique traitement (message_id, thread_id, step, label, confidence, draft_id, tokens, duration) |
| `t_neomail_usage` | Billing/usage tracking |

Labels système auto-insérés : `NeoMail/Traite`, `NeoMail/Echec`.

## API Endpoints

| Méthode | Path | Rôle |
|---------|------|------|
| POST | `/api/v1/webhook/gmail` | Réception Pub/Sub (background task) |
| POST | `/api/v1/agents/chat` | Agent conversationnel SSE |
| GET | `/api/v1/labels` | Liste labels |
| POST | `/api/v1/labels` | Créer label |
| PUT | `/api/v1/labels/{id}` | Modifier label |
| DELETE | `/api/v1/labels/{id}` | Supprimer label |
| GET | `/api/v1/mail/{id}/status` | Statut traitement d'un mail |
| GET | `/api/v1/admin/webhook-stats` | Stats webhook |
| GET | `/health` | Healthcheck |

Rate limits : 30/min chat, 120/min webhook.

## Fichiers clés

| Fichier | Rôle |
|---------|------|
| `agents/neomail/blueprint.py` | NEOMAIL_BLUEPRINT déclaratif |
| `agents/neomail/builder.py` | AdaptivePromptBuilderV2 config |
| `agents/neomail/prompts.py` | System prompt, task rules, classification |
| `agents/neomail/tools.py` | HybridToolSelector + CORE_TOOLS |
| `agents/neomail/graph.py` | create_neomail_graph() factory |
| `services/webhook_handler.py` | Pipeline auto complet |
| `services/classification.py` | Classificateur LLM |
| `services/gmail_watch.py` | Gmail Push Notifications setup |
| `api/v1/webhook.py` | Endpoint Pub/Sub |
| `api/v1/agents/chat.py` | Endpoint agent SSE |

## Liens

- [[neo_ia]]
- [[neochat-architecture]]
- [[neomail-webhook-pipeline]]
