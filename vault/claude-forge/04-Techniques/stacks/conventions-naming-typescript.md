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


---

## AJOUT 10 juin 2026 (soir) — Organisation par DOMAINE métier + limites de taille (post-incident US1)

Incident US1 neoteem-back-ts (schéma généré monolithique 3161 lignes) → 3 décisions Raphael gravées dans `doc/conventions.md` § 2bis + CDC §6.1 + rule `file-size-limit` :

1. **Vertical slice × hexagonal** (état de l'art vérifié web — Sairyss/domain-driven-hexagon, vertical-slice guides) : le 1er niveau de dossiers de CHAQUE package = le domaine métier ; 1 use-case = 1 dossier. Les couches répondent « comment les dépendances coulent », les domaines « où vit quoi ».
2. **Domaines canoniques issus du MÉTIER RÉEL** (pas inventés) : `commun` · `syndic` · `gerance` · `comptabilite` · `reporting` — sources : modules du Damier Lojii (Syndic/Gérance/Commun/Admin, glossaire neoteem-brain) + taxonomie `01-Domaines/` + organisation des 50 schémas BDD (MOC-BDD). Liste fermée, ajout = décision humaine. Affectation ambiguë → brain (`neo-brain-dev-ia`), jamais devinée.
3. **Limite stricte de taille** : aucun fichier source > 1000 lignes, JAMAIS — triple capteur (hook `file-size-guard` PreToolUse + `scripts/check-file-sizes.ts` en CI et `/go` pour attraper les fichiers générés par scripts + review). Visé : ~200-300 lignes/fichier, ~40 lignes/fonction. Schéma généré = fichiers de domaine (mapping déclaratif `schema-domains.json`, `_a-classer` fait échouer le test).

Méthode réutilisable pour tout futur repo : interroger le brain métier pour la liste des domaines AVANT d'inventer une taxonomie technique.

## CORRECTIF 10 juin (soir, 2e passe) — Deux axes, pas un : la leçon du croisement multi-sources

L'AJOUT ci-dessus classait TOUT par domaine métier — corrigé après croisement avec l'articulation RÉELLE de la BDD (brain `schema-public`) : le schéma `public` est PARTAGÉ entre métiers (`T_CONTRAT` porte baux ET mandats, `T_ACTEUR` polymorphe) — un classement métier du SCHÉMA serait artificiel.

**Doctrine finale (back-ts a43e32a)** : Axe 1 — la LOGIQUE (use-cases/routes/queries) par domaine MÉTIER (`commun·syndic·gerance·comptabilite·reporting`, Damier Lojii) ; Axe 2 — le SCHÉMA GÉNÉRÉ par groupes d'ARTICULATION BDD (`acteurs-roles·patrimoine·comptabilite·travaux-fournisseurs·relances·dossiers-ged·referentiels·reporting`).

**Méthode gravée** : une taxonomie d'architecture se décide en CROISANT plusieurs sources du brain (Damier/glossaire × 01-Domaines × MOC-BDD × schema-public) — une seule source (le Damier seul) = conclusion fragile, corrigée par Raphael. Skill à invoquer : `/neoteem-brain-dev-ia:neo-brain-dev-ia`.