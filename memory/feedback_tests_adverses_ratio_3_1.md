---
name: tests-adverses-ratio-3-1-hooks-secu
description: "Hooks sécu/contrôle = suite de tests ≥3:1 adverse/happy. Ne pas gonfler avec du hors-scope. Caractériser les bugs (épingler le comportement actuel, pas masquer). Docstring de scope."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f598fcbc-1e1f-4161-bd42-75eddf13fbdf
---

Une suite de tests pour un hook de sécurité/contrôle (security-guard, delegate-guard, scope-guard) doit être **majoritairement adverse** : ≥75% tentatives de bypass, ≤25% happy path.

**Why:** Le happy path seul prouve que le légitime passe, jamais que l'illégitime est bloqué — trompeur sur du code de contrôle. Validé 27 mai (Phase 2) : security-guard ratio 5.3:1, delegate-guard 8:1. Les tests adverses ont révélé 1 vrai bug (substring agent_id, cf [[delegate-guard-substring-agent-id-bug]]) + 1 défaut testabilité (security-guard sans main() gardé).

**How to apply:**
1. **Pas de 3:1 artificiel** : ne pas gonfler le ratio avec des patterns hors-scope que le hook n'a jamais prétendu couvrir (ex : tester `dd`/`mkfs`/base64 sur un hook qui ne couvre que `rm`/`git`). Le vrai 3:1 = ≥3 variations de bypass PAR pattern réellement claimed (espaces, tabs, ordre flags, casse, chemin équivalent).
2. **Caractériser, pas masquer** : si un test révèle un bug, épingler le comportement ACTUEL (`assert ok is True  # current buggy`), documenter dans le docstring, lister le bug. NE PAS aplatir pour faire passer.
3. **Docstring de scope** en tête du fichier : périmètre déclaré + ce que les tests NE vérifient PAS (gaps hors-scope volontaires), pour qu'un futur lecteur sache que l'omission est délibérée.
4. **Testabilité** : hook doit exposer sa logique en fonctions pures importables + traitement stdin dans `main()` gardé. Sinon `importlib` déclenche `sys.exit` à l'import.
5. **Self-blocking** : tester un security-guard via Bash déclenche le hook sur sa propre commande. Construire les payloads par concaténation runtime, ou exécuter via `pytest fichier.py` (le hook scanne la commande, pas le contenu du fichier).

Règle capitalisée dans la canonique [[comment-creer-hook]] étape 5. Cf [[tests-adverses-obligatoires]] (règle parente), [[hook-self-blocking-catch22]].
