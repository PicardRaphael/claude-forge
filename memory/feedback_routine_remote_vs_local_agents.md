---
name: routine-remote-cloud-pas-acces-local-agents
description: "Routines /schedule = cloud Anthropic, PAS d'accès à ~/.claude/agents/ user-scope local ni vault local. Inutile pour invoquer Agent Teams locale. Préférer skill manuelle (/forge-review) ou Task Scheduler Windows."
metadata: 
  node_type: memory
  type: reference
  originSessionId: a4e196c9-ffac-4668-a189-2e0902c13357
---

Erreur évitée 26 mai 2026 : j'allais créer une routine `/schedule` mensuelle pour relancer Agent Team `forge-audit-doctrines` avec les 3 user-scope auditors. **Faux**.

**Why** : Routines remote tournent dans le cloud Anthropic (CCR sandbox isolé), avec son propre git checkout. Ne voit PAS :
- `~/.claude/agents/` user-scope local (will/ecc/boris-auditor)
- Vault forge-brain local
- MCP locaux non déclarés dans la routine
- Tout fichier hors du repo GitHub checkouté

**Conséquence** : impossible de spawn une Agent Team locale avec teammates qui n'existent que sur la machine Raphael.

**Cumul de problèmes** :
1. Claude GitHub App pas installé sur le repo → routine ne peut même pas accéder
2. Doublon avec skill `/forge-review` (review stratégique mensuelle existante)
3. Feedback existant `org-blocks-github` : "Orga Team bloque GitHub, tout en local Task Scheduler"
4. Capitalisation Day 0 → mesurer drift mensuel sans 2+ usages = no signal

**How to apply** :
1. **Pour réévaluation drift doctrinal** : utiliser `/forge-review` manuel quand drift suspecté, PAS cron remote
2. **Pour Agent Team réutilisable** : invoquer manuellement *"Crée une agent team avec will-auditor, ecc-auditor, boris-auditor"* depuis n'importe quel repo local
3. **Routines remote = TÂCHES AUTONOMES** : check repo PRs, lint scheduled, deploy monitoring — pas orchestration locale
4. **Critère de décision routine remote** : "ce que ferait la routine peut-il fonctionner avec UNIQUEMENT git checkout du repo + MCP connecté ?" Si non → skill locale ou Task Scheduler

**Anti-pattern observé** : proposer routine sans vérifier dépendances locales (agents user-scope, vault, MCP non-connecté).

Liens : [[org-blocks-github]], [[skills-user-scope-pas-cross-repo]], [[audit-tripartite-doctrinal-pattern]]
