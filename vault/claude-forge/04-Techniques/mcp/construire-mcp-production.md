---
titre: "Construire un serveur MCP de production — recipe TypeScript + Python"
resume: "Recipe de bout en bout pour un serveur MCP production-ready, TS et Python à parité : protocole (JSON-RPC, initialize, 3 primitives Tools/Resources/Prompts), transports (stdio local, Streamable HTTP remote), choix de SDK (FastMCP 3.0 GA / SDK officiel mcp côté Python, @modelcontextprotocol/sdk côté TS), puis maintenance/debug/observabilité (MCP Inspector, evals, OpenTelemetry, versioning). Patterns durables + liens doc canonique (versions épinglées juin 2026)."
aliases:
  - "construire un mcp"
  - "créer un serveur mcp"
  - "recipe mcp production"
  - "mcp typescript python"
  - "fastmcp serveur"
  - "mcp sdk officiel"
  - "structure d'un mcp"
  - "mcp inspector debug"
derniere-maj: 2026-06-09
auteur: claude
type: technique
sources:
  - "modelcontextprotocol.io/specification/2025-11-25 (transports, lifecycle)"
  - "gofastmcp.com + github.com/PrefectHQ/fastmcp (FastMCP 3.0 GA 18 fév 2026)"
  - "github.com/modelcontextprotocol/typescript-sdk (v1.29.0, mars 2026)"
  - "github.com/modelcontextprotocol/python-sdk"
  - "modelcontextprotocol.io/docs/tools/inspector (port 6274, --cli)"
  - "jlowin.dev/blog/fastmcp-3-whats-new (OpenTelemetry, versioning, granular auth)"
tags:
  - "#type/technique"
  - "#domaine/mcp"
  - "#domaine/claude-code"
  - "#domaine/typescript"
  - "#doctrine/2026"
---

# Construire un serveur MCP de production

> Recipe de bout en bout, **TypeScript et Python à parité**. Les snippets montrent le **pattern** durable (versions épinglées à juin 2026) ; pour les imports/signatures exacts, suivre le lien vers la doc SDK officielle — c'est elle la source de vérité versionnée, pas cette note.

---

## ÉTAPE 0 — Est-ce vraiment un MCP qu'il te faut ?

Avant tout : [[mcp-vs-skills-doctrine]]. MCP = accès données / actions atomiques cross-clients. Si c'est du how-to → Skill. Si c'est de l'exploration locale → Bash. Construire un MCP pour ce qu'un `Read` ferait = sur-engineering.

---

## ÉTAPE 1 — Le protocole (ce qu'un MCP EST)

- **JSON-RPC 2.0**, messages UTF-8. Protocole **stateful** aujourd'hui (négociation de capacités via `initialize`).
- Architecture : **Host → Clients (1:1) → Servers**.
- **3 primitives serveur** — un MCP « parfait » les traite à égalité, pas seulement les Tools :

| Primitive | Contrôlé par | Rôle | Analogie |
|---|---|---|---|
| **Tools** | le modèle | actions / effets de bord / calcul (`find_customer`, `send_email`) | fonctions appelables |
| **Resources** | l'application | données contextuelles en lecture (fichiers, schémas DB, blobs) exposées par URI | fichiers montés |
| **Prompts** | l'utilisateur | templates de prompt réutilisables avec arguments | slash-commands |

> Erreur fréquente : tout mettre en Tools. Un schéma de DB que le modèle doit lire = **Resource**, pas un tool `get_schema`. Un workflow guidé = **Prompt**.

- Lifecycle : `initialize` (négociation version + capacités) → `initialized` → échanges → fermeture.
- État du spec (juin 2026) : **courant = 2025-11-25** ; **RC = 2026-07-28** (MCP devient *stateless* au niveau protocole via 6 SEPs ; headers `Mcp-Method`/`Mcp-Name` pour routage par les gateways ; schemas → JSON Schema 2020-12).

---

## ÉTAPE 2 — Le transport (comment il parle)

Deux transports standard (spec 2025-11-25) :

| Transport | Usage | Mécanique |
|---|---|---|
| **stdio** | local, sous-process | le client lance le serveur en subprocess, JSON-RPC sur stdin/stdout, délimité par newlines. **Rien d'autre que du MCP valide sur stdout** ; logs sur stderr. Clients **SHOULD** supporter stdio quand c'est possible. |
| **Streamable HTTP** | remote | endpoint HTTP unique (POST + GET), ex. `https://example.com/mcp`. SSE optionnel pour le streaming serveur→client. |

