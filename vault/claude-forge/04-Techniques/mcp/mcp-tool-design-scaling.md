---
titre: "MCP tool design & scaling — peu de tools, le modèle ne se perd pas"
resume: "Comment concevoir les tools d'un MCP pour qu'un LLM les utilise bien : JSON Schema strict, annotations readOnly/destructive/idempotent/openWorld, descriptions complètes (3-4x moins d'échecs), et les 4 réponses 2026 au problème trop-de-tools : Code Execution with MCP (98,7% tokens en moins), Tool Search Tool, Dynamic Tool Discovery (GitHub), Codemode (Cloudflare search+execute)."
aliases:
  - "mcp tool design"
  - "design tools mcp"
  - "trop de tools mcp"
  - "mcp too many tools"
  - "code execution mcp"
  - "tool search tool"
  - "dynamic tool discovery"
  - "annotations mcp readonly destructive"
  - "le modèle se perd tools"
derniere-maj: 2026-06-09
auteur: claude
type: technique
sources:
  - "anthropic.com/engineering/code-execution-with-mcp (vérifié 2026-06-09)"
  - "anthropic.com/engineering/advanced-tool-use (Tool Search Tool)"
  - "blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations"
  - "github.com/github/github-mcp-server (toolsets, dynamic discovery, read-only)"
  - "blog.cloudflare.com/enterprise-mcp (Codemode, search+execute)"
  - "modelcontextprotocol.io/specification/2025-11-25"
tags:
  - "#type/technique"
  - "#domaine/mcp"
  - "#domaine/claude-code"
  - "#doctrine/2026"
---

# MCP tool design & scaling

> **Thèse centrale.** Le danger n°1 d'un MCP n'est pas le code : c'est d'exposer **trop de tools mal conçus**. Un LLM avec 50-100 tools chargés se perd, gaspille des dizaines de milliers de tokens, et choisit mal. La discipline : peu de tools orientés objectif, annotés et bien décrits ; et quand le volume est inévitable, **découverte dynamique** plutôt que chargement upfront.

---

## PARTIE 1 — Concevoir un bon tool

### Règle d'or : objectif, pas API

> « Don't treat your MCP server as a wrapper around your full API schema. Build tools optimized for specific user goals and reliable outcomes. **Fewer, well-designed tools often outperform many granular ones.** »
> — Cloudflare Agents docs (developers.cloudflare.com)

Mauvais : exposer `create_record`, `update_record`, `get_record`, `list_records`, `delete_record`, `search_records`… pour chaque entité (× N entités = explosion).
Bon : exposer `find_customer(query)` et `update_customer_status(id, status)` — ce que l'agent VEUT faire, pas ce que l'API PEUT faire.

### JSON Schema des inputs

- Input schema = objet JSON Schema avec `type: "object"` à la racine (contrainte conservée même dans le RC 2026-07-28).
- Le RC 2026-07-28 lève les schemas à **JSON Schema 2020-12 complet** (SEP-2106) : `oneOf`/`anyOf`/`allOf`, conditionnels, `$ref`. Les output schemas deviennent non contraints, `structuredContent` peut être n'importe quelle valeur JSON.
- **Gotcha cross-client** : les différences de validation JSON Schema cassent des tools d'un client à l'autre. Optional fields + combinaisons `$ref` qui passent dans Claude Desktop peuvent hard-fail dans Cursor/VS Code Copilot. Tester sur plusieurs clients (cf [[mcp-multi-client-claude-chatgpt-gemini]]).

### Annotations — vocabulaire de risque (spec 2025-03-26)

Interface `ToolAnnotations` (chaque champ est un **hint**, pas une garantie) :

| Annotation | Défaut | Sens si omis |
|---|---|---|
| `readOnlyHint` | `false` | suppose que le tool écrit |
| `destructiveHint` | `true` | suppose que le tool est destructif |
| `idempotentHint` | `false` | suppose que chaque appel a des effets additionnels |
| `openWorldHint` | `true` | suppose une interaction avec des systèmes externes |

Conséquence directe : **omettre les annotations = tout est traité comme destructif + open-world** → friction de confirmation maximale pour l'utilisateur. Claude et ChatGPT utilisent ces hints pour décider d'afficher un prompt de confirmation ou d'auto-approuver.

