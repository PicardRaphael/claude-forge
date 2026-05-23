---
titre: "Running Implementation Notes — Pattern Thariq (Anthropic)"
resume: "Pendant l'implémentation d'une spec, Claude maintient un fichier implementation-notes.md vivant qui capture décisions d'ambiguïté, déviations, tradeoffs et open questions. Thariq Shihipar 19 mai 2026"
aliases:
  - "running implementation notes"
  - "implementation-notes.md pattern"
  - "implementation notes thariq"
  - "spec ambiguity notes"
  - "decisions log live"
  - "thariq implementation pattern"
domaine: prompt-engineering
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://x.com/trq212"
  - "https://abmedia.io/thariq-anthropic-claude-code-prompt-implementation-notes-may-2026"
  - "https://www.chatprd.ai/how-i-ai/claude-code-anthropic-thariq-shihipar-on-replacing-markdown-with-html"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/prompt-engineering"
  - "#pattern/spec-driven"
---

## Pattern

Pendant que Claude implémente une spec, lui demander de tenir en parallèle un fichier `implementation-notes.md` (ou `.html`) qui documente tout ce qui sort du spec écrit. Le fichier vit *pendant* le travail, pas *après* via un hook post-commit.

**Auteur** : Thariq Shihipar (Anthropic Claude Code lead). Tweet original daté **19 mai 2026** (relayé par ABMedia, ChatPRD, Lenny's Newsletter).

> ⚠️ Note : l'URL de tweet exact `x.com/trq212/status/...` doit être récupérée directement via x.com/trq212 timeline (paywall API). Tweet attesté par 2+ sources tierces convergentes.

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

Version courte (tweet original) :

```
implement <SPEC> and while you do, keep a running implementation-notes.html
file (or markdown) with decisions you had to make weren't in the spec, things
you had to change, tradeoffs you had to make or anything else I should know
```

## Pourquoi ça marche

- Aucune spec n'est complète — il reste toujours des **unknown unknowns** et des ambiguïtés
- Sans cette consigne, Claude prend des décisions silencieuses qu'on découvre dans le diff (ou jamais)
- Le fichier donne au modèle "a good out to make decisions but keep you in the loop" (Thariq)
- Le coût marginal est minime (fichier append-only), le gain en review est énorme

## 4 sections du fichier

| Section | Contenu | Exemple |
|---------|---------|---------|
| **Design decisions** | Choix faits où la spec était ambiguë | "Spec ne précise pas le format des erreurs API → Problem Details RFC 7807" |
| **Deviations** | Départ intentionnel de la spec, avec raison | "Spec demande Redis, j'ai utilisé in-memory LRU car volume < 10k entries" |
| **Tradeoffs** | Alternatives considérées + pourquoi le choix | "Option A async queue vs Option B sync avec retry — choisi B pour simplicité debug" |
| **Open questions** | Demandes de confirmation à l'humain | "Confirme : rate limits par user ou par API key ?" |

## Différence avec spec-driven development

| Aspect | [[pattern-spec-driven-development]] | Running implementation notes |
|--------|-------------------------------------|------------------------------|
| Quand | Avant + Après l'implémentation | **Pendant** l'implémentation |
| Outil | SPEC.md + hook post-commit | Fichier vivant maintenu par Claude |
| Cible | Décisions extraites du diff | Décisions verbalisées en temps réel |
| Lourdeur | Setup pipeline, agents, hooks | Une ligne dans le prompt |

Les deux patterns sont **complémentaires** : SDD capture le quoi (changements de code), running notes capture le pourquoi.

## Quand utiliser

- TOUTE implémentation à partir d'une spec écrite (long PR, feature complète)
- Particulièrement utile quand la spec vient d'une autre personne (PM, autre dev)
- Combinable avec n'importe quel workflow Claude Code

## Anti-patterns

- Ne PAS demander au modèle de re-décrire ce qu'il a fait (= duplicate diff)
- Ne PAS confondre avec un changelog
- Ne PAS attendre la fin pour écrire — le pattern repose sur le caractère **running**

## Métriques tweet (mises à jour 2026-05-23)

- **951 likes, 44 retweets** confirmés via ABMedia
- Claim "758k vues" non confirmé dans les sources publiques

## Liens

- [[pattern-spec-driven-development]]
- [[pattern-sdd-triangle]]
- [[Thariq Shihipar]]
- [[Silent Assumptions]] — anti-pattern complémentaire (Karpathy)
