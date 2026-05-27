"""Tests for BrainDB.search — the FTS5/BM25 core of the brain (4 strategies).

This is the heart of the product: every search_brain call routes here. Until
2026-05-27 it had ZERO direct test coverage. A silent regression here feeds the
LLM wrong results, which cascades into wrong decisions.

The search() pipeline (database.py):
  - clean query: strip ' " - ( ) → spaces
  - tokenize, drop STOP_WORDS_FR and len<=1 tokens
  - if everything was a stop word → fall back to len>1 tokens
  - Strategy 1: AND with prefix wildcard  ("a"* "b"*)         strictest
  - Strategy 2: OR  with prefix wildcard  ("a"* OR "b"*)      looser
  - Strategy 3: OR  without wildcard      ("a" OR "b")        exact subwords
  - Strategy 4: alias expansion only (with stem variants)     last resort
  Each FTS hit set is merged with alias hits (_merge_alias_hits), deduped by path.

Corpus is a minimal, deterministic fixture (approach (a)): 5 notes chosen so
each strategy is reachable and discriminable. No real-vault export (fragile).

Run: py -m pytest tests/test_search.py -v
"""

import pytest

from src.config import FTSWeights
from src.database import BrainDB
from src.indexer import parse_note


@pytest.fixture
def db(tmp_path):
    """5-note corpus crafted so each search strategy is reachable.

    - rag-technique         : content has both 'embeddings' and 'vectoriel'
                              (Strategy 1 AND-prefix target)
    - agents-autonomes      : content has 'agents', alias 'orchestration'
    - prompt-engineering    : content has 'prompt', no 'agents'
    - fine-tuning-lora      : content has 'finetuning', alias 'LoRA'/'PEFT'
    - karpathy-leader       : NO body keyword for 'eureka'; only alias 'eureka-concept'
                              (Strategy 4 alias-only target)
    """
    vault = tmp_path / "vault"
    vault.mkdir()
    notes = {
        "rag-technique.md": """---
aliases: ["RAG", "retrieval augmented generation"]
tags: ["#technique/rag"]
---
Le RAG combine embeddings et recherche vectoriel pour augmenter le contexte.
""",
        "agents-autonomes.md": """---
aliases: ["agents", "orchestration"]
tags: ["#technique/agents"]
---
Les agents autonomes orchestrent des sous-tâches via des outils.
""",
        "prompt-engineering.md": """---
aliases: ["prompt eng", "PE"]
tags: ["#technique/prompt"]
---
Le prompt engineering structure les instructions données au modèle.
""",
        "fine-tuning-lora.md": """---
aliases: ["LoRA", "PEFT", "finetuning leger"]
tags: ["#technique/fine-tuning"]
---
Le finetuning ajuste les poids du modèle sur un corpus dédié.
""",
        "karpathy-leader.md": """---
aliases: ["Karpathy", "eureka-concept", "andrej"]
tags: ["#leader/industrie"]
---
Fiche biographique. Aucun mot-clef de recherche dans le corps du texte ici.
""",
    }
    for name, content in notes.items():
        (vault / name).write_text(content, encoding="utf-8")
    database = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    database.create_schema()
    for name, content in notes.items():
        p = vault / name
        database.index_note(parse_note(p.stem, name, content), p.stat().st_mtime)
    return database


def _stems(rows):
    return [r["file_stem"] for r in rows]


# ===========================================================================
# STRATEGY 1 — AND with prefix wildcard (strictest): all terms must co-occur
# ===========================================================================

def test_and_prefix_requires_all_terms(db):
    """'embeddings vectoriel' both live only in rag-technique → exactly that note."""
    rows = db.search("embeddings vectoriel", limit=5)
    assert "rag-technique" in _stems(rows)
    # agents-autonomes has neither term → must not appear via the AND strategy
    assert "agents-autonomes" not in _stems(rows)


def test_prefix_wildcard_matches_word_start(db):
    """'embed' (prefix of 'embeddings') matches via the "embed"* wildcard."""
    rows = db.search("embed", limit=5)
    assert "rag-technique" in _stems(rows)


# ===========================================================================
# STRATEGY 2 — OR with prefix wildcard: at least one term, looser
# ===========================================================================

def test_or_prefix_disjunction(db):
    """'prompt finetuning' — no single note has both, OR-prefix returns both owners."""
    rows = db.search("prompt finetuning", limit=5)
    stems = _stems(rows)
    assert "prompt-engineering" in stems
    assert "fine-tuning-lora" in stems


