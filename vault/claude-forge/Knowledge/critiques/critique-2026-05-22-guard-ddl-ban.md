---
titre: "Critique — guard-ddl-ban.py (hook PreToolUse Bash neo_ia)"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-22
auteur: claude
aliases:
  - "critique guard-ddl-ban"
  - "da hook ddl ban neo_ia"
  - "verdict keep ddl enforcement"
  - "critique ddl gate runtime security"
  - "DA hook database rule enforcement"
tags:
  - "#type/critique"
  - "#domaine/claude-code"
  - "#domaine/hooks"
  - "#projet/neo_ia"
resume: "DA sur guard-ddl-ban.py — verdict KEEP avec 3 corrections mineures (bypass env var, retirer alembic du runner, couvrir trou python script.py). Différencier de doctrine-drift-guard : ici gate security légitime (DDL prod = irréversible), pas workflow agentique sur méta-doctrine."
---

# Critique — guard-ddl-ban.py (hook PreToolUse Bash neo_ia)

## Contexte

Promotion en enforcement 100% de la rule `database-rules.md` (interdiction DDL) via hook Bash qui bloque psql/python -c contenant CREATE/ALTER/DROP/TRUNCATE/GRANT/REVOKE + `Base.metadata.create_all`/`checkpointer.setup`. Inscrit dans settings.json PreToolUse matcher "Bash". 20 tests adverses passent.

## Verdict : LIVRER AVEC CORRECTIONS (KEEP)

Bloquants : 0 | Avertissements : 3 | Nitpicks : 2

Ce hook n'est PAS l'anti-pattern doctrine-drift-guard ([[critique-2026-05-22-doctrine-drift-guard]]).

| Critère | doctrine-drift-guard (BLOQUÉ 22 mai) | guard-ddl-ban (KEEP) |
|---------|--------------------------------------|----------------------|
| Cible | Texte d'opinion (MEMORY/RECAP) | Commande shell exécutable |
| Risque protégé | Régression doctrinale (méta-process) | Corruption schéma DB prod (sécurité opérationnelle) |
| Fréquence du risque | Pivot ~1×/trimestre | Action quotidienne dans un repo Python+PG |
| Catégorie doctrine | Workflow agentique (interdite) | Security/DDL gate (autorisée) |
| Signal-to-noise | 26/26 faux positifs | Faible bruit (DDL hors migrations = rare) |

La doctrine 22 mai ([[raisonnement-22mai-doctrine-vs-enforcement]]) autorise explicitement « lint / security / scope ». Bloquer DDL sur DB partagée = sécurité opérationnelle, pas workflow.

## Corrections recommandées

1. **Bypass env var** (avt 1) — ajouter `if os.environ.get("DDL_BAN_BYPASS") == "1": sys.exit(0)`. Évite édition manuelle settings.json en dev local.
2. **Retirer alembic** du SQL_RUNNER_PATTERN — `alembic upgrade head` ne contient pas de mot DDL dans la commande shell, le DDL est dans les fichiers migrations versionnés (alembic ne lit pas `-c`). Inclusion trompeuse. neo_ia n'utilise pas alembic d'ailleurs.
3. **Couvrir trou `python script.py`** (avt 2) — soit accepter explicitement (« on bloque inline, pas les scripts ; review code couvre »), soit ajouter PostToolUse Edit/Write qui grep ces patterns dans .py modifiés.

## Forces réelles

- 20 tests adverses passent — testé empiriquement (contrairement à 90% des hooks similaires)
- Normalisation backslash-escape `\\(\s)` → `\1` traite vrai bypass courant
- Filtre SQL_RUNNER en première passe évite faux positifs grossiers sur grep/cat/edit

## Avertissements

- **Trou `python script.py`** : hook voit la commande Bash, pas le contenu du script. Un dev qui fait `python migrate_dev.py` où le fichier contient `Base.metadata.create_all(engine)` n'est PAS bloqué. Rule dit « never auto-create » — hook ne couvre que la fraction `-c` inline. Faux sentiment de sécurité partiel.
- **Pas de distinction prod / test / dev** : bloque indistinctement `psql -h prod` (danger réel) et `psql -h localhost -c "CREATE TABLE TEST_foo"` (cas dev légitime). Sur-bloque le dev local. Le bypass env var résoudrait.
- **Coût de mort lente** : si bypass manque, devs commentent le hook entier au lieu de l'évoluer. Pattern classique d'abandon par friction.

## Nitpicks

- `alembic\s+upgrade` cosmétique (cf correction 2)
- `GRANT\s+\w+` légèrement permissif sur `GRANTED_BY` mais `\b` + `\s+` requiert espace, faux positif théorique

## Différence avec doctrine-drift-guard (vault context)

DA 22 mai bloqué hook qui transformait *règle de méthode* en sensor permanent. Ici on transforme *règle d'opérations DB* en gate runtime. La règle d'ops est binaire (DDL = bloqué), pas contextuelle. Le gate fonctionne.

## Liens

- [[critique-2026-05-22-doctrine-drift-guard]] — précédent différencié
- [[raisonnement-22mai-doctrine-vs-enforcement]] — doctrine source
- [[comment-creer-hook]] — canonique forge hook
- [[trail-of-bits-config]] — setup entreprise sécu publique
