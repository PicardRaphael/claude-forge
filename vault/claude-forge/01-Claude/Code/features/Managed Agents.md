---
titre: "Managed Agents — Beta publique"
resume: "Agents cloud Anthropic $0.08/session-hour + tokens, sandbox, checkpointing, Notion/Rakuten/Asana"
aliases:
  - "managed agents"
  - "agents cloud anthropic"
  - "managed agents beta"
  - "agents geres"
  - "anthropic cloud agents"
type: feature
derniere-maj: 2026-05-24
auteur: claude
sources:
  - "https://siliconangle.com/2026/04/08/anthropic-launches-claude-managed-agents-speed-ai-agent-development/"
tags:
  - "#type/feature"
  - "#domaine/industrie"
---

## Contexte

Beta publique depuis le 8 avril 2026. Agents cloud gérés par Anthropic.

## Découvertes

- **$0.08/session-hour** + tokens
- Sandbox, checkpointing, credentials, tracing
- Early adopters : Notion, Rakuten, Asana, Sentry

## Update mai 2026 — Code with Claude

3 nouvelles capacites en public beta (annoncees 6 mai) :
- **Multi-agent orchestration** — flottes d'agents coordonnes
- **Outcomes** — definition de criteres de succes mesurables
- **Dreaming** (research preview) — auto-review des sessions passees overnight, cree des memories automatiquement

## Liens

- [[MOC-Claude-Code]]
- [[Cowork GA]]
- [[Code with Claude Conference]]
- [[MOC-Industrie]]


## Update London (19 mai 2026)

### Nouvelles features
- **[[Self-Hosted Sandboxes]]** (public beta) — exécution dans l'infra client (Cloudflare, Modal, Vercel, Daytona, custom)
- **[[MCP Tunnels]]** (research preview) — accès sécurisé aux MCP servers privés via tunnel outbound

### Webhooks (public beta, 7 mai)

8 event types :
- **Status lifecycle** : `session.status_run_started`, `_idled`, `_rescheduled`, `_terminated`
- **Thread lifecycle** : `session.thread_created`, `_idled`, `_terminated`
- **Outcomes** : `session.outcome_evaluation_ended`
- **Vault** : `vault_credential.refresh_failed`

Delivery at-least-once (idempotent sur `id`), pas d'ordering garanti. `X-Webhook-Signature` avec replay protection 5 min. Thin payloads — full state via API callback.

### Outcomes — détails techniques

| Paramètre | Valeur |
|-----------|--------|
| `max_iterations` default | 3 |
| `max_iterations` maximum | 20 |
| Events | `span.outcome_evaluation_start`, `_ongoing`, `_end` |
| Résultats possibles | `satisfied`, `needs_revision`, `max_iterations_reached`, `failed`, `interrupted` |
| Performance | +10 points taux succès vs standard prompting (benchmark interne) |

Un rubric vague produit des évaluations bruitées — la qualité du rubric est critique.

### Advisor Strategy

Implémentation simple : update du `tools` array dans Messages API. Architecture qui split execution (Sonnet/Haiku) et advising (Opus). EVE Legal : "frontier model quality at 5x lower cost".

### Clients mentionnés keynote
- **Notion** — agents long-running dans le produit via Managed Agents
- **Shopify** — CC across engineering + non-engineering (design, product, data science)
- **Mercado Libre** — 23K engineers, 500K+ PRs reviewées, 9000+ apps modernisées, objectif 90% autonomous coding Q3 2026 ⚠️ _Chiffres précis à confirmer livestream CwC London 19 mai 2026 — non trouvés dans sources externes accessibles (audit 23 mai 2026)._
