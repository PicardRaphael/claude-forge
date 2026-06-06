---
name: forge-brain
allowed-tools: mcp__forge-brain__*
user-invocable: true
description: ALWAYS invoke when user asks about vault content, past decisions, or knowledge base. Search, read, and write the forge-brain Obsidian vault. Use PROACTIVELY at session start, before creating skill/agent/hook, after cc-news.
---

# Forge Brain

Knowledge base Obsidian de claude-forge. Stocke tout ce que j'apprends : Claude Code, concurrents, modèles, techniques, leaders, industrie.

**Vault** : `vault/claude-forge/`

## Quand utiliser — Le vault est un RÉFLEXE

| Situation | Action |
|-----------|--------|
| Début de session | Chercher les notes récentes pour rappel contexte |
| **Avant de créer skill/agent/hook/prompt** | **Chercher best practices + erreurs passées + prompts réutilisables** |
| **Analyse de repo / projet** | **Chercher patterns, concurrents, techniques pertinentes** |
| Question sur feature/outil | Chercher dans le vault AVANT de répondre |
| Après cc-news | Créer/mettre à jour les notes avec les découvertes |
| Nouvelle info apprise | Créer une note atomique |
| **Erreur significative commise** | **Créer note dans `Knowledge/erreurs/` avec template `erreur.md`** |
| Info potentiellement datée | Vérifier la note existante + `derniere-maj` |

## Accès au vault — MCP forge-brain (OBLIGATOIRE)

Le MCP forge-brain (auto-start SessionStart, port 8091) est le SEUL moyen d'accès au vault.
Ne JAMAIS utiliser la CLI Obsidian, Grep, Read ou Glob brut sur le vault.

### Pattern Karpathy opérationnel — Doctrine consultation vault

Source canonique : [[pattern-vault-llm-karpathy]] (architecture) + [[comparaison-mcp-forge-brain-vs-mcp-brain-28mai2026]] (gap utilisation skills).

**Principe** : une réponse construite à partir de snippets est PIRE qu'une réponse construite à partir de notes entières top N. Les snippets `search_brain(context=true)` servent à IDENTIFIER les notes pertinentes, JAMAIS à RÉPONDRE.

#### 3 temps SEARCH/SELECT/READ

```
1. SEARCH (large)     → search_brain(query, limit=5, context=true)
                        → snippets pour scorer la pertinence

2. SELECT (sélectif)  → identifier top N notes selon mode (table ci-dessous)
                        → trier par dossier : Knowledge/ > 04-Techniques/ > 01-Claude/ > autres

3. READ (entier)      → read_note ENTIÈRE sur CHAQUE note du top N
                        → ou read_section ciblée si section précise connue
                        → croiser les N notes pour construire la réponse
```

#### Table 4 modes — N par type de question

| Signal dans la question | Mode | N (top notes à lire entièrement) | Budget appels max |
|---|---|---|---|
| « Comment fonctionne X ? », « Pourquoi Y ? » | Query | N=3 | 1 search + 3 read_note = 4 |
| Audit / classification N composants | Audit | N=4 | 1-2 search + 4 read_note = 6 |
| « Tous les X », « liste complète », « récap exhaustif » | Exhaustive | 2-4 sources | 1 search + 1 MOC + 2-4 read_note = 7 |
| « Cartographie le domaine X », exploration explicite | Exploration | Illimité | BFS, suivre `[[wikilinks]]` jusqu'à contexte complet |

#### Anti-patterns Karpathy

❌ « Le snippet de search_brain contient la réponse → je réponds sans read_note »
✅ « Le snippet m'indique que cette note est pertinente → je read_note ENTIÈRE »

❌ « Je lis seulement la note la plus pertinente (N=1) »
✅ « Je lis les 3 premières notes pertinentes (N=3) et je croise »

❌ « Je m'arrête au snippet contenant un mot-clé recherché »
✅ « Le snippet indique pertinence, pas réponse — je read_note pour fonder ma réponse »

### Outils MCP — Lecture

