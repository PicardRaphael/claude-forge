# Neoteem Backend — Choix techniques et pourquoi

*Document à destination de la direction — version accessible, sans jargon inutile.*

---

## Le problème qu'on résout

Aujourd'hui, toute la logique métier de Loji est enfermée dans des fonctions PostgreSQL.
C'est comme si toute l'intelligence de l'application était écrite dans le moteur de la base
de données — un endroit conçu pour stocker des données, pas pour gérer des règles métier.

**Conséquences concrètes :**
- Impossible de tester les règles métier de manière isolée
- Chaque modification risque de casser autre chose sans qu'on le sache
- Très difficile pour un nouveau développeur de comprendre le code
- L'agent IA (chatbot) tape directement dans la base sans contrôle
- Pas de documentation vivante de l'API

**L'objectif :** construire un vrai backend applicatif qui se place ENTRE la base
de données et les consommateurs (agent IA, futur frontend). Ce backend contrôle,
valide, et documente tout ce qui entre et sort.

---

## Pourquoi TypeScript et pas Go ?

| Critère | TypeScript | Go |
|---------|-----------|-----|
| Claude Code (notre outil de dev) | Excellent — c'est le langage que Claude maîtrise le mieux | Bon mais moins fluide |
| SDKs IA (Anthropic, Google, OpenAI) | Natifs et prioritaires en TypeScript | Disponibles mais secondaires |
| Recrutement Grenoble | Large vivier | Plus restreint, profils plus chers |
| Partage de code avec le futur frontend | Direct — le front sera aussi en TypeScript | Impossible — deux langages différents |
| Rapidité de développement | Très rapide, surtout assisté par IA | Plus verbeux, plus de code pour le même résultat |
| Performance | Très suffisante pour un ERP API | Supérieure sur le papier, mais non nécessaire ici |

**Verdict :** Go serait un bon choix pour un système à très haute performance
(moteur de trading, infrastructure réseau). Pour un ERP qui sert des cabinets
immobiliers via API, TypeScript offre un meilleur ratio productivité/qualité,
surtout avec Claude Code comme outil principal.

---

## Pourquoi Bun et pas Node.js ?

Bun est un runtime JavaScript plus récent et plus rapide que Node.js.
Anthropic (le créateur de Claude) a acquis Bun en décembre 2025.
Bun est maintenant l'infrastructure qui propulse Claude Code.

**Ce que ça change concrètement :**
- Démarrage 3 à 4× plus rapide → nos conteneurs Cloud Run répondent plus vite
- Outils intégrés (tests, build, packages) → moins de configuration, moins de bugs d'outillage
- Alignement avec Claude Code → le code généré par Claude est nativement optimisé pour Bun
- Adopté en production par Midjourney, Lovable et d'autres scale-ups

**Risque :** écosystème plus jeune que Node.js. Mais pour notre usage (API backend
avec des librairies standards), la compatibilité est à 95%+.

---

## Pourquoi REST et pas GraphQL ?

Notre API sert deux consommateurs :
1. L'agent IA (Python/LangGraph) → a besoin d'endpoints simples et prévisibles
2. Le futur frontend → a besoin d'endpoints documentés

REST est le standard universel. Tout le monde le comprend, tout client peut l'appeler,
et la documentation se génère automatiquement (OpenAPI/Swagger).

GraphQL serait pertinent si on avait un frontend complexe avec des dizaines de vues
différentes qui demandent des données très variées. Ce n'est pas notre cas en V1.

**Bonus :** des endpoints REST bien décrits se convertissent facilement en outils
MCP (le standard émergent pour connecter des IA à des services). C'est une porte
ouverte vers le futur sans effort supplémentaire maintenant.

---

## Pourquoi Drizzle et pas Prisma ?

Drizzle et Prisma sont deux "traducteurs" entre le code TypeScript et PostgreSQL.

Prisma est plus connu et plus simple pour les débutants. Mais pour Neoteem :

- **Notre base existe déjà** avec des centaines de tables. Drizzle permet d'introspecter
  le schéma existant et de travailler avec tel quel, sans forcer une migration.
- **Drizzle est proche du SQL** — les développeurs qui connaissent PostgreSQL
  ne sont pas dépaysés. Prisma impose sa propre logique qui peut surprendre
  sur des requêtes comptables complexes.
- **Drizzle est 8× plus léger** → démarrage plus rapide sur Cloud Run.
- **Pas de génération de code** → le cycle de développement est plus fluide,
  surtout avec Claude Code.

---

## Pourquoi un seul repo simple (pas de monorepo) ?

Un seul dépôt Git, un seul `package.json`, une structure de dossiers bien découpée.
Pas de monorepo multi-packages (Turborepo, Nx) — c'est surdimensionné pour la V1.

