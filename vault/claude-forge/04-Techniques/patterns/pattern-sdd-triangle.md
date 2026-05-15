---
titre: "SDD Triangle — Spec ↔ Tests ↔ Code feedback loop"
resume: "Drew Breunig : SPEC, TESTS et CODE doivent rester synchronisés. Implémenter le code améliore la spec. Outil Plumb extrait les décisions des diffs et met à jour la spec automatiquement"
aliases:
  - SDD triangle
  - spec tests code
  - Drew Breunig SDD
  - Plumb tool
  - spec diffing
  - living specification
domaine: development
type: technique
derniere-maj: 2026-05-12
tags:
  - "#type/technique"
  - "#domaine/workflow"
  - "#domaine/testing"
auteur: claude
---

## Le Triangle

```
    SPEC
   /    \
  /      \
TESTS ── CODE
```

Les 3 nœuds doivent rester synchronisés. Si on améliore le code, on doit améliorer la spec. La spec n'est PAS un document figé — implémenter le code révèle des décisions non anticipées qui doivent refluer dans la spec.

## Trois niveaux de maturité

1. **Spec-first** — spec guide le build initial, peut drifter après
2. **Spec-anchored** — spec et code évoluent ensemble, sync enforced
3. **Spec-as-source** — humains éditent uniquement les specs, machines génèrent le code

## Outil Plumb (Drew Breunig)

Pre-commit hook qui intercepte `git commit` :

1. Analyse le diff stagé + les logs de conversation Claude Code
2. Extrait les "décisions prises" pendant l'implémentation
3. Gate le commit sur la review humaine des décisions
4. Les décisions approuvées mettent à jour la spec automatiquement

### Structure

```
.plumb/
  config.json
  decisions.jsonl      ← log append-only des décisions
  requirements.json    ← requirements extraits
  coverage.json        ← couverture 3 dimensions
```

### Couverture 3D (`plumb coverage`)

1. **Code coverage** — tests qui couvrent le code
2. **Spec-to-test mapping** — chaque requirement a au moins 1 test
3. **Spec-to-code mapping** — chaque requirement a du code qui l'implémente

## Lossless Feedback Loop (TDD + SDD)

Le coding IA traditionnel est LOSSY — le raisonnement est éphémère, les décisions disparaissent entre sessions. Combiner TDD + SDD rend le processus lossless :

- Spec + tests + code committés atomiquement
- Chaque décision est tracée dans le decision log
- Endgame prédit : devs écrivent specs + tests, IA génère le code, humains reviewent spec + résultats de tests (jamais le code directement)

## Application dans /spec Neoteem

Actuellement au niveau **spec-first** (la spec est écrite avant le dev mais peut drifter). Pour évoluer vers spec-anchored :

- Post-implémentation : générer un "spec diff" (planning vs réalité)
- Intégrer Plumb ou équivalent dans le pipeline /go
- Tracker les décisions prises pendant l'implémentation qui modifient la spec

## Liens

- [[MOC-Techniques]]
- [[pattern-spec-driven-development]] — Pattern SDD complet
- [[pattern-spec-skill-deployment]] — Déploiement skill /spec
- [[over-specification-paradox]] — Ne pas sur-spécifier (S*=0.509)