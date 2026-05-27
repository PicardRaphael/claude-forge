---
name: gotchas-line-numbers-verifies-empiriquement
description: "Tout claim line-number dans CLAUDE.md ou doc (`fichier.py:N`) DOIT etre verifie par grep -n empirique AVANT relayage. Heriter d'un plan antérieur sans re-verifier = pattern feedback_audit_claims_after_brief viole."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 632e98ec-976c-4408-8507-4988788a8d26
---

Avant d'ecrire `<fichier>:<ligne>` dans CLAUDE.md, doc ou gotcha, executer `grep -n` ou `find` pour confirmer l'existence du chemin ET du contenu attendu a cette ligne. Si numero change avec le code, retirer le numero ou pointer chemin seul.

**Why:** Session 3 (22 mai 2026), j'ai relaye 2 gotchas du plan ULTIME S1+S2 dans CLAUDE.md neo_ia sans verifier empiriquement :
- `react.py:151` -> chemin `apps/neochat/neochat/agents/universal/react.py` **N'EXISTE PAS** (vrai chemin = `packages/shared_utils/shared_utils/engine/react.py:150`)
- `streaming.py:929` -> AUCUN `gemini-2.5-flash` dans `streaming.py` (hardcode dans 7 autres fichiers : extract.py, summarizer.py, rest_utils.py, etc.)

Detectes par advisor V2 (verification post-write). Bruit silencieux dans CLAUDE.md = anti-pattern "over-specified" canonique Anthropic. Pattern `feedback_audit_claims_after_brief` viole : claims herites du plan precedent jamais re-verifies.

Corriges commit 96142b0 apres detection.

**How to apply:**
1. `<fichier>:<N>` dans CLAUDE.md ou skill = TRIGGER verification : `find` chemin + `grep -n` contenu attendu a ligne N
2. Si numero precis = volatile (refactor du code casse le numero) → preferer chemin sans numero OU pattern grepable
3. Plans/specs herites de sessions anterieures : leurs claims line-number DOIVENT etre re-verifies avant relayage. La verite empirique > la verite du plan.
4. Pattern Boris compounding error-driven : capturer cette regle ici evite la recurrence
5. Si line-number critique, ajouter un test smoke `grep -n "<pattern>" <file>` qui casse si le contenu disparait
