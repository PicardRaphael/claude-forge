---
description: Query forge-brain vault proactively — at session start, before creating components, after learning, and after mistakes
globs: "*"
---

# Forge Brain — Requêtage proactif

Le vault forge-brain = mémoire infinie. L'interroger est un RÉFLEXE.

## COMMENT — MCP forge-brain UNIQUEMENT

Accès vault EXCLUSIVEMENT via MCP `forge-brain` (auto-start SessionStart, port 8091). JAMAIS Grep/Read/Glob brut, JAMAIS CLI Obsidian.

**22 outils disponibles** — matrice de décision complète : skill `forge-brain` + [[mcp-vault-llm-design]].

Outils les plus utilisés :
- `search_brain` — FTS5 BM25 (file_stem:10 / aliases:8 / content:1)
- `read_note` (lit ENTIÈRE par défaut), `read_section` (1 section)
- `create_note`, `append_note`, `update_property`, `bulk_update_property`
- `move_note`, `delete_note` (atomiques + wikilinks auto)

Fallback : si MCP crash, Read/Glob `vault/claude-forge/`. Cas anormal.

## QUAND interroger

| Situation | Action |
|---|---|
| **Début de session** | Notes récentes pertinentes |
| **Avant CRÉER skill/agent/hook/rule/CLAUDE.md** | Best practices + `Knowledge/erreurs/` |
| **Avant répondre technique** | Vérifier vault + `derniere-maj` (> 7j = compléter web) |
| **Analyse repo/projet** | Notes concurrents + patterns existants |
| **Après cc-news ou recherche web** | Capitaliser en notes atomiques + MAJ MOCs |
| **Après erreur significative** | Note `Knowledge/erreurs/` |

## OÙ écrire — Ontologie vault

Source canonique : `vault/claude-forge/SCHEMA.md` (13 dossiers wiki + Knowledge/ + raw/). Voir aussi [[pattern-vault-llm-karpathy]].

## Standard qualité notes

Source canonique : [[architecture-cerveau-obsidian-mcp]] section "Standard qualité" + skill `obsidian-markdown` pour syntaxe.

Minimums : 4-6 aliases · resume 1 phrase spécifique · derniere-maj ISO · 2+ tags · 2+ wikilinks.

## Cycle d'apprentissage vault

Le vault = système nerveux forge. Chaque agent y lit ET écrit. Pas de Langfuse externe — single source of truth.

| Agent/Skill | Lit | Écrit |
|---|---|---|
| `devils-advocate` | `Knowledge/erreurs|critiques/` | `Knowledge/critiques/` |
| `reasoning-cache` | `Knowledge/raisonnements/` | `Knowledge/raisonnements/` |
| `skill-evolve` | Skills + `Knowledge/evolutions/` + mémoire | `Knowledge/evolutions/` |
| `forge-review` | CLAUDE.md + rules + skills + agents | `Knowledge/reviews/` |

## Vault path

`vault/claude-forge/`
