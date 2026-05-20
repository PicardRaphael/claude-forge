---
titre: "Running Implementation Notes — Pattern Thariq"
resume: "Pendant l'implémentation d'une spec, Claude maintient un fichier implementation-notes.md vivant qui capture décisions d'ambiguïté, déviations, tradeoffs et open questions"
aliases:
  - "running implementation notes"
  - "implementation-notes.md pattern"
  - "implementation notes thariq"
  - "spec ambiguity notes"
  - "decisions log live"
  - "thariq implementation pattern"
domaine: prompt-engineering
type: technique
derniere-maj: 2026-05-20
auteur: claude
sources:
  - "https://x.com/trq212/status/2056415973125796184"
  - "Thariq (Anthropic) — 18 mai 2026, 758k vues"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/prompt-engineering"
  - "#pattern/spec-driven"
---

## Pattern

Pendant que Claude implémente une spec, lui demander de tenir en parallèle un fichier `implementation-notes.md` (ou `.html`) qui documente tout ce qui sort du spec écrit. Le fichier vit *pendant* le travail, pas *après* via un hook post-commit.

## Prompt canonique (version finale Thariq, raffinée avec Claude)

```
Implement <SPEC>. As you work maintain a running implementation-notes.html file
that captures anything I should know about how the implementation diverges from
or interprets the spec, including:

- Design decisions: choices you made where the spec was ambiguous
- Deviations: places where you intentionally departed from the spec, and why
- Tradeoffs: alternatives you considered and why you picked what you did
- Open questions: anything you'd want me to confirm or revise
```

Version courte (tweet original, 758k vues) :

```
implement <SPEC> and while you do, keep a running implementation-notes.html
file (or markdown) with decisions you had to make weren't in the spec, things
you had to change, tradeoffs you had to make or anything else I should know
```

## Pourquoi ça marche

- Aucune spec n'est complète — il reste toujours des **unknown unknowns** et des ambiguïtés
- Sans cette consigne, Claude prend des décisions silencieuses qu'on découvre dans le diff (ou jamais)
- Le fichier donne au modèle "a good out to make decisions but keep you in the loop" (Thariq)
- Le coût marginal est minime (un fichier append-only), le gain en review est énorme

## 4 sections du fichier

| Section | Contenu | Exemple |
|---------|---------|---------|
| **Design decisions** | Choix faits où la spec était ambiguë | "Spec ne précise pas le format des erreurs API → j'ai utilisé Problem Details RFC 7807" |
| **Deviations** | Départ intentionnel de la spec, avec raison | "Spec demande Redis pour le cache, j'ai utilisé in-memory LRU car volume < 10k entries" |
| **Tradeoffs** | Alternatives considérées + pourquoi le choix | "Option A async queue vs Option B sync avec retry — choisi B pour simplicité de debug" |
| **Open questions** | Demandes de confirmation à l'humain | "Confirme : les rate limits s'appliquent par user ou par API key ?" |

## Différence avec spec-driven development

| Aspect | [[pattern-spec-driven-development]] | Running implementation notes (ce pattern) |
|--------|-------------------------------------|-------------------------------------------|
| Quand | Avant + Après l'implémentation | **Pendant** l'implémentation |
| Outil | SPEC.md + hook post-commit | Fichier vivant maintenu par Claude |
| Cible | Décisions extraites du diff | Décisions verbalisées en temps réel |
| Lourdeur | Setup pipeline, agents, hooks | Une ligne dans le prompt |
| Couvre | Décisions visibles dans le code | Aussi : ambiguïtés, tradeoffs non-évidents, questions |

Les deux patterns sont **complémentaires** : SDD capture le quoi (changements de code), running notes capture le pourquoi (décisions et incertitudes).

## Quand utiliser

- TOUTE implémentation à partir d'une spec écrite (long PR, feature complète)
- Particulièrement utile quand la spec vient d'une autre personne (PM, autre dev)
- Combinable avec n'importe quel workflow Claude Code (avec ou sans plugins)
- Excellent en début de session `/expand` → spec → "implement avec running notes"

## Anti-patterns

- Ne PAS demander au modèle de re-décrire ce qu'il a fait (= duplicate diff)
- Ne PAS confondre avec un changelog (le changelog dit "j'ai fait X", les notes disent "j'ai dû choisir X parce que Y était ambigu")
- Ne PAS attendre la fin pour écrire — le pattern repose sur le caractère **running** (append au fur et à mesure)

## Variante avancée — combiner avec subagents

Pour grosses features : un subagent read-only explore, écrit un fichier `exploration-notes.md`, le main agent l'utilise pour implémenter en maintenant `implementation-notes.md`. Voir [[subagent-explore-then-edit]].

## Liens

- [[pattern-spec-driven-development]] — Workflow lourd complémentaire
- [[pattern-sdd-triangle]] — Triangle spec / code / décisions
- [[Thariq]] — Auteur du pattern
- [[subagent-explore-then-edit]] — Pattern complémentaire pour grosses features
