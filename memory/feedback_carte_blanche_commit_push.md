---
name: carte-blanche-commit-push-tranche-pas-revalider
description: "Quand Raphael dit \"carte blanche jusqu'au commit/push\" — exécuter directement sans re-valider note par note, advisor uniquement si bloqueur réel"
trigger: carte blanche, jusqu au commit, valide, fais tout, go
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8fa91757-f7b7-4aca-8e12-6bce6d8e70c2
---

**Verbatim Raphael** (23 mai 2026, audit thème 06) :
> "Tu t'arrête jamais jusqu'a ce que tu commit push tu as carte blanche si tu as des question demande advisor et devil si vraiment besoin"

## La règle

Sur un chantier long (audit massif, refonte structurelle, propagation cross-files), si Raphael dit "carte blanche" / "tu as carte blanche" / "vas-y" / "à toi de voir" :

1. **NE PAS s'arrêter** pour demander validation note par note ou vague par vague
2. **NE PAS multiplier les advisor()** pour confirmer ce qui est déjà clair
3. **Exécuter direct** : phase B → C → D → E → F → commit → push d'un seul flux
4. advisor() / devils-advocate **uniquement si bloqueur réel** (incohérence détectée, décision ambiguë non résolvable seul)

**Why** : Raphael délègue pour gagner du temps. Multiplier les checkpoints = perdre son temps = anti-pattern. Les advisors successifs sur chantier validé = anti-pattern `feedback_couper_loops_decision_fatigue`.

**How to apply** :
- Reconnaître les signaux "carte blanche" : "tu as carte blanche", "vas-y", "à toi", "trance", "go"
- Si plan validé et méthode validée (cf `feedback_audit_thematique_methode`) → exécuter directement
- Garder advisor() pour : bloqueur conceptuel, ambiguïté méthodologique nouvelle, décision destructive non-évidente
- **Carte blanche couvre le bulk non-structurel ; elle ne dispense PAS du DA sur le sous-ensemble structurel** (KILL hook/skill, retrait d'outil touchant un claim sécu, refonte d'enforcement, suppression de composant). Ces cas restent OUI-DA même sous carte blanche — cf `.claude/rules/devils-advocate-pipeline.md` (« le LIVRABLE déclenche, pas l'activité »)
- Rapport final intermédiaire OK et utile, mais sans demander validation à chaque étape
- En fin de chantier : 1 rapport global + `/done` pour capitalisation

## Lien

- [[feedback_couper_loops_decision_fatigue]] — couper loops après validation + pas multiplier options en session longue
- [[feedback_never_pure_executor]] — Jarvis actif même sur prompts directifs (proposer si meilleur)
