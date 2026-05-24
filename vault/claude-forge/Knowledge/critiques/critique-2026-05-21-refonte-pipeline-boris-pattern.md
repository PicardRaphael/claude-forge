---
titre: "Critique — Refonte pipeline agentic ia_back + neo_ia (Boris pattern)"
resume: "4 bloquants : Plan Mode CC sans trace persistante, classifier path+LOC avec faux-negatifs, chaine marker cassee sans remplacement, liste fichiers critiques incomplete. Reproduit pattern advisory deja documente comme defaillant 3 fois (~80% compliance)."
aliases:
  - critique refonte pipeline boris
  - critique architect-guard suppression
  - DA plan-mode-classifier neo_ia ia_back
  - devil advocate boris pattern transposable
  - critique pipeline agentic mai 2026
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-24
auteur: devils-advocate
tags:
  - "#type/knowledge"
  - "#type/critique"
  - "#projet/ia-back"
  - "#projet/neo-ia"
  - "#domaine/claude-code"
  - "#technique/hooks"
sources:
  - "Session 2026-05-21 — proposition refonte pipeline Boris pattern"
  - "Recherche web Boris Cherny Plan Mode 2026"
---

## Verdict

**LIVRER AVEC CORRECTIONS** — 4 bloquants, 5 avertissements, 3 nitpicks. La direction (sortir de l'architect-first gate hard) est defendable, mais le DESIGN reproduit 2 antipatterns du vault.

## 4 Bloquants

### 1. Plan Mode CC ne laisse pas de trace persistante verifiable par hook
ExitPlanMode est interactif cote UI. Aucune API documentee n'expose "un plan a eu lieu" a un hook PreToolUse. Consequence : classifier dit "ce diff exige un plan" → user accepte cote terminal → Edit lance → classifier voit Edit, ignore si Plan Mode est passe. Retombe en advisory (80% compliance).

### 2. Seuil "> 50 LOC OU > 1 fichier" a des faux-negatifs structurels
- 30 LOC dans `tool_selector.py` casse OATS
- 1 ligne change ordre middlewares = bug auth invisible
- Renommage methode dans 1 fichier propage silencieusement
- LOC sous-estime portee semantique, 1-fichier sous-estime impact
Ratio attendu : ~30-40% des incidents previsibles passent sous le seuil.

### 3. Chaine marker cassee sans remplacement persistant
Retirer architect-guard sans poser marker equivalent brise la chaine `architect-marker → dev → code-reviewer-marker → commit`. `commit-guard` continue de tourner sans condition amont. Audit necessaire de tous hooks lisant `.architect-marker` : commit-guard, marker-protect, agent-marker-writer, pipeline-reset, session-reset-markers.

### 4. Liste fichiers critiques incomplete au regard du vault
Manque (deja incidents documentes) : `apps/*/agents/`, `packages/shared/`, `app/main.py`, `app/api/*.py`, fichiers `*Selector*`, `*Router*`, `*Dispatcher*`, lockfiles, `apps/*/conftest.py` (pas seulement racine).

## Pattern advisory deja documente defaillant

Le point 6 (agent architect "opt-in") reproduit exactement le pattern documente dans [[erreur-advisory-rules-insuffisantes]] : 3 incidents avril-mai 2026, dont incident neo_ia (7 mai) ou Raphael lui-meme (Lead IA) a skippe les rules "OBLIGATOIRE". Si le Lead skip, le junior skip plus.

## Chemin recommande

1. **Garder le pattern marker+guard, changer le nom et le scope.** Remplacer `architect-marker` par `plan-marker`. Marker pose via slash command `/plan-validated` ou hook PostToolUse sur ExitPlanMode si CC l'expose.
2. **Calibrer classifier sur semantique + path, pas juste path+LOC.** Inclure la liste etendue (agents, libs cross-app, API contracts, *Selector*, *Router*).
3. **Diagnostic moins radical possible.** Le vrai cout pointe par Raphael ("architect tourne 100 ans") peut etre (a) scope GUARDED_PREFIXES trop large — corrige en 4 lignes par hook, ou (b) prompt architect Opus trop verbose sur taille S — mode `--fast-pass` mini-plan 3 lignes.
4. **Un seul mode pour tous, pas de differentiation Raphael vs collegues.** Bypass invisible cote collegue + asymetrie de feedback. Friction asymetrique correcte = `/plan-validated` 1 commande.
5. **Code-reviewer post-commit trop tard.** Compromis : PostToolUse sur fenetre de N writes ou exit 2 dur sur commit (pas warning).
6. **Tests adverses obligatoires AVANT deploiement.** Precedent direct [[erreur-tests-heureux-vs-adverses]] : classifier qui remplace toute la defense amont = barre validation plus haute, pas plus basse.

## Pattern transposable Boris → Neoteem

Boris solo + expert + session interactive. Neoteem 2-3 devs + sub-agents + sessions paralleles. Cas qui cassent :
- Sub-agent qui tourne sans humain = qui accepte Plan Mode ?
- Junior ne rattrape pas en review mental = besoin gate dur
- Raphael Lead IA doit garantir qualite envers equipe = filet = SA garantie

## Liens

- [[erreur-advisory-rules-insuffisantes]] — pattern advisory 80% vs hook 100%, 3 incidents chiffres
- [[raisonnement-22mai-doctrine-vs-enforcement]] — diagnostic historique du blocage marker = TTL, pas existence
- [[raisonnement-22mai-doctrine-vs-enforcement]] — bug scope du 21 mai, fix = 4 lignes pas suppression
- [[critique-2026-05-21-outcomes-test-deploy]] — meme pattern parite forcee multi-repo critique hier
- [[critique-2026-05-13-setup-lojii]] — precedent parite forcee
- [[erreur-tests-heureux-vs-adverses]] — 8 tests PASS sur cas heureux ne valident PAS securite
- [[feedback_enforce_not_advise]] — advisory 80% → hook 100% immediatement
- [[feedback_workaround_sediment]] — autouse global devient dette permanente
- [[feedback_devlead_vs_devapp]] — cross-app modifs critiques
- markers-pipeline-must-be-complete — concept obsolète post-pivot 22 mai, voir [[raisonnement-22mai-doctrine-vs-enforcement]]
- hooks-enforcement-pattern — concept obsolète post-pivot 22 mai, voir [[raisonnement-22mai-doctrine-vs-enforcement]]
