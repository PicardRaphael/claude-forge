---
titre: "Erreur — Modification majeure de skill sans checklist check-before-create"
resume: "Session du 2026-05-07 : modification lourde de triage-tickets sans lire memoire, vault, references ni charger cc-skills-ref. Anti-pattern recurrent."
aliases:
  - "skip checklist skill"
  - "modification sans verification"
  - "je sais deja"
type: knowledge
derniere-maj: 2026-05-07
auteur: claude
sources:
  - "[[Best practices Boris Thariq]]"
tags:
  - "#type/knowledge"
  - "#domaine/claude-code"
  - "#erreur"
---

## Contexte

Session du 2026-05-07, modification de la skill `triage-tickets` (plugin support-lojii). Ajout de Phase C (retrospective), etape COMPRENDRE (lexique), format learnings enrichi, causes racines, enrichissement lexique automatique.

Modification substantielle (~150 lignes ajoutees) sur plusieurs heures.

## Ce qui s'est passe

Aucune etape du checklist `check-before-create` executee :
1. Memoire (MEMORY.md) — PAS lu. Les feedbacks `feedback_skill_*`, `feedback_use_skill_creator`, `feedback_major_mistakes` existaient mais non consultes.
2. Forge Brain — PAS interroge. `04-Techniques/`, `Knowledge/erreurs/`, `07-Prompts/` non consultes.
3. References existantes — PAS lu. Les `references/` de la skill non consultees avant modification.
4. Skill forge (cc-skills-ref) — PAS chargee.
5. SKILL.md a depasse 500 lignes sans reaction — deporter dans references/ suggere par l'utilisateur, pas par moi.

## Pourquoi c'est une erreur

- Anti-pattern "je sais deja" — documente dans `check-before-create.md` comme erreur recurente (2026-04-26)
- Les feedbacks memoire auraient rappele : `feedback_use_skill_creator` (toujours deleguer), `feedback_skill_structure` (dossier complet), `feedback_read_references_first` (lire references AVANT)
- Le vault aurait montre les best practices skills (progressive disclosure, < 500 lignes)
- Le fichier a depasse la limite sans alerte proactive

## Quoi faire a la place

1. TOUJOURS executer le checklist, meme si "c'est juste un ajout"
2. Verifier la taille du SKILL.md APRES chaque modification
3. Si > 430 lignes → proposer proactivement d'extraire dans references/
4. Ne pas attendre que l'utilisateur signale le probleme

## Liens

- `check-before-create.md` — rule qui definit le checklist
- `feedback_major_mistakes.md` — erreurs recurrentes
- `feedback_proactive_references.md` — feedback cree suite a cette erreur
- `feedback_checklist_before_modify.md` — feedback cree suite a cette erreur
