---
titre: "Décision — garder learning-reminder (exception assumée doctrine 22 mai)"
resume: "Le hook Stop learning-reminder force un comportement (rappel de capitalisation) via decision:block+once:true, ce que la doctrine 22 mai interdit. Gardé volontairement comme filet de sécurité car Raphael n'exécute pas /done de façon fiable. proactivity-reminder, lui, est supprimé."
aliases:
  - "garder learning-reminder"
  - "exception doctrine 22 mai learning-reminder"
  - "Stop hook learning-reminder décision"
  - "proactivity-reminder supprimé"
domaine: claude-code
type: decision
derniere-maj: 2026-05-29
auteur: claude
tags:
  - "#type/decision"
  - "#domaine/claude-code"
  - "#doctrine/2026"
---

# Décision — garder learning-reminder (exception assumée doctrine 22 mai)

## Contexte

Audit `.claude/` multi-repo (29 mai 2026, pilote Dynamic Workflows) flague 2 Stop hooks forge comme drift doctrinal :
- `learning-reminder.py` — rappelle en fin de session de capitaliser les apprentissages
- `proactivity-reminder.py` — force une proposition Jarvis au tour 5

Discriminateur appliqué (validé advisor) : **blocking pour forcer un comportement** (`decision:block` / exit 2) = enforcement workflow = drift 22 mai. **advisory** (`additionalContext` / exit 0) = acceptable.

## Le point technique décisif

L'event **Stop ne supporte PAS `additionalContext`** (cf [[feedback_stop_hook_injection]]). Le seul moyen de surfacer du texte au Stop est `decision:block + reason + once:true` — exactement ce que ces hooks font déjà. Donc « convertir en advisory » est **infaisable** pour un Stop hook. Le choix se réduit à : **garder** (once:true = mécanisme légitime) vs **supprimer**.

## Décision

| Hook | Décision | Raison |
|------|----------|--------|
| `proactivity-reminder.py` | **SUPPRIMÉ** | Valeur faible, pur behavior-shaping (force une proposition au tour 5), zéro payoff démontré. Aucun cas d'utilité pour surpasser la doctrine. |
| `learning-reminder.py` | **GARDÉ** (exception assumée) | Filet de sécurité réel : Raphael confirme ne PAS exécuter `/done` de façon fiable. Le hook a capturé 2 feedbacks réels dans la session du 29 mai. C'est un override utilité-sur-doctrine, pris **en connaissance de cause**, pas un déni de drift. |

## Pourquoi c'est une exception cohérente

La doctrine 22 mai = doctrine-over-case-by-case-utility. Garder learning-reminder est une dérogation explicite, justifiée par un fait empirique (`/done` non fiable → le filet compense). Si un jour `/done` devient systématique (ou est lui-même hooké), learning-reminder deviendra pure redondance → le supprimer à ce moment.

Son jumeau structurel `devil-advocate-stop` avait été supprimé au pivot 22 mai — la différence ici est l'utilité démontrée + l'absence d'alternative advisory sur l'event Stop.

## Liens

- [[raisonnement-22mai-doctrine-vs-enforcement]] — doctrine hooks = lint/security/scope
- [[feedback_stop_hook_injection]] — Stop ne supporte pas additionalContext
- [[devils-advocate-pipeline]] — le sibling devil-advocate-stop supprimé au pivot
