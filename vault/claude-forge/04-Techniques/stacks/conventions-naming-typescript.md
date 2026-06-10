---
titre: Conventions de nommage TypeScript — état de l'art 2026
resume: Table de nommage TS canonique (Google/typescript-eslint/Biome) + enforcement mécanique Biome useNamingConvention/useFilenamingConvention + verdict patterns hexagonal — appliquée à neoteem-back-ts
aliases:
  - conventions nommage typescript
  - typescript naming conventions
  - naming ts
  - biome naming convention
  - kebab-case fichiers ts
type: technique
derniere-maj: 2026-06-10
auteur: claude
sources:
  - "https://google.github.io/styleguide/tsguide.html"
  - "https://typescript-eslint.io/rules/naming-convention/"
  - "https://biomejs.dev/linter/rules/use-naming-convention/"
  - "https://biomejs.dev/linter/rules/use-filenaming-convention/"
  - "https://github.com/Sairyss/domain-driven-hexagon"
  - "https://khalilstemmler.com/articles/enterprise-typescript-nodejs/clean-nodejs-architecture/"
tags:
  - "#type/technique"
  - "#domaine/typescript"
  - "#domaine/stacks"
---
# Conventions de nommage TypeScript — état de l'art 2026

Convergence Google TS Style Guide + typescript-eslint `naming-convention` + Biome.

## Table canonique

| Construct | Convention |
|---|---|
| Fichiers | `kebab-case` (+ suffixes de rôle métier : `.use-case.ts`, `.queries.ts`, `.routes.ts`, `.test.ts` colocalisé) |
| Variables / fonctions | `camelCase` (fonctions : verbe d'abord) |
| Classes / types / interfaces / enums / type params | `PascalCase` — pas de préfixe `I` |
| Schémas Zod | `PascalCase` + suffixe `Schema` (const PascalCase accepté par Biome au top-level) |
| Constantes module | `CONSTANT_CASE` |
| Acronymes | `strictCase` : `HttpServer`, jamais `HTTPServer` |
| Booléens | préfixe `is`/`has`/`can` |
| URL REST | `kebab-case`, ressources au pluriel ; JSON `camelCase` |

## Enforcement mécanique (la vraie réponse à « skill, rule ou hook ? »)

**Biome enforce nativement** — pas besoin de hook custom ni de skill :
- `useNamingConvention` (`{ "strictCase": true }`) — code.
- `useFilenamingConvention` (`{ "filenameCases": ["kebab-case", "export"] }`) — fichiers.
Brancher en `linter.rules.style` du biome.json → CI bloquante + hook format-on-write couvrent tout. Vérifié empiriquement (neoteem-back-ts, 10 juin 2026) : test positif (existant vert, `DevisSchema` accepté) ET négatif (`HTTPServer`, `Get_Devis`, fichier `BadProbeFile.ts` → 4 violations).

Architecture d'enforcement complète : Biome (nommage, 100 % déterministe) + dependency-cruiser (emplacement des patterns) + doc `conventions.md` préchargée dans les agents + reviewer (jugement du choix de pattern). Le seul étage non garantissable mécaniquement = le CHOIX du pattern → capteur reviewer.

## Verdict design patterns hexagonal TS (recherche 10 juin 2026)

Le vocabulaire CDC §6ter de [[neoteem-back-ts]] est conforme aux références (Sairyss/domain-driven-hexagon, Khalil Stemmler) : use-case = orchestration (jamais la logique métier, qui vit dans les entités), domaine/persistance séparés avec mapper seulement si divergence, agrégat = frontière transactionnelle, erreurs métier = valeurs typées (Result/Either). Patterns GoF retenus avec adaptation anti-cérémonie : Factory = **static factory method** (`Entite.create()` → Result, constructeur private), Strategy = **map de fonctions**, Singleton = **const de module**, Decorator = **middlewares**. Refusés : `Repository<T>` générique, Builder custom, Template Method/Visitor, Event Sourcing prématuré.

## Liens

- [[neoteem-back-ts]] — premier repo d'application (doc/conventions.md + biome.json)
- [[stack-typescript-ia]] — stack IA TS (complémentaire)
