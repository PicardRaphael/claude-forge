---
titre: "Idée — workflow inbox capture-vrac → tri auto (dormant dans forge, à réactiver si flux entrant)"
resume: "Capture de l'idée Eliott Meunier d'une inbox alimentée en vrac puis triée automatiquement dans projets/casquettes. Diagnostic : dormant dans forge faute de flux entrant (on crée déjà en chemin direct via create_note). À implémenter le jour où un vrai flux entrant existe (capture mobile, résumés réunion, veille auto)."
aliases:
  - "workflow inbox capture vrac"
  - "inbox processor forge"
  - "tri automatique inbox IPCRA"
  - "flux entrant vault"
type: idee
domaine: claude-code
status: idee
derniere-maj: 2026-06-27
auteur: claude
tags:
  - "#type/idee"
  - "#domaine/claude-code"
sources:
  - "https://www.youtube.com/watch?v=IubQUC9TL2w (Eliott Meunier — Second Cerveau IA)"
---

## L'idée (Eliott Meunier)

Tout ce qui entre (notes à la volée, **résumés de réunion**, captures) atterrit dans `0-Inbox/`. Puis, chaque semaine, un **processeur d'inbox** (`/inbox` chez lui) relit le dossier, applique l'arbre IPCRA (projet ? casquette ? ressource ? archive ?), **déplace** chaque note au bon endroit et **met à jour la note de contexte** du projet concerné. Gain annoncé : ~1 h/semaine.

## Pourquoi c'est dormant dans forge (diagnostic 27 juin)

Vérifié dans le réel (`list_notes 0-Inbox` + grep `.claude/`) :

1. **Aucun flux entrant automatique.** Forge n'a pas de capture vrac : quand une note est créée, c'est via `create_note` avec le **chemin précis** (`1-Projets/…`, `Knowledge/…`) → l'inbox est shuntée.
2. **Le tri « par /done » du SCHEMA n'est pas implémenté.** `/done` ne fait que réécrire `0-Inbox/context-actuel.md` ; il ne retrie pas les autres notes → les quelques notes présentes y stagnent (orphelines).
3. Conclusion : l'inbox n'est pas un pattern actif. Une skill `/inbox-processor` serait une **coquille vide** aujourd'hui.

## Condition de viabilité — d'abord un flux entrant

L'inbox-processor n'a de sens que si un **flux entrant** existe vraiment. Pistes pour un jour :
- **Capture mobile / rapide** : Dispatch channel (Telegram/Discord → dépose dans `0-Inbox/`), ou skill de capture éclair.
- **Résumés de réunion** : automatisation n8n (cf [[n8n-self-host-mcp-claude]]) qui dépose un résumé dans l'inbox après chaque call.
- **Veille auto** : rapport quotidien déposé en inbox.

## Si on l'implémente un jour

1. Créer/activer le flux entrant (au moins un).
2. Skill `/inbox-processor` : lit `0-Inbox/`, applique l'arbre IPCRA, `move_note` vers projet/casquette/ressource/archive, met à jour la note de contexte cible. Idempotence : marquer/traiter une seule fois.
3. Décider du trigger : manuel hebdo (slash command) ou `/loop` planifié.

→ Passer par [[cartographier-process-cma]] (fiche process « traiter l'inbox ») puis `loop-forge`.

## Décision

**Dormant assumé.** Ne pas créer la skill tant qu'aucun flux entrant n'existe. Réactiver cette note (la sortir de l'inbox vers une vraie fiche process) le jour où un flux est en place. En attendant, retrier les orphelines actuelles de `0-Inbox/` vers leur vrai dossier.

## Liens

- [[cartographier-process-cma]] — fiche process « traiter l'inbox »
- [[n8n-self-host-mcp-claude]] — flux entrant possible (résumés réunion)
- [[architecture-cerveau-obsidian-mcp]] — structure IPCRA du vault
