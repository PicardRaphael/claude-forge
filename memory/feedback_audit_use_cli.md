---
name: audit-use-cli-validation
description: Auditer un repo .claude/ avec la CLI (claude agents/skills/hooks/rules list), pas juste en lisant les fichiers
type: feedback
originSessionId: b3529a11-dcf4-49f9-aa3d-d8b5e7bdabc2
---
Toujours valider un audit de setup .claude/ avec les commandes CLI :
- `claude agents list` — confirme detection, model, memory
- `claude skills list` — confirme skills visibles et groupees
- `claude hooks list` — confirme hooks actifs dans settings.json
- `claude rules list` — confirme rules chargees avec descriptions

**Why:** Lire les fichiers bruts ne garantit pas que Claude Code les detecte. Un fichier peut exister mais avoir un frontmatter invalide, un name incorrect, ou etre dans le mauvais dossier. La CLI est la source de verite.

**How to apply:** Apres toute modification de .claude/ (agents, skills, rules, hooks), lancer les commandes CLI depuis le repo cible (`cd <repo> && claude <component> list`) pour confirmer.
