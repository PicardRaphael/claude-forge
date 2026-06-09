---
titre: "Sécuriser un serveur MCP remote — OAuth 2.1, confused deputy, lethal trifecta"
resume: "Doctrine sécurité 2026 pour un MCP remote : serveur = OAuth 2.1 Resource Server, token passthrough INTERDIT par le spec, confused deputy problem, audience binding RFC 8707, PKCE S256, token exchange vs forwarding, lethal trifecta de Simon Willison, patterns Cloudflare (workers-oauth-provider, Access, portals). Liste mandatory/forbidden/should du spec."
aliases:
  - "sécurité mcp"
  - "mcp oauth 2.1"
  - "mcp resource server"
  - "confused deputy mcp"
  - "token passthrough mcp interdit"
  - "rfc 8707 resource indicators mcp"
  - "lethal trifecta"
  - "mcp remote sécurisé"
  - "cloudflare workers oauth provider"
derniere-maj: 2026-06-09
auteur: claude
type: technique
sources:
  - "modelcontextprotocol.io/specification/draft/basic/authorization"
  - "modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices"
  - "developers.cloudflare.com/agents/model-context-protocol/authorization"
  - "blog.cloudflare.com/enterprise-mcp (portals, scoped permissions)"
  - "simonwillison.net/2025/Jun/16/the-lethal-trifecta/"
  - "OWASP GenAI guide (short-lived tokens)"
tags:
  - "#type/technique"
  - "#domaine/mcp"
  - "#domaine/securite"
  - "#doctrine/2026"
---

# Sécuriser un serveur MCP remote

> Un MCP **local** (stdio) hérite de la confiance du process qui le lance. Un MCP **remote** (Streamable HTTP) est exposé sur le réseau → il DOIT être un Resource Server OAuth 2.1 correct. La majorité des failles MCP 2026 viennent d'OAuth mal fait, pas du protocole.

---