Discipline minimale :
- tool lecture seule → `readOnlyHint: true`, `destructiveHint: false`
- opération additive (append) → `destructiveHint: false`
- domaine fermé (pas d'appel externe) → `openWorldHint: false`

**Contradiction logique à éviter** : un tool ne peut pas être `readOnlyHint: true` ET `destructiveHint: true`. Si `readOnlyHint: true`, `destructiveHint`/`idempotentHint` ne s'appliquent pas.

> ⚠️ **Hints ≠ garanties.** Le spec est explicite : un client NE DOIT PAS faire confiance aux annotations d'un serveur non-trusted. Un serveur malveillant peut annoncer `readOnlyHint: true` et supprimer quand même. Les garanties de sécurité réelles restent des **contrôles déterministes côté client**, pas des hints. (cf [[mcp-securite-oauth-remote]])

Évolution (mars 2026) : 5 SEPs en discussion (trust/sensitivity, `unsafeOutputHint`, `secretHint`, `trustedHint`), Tool Annotations Interest Group avec Microsoft, OpenAI, AWS, Cloudflare, Anthropic.

### Descriptions — le levier le plus rentable

Une bonne description de tool a 3 parties : **action spécifique** + **contraintes des paramètres** + **format de sortie**. Éviter « gets data » / « performs search ».

> Mesure : les tools à description complète ont **3-4× moins d'invocations échouées** que les tools à description une ligne.
> — apigene.ai/blog/mcp-tools

En Python (FastMCP) : documenter chaque paramètre avec `Annotated` + `Field`, décrire le format de réponse dans le docstring, préserver des messages d'erreur détaillés pour que le LLM récupère intelligemment.

### Error handling

- Erreur **applicative** (le tool a tourné mais échoue métier) → résultat avec `isError: true` + message exploitable par le LLM. Le modèle voit l'erreur et peut s'adapter.
- Erreur **protocole** (tool inexistant, params invalides) → erreur JSON-RPC.
- Ne jamais avaler l'erreur en silence : « preserve detailed error messages so the LLM can recover intelligently ».

### Sécurité au niveau tool

> « Treat every LLM-generated string as untrusted input, because that is exactly what it is. For MCP servers, *the model asked for it* is not a security model. »

Valider les inputs contre le schema ET dans le handler ; access control si ressource sensible ; sanitize les outputs (surtout s'ils incorporent du contenu externe — vecteur prompt injection).

---

## PARTIE 2 — Le problème « trop de tools » et ses réponses 2026

### Le coût chiffré (Anthropic)

> Un setup à 5 serveurs = **58 tools ≈ 55 000 tokens** consommés *avant même* que la conversation commence. MCP classique charge ~15 400 tokens de définitions de tools par appel.
> — anthropic.com/engineering/code-execution-with-mcp

Deux inefficacités : (1) les définitions saturent le contexte upfront ; (2) les résultats intermédiaires repassent dans le contexte (ex. transcript de réunion 2h = +50 000 tokens qui transitent deux fois).

GitHub nomme le symptôme : **« tool confusion »** — le modèle se perd dans le nombre.

### Réponse A — Code Execution with MCP (Anthropic)

Présenter les serveurs MCP comme une **API de code** (filesystem de fichiers TypeScript) plutôt que comme des définitions de tools directes :

```
servers/google-drive/getDocument.ts
servers/salesforce/updateRecord.ts
```

L'agent **explore le filesystem** pour découvrir les tools à la demande, ne lit que les fichiers pertinents, et appelle `callMCPTool()` depuis du code généré.

Gains mesurés :
- **150 000 → 2 000 tokens = -98,7 %** (exemple Drive→Salesforce)
- **-78,5 %** input tokens sur l'éval (165K vs 771K)

Bénéfices annexes : filtrage in-environment (10 000 lignes → 5 lignes via `.filter()` avant que ça atteigne le modèle) ; les résultats intermédiaires restent dans l'environnement d'exécution (privacy, PII tokenisable en `[EMAIL_1]`) ; persistance d'état et de « skills » réutilisables.

> Réserve : adapté aux tools « API wrappers » produisant de la donnée structurée ; surcoût opérationnel non justifié pour les petits déploiements à peu de tools.

### Réponse B — Tool Search Tool (Claude Developer Platform)

Fournir TOUTES les définitions à l'API mais marquer les tools `defer_loading: true` : ils ne sont pas chargés dans le contexte initial. Claude ne voit que le Tool Search Tool + les tools critiques (`defer_loading: false`), puis recherche dynamiquement les tools pertinents.

- **-85 %** d'usage tokens
- Précision MCP : Opus 4 49 % → 74 % ; **Opus 4.5 79,5 % → 88,1 %** avec Tool Search activé.

### Réponse C — Dynamic Tool Discovery côté serveur (GitHub MCP)

Le serveur MCP officiel GitHub illustre le pattern composable :
- **Toolsets** (`--toolsets`) : groupes de fonctionnalités activables (`context`, `issues`, `pull_requests`, `repos`, `users` par défaut). Réduit le contexte et aide le choix.
- **Tools individuels** (`X-MCP-Tools` header) : granularité fine (n'activer que `get_file_contents` + `pull_request_read` au lieu des 27 tools de `repos`+`pull_requests`).
- **Dynamic Toolset Discovery** (`--dynamic-toolsets` / `GITHUB_DYNAMIC_TOOLSETS=1`) : le LLM découvre et active des sets de tools seulement quand il en a besoin.
- **Read-only mode** (`GITHUB_READ_ONLY=1`) : filtre de sécurité **strict** qui désactive tout tool non-read-only, même explicitement demandé — prioritaire sur toute autre config.
- **Lockdown mode** + content sanitization par défaut : anti-prompt-injection sur contenu de contributeurs non-trusted.

Proposition spec **SEP-1821** : param `query` sur `tools/list` (le serveur interprète une requête texte : catégorie, tag, use case) au lieu de tout retourner.

### Réponse D — Codemode (Cloudflare)

Le **Cloudflare API MCP server** expose **2 500+ endpoints** (DNS, Workers, R2, Zero Trust…) via **2 tools seulement** : `search()` et `execute()`. Le modèle écrit du JavaScript contre une représentation typée de l'OpenAPI spec. C'est l'incarnation extrême de « peu de tools » + « code execution » : la surface d'API est immense, la surface de tools est minuscule.

### Arbre de décision scaling

```
Combien de tools logiques ?
├─ ≤ ~15 → charge-les directement, annotés + bien décrits. Stop.
├─ 15-50 → groupe en toolsets activables (pattern GitHub) ; read-only mode si pertinent.
└─ 50+ ou API entière → découverte dynamique :
     ├─ tu contrôles le runtime / sandbox → Code Execution (filesystem) ou Codemode (search/execute)
     └─ via l'API Claude → Tool Search Tool (defer_loading)
```

---

## ANTI-PATTERNS

- ❌ **Wrapper l'API entière** en tools 1:1 — origine de la tool confusion.
- ❌ **50-100 tools chargés upfront** — « le modèle se perd » (Thariq), 55k tokens avant le premier message.
- ❌ **Annotations omises** — tout devient destructif + open-world, friction max.
- ❌ **`readOnlyHint: true` + `destructiveHint: true`** — contradiction logique.
- ❌ **Faire confiance aux annotations d'un serveur non-trusted** — hints ≠ garanties.
- ❌ **Description « gets data »** — 3-4× plus d'échecs qu'une description complète.
- ❌ **Avaler les erreurs** — le LLM ne peut pas récupérer sans message.
- ❌ **Code Execution sur un MCP à 5 tools** — surcoût opérationnel non justifié.

---

## WIKILINKS

- [[MOC-MCP]] — point d'entrée du dossier
- [[mcp-vs-skills-doctrine]] — quand un MCP est le bon outil (vs Skill/Bash)
- [[construire-mcp-production]] — la recipe d'implémentation TS/Python
- [[mcp-securite-oauth-remote]] — les garanties déterministes derrière les hints
- [[mcp-multi-client-claude-chatgpt-gemini]] — différences de validation cross-client
- [[mcp-vault-llm-design]] — application : 21 tools forge-brain orientés objectif
- [[Context Engineering]] — le scaling tools est un cas de context engineering
