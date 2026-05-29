---
name: doctrine-drift-silent-regression
description: "Doctrine encodée dans rules mais annulée silencieusement par MEMORY/RECAP non purgés. Solution = méthode canonique [[methode-pivoter-doctrine]] (checklist 5 étapes), PAS un hook palliatif"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4934145e-38d9-4979-8bde-a6fca1222063
---

# Doctrine drift — régression silencieuse via MEMORY/RECAP non purgés

Cf [[methode-pivoter-doctrine]] (doctrine : checklist 5 étapes pour pivoter une doctrine sans laisser de résidus textuels MEMORY/RECAP/agent-memory qui réactivent l'ancienne doctrine — purge = étape 4 critique ; refus argumenté du hook palliatif ; pattern « grep avant hook substring »). L'incident origine 22 mai neo_ia est l'EXEMPLE CONCRET de cette note canonique.

## Cas empirique(s) — pattern récurrent, 3 incidents en 3 jours (22-23 mai 2026)

- **Incident 1 (22 mai)** : pivot doctrinal hooks workflow → `MEMORY.md` neo_ia non purgé (contenait `pipeline-enforcement` « TOUJOURS architect → dev → test-writer → code-reviewer → commit » et `no-direct-coding ») + `RECAP.md` avec phase REFACTOR → doctrine 22 mai annulée silencieusement pendant ~10 jours, détectée seulement par l'audit profond 10-agents.
- **Incident 2 (23 mai matin)** : audit thématique vault Claude Code → 22 claims fausses détectées, dont **MOC-Claude-Code** + **MOC-Leaders** contenaient encore « Angela Jiang advisor 5× » malgré la réécriture des notes canoniques le 22 mai. Cause : propagation vers les MOCs non faite à l'étape 4. Corrigé via commit `4aee799`.
- **Incident 3 (23 mai après-midi)** : audit forge dogfooding → 11 drifts factuels supplémentaires dans CLAUDE.md, vault/index.md, `.claude/skills/cc-hooks-ref/SKILL.md`, `.claude/agents/hook-creator.md`, ia_back. Pattern identique : canoniques OK, propagation aval pas resynchronisée.

→ **Le pattern n'est PAS une exception, c'est une régularité.** Skill `/pivot-check` v1 draftée pour automatiser la détection (4 fixes DA pending avant activation).

## Méta-leçon empirique

La **propagation** est l'étape qui dérive systématiquement. La doctrine canonique est facile à mettre à jour (1-N notes). **Tous les composants qui la citent** (MOCs, CLAUDE.md, skills cc-*, agents, mémoire forge, vault d'autres repos) sont l'angle mort. Sans check automatisé, il faut un audit dogfooding pour les détecter — coût mesuré ~3h par incident. **Investissement justifié** : automatiser via `/pivot-check`, ~2h dev pour gagner ~3h × N pivots futurs.

## Liens

- [[methode-pivoter-doctrine]] — solution canonique (vault)
- [[critique-2026-05-22-doctrine-drift-guard]] — DA qui a refusé l'approche hook
- [[critique-2026-05-23-skill-pivot-check]] — DA sur skill /pivot-check (verdict GO-WITH-FIXES)
- [[raisonnement-22mai-doctrine-vs-enforcement]] — doctrine 22 mai
- [[erreur-22-claims-fausses-vault-claude-code-2026-05-23]] — Incident 2 (audit thématique)
- [[feedback_recurring_meta_anti_pattern]] — anti-pattern Jarvis (1 incident → refonte structurelle = NON, mais 3 incidents = pattern)
- [[enforce-not-advise]] — quand promouvoir rule → hook (critères que ce hook NE remplissait PAS)
- [[feedback_audit_thematique_methode]] — méthode validée audit sub-agents par cluster
