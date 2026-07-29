---
name: org-blocks-github-cloud
description: Org "Claude IA" blocks GitHub access — remote triggers need admin approval. Use local Task Scheduler instead.
trigger: github, remote trigger, cloud, task scheduler, org
type: feedback
originSessionId: b8821289-a77e-4c03-9a03-e61d32124156
---
L'orga Team "Claude IA" bloque l'acces GitHub pour les utilisateurs non-admin. Les triggers cloud (/schedule) ne fonctionnent pas car ils ont besoin de GitHub pour cloner/push.

**Why:** Raphael est "Utilisateur" dans l'orga, pas proprietaire. L'admin doit installer l'app Claude GitHub sur l'orga.

**How to apply:**
- Ne PAS proposer de triggers cloud (/schedule) — ils ne marcheront pas
- Utiliser **Task Scheduler Windows** pour toute automatisation (brain sync, news check)
- Le trigger `trig_0187SwpsFoJ57NiSYfgKxWkE` (cc-news-check) est DESACTIVE, pas supprime — reactiver si l'admin connecte GitHub
- Si l'admin connecte GitHub un jour, migrer les taches locales vers des triggers cloud