## Le modèle : MCP server = OAuth 2.1 Resource Server
> **Précisions spec (fetché modelcontextprotocol.io/specification/draft/basic/authorization, 2026-06-09) :**
> - L'autorisation est **OPTIONAL** pour MCP. Implémentations **HTTP** → **SHOULD** s'y conformer. Implémentations **stdio** → **SHOULD NOT** suivre ce flow et récupèrent les credentials **depuis l'environnement** (la sécu d'un MCP stdio = la sécu du process qui le lance).
> - Le MCP server **MUST** valider que les tokens ont été émis spécifiquement pour lui (audience, RFC 8707), et **MUST NOT accept or transit any other tokens** (= fondement normatif de l'interdiction de passthrough).
> - **DCR (Dynamic Client Registration, RFC 7591) est DÉPRÉCIÉ**, conservé pour rétrocompat avec les AS qui ne supportent pas **CIMD** (Client ID Metadata Documents). Les serveurs et clients **SHOULD** supporter CIMD ; client_id = URL HTTPS dont l'AS fetche les metadata. C'est la voie d'enregistrement moderne.
> - Le MCP server **MUST** implémenter Protected Resource Metadata (RFC 9728) ; validation `iss` côté client (RFC 9207) contre l'issuer enregistré.


Depuis la révision spec de juin 2025, la séparation est formalisée :
- **MCP server** = OAuth 2.1 **Resource Server** (accepte et valide des access tokens).
- **MCP client** = OAuth 2.1 **client** (fait les requêtes au nom du resource owner).
- **Authorization server** = entité dédiée qui parle à l'utilisateur et émet les tokens.

MCP utilise un **sous-ensemble d'OAuth 2.1**. Découverte : `WWW-Authenticate` → `/.well-known/oauth-protected-resource` → `/.well-known/oauth-authorization-server`.

---

## L'attaque centrale : le Confused Deputy

> Le MCP server devient le « député confus » : il a une autorisation légitime mais l'applique mal. Il suppose que l'authentification de l'utilisateur implique l'autorisation pour tous les clients — c'est ça, la vulnérabilité.

C'est une **escalade de privilèges** : le serveur est trompé pour utiliser SES propres privilèges (souvent plus élevés) afin d'exécuter des actions que l'utilisateur n'est pas autorisé à faire. Apparaît typiquement avec le **token passthrough** et avec les **proxies à client ID statique + DCR**.

Variante proxy/DCR (verbatim spec) : *« MCP proxy servers using static client IDs MUST obtain user consent for each dynamically registered client before forwarding to third-party authorization servers. »* Sauter ce consentement laisse un client DCR échanger un code d'autorisation contre un token émis sous l'identité d'un autre client.

---

## Le pattern INTERDIT : token passthrough

**Le spec interdit explicitement** de prendre le token que le client présente et de le forwarder tel quel à une API downstream (Slack, GitHub, Stripe).

Pourquoi c'est dangereux :
1. **Casse les pistes d'audit** — le downstream voit le token utilisateur, pas le MCP server ; impossible d'attribuer les actions.
2. **Contourne les politiques d'accès** propres au MCP server.
3. **Crée le confused deputy** si le downstream fait plus confiance à l'identité du MCP server qu'à celle de l'utilisateur.
4. **Si le MCP server est compromis**, l'attaquant récupère les tokens forwardés de TOUS les downstreams connectés.

> Le downstream fait confiance au token *parce qu'il est signé*, sans réaliser qu'il a été émis pour une autre ressource → audience binding cassé.

### Le pattern CORRECT : token exchange

1. Valider l'**audience** (`aud`) du token entrant à **chaque** requête : il DOIT inclure l'URI/identifiant de CE serveur. Rejeter même un token valide et non expiré s'il a été émis pour un autre service (anti cross-server replay).
2. Pour appeler un downstream : utiliser un token **séparé, scopé pour cette API**, stocké côté serveur (token exchange), JAMAIS le token du client.
3. Re-valider signature + audience + expiry à chaque invocation de tool — pas de cache « validé au début de session ».

---

## RFC 8707 — Resource Indicators (obligatoire)

Les clients MCP **MUST** implémenter les Resource Indicators (RFC 8707) : paramètre `resource=` sur chaque requête authorize ET token, qui lie chaque token à UN serveur MCP. Bloque le replay vers un autre serveur. Sans ça, partager un authorization server entre plusieurs MCP servers crée un chemin d'escalade cross-server (token bas-privilège présenté à un serveur haut-privilège).

---

## Checklist normative (spec MCP)

**MANDATORY**
- PKCE pour tous les clients (S256 si capable)
- Découverte via `WWW-Authenticate` → metadata
- Paramètre `resource=` sur chaque authorize + token (RFC 8707)
- Tokens audience-bound, validés localement à chaque requête

**FORBIDDEN**
- Implicit flow
- ROPC (password grant)
- plain-PKCE quand S256 est possible
- Bearer tokens dans les query strings d'URI
- **Token passthrough** vers les APIs upstream

**SHOULD**
- Dynamic Client Registration des deux côtés
- Rotation des refresh tokens pour clients publics
- Access tokens **courts** (minutes, pas heures — OWASP GenAI)
- Redirect-URI exact-match

---

## Surface d'attaque MCP (6 patterns)

1. Confused deputy via proxy (privilèges serveur au lieu de privilèges user)
2. Tool poisoning / rug pulls (un tool change de comportement après approbation)
3. Token passthrough abuse
4. Vol de credentials (env vars, logs)
5. SSRF pendant la découverte de metadata OAuth
6. Supply chain (serveur ou dépendances compromis)

---

## Lethal trifecta (Simon Willison)

Terme forgé par **Simon Willison** (simonwillison.net, 16 juin 2025 — **pas** Thariq, attribution corrigée dans le vault). Combinaison toxique :

1. **Private data** (données privées)
2. **Untrusted content** (input non-trusted : user, web, contenu de tiers)
3. **Exfiltration vector** (capacité d'exfiltration externe)

Les 3 ensemble = prompt injection exfiltration. **Couper au moins 1 des 3 axes.** Un MCP qui lit des données privées ET ingère du contenu web ET peut appeler une API sortante coche les 3 — d'où l'importance de la sanitization de contenu (cf le lockdown mode + content sanitization de GitHub, [[mcp-tool-design-scaling]]).

---

## Patterns Cloudflare (remote managé)

- **`workers-oauth-provider`** : librairie TS qui wrappe le Worker, le rend OAuth-2.1-spec-compliant en tant que provider. Le serveur est à la fois client OAuth de l'upstream et provider pour les clients MCP.
- 4 voies d'autorisation : Cloudflare **Access** comme provider SSO (le serveur n'implémente aucune logique d'auth) ; intégration directe GitHub/Google ; auth-as-a-service (Stytch, Auth0, WorkOS) ; ou tout gérer soi-même.
- **MCP server portals** (entreprise) : un portail unique révèle à l'employé tous les MCP servers internes/tiers qu'il est autorisé à utiliser → gouvernance + audit centralisés.
- **Scoped permissions** : plusieurs MCP servers focalisés, chacun à permissions étroites > un serveur sur-privilégié. Réduit le risque, facilite l'audit.
- Verdict sécu Cloudflare : les serveurs MCP **locaux** sont identifiés comme un risque entreprise (software non vérifié, non gérable par l'IT) → pousser vers du remote gouverné.

---

## ANTI-PATTERNS

- ❌ **Token passthrough** — interdit par le spec, crée le confused deputy.
- ❌ **Ne pas valider l'audience** (`aud`) à chaque requête.
- ❌ **Authorization server partagé sans `resource=`** — escalade cross-server.
- ❌ **Implicit flow / ROPC / plain-PKCE** — interdits.
- ❌ **Credentials dans `.mcp.json` versionné** (cf [[mcp-vs-skills-doctrine]] gotcha).
- ❌ **Faire confiance aux annotations readOnly d'un serveur non-trusted** — garanties = contrôles déterministes (cf [[mcp-tool-design-scaling]]).
- ❌ **Proxy DCR sans consentement par client** — escalade d'identité.
- ❌ **Tokens longue durée** — fenêtre d'exploitation large si vol.

---

## WIKILINKS

- [[MOC-MCP]] — point d'entrée
- [[mcp-tool-design-scaling]] — annotations ≠ garanties, sanitization anti-injection
- [[construire-mcp-production]] — où la sécu s'insère dans le transport remote
- [[mcp-multi-client-claude-chatgpt-gemini]] — OAuth supporté par chaque client
- [[mcp-vs-skills-doctrine]] — lethal trifecta y est aussi documenté
- [[mcp-vault-llm-design]] — défenses d'un MCP réel (path normalization, etc.)
