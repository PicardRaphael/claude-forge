---
name: vault-query-pair-hooks
description: DEPRECATED 2026-05-22 — paire tracker+guard supprimee (anti-pattern workflow gate per doctrine 22 mai). Conserve a titre historique.
type: project
deprecated: 2026-05-22
---

**STATUT : DEPRECATED — hooks supprimes le 22 mai 2026.**

Raison : la paire `vault-query-tracker.py` + `vault-query-guard.py` etait un workflow gate (bloque Write si marker absent). La doctrine 22 mai 2026 reserve les hooks a lint/test/security ; cf [[raisonnement-22mai-doctrine-vs-enforcement]]. Le couple a ete supprime au meme titre que `architect-guard`, `commit-guard`, `dispatch-guard`.

Conserve a titre historique pour les hook-creator qui auditeraient des repos plus anciens.

---

## Description historique (2026-05-06 -> 2026-05-22)

Deux hooks complementaires :

- `vault-query-tracker.py` (PostToolUse Read|Grep|Glob|Skill) — ecrit un marker ISO timestamp dans `.claude/.session-vault-queried` si le tool cible vault/, memory/, Knowledge/, forge-brain, 04-Techniques/, 07-Prompts/.
- `vault-query-guard.py` (PreToolUse Write) — bloque avec exit 2 tout Write vers vault/, output/, .claude/skills/, .claude/agents/ si le marker etait absent ou > 60 min.

**Why historique :** les advisory rules (check-before-create, forge-brain-proactive) avaient un taux d'echec documente. Failure #8 dans feedback_major_mistakes.

**Cause du retrait :** sur-enforcement workflow != lint/security. Voir doctrine 22 mai.
