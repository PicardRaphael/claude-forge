---
titre: "Google Engineering Practices — guide CL & code review (référence externe)"
resume: "Doctrine Google publique sur code review : CL = changelist self-contained, small CLs (~100L, jamais >1000L), descriptions imperatives stand-alone, handling comments avec courtoisie, mission code review = améliorer la santé globale du code (pas perfection). Référence externe pour workflow forge."
aliases:
  - "google eng practices"
  - "google code review developer"
  - "small CLs google"
  - "writing good CL descriptions"
  - "handling reviewer comments google"
  - "code review developer guide google"
  - "Critique Piper Google"
  - "LGTM looks good to me"
derniere-maj: 2026-05-23
auteur: claude
type: reference
sources:
  - "https://github.com/google/eng-practices (repo officiel)"
  - "https://google.github.io/eng-practices/ (site rendu)"
  - "https://google.github.io/eng-practices/review/developer/index.html"
  - "https://google.github.io/eng-practices/review/developer/cl-descriptions.html"
  - "https://google.github.io/eng-practices/review/developer/small-cls.html"
  - "https://google.github.io/eng-practices/review/developer/handling-comments.html"
tags:
  - "#type/reference"
  - "#domaine/code-review"
  - "#sujet/workflow"
  - "#meta/externe"
---

# Google Engineering Practices — guide CL & code review

> Référence externe (provider officiel Google sur ses propres pratiques = single source acceptable cf [[feedback_anthropic_single_source]]). Doctrine publique Google sur code review et changelists, applicable au workflow forge avec adaptation.

## QUOI — Source

