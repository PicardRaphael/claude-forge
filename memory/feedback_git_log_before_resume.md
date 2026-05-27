---
name: git-log-before-resume
description: "Avant de \"finir/reprendre\" tâche audit/chantier, TOUJOURS git log --oneline -10 d'abord. Commit avec message qui matche = travail déjà fait"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4403f197-2d1a-42ea-b19e-8bb88a8b1a30
---

# git log AVANT reprise de tâche d'audit/chantier

Quand Raphael dit "finis l'audit X" ou "reprends le chantier Y", la première action DOIT être `git log --oneline -10` AVANT de lire les plans/outputs.

**Why:** Session 24 mai — Raphael dit "finis l'audit dogfooding". J'ai lu le plan d'audit (`08-claude-forge-dogfooding.md`) + le rapport (`RAPPORT-FINAL-V2.md`) avant de vérifier git. L'audit était DÉJÀ commité (`7b9f46c` du 23 mai "audit-dogfooding-23mai: forge respecte sa propre doctrine canonique vault") + 3 commits suivants (polish, /done, ajouts vault). Risque évité de justesse : relancer un audit terminé, écraser des décisions validées.

**How to apply:**
1. User dit "finis X" / "reprends Y" / "où en est Z" → `git log --oneline -10` EN PREMIER
2. Chercher message commit qui matche le sujet (audit-X, X-final, chantier-Y)
3. Si match → lire le commit ET le rapport final pour confirmer scope avant toute action
4. Si pas de match → procéder à la reprise normalement
5. Vérifier aussi `git status` pour distinguer working tree state vs commits

Anti-pattern : lire un plan d'audit de 340 lignes avant de vérifier qu'il a déjà été exécuté.

## Wikilinks
- [[feedback_stop_over_verifying]] (cousin : verdict direct si travail fait dans la session, mais ici travail fait dans session précédente — check git log = équivalent rapide)
