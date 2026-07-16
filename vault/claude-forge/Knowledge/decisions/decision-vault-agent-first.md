---
titre: "Décision — vault forge-brain agent-first (Karpathy = échafaudage dépassé)"
resume: "Le vault forge-brain est optimisé pour la boucle agent (Jarvis pilote via MCP/search), pas pour la navigation humaine Obsidian (débranchée). Karpathy était l'échafaudage de départ ; raw/ supprimé, MOCs/index = couche humaine optionnelle non auto-maintenue, SCHEMA à refondre. Pivot à instruire via methode-pivoter-doctrine."
aliases:
  - "vault agent-first"
  - "decision agent-first forge"
  - "Karpathy echafaudage depasse"
  - "cerveau agent vs wiki humain"
  - "pivot vault agent-first"
type: knowledge
derniere-maj: 2026-07-16
auteur: claude
tags:
  - "#type/knowledge"
  - "#domaine/claude-code"
  - "#domaine/patterns"
sources:
  - "[[pattern-vault-llm-karpathy]]"
  - "session 2026-06-27 (audit outillage vault + cours Eliott Meunier)"
---

## Statut : accepté | 2026-06-27

## Contexte
Obsidian est débranché de fait (GUI humaine seule depuis ~30 mai). C'est Jarvis qui lit/écrit le vault via MCP forge-brain ; l'usage réel (`usage_stats`) est dominé par `search_brain` + `read_note`, jamais par la navigation humaine. Le pattern Karpathy (raw/ immuable, index navigable, MOCs, graphe) a été conçu pour un humain qui butine — pas pour un agent. Symptômes mesurés : raw/ mort (8 notes d'un chantier, 0 consommateur), MOCs maintenus par vault-audit mais non lus, `FOLDER_TO_MOC` cassé (dossiers périmés).

## Options envisagées
- Rester fidèle au pattern Karpathy (raw/wiki/schema, MOCs, index navigable).
- Assumer un vault **agent-first** : retirer les couches qui ne servent que l'humain absent, investir dans ce que l'agent consomme.

## Décision
forge-brain = **cerveau d'agent**. On optimise pour la boucle Jarvis (search → read → répondre vite et juste), pas pour la navigation humaine. Karpathy = échafaudage de départ, pas la cible.

## Conséquences
- raw/ supprimé (bruts = variables jetables : distillés puis jetés).
- MOCs + index navigables = couche humaine **optionnelle** : ne plus les auto-maintenir (alléger/retirer la logique `FOLDER_TO_MOC` de vault-audit). Ne PAS les supprimer (~95 backlinks sur MOC-Techniques = dette nette).
- `SCHEMA.md` à refondre : retirer raw/ du Layer 1 immuable, décrire l'état agent-first réel.
- Investir : note de contexte projet vivante (`/done` étape 6-bis), Knowledge compounding, recherche FTS + aliases, doctrine à jour qui ne ment pas.
- Canoniques impactées : [[pattern-vault-llm-karpathy]] (« LLM modifie raw/ = bug fatal » devient caduc), [[architecture-cerveau-obsidian-mcp]], [[SCHEMA]].

## Déclencheur de réactivation
Instruire le pivot via la skill `methode-pivoter-doctrine` en session dédiée : refondre les 3 canoniques ci-dessus sans drift résiduel. Jusque-là, cette décision est la source de vérité sur l'orientation.

## Validation externe — 2026-07-16

Le consensus communautaire de juillet 2026 (retours d'usage 3+ mois du pattern Karpathy, 15 sources croisées) converge exactement sur cette décision : « gouvernance > infrastructure », « la conformité au pattern n'est jamais le critère », vectoriel overkill à cette échelle, « ce qui vit est ce qui est utilisé en boucle ». Détail : [[pattern-vault-llm-karpathy]] section « VAGUE VIRALE JUILLET 2026 ».

**Extension actée le 16 juil. (Raphael)** : le cerveau devient **user-scope machine** — disponible dans toutes les sessions Claude Code de la machine (config `~/.claude.json` user + démarrage au logon), **rien dans les repos** (repos d'équipe). Réponse au diagnostic mesuré « 65 % des sessions hors forge sans MCP, consultation −80 % en un mois » : la boucle agent que cette décision optimise s'étend de « sessions forge » à « toutes les sessions Jarvis ».

## Liens
- [[pattern-vault-llm-karpathy]]
- [[architecture-cerveau-obsidian-mcp]]
- [[cartographier-process-cma]]
