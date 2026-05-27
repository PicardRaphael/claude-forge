---
name: doctrine-drift-silent-regression
description: "Doctrine encodée dans rules mais annulée silencieusement par MEMORY/RECAP non purgés. Solution = méthode canonique [[methode-pivoter-doctrine]] (checklist 5 étapes), PAS un hook palliatif"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4934145e-38d9-4979-8bde-a6fca1222063
---

# Doctrine drift — régression silencieuse via MEMORY/RECAP non purgés

## La règle

Quand la doctrine pivote (ex: 22 mai 2026 "doctrine vs enforcement"), il NE SUFFIT PAS de mettre à jour les rules. Il FAUT AUSSI purger `MEMORY.md` + `.claude/RECAP.md` + `.claude/agent-memory/*/MEMORY.md` des phrases verbatim contredisant la nouvelle doctrine.

**Sans cette purge** : la session principale recharge la doctrine pré-pivot à chaque démarrage et le travail doctrinal est invisiblement annulé.

**Why** : Bug découvert session 2026-05-22 sur neo_ia. La doctrine "Claude decides when to invoke" était dans les rules. MAIS `MEMORY.md` contenait `pipeline-enforcement` ("TOUJOURS architect → dev → test-writer → code-reviewer → commit") et `no-direct-coding` ("Session principale = CTO, ne code JAMAIS directement. Hooks architect-guard et commit-guard bloquent."). `RECAP.md` décrivait le pipeline pré-pivot avec phase REFACTOR. Résultat : doctrine 22 mai annulée à chaque session pendant ~10 jours.

**How to apply** : à chaque pivot doctrinal majeur, appliquer la **méthode canonique** [[methode-pivoter-doctrine]] (checklist 5 étapes), pas un hook palliatif.

## Pourquoi PAS un hook

Tentation initiale : créer `doctrine-drift-guard.py` SessionStart qui scanne MEMORY/RECAP pour phrases-signal. **REFUSÉ par DA** (cf [[critique-2026-05-22-doctrine-drift-guard]]) :

1. **Signal-to-noise = 0 par construction** : la doc correcte du pivot mentionne TOUJOURS l'ancienne doctrine pour la déclarer obsolète → le hook punit la documentation correcte. Test empirique : 26/26 faux positifs sur neo_ia post-purge.
2. **Mauvaise forme** : pivot doctrinal = événement one-shot (~1×/trimestre). Hook permanent au SessionStart = mauvais outil.
3. **Self-violation doctrine 22 mai** : "hooks = lint/security/scope, JAMAIS workflow". Mécaniser conformité doctrinale = workflow hook abstrait. Isomorphe à `architect-guard` (supprimé 22 mai).

## La vraie solution — checklist 5 étapes

Voir note canonique [[methode-pivoter-doctrine]] (vault forge-brain) :

1. Note canonique vault à jour
2. Rules du repo mises à jour (frontmatter `description:` présent)
3. CLAUDE.md repo (racine + secondaires) avec STOP bloc <ligne 25 si critique
4. **PURGE MEMORY.md + .claude/RECAP.md + .claude/agent-memory/*/MEMORY.md** ⚠️ étape la plus oubliée
5. Test session fraîche pour valider que l'ancienne doctrine n'est plus chargée

## Pattern à mémoriser (méta)

**Avant d'écrire un hook substring/regex** : grep les patterns sur les fichiers cibles AVANT de coder. Si le grep matche la documentation canonique de ce que le hook protège, le hook est mal conçu. Pattern symétrique à `feedback_da_failure_options` mais en amont.

## Pattern récurrent — 3 incidents en 3 jours (22-23 mai 2026)

**Incident 1 (22 mai)** : pivot doctrinal hooks workflow → MEMORY.md neo_ia non purgé → doctrine 22 mai annulée silencieusement pendant ~10 jours.

**Incident 2 (23 mai matin)** : audit thématique vault Claude Code → 22 claims fausses détectées dont **MOC-Claude-Code** + **MOC-Leaders** contenaient encore "Angela Jiang advisor 5×" malgré que les notes canoniques aient été réécrites le 22 mai. Cause : la propagation vers les MOCs n'a pas été faite à l'étape 4 de methode-pivoter-doctrine. Découvert pendant cet audit, corrigé via commit `4aee799`.

**Incident 3 (23 mai après-midi)** : audit forge dogfooding → 11 drifts factuels supplémentaires dans CLAUDE.md, vault/index.md, .claude/skills/cc-hooks-ref/SKILL.md, .claude/agents/hook-creator.md, ia_back. Pattern identique : canoniques OK, propagation aval pas resynchronisée.

→ **Le pattern n'est PAS une exception, c'est une régularité.** Skill `/pivot-check` v1 draftée pour automatiser détection (4 fixes DA pending avant activation).

## Méta-leçon

La **propagation** est l'étape qui dérive systématiquement. La doctrine canonique est facile à mettre à jour (1-N notes). **Tous les composants qui citent cette doctrine** (MOCs, CLAUDE.md, skills cc-*, agents, mémoire forge, vault d'autres repos) sont l'angle mort. Sans check automatisé, il faut un audit dogfooding pour les détecter — ce qui prend ~3h par incident.

**Investissement justifié** : automatiser via `/pivot-check` ou équivalent. Coût ~2h dev pour gagner ~3h × N pivots futurs.

## Liens

- [[methode-pivoter-doctrine]] — solution canonique (vault)
- [[critique-2026-05-22-doctrine-drift-guard]] — DA qui a refusé l'approche hook
- [[critique-2026-05-23-skill-pivot-check]] — DA sur skill /pivot-check (verdict GO-WITH-FIXES)
- [[raisonnement-22mai-doctrine-vs-enforcement]] — doctrine 22 mai
- [[erreur-22-claims-fausses-vault-claude-code-2026-05-23]] — Incident 2 (audit thématique)
- [[feedback_recurring_meta_anti_pattern]] — anti-pattern Jarvis (1 incident → refonte structurelle = NON, mais 3 incidents = pattern)
- [[enforce-not-advise]] — quand promouvoir rule → hook (critères que ce hook NE remplissait PAS)
- [[feedback_audit_thematique_methode]] — méthode validée audit sub-agents par cluster
