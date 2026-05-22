---
titre: "MCP vs CLI vs Skills — Quand utiliser quoi"
resume: "Comparaison MCP vs CLI vs Skills pour Claude Code — matrice de decision 5 criteres, benchmarks tokens et fiabilite, consensus skills-first de Willison et Boris"
aliases:
  - "MCP vs CLI"
  - "skills vs MCP"
  - "CLI vs MCP comparison"
  - "quand utiliser MCP"
  - "MCP ou CLI"
domaine: claude-code
type: technique
derniere-maj: 2026-05-14
auteur: claude
sources:
  - "https://simonwillison.net/2025/Oct/16/claude-skills/"
  - "https://systemprompt.io/guides/mcp-vs-cli-tools"
  - "https://www.mindstudio.ai/blog/mcp-vs-cli-agentic-workflows-token-overhead-reliability"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/mcp"
---

## Position des leaders

### Simon Willison : "Skills > MCP"

> "Almost everything I might achieve with an MCP can be handled by a CLI tool instead."

- Les skills ne coutent que quelques dizaines de tokens au demarrage (metadata seule)
- Le MCP GitHub officiel consomme des dizaines de milliers de tokens de contexte a lui seul
- Les skills "outsource the hard parts to the LLM harness and the associated computer environment"
- Prediction : "I expect we'll see a Cambrian explosion in Skills which will make this year's MCP rush look pedestrian"

### Boris Cherny : "Agentic search > RAG"

> "Early versions of Claude Code used RAG + a local vector db, but we found that agentic search generally works better. It is also simpler."

Glob + grep pilotes par le modele > RAG indexe. Pas d'index a construire, pas de staleness, pas de fuite de donnees.

## Benchmarks (MindStudio, systemprompt.io)

| Critere | CLI | MCP |
|---------|-----|-----|
| **Cout tokens** | 4-32x moins cher | 35x plus sur taches identiques |
| **Fiabilite** | 100% quelle que soit la complexite | 100% facile, 72% quand complexite monte |
| **Latence par appel** | ~200ms (Bash) | ~5ms (connection pool, appels repetes) |
| **Economie contexte** | — | Sur 20+ queries DB, ~100K tokens economises |

## Matrice de decision (5 criteres)

Score 0 = CLI, 1 = MCP. Total 0-1 = CLI, 4-5 = MCP.

| Critere | CLI | MCP |
|---------|-----|-----|
| **Frequence** | One-off / rare | Daily / continu |
| **Audience** | Usage personnel | Equipe / organisation |
| **State** | Stateless (lecture fichier, git) | Stateful (DB pools, sessions API, auth cache) |
| **Complexite output** | Texte simple | JSON structure / tables |
| **Distribution** | Outils locaux | Shared / marketplace |

## Recommandation

1. **Commencer par CLI** — toujours
2. **Promouvoir en MCP** quand : 10+ executions, acces equipe necessaire, auth persistante, output > 50 lignes regulierement
3. **Garder en CLI** : operations fichiers, git, gestion de process
4. **Preferer Skills** quand le workflow est repetable et ne necessite pas de connexion persistante

## Skills vs MCP — quand choisir

| Besoin | Skills | MCP |
|--------|--------|-----|
| Workflow repetable | Oui — chemin par defaut | Non |
| Connexion API persistante | Non | Oui |
| Distribution equipe | Plugin marketplace | Plugin ou serveur partage |
| Cout contexte | Minimal (~100 tokens metadata) | Eleve (milliers de tokens) |
| Fiabilite | Deterministe (fichiers) | Depend du serveur |
| Donnees temps reel | Via CLI dans la skill | Natif |

## Liens

- [[comment-creer-skill]] — Format et best practices skills
- [[comment-creer-hook]] — Hooks comme alternative a MCP pour enforcement
- [[harness-engineering]] — Skills et MCP dans l'architecture harness
- [[Simon Willison]] — Position "skills > MCP" detaillee
- [[Boris Cherny]] — "Agentic search > RAG"
