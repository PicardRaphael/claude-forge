---
titre: "Critique — Plan de modifications audit règles forge (doctrine prompting frontière)"
resume: "DA sur le plan 7 actions issu de l'audit .claude/ du 27 juil : I2 (bump xhigh du DA) BLOQUANT car contredit décision Option C actée + CLAUDE.md live (reviewers=high). Verdict PASS-avec-réserves."
aliases:
  - critique plan audit regles forge 27 juillet
  - critique bump xhigh devils-advocate
  - critique I2 effort reviewers high
  - critique reformulation TDD code-dev
  - DA plan audit doctrine prompting frontiere
domaine: claude-code
type: knowledge
derniere-maj: 2026-07-27
auteur: claude
sources:
  - "[[effort-opus-47-doctrine-anthropic-2026]]"
  - "[[conflit-effort-xhigh-anthropic-vs-pivot-22mai]]"
tags:
  - "#type/critique"
  - "#domaine/claude-code"
---

# Critique — Plan de modifications audit règles forge

## Intention déclarée
Aligner le corpus de règles forge (~92 % déjà conforme) sur la doctrine prompting frontière du fireside Cat Wu × Thariq (« fewer hard constraints, more context ») + fixer un hook fantôme, via 7 actions.

## Verdict
Bloquants : 1 (I2) · Avertissements : 3 (I1, C1, exécutabilité) · Nitpicks : 2 (I3, S1)
Décision : **PASS-avec-réserves** — I2 bloquant à ne PAS appliquer en l'état, reste avance sur ses mérites.

## BLOQUANT — I2 (score 85) : le bump xhigh contredit une décision actée + le CLAUDE.md live
L'audit veut bumper `devils-advocate.md` de `high` → `xhigh` « pour aligner sur la grille canonique ». Or trois autorités disent `high` pour les reviewers, une seule cellule dit xhigh :
- **CLAUDE.md (chargé cette session)** : « `high` pour comparatif structuré (graders, reviewers, designers, conseil) ».
- **Décision Option C, arbitrée Raphael 18 juin** (corps de [[effort-opus-47-doctrine-anthropic-2026]] + [[conflit-effort-xhigh-anthropic-vs-pivot-22mai]] statut résolu) : « `high` = analyse / comparatif / jugement structuré (graders, reviewers, conseil) ; `xhigh` = agentique/coding multi-tool long-horizon (dev, architect, refactor, auditeurs/analyzers) ».
- **memory feedback_allocation_modele_effort** : « xhigh RÉSERVÉ architect/dev-lead/refactor-pg, high ailleurs ».

Contre : une seule cellule du tableau de la même note (Reviewers → xhigh), qui colle xhigh sur presque tout (Créateurs/Analyseurs/Reviewers) — **outlier en drift interne vs le principe nuancé d'Option C qu'il est censé résumer**. Un DA est reviewer-shaped (reçoit un livrable, 1-2 requêtes + jugement structuré), pas auditeur-shaped (exploration agentique multi-tours). Le plan pioche silencieusement la cellule outlier sans mentionner qu'il contredit le CLAUDE.md live → contradiction NON adressée avec décision actée = 80+.
**Fix correct** : ne PAS appliquer I2 sur l'agent. Corriger la CELLULE du tableau `effort-opus-47-doctrine` de `xhigh` → `high` pour la réconcilier avec Option C + CLAUDE.md (canal : édition note vault, pas subagent-creator). Le conflit d'intérêt (agent qui bumpe son propre effort) va dans le sens du rejet : rejeter est le choix désintéressé.

## AVERTISSEMENT — exécutabilité I2 non vérifiée (score 70)
Canal proposé = `subagent-creator`. Mais `mcp-brief-then-direct.md` : « Self-modification forge bloquée : subagent-creator ne peut pas modifier ses propres agents forge. » I2 modifie `devils-advocate.md` → probablement non exécutable via le canal indiqué (edit manuel requis, comme C1). L'audit ne l'a pas relevé. Moot si I2 est rejeté, mais à vérifier pour tout futur edit d'agent forge.

## AVERTISSEMENT — I1 exceptions TDD auto-déclarées non vérifiables (score 55)
Direction juste (l'absolu TDD est non motivé, aucun incident forge — l'audit l'admet). MAIS pour un exécutant Sonnet, une liste d'exceptions (spike/config/UI) + « dis pourquoi tu sautes » est auto-déclarée, aucun hook ne la contrôle. La méthode fireside = *fewer hard constraints, MORE context*, pas un menu d'exceptions ouvert. Resserrer : narrower les exceptions OU exiger la remontée humaine plutôt que l'auto-dispense.

## AVERTISSEMENT — C1 : pousser le RETRAIT, pas la création (score 50)
Le bug = ligne fantôme dans settings.json, pas l'absence de feature Discord. Option (a) créer le hook = dépendance webhook + secret-en-config (memory interdit de le committer) + bruit, pour zéro valeur demandée. Occam : supprimer la ligne. Ne créer que si Raphael veut réellement des notifs — sinon c'est résoudre le mauvais problème.

## NITPICK — I3 / S1 (score 25)
Dedup faible risque. S1 vise une dup dans un tableau de dispatch d'une règle déjà canonique ailleurs et toujours chargée → OK. La redondance de salience CLAUDE.md < ligne 25 est un choix de design réel, mais pas ce que S1 touche. Ne pas gonfler en avertissement.

## Si je devais le faire marcher
1. I2 : rejeter le bump agent ; à la place corriger la cellule tableau → `high`. Le vrai drift est dans le tableau, pas dans l'agent.
2. C1 : retrait de la ligne fantôme par défaut (edit manuel Raphael, settings.json hard block) ; création hook seulement si demande explicite.
3. I1 : resserrer les exceptions ou basculer sur remontée humaine.
4. Vérifier le canal d'exécution de tout edit d'agent forge (self-modification bloquée).
5. S2/S3/S4/I3/S1 : avancent tels quels.

## Angle stratégique méta
Seul vrai risque du plan : transformer « fewer hard constraints » en nouvel absolu. Le plan tient là où chaque règle assouplie manque vraiment d'un incident (I1 = le cas à scruter). Le reste est dedup/typo cohérent.

## Décisions actées confrontées
- Option C effort ([[effort-opus-47-doctrine-anthropic-2026]] + [[conflit-effort-xhigh-anthropic-vs-pivot-22mai]], statut résolu 18 juin) → **contredite NON adressée par I2** → BLOQUANT.
