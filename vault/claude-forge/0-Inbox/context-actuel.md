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
Audit transverse conformité doctrinale claude-forge TERMINÉ — 78 composants audités (11 agents, 47 skills, 9 hooks, 10 rules, CLAUDE.md), 5 résidus corrigés (94% conformes d'emblée). 244 tests verts. 6 commits poussés sur main (5 audit + 1 résidu fermé). /done effectué (1 feedback méta nouveau). Suivant = **régénération SELF_PORTRAIT** (session fraîche après /clear).

## Dernière session (2026-05-27)
### Décisions prises
- **Audit transverse 9 critères** (mémoire, path resolution, dépendances fragiles, meta-commentaire, frontmatter↔body, doctrine, code mort, wikilinks, chemins portables). Méthode A→B→C→D→E avec STOP étape D. Cartographie exhaustive : grep patterns suspects + passage du hook `meta-commentary-detector` en scan sur tout son scope (oracle de classification) + pyflakes hooks + croisement wikilinks ⨯ existence vault MCP.
- **5 non-conformités corrigées** (toutes triviales, déléguées) : `agent-creator.md:17` wikilink mort `[[agents-orchestration]]`→`[[agents-architecture]]` ; `responsable-ia.md:8` `color: pink`→`purple` (pink réservé méta-créateurs) ; `notes/SKILL.md:12` `Source :`→`Référence :` (attribution-source) ; `mcp-brief-then-direct/SKILL.md:70` retrait `(validé 26 mai 2026)` ; `mcp-autostart.py:6-7` imports orphelins `json`/`os`.
- **Cas ambigus tranchés = garder** : `cc-features-ref:95` (`~/.claude/projects/` = doc feature native CC, fait exact) ; `tip #1` dans `cc-*-ref` (skills documentaires, hook les exempte) ; `(Boris)`/`(Anthropic)` parenthèses ≤3 mots (tolérées doctrine + hook).
- **Délégation forcée respectée** : skill-creator pour les 2 SKILL.md + cross-dispatch sur les 2 agents (self-mod agent-creator), hook-creator pour le hook. Vérif grep/hook/pyflakes empirique post chaque dispatch.
- **/done — pattern méta capitalisé** : re-violation 3× du feedback `mcp-alias-ambigu-chemin-exact` (`append_note` par alias → mauvais fichier `log.md`). Nouveau feedback [[feedback-reviole-3x-regle-insuffisante]] : feedback re-violé ≥3× = la règle écrite ne suffit pas, formuler un réflexe pré-action ou un garde-fou hook (candidat : garde scope sur `append_note(stem multi-dossier)`).

### En cours
Rien. 5 corrections appliquées et vérifiées, 244 tests verts. **Pas de commit lancé** (Raphael décide du découpage).

### Prochaines étapes
- **Régénérer le SELF_PORTRAIT** (proposition Jarvis — l'audit a confirmé le setup propre, base saine pour le portrait).
- Commits de l'audit (5 fichiers : 2 agents, 2 skills, 1 hook + memory feedback + MEMORY.md + context-actuel + CHANGELOG + log).
- Valider empiriquement le pivot `/recall-uncaptured` si l'intuition se présente.
- TODO différé : désactiver l'auto-memory native pour single-source (clé settings global, hard-block classifier → modif manuelle).

## Fils ouverts
- **Double-source mémoire transitoire** : auto-memory native (`~/.claude/projects/`) encore injectée en parallèle de l'@import. Dette tracée, désactivation différée. Cf [[import-ajoute-pas-remplace-automemory]].
- **A1×A3 tué** : ne pas réouvrir le scan rétroactif systématique sans nouvelle donnée infirmant le 0/12. Cf [[idee-compounding-retroactif]] (statut TUÉE).
- Détection contradictions vault (extension lint_vault, gap léger Hermes `contradict`) — non priorisé.
- HERMES_ARCHITECTURE.md reste dans C:\temp\hermes-audit\ (artefact local, non versionné).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[resolution-path-3-contextes]]
[[erreur-meta-commentaires-composants]]
[[critique-2026-05-27-compounding-retroactif]]
