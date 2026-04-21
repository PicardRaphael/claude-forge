# MCP Feedback Neoteem — Spec de dev

## Contexte

On a besoin d'un serveur MCP (Model Context Protocol) qui permet a Claude (Cowork + Claude Code) d'acceder aux feedbacks utilisateurs stockes en BDD. Ce MCP est la brique d'entree du workflow de triage automatique des feedbacks.

**Stack :** Python + FastMCP
**BDD :** PostgreSQL Neoteem (table existante, schema ci-dessous)
**Consommateurs :** Claude Cowork (analyse automatique) + Claude Code (dev assiste)

---

## Table source

Table : `public.t_neochat_feedback`

```sql
feedback_id          UUID        PK, auto-genere
feedback_positif_y   BOOLEAN     -- true = positif (score >= 0.5 ou rating >= 3.0)
feedback_messages    JSONB       -- contexte riche :
  -- {
  --   "user": "question posee",
  --   "assistant": "reponse de l'agent",
  --   "agent": "support",           -- quel agent a repondu
  --   "score_type": "thumbs",       -- "thumbs" ou "rating"
  --   "raw_score": 1.0              -- 0/1 thumbs, 0-5 rating
  -- }
feedback_clientid    VARCHAR     -- ID client (vient du JWT)
feedback_acteurid    UUID        -- ref public.T_ACTEUR.acteur_id
feedback_commentaire TEXT        -- commentaire libre utilisateur (max 1000 chars, nullable)
feedback_threadid    UUID        -- = SESSION Langfuse = thread_id conversation entiere
feedback_trace_id    VARCHAR(32) -- = TRACE Langfuse = echange specifique (nullable)
feedback_type        VARCHAR     -- "positive" ou "negative" (auto via trigger trg_sync_feedback)
feedback_exchange    JSONB       -- paire question/reponse epuree (nullable)
  -- { "question": "...", "answer": "..." }
feedback_a_traite    BOOLEAN     -- true = a analyser par l'IA, false = deja traite
feedback_date_creation TIMESTAMPTZ -- DEFAULT now()
feedback_date_modif    TIMESTAMPTZ -- DEFAULT now()
```

---

## Tools MCP a implementer

### 1. `get_pending_feedbacks`

Recupere les feedbacks en attente d'analyse.

**Parametres :**
| Param | Type | Requis | Description |
|-------|------|--------|-------------|
| limit | int | non | Nombre max de resultats (default 50) |
| client_id | string | non | Filtrer par client |
| type | string | non | "positive" ou "negative" |

**Logique :**
```sql
SELECT * FROM public.t_neochat_feedback
WHERE feedback_a_traite = true
ORDER BY feedback_date_creation ASC
LIMIT :limit
```

**Retour :** liste de feedbacks (tous les champs)

---

### 2. `get_feedback_by_id`

Recupere un feedback specifique par son ID.

**Parametres :**
| Param | Type | Requis | Description |
|-------|------|--------|-------------|
| feedback_id | string (UUID) | oui | ID du feedback |

**Retour :** le feedback complet ou erreur 404

---

### 3. `get_session_feedbacks`

Recupere tous les feedbacks d'une session (conversation). Utile quand l'IA a besoin de remonter le contexte complet.

**Parametres :**
| Param | Type | Requis | Description |
|-------|------|--------|-------------|
| thread_id | string (UUID) | oui | Le feedback_threadid (= session Langfuse) |

**Logique :**
```sql
SELECT * FROM public.t_neochat_feedback
WHERE feedback_threadid = :thread_id
ORDER BY feedback_date_creation ASC
```

**Retour :** liste de feedbacks de la session

---

### 4. `mark_feedback_processed`

Marque un ou plusieurs feedbacks comme traites apres analyse.

**Parametres :**
| Param | Type | Requis | Description |
|-------|------|--------|-------------|
| feedback_ids | list[string] | oui | Liste d'UUIDs a marquer |

