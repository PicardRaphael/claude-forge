---
titre: Context Actuel
resume: "Working memory dynamique — mis à jour par /done, lu par /recap. Session 2026-05-24 tour 2 : propagation meta-commentary-detector hook sur ia_back (TS) + neo_ia (Python). Regex refiné (Option E lookahead) après DA. Cross-repo guard ajouté."
aliases:
  - "context actuel"
  - "contexte courant"
  - "working memory"
  - "memoire de travail"
  - "etat actuel"
type: context
status: active
derniere-maj: 2026-05-24
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

Hook `meta-commentary-detector` déployé en production sur les 3 repos forge (claude-forge Python, ia_back TS, neo_ia Python uv). Regex Option E (lookahead syntaxique) après DA — autorise backtick/chevron/accolade/bracket simple, bloque texte libre/wikilink/URL.

## Dernière session (2026-05-24 tour 2)

### Décisions prises

- **Option E DA retenue** vs Option A advisor : lookahead syntaxique plus robuste que capitalisation
- **Port TS complet pour ia_back** (~195 L) au lieu de violer `feedback_hooks_same_stack` — stack bun cohérent
- **Cross-repo guard ajouté au hook claude-forge** : `is_inside_forge()` comme delegate-guard.py
- **Self-exclusion ajoutée** : detector + tests dans EXCLUDED_SUFFIXES (anti-catch-22)
- **Audit empirique AVANT propagation** : grep 9 patterns → 2 FP identifiés, regex affiné
- **neo_ia** : copie hook Python + adaptation commande `uv run python` (pas `py`)

### En cours

- **Hook actif en prod sur 3 repos** : claude-forge (Python), ia_back (TS bun), neo_ia (Python uv)
- **Tests** : 21/21 Python, 14/14 TS
- **Audit ia_back + neo_ia** : 0 violation après refinement

### Prochaines étapes

- Tester hook en condition réelle (edit avec `Source : Karpathy` → doit bloquer exit 2)
- Surveiller faux positifs émergents pendant 1-2 semaines
- **Décision à prendre** : trou architectural delegate-guard (sub-agents contournent via Bash). Mini-DA dédié.
- **Proposition Jarvis ouverte** : audit autres hooks claude-forge — grep `SCOPED_PATTERNS` sans `is_inside_forge` pour détecter trous similaires

## Fils ouverts

- **Critique DA `critique-2026-05-24-regex-source-faux-positifs`** : sauvegardée vault via Write fallback (MCP create_note silent fail)
- **MCP forge-brain instable** : `create_note` + `search_brain` ont échoué silencieusement plusieurs fois cette session
- **MEMORY.md à ~25.7 KB** (>limite 24.4) : 3 nouveaux feedback ajoutés. Purge trimestrielle nécessaire.

## Métriques session tour 2

- **3 commits** : `d07f8fa` (claude-forge), `3fb9686` (ia_back), `86dbf4f` (neo_ia)
- **2 nouveaux fichiers hook** : `meta-commentary-detector.ts` (ia_back), `.py` (neo_ia)
- **2 patches successifs sur regex source-label** (capitalisation rejetée → lookahead → bug fix `[ \t]+`)
- **3 nouvelles feedback memory** : `hook_scope_per_repo`, `hook_self_blocking_catch22`, `regex_lookahead_greedy_trap`

## Patterns émergeant cette session

- **Pattern méta hook scope** : tout hook avec scope par chemin DOIT vérifier scope par repo
- **Pattern méta self-blocking** : tout hook qui détecte des patterns DOIT s'auto-exclure
- **Pattern méta regex enforcement** : `\s*` greedy + lookahead = backtrack vicieux. Préférer `[ \t]+`
- **Préférence Raphael confirmée** : "DA + advisor disent quoi ?" sur décisions techniques non-triviales

## Liens

[[Raphael-Picard|Raphael Picard]]
[[Claude-Forge|Claude-Forge]]
[[comment-creer-hook]]
[[erreur-meta-commentaires-composants]]
[[critique-2026-05-24-regex-source-faux-positifs]]
[[critique-2026-05-24-meta-commentaires-doctrine]]
