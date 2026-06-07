---
titre: "Limite connue MCP forge-brain — lag de réindexation des agrégats (poll watcher 30s)"
resume: "Les vues agrégées (get_tags, compteurs lint_vault) peuvent diverger transitoirement du disque : le watcher réindexe par poll 30s, et la fluctuation 88/89 du compteur wikilinks brisés est non liée aux edits (prouvé Ch.3). Non codé car sans impact. À traiter seulement si un usage dépend d'un compteur temps-réel."
aliases:
  - "limite lag réindexation MCP"
  - "fluctuation compteur lint_vault"
  - "poll watcher 30s vault"
  - "MCP aggregate reindex lag"
  - "agregat get_tags retard"
  - "chantier 5 limite 4"
type: technique
domaine: claude-code
derniere-maj: 2026-06-07
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/claude-code"
---

## Symptôme

Les vues **agrégées** du MCP (`get_tags`, compteurs `lint_vault`) peuvent **diverger transitoirement** de l'état disque réel. Le watcher réindexe par **poll toutes les 30 s** (`poll_interval_seconds: 30` dans `config.yaml`), donc une écriture juste après un tick n'est reflétée dans les agrégats qu'au tick suivant. Observé : le compteur de wikilinks brisés fluctue (131/132/133 au chantier 2/5, 88/89 au chantier 5) **indépendamment des edits réels**.

Distinct du lag d'écriture hors-MCP (voir feedback mémoire `vault-edit-gotchas-outillage` gotcha #3) : là, c'est un Edit disque qui n'a pas déclenché `index_note` ; ici, c'est la nature **agrégée** des compteurs qui traîne même après réindexation normale. Les accès **directs** (`find_by_property`, `get_property`, `read_note`) reflètent le disque immédiatement — seuls les agrégats globaux traînent.

## Pourquoi non codé (chantier 5)

**Non lié aux edits, prouvé au chantier 3.** Un `git diff --unified=0` filtré démontrait que seules des lignes de tags avaient bougé (0 wikilink touché, 0 frontmatter cassé) alors que le compteur dérivait — donc l'edit ne pouvait pas, par construction, créer ou casser un lien. La fluctuation est un artefact d'agrégat, **sans impact** sur la justesse des opérations. Géré par discipline : **vérifier l'invariant réel par `git diff`, pas par le compteur agrégé** (un compteur en liste tronquée n'est de toute façon pas comparable baseline↔courant). Coder un cache invalidé en temps réel ou un scan forcé après chaque écriture ajouterait de la complexité pour un symptôme cosmétique.

## Déclencheur qui justifierait de coder

Si un **usage dépend d'un compteur agrégé temps-réel** (ex. un hook qui bloque sur « N wikilinks brisés ne doit pas augmenter » entre deux états immédiats, ou un dashboard live). À ce moment : exposer un outil de scan forcé (déclencher `watcher.scan()` à la demande) ou invalider/recalculer l'agrégat en fin d'écriture. Tant que les compteurs servent au diagnostic humain ponctuel (pas à une décision automatique synchrone), inutile.

## Liens

- [[mcp-vault-llm-design]] — doctrine et matrice des outils MCP forge-brain
- [[architecture-cerveau-obsidian-mcp]] — architecture du serveur (watcher poll incrémental)
- [[sqlite-fts5-vault]] — l'index SQLite FTS5 que le watcher alimente
