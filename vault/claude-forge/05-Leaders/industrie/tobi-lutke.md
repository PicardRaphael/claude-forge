---
titre: "Tobi Lütke — CEO Shopify, créateur de qmd (vault LLM search)"
resume: "CEO Shopify. Créateur de qmd (github.com/tobi/qmd) : moteur de recherche local pour markdown — BM25 + vector + LLM re-ranking, CLI ET MCP server simultanément. Recommandé par Karpathy dans le LLM Wiki Gist (avril 2026) mais c'est bien Tobi qui l'a créé"
aliases:
  - "Tobi Lütke"
  - "Tobi Lutke"
  - "tobi"
  - "CEO Shopify"
  - "qmd"
  - "qmd Tobi"
  - "Shopify CEO"
derniere-maj: 2026-05-22
auteur: claude
type: leader
sources:
  - "https://github.com/tobi/qmd"
  - "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
tags:
  - "#type/leader"
  - "#domaine/industrie"
  - "#domaine/agents"
  - "#leader/industrie"
---

# Tobi Lütke — CEO Shopify, créateur de qmd

## QUI

**Tobi Lütke** — Fondateur et CEO de **Shopify** depuis 2006 (~10 000 employés, $700B+ GMV cumulé). Allemand, vit au Canada. Connu pour son style "founder-CTO" (encore activement développeur) et son endorsement précoce de Claude Code en entreprise (memo interne Shopify *"AI is the new floor"*, mars 2025).

GitHub : `tobi`. Twitter : `@tobi`.

Profil : couche 3 (secondaire) — pas Anthropic, pas équipe modèle. Mais **leader de l'industrie** côté adoption Claude Code en entreprise, et **outilleur** (qmd).

## POURQUOI EST PERTINENT

### 1. CORRECTION D'ATTRIBUTION CRITIQUE

**Tobi est le créateur de `qmd`, PAS Karpathy.** Karpathy l'a simplement **recommandé** dans son [Gist LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) du 4 avril 2026 :

> "qmd is a good option: it's a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device."

Plusieurs notes anciennes du vault attribuaient qmd à Karpathy — c'est faux. Repo officiel : https://github.com/tobi/qmd. Auteur GitHub : `tobi` = Tobi Lütke.

### 2. Pourquoi qmd est important pour le vault forge-brain

`qmd` est le **canonical example** d'un outil de search vault qui sert **à la fois** :

- **CLI** (`qmd search "..."`) — pour agents bash-centric
- **MCP server** (`qmd mcp`) — pour agents tool-centric

C'est exactement la doctrine Karpathy / Thariq sur CLI vs MCP : **les deux à la fois** (cf [[mcp-vs-skills-doctrine]]).

Tobi a anticipé d'un an la doctrine officielle Anthropic ("MCP connects data, Skills teach what to do") en livrant l'outil **avant** que le débat ait lieu.

### 3. Comparaison qmd vs MCP forge-brain

| Dimension | qmd (Tobi) | MCP forge-brain (forge) |
|-----------|------------|-------------------------|
| Search | BM25 + vector + LLM re-ranker | FTS5 SQLite + fallback 4 strat + BM25 10/1/8 |
| Interface | **CLI + MCP** | MCP only |
| Local-first | Oui, on-device | Oui, port 8091 |
| Re-ranking | LLM re-ranker | Pas de re-ranker, BM25 pondéré opinionated |
| Frontmatter | Pas exigé | 1774 aliases indexés |
| Watcher | (à vérifier) | content-hash short-circuit |

Forge a fait un choix opinionated (MCP only, FTS5 vs vector) — qmd reste la **référence externe** à connaître si on veut un fallback CLI.

## CONTRIBUTIONS CLÉS

### 1. qmd — moteur de recherche markdown local

- Repo : https://github.com/tobi/qmd
- Architecture : BM25 + vector embeddings + LLM re-ranking (3 étages)
- Interfaces : CLI + MCP server (les deux)
- Cible : vaults Obsidian / dossiers de markdowns à l'échelle 100-1000+ notes
- Local-first : pas de cloud, pas d'index distant

### 2. Memo Shopify "AI is the new floor" (mars 2025)

Tobi a publié un mémo interne devenu viral où il déclare :
- AI fluency = nouvelle compétence de base attendue à Shopify
- Pas d'embauche tant qu'on n'a pas démontré qu'un agent IA ne peut pas faire le job
- "Reflexive AI usage" attendu chez tout employé

C'est le **mémo le plus cité** par les CEOs tech en 2025-2026 pour justifier la transition agentic.

### 3. Endorsement Claude Code

Tobi tweete régulièrement (`@tobi`) son usage personnel de Claude Code. Style : pragmatique, hands-on, partage de patterns concrets sans hype.

## VERBATIM NOTABLES

(Note : verbatim qmd cité par Karpathy, pas directement Tobi — Tobi ne fait pas de marketing sur qmd au-delà du README GitHub)

> "qmd is a good option: it's a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device."
> — Karpathy, LLM Wiki Gist 4 avril 2026 (citant et recommandant le projet de Tobi)

> "a CLI (so the LLM can shell out to it) **and** an MCP server (so the LLM can use it as a native tool)"
> — Karpathy (idem, décrivant l'architecture qmd)

## ALIGNEMENT FORGE

qmd valide doctrine forge :
- **Local-first sur vault** = exactement MCP forge-brain (auto-start SessionStart, port 8091)
- **CLI + MCP** = doctrine cross-surface Thariq (cf [[mcp-vs-skills-doctrine]])
- **Re-ranking** = différence de design avec forge (forge n'a pas de re-ranker, mais BM25 pondéré 10/1/8 + 4-strat fallback)

Si forge-brain devait évoluer, exposer un **CLI fallback** (`forge-brain search "..."`) en plus du MCP serait l'évolution la plus alignée Karpathy/Tobi.

## WIKILINKS

- [[mcp-vs-skills-doctrine]] — doctrine CLI vs MCP, qmd cas d'école
- [[pattern-vault-llm-karpathy]] — Karpathy recommande qmd dans le Gist LLM Wiki
- [[workflow-claude-code-optimal]] — outils vault dans le pipeline complet

## SOURCES

- **Repo qmd** : https://github.com/tobi/qmd
- **Karpathy LLM Wiki Gist** (recommandation) : https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Profil GitHub Tobi** : https://github.com/tobi
- **Twitter** : https://x.com/tobi

---

## NOTE D'HIÉRARCHIE DES SOURCES

Source **secondaire** (couche 3). Mais **correction critique** : ne jamais attribuer qmd à Karpathy. Karpathy = recommandeur, Tobi = créateur. Plusieurs notes du vault antérieures à 2026-05-22 contenaient cette erreur — la correction est appliquée dans toutes les nouvelles canoniques du chantier 22 mai.
