---
titre: "Erreur — Changer un mécanisme sans lire les tests qui le verrouillent"
aliases:
  - changer-mecanisme-lire-tests-qui-verrouillent
  - tests qui verrouillent mécanisme
  - lire tests avant mécanisme
  - patch mock casse mécanisme changé
  - tests silencieux changement contrat
  - casse tests import retiré
resume: Avant de changer le mécanisme ou le contrat observable d'un fichier, lire ses tests pour repérer les 3 dépendances fragiles (patch/mock sur l'ancien nom, grep du source, imports) — sinon des tests neutres cassent en silence.
derniere-maj: 2026-07-07
tags:
  - "#type/erreur"
  - "#erreur/tests"
  - "#erreur/process"
  - "#domaine/dev"
  - "#domaine/python"
type: erreur
---

# Erreur — Changer un mécanisme sans lire les tests qui le verrouillent

## Ce qui s'est passé

2026-06-17, fix Langfuse neo_ia. Changement du canal de lecture du statut (`os.getenv(...)` → `get_config().is_configured()`) + retrait de `import os` de `neodoc/main.py` (devenu mort code). Fonctionnellement correct (`is_configured()` = True confirmé). Résultat : **9 tests cassés** :

- 8 patchaient `neodoc.main.os.getenv` — dont 6 comme **effet neutre**, sans rapport avec Langfuse (startup, flush, checkpointer) → `AttributeError: module has no attribute 'os'`
- 1 grepait `"LANGFUSE_PUBLIC_KEY" in source` de `main.py` (anti-régression mono-projet) → symbole littéral disparu du fichier

`/go` (give-Claude-a-way-to-verify) les a rattrapés, mais ils auraient dû être vus AVANT en lisant `test_main.py`.

## Pourquoi c'est une erreur

Lire le fichier édité ne suffit pas quand on change le **mécanisme** ou le **contrat observable** (pas juste la logique interne). Des tests ailleurs peuvent verrouiller l'ancien nom, même des tests qui ne testent PAS le sujet modifié.

## Les 3 dépendances fragiles à grep AVANT tout changement de mécanisme

Dans `X.py` qu'on va modifier, chercher dans ses tests :

1. **`patch("X.<attr>")` / `mock.patch.object(X, ...)`** — un patch cible un *nom* ; retirer ce nom casse le patch, même si le test ne teste pas ce nom directement (tests neutres qui patchent pour isolation)
2. **`read_text()` / grep du source de X** — tests structurels qui vérifient la présence/absence d'un symbole littéral dans le fichier source
3. **`from X import Y` côté test** — imports du module depuis les tests

Si l'un de ces patterns existe → **adapter le test dans le même changement**, en préservant son INTENTION :
- Test neutre qui patchait `os.getenv` pour isolation → patcher la nouvelle source neutre
- Test anti-régression qui grepait une clé → vérifier le nouveau canal, pas l'ancien symbole

## Distinct des patterns adjacents

- `edit-tool-read-obligatoire-meme-en-parallele` — lire le fichier qu'on édite (avant l'edit)
- `regression-diagnostic-diff-avant-redesign` — diagnostiquer une régression déjà présente
- [[erreur-tests-heureux-vs-adverses]] — tests adverses manquants sur hooks sécurité

Ici on **anticipe** la casse de tests existants lors d'un changement de mécanisme.

## Liens

- feedback : changer-mecanisme-lire-tests-qui-verrouillent
- [[erreur-subagent-bypass-delegate-guard]] (cite ce pattern)
- [[erreur-tests-heureux-vs-adverses]]
