---
titre: Tests "8/8 PASS" sur cas heureux ne valident PAS la sécurité
aliases:
  - "tests heureux vs adverses"
  - "tests adverses obligatoires"
  - "validation tests cas evidents"
  - "tests PASS faux validation"
  - "cas adverses non testes"
  - "da-dicte-tests-adverses"
resume: J'ai proclamé "tests 8/8 PASS validés" sur le hook repo-scope-guard alors que je n'avais testé que des cas évidents (Read bdd direct) sans tester les bypass (Glob pattern, Write/Edit, Bash exotique). Le DA a trouvé 3 bloquants en lisant le code.
derniere-maj: 2026-05-24
tags:
  - "#type/erreur"
  - "#erreur/process"
  - "#erreur/tests"
  - "#domaine/claude-code"
---

# Tests heureux vs tests adverses

## Ce qui s'est passé

Lors du déploiement de `repo-scope-guard.py` dans neo_ia, j'ai écrit 8 tests empiriques qui ont tous PASS, et j'ai proclamé "système validé, livraison OK". Push effectué (commit 6e1160b).

Quand le devil's advocate a relu le code à froid, il a trouvé **3 bloquants** que mes tests n'avaient pas couverts :

1. **Glob pattern hors scope** : `Glob(pattern="../bdd/**/*.sql")` passait sans blocage, car le hook lisait `tool_input.path` (vide → fallback cwd) mais pas le pattern résolu.
2. **Write/Edit/MultiEdit non testés** : code matchait Write|Edit dans le hook, mais aucun test empirique → on ne savait pas si `file_path` était résolu correctement.
3. **Bash bypass triviaux** : `cat $(echo ../bdd)`, env vars, heredoc, `cd ..; cd bdd; cat` (commandes séparées) — non couverts par le scan token-par-token.

## Pourquoi c'était une erreur

**Tests "heureux"** : on prend les cas évidents (`Read ../bdd/foo.sql`), on vérifie que ça marche, on déclare "validé".

**Tests "adverses"** : on cherche ce qui pourrait contourner la défense. Pour un hook de sécurité, c'est OBLIGATOIRE. Les bugs adversaires sont la raison d'être du hook.

Ratio de couverture : 8 tests heureux sur ~15 cas adverses possibles = **~50% de couverture réelle**. Proclamer "validé" était une auto-tromperie.

## La leçon (Jarvis)

Pour TOUT hook de sécurité ou enforcement :

1. **Tester les cas heureux** (le système attendu fonctionne)
2. **Tester les cas adverses** : pour chaque outil bloqué, lister 3-5 façons de contourner et tester chacune
3. **Lancer le devil's advocate AVANT push**, pas après
4. **Documenter les limites assumées** : si une attaque n'est pas couverte, l'écrire dans la rule (`by discipline` vs `by construction`)

## Application concrète à repo-scope-guard

**Tests adverses qu'on aurait dû faire d'office** :
- Glob avec pattern relatif (`../bdd/**/*.sql`)
- Glob avec pattern absolu (`/bdd/...`)
- Write/Edit/MultiEdit sur chaque repo bloqué
- Bash avec env var (`D=../bdd; cat $D/x`)
- Bash avec heredoc, subshell, eval
- Bash en commandes séparées (`cd ..; cd bdd; cat foo`)
- Read avec path Git Bash style (`/c/Users/.../bdd/x`)
- Symlink (cas couvert par Path.resolve, mais à vérifier)

**Résultat post-fix** :
- Glob pattern résolu en plus du path de base ✅
- Write/Edit testés empiriquement → bloque ✅
- Write sur ia_back maintenant interdit (cohérence rule/hook, FREE_READ_REPOS vs FREE_WRITE_REPOS) ✅
- Bash bypass exotiques : position assumée *by discipline*, documenté dans rule

## Anti-pattern adjacent : "exit code via pipe"

En vérifiant les tests, j'ai aussi commis l'erreur de capturer l'exit code via une fonction shell qui utilisait `$(uv run python ...)`. Ce pattern propage parfois mal l'exit code, donnant tous tests à 0. **Toujours capturer `$?` immédiatement après la commande**, pas via wrapper.

## Liens

- feedback : claim-security-must-be-provable
- feedback : test-everything
- feedback : verify-exhaustive-claims
- feedback : audit-claims-after-brief
- [[erreur-architect-neo_ia-fouille-bdd]]
- [[erreur-vault-before-specialist-ttl-scope]]
- feedback : enforce-not-advise

## Méta — leçon Jarvis renforcée

Quand un livrable a une dimension "sécurité" ou "enforcement", la barre de validation est plus haute :
- Tests heureux ≠ validation
- Devil's advocate AVANT le push, pas après
- Si on n'a PAS lancé DA, on n'a pas terminé

Le stop hook a fait son job ici : il m'a obligé à lancer DA après que j'aie déjà push. Sans le hook, j'aurais clos la session sur "tout est validé" alors que des bypass étaient possibles. **Le hook stop-DA a sauvé la livraison.**
