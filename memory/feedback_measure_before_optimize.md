---
name: measure-before-optimize-tests
description: "Avant de proposer un plan d'optimisation tests, mesurer le coût unitaire réel + --durations pour distinguer \"trop de tests\" vs \"chaque test trop lent\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4737c3cd-d380-4c1b-b98a-0978cfcbc5cd
---

Avant de proposer un plan d'optim de tests (perçu lent), TOUJOURS mesurer empiriquement avant de conclure :
1. Compter les tests réels (filtrer `.venv/` qui pollue les counts find/grep)
2. Lancer UN fichier avec `--durations=10 --no-header` pour voir le coût unitaire et identifier setup vs call
3. Si top durations = 100% setup/teardown → le fixture est le coupable, pas le volume
4. Chercher les autouse fixtures dans conftest.py racine en priorité

**Why:** Sur neo_ia 2026-05-21, user dit "6000 tests, 10 minutes". Réalité : 2166 tests (les 6000 venaient de `.venv/Lib`), et 460 ms/test à cause d'un `clean_caches` autouse + 2 gc.collect() par test. Sans la mesure, j'aurais proposé "lancez moins de tests" alors que le vrai problème était "chaque test est 10x trop lent".

**How to apply:** Toute plainte "les tests sont lents" déclenche : `pytest <un_fichier> --durations=10 --no-header` avant tout plan. Si setup/teardown domine → chercher autouse global. Si call domine → chercher I/O réels (DB, LLM, réseau) qui auraient dû être mockés.