| Outil | Usage | Quand utiliser |
|-------|-------|----------------|
| `search_brain(query, limit, context)` | FTS5 BM25 pondéré file_stem:10 / aliases:8 / content:1 | Chercher info CAPITALISÉE (vault), défaut exploration |
| `search_sessions(query, limit, project, role, since)` | FTS5 sur transcripts session BRUTS non capitalisés | "Qu'a-t-on dit sur X" — complément search_brain, historique conversationnel |
| `read_note(file)` | **Lit la note ENTIÈRE** (frontmatter + body) | **Défaut pour lire une note** — pas de troncature |
| `read_note(file, offset, limit_chars)` | Pagination char-based | UNIQUEMENT si note > 50k chars (CHANGELOG, log) |
| `read_section(file, heading)` | Lit UNE section (header → prochain header même niveau) | Économie tokens 30x sur grosses notes (CHANGELOG) |
| `read_note_resolved(file, depth=1)` | Note + inline embeds récursivement | MOC avec embeds — 1 appel = N+1 notes en contexte |
| `read_note_by_path(path)` | Lire par chemin exact | Quand on a le path complet (pas le stem) |
| `get_backlinks(file)` | Notes pointant vers (case-insensitive) | Navigation graphe, audit orphelines |
| `get_tags()` | Tags triés par fréquence | Vue structurelle |
| `get_property(file, name)` | 1 propriété frontmatter | Vérif derniere-maj/type sur 1 note |
| `find_by_property(name, value, comparator, folder, limit)` | **Dataview-equivalent** : query frontmatter | Notes stales (`lt` date), doublons (`eq`), sources vides (`missing`). Comparateurs : eq/ne/lt/gt/contains/missing/present |
| `list_notes(folder, limit)` | Inventaire notes d'un dossier | Audit par cluster |
| `vault_stats()` | Stats vault complètes | Photo globale |
| `lint_vault(limit)` | Détecte aliases<4, orphelines, sans tag, YAML cassé, wikilinks brisés | Audit qualité vault |
| `usage_stats(days)` | Agrégation calls/total_ms/errors par tool | Décisions pruning outils MCP |

### Pagination autoguidée — Ne jamais s'arrêter au milieu d'une note

**Règle Karpathy dure** : notes vault (CHANGELOG, log, MOCs riches) peuvent faire 1000+ lignes. Ne JAMAIS couper la lecture au milieu. Le MCP forge-brain offre un mécanisme **autoguidé** via header serveur.

#### Mécanisme serveur

```python
# forge-brain/src/tools/brain.py:215-217
header = f"[chars {offset}-{end}/{total_chars}]\n"
if end < total_chars:
    header += f"[suite : appeler avec offset={end}, limit_chars={limit_chars}]\n"
```

#### Comment exploiter la pagination

1. **Première lecture** : `read_note(file, offset=0, limit_chars=20000)` (20k chars ≈ 500 lignes)
2. **Suivre le header** : si réponse contient `[suite : appeler avec offset=20000, limit_chars=20000]`, **APPELER** avec ces paramètres exacts
3. **Itérer** jusqu'à ce que le header ne contienne plus `[suite :]`
4. **Croiser** les N chunks pour construire la réponse

#### Quand paginer vs read_section

| Cas | Outil |
|---|---|
| Note > 50k chars (CHANGELOG, log) | `read_note(offset, limit_chars)` en N passes |
| Section précise connue | `read_section(file, heading)` — 1 appel, gain 30x |
| Note normale < 50k chars | `read_note(file)` entière — Karpathy compliant |

#### Anti-patterns pagination

❌ « C'est massif, je ne peux pas tout lire » → INTERDIT. Paginer ou read_section.
❌ Ignorer le header serveur `[suite : offset=N]` → l'outil donne l'autoguidage, l'exploiter.
❌ « Le snippet du milieu suffit » → INTERDIT. Lire la suite.

### Outils MCP — Écriture

| Outil | Usage | Quand utiliser |
|-------|-------|----------------|
| `create_note(path, content)` | Créer note | Capitaliser info |
| `append_note(file, content)` | Ajouter à la fin | Étoffer note existante |
| `insert_section(file, marker, content, position)` | Insérer avant/après un header | Insertion ciblée |
| `update_note(file, content)` | **Remplace EN ENTIER** | Refonte complète (rare) |
| `update_property(file, name, value)` | 1 prop sur 1 note | Update ciblé |
| `bulk_update_property(files, name, value)` | **Même prop sur N notes en 1 appel** | Pattern audit : derniere-maj 16 leaders = 1 appel |

### Outils MCP — Move / Delete

