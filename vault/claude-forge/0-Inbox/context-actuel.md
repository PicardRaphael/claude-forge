---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-06
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---
## Phase actuelle
Refonte du CLAUDE.md de Marie-Laure (PO Neoteem) livrée dans `Downloads`. CLAUDE.md recentré 100% rôle PO : suppression de toute la mécanique dev Go (build/test/linter/docker/archi/code style), description réécrite (espace de travail PO, pas monorepo Go), skills `spec`/`maquette` rendus obligatoires, Jira passé en MCP-first, section mémoire + plugins brain ajoutés, Role Convention PostgreSQL conservée verbatim.

## Dernière session (2026-06-06)
### Décisions prises
- **CLAUDE.md PO ≠ CLAUDE.md dev** : pour une utilisatrice non-dev, virer tout le dev (test "would removing cause mistakes?" appliqué) et recentrer sur son rôle réel (tickets, specs, maquettes).
- **Routing skills obligatoire via CLAUDE.md** : `spec` pour tout ticket, `maquette` pour toute maquette — formulation "TOUJOURS utiliser le skill X". Application directe de [[claude-desktop-preferences]] (routing par skill pour non-dev).
- **Jira MCP-first** : MCP d'abord (Atlassian officiel CRUD + MCP NEOTEEM interne JSM, complémentaires), acli en fallback uniquement.
- **5 lignes Karpathy adaptées** (pas verbatim) car CLAUDE.md hors gouvernance forge + utilisatrice non-dev.
- **Mémoire Marie-Laure = Auto-Memory native + CLAUDE.local.md** (repo partagé → jamais de mémoire versionnée pour éviter la pollution croisée).

### En cours
- Rien d'inachevé. Livrable remis. Capitalisation vault faite au fil de l'eau (tour précédent : [[plugin-vs-skill-anatomie]] + CHANGELOG 2026-06-06 sur mémoire Code Desktop = CLI).

### Prochaines étapes
- 2 points en attente de validation Raphael : (1) Projects Structure mise en générique — à réintégrer si le dossier de Marie-Laure contient réellement le repo `ws` ; (2) nom exact du skill `maquette` à confirmer.

## Fils ouverts
- Tri `reference_`/`project_` mémoire → vault si besoin de descendre le corpus (non urgent, décision de fond).
- V2 `align-vault-skills` si faux positifs récurrents (2e agent validateur) — toujours ouvert.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[plugin-vs-skill-anatomie]]
[[claude-desktop-preferences]]