**SSE pur (HTTP+SSE) = déprécié** depuis le spec 2025-03-26, remplacé par Streamable HTTP. Gardé seulement pour rétrocompat. Ne PAS bâtir un nouveau serveur en SSE.

Exigences normatives Streamable HTTP (verbatim spec) :
- Le serveur **MUST** valider le header `Origin` (anti DNS-rebinding) ; si invalide → **403**.
- En local, le serveur **SHOULD** bind sur `127.0.0.1`, pas `0.0.0.0`.
- Le serveur **SHOULD** implémenter une authentification (cf [[mcp-securite-oauth-remote]]).
- Session : `MCP-Session-Id` (UUID crypto, ASCII visible) assigné à l'init, renvoyé par le client sur chaque requête ; 404 = session expirée → le client réinitialise.
- Header `MCP-Protocol-Version: 2025-11-25` sur chaque requête HTTP après init.

---

## ÉTAPE 3 — Le SDK (avec quoi le coder)

### Python — défaut : FastMCP 3.0

**FastMCP 3.0 = GA (stable) depuis le 18 février 2026** (repo `PrefectHQ/fastmcp`, anciennement `jlowin/fastmcp` — imports/PyPI inchangés). C'est le défaut production : ~1M téléchargements/jour, ~70 % des serveurs MCP tous langages.

Relation avec le SDK officiel : **FastMCP 1.0 a été absorbé dans le SDK officiel `mcp` en 2024** (`from mcp.server.fastmcp import FastMCP`). FastMCP 2.x/3.x est le **standalone** au-dessus du protocole, avec le tooling production. Doctrine : **commencer par FastMCP** (meilleure DX), retomber sur le SDK officiel `mcp` si on a besoin du contrôle bas niveau (transports/sessions custom, conformité spec garantie).

Pattern minimal (vérifié gofastmcp.com) :

```python
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool          # sans parenthèses
def add(a: int, b: int) -> int:
    """Add two numbers"""   # docstring = description du tool
    return a + b

if __name__ == "__main__":
    mcp.run()              # stdio par défaut ; mcp.run(transport="http", ...) pour remote
```

Architecture FastMCP 3.0 (components / providers / transforms) : un serveur EST un provider → on peut **imbriquer des serveurs** ; les transforms sont du middleware (rename, namespace, filtre par version/tag) qui se composent. Utile pour la composition à grande échelle.

→ Imports/signatures exacts (annotations, resources, prompts, auth) : **gofastmcp.com** (source de vérité versionnée).

### TypeScript — SDK officiel

Package : **`@modelcontextprotocol/sdk`** (+ `zod`). Version prod = **v1.x** (v1.29.0, mars 2026) ; **v2 sur `main` est pre-alpha**, GA visée Q3 2026 ; v1 reçoit fixes + sécu ≥ 6 mois après v2.

```bash
npm install @modelcontextprotocol/sdk zod
```

Pattern (haut niveau) : instancier `McpServer({ name, version })`, enregistrer un tool avec son input schema (Zod), connecter un transport (`StdioServerTransport` en local, Streamable HTTP en remote — « recommended » pour remote dans le README).

> ⚠️ La signature exacte d'enregistrement de tool (`server.tool(...)` en v1 vs `registerTool(...)`/Standard Schema en v2) **diffère entre v1 et v2**. Ne pas mélanger. Pour le code production AUJOURD'HUI, suivre `docs/server.md` + `src/examples/server/simpleStreamableHttp.ts` du **repo v1.x** : github.com/modelcontextprotocol/typescript-sdk (source de vérité versionnée).

### Sur Cloudflare (remote managé)

3 approches (developers.cloudflare.com) : stateless `createMcpHandler()` ; stateful `McpAgent` + Durable Objects (état par session) ; raw `@modelcontextprotocol/sdk` (contrôle total). OAuth fourni par `workers-oauth-provider`. Détail sécu : [[mcp-securite-oauth-remote]].

---

## ÉTAPE 4 — Structure projet recommandée

