---
aliases:
  - "neo-ia tests lenteur"
  - "pytest neo_ia slow"
  - "clean_caches autouse problem"
  - "test infrastructure neo_ia diagnostic"
  - "diagnostic lenteur tests neoia"
tags:
  - "#type/exploration"
  - "#projet/neo_ia"
  - "#technique/testing"
resume: "Diagnostic root cause de la lenteur des tests neo_ia : clean_caches autouse + log_cli + absence de pytest-xdist + pytest 9 incompatible options"
derniere-maj: 2026-05-21
projet: neo_ia
type: exploration
---

# Diagnostic — Lenteur tests neo_ia (10+ min pour ~2166 tests unit)

## Problème observé

Raphael : "on a énormément de problèmes quand on lance les tests, plus de 6000 tests, des fois 10 minutes pour finir, test-writer relance tous les tests".

## Mesure terrain

- **Volume réel** : 2166 tests passing (test.json), pas 6000. Les 6000 supposés sont les test_*.py de `.venv/Lib` (deps Python).
- **Coût unitaire mesuré** : `apps/neochat/tests/unit/api/test_helpers.py` = 26 tests / 12 secondes = **460 ms/test** pour du unit mocké (devrait être < 50 ms).
- **Top 10 durations** : **10/10 sont setup ou teardown**, aucun "call" dans le top → le test lui-même est rapide, le fixture est lent.
- Extrapolation : 2166 × 0.45s = **975 s ≈ 16 minutes** rien que pour les fixtures.

## Root causes (par ordre d'impact)

### 1. `clean_caches` autouse — coupable principal (≈80% du temps)

Dans `conftest.py` racine, fixture `@pytest.fixture(autouse=True)` qui execute :
- 6 imports (try/except ImportError) → 5 ratent sur les tests qui n'ont pas besoin
- 6 appels `clear_xxx_cache()` avant ET après chaque test
- 2 `gc.collect()` complets (avant + après)

Soit **4332 gc.collect() + 4332 cycles d'imports** sur une run complète.

**Historique** : ajoutée le 5 mars 2026 (commit `460b597`) en réponse à un commit antérieur `aab8a8c "Resolve asyncio event loop isolation"`. C'est un workaround, pas une fix. La vraie cause asyncio est masquée.

### 2. `log_cli = true` + `log_cli_level = INFO`

Stdout flush par test → I/O overhead non négligeable.
**Bonus bug** : pytest 9 ne reconnaît plus `log_cli_format` ni `log_cli_level` (warnings au lancement). Options mortes.

### 3. `pytest-xdist` installé mais NON utilisé

Présent dans `uv.lock` (3.8.0) mais absent de `pyproject.toml [test]` et absent de `addopts`. Sur 2000 tests unit mockés, `-n auto` = **4-8x gratuit** (8 cœurs typiquement).

### 4. Toutes les fixtures sont `scope="function"`

Aucun `scope="module"` ou `scope="session"` dans les conftest des apps/packages. Chaque test reconstruit son contexte.

### 5. Granularité agents trop large

Les agents `dev-*` finissent par `uv run pytest apps/neochat/tests/unit/ -v` = **TOUT le dossier unit** (128 fichiers neochat). Le hook `guard-pytest-scope.py` n'attrape que `pytest` nu — il laisse passer `tests/unit/`. La rule dit "par répertoire granulaire" mais les agents prennent l'app entière, pas le fichier modifié.

### 6. `pytest-rerunfailures` actif → masque flakiness

Si un test est flaky, il est rerun automatiquement → temps × 2-3 sur les flakes.

## Plan d'optimisation (par ordre ROI)

### Quick wins (gains immédiats, < 1h)

1. **Désactiver `log_cli` par défaut** (-30% temps probable)
   - Supprimer `log_cli = true` de `pyproject.toml`
   - Réactivable via `--log-cli-level=INFO` au cas par cas
   - Supprime aussi les warnings pytest 9

2. **Ajouter `pytest-xdist` actif** (-75% temps)
   - Ajouter `pytest-xdist>=3.8.0` dans `[project.optional-dependencies].test`
   - Ajouter `-n auto` dans `addopts` (ou laisser opt-in par flag)
   - Compatible avec `asyncio_mode = "auto"`

### Fix root cause (1-3h)

3. **Remplacer `clean_caches` autouse par des fixtures opt-in scopées**
   - Identifier les tests qui ont VRAIMENT besoin du clear (ceux qui ont déclenché le bug asyncio mars 5)
   - Pour les autres : utiliser `scope="session"` pour les caches stables, fixture `autouse=True` uniquement dans les conftest des dossiers concernés
   - Le clear "before AND after" est doublonnant : garder uniquement teardown
   - Mesure après chaque étape pour quantifier

### Discipline tests scope (workflow agents)

4. **Resserrer `guard-pytest-scope.py`** — bloquer aussi `tests/unit/` nu, exiger profondeur ≥ 2 sous `tests/`
   - Empêche `pytest apps/neochat/tests/unit/` → force `pytest apps/neochat/tests/unit/api/`

5. **Workflow agents `dev-*`** : depuis git diff, mapper aux fichiers test miroirs et lancer SEULEMENT ces fichiers
   - Patcher la skill `commit-push` ou créer une skill `pytest-scope-from-diff`
   - Le workflow actuel "uv run pytest apps/neochat/tests/unit/" doit devenir "uv run pytest apps/neochat/tests/unit/<sous-dossier-modifié>/test_X.py"

### Bonus (hygiène)

6. **Retirer `pytest-rerunfailures`** ou le limiter à `--reruns 1 -m flaky`
7. **Fix les options pytest 9 mortes** dans `pyproject.toml`

## Pourquoi pas la solution naïve "lancer moins de tests"

Le user perçoit "test-writer relance tous les tests" → tentation = ajouter une rule "soyez plus granulaire". Mais :
- Il y a déjà 5 rules qui disent ça
- Le vrai problème : **chaque test est trop lent** (460ms au lieu de < 50ms)
- Diviser par 10 le scope sans fixer `clean_caches` = encore 50s pour 100 tests
- Diviser par 4 avec xdist + virer `clean_caches` = même les 2166 tests passent en < 2 min

## Anti-pattern observé

L'historique git montre le pattern :
1. Bug asyncio event loop apparaît → fix rapide via cleanup global
2. Cleanup global devient autouse → ralentit tout
3. Tests deviennent lents → on découpe le scope
4. Le scope devient une rule → 5 rules qui se répètent
5. Personne ne revient sur le cleanup global

**Leçon** : un workaround autouse qui résout 77 tests cassés mérite une dette technique loggée, pas un sédiment permanent.

## Liens

- [[neoia-test-infrastructure]]
- [[boris-thariq-bestpractices]]
- Vault `Knowledge/erreurs/` (à créer après application : `erreur-clean-caches-autouse.md`)
