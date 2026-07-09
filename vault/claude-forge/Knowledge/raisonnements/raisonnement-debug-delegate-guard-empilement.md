---
titre: "Raisonnement — debug du delegate-guard face aux skills empilées (9 juil. 2026)"
resume: "Chaîne de diagnostic complète d'un hook de détection qui bloque à tort : debug log → lecture du code → double cause (fenêtre 15 lignes + estampille figée sur la première skill du tour) → blocage classifier self-modification → inspection du transcript réel → fix .proposed appliqué manuellement → 39/39 + validation en conditions réelles."
aliases:
  - "debug delegate-guard empilement"
  - "raisonnement hook attribution skills"
  - "diagnostic hook detection transcript"
  - "attributionSkill stacking debug"
  - "fix delegate guard 9 juillet"
type: raisonnement
derniere-maj: 2026-07-09
auteur: claude
sources:
  - "Session 2026-07-09 — chantier forge-review fusions (commits fb0163→739fb04)"
  - "Debug log delegate-guard + transcript session inspecté ligne à ligne"
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
  - "#domaine/hooks"
---
# Raisonnement — debug du delegate-guard face aux skills empilées

## Problème initial

Batch de 21 édits SKILL.md sous skill-creator : 11 passent, puis blocages `attributionSkill: None`. Plus tard, dans un tour ouvert par forge-review : blocages `attributionSkill: 'forge-review'` alors que skill-creator venait d'être invoquée.

## Chemin de diagnostic (l'ordre a compté)

1. **Ne pas contourner, comprendre** : lecture du debug log du hook (`delegate-guard-debug.log`) → les blocages montrent la valeur d'attribution VUE par le hook, pas celle attendue.
2. **Lire le code du hook** (les lectures ne sont jamais bloquées) → deux constats : `TRANSCRIPT_TAIL = 15` (fenêtre de scan) et « retourne le premier attributionSkill trouvé en remontant ».
3. **Double cause identifiée** :
   - *Expiration* : un batch de ~8+ édits pousse le tampon hors de la fenêtre de 15 lignes.
   - *Empilement (CC ≥ 2.1.202)* : les événements assistant gardent la PREMIÈRE skill du tour comme `attributionSkill` — une invocation imbriquée `Skill(skill-creator)` ne ré-estampille jamais.
4. **Tentative de fix directe bloquée par le classifier Auto mode** (self-modification d'un hook d'enforcement) → respecter le blocage : seul l'ajout de docstring (zéro comportement) passe ; le fix comportemental part en `.proposed` pour application manuelle (workaround documenté CLAUDE.md).
5. **Inspection du transcript réel** (mon propre fichier .jsonl, comptage des lignes `attributionSkill`) → découverte contre-intuitive : **les tentatives d'édit BLOQUÉES sont elles-mêmes estampillées** avec la bonne skill — elles sèment des tampons valides dans la fenêtre. Re-tirer immédiatement le même batch passe (effet seeding). C'est ce qui a débloqué le chantier AVANT le fix.
6. **Fix .proposed** : fenêtre 15→80 + nouvelle détection `skill_invocations_from_transcript` (une invocation `Skill(<spécialiste requis>)` dans la fenêtre vaut activation — ownership strict conservé). Smoke-test sur transcript forgé, suite existante 36/36, +3 tests empilement → 39/39. Application manuelle Raphael, puis validation en conditions réelles (bypass loggé `attribution='skill-creator' invoked=['skill-creator']`).

## Leçons transférables

- **Un hook de détection basé transcript doit être testé contre les évolutions du harness** : l'empilement de skills (v2.1.202) a cassé silencieusement une hypothèse (« le plus récent tampon = skill active ») vraie sur 2.1.167.
- **Le debug log du hook + la lecture de son propre transcript** sont les deux sources de vérité — jamais de supposition sur ce que CC écrit : compter les lignes réelles.
- **L'œuf-et-poule des hooks PreToolUse** : le hook ne voit jamais l'événement du call courant ; toute détection repose sur les événements ANTÉRIEURS (d'où l'effet seeding des tentatives bloquées).
- **Blocage classifier ≠ mur** : docstring/documentation passe, comportement → `.proposed` + application humaine + tests immédiats.

## Liens

- [[erreur-delegate-guard-env-var-vs-stdin]] — précédent debug du même hook
- [[erreur-subagent-bypass-delegate-guard]] — anti-pattern contournement (jamais)
- [[critique-2026-07-09-fusions-skills-forge]] — le chantier qui a révélé le bug
- `.claude/hooks/delegate-guard.py` (docstring DETECTION) + `tests/test_delegate_guard.py` (3 cas empilement)
