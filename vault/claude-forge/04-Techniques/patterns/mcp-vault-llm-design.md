---
titre: "Pattern : MCP vault optimise pour LLM (pas pour humain)"
resume: "Design principles canoniques pour un MCP qui sert un vault Karpathy a un LLM : 3 ops Karpathy + 6 ops LLM-specific (find_by_property, bulk_update, read_section, embed resolution, lint, usage_stats). Base : MCP forge-brain v1.3, 69 tests, 348 notes prod."
aliases:
  - "mcp vault llm design"
  - "mcp pour llm pas humain"
  - "design mcp vault karpathy"
  - "recipe mcp forge-brain"
  - "mcp llm-optimized"
  - "pattern mcp obsidian vault"
derniere-maj: 2026-05-24
auteur: claude
type: pattern
sources:
  - "Design pattern Karpathy LLM Wiki (Gist 4 avril 2026)"
  - "kepano/obsidian-skills (5 skills officielles Anthropic)"
  - "Implementation forge-brain v1.0 -> v1.3 (24-25 mai 2026)"
  - "69 tests pytest, 348 notes prod, 297->5 wikilinks brises (-98%)"
tags:
  - "#type/pattern"
  - "#domaine/vault"
  - "#domaine/mcp"
  - "#domaine/karpathy"
  - "#domaine/llm-wiki"
---

# Pattern MCP vault LLM-optimized

> **Principe fondateur** : un MCP qui sert un vault Obsidian a un LLM n'a PAS les memes besoins qu'un Obsidian client humain. Le LLM ne voit pas la graph view, n'a pas besoin de Dataview UI, ne fait pas de Templater interactif. Il lui faut : recherche rapide, ecriture atomique, queries frontmatter, economie tokens, observabilite usage.

---

## QUOI — 9 ops canoniques

### 3 ops Karpathy (universelles)

1. **Ingest** : capturer une source externe vers le wiki
   - `create_note(path, content)`, `append_note(file, content)`, `insert_section(file, marker, content, position)`, `update_note(file, content)`

2. **Query** : repondre a une question via le wiki
   - `search_brain(query, limit, context)` — FTS5 BM25 pondere file_stem:10 / aliases:8 / content:1
   - `read_note(file, max_lines, offset, limit_chars)` — pagination char-based pour grosses notes
   - `read_note_by_path(path)` — acces direct path normalise (defensif)
   - `get_backlinks(file)` — graphe, case-insensitive
   - `get_tags()` — vue structurelle
   - `get_property(file, name)` — frontmatter lookup
   - `list_notes(folder, limit)` — inventaire

3. **Lint** : maintenir la qualite du wiki
   - `lint_vault(limit)` — aliases<4, orphelines, sans tag, YAML casse, wikilinks brises (filtres false-positives)

### 6 ops LLM-specific (forge-brain v1.3)

4. **find_by_property** — Dataview-equivalent pour LLM
   - Comparateurs : `eq | ne | lt | gt | contains | missing | present`
   - Cas d'usage : notes stales (`derniere-maj lt`), doublons marques (`statut eq doublon`), sources vides (`sources missing`)
   - Remplace : Dataview UI cote Obsidian

5. **bulk_update_property** — economie round-trips
   - Pattern observe : update derniere-maj sur 16 leaders apres audit = 16 appels avant, 1 appel maintenant
   - Reporte succes/echecs par note

