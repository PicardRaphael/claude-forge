---
name: ecrire-partout-invoquer-skill-creatrice
description: Forge écrit dans n'importe quel repo MAIS doit TOUJOURS invoquer la skill créatrice (jamais SKILL.md/agent/hook/CLAUDE.md à la main), même hors forge
metadata:
  type: feedback
---

Formulation Raphael (24 juin 2026) : « tu peux écrire de partout mais toujours respecte la skill à invoquer ». La permission cross-repo TOTALE (write partout) n'autorise PAS le raccourci d'écrire un composant `.claude/` à la main. Composant = SKILL.md, agents/*.md, hooks/*.py, CLAUDE.md → TOUJOURS via skill-creator / subagent-creator / hook-creator / claudemd-creator, quel que soit le repo cible.

**Why:** le hook `delegate-guard.py` de forge ne fire que sur les fichiers SOUS `forge/` (test `is_inside_forge`, l.228-229). Dès que la session forge édite un `.claude/` d'un AUTRE repo (migration_script, ia_back...), aucun garde-fou technique → seule la doctrine reste, et la canonique [[delegate-guard-pattern]] le dit : « les rules advisory ne sont pas respectées sous pression ». Incident 24 juin : 9 SKILL.md écrits à la main dans `neot-v2/migration_script` (repo d'équipe Bitbucket) sans déclencher le guard.

**How to apply:** réflexe pré-écriture — avant tout Write/Edit d'un composant `.claude/`, se demander « est-ce un SKILL.md/agent/hook/CLAUDE.md ? » → si oui, invoquer la skill créatrice AVANT, même hors forge. C'est un engagement de COMPORTEMENT (Raphael ne veut pas durcir le hook : le guard forge ne fire que sous forge/, et on ne livre pas de hook bloquant à un repo d'équipe). La discipline tient la couverture que le hook n'a pas. Subtilité repo d'équipe : la skill créatrice doit produire du contenu auto-portant (pas de wikilinks vault ni refs MCP forge-brain), cf [[config-repo-equipe-vs-forge]].

**Récidive 25 juin 2026 (audit migration_script) :** 2e occurrence — Edit direct sur le CLAUDE.md de migration_script (2 libellés de table) avant de me reprendre vers `claudemd-creator`. Édit cosmétique et conforme, mais le réflexe pré-écriture n'a PAS tenu sous le flux « petite modif ». Le déclencheur est toujours le même : une modif jugée « triviale » court-circuite la question « est-ce un composant .claude protégé ? ». Par la doctrine [[feedback-reviole-3x-regle-insuffisante]], 2/3 vers le seuil « règle insuffisante → garde-fou structurel ». À la 3e, envisager un réflexe pré-Edit explicite plutôt qu'une énième note.
