---
name: tests-adverses-hooks-secu
aliases:
  - tests-adverses-obligatoires
  - tests-adverses-ratio-3-1-hooks-secu
description: "Hook sécu/enforcement (guard, scope-guard, delegate-guard) = suite de tests MAJORITAIREMENT adverse (≥3:1 bypass/happy), DA AVANT push (pas après), caractériser les bugs (épingler le comportement actuel, pas masquer), docstring de scope, + cas d'usage légitime réaliste pour attraper les false-positives qui émergent à l'usage."
metadata:
  type: feedback
---

Cf [[comment-creer-hook]] étape 5 (doctrine : ratio adverse/happy ≥3:1 sans 3:1 artificiel, 3 catégories de tests, caractérisation vs masquage, docstring de scope, testabilité fonctions pures importables, self-blocking, DA AVANT push).

**Cas empirique(s) :**

- **Session 2026-05-21** : repo-scope-guard.py déployé dans neo_ia avec 8 tests "heureux" tous PASS, proclamé "8/8 validé", pushé. Le DA (lancé APRÈS push) a trouvé 3 bloquants : Glob hors scope non testé, Write/Edit jamais testés (pourtant dans les matchers), Bash bypass triviaux (env vars, heredoc, `;`). Tests heureux ≠ validation.
- **Session 2026-05-27 (Phase 2)** : ratio porté à 5.3:1 (security-guard) et 8:1 (delegate-guard). Les tests adverses ont révélé 1 vrai bug (substring agent_id, cf [[delegate-guard-substring-agent-id-bug]]) + 1 défaut de testabilité.
- **False-positives à l'usage (27 mai)** : `vault-cat-guard` = 33 tests verts puis 2 over-blocks découverts seulement à l'usage réel (Read vault en session principale, commande chaînée `git add ... && git push | tail`). Les false-positives (sur-blocage du légitime) émergent souvent après la suite adverse initiale, qui ne cible que les false-negatives. → Ajouter des cas d'USAGE LÉGITIME réaliste (commandes chaînées, contextes main vs sub-agent, workflows commit/push/Edit).
- **Self-blocking (catch-22)** : tester un security-guard via Bash déclenche le hook sur sa propre commande de test. Construire les payloads par concaténation runtime, ou exécuter via `pytest fichier.py`. Capturer `$?` immédiatement après la commande, pas via wrapper shell. Cf [[hook-self-blocking-catch22]].

Consolide les feedbacks tests-adverses antérieurs (règle parente + précision quantitative ratio), archivés 2026-05-29. Lié : [[claim-security-must-be-provable]], [[da-dicte-tests-adverses-pas-moi]].