**Avantages concrets pour Neoteem :**
- Configuration minimale — un seul `package.json`, un seul `tsconfig.json`
- Claude Code voit tout le projet d'un coup → génère du code cohérent
- Zéro complexité de workspaces ou de résolution de packages
- Un nouveau développeur clone le repo et peut coder en 5 minutes
- La séparation architecturale est dans les dossiers, pas dans le packaging

**Alternative rejetée pour l'instant :** monorepo multi-packages (Turborepo) —
pertinent quand le frontend rejoindra le même repo ou quand on aura 50+ modules.
La migration est simple car les dossiers ont la même structure.

---

## Pourquoi l'architecture hexagonale ?

C'est le choix qui protège notre investissement à long terme.

**Le principe :** le code métier (les règles de gestion de copropriété,
la comptabilité, les appels de fonds) est isolé dans un "noyau" qui ne dépend
d'aucune technologie.

```
Si demain on change de base de données → seul l'adaptateur DB change
Si demain on change de framework HTTP  → seul l'adaptateur HTTP change
Si demain on ajoute un nouveau client  → on ajoute un adaptateur, le métier reste
```

**Sans architecture hexagonale :** le code métier est mélangé avec le code technique.
Changer une technologie implique de tout réécrire. C'est exactement le problème
qu'on a aujourd'hui avec les fonctions PostgreSQL.

**Avec :** les règles métier sont écrites une seule fois, testées indépendamment,
et réutilisables quel que soit le contexte technique.

**Coût :** un peu plus de fichiers et de structure au départ. Mais c'est ce qui rend
le code maintenable sur 5-10 ans au lieu de recréer de la dette technique.

---

## Pourquoi CQRS light (séparation lecture/écriture) ?

On sépare les opérations de lecture (consulter un solde, lister des lots)
et d'écriture (créer un appel de fonds, enregistrer une écriture).

**Pourquoi :** les lectures et les écritures ont des besoins différents.
Les lectures doivent être rapides et peuvent être mises en cache.
Les écritures doivent être fiables et vérifiées.

**"Light" :** on fait cette séparation dans le code uniquement, pas dans l'infrastructure.
On garde une seule base de données, un seul service. Pas de surcoût d'infrastructure.

Si un jour on a 500 cabinets qui consultent des dashboards en même temps,
on pourra séparer physiquement les lectures sur un serveur dédié (read replica)
sans toucher au code métier.

---

## Stratégie de migration

On ne jette pas l'existant. On construit le nouveau à côté.

```
Phase 1 (V1) : Backend pour l'agent IA
              → 3 à 10 endpoints, périmètre chatbot
              → Prouve que l'architecture fonctionne

Phase 2 (V2) : Migration progressive des fonctions métier
              → On extrait les fonctions PostgreSQL une par une
              → L'ancien et le nouveau coexistent (pattern Strangler Fig)

Phase 3 (V3) : Backend commun IA + Frontend
              → Le frontend utilise la même API que l'agent IA
              → Les fonctions PostgreSQL sont progressivement abandonnées
```

Ce modèle est éprouvé — c'est exactement ce que font les grandes entreprises
quand elles modernisent un système legacy sans interrompre la production.

---

## Résumé des choix

| Décision | Choix | Alternative rejetée | Raison principale |
|----------|-------|--------------------|--------------------|
| Langage | TypeScript | Go | Productivité, Claude Code, recrutement |
| Runtime | Bun | Node.js | Performance, propriété Anthropic |
| Framework | Hono | NestJS, Fastify | Légèreté, Cloud Run, Claude Code |
| API style | REST + OpenAPI | GraphQL | Simplicité, agent IA Python, futur MCP |
| ORM | Drizzle | Prisma | SQL-first, schéma existant, performance |
| Structure repo | Single repo + dossiers | Monorepo, repos séparés | Simplicité V1, migration facile |
| Architecture | Hexagonale | Aucune / en couches simple | Testabilité, évolutivité, dette maîtrisée |
| Base | PostgreSQL (conservée) | — | Existante, pas de migration DB en V1 |
| Déploiement | Cloud Run / Docker | — | Infrastructure existante conservée |

---

## Ce que ça change concrètement

**Avant :** un changement de règle métier = modifier une fonction SQL dans DataGrip,
espérer que ça ne casse rien, déployer en croisant les doigts.

**Après :** un changement de règle métier = modifier un fichier TypeScript,
les tests vérifient automatiquement que rien n'est cassé, la documentation
API se met à jour toute seule, le déploiement est automatisé.

**Avant :** l'agent IA tape directement dans PostgreSQL sans contrôle.

**Après :** l'agent IA passe par une API qui valide chaque requête,
vérifie les permissions, et retourne des erreurs explicites.

**Avant :** un nouveau développeur met des semaines à comprendre le système.

**Après :** la documentation est dans le code, l'architecture est claire,
Claude Code connaît toutes les conventions et guide le développeur.
