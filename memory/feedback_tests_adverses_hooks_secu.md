---
name: tests-adverses-hooks-secu
aliases:
  - tests-adverses-obligatoires
  - tests-adverses-ratio-3-1-hooks-secu
description: "Hook sécu/enforcement (guard, scope-guard, delegate-guard) = suite de tests MAJORITAIREMENT adverse (≥3:1 bypass/happy), DA AVANT push (pas après), caractériser les bugs (épingler le comportement actuel, pas masquer), docstring de scope, + cas d'usage légitime réaliste pour attraper les false-positives qui émergent à l'usage."
metadata:
  type: feedback
---

Pour tout livrable de sécurité ou enforcement (hook bloquant, guard, validation) : tester les cas ADVERSES (bypass possibles) AVANT de proclamer "validé", pas seulement les cas heureux. Lancer devil's advocate AVANT le push, pas après. La suite doit être majoritairement adverse : **≥75% tentatives de bypass, ≤25% happy path**.

**Why:**
- Session 2026-05-21 : repo-scope-guard.py déployé dans neo_ia avec 8 tests "heureux" tous PASS, proclamé "8/8 validé", pushé. Le DA (lancé APRÈS push) a trouvé 3 bloquants : Glob hors scope non testé, Write/Edit jamais testés (pourtant dans les matchers), Bash bypass triviaux (env vars, heredoc, `;`). Tests heureux ≠ validation.
- Session 2026-05-27 (Phase 2) : ratio porté à 5.3:1 (security-guard) et 8:1 (delegate-guard). Les tests adverses ont révélé 1 vrai bug (substring agent_id, cf [[delegate-guard-substring-agent-id-bug]]) + 1 défaut de testabilité.

**How to apply:**
1. **Pas de 3:1 artificiel** : ne pas gonfler avec des patterns hors-scope que le hook n'a jamais prétendu couvrir (ex tester `dd`/`mkfs` sur un hook qui ne couvre que `rm`/`git`). Le vrai 3:1 = ≥3 variations de bypass PAR pattern réellement claimed (espaces, tabs, ordre flags, casse, chemin équivalent).
2. **Pour chaque outil bloqué, lister 3-5 bypass ET les tester** : Glob/Grep relatif ET absolu ; Write/Edit/MultiEdit sur CHAQUE repo bloqué (pas juste Read) ; Bash env var, heredoc, subshell, eval, commandes séparées par `;` ; paths Windows mixtes (`C:/`, `C:\`, `/c/`) ; symlinks.
3. **Caractériser, pas masquer** : si un test révèle un bug, épingler le comportement ACTUEL (`assert ok is True  # current buggy`), documenter dans le docstring, lister le bug. NE PAS aplatir pour faire passer.
4. **Docstring de scope** en tête du fichier : périmètre déclaré + ce que les tests NE vérifient PAS (gaps hors-scope volontaires).
5. **Testabilité** : hook expose sa logique en fonctions pures importables + traitement stdin dans `main()` gardé (sinon `importlib` déclenche `sys.exit` à l'import).
6. **Self-blocking** : tester un security-guard via Bash déclenche le hook sur sa propre commande. Construire les payloads par concaténation runtime, ou exécuter via `pytest fichier.py`. Cf [[hook-self-blocking-catch22]].
7. **DA AVANT push** (workflow architect → impl → test → DA → livraison). Toujours capturer `$?` immédiatement après la commande, pas via wrapper shell.
8. **False-positives à l'usage (27 mai)** : la suite adverse initiale cible les false-negatives (bypass). Les false-positives (sur-blocage du légitime) émergent souvent seulement en usage réel. `vault-cat-guard` : 33 tests verts puis 2 over-blocks découverts à l'usage (Read vault en session principale, commande chaînée `git add ... && git push | tail`). → Ajouter des cas d'USAGE LÉGITIME réaliste (commandes chaînées, contextes main vs sub-agent, workflows commit/push/Edit). Distinguer explicitement les deux familles : false-negative (bypass tenté) ET false-positive (légitime sur-bloqué).

Consolide depuis : [[feedback_tests_adverses_obligatoires]] (règle parente) et [[feedback_tests_adverses_ratio_3_1]] (précision quantitative ratio + caractérisation). Capitalisé dans la canonique [[comment-creer-hook]] étape 5. Lié : [[claim-security-must-be-provable]], [[test-everything]], [[verifier-claims-empiriquement]], [[da-dicte-tests-adverses-pas-moi]].
