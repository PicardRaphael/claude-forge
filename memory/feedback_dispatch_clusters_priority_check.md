---
name: dispatch-clusters-priority-check-mandatory
description: "Avant dispatch sub-agents par cluster, cross-check ENTRE clusters dispatched ET claims PRIORITÉ HAUTE listées dans inventaire — risque oublier un cluster même si claim haute priorité dedans."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9d187182-be69-4f77-822a-84b8ce7a1e5c
---

**Règle** : Lors d'un audit thématique avec sub-agents dispatched par cluster, AVANT de lancer les sub-agents, faire un cross-check explicite : "chaque claim PRIORITÉ HAUTE listée dans inventaire est-elle couverte par un cluster dispatched ?". Si non → ajouter un sub-agent rattrapage AVANT, pas après.

**Why** : Audit fine-tuning 23 mai 2026. C6.11 JudgeBench (ICLR 2025) listé en PRIORITÉ HAUTE dans `A-inventaire-claims.md`. Cluster 6 (Datasets+Evaluation) silencieusement skippé lors du dispatch des 6 sub-agents. Advisor a détecté l'oubli en Phase C ("tu vas livrer un audit avec 2 notes sur 10 non-vérifiées"). Rattrapage possible mais friction inutile.

**How to apply** :
- Phase A doit produire l'inventaire AVEC une section "Claims PRIORITÉ HAUTE" explicite (déjà le cas)
- Phase B doit débuter par un mapping cross-check : "claim haute prio → cluster qui la couvre"
- Si une claim haute prio n'est dans AUCUN cluster dispatched → ajouter cluster ou la rattacher à un cluster existant
- Pour les audits suivants (prompt engineering, context engineering, etc.) : intégrer ce cross-check dans le template phase B

**Sister rules** : [[verify-exhaustive-claims]], [[audit-thematique-claims-vault]]
