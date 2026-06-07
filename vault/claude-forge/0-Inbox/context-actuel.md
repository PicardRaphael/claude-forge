---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-07
auteur: claude
tags: ["#type/context", "#meta"]
---
## Phase actuelle
Capitalisation de connaissances dans le vault terminée — dossier `Important/` entièrement réconcilié et vidé, doctrine single-source rétablie.

## Dernière session (2026-06-07)
### Décisions prises
- Sous-dossier `04-Techniques/serving/` créé (granularité validée vs stacks/) : serving-inference-optimisation + prompt-caching-kv-cache + reference-technique-stack-ia (déplacée d'Important/).
- Doctrine reference-grade : doc source = référence exhaustive cherchable MCP, notes atomiques = deltas décisionnels seulement.
- Réconciliation `Important/` menée 1 doc à la fois, 1 commit par doc, validation utilisateur par doc.
- Stack IA.md supprimé + 4 sources mortes nettoyées (pas gardé comme archive).

### En cours
- Rien de bloqué. 7 commits poussés sur main (c3a29b7 → 78f21ef). Working tree clean, branche synchro origin.

### Prochaines étapes
- **Chantier 3/5 wikilinks : CLÔTURÉ 7 juin** (133 → 96 liens brisés, −37). 0 lien cassé par ERREUR ; le résidu 96 est sain et expliqué : ~70 roadmap G1 (contenu à écrire), 8 narration CHANGELOG (→ exclusion Ch.5), ~15 placeholders syntaxiques (F). Voir CHANGELOG entrées 2026-06-07.
- Chantier CONTENU futur (roadmap G1 responsable-ia, ~52 cibles distinctes) — les liens s'auto-réparent à mesure que les notes sont écrites.

## Fils ouverts
- Le garde-fou lecture-entière (feedback + rule sequence-canonique renforcée) vient d'être posé — surveiller qu'il tient sur les prochains audits/comparaisons (ne plus juger « doublon/subsumé » sur 30 lignes).
- Les canoniques `comment-creer-hook`/`-agent`/`-skill` ont reçu des sections « AJOUT 7 juin » (deltas vérifiés source primaire) — si elles approchent une taille lourde, envisager déport en references/ à terme.
- **Bug frontmatter — `comment-creer-agent`/`-skill`/`-hook`** : double bloc YAML + BOM en tête (`derniere-maj:` seul, puis `﻿---`) → 0 alias / 0 tag au lint. 3 canoniques majeures. Réparation dédiée (retrait BOM + fusion des 2 blocs). Rejoint la tâche hygiène frontmatter du plan. Manip YAML délicate (le BOM casse le parsing) → session attentive, Obsidian fermé, séparée de toute autre écriture — PAS un coup de fin de journée.
- **Exclusion `CHANGELOG.md` du lint** (Chantier 5, limite MCP #6) : les 8 derniers liens « narration » du lint sont des noms morts re-mentionnés dans le CHANGELOG (le lint parse les `[[]]` même entre backticks, cf gotcha `mcp-vault-llm-design`). Fix = exclure `CHANGELOG.md` du scan comme `raw/`/`log.md`. DEV MCP, pas en chantier d'usage.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
