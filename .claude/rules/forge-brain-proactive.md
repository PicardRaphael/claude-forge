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

## read_section vs read_note (absorbe l'ex-rule read-section-preference)

- Question PRÉCISE + section identifiable depuis `search_brain` → `read_section` (économe).
- Scope LARGE, première lecture d'une note, ou doute sur la pertinence d'une section seule → `read_note` ENTIÈRE (mieux vaut redondance qu'info manquante).
- Après un `read_section` insuffisant → escalader à `read_note`. Refuser la lecture entière par dogme tokens quand le besoin est large = info manquante garantie.
- ❌ `read_note` systématique sur grosse note (CHANGELOG, log) quand 1 section suffit · ❌ `read_section` sans connaître la structure de la note.

## Protocole par type d'agent (absorbe l'ex-rule vault-consultation-protocol)

Vault check = advisory (doctrine 22 mai : pas de hook d'enforcement). Si le prompt d'invocation contient déjà les infos vault, l'étape est satisfaite. Écriture de notes → skill `obsidian-markdown` pour la syntaxe.

| Type d'agent | Vault |
|---|---|
| Créateurs (skill/agent/hook/claudemd) | Systématique au démarrage |
| Analyseurs (repo-inspector tous modes) | Systématique — référentiel pour juger |
| Exécutants (code-dev, self-updater) | Si sujet nouveau ou doute sur prior art |
| devils-advocate | Conditionnel ciblé, max 2 requêtes |

Référence dans un agent (2 lignes, pas de copier-coller) : « Vault check : consulter le vault selon `.claude/rules/forge-brain-proactive.md` (advisory). »
Anti-patterns : scanner le vault par réflexe sans besoin · skipper le vault sur un créateur « parce que simple » · Bash heredoc pour écrire des notes (boucle quoting Windows).

## OÙ écrire — Ontologie vault

Source canonique : `vault/claude-forge/SCHEMA.md` (dossiers wiki + Knowledge/ — `raw/` supprimé au pivot agent-first 2026-06-27). Voir aussi [[decision-vault-agent-first]].

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
