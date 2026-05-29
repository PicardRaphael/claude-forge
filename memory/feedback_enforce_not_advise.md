---
name: enforce-not-advise
description: "Quand l'advisory est SKIPPÉ (compliance miss), corriger via hook. PAS quand la sur-conformité existe déjà — la sur-enforcement est son propre mode de défaillance. Hooks = lint/security/scope, JAMAIS workflow agentique."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 42f0ff3e-7431-4682-bf0b-f2823840a715
  revised: 2026-05-22
---

Cf [[erreur-hooks-workflow-enforcement]] (doctrine : hook PreToolUse exit 2 forçant architect-first / commit-after-review / délégation au dev = anti-pattern Anthropic ; hooks = lint/security/scope/invariant technique, workflow = doctrine dans rules + session juge). Voir aussi [[raisonnement-22mai-doctrine-vs-enforcement]].

**Cas empirique(s) :**

- Session 22 mai 2026 — refonte ia_back + neo_ia : suppression de 7 hooks workflow nommés (architect-guard, commit-guard, dispatch-guard, marker-protect, agent-marker-writer, pipeline-reset, session-reset-markers) car friction 6× mesurée (Raphael, 21-22 mai) — développer une feature prenait 6× plus de temps.
- Anti-scope (seuil empirique) : si la session respecte DÉJÀ l'advisory (compliance > 80%) ET que le hook proposé forcerait un workflow agentique → NE PAS créer le hook. C'est l'inverse du problème : sur-enforcement génère sa propre friction.
- Si l'advisory workflow est skippé : améliorer description d'agent + rule + gotcha CLAUDE.md, pas créer un hook. Le skip indique souvent une doctrine mal calibrée, pas un manque d'enforcement.
