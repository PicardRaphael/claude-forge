---
name: python-ref
description: ALWAYS load this reference when writing, reviewing, or debugging Python code. Covers Python 3.11+ best practices, patterns, testing, and packaging. Do NOT write Python without loading this first.
model: sonnet
effort: medium
user-invokable: false
---

# Python 3.11+ — Reference

Reference Python generique. Charger quand on ecrit, relit ou genere du code Python — tout projet.

---

## Stack courante

| Composant | Outil |
|-----------|-------|
| Runtime | Python 3.11+ |
| Tests | pytest (fixtures, parametrize, tmp_path, conftest.py) |
| Serveurs MCP | FastMCP |
| Config | PyYAML (`safe_load` uniquement) |
| Stockage léger | SQLite (module `sqlite3` intégré) |
| Background | asyncio |

---

## Structure projet canonique

```
project/
  src/
    __init__.py
    server.py          # Point d'entrée
    config.py          # Dataclasses de config + loader YAML
    database.py        # Couche données
    tools/             # Modules fonctionnels
      __init__.py
      module.py
  tests/
    __init__.py
    conftest.py        # Fixtures partagées
    test_module.py
  config.yaml
  pyproject.toml
```

---

## Conventions de code

- **Type hints partout** — paramètres et retours, sans exception
- **dataclasses** pour les modèles (pas de dicts anonymes)
- **pathlib.Path** pour tous les chemins — jamais `os.path`
- **f-strings** pour le formatting
- `from __future__ import annotations` si forward references nécessaires
- **Docstrings une ligne max** — uniquement si le nom ne suffit pas
- **Pas de `print()` en production** — `logging` si besoin

---

## TDD

- Test d'abord, implémentation ensuite
- `python -m pytest` (jamais `pytest` direct — voir Gotchas)
- Fixtures dans `conftest.py` pour le partage entre tests
- `tmp_path` pour les fichiers temporaires
- Nommer les tests : `test_<comportement_attendu>`

```python
# conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    p = tmp_path / "config.yaml"
    p.write_text("key: value", encoding="utf-8")
    return p
```

---

## SQLite best practices

```python
import sqlite3

conn = sqlite3.connect("db.sqlite3")
conn.row_factory = sqlite3.Row          # résultats dict-like
conn.execute("PRAGMA journal_mode=WAL") # multi-lecteurs
conn.execute("PRAGMA foreign_keys=ON")  # intégrité référentielle

# Paramétrer TOUJOURS — jamais de f-string SQL
conn.execute("SELECT * FROM items WHERE id = ?", (item_id,))
```

### FTS5

```sql
-- Créer la table FTS5
CREATE VIRTUAL TABLE items_fts USING fts5(
    title, body,
    content=items,
    tokenize='unicode61 remove_diacritics 2'
);

-- bm25() pour le ranking pondéré (négatif = meilleur score)
SELECT * FROM items_fts
WHERE items_fts MATCH ?
ORDER BY bm25(items_fts, 10.0, 1.0);
```

**Attention** : avec `content=` table, les INSERT/DELETE sur la table source ne propagent PAS vers FTS automatiquement. Voir Gotchas.

---

## FastMCP best practices

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mon-serveur")

@mcp.tool()
def search_items(query: str, limit: int = 10) -> list[dict]:
    """Recherche des items par texte. Retourne une liste d'items matchés."""
    # type hints → schéma auto-généré
    # docstring → description pour Claude
    ...

# Transport local
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

## Gotchas

- **`python` vs `python -m pytest`** : sur Windows Git Bash, `python` peut résoudre vers le mauvais binaire ou vers le store Windows. Toujours `python -m pytest`.
- **Hook global + `python -c "..."`** : le hook bloque les commandes Python multi-lignes en ligne. Écrire un `.py` temporaire et l'exécuter à la place.
- **SQLite FTS5 `content=` table** : les INSERT/DELETE dans la table source ne mettent PAS à jour la FTS automatiquement. Synchroniser manuellement avec `INSERT INTO items_fts(...)` et `DELETE FROM items_fts WHERE rowid = ?`.
- **PyYAML** : toujours `yaml.safe_load()`, jamais `yaml.load()` (exécution arbitraire).
- **Encoding** : toujours `encoding="utf-8"` sur `open()`, `Path.read_text()`, `Path.write_text()`. Windows peut utiliser cp1252 par défaut.
- **asyncio + SQLite** : `sqlite3` n'est pas thread-safe par défaut. Utiliser `check_same_thread=False` ou `aiosqlite` pour les contextes async.
- **dataclasses et YAML** : `@dataclass` ne désérialise pas depuis dict automatiquement — utiliser `dacite.from_dict()` ou un loader explicite.
- **pytest imports** : sans `src/` dans `PYTHONPATH`, les imports échouent. Ajouter `pythonpath = ["src"]` dans `pyproject.toml` section `[tool.pytest.ini_options]`.

---

## pyproject.toml minimal

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mon-projet"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.hatch.build.targets.wheel]
packages = ["src"]
```

---

## Apprentissage

Patterns et gotchas découverts pendant le dev — enrichir au fil des projets.

> Mettre à jour via : `memory: project` ou noter dans `vault/claude-forge/04-Techniques/`

| Date | Projet | Découverte |
|------|--------|------------|
| — | — | — |
