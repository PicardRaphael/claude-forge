---
titre: "Erreur — gotchas line-numbers non verifies dans CLAUDE.md neo_ia"
resume: "Session 3 neo_ia (22 mai 2026) : 2 gotchas CLAUDE.md herites du plan ULTIME S1+S2 relayes sans verification empirique. react.py:151 chemin inexistant, streaming.py:929 hardcode absent. Detectes par advisor V2, corriges commit 96142b0. Pattern feedback_audit_claims_after_brief viole a l'echelle d'un line-number."
aliases:
  - "erreur gotchas line numbers"
  - "F1 F2 CLAUDE.md neo_ia"
  - "claims line number non verifies"
  - "react.py 151 streaming.py 929"
  - "anti pattern over specified gotcha"
  - "audit claims after brief viole"
derniere-maj: 2026-05-23
auteur: claude
type: knowledge
domaine: claude-code
sources:
  - "Session 3 deploiement neo_ia 2026-05-22"
  - "Plan ULTIME forge `output/plan-ULTIME-neo_ia-2026-05-22.md`"
  - "Advisor verification V2 forge 2026-05-22"
  - "Commit fix `96142b0` neo_ia develop branch"
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#projet/neo_ia"
  - "#domaine/claudemd"
  - "#anti-pattern"
---

# Erreur — gotchas line-numbers non verifies dans CLAUDE.md neo_ia

## Contexte

Session 3 du deploiement neo_ia (22 mai 2026). 25 changes restants du plan ULTIME S1+S2 a appliquer. VAGUE 7 = update CLAUDE.md racine avec gotchas + STOP block.

Le plan ULTIME (`output/plan-ULTIME-neo_ia-2026-05-22.md` cote forge) listait dans VAGUE 7.3 :
> "CLAUDE.md Gotchas ajouter (du scan code session 1) :
> - Couplage circulaire `react.py:151`
> - Model `gemini-2.5-flash` hardcode `streaming.py:929`
> ..."

J'ai relaye ces 2 gotchas tels quels dans CLAUDE.md neo_ia commit `9fe02a6` sans verifier empiriquement.

## Detection

Apres push de la session, advisor() a recommande 2 verifications avant push final :
- V1 : CHANGELOG.md update
- V2 : verifier line numbers gotchas

V2 a revele :

```bash
find apps/neochat/neochat/agents/universal -name "react.py"
# Rien trouve -> chemin INEXISTANT

grep -n "gemini-2.5-flash" apps/neochat/neochat/api/streaming.py
# Aucun match -> hardcode ABSENT de streaming.py
```

Verites empiriques :
- `react.py` vrai chemin = `packages/shared_utils/shared_utils/engine/react.py:150` (import lazy `from shared_utils.engine.status import emit_status` a l'interieur de la fonction)
- `gemini-2.5-flash` hardcode dans **7 emplacements** (extract.py:32, summarizer.py:160,215, rest_utils.py:52, responses.py:27,40, usage.py:13) — pas dans streaming.py

## Cause

**Pattern feedback_audit_claims_after_brief viole** : claims herites du plan precedent jamais re-verifies avant relayage. Le plan ULTIME a peut-etre ete genere avant un refactor du code (chemins ont change), ou contient une hallucination d'origine sub-agent S1.

A la difference des claims niveau "fichier existe / fonction existe", les claims line-number sont **doublement fragiles** :
1. Le fichier peut avoir change de chemin
2. La ligne peut avoir bouge avec n'importe quel edit du fichier

Donc tout `fichier.py:N` herite a une volatilite ~quadratique. Le verifier coute < 5s, ne pas le verifier produit du bruit silencieux pendant des mois.

## Correction

Commit `96142b0` neo_ia develop :

CLAUDE.md ligne 110 :
```diff
- - **Couplage circulaire `react.py:151`** : import lazy dans la boucle ReAct — dette technique connue
+ - **Couplage circulaire `packages/shared_utils/shared_utils/engine/react.py:150`** : import lazy `from shared_utils.engine.status import emit_status` a l'interieur de la fonction. Dette technique connue.
```

CLAUDE.md ligne 112 :
```diff
- - **Model hardcode `streaming.py:929`** : `gemini-2.5-flash` litteral
+ - **Model `gemini-2.5-flash` hardcode dans 7 emplacements** : `apps/neochat/neochat/agents/devis/nodes/extract.py:32`, `services/summarizer.py:160,215`, `api/v1/agents/rest_utils.py:52`, `models/responses.py:27,40`, `services/usage.py:13`
```

## Lecon a ne plus repeter

**Avant d'ecrire `<fichier>:<ligne>` dans CLAUDE.md ou doc, executer `find` chemin + `grep -n` contenu attendu.**

Pattern Boris compounding error-driven : cette regle est maintenant dans `feedback_gotchas_line_numbers_verifies_empiriquement` mémoire projet forge + cette note vault.

## Anti-pattern canonique connexe

- **Over-specified** (canonique [[comment-ecrire-claudemd]] anti-pattern #3) : precision sur l'inutile = bruit silencieux. Un line-number faux = sur-precision dans une direction trompeuse.
- **Trust-then-verify gap** (anti-pattern #4) : lister une regle sans la verifier. Ici "le plan dit X, donc X" = trust-then-verify gap a l'echelle d'un single line-number.

## Liens

- [[feedback_audit_claims_after_brief]] — pattern parent viole
- [[comment-ecrire-claudemd]] — canonique source anti-patterns
- [[niveau-1-static-mesure-agents-neo-ia-2026-05-22]] — session 3 trace
- [[critique-2026-05-22-doctrine-drift-guard]] — autre erreur meta de la meme session
