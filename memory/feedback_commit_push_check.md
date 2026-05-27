---
name: commit-push-check-pattern
description: Quand Raphael dit "regarde commit et push tout", verifier git status + diff des repos externes avant push
type: feedback
originSessionId: b3529a11-dcf4-49f9-aa3d-d8b5e7bdabc2
---
Quand Raphael demande de "regarder les commits et push", verifier le git status et diff de chaque repo externe (ia_back, neo_ia, neoteem-brain, bdd) avant de push. Ne pas push aveuglément.

**Why:** Raphael veut un contrôle qualité avant push — vérifier qu'il n'y a pas de changements oubliés ou de fichiers non commités.

**How to apply:** `git status` + `git log origin/develop..HEAD` sur chaque repo, résumer ce qui va être pushé, attendre confirmation.
