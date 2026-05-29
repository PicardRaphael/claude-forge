---
name: workflow-spec-forge-jira-tickets
description: "Workflow Neoteem validé 26 mai — Idée → forge (challenge) → /spec dans repo cible → forge (génère tickets Jira) → équipe. Spec = vérité technique, Jira = process."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: df277af9-47f3-4793-8326-bf2e183d5f4a
---

Cf [[pattern-spec-driven-development]] (doctrine : SDD interview→SPEC→execute, workflows Thariq/Boris/Anthropic, architecture /spec Neoteem tailles M/L/XL, pipeline /spec→/decompose→/go, déploiement).

**Cas empirique(s) :**

- **2026-05-26, `feature-jira-ticket-from-neochat`** : validation empirique du pont forge ↔ Jira ↔ équipe (PAS dans le vault). Découpage des rôles : Spec/BRIEF = source de vérité technique (versionnée Git, lue par Claude Code via routing) ; Jira ticket = source de vérité process (qui, deadline, blockers, KPI, retro) ; Forge (Jarvis) = pont + challenge qualité + génère les tickets (mère + sous-tickets, KPI dans Jira, Gherkin COPIÉ du BRIEF). Boucle : idée → forge challenge → /spec repo cible → retour forge (challenge + ajouts Langfuse/sécu IA/KPI) → forge génère tickets → Raphael copie dans Jira + colle liens Bitbucket → implémentation Claude Code → /go (STOP) → test manuel → /ship. BRIEF enrichi 4 sections (Gherkin DANS le BRIEF = source unique, recherche préalable, refs, comment vérifier) + sécu IA + Langfuse + décisions assignées.
- **2026-05-27, SPEC NON SYSTÉMATIQUE (décision)** : grosse feature (multi-repo, >5 fichiers, beaucoup de décisions, branches/cas) → /spec OBLIGATOIRE ; petit truc (tient en 1 phrase claire) → ticket Jira direct SANS spec, l'architect produit les contrats testables à la volée.
- **2026-05-27, split /go ≠ /ship** : /go vérifie (typecheck + tests + review + changelog) puis STOP ; /ship commit+push quand Raphael décide. Checkpoint humain entre les deux.
- **2026-05-27, décisions outillage** : Pas de skill /dev — le routing (agent-delegation ia_back / agent-routing neo_ia) orchestre déjà. `architect-quick` = skill `architect-sanity-check` (PAS un agent), mode S de architect-deep pour léger. Nettoyage dette architect-quick appliqué sur les 2 repos.

Lien : [[feedback_lire_canoniques_avant_audit]], [[erreur-vault-jamais-consulte-session-principale]], [[feedback_spec_trous_structurels_a_checker]].