```
mcp-server/
├── src/
│   ├── server.(py|ts)        # instanciation + enregistrement primitives
│   ├── tools/                # 1 fichier par tool ou par toolset, orienté objectif
│   ├── resources/            # exposition data en lecture (URI)
│   └── prompts/              # templates réutilisables
├── tests/                    # tests par tool + conformité protocole
├── README.md                 # schema documenté (sinon le modèle l'utilise mal)
└── (Python) pyproject.toml | (TS) package.json
```

Principes : 1 tool = 1 cas d'usage clair ; peu de tools orientés objectif (cf [[mcp-tool-design-scaling]]) ; jamais de credentials dans un fichier versionné.

---

## ÉTAPE 5 — Maintenance / debug / observabilité

### MCP Inspector (debug officiel Anthropic)

```bash
npx @modelcontextprotocol/inspector
# UI : http://localhost:6274
```

- UI browser-based (« Postman du MCP ») : panneaux **Tools / Resources / Prompts**, formulaires générés depuis le JSON Schema, validation protocole (flag les schemas invalides, champs requis manquants).
- Mode **`--cli`** scriptable (`tools/list`, `tools/call`, `--tool-name`, `--tool-arg`) → CI / GitHub Actions.
- **Limite** : agit comme **client**, pas comme proxy — montre le trafic Inspector↔serveur, PAS Claude↔serveur. Pour observer le trafic réel d'un client : proxy (`mcps-logger`, `emceepee`, MCP gateway).
- **Sécu** : un serveur MCP malveillant peut exécuter du code arbitraire sur la machine de l'Inspector. Container/VM pour tester des serveurs non-trusted, toujours à jour.

### Évaluation / testing

Stratégie cohérente = 2 couches : **conformité protocole** (le serveur parle MCP correctement) + **automation fonctionnelle** (il fait un travail utile). Ni l'une ni l'autre seule ne suffit. **MCPJam Inspector** ajoute un playground LLM + evals multi-LLM pour tracer la précision de sélection de tools dans le temps (utile en dialogue multi-tour).

### Observabilité

FastMCP 3.0 a une instrumentation **OpenTelemetry native** : chaque tool call / resource read / prompt render tracé avec attributs standardisés. À défaut : logger chaque appel (1 ligne JSONL : tool, durée, erreurs, args tronqués) — pattern forge-brain `usage_stats`, indispensable pour décider « garder / supprimer un tool » (cf [[mcp-vault-llm-design]]).

### Versioning

- Versionner le serveur (name + version au `initialize`).
- FastMCP 3.0 : versioning au niveau composant (`@tool(version="1.0")`) — exposer la version la plus haute tout en gardant les anciennes ; transform `VersionFilter` pour servir v1 et v2 du même code.

---

## ANTI-PATTERNS

- ❌ **Écrire sur stdout autre chose que du MCP** en transport stdio → casse le protocole (logs → stderr).
- ❌ **Bind `0.0.0.0` en local** sans validation Origin → DNS rebinding.
- ❌ **Nouveau serveur en SSE** → déprécié, mourra côté clients.
- ❌ **Mélanger API SDK TS v1 et v2** dans un même snippet → chimère qui ne tourne pas.
- ❌ **Présenter FastMCP comme « non-officiel »** → faux : 1.0 absorbé dans le SDK officiel, 3.0 GA est le défaut de fait.
- ❌ **Pas de README/schema documenté** → le modèle utilise mal le serveur.
- ❌ **Tester seulement avec l'Inspector** et croire voir le trafic Claude → l'Inspector est un client, pas un proxy.
- ❌ **Pas de logging d'usage** → impossible de décider quels tools garder.

---

## WIKILINKS

- [[MOC-MCP]] — point d'entrée
- [[mcp-vs-skills-doctrine]] — étape 0 : est-ce le bon outil
- [[mcp-tool-design-scaling]] — comment concevoir les tools (étape critique)
- [[mcp-securite-oauth-remote]] — sécuriser un serveur remote
- [[mcp-multi-client-claude-chatgpt-gemini]] — tester cross-client
- [[mcp-vault-llm-design]] — exemple complet : forge-brain
- [[architecture-cerveau-obsidian-mcp]] — archi cerveau de bout en bout
- [[reference-technique-stack-ia]] — MCP dans la stack IA globale
