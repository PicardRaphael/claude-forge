---
titre: Critique - Audit consolide neo_ia 22 mai 2026
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-22
auteur: claude
aliases:
  - critique audit neo_ia 22 mai
  - da rapport audit consolide neoia
  - verdict revise audit neo_ia
  - critique 4 project-auditor neo_ia
  - audit miss postgres password mcp optional
tags:
  - #type/critique
  - #projet/neo_ia
  - #domaine/claude-code
  - #technique/audit
resume: DA audit consolide neo_ia. 3 bloquants manques dont 1 securite critique (password Postgres en clair commit ffb5963). VERDICT REVISE.
---

# Critique - Audit consolide neo_ia 22 mai 2026

## 🔴 BLOQUANT SECU CONFIRME (manque MAJEUR des 4 auditeurs)

> NOTE : note rétroactivement nettoyée le 2026-05-27 (audit Mémoire Portable). Secret réel (mdp PostgreSQL prod + IP serveur) remplacé par `[REDACTED]`. Le constat de sécurité reste valide. Rotation du mdp = seul fix réel, suivie dans [[todo-rotation-password-postgres-prod]].

Fichier `.mcp.json.postgres-optional` commit `ffb5963` versionne :
- Password Postgres en clair : `[REDACTED]@[REDACTED]:5432/test`
- TLS verification desactivee : `NODE_TLS_REJECT_UNAUTHORIZED=0`
- Paths vers certs `.crt/.key` dans ia_back

Match exact feedback memoire `secret-in-mcp-json-never`. Auto-mode classifier signalerait.

**Action immediate** : 
1. Rotate le password sur l'instance PostgreSQL prod (IP [REDACTED])
2. `git rm --cached .mcp.json.postgres-optional` + `.gitignore`
3. `git filter-repo` ou BFG pour purger l'historique
4. Migrer vers env vars : `${POSTGRES_PASSWORD}` dans le template

## Manques auditeurs

Les 4 project-auditor n'ont audite QUE `.claude/` — ils ont rate :
- `.mcp.json` + `.mcp.json.postgres-optional` (racine repo)
- `.architect-marker` qui trainait en racine .claude/
- `conftest.py` autouse global (feedback `workaround-becomes-sediment`)
- `coverage_final.json` 432k a la racine

## Verdict

REVISE — audit consolide doit etre repris avec scope elargi a la racine repo, pas juste `.claude/`.
