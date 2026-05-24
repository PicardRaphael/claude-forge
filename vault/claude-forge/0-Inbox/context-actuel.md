---
titre: Context Actuel
resume: "Working memory dynamique — mis à jour par /done, lu par /recap. Session 2026-05-25 : audit + nettoyage vault (297→5 brisés), MCP forge-brain v1.0→v1.3 (8 outils LLM-optim, 69 tests pytest), skill + rule synchronisées."
aliases:
  - "context actuel"
  - "contexte courant"
  - "working memory"
  - "memoire de travail"
  - "etat actuel"
type: context
status: active
derniere-maj: 2026-05-25
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

MCP forge-brain v1.3 livré et documenté. Vault forge-brain assaini (348 notes, 5 wikilinks brisés résiduels = faux positifs). Pattern canonique [[mcp-vault-llm-design]] créé pour recréer un MCP vault LLM-optimisé chez quelqu'un d'autre.

## Dernière session (2026-05-25)

### Décisions prises

- **MCP v1.3 ship sans attendre usage_stats** : convergence 80%+ "game-changer" (cas d'usage observés cette session sur bulk_update, read_section, embeds) → ship avec tests adverses rigoureux. Cf [[feedback_80_percent_confidence_ship]].
- **8 outils MCP ajoutés** : delete_note, move_note (atomique + rewriting), lint_vault, usage_stats, find_by_property, bulk_update_property, read_section, read_note_resolved
- **Skip features Obsidian humaines** : graph view, Templater UI, Excalidraw, obsidian-cli (viole doctrine MCP-only). Advisor a cadré.
- **21 notes supprimées** (vs archivées) : `_chantier-22mai/` (12), fiches `Agent — X` doc obsolètes (7), snapshots datés (2). Décision Raphael : "session pivot depuis 21/05 = repart de 0".
- **Inversions canonique/doublon** : Harrison Chase (rag canonique), Ethan Mollick (prompt canonique).
- **Single-source-of-truth** : skill + rule mis à jour, 8 agents NON touchés (héritent via `skills:[forge-brain]`).

### En cours

- **MCP v1.3 prod-ready** : 69 tests pytest pass, 2 moves prod réels validés (sans rename + avec rename + 3 backlinks réécrits sans perte), pagination CHANGELOG OK, logging usage actif depuis v1.2.
- **Vault forge-brain assaini** : 348 notes (-20 du début), 5 brisés résiduels (vs 297 initial = -98%), 0 orpheline, 0 YAML cassé.
- **Note canonique [[mcp-vault-llm-design]]** : recette complète pour recréer un MCP vault LLM (9 ops, 7 défenses critiques, anti-patterns, métriques v1.3).

### Prochaines étapes

- **Mesurer usage_stats(days=7)** dans 1 semaine pour décisions pruning outils MCP (DA-recommandation)
- **Proposition Jarvis ouverte** : appliquer même chantier MCP sur `neoteem-brain` (mêmes limites probables avant v1.3 forge)
- Si une note est référencée 0 fois après 30j → candidate suppression future
- Embed resolution profondeur 2+ à mesurer (risque explosion contexte)
- Pattern read_section pour CHANGELOG/log automatiquement préféré par LLM = à observer

## Fils ouverts

- **`_META-GENERATOR.md`** (07-Prompts/analyse/) : Raphael a dit "je le fais après" — exécution méta-prompt génération bibliothèque ~25 prompts pending
- **5 brisés vault résiduels** : faux positifs structurels (exemples syntaxiques, notes pas créées, addy-osmani.md fichier inexistant flag par lint) — acceptables
- **CLAUDE.md modifié hors session** : version downgrade (3.2 sans suffixe) + suppression refs Karpathy raisonnement-22mai + claim doctrine. Restauré par git checkout cette session mais re-modifié par autre process (hook meta-commentary-detector.py orphelin observé). À investiguer prochaine session.
- **Anthropic $900B négociation** (Bloomberg 12 mai) : deal non finalisé, à actualiser
- **Boris Cherny $1B ARR** Claude Code (déc 2025 → $2.5B fév 2026 → $2B+ mai 2026)

## Métriques session

- **15 commits push** sur main (vault cleanup, MCP v1.1→v1.3, skill, rule)
- **MCP** : 11 → 19 tools, 0 → 69 tests, 0 → 4 tests adverses critiques (self-link/embed/case/code-blocks)
- **Vault** : 368 → 348 notes (-20), 297 → 5 wikilinks brisés (-98%), 0 orpheline, 0 YAML cassé
- **2 moves prod** réussis : question-idor-coproprietes (sans rename) + claude-mythos-preview (rename kebab + 3 backlinks réécrits)

## Liens

[[Raphael-Picard|Raphael Picard]]
[[Claude-Forge|Claude-Forge]]
[[mcp-vault-llm-design]]
[[pattern-vault-llm-karpathy]]
[[methode-pivoter-doctrine]]