6. **read_section(file, heading, include_subsections)** — economie tokens
   - CHANGELOG 62k chars, section "2026-05-24" = ~2k chars (gain 30x)
   - Respect hierarchie headers (s'arrete au prochain de meme niveau)

7. **read_note_resolved(file, depth)** — embed resolution recursive
   - Inline le contenu des `![[X]]` (avec section optionnelle `![[X#H]]`)
   - Detection cycles (`CYCLE: X`)
   - Marqueurs `<!-- EMBED: X -->` pour parsing LLM
   - Remplace : rendering embeds Obsidian client

8. **move_note(file, new_path, update_wikilinks)** — rename + rewriting
   - Reecrit `[[stem]]`, `[[stem|alias]]`, `[[stem#section]]`, `![[stem]]` (embeds), `[[Stem]]` (case-insensitive)
   - SKIP wikilinks dans code blocks (litteral)
   - Atomicite : snapshot backlinks AVANT rename
   - Remplace : rename natif Obsidian (2024+)

9. **delete_note(file, force)** — suppression sure
   - Refuse par defaut si backlinks > 0
   - `force=True` rapporte liste wikilinks brises post-suppression

### Bonus observabilite

- **usage_stats(days)** — agregation calls/total_ms/errors/avg_chars par tool
- Backed by `logs/usage.jsonl` (1 ligne par appel, args tronques >200 chars)
- Permet : detection tools jamais appeles, latence anormale, taux d'erreur par tool

---

## POURQUOI — Le probleme resolu

Sans MCP LLM-optimized :
- **Tokens gaspilles** : `read_note(CHANGELOG)` retourne 62k chars dont 60k inutiles
- **Round-trips multiplies** : 16 `update_property` au lieu d'1 `bulk_update_property`
- **Drift silencieux** : aliases dupliques YAML casses non detectes, notes orphelines accumulees
- **Move dangereux** : rename + wikilinks brises silencieusement (Obsidian le fait, LLM ne devrait pas dupliquer)
- **Embeds opaques** : `![[X]]` rendu litteral par read_note brut, le LLM ne voit pas le contenu

Avec MCP LLM-optimized :
- **Pagination** : offset/limit_chars sur read_note + read_section dedie
- **Bulk ops** : economie 80%+ round-trips sur audits/refactors mass
- **Lint structurel** : 297 -> 5 brises (-98%) sur vault 348 notes en 1 session
- **Move atomique** : 2 cas prod testes (avec/sans rename, 3 backlinks reecrits)
- **Embed resolution** : `read_note_resolved(MOC)` inline N notes en 1 appel

---

## COMMENT — Architecture forge-brain

### Stack
- **FastMCP 2** (Python 3.11+) — protocol MCP
- **SQLite FTS5** — search BM25 + tokenize unicode61 + remove diacritics
- **pyyaml** — frontmatter parsing
- **Tables** : notes (id, file_stem, path, content, frontmatter, last_modified, content_hash), aliases, links, tags, notes_fts (virtual FTS5)

### Layer Karpathy strict
- `raw/` — sources externes immuables (Karpathy layer 1, LLM ne touche pas)
- `wiki/` — couche LLM-owned (00-Hub a 07-Prompts + 1-Projets + 2-Casquettes + Knowledge + 0-Inbox)
- `SCHEMA.md`, `index.md`, `log.md`, `CHANGELOG.md` — schema/orientation/trace/narration

### Defenses critiques observees
1. **Path normalization** — strip prefix vault accidentel, refuse path absolu hors vault (security)
2. **Tag null filter** — `None` dans liste YAML filtres
3. **Aliases dupliques detection** — pattern inline `[...]` + bloc liste orphelin = warning
4. **Atomicite move** — snapshot backlinks AVANT rename (transaction-like)
5. **Code block protection** — wikilinks dans `` ` `` ou ` ``` ` preserves litteraux lors move
6. **Case-insensitive backlinks** — `[[Alpha]]` matche `alpha.md` (coherence Obsidian)
7. **Self-link rewriting** — note deplacee qui contient `[[own-stem]]` mis a jour

---

## ANTI-PATTERNS

### Cote design
- **Copier Obsidian feature par feature** — graph view, Dataview UI, Templater sont pour humains. Skip.
- **Implementer `obsidian-cli` skill** — viole doctrine "MCP UNIQUEMENT". Cf [[forge-brain-proactive]].
- **Tools generaux a tout faire** — un tool = un cas d'usage clair. `find_by_property` != `query_anything`.
- **"PARFAIT" pre-mesure** — feature creep. Toujours `usage_stats` avant ajouts.

### Cote implementation
- **Move sans tests adverses** — 4 silent data loss sauves par DA cette session (self-link, embed, casse, code blocks)
- **Wikilink rewriting par partial match** — `re.escape(old_stem) + r"(?=[\]|#])"` obligatoire (sinon foo matche foo-bar)
- **delete force=True sans reporter brises** — caller doit savoir quoi nettoyer apres
- **Sub-agent qui copie-colle drift** — verifier source de verite AVANT mass-fix (cf [[feedback_subagent_audit_category_error]])

### Cote workflow
- **`@_tool` wrapping sans logging** — observabilite indispensable pour decision "garder/supprimer outil"
- **Tests sur fixtures uniquement** — DA requiert "test sur snapshot reel" avant declarer prod-ready

---

## EXEMPLES CONCRETS (forge-brain v1.3)

### Audit massif (4 vagues sub-agents paralleles)
```python
# Avant v1.2 : 16 round-trips
for leader in leaders_to_update:
    update_property(leader, "derniere-maj", "2026-05-24")  # 16x

# Apres v1.3 : 1 round-trip
bulk_update_property(leaders_to_update, "derniere-maj", "2026-05-24")
```

### Lecture grosse note ciblee
```python
# Avant : 62k chars charges
read_note("CHANGELOG")

# Apres : section specifique
read_section("CHANGELOG", "## 2026-05-24")  # ~2k chars
```

### Pivot doctrinal (move + rewriting auto)
```python
# Avant : git mv + grep -r [[old]] + sed mass + reindex manuel
mv vault/X.md vault/Archive/X.md
grep -r "\[\[X\]\]" vault/ | xargs sed -i ...  # casse les variantes

# Apres : atomique avec tests adverses
move_note("X", "Archive/X.md")  # snapshot backlinks AVANT, rewriting safe
```

### Detection drifts post-pivot
```python
# Notes stales > 90 jours
find_by_property("derniere-maj", "2026-02-24", "lt")

# Doublons marques
find_by_property("statut", "doublon")

# Notes sans sources
find_by_property("sources", comparator="missing")

# Lint complet
lint_vault(limit=50)  # 297 -> 5 brises (-98%)
```

---

## WIKILINKS

- [[pattern-vault-llm-karpathy]] — pattern 3-layers Karpathy
- [[mcp-vs-skills-doctrine]] — MCP / Skills / Bash quand quoi
- [[methode-pivoter-doctrine]] — checklist post-pivot (anti-drift)
- [[methode-analyser-repo]] — sequence A->B->C->D->E
- [[SCHEMA]] — conventions vault forge-brain
- [[index]] — orientation LLM content-oriented
- [[log]] — trace append-only Karpathy

---

## GOTCHAS

- **Indexation** : restart MCP necessaire apres modif src/ (FastMCP charge tools au demarrage)
- **CRLF Windows** : Git warning `LF will be replaced by CRLF` benin, contenu identique
- **Sub-agents et MCP** : sub-agents non-reentrants, NE PEUVENT PAS appeler Agent. Sub-agent qui doit deleguer = ESCALADE REQUISE vers session principale.
- **Pagination offset** : char-based, pas line-based. Plus precis pour LLM (token-aware ?)
- **Embed resolution depth** : par defaut depth=1. Profondeur 5+ = explosion contexte potentielle.

---

## METRIQUES (24 mai 2026)

- **15 -> 19 tools MCP** (+find_by_property, +bulk_update_property, +read_section, +read_note_resolved)
- **69 tests pytest** (vs 0 au depart session)
- **348 notes vault** indexees, 2277 wikilinks, 2078 aliases
- **297 -> 5 brises** apres lint + 2 vagues fixes (-98%)
- **2 moves prod reussis** (sans rename + avec rename + 3 backlinks reecrits)
- **Pagination CHANGELOG** : 62k chars accessibles par chunks de 500 (sans fichier intermediaire)
- **Logging** : `logs/usage.jsonl` actif depuis v1.2

---

## STATUT

- **v1.0** (24 mai 2026 matin) : 11 tools initiaux, 0 tests
- **v1.1** (24 mai 2026 apres-midi) : +delete_note, +move_note, +lint_vault, 35 tests, fix path interp + tag None + aliases duplicates
- **v1.1.1** : tests prod move_note (2 cas reels), filtres lint false-positives
- **v1.2** (24 mai 2026 soir) : +pagination read_note, +usage_log, +usage_stats, 44 tests
- **v1.3** (24 mai 2026 soir) : +find_by_property, +bulk_update_property, +read_section, +read_note_resolved, 69 tests
- **Next** (v1.4+) : decision basee sur `usage_stats(days=30)` reels (DA-recommandation)