# ===========================================================================
# STRATEGY 3 — OR without wildcard (exact subwords)
# ===========================================================================

def test_exact_word_match(db):
    """'agents' appears verbatim in agents-autonomes content."""
    rows = db.search("agents", limit=5)
    assert "agents-autonomes" in _stems(rows)


# ===========================================================================
# STRATEGY 4 — alias-only expansion (last resort): term lives only in an alias
# ===========================================================================

def test_alias_only_expansion(db):
    """'eureka' is NOT in any note body; only karpathy-leader has alias 'eureka-concept'.
    FTS strategies 1-3 find nothing → strategy 4 (alias expansion) recovers it."""
    rows = db.search("eureka", limit=5)
    assert "karpathy-leader" in _stems(rows)


def test_alias_expansion_stem_variant(db):
    """_like_variants strips trailing plural/e: alias 'agents' found by query 'agent'."""
    # 'agent' (singular) should still surface agents-autonomes via alias 'agents'
    rows = db.search("agent", limit=5)
    assert "agents-autonomes" in _stems(rows)


# ===========================================================================
# STOP WORDS — French stop words must be dropped before querying
# ===========================================================================

def test_stop_words_dropped(db):
    """'le rag et les embeddings' — stop words (le/et/les) dropped, real terms kept."""
    rows = db.search("le rag et les embeddings", limit=5)
    assert "rag-technique" in _stems(rows)


def test_all_stop_words_fallback(db):
    """Query made ONLY of stop words → fallback keeps len>1 tokens so we don't crash.
    'le la les' are all <=3-char stop words; result is empty list, not an error."""
    rows = db.search("le la les", limit=5)
    assert isinstance(rows, list)  # no exception; may be empty


def test_empty_query_returns_empty(db):
    """Empty / punctuation-only query → empty list, never an exception."""
    assert db.search("", limit=5) == []
    assert db.search("   ", limit=5) == []


# ===========================================================================
# QUERY SANITIZATION — quotes, dashes, parens stripped (FTS injection safety)
# ===========================================================================

def test_query_with_quotes_does_not_crash(db):
    """Double/single quotes are stripped by the clean regex — no FTS syntax error."""
    rows = db.search('"embeddings" vectoriel', limit=5)
    assert isinstance(rows, list)
    assert "rag-technique" in _stems(rows)


def test_query_with_dash_and_parens(db):
    """Dashes and parens are sanitized — 'fine-tuning (lora)' must not raise."""
    rows = db.search("finetuning (lora)", limit=5)
    assert isinstance(rows, list)


def test_query_with_fts_operators_safe(db):
    """Bare FTS operators in user text must not break the query (sanitized/quoted)."""
    for hostile in ["embeddings OR", "AND vectoriel", "NEAR(x y)", "* embeddings"]:
        rows = db.search(hostile, limit=5)
        assert isinstance(rows, list)  # never raises


# ===========================================================================
# LIMIT — result count is bounded
# ===========================================================================

def test_limit_respected(db):
    """A broad OR query is capped at `limit` results."""
    rows = db.search("rag agents prompt finetuning karpathy", limit=2)
    assert len(rows) <= 2


def test_limit_one(db):
    rows = db.search("agents prompt finetuning", limit=1)
    assert len(rows) <= 1


# ===========================================================================
# CONTEXT SNIPPET — context=True adds a snippet field, context=False omits it
# ===========================================================================

def test_context_true_has_snippet(db):
    rows = db.search("embeddings", limit=5, context=True)
    assert rows
    assert "context" in rows[0]


def test_context_false_no_snippet(db):
    rows = db.search("embeddings", limit=5, context=False)
    assert rows
    assert "context" not in rows[0]


# ===========================================================================
# RANKING / MERGE — alias hits merged into FTS hits, deduped by path
# ===========================================================================

def test_merge_dedupes_by_path(db):
    """A note matching both via content AND alias must appear exactly once.
    'agents' matches agents-autonomes by content (strat 3) and by alias (expansion)."""
    rows = db.search("agents", limit=5)
    paths = [r["path"] for r in rows]
    assert len(paths) == len(set(paths))  # no duplicate paths


def test_result_shape(db):
    """Every result row exposes path + file_stem + score."""
    rows = db.search("embeddings", limit=5)
    assert rows
    for r in rows:
        assert "path" in r and "file_stem" in r and "score" in r


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
