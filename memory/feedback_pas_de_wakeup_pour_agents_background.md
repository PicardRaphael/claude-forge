---
name: pas-de-wakeup-pour-agents-background
description: Ne JAMAIS programmer un ScheduleWakeup pour attendre mes propres agents background — le harness notifie déjà à leur fin. Wakeup = seulement travail externe non-tracké.
metadata:
  type: feedback
---

Quand je lance des agents en arrière-plan (Agent tool async), le harness me **réveille automatiquement** à leur fin via `<task-notification>`. Programmer en plus un `ScheduleWakeup` « fallback » est **inutile et nuisible** : si l'agent finit normalement, je traite son résultat puis le wakeup se déclenche plus tard sur une tâche déjà faite → relance fantôme périmée (« Reprendre : l'agent a-t-il fini ? » alors que tout est terminé). Observé 3-4× en une session (29 juin 2026), agaçant pour Raphael.

**Why** : le wakeup duplique un signal (la notification de fin) que le harness fournit déjà. Et je n'annulais pas le wakeup en traitant la notification → il survivait, périmé.

**How to apply** :
- Agents background que j'ai lancés → **ne PAS** programmer de ScheduleWakeup. Attendre la `<task-notification>`, c'est tout.
- ScheduleWakeup réservé au travail EXTERNE que le harness ne tracke pas : CI distant, déploiement, file d'attente, état externe à poller.
- Si malgré tout un wakeup est programmé et que la tâche se termine avant : considérer le wakeup comme caduc, ne pas ré-exécuter le travail, ne pas reprogrammer.

Cf comportement /loop dynamique (ScheduleWakeup légitime) vs simple attente d'agents (illégitime).