| Outil | Usage | Quand utiliser |
|-------|-------|----------------|
| `move_note(file, new_path, update_wikilinks=True)` | Déplace + réécrit wikilinks dans backlinks si stem change | Rename + déplacement atomique safe |
| `delete_note(file, force=False)` | Refuse si backlinks > 0 sauf force. `force=True` rapporte wikilinks brisés | Cleanup safe |

### Matrice décision rapide

| Tâche | Outil prioritaire |
|-------|-------------------|
| Chercher info | `search_brain` |
| Chercher dans l'historique de session brut | `search_sessions` |
| Lire 1 note complète | `read_note(file)` |
| Lire section précise | `read_section(file, heading)` |
| Lire MOC avec embeds | `read_note_resolved(file)` |
| Lire grosse note par morceaux | `read_note(file, offset, limit_chars)` |
| Trouver notes par frontmatter | `find_by_property` |
| Update prop sur 1 note | `update_property` |
| Update prop sur N notes | `bulk_update_property` |
| Renommer + rewriting | `move_note` |
| Supprimer safe | `delete_note` |
| Audit qualité vault | `lint_vault` |
| Mesurer usage outils | `usage_stats(days=7)` |

### Priorisation tools AVANT search_brain — Hiérarchie économie tokens

**`search_brain` est le DERNIER RECOURS**, pas le réflexe par défaut. L'anti-pattern identifié dans [[comparaison-mcp-forge-brain-vs-mcp-brain-28mai2026]] : enchaîner 3+ search_brain quand 1 outil ciblé suffit.

| Signal dans la question | Tool à privilégier (AVANT search_brain) | Gain tokens |
|---|---|---|
| Recherche par metadata (frontmatter : type, derniere-maj, auteur, tag) | `find_by_property(name, value, comparator)` | Ciblage direct vs scan FTS5 |
| Section précise connue d'une note (header markdown) | `read_section(file, heading)` | 30x sur grosses notes |
| Nom de note ou alias connu | `read_note(file)` direct ou `read_note_by_path(path)` | Pas de recherche, lecture directe |
| MOC avec embeds `![[X]]` à explorer | `read_note_resolved(file, depth=1)` | 1 appel = N+1 notes en contexte |
| Backlinks vers une note (graphe inverse) | `get_backlinks(file)` | Direct, pas de FTS5 |
| Inventaire dossier | `list_notes(folder, limit)` | Direct |
| Exploration large sans nom technique précis | `search_brain(query, limit, context=true)` | Dernier recours |

**Anti-pattern majeur** : `search_brain` en 5 variantes de mots-clés pour trouver une note → 5 appels FTS5 quand `find_by_property` ou `read_section` ferait le job en 1 appel ciblé.

**Règle** : classer la question (metadata ? section ? nom connu ?) → outil ciblé. `search_brain` UNIQUEMENT si rien d'autre ne convient.

### Format Obsidian Flavored Markdown

Quand on CRÉE une note via MCP `create_note`, le contenu doit respecter la skill `obsidian-markdown` :
- Frontmatter YAML (titre, resume, aliases 4-6, type, derniere-maj, tags)
- Wikilinks `[[Note]]` (pas de markdown links pour les notes internes)
- Minimum 2 wikilinks par note
- Résumé spécifique dans le frontmatter

### Fallback (si MCP crash)

Read/Glob direct sur `vault/claude-forge/`. Ne devrait jamais arriver.

## Créer une note

1. Lire le template correspondant via MCP : `read_note(file="<type>")` dans `Templates/`
2. Créer la note avec `create_note(path="...", content="...")` en suivant le template
3. Ajouter le wikilink dans le MOC correspondant via `append_note`

## Structure du vault

```
0-Inbox/          — Capture rapide, à trier par /done
1-Projets/        — Notes de contexte par projet (Neoteem, Claude-Forge, etc.)
2-Casquettes/     — Aires de responsabilité de vie (profil holistique, famille, gaming)
00-Hub/           — Home + 6 MOCs (index par thème)
01-Claude/Code/   — features/, changelog/, best-practices/, hooks/, skills/, agents/
02-Concurrents/   — gemini-cli/, codex/, copilot/, cursor/, xai/
03-Modeles/       — claude/, gpt/, gemini/, grok/
04-Techniques/    — prompt-engineering/, context-engineering/, patterns/
05-Leaders/       — Fiches personnes clés
06-Industrie/     — Market, funding, événements, tendances
07-Prompts/       — system-prompts/, agent-prompts/, skill-prompts/, templates-prompts/
Knowledge/        — explorations/, syntheses/
Templates/        — 12 templates (+context-projet, +context-casquette)
```

