---
titre: bdd
resume: Repo PG/PL-pgSQL Neoteem — 2779 fichiers, fonctions métier, base de données
aliases:
  - bdd
  - base de données
  - database
  - postgresql neoteem
  - bdd neoteem
type: context
status: active
derniere-maj: 2026-05-09
auteur: claude
tags:
  - "#type/context"
  - "#type/projet"
  - "#projet/bdd"
---

## Description

Repo PostgreSQL/PL-pgSQL de [[Neoteem|Neoteem]]. ~65 schémas, 2779 fichiers SQL, ~10 devs.

## Schémas principaux

public, proprietaire, comptabilite, requete, suivicopro, suivilocataire, ag, lettrage, ia. Le schéma `ia` est appelé par [[ia_back|ia_back]] — ne jamais casser ses signatures.

## Composants Claude Code (déployé 2026-04-07)

- **3 agents** : sql-dev (vert), sql-bugfix (rouge), migration-writer (orange)
- **4 skills** : sql-reviewer, impact-analyzer, find-function, schema-map
- **2 rules** : sql-conventions, routing
- **1 hook** : sql_commit_validator.py

## Contraintes

- Git : Bitbucket `neot-v2/bdd`, branches protégées release/test → prépilote → master
- Commits obligatoires avec N2-XXXXX (Jira)

## Liens

- [[Neoteem|Neoteem]]
