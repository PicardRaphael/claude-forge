---
titre: "NeoMail Webhook Pipeline — Gmail Pub/Sub → Classification → Auto-Reply"
resume: "Pipeline automatique de traitement mail : réception Pub/Sub GCP, décodage History API, classification LLM Gemini, labelling Gmail sync, brouillon auto-reply via agent ReAct, défense en profondeur BROUILLON ONLY"
aliases:
  - "neomail webhook pipeline"
  - "neomail pipeline"
  - "gmail webhook pipeline"
  - "neomail pub/sub"
  - "pipeline mail automatique"
  - "classification mail neomail"
type: context
status: active
derniere-maj: 2026-05-11
auteur: claude
tags:
  - "#type/context"
  - "#type/technique"
  - "#projet/neo-ia"
  - "#domaine/agents"
---

## Concept

Le webhook pipeline est le mode principal de NeoMail : traitement automatique des mails entrants sans intervention humaine. Gmail pousse une notification Pub/Sub, NeoMail classifie, labelle et peut créer un brouillon de réponse.

## Pipeline complet (10 étapes)

```
Gmail reçoit un mail
    │
    ▼
1. Gmail Push Notification
   Gmail API → Pub/Sub GCP → Cloud Run
   Topic configuré via gmail_watch.py (setup_watch)
    │
    ▼
2. POST /api/v1/webhook/gmail
   Sécurité IAM GCP (service account roles/run.invoker)
   Retourne 200 IMMEDIATEMENT, traite en background
   Rate limit: 120/min (slowapi)
    │
    ▼
3. Décodage payload
   Base64 → JSON → { emailAddress, historyId }
    │
    ▼
4. Gmail History API
   users().history().list(historyTypes=["messageAdded"])
   Filtre: uniquement mails avec label INBOX
    │
    ▼
5. Déduplication
   Check t_neomail_mail_processed (message_id déjà traité ?)
   Si oui → skip
    │
    ▼
6. Fetch message complet
   users().messages().get(format="full")
   Extraction: from, to, subject, body (text/plain ou text/html)
    │
    ▼
7. Classification LLM
   get_llm_for_task(LLMTaskType.EXTRACTION) = Gemini 2.5 Flash, temp 0
   Prompt dynamique basé sur les labels actifs en BDD
   Output: { label_name, confidence }
   Fallback: ClassificationResult(label_name="DEFAULT", is_default=True)
    │
    ▼
8. Résolution label + sync Gmail
   Lookup label en BDD (t_neomail_label)
   Si label_name="DEFAULT" → utiliser le label avec is_default=True
   Créer le label dans Gmail si gmail_id absent
   Appliquer le label sur le message Gmail
    │
    ▼
9. Enregistrement BDD
   Insert t_neomail_mail_processed (step="classified")
   Stocke: label_id, confidence, agent_reasoning, tokens, duration
    │
    ▼
10. Auto-reply (optionnel)
    Si label.auto_reply=True :
    → Invocation agent NeoMail via create_neomail_graph()
    → Message forcé: "CREE UN BROUILLON UNIQUEMENT"
    → Agent utilise creer_brouillon (JAMAIS envoyer_mail)
    → Update BDD: step="draft_created", draft_id stocké
    
    Si erreur:
    → Label NeoMail/Echec appliqué
    → failure_reason + error_type enregistrés
    
    Dans tous les cas:
    → Label NeoMail/Traite appliqué (mail traité)
```

## Classification — Prompt dynamique

Le classificateur n'est PAS dans le ReAct graph — c'est un **appel LLM direct** (`services/classification.py`).

Le prompt est construit dynamiquement à partir des labels configurés en BDD :
```
Pour chaque label actif (is_active=True, is_system=False):
  - nom du label
  - description du label
  
"Classifie ce mail dans un des labels ci-dessus.
 Réponds en JSON: {label_name, confidence}"
```

Cela signifie que les utilisateurs contrôlent les catégories de classification via la UI (CRUD labels), sans toucher au code.

## Sécurité webhook

- **Pas d'auth applicative** — la sécurité repose sur IAM GCP :
  - Cloud Run "Require authentication"
  - Service account avec `roles/run.invoker`
  - Seul le service Pub/Sub GCP peut appeler l'endpoint
- **Traitement async** — `asyncio.create_task()` en background, HTTP 200 immédiat
- **Déduplication** — check BDD avant traitement (idempotent)

## Gmail Watch (Pub/Sub setup)

`services/gmail_watch.py` :
- `setup_watch(user_email, topic_name)` — utilise Domain-Wide Delegation (DWD) pour impersonate l'utilisateur, abonne INBOX au topic Pub/Sub
- `stop_watch(user_email)` — désabonne
- Le watch expire après 7 jours, renouvellement nécessaire (cron externe)

## Labels système

| Label | Rôle |
|-------|------|
| `NeoMail/Traite` | Appliqué après traitement réussi |
| `NeoMail/Echec` | Appliqué si erreur dans le pipeline |

Auto-insérés dans la migration SQL initiale.

## Exceptions (hiérarchie)

```
WebhookError
├── GmailAPIError      — erreur API Gmail (fetch, label, watch)
├── ClassificationError — erreur classification LLM
└── DraftCreationError  — erreur création brouillon auto-reply
```

## Liens

- [[neomail-architecture]]
- [[neochat-react-engine]]
- [[neochat-tool-rag]]