**Repo officiel** : [github.com/google/eng-practices](https://github.com/google/eng-practices) (CC-By 3.0 License)
**Site rendu** : [google.github.io/eng-practices](https://google.github.io/eng-practices/)

Documents publics maintenus par Google qui formalisent leur **collective experience** sur les best practices code review développées en interne (outils Piper version control + Critique code review).

## Terminologie Google

- **CL (Changelist)** : "one self-contained change submitted to version control or undergoing code review". Équivalent : PR / patch / change selon contexte.
- **LGTM** : "Looks Good to Me" — ce que le reviewer dit en approuvant une CL.

## Mission code review (verbatim Google)

> "The primary purpose of code review is to ensure that the overall code health of Google's codebase improves over time."

**Principe senior** : reviewer approuve une CL dès qu'elle améliore la santé globale du code, **même imparfaite**.

> "There is no such thing as 'perfect' code — there is only better code."

Reviewer cherche **continuous improvement**, pas perfection.

## 1. Writing Good CL Descriptions (verbatim docs)

### Première ligne
- Short summary de ce qui change
- **Imperative sentence** : "Delete the FizzBuzz RPC", pas "Deleted..." ni "This deletes..."
- Suivie d'une ligne blanche
- Doit **stand alone** pour skimming history

### Body
- Le problème résolu
- Pourquoi cette approche
- Shortcomings éventuels
- Bug numbers, benchmarks, design doc links

### Mauvaises descriptions (exemples Google)
- "Fix bug"
- "Add patch"
- "Phase 1"

Vagues, sans actionnable.

### Bonnes descriptions
- Functionality changes : problème + rationale implémentation
- Refactorings : ce qui change, contexte, direction future
- **Même les petits CLs nécessitent contexte expliquant le pourquoi**

### Règle finale verbatim
> "Review a CL description before submitting the CL, to ensure that the description still reflects what the CL does."

## 2. Small CLs (verbatim Google)

### Pourquoi
> "Reviewers have discretion to reject your change outright for the sole reason of it being too large."

Small CLs :
- Reviewed plus vite, plus thoroughly
- "less likely to introduce bugs"
- Réduisent wasted work si rejected
- Plus faciles à merger, designer, rollback

### Qu'est-ce que "small"
- **One self-contained change addressing "just one thing"**
- Include related test code
- Système doit keep working après submission
- New APIs incluent usage examples dans le même CL
- **~100 lignes raisonnable** ; **~1000 lignes usually too large**
- File count compte : 200L dans 1 fichier OK, 200L spread 50 fichiers = too large

### Quand large CLs OK
- Suppression d'un fichier entier ≈ 1 ligne
- Outputs auto-générés d'un refactoring tool

### Stratégies de split

| Stratégie | Comment |
|-----------|---------|
| **Stacking** | Build CLs sequentially on top of each other |
| **By files** | Split par domaine reviewer (proto vs consuming code) |
| **Horizontally** | Split par tech-stack layer via shared stubs/abstractions |
| **Vertically** | Split par full-stack feature (multiplication vs division separate) |
| **Combined grid** | Chaque layer × feature = own CL |

### Autres règles clés
- **Refactorings = CL séparés** des features/bug work
- **Tests = same CL** que la logique qu'ils couvrent
- **Dependent CLs ne doivent pas casser le build** entre submissions
- Si large CL semble inévitable → **advance consent** des reviewers

## 3. Handling Reviewer Comments (verbatim Google)

### 1. Don't Take it Personally
> "Never respond in anger to code review comments"

Reviews visent code quality, pas l'attaque personnelle. Walk away si besoin. Rudeness persistante : adresser en privé d'abord, escalader management si non résolu.

### 2. Fix the Code (pas juste le commentaire review)
Quand quelque chose est unclear pour le reviewer, clarifier **le code lui-même** d'abord, puis inline comments si nécessaire.

> "A comment in the review tool only helps the reviewer — clarifying your code or adding code comments does help future readers too."

### 3. Think Collaboratively
Avant de disagree, confirmer que tu comprends ce qui est demandé. Instead of flat refusal :
- Explain reasoning
- Invite dialogue (describe tradeoffs, ask if reviewer voit la balance différemment)

> "Courtesy and respect should always be a first priority."

### 4. Resolving Conflicts
1. Seek consensus avec reviewer
2. Si échec → refer to Google's *Standard of Code Review* pour principes guidants

## Ce que les reviewers évaluent (référence)

**Design** (architecture) · **Functionality** · **Complexity** (no "clever" unreadable) · **Tests** · **Naming** · **Comments** ("Why" not just "What") · **Style** · **Documentation**

**Vigilance over-engineering** : code rendu plus générique que nécessaire, ou functionality pas needed maintenant.

## Pertinence pour forge

### ⚠️ Calibrage honnête

Google eng-practices = **code review humain → humain**. Forge utilise Claude Code = workflow LLM-assisted où c'est **Raphael qui review les outputs Claude**, pas un peer reviewer.

**Pertinence applicable** :
- ✅ **Small CLs principle** → applicable forge : préférer petits diffs (~100 lignes), faciles à review, faciles à rollback
- ✅ **Description imperative + body avec rationale** → applicable aux commit messages forge (déjà fait, ex : commits cette session)
- ✅ **Refactorings = commits séparés** des features → applicable forge
- ✅ **Tests = same commit** que la logique → applicable forge
- ✅ **"Improve over time, not perfection"** → mindset compounding aligné avec Boris/Karpathy
- ⚠️ **Handling comments** = peu applicable forge perso (pas de peer review humain)
- ⚠️ **Conflict resolution reviewer/author** = pas applicable forge

### Convergences avec doctrine forge existante

| Google | Forge canonique | Convergence |
|--------|-----------------|-------------|
| Small CLs ~100L | [[comment-ecrire-claudemd]] target 200L CLAUDE.md | Principe "court > long" |
| Tests same CL que logique | Doctrine TDD conditionnelle (cf [[raisonnement-22mai-doctrine-vs-enforcement]]) | Test-with-code |
| Improve over time, pas perfection | Boris compounding "Anytime we see Claude do something incorrectly, we add it to CLAUDE.md" | Évolution iterative |
| Refactorings séparés | Pas explicite forge, candidat à ajouter | Nouvelle règle |

## QUAND consulter cette note

- Avant de produire un commit message non-trivial → review les patterns "good CL description"
- Avant de soumettre un diff large → vérifier stratégies de split
- Si conflit avec un teammate sur un review → handling-comments principles
- Si on veut formaliser des conventions PR pour un repo collaboratif (ia_back / neo_ia / lojii) → guide complet

## NE PAS appliquer

- ❌ Pas de section dédiée Google dans [[comment-creer-agent]] ou [[methode-analyser-repo]] (out of scope)
- ❌ Pas de hook qui enforce small CLs (workflow hook = anti-pattern doctrine 22 mai cf [[raisonnement-22mai-doctrine-vs-enforcement]])
- ❌ Pas de rule forge dérivée — référence externe, pas doctrine canonique forge

## SOURCES verbatim

### Repo officiel
- [github.com/google/eng-practices](https://github.com/google/eng-practices) — CC-By 3.0 License
- [google.github.io/eng-practices](https://google.github.io/eng-practices/) — site rendu

### Section developer
- [Index — Code Review Developer Guide](https://google.github.io/eng-practices/review/developer/)
- [Writing good CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html)
- [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [Handling reviewer comments](https://google.github.io/eng-practices/review/developer/handling-comments.html)

### Section reviewer (référence croisée)
- [The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)

## ALIASES (8)

- google eng practices
- google code review developer
- small CLs google
- writing good CL descriptions
- handling reviewer comments google
- code review developer guide google
- Critique Piper Google
- LGTM looks good to me

## WIKILINKS

### Notes canoniques (croisements pertinents)
- [[comment-ecrire-claudemd]] — convergence "court > long"
- [[workflow-claude-code-optimal]] — workflow forge complémentaire
- [[raisonnement-22mai-doctrine-vs-enforcement]] — pas de hook workflow forcé (différent de Google peer review)
- [[methode-analyser-repo]] — pipeline forge (architect/dev/reviewer/test)

### Refs externes
- [[programmatic-tool-calling]] — feature Anthropic complémentaire (orchestration code)

---

**Fin note référence `google-eng-practices.md`** — créée 23 mai 2026 sur demande Raphael. Référence externe documentée, pas doctrine canonique forge.