## Templates (OBLIGATOIRE)

Toujours lire le template AVANT de créer une note :

| Dossier cible | Template |
|---|---|
| `01-Claude/Code/features/` | `Templates/feature.md` |
| `01-Claude/Code/changelog/` | `Templates/changelog.md` |
| `01-Claude/Code/best-practices/` | `Templates/best-practice.md` |
| `02-Concurrents/` | `Templates/concurrent.md` |
| `03-Modeles/` | `Templates/modele.md` |
| `04-Techniques/` | `Templates/technique.md` |
| `05-Leaders/` | `Templates/leader.md` |
| `06-Industrie/` | `Templates/knowledge.md` |
| `07-Prompts/` | `Templates/prompt.md` |
| `Knowledge/` | `Templates/knowledge.md` |
| `1-Projets/` | `Templates/context-projet.md` |
| `2-Casquettes/` | `Templates/context-casquette.md` |

## Frontmatter obligatoire

```yaml
---
titre: "Titre lisible"
resume: "1 ligne"
aliases:
  - "synonyme"
domaine: claude-code | gemini | openai | copilot | cursor | xai | technique | industrie
type: feature | changelog | deprecation | best-practice | technique | leader | modele | concurrent | knowledge
derniere-maj: YYYY-MM-DD
auteur: claude
sources:
  - "URL ou [[wikilink]]"
tags:
  - "#type/<type>"
  - "#domaine/<domaine>"
---
```

## Règles

1. **1 concept = 1 note** — atomique, jamais de dump monolithique
2. **Wikilinks** partout — `[[Opus 4.7]]`, `[[Boris Cherny]]`
3. **MOC à jour** — chaque nouvelle note doit être linkée dans son MOC
4. **derniere-maj** — mettre à jour à chaque édition
5. **Ne jamais modifier Templates/** — lecture seule
6. **Vault ≠ mémoire projet** — le vault stocke du savoir référence, pas du feedback/projet

## Gotchas

- **MCP auto-start** — le hook SessionStart lance le MCP automatiquement. Si les outils MCP ne répondent pas, vérifier que `mcp-forge-brain/start.py` existe et que le port 8091 est libre.
- **Écriture via MCP, format via obsidian-markdown** — le MCP gère le transport (create/append/update), la skill obsidian-markdown gère le format (wikilinks, frontmatter, callouts).
- **Aliases minimum 4-6 par note** — standard neoteem-brain : inclure synonymes FR/EN et variantes techniques (ex : "Opus 4.7", "claude-opus-4-7", "opus47", "Claude Opus").

## MCP — accès direct (filet de sécurité)

Tu reçois normalement un brief enrichi de la session principale avec les éléments MCP pertinents déjà extraits (vault, DB, docs). Si pendant l'exécution tu rencontres un doute non couvert par ton brief (terme inconnu, décision technique conflictuelle, pattern incertain, valeur précise non fournie), tu peux re-consulter directement le MCP via `mcp__forge-brain__*`.

**Pas systématique** — la session principale t'a déjà briefé. C'est un filet de sécurité, pas une exploration parallèle. Anti-pattern : scanner par réflexe (coût tokens × N agents).

**Quand l'utiliser** :
- ✅ Terme/acronyme non défini dans le brief
- ✅ Conflit entre 2 approches mentionnées
- ✅ Valeur précise nécessaire (note canonique exacte)
- ❌ Re-vérifier ce que le brief dit clairement
- ❌ "Au cas où" sans déclencheur précis

Source canonique : [[pattern-mcp-brief-then-direct]] vault forge.

## Apprentissage

Après chaque session significative utilisant le vault :
- Vérifier que les notes créées/modifiées sont correctement linkées
- Mettre à jour les MOCs si de nouvelles notes ont été ajoutées
- Si un pattern de recherche revient souvent, créer une note synthèse dans `Knowledge/syntheses/`
- Appliquer le pattern Karpathy 3 temps (SEARCH/SELECT/READ, N=3) : snippets = identification, pas réponse
- Prioriser les outils ciblés (`find_by_property`, `read_section`, `read_note` direct) AVANT `search_brain`
- Pour notes > 50k chars : paginer avec `read_note(offset, limit_chars)` en suivant le header `[suite :]`
