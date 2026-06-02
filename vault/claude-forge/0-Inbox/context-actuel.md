---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-02
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Veille IA (cc-news) + maintenance doctrine forge. Date de référence cc-news à jour : 2 juin 2026, CC v2.1.160. EN PARALLÈLE, chantier non clos : déploiement automatisation triage tickets support LOJII chez Valérie (voir section dédiée plus bas).

## Dernière session (2026-06-02) — Veille cc-news
### Décisions prises
- Ne PAS créer de hook/skill "prompt-improver" — déjà tranché par [[prompt-rewriter-pattern]] + violerait pivot 22 mai. Confirmé Raphael.
- Tri source-primaire strict sur sweep cc-news global : 0 note doctrinale créée, uniquement 1 note INFO à-vérifier. Advisor a bloqué une dérive (capitaliser des résumés WebSearch d'aggregateurs).
- Ne rien toucher aux emphases des rules : à la mesure, densité conforme à la doctrine (1-2/fichier). Sur-vendu un non-problème → corrigé.
- Skill cc-news enrichie : nouvelle étape 7 « confronter chaque finding majeur à l'existant » (notes vault + composants .claude/), gate humaine. Feedback Raphael [[feedback_ccnews_confronter_existant]].

### Prochaines étapes (veille)
- Re-vérifier [[split-credit-programmatique-15-juin-2026]] APRÈS le 15 juin (confirmer/poser montants, ou supprimer).
- Grep `.claude/` si un setup attend « workflow » comme mot-déclencheur (renommé `ultracode` en v2.1.160, cf reference mémoire workflow-ultracode-keyword).

## Chantier en cours (non clos) — Déploiement support LOJII chez Valérie (2026-06-01)
### État
- Serveur MCP mcp-obsidian-brain = 2 transports : stdio (défaut Desktop/Chat) + HTTP (`--http`, Claude Code/VM). Commit `cb06072`.
- Valérie passe par Claude Code (dans l'app Desktop), PAS Cowork (MCP local localhost KO en VM cloud Cowork). Config stdio command/args.
- Plugins brain v3.0.4 : ne plus afficher les sources (croisement interne gardé). Commit `63053b5`.
- CLAUDE.md project : Règle n°1 (mode SUPPORT par défaut) + Règle n°2 (relire support-memory/learnings.md avant toute réponse).
- Livrables : `output/support-lojii-plugin-v3/` (4 zips v3.0.4 + CLAUDE.md + fiches install MCP).

### Reste à faire chez Valérie
- `git pull` mcp-obsidian-brain (server.py stdio) + config command/args + redémarrer.
- Vérifier `claude mcp list` → "Connected".
- Tester relecture learnings (Règle n°2) + langage support (pas dev) + pas de sources affichées.

## Fils ouverts
- /schedule re-vérif split-crédit le 16 juin — proposé, non tranché par Raphael.
- Si Règle n°2 (relecture learnings) insuffisante → envisager hook injection learnings.md.
- Bug Desktop Tasks (MCP parfois non chargé) → workaround "utilise un sub-agent".
- Passage VM (futur) : rebrancher HTTPS central, supprimer MCP local, Cowork entreprise. Cf [[automatisation-triage-tickets-support-suivi]].

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[automatisation-triage-tickets-support-suivi]]
[[mcp-local-cowork-vs-claude-code]]
[[cowork-write-vault-headless-impossible]]
