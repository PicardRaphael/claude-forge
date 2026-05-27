---
name: workflow-spec-forge-jira-tickets
description: "Workflow Neoteem validé 26 mai — Idée → forge (challenge) → /spec dans repo cible → forge (génère tickets Jira) → équipe. Spec = vérité technique, Jira = process."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: df277af9-47f3-4793-8326-bf2e183d5f4a
---

Workflow Spec-Driven Development Neoteem validé empiriquement 2026-05-26 sur `feature-jira-ticket-from-neochat`.

**Why :** Raphael cherchait le bon workflow Responsable IA — qui consomme la spec ? Claude Code ? Équipe via Jira ? Réponse pragmatique testée et validée.

**How to apply :**

```
1. Idée / besoin → discussion forge (Jarvis challenge, trouve trous)
2. Idée claire → /spec dans repo cible (ia_back OU neo_ia)
   → produit TODO/feature-X/SPEC.md + BRIEFs (Gherkin DANS le BRIEF = source unique)
3. Retour vers forge → challenge spec, propose ajouts (Langfuse, sécu IA, KPI)
4. Forge GÉNÈRE les tickets Jira (mère + sous-tickets) — KPI dans Jira, Gherkin COPIÉ du BRIEF
5. Raphael copie tickets dans Jira + colle liens Bitbucket vers spec
6. IMPLÉMENTATION (Claude Code dans repo cible) : "implémente TODO/feature-X/BRIEF.md"
   → routing auto : architect (explore repo réel) → test-writer (tests depuis Gherkin) → dev/dev-{app} → code-reviewer
7. /go (typecheck + tests + review + changelog, STOP) → test manuel Raphael → /ship (commit + push)
```

SPEC NON SYSTÉMATIQUE (décidé 27 mai) :
- Grosse feature (multi-repo, >5 fichiers, beaucoup de décisions) → /spec OBLIGATOIRE
- Petit truc (tient en 1 phrase claire) → ticket Jira direct SANS spec, l'architect produit les contrats testables à la volée
- Règle : si la feature a des branches/cas/multi-repo → /spec. Sinon ticket direct.

Découpage des rôles :
- **Spec/BRIEF** = source de vérité technique (versionnée Git, lue par Claude Code via routing)
- **Jira ticket** = source de vérité process (qui, deadline, blockers, KPI, retro)
- **Forge (Jarvis)** = pont + challenge qualité + génère les tickets
- **/go ≠ /ship** : /go vérifie (STOP), /ship commit+push quand Raphael décide. Checkpoint humain.
- **Pas de skill /dev** : le routing (agent-delegation ia_back / agent-routing neo_ia) orchestre déjà.
- **architect-quick = skill architect-sanity-check** (PAS un agent). Mode S de architect-deep pour léger.

Validé sur feature-jira-ticket-from-neochat. BRIEF enrichi 4 sections (Gherkin, recherche préalable, refs, comment vérifier) + sécu IA + Langfuse + décisions assignées. Split go/ship + nettoyage dette architect-quick sur les 2 repos (27 mai).

Lien : [[feedback_lire_canoniques_avant_audit]], [[feedback_session_consulte_vault_avant_brief]], [[feedback_spec_trous_structurels_a_checker]].
