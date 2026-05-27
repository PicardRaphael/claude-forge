---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-05-27
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Mémoire portable FAIT (architecture @import validée empiriquement — 231 lignes MEMORY.md chargé depuis `<repo>/memory/`, 5 composants adaptés, doctrine 4-contextes capitalisée, double-source transitoire acceptée). Suivant = DA sur A1×A3 (compounding rétroactif) en session dédiée.

## Dernière session (2026-05-27)
### Décisions prises
- Résolution de path par contexte (4 mécanismes) : skill = `$(git rev-parse --show-toplevel)`, hook = `__file__`, settings command = `${CLAUDE_PROJECT_DIR}` (expansion harness), .mcp.json = paths relatifs. `${CLAUDE_PROJECT_DIR}` vide en skill, non garanti en hook → vérifié empiriquement.
- Hook `session-reminder.py` : `__file__` choisi (pas `os.environ`, pas `git rev-parse`) — déterministe, robuste au cwd (testé depuis /tmp).
- Double-source transitoire (auto-memory native + @import) acceptée comme dette tracée. Désactivation native = TODO différé (déclencheur : pollution contexte problématique ou avant communication externe studio).
- Comportement /done pendant transition = écrit UNIQUEMENT dans `<repo>/memory/` (pas dans les deux).

### En cours
Rien en cours. Étapes 7-9 livrées (NON commitées — Raphael décide granularité/ordre/push). 244 tests verts (101 hooks + 143 MCP), 0 régression. Test cross-machine probant (clone C:\temp\forge-test lit sa propre mémoire).

### Prochaines étapes
- **DA sur A1×A3 (compounding rétroactif)** en session dédiée `/clear` : chercher dans les transcripts (A1) les apprentissages jamais capitalisés et les proposer (A3). Risque faux positifs + coût LLM scan rétroactif. Détail [[idee-compounding-retroactif]].
- TODO différé : désactiver l'auto-memory native pour single-source (clé settings global, hard-block classifier → modif manuelle).
- A2 (skill skills-lifecycle, P2) si le besoin se confirme.

## Fils ouverts
- **Double-source mémoire transitoire** : auto-memory native (`~/.claude/projects/`) encore injectée en parallèle de l'@import. Dette tracée, désactivation différée. Cf [[import-ajoute-pas-remplace-automemory]].
- Détection contradictions vault (extension lint_vault, gap léger Hermes `contradict`) — non priorisé.
- HERMES_ARCHITECTURE.md reste dans C:\temp\hermes-audit\ (artefact local, non versionné).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[phase-4-comparaison-hermes-roadmap]]
[[ajouter-source-donnees-mcp-forge-brain]]
