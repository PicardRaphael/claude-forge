---
titre: "SDD Triangle — Drew Breunig (Spec/Tests/Code)"
resume: "Drew Breunig : SPEC, TESTS et CODE doivent rester synchronisés. Outil Plumb extrait les décisions des diffs et met à jour la spec. Trois niveaux de maturité (Böckeler, pas Breunig)"
aliases:
  - SDD triangle
  - spec tests code
  - Drew Breunig SDD
  - Plumb tool
  - spec diffing
  - living specification
domaine: development
type: technique
derniere-maj: 2026-05-23
sources:
  - "https://www.dbreunig.com/2026/03/04/the-spec-driven-development-triangle.html"
  - "https://github.com/dbreunig/plumb"
  - "https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html"
  - "https://heeki.medium.com/using-spec-driven-development-with-claude-code-4a1ebe5d9f29"
tags:
  - "#type/technique"
  - "#domaine/workflow"
  - "#domaine/testing"
auteur: claude
---

## Le Triangle (Drew Breunig)

```
    SPEC
   /    \
  /      \
TESTS ── CODE
```

Pattern de **Drew Breunig** : les 3 nœuds doivent rester synchronisés. Implémenter le code révèle des décisions non anticipées qui doivent refluer dans la spec. La spec n'est PAS un document figé.

## Trois niveaux de maturité — Birgitta Böckeler (Thoughtworks)

⚠️ **Attribution corrigée** : les 3 niveaux **NE viennent PAS** de Breunig (qui parle de Spec/Tests/Code, les 3 sommets du triangle). Ils viennent de **Birgitta Böckeler (Thoughtworks)** dans son article martinfowler.com. Heeki Park (AWS) les utilise en référençant explicitement Böckeler.

1. **Spec-first** — spec écrite pour une tâche, utilisée pendant le dev, peut être abandonnée après
2. **Spec-anchored** — spec maintenue comme living document tout au long du cycle de vie ; modifications commencent par la spec, AI regénère le code. C'est la cible de la plupart des outils SDD actuels.
3. **Spec-as-source** — la spec est le SEUL artefact humain, code = output transient généré, jamais touché à la main

> Verbatim Böckeler/Fowler : *"Are we making something worse in the attempt of making it better?"* (Verschlimmbesserung) — risque d'over-engineering SDD.

## Outil Plumb (Drew Breunig)

Pre-commit hook qui intercepte `git commit` :

1. Analyse le diff stagé + logs de conversation Claude Code
2. Extrait les "décisions prises" pendant l'implémentation
3. Gate le commit sur review humaine des décisions
4. Décisions approuvées → spec auto-mise-à-jour

Repo : https://github.com/dbreunig/plumb. Slogan : *"A tool for keeping things true."*

### Structure type

```
.plumb/
  config.json
  decisions.jsonl      ← log append-only
  requirements.json    ← requirements extraits
  coverage.json        ← couverture 3 dimensions
```

### Couverture multi-dimensions (Breunig)

Breunig mentionne plusieurs dimensions de couverture dans `plumb coverage` :

1. **Code coverage** (tests qui couvrent le code)
2. **Spec-to-test mapping** (chaque requirement a un test)
3. **Spec-to-code mapping** (chaque requirement a du code)

Le terme exact "Couverture 3D" n'est pas verbatim Breunig — c'est une lecture forge. Les concepts spec-to-test/spec-to-code sont bien chez lui.

## Lossless Feedback Loop (TDD + SDD)

Combiner TDD + SDD rend le processus lossless :

- Spec + tests + code committés atomiquement
- Chaque décision tracée dans le decision log
- Endgame : devs écrivent specs + tests, IA génère code, humains reviewent spec + résultats de tests

## Application dans /spec Neoteem

Actuellement au niveau **spec-first** (Böckeler). Évolution vers spec-anchored possible :

- Post-implémentation : générer un "spec diff" (planning vs réalité)
- Intégrer Plumb ou équivalent dans le pipeline /go
- Tracker les décisions qui modifient la spec

## Liens

- [[MOC-Techniques]]
- [[pattern-spec-driven-development]]
- [[pattern-spec-skill-deployment]]
- [[Drew Breunig]]
- [[Birgitta Böckeler]]
- [[Heeki Park]]
