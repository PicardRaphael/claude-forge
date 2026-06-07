---
titre: "Comparaison MCP forge-brain vs MCP brain (28 mai 2026)"
resume: "Audit empirique 14 critères tokens/Karpathy serveur — verdict A : MCP forge-brain mieux conçu (6/1/7). Vrai gap = utilisation par skills, pas code MCP."
aliases:
  - "comparaison mcp forge-brain vs mcp brain"
  - "audit mcp serveurs 28 mai"
  - "verdict mcp forge-brain optimise"
  - "mcp tokens karpathy comparaison"
  - "forge-brain vs neoteem-brain mcp"
domaine: claude-code
type: technique
derniere-maj: 2026-05-28
auteur: claude
sources:
  - "mcp-forge-brain/src/tools/brain.py (1135L, 22 outils, forge)"
  - "mcp-obsidian-brain/src/tools/brain.py (595L, 11 outils, neoteem-brain)"
  - "Audit session 28 mai — recadrage tokens-only Raphaël"
  - "[[pattern-vault-llm-karpathy]] doctrine Karpathy LLM Wiki"
  - "[[mcp-vault-llm-design]] design canonique MCP LLM-optimized"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/mcp"
  - "#domaine/karpathy"
  - "#sujet/tokens"
---

# Comparaison MCP forge-brain vs MCP brain (28 mai 2026)

> Audit empirique honnête bidirectionnel — 14 critères techniques avec extraits code preuve. Verdict A : forge-brain mieux conçu sur tokens/Karpathy/lifecycle. Brain garde 1 avantage (graph/concept), inapplicable au vault forge sans pivot frontmatter.

---

## CONTEXTE — Recadrage de la vraie question

Audit comparatif initial portait sur "claude-forge vs neoteem-brain" globalement. Raphaël a recadré : **vraie question technique** = sur les 2 serveurs MCP (`brain.py` 595L neoteem-brain vs `brain.py` 1135L claude-forge), lequel est mieux conçu côté **économie tokens** et **application Karpathy 3 temps serveur** ?

Procédure : 8 critères empiriques → tableau extraits code → verdict A/B/C.

---

## TABLEAU COMPARATIF 14 CRITÈRES

| # | Critère | forge-brain.py (1135L) | brain.py (595L) | Qui mieux | Preuve code |
|---|---|---|---|---|---|
| 1 | Snippet search_brain (32 tokens entourés `>>> <<<`) | `snippet(notes_fts, 1, '>>> ', ' <<<', '...', 32)` | Identique | égalité | `forge/database.py:125` ↔ `brain/database.py:143` |
| 2 | read_note ENTIÈRE par défaut (Karpathy compliant) | Oui — si `max_lines=0, offset=0, limit_chars=0`, retourne content entier | Oui — `read_text()` direct, signature simple | brain plus pur, forge plus flexible | forge:187-224 / brain:29-40 |
| 3 | Pagination char-based offset/limit_chars | PRÉSENT — header autoguidage `[chars X-Y/total]` + `[suite : appeler avec offset=N, limit_chars=Y]` | ABSENT — tout ou rien | **forge MIEUX** | forge:210-218 |
| 4 | read_section ciblée (économie 30x grosses notes) | PRÉSENT — parsing markdown header levels, include_subsections | ABSENT | **forge MIEUX** | forge:550-594 |
| 5 | read_note_resolved (embeds inlined) | PRÉSENT — résout `![[X#H]]` récursivement, markers `<!-- EMBED -->`, cycle detection | ABSENT | **forge MIEUX** | forge:596-637 |
| 6 | Outils graph/concept (find_by_symbol, traverse_graph, find_concept_chain) | ABSENT — vault forge sans frontmatter cross-stack `references-*` (0 note) | PRÉSENT — table SQLite `symbols(symbol, kind)` + 3 outils + tests dédiés | **brain MIEUX** mais inapplicable forge sans pivot vault | brain:72-363 + brain/database.py:66-73 |
| 7 | find_by_property (Dataview-equivalent) | PRÉSENT — 7 comparateurs (eq/ne/lt/gt/contains/missing/present), filter folder | ABSENT | **forge MIEUX** | forge:639-714 |
| 8 | Observabilité usage_log + usage_stats | PRÉSENT — décorateur `_tool` auto + `usage_stats(days)` agrégation par tool | ABSENT | **forge MIEUX** | forge:867+1097, `usage_log.py` |
| 9 | Lifecycle vault (lint, move, delete, bulk, sessions) | PRÉSENT — `lint_vault`, `move_note`, `delete_note`, `bulk_update_property`, `search_sessions` (FTS5 séparé transcripts) | ABSENT — 0 outil lifecycle | **forge MIEUX** | forge:382-548 |
| 10 | Snippets context défaut (`context=True`) | Oui | Oui | égalité | forge:175-185 ↔ brain:17-27 |
| 11 | suggest_notes si introuvable | PRÉSENT (limit=5) | PRÉSENT (limit=5) | égalité | forge:198-201 ↔ brain:32-36 |
| 12 | Tests pytest | 12 fichiers, 1814L. Tests lifecycle (move/bulk/section/find_by_property/lint/usage_log). 0 test graph/concept | 11 fichiers ~1500L. Tests dédiés graph/concept | égalité orientations | tests/ chaque repo |
| 13 | Architecture code modules src/ | 13 fichiers — brain.py 1135L + database/indexer/usage_log/sessions_*/git_sync | 9 fichiers — brain.py 595L + database 1054L + indexer/git_sync | forge plus large périmètre, brain plus compact | src/ chaque repo |
| 14 | Pondération BM25 (file_stem:10 / content:1 / aliases:8) | Identique | Identique | égalité | config.yaml |

**Score net** : forge 6 gains (#3, 4, 5, 7, 8, 9) — brain 1 gain (#6 mais inapplicable forge) — égalité 7 (#1, 2, 10, 11, 12, 13, 14).

---

## VERDICT A — forge-brain mieux conçu techniquement

### Faits empiriques

1. **Économie tokens** — forge a 3 mécanismes économiques uniques :
   - `read_section` (gain 30x sur CHANGELOG 62k → 2k chars)
   - `read_note(offset, limit_chars)` (pagination autoguidée avec header `[suite : offset=N]`)
   - `read_note_resolved` (MOC → N notes en 1 appel)

2. **Karpathy server-side** — les 2 retournent note ENTIÈRE par défaut sur `read_note` (Karpathy compliant). Forge **RENFORCE Karpathy** : la note reste lisible en N passes sans tronquer grâce au header autoguidage. Brain n'a pas ce filet — sur une note de 5000L, brain retourne 5000L d'un coup ou rien.

3. **Observabilité** — forge logue chaque appel + `usage_stats(days)` permet décisions data-driven sur outils à garder/retirer. Brain n'a pas. Anti-pattern explicite dans [[mcp-vault-llm-design]] : *"@_tool wrapping sans logging = observabilité indispensable pour décision garder/supprimer outil"*.

4. **Lifecycle vault** — forge 9 outils lifecycle. Brain 0.

### Faiblesse réelle identifiée côté forge

**Critère #6 graph/concept** : brain a `find_by_symbol` + `traverse_graph` + `find_concept_chain` = routage déterministe vault sans dépendre de FTS5 lexical. Forge n'en a pas. **Précondition bloquante** : vault forge typage cross-stack `references-*` absent (grep empirique : 0 note avec `pg-functions:`/`tables:`/`endpoints:`). Faiblesse théorique, pas exploitable sans pivot vault structurel.

### Verdict empirique honnête

**MCP forge-brain n'est PAS sous-optimisé**. Aucune action sur code MCP forge-brain nécessaire.

---

## LE VRAI GAP — Utilisation par les skills forge

Le serveur forge a les meilleurs mécanismes économie tokens mais la **skill `forge-brain` SKILL.md** (197L) ne prescrit pas :

- Quand utiliser `read_section` plutôt que `read_note` (gain 30x)
- Quand paginer avec `offset/limit_chars` (autoguidage présent côté serveur mais skill ne l'invoque pas)
- Quand utiliser `read_note_resolved` sur un MOC
- Quand consulter `usage_stats` pour pruning

C'est **exactement le gap identifié** : plugin neoteem-brain a la doctrine opérationnelle Karpathy (3 temps SEARCH/SELECT/READ + N=3 + table 4 modes + priorisation tools + pagination 500L par passes formalisés en skill). Forge a les MEILLEURS outils côté serveur mais pas la doctrine opérationnelle pour les exploiter côté skill.

---

## RECOMMANDATIONS AMEND skills forge

AMEND `.claude/skills/forge-brain/SKILL.md` (aucune modif code MCP) :

| ID | AMEND | Effort | Justification |
|---|---|---|---|
| A1 | Section "Pattern Karpathy opérationnel 3 temps + N=3 + 4 modes" | ~30 min | Canonique vault [[pattern-vault-llm-karpathy]] codifie architecture, pas opération. Plugin neoteem-brain a la doctrine opérationnelle, forge ne l'a pas. |
| A2 | Matrice priorisation tools "search_brain = dernier recours" (find_by_property > read_section > find_by_path > search_brain) | ~15 min | Skill liste 22 outils sans hiérarchie. Anti-pattern : enchaîner search_brain quand 1 read_section/find_by_property suffit. |
| A3 | Règle pagination autoguidée "ne jamais s'arrêter au milieu" + appel à `read_note(offset, limit_chars)` suivant header serveur | ~15 min | Mécanisme serveur présent (forge:215-217), skills ne l'exploitent pas. |

Total effort : ~1h pour faire matcher l'utilisation skill à la qualité du serveur.

---

## RECOMMANDATIONS P3 BRAIN ← FORGE (à transmettre Raphaël pour décision séparée)

Optimisations possibles côté neoteem-brain repo global (hors plugin) :

- **P3a — Pagination autoguidée serveur** : `brain.py` retourne tout d'un coup. Ajouter mécanisme `offset/limit_chars` avec header `[suite : offset=N]` (porter de `forge:210-218`). Effort ~1-2h port + tests.
- **P3b — read_section ciblée** : gain 30x grosses notes. Porter `forge:550-594`. Effort ~2-3h.
- **P3c — usage_log + usage_stats** : pas d'observabilité. Porter `forge:867+1097`. Effort ~1-2h.
- **P3d — read_note_resolved (embeds inlined)** : pour MOC = N appels au lieu de 1. Porter `forge:596-637`. Effort ~2h.

---

## ANTI-PATTERNS

- ❌ **Conclure "brain mieux car plus simple"** — économie tokens nécessite mécanismes non triviaux (pagination autoguidée, read_section, find_by_property). Simplicité n'est pas optimalité.
- ❌ **Migrer find_by_symbol vers forge sans pivot vault** — vault forge n'a pas le typage cross-stack `references-*`. Outils auraient rien à traverser. Migration plug-and-play impossible.
- ❌ **Modifier code MCP forge-brain** — verdict A : déjà bien conçu. Gap = utilisation par skills, pas serveur.
- ❌ **Ignorer le gap doctrinal opérationnel** — les mécanismes serveur existent mais ne sont pas exploités. Sans AMEND skill, gain tokens potentiel non réalisé.

---

## WIKILINKS

- [[pattern-vault-llm-karpathy]] — Doctrine Karpathy LLM Wiki (architecture)
- [[mcp-vault-llm-design]] — Design canonique MCP LLM-optimized (forge-brain v1.3)
- [[mcp-vs-skills-doctrine]] — MCP data / Skills how-to / Bash exploration
- [[forge-brain-proactive]] — Rule vault check MCP obligatoire
- [[architecture-cerveau-obsidian-mcp]] — Architecture cerveau Obsidian + MCP

---

## SOURCES — Extraits code preuve

### forge-brain pagination autoguidée
```python
# forge:215-218
header = f"[chars {offset}-{min(end, total_chars)}/{total_chars}]\n"
if end < total_chars:
    header += f"[suite : appeler avec offset={end}, limit_chars={limit_chars}]\n"
return header + "\n" + chunk
```

### forge-brain read_section economie 30x
```python
# forge:550-594
def read_section(self, file: str, heading: str, include_subsections: bool = True) -> str:
    """Cas d'usage : CHANGELOG 62k chars, section "2026-05-24" = ~2k chars."""
```

### brain find_by_symbol routage déterministe
```python
# brain:72-117
def find_by_symbol(self, symbol: str, kind: str | None = None,
                   include_collections: bool = True) -> str:
    """Trouve la ou les note(s) du vault qui documentent un symbole technique exact."""
```

### forge-brain usage_log observabilité
```python
# forge:1097-1103
def usage_stats(days: int = 7) -> str:
    """Aggregate usage des outils MCP sur les N derniers jours (depuis logs/usage.jsonl)."""
```
