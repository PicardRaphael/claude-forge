# MCP Server Catalog — Detection & Recommendations

Catalogue structuré : signal codebase → MCP server recommandé.
Utiliser lors de l'analyse d'un projet pour recommander les bons serveurs MCP.

## Setup & Team Sharing

| Méthode | Scope | Partage |
|---------|-------|---------|
| `.mcp.json` (projet) | Ce dossier uniquement | Git = toute l'équipe |
| `~/.claude.json` (global) | Tous les projets | Personnel |

**Tip** : toujours checker `.mcp.json` dans git pour standardiser l'équipe.
**Debug** : `claude --mcp-debug` pour diagnostiquer.

## Documentation & Knowledge

| Signal | MCP Server | Install | Valeur |
|--------|-----------|---------|--------|
| React, Vue, Angular, Next.js | **context7** | `claude mcp add context7` | Docs live au lieu de training data |
| Express, FastAPI, Django | **context7** | idem | APIs framework à jour |
| Prisma, Drizzle, SQLAlchemy | **context7** | idem | ORM docs à jour |
| Stripe, Twilio, SendGrid | **context7** | idem | APIs tierces |
| AWS SDK, GCP, Azure | **context7** | idem | Cloud SDKs |
| LangChain, OpenAI SDK, Anthropic SDK | **context7** | idem | AI/ML libraries |

## Databases

| Signal | MCP Server | Détection |
|--------|-----------|-----------|
| `@supabase/supabase-js` dans deps | **Supabase MCP** | package.json |
| `pg`, `postgres`, raw SQL | **PostgreSQL MCP** | deps ou `*.sql` files |
| Neon serverless | **Neon MCP** | `@neondatabase/*` dans deps |
| Turso/libSQL | **Turso MCP** | `@libsql/*` dans deps |
| PL/pgSQL, fonctions PG | **MCP BDD custom** | `*.sql` avec `CREATE FUNCTION` |

## Browser & Frontend

| Signal | MCP Server | Détection |
|--------|-----------|-----------|
| Frontend avec tests UI | **Playwright MCP** | `@playwright/test` ou `playwright.config` |
| PDF depuis HTML, scraping | **Puppeteer MCP** | `puppeteer` dans deps |

## Version Control & DevOps

| Signal | MCP Server | Détection |
|--------|-----------|-----------|
| Repo GitHub | **GitHub MCP** | `git remote -v` → github.com |
| Repo GitLab | **GitLab MCP** | `git remote -v` → gitlab |
| Issues Linear | **Linear MCP** | Refs `ABC-123` dans code/commits |
| Issues Jira | **Jira MCP** | Refs `PROJ-123`, `.jira` config |
| Confluence/Atlassian | **Atlassian MCP** | Wiki refs, `atlassian-connect.json` |

## Cloud Infrastructure

| Signal | MCP Server | Détection |
|--------|-----------|-----------|
| `@aws-sdk/*` | **AWS MCP** | package.json |
| Cloudflare Workers/Pages/R2/D1 | **Cloudflare MCP** | `wrangler.toml` |
| Vercel deployment | **Vercel MCP** | `vercel.json` |
| Docker/Compose | **Docker MCP** | `docker-compose.yml`, `Dockerfile` |
| Kubernetes | **Kubernetes MCP** | `*.yaml` avec `apiVersion:`, `helm/` |

## Monitoring & Observability

| Signal | MCP Server | Détection |
|--------|-----------|-----------|
| `@sentry/*` | **Sentry MCP** | deps |
| Datadog APM | **Datadog MCP** | `dd-trace`, `datadog.yaml` |
| Langfuse traces | **Langfuse MCP** | `langfuse` dans deps ou config |

## Communication

| Signal | MCP Server | Détection |
|--------|-----------|-----------|
| Slack workspace | **Slack MCP** | Webhook URLs, `.slack` |
| Notion docs | **Notion MCP** | Refs Notion dans README |
| Google Chat webhooks | **GChat webhook** | URLs `chat.googleapis.com` |

## Obsidian & Knowledge

| Signal | MCP Server | Détection |
|--------|-----------|-----------|
| Vault Obsidian | **Obsidian MCP** (obsidian-brain) | `.obsidian/` directory |
| Memory cross-session | **Memory MCP** | Projet long-running |

## AI & Research

| Signal | MCP Server | Détection |
|--------|-----------|-----------|
| Research tasks | **Exa MCP** | Besoin de recherche web avancée |

## Neoteem-specific

| Projet | MCPs déjà configurés |
|--------|---------------------|
| ia_back | MCP BDD, Jira, Langfuse, GChat webhooks |
| neo_ia | MCP BDD, Langfuse |
| neoteem-brain | Obsidian MCP (3 profils) |
| bdd | MCP BDD (auto-référent) |

## Decision Framework

**Recommander un MCP quand :**
- Intégration service externe nécessaire (DB, API, cloud)
- Lookup docs pour librairies/SDKs (context7)
- Automatisation browser (Playwright)
- Intégration outils d'équipe (GitHub, Jira, Slack)
- Gestion infra cloud (AWS, Docker, K8s)

**NE PAS recommander quand :**
- Le besoin est couvert par un outil natif CC (Read, Grep, Bash)
- L'intégration est ponctuelle (un curl suffit)
- L'org bloque l'accès cloud (cas Neoteem → pas de GitHub MCP cloud)
