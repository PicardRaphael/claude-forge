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
Réparation + refonte de l'automatisation triage tickets support LOJII (Cowork) — v3 livrée, prête pour test poste unique (Valéry).

## Dernière session (2026-06-01)
### Décisions prises
- Architecture support-lojii **v3** : 2 skills (pas de découpage), mémoire d'apprentissage **LOCALE** (`support-memory/`, convention zéro-config), vault en LECTURE seule en batch, écriture vault gardée en `/analyse` interactif.
- Run 7h = **1 seul scheduled** : Phase C (rétro, apprend de la veille) PUIS Phase A (triage).
- JQL rétro corrigée : marqueur = **label `À_valider`**, jamais le texte de note (gras Unicode non cherchable).
- MCP obsidian-brain installé **en local par poste** en attendant la VM. Lanceur portable commité (`mcp-obsidian-brain`, commit `ce00a62` master Bitbucket).
- Suivi projet sauvegardé dans **forge** : [[automatisation-triage-tickets-support-suivi]].

### En cours
- Déploiement v3 sur le poste de Valéry (test à venir avec le collègue support).
- Livrables prêts : `claude-forge/output/support-lojii-plugin-v3/` (4 zips import + prompt 7h + checklists + fiche install MCP).

### Prochaines étapes
- Tester le 1er run réel : la rétro trouve-t-elle des tickets (JQL `À_valider` corrigée, non testée contre Jira) ?
- Vérifier que `support-memory/learnings.md` se remplit après un `/analyse` avec correction.
- Confirmer le branchement MCP HTTP dans Cowork (sinon fallback CLI, non bloquant).

## Fils ouverts
- **Passage VM** (futur) : supprimer MCP local, rebrancher vers serveur central HTTPS, passer au partage Cowork entreprise (Team/Enterprise « Share »), étendre aux 4 agents N1. Checklist dans [[automatisation-triage-tickets-support-suivi]].
- Branchement MCP dans Cowork Desktop : mécanisme exact non confirmé (`mcpServers` vide chez Raphael).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[automatisation-triage-tickets-support-suivi]]
[[cowork-write-vault-headless-impossible]]
