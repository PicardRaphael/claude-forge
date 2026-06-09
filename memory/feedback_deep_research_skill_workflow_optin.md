---
name: deep-research-skill-workflow-optin
description: La skill forge deep-research est un harness Workflow — nécessite opt-in explicite, sinon basculer sur WebSearch/WebFetch manuels
metadata:
  type: feedback
---

La skill `deep-research` (invocable forge) n'est PAS une skill d'exécution directe : c'est un **harness Workflow** (fan-out d'agents). L'invoquer via le Skill tool renvoie une instruction `Workflow({ name: "deep-research", args: ... })` — et le tool Workflow exige un **opt-in explicite** de l'utilisateur (mot-clé `ultracode`, demande directe « use a workflow », ou ultracode session-on). « Recherches ultra poussées / prends ton temps » NE compte PAS comme opt-in (règle stricte du tool Workflow).

**Pourquoi :** un Workflow peut spawner des dizaines d'agents et brûler beaucoup de tokens — l'utilisateur doit l'avoir demandé, pas l'avoir inféré. Observé 9 juin 2026 (dossier MCP) : `deep-research` invoquée pour une recherche multi-axes, renvoyée comme appel Workflow non-déclenchable → bascule sur WebSearch + WebFetch parallèles en main-loop (sanctionné, contrôle de la vérification gardé).

**Comment l'appliquer :** pour une recherche poussée SANS opt-in Workflow explicite → faire les WebSearch/WebFetch en parallèle soi-même (sources primaires d'abord, vérifier les claims actionnables sur doc primaire). N'invoquer `deep-research` que si l'utilisateur a explicitement opté pour l'orchestration multi-agents. Cf [[llm-deep-research-version-numbers-hallucinated]] (qualité du contenu) et [[workflow-ultracode-keyword]] (déclencheur Workflow).
