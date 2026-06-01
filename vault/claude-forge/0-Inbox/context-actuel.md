---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-01
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Déploiement de l'automatisation triage tickets support LOJII sur le poste de Valérie — résolution des questions de transport MCP (Cowork vs Claude Code) et de comportement (mode support, sources, relecture mémoire).

## Dernière session (2026-06-01, suite)
### Décisions prises
- **Serveur MCP = 2 transports** : stdio (défaut, Claude Desktop/Chat via command+args) + HTTP (`--http`, Claude Code/VM). Commit `cb06072` sur repo mcp-obsidian-brain.
- **Valérie passe par Claude Code (dans l'app Desktop)**, PAS Cowork — car MCP local localhost ne marche pas en Cowork (VM cloud). Sa config `command`/`args` (stdio) marche maintenant que le serveur fait du stdio.
- **Plugins brain v3.0.4** : ne plus afficher les sources dans la réponse (croisement interne gardé). Commit `63053b5` sur repo neoteem-brain.
- **CLAUDE.md project** : Règle n°1 (mode SUPPORT par défaut, dev en coulisse) + Règle n°2 (relire support-memory/learnings.md AVANT toute réponse, même chat libre).
- Référence plugins = `neoteem-brain/plugin/` ; `output/plugins-brain/` = copie miroir (sens source→copie only).

### En cours
- Test du déploiement chez Valérie : import skills/plugins, config MCP stdio, CLAUDE.md project.
- Livrables à jour dans `output/support-lojii-plugin-v3/` (4 zips v3.0.4 + CLAUDE.md + fiches install MCP).

### Prochaines étapes
- Valérie : `git pull` mcp-obsidian-brain (récupérer server.py stdio) + garder config command/args + redémarrer.
- Vérifier `claude mcp list` → "Connected" (pas juste "running").
- Tester : reposer une question déjà corrigée → l'IA doit relire learnings et appliquer (Règle n°2).
- Vérifier réponses en langage support (pas dev) et sans sources affichées.

## Fils ouverts
- Si la Règle n°2 (relecture learnings) ne suffit pas en pratique → envisager un hook qui injecte learnings.md à chaque message (plus lourd, seulement si besoin).
- Bug Desktop Tasks (MCP parfois non chargé) → workaround prompt "utilise un sub-agent".
- Passage VM (futur) : rebrancher HTTPS central, supprimer MCP local, partage Cowork entreprise. Cf [[automatisation-triage-tickets-support-suivi]].

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[automatisation-triage-tickets-support-suivi]]
[[mcp-local-cowork-vs-claude-code]]
[[cowork-write-vault-headless-impossible]]
