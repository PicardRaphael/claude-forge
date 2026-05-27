---
name: tests-adverses-obligatoires
description: "Pour tout hook de sécurité ou enforcement, tester les cas adverses (bypass possibles), pas seulement les cas heureux — DA AVANT push, pas après"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e3438a06-ff07-4470-93a8-d0fcd072063d
---

Pour tout livrable de sécurité ou enforcement (hook bloquant, guard, validation) :

**Règle** : tester les cas adverses (bypass possibles) AVANT de proclamer "validé", pas seulement les cas heureux. Lancer devil's advocate AVANT le push, pas après.

**Why:** Session 2026-05-21. J'ai déployé repo-scope-guard.py dans neo_ia, écrit 8 tests "heureux" (Read bdd, Bash cat ../bdd/foo.sql) tous PASS, et proclamé "8/8 PASS validé". Push effectué. Le DA, lancé APRÈS push à cause du stop hook, a trouvé 3 bloquants en relisant le code : Glob pattern hors scope non testé, Write/Edit jamais testés (alors qu'ils étaient dans les matchers), Bash bypass triviaux (env vars, heredoc, commandes séparées). Tests heureux ≠ validation.

**How to apply:**
- Pour chaque outil bloqué par le hook, lister 3-5 bypass possibles ET les tester
- Lancer devils-advocate AVANT push (workflow architect → impl → test → DA → livraison documenté dans rules/devils-advocate-pipeline.md)
- Si une attaque n'est pas couverte (ex: Bash arbitraire), documenter explicitement "by discipline" vs "by construction" dans la rule
- Toujours capturer `$?` immédiatement après la commande, pas via wrapper shell function (qui propage mal l'exit code)
- Le stop hook DA a sauvé cette livraison — l'écouter, pas le contourner

Cas concrets à tester pour un hook path-based :
- Glob/Grep avec pattern relatif ET absolu
- Write/Edit/MultiEdit sur CHAQUE repo bloqué (pas juste Read)
- Bash env var, heredoc, subshell, eval, commandes séparées par `;`
- Paths Windows mixtes (`C:/...`, `C:\...`, `/c/...`)
- Symlinks

Liens : [[claim-security-must-be-provable]], [[test-everything]], [[audit-claims-after-brief]]