**Logique :**
```sql
UPDATE public.t_neochat_feedback
SET feedback_a_traite = false, feedback_date_modif = now()
WHERE feedback_id = ANY(:feedback_ids)
```

**Retour :** nombre de feedbacks mis a jour

---

### 5. `get_feedback_stats`

Stats rapides pour le dashboard / monitoring (optionnel mais utile).

**Parametres :**
| Param | Type | Requis | Description |
|-------|------|--------|-------------|
| client_id | string | non | Filtrer par client |
| since | string (ISO date) | non | Depuis quand (default 7 jours) |

**Retour :**
```json
{
  "total": 42,
  "pending": 5,
  "positive": 30,
  "negative": 12,
  "by_agent": { "support": 20, "neodoc": 15, "neomail": 7 }
}
```

---

## Stack technique

### Dependances

```
fastmcp>=2.0
asyncpg          # ou psycopg[binary] si preferez sync
python-dotenv    # pour les credentials BDD
```

### Structure du projet

```
mcp-feedback-neoteem/
  pyproject.toml
  .env.example        # DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
  src/
    server.py          # point d'entree FastMCP
    db.py              # connexion pool PostgreSQL
    tools/
      feedbacks.py     # les 5 tools ci-dessus
```

### Exemple de code (server.py)

```python
from fastmcp import FastMCP

mcp = FastMCP(
    name="feedback-neoteem",
    instructions="Acces aux feedbacks utilisateurs Neoteem. "
                 "Utilise get_pending_feedbacks pour recuperer les feedbacks a analyser, "
                 "puis mark_feedback_processed une fois le ticket Jira cree."
)

# Importer les tools
from tools.feedbacks import register_tools
register_tools(mcp)

if __name__ == "__main__":
    mcp.run()
```

### Exemple de tool (feedbacks.py)

```python
from fastmcp import Context

def register_tools(mcp):

    @mcp.tool()
    async def get_pending_feedbacks(
        limit: int = 50,
        client_id: str | None = None,
        type: str | None = None,
        ctx: Context = None
    ) -> list[dict]:
        """Recupere les feedbacks en attente d'analyse par l'IA (feedback_a_traite = true)."""
        pool = await get_db_pool()
        query = "SELECT * FROM public.t_neochat_feedback WHERE feedback_a_traite = true"
        params = []
        if client_id:
            query += " AND feedback_clientid = $" + str(len(params) + 1)
            params.append(client_id)
        if type:
            query += " AND feedback_type = $" + str(len(params) + 1)
            params.append(type)
        query += " ORDER BY feedback_date_creation ASC LIMIT $" + str(len(params) + 1)
        params.append(limit)
        rows = await pool.fetch(query, *params)
        return [dict(r) for r in rows]

    # ... meme pattern pour les autres tools
```

### Configuration MCP cote Claude

Une fois le serveur pret, l'ajouter dans les settings Claude (Cowork ou Code) :

Le MCP gere sa propre connexion BDD en interne (`.env` du projet MCP). Cowork/Claude Code ne voit rien de la config DB — il appelle juste les tools.

L'installation cote Cowork se fait via l'interface : Customize → MCP Servers → ajouter le serveur.

---

## Contraintes

- **Read-heavy** : le MCP est surtout en lecture. La seule ecriture est `mark_feedback_processed`.
- **Pas de suppression** : on ne supprime jamais un feedback.
- **Pas de creation** : les feedbacks sont crees par l'app (NeoChat/NeoDoc/NeoMail), pas par le MCP.
- **Securite** : credentials BDD en variables d'env, jamais en dur. Connexion read-only sauf pour le UPDATE de `feedback_a_traite`.
- **Performance** : pool de connexions (asyncpg pool), pas de connexion par requete.

---

## Test rapide

Une fois le MCP lance, tester avec :

```bash
# Lister les feedbacks en attente
echo '{"method":"tools/call","params":{"name":"get_pending_feedbacks","arguments":{"limit":5}}}' | python -m src.server

# Ou via Claude : "Recupere les feedbacks en attente d'analyse"
```
