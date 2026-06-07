"""Tests des variantes *_by_path — Chantier 6-B.

Les 4 outils d'ecriture coeur (update_note, append_note, insert_section, update_property)
resolvent par file= via resolve_note (FTS) -> AMBIGU quand plusieurs notes partagent le
meme stem (log.md, index.md, CHANGELOG.md existent dans plusieurs dossiers du vault).
Les variantes *_by_path resolvent par CHEMIN EXACT via _normalize_path -> jamais de travers.

Ce que ces tests verrouillent :
  1. DESAMBIGUISATION : deux notes meme stem, by-path ecrit dans la BONNE, jamais l'autre.
     (C'est la raison d'etre du chantier — le coeur du contournement Edit-direct dissous.)
  2. EOL byte-exact herite du fix 6-A : le coeur _*_core est partage file=/by-path, donc
     un content LF reste LF et un CRLF reste CRLF (tests LIVE write_bytes/read_bytes).
  3. ERREURS : fichier introuvable, chemin absolu hors-vault refuse (securite _normalize_path).
  4. WARNING prefixe : un chemin avec prefixe vault/claude-forge/ accidentel est strip + warn.

Convention de test alignee sur test_eol_byte_exact.py (helpers _live_tools/_index/_assert_*).
"""

import pytest

from src.config import FTSWeights
from src.database import BrainDB
from src.indexer import parse_note
from src.tools.brain import BrainTools


def _live_tools(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    db = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    return BrainTools(db, vault, git_sync=None), vault


def _index(tools, note, rel):
    """Indexe une note depuis le disque (read_text aplatit l'EOL pour le parsing, OK)."""
    tools._db.index_note(
        parse_note(note.stem, rel, note.read_text(encoding="utf-8")),
        note.stat().st_mtime,
    )


def _assert_lf(after: bytes):
    assert b"\r\n" not in after, "Fichier LF converti en CRLF (diff full-file)"
    assert b"\r" not in after, "CR parasite introduit dans un fichier LF"


def _assert_crlf(after: bytes):
    assert b"\r\r\n" not in after, "Double conversion CRLF -> \\r\\r\\n"
    assert after.replace(b"\r\n", b"").count(b"\n") == 0, "LF orphelin introduit dans un fichier CRLF"


def _two_ambiguous_index(tmp_path):
    """Vault avec DEUX notes 'index.md' a des chemins differents (stem ambigu)."""
    tools, vault = _live_tools(tmp_path)
    racine = vault / "index.md"
    racine.write_bytes(b'---\ntitre: "Racine"\n---\n\nIndex racine.\n')
    _index(tools, racine, "index.md")
    sous = vault / "sub"
    sous.mkdir()
    sous_idx = sous / "index.md"
    sous_idx.write_bytes(b'---\ntitre: "Sous"\n---\n\nIndex sous-dossier.\n')
    _index(tools, sous_idx, "sub/index.md")
    return tools, vault, racine, sous_idx


# ====================== DESAMBIGUISATION (raison d'etre) ======================

def test_update_note_by_path_vise_la_bonne_note(tmp_path):
    tools, vault, racine, sous_idx = _two_ambiguous_index(tmp_path)
    # by-path cible explicitement la note du sous-dossier.
    res = tools.update_note_by_path("sub/index.md", '---\ntitre: "SousMAJ"\n---\n\nNouveau.\n')
    assert "mise a jour" in res
    # La bonne note est modifiee...
    assert b'titre: "SousMAJ"' in sous_idx.read_bytes()
    # ...et la note RACINE homonyme est intacte (pas de resolution de travers).
    assert b'titre: "Racine"' in racine.read_bytes()


def test_append_note_by_path_vise_la_bonne_note(tmp_path):
    tools, vault, racine, sous_idx = _two_ambiguous_index(tmp_path)
    tools.append_note_by_path("index.md", "\nLigne ajoutee racine.\n")
    assert b"Ligne ajoutee racine." in racine.read_bytes()
    assert b"Ligne ajoutee racine." not in sous_idx.read_bytes()


def test_update_property_by_path_vise_la_bonne_note(tmp_path):
    tools, vault, racine, sous_idx = _two_ambiguous_index(tmp_path)
    tools.update_property_by_path("sub/index.md", "statut", "actif")
    assert b"statut: actif" in sous_idx.read_bytes()
    assert b"statut: actif" not in racine.read_bytes()


def test_insert_section_by_path_vise_la_bonne_note(tmp_path):
    tools, vault = _live_tools(tmp_path)
    a = vault / "log.md"
    a.write_bytes(b'---\ntitre: "A"\n---\n\n## Entrees\n\nX.\n')
    _index(tools, a, "log.md")
    b_dir = vault / "casquette"
    b_dir.mkdir()
    b = b_dir / "log.md"
    b.write_bytes(b'---\ntitre: "B"\n---\n\n## Entrees\n\nY.\n')
    _index(tools, b, "casquette/log.md")
    tools.insert_section_by_path("casquette/log.md", "## Entrees", "INSERE B", position="after")
    assert b"INSERE B" in b.read_bytes()
    assert b"INSERE B" not in a.read_bytes()


# ====================== EOL byte-exact (herite du fix 6-A via coeur partage) ======================

def test_update_note_by_path_lf_reste_lf(tmp_path):
    tools, vault = _live_tools(tmp_path)
    note = vault / "u.md"
    note.write_bytes(b'---\ntitre: "T"\n---\n\nBody LF.\n')
    _index(tools, note, "u.md")
    tools.update_note_by_path("u.md", '---\ntitre: "T2"\n---\n\nNouveau LF.\n')
    _assert_lf(note.read_bytes())


def test_update_note_by_path_crlf_reste_crlf(tmp_path):
    tools, vault = _live_tools(tmp_path)
    note = vault / "uc.md"
    note.write_bytes(b'---\r\ntitre: "T"\r\n---\r\n\r\nBody CRLF.\r\n')
    _index(tools, note, "uc.md")
    tools.update_note_by_path("uc.md", '---\r\ntitre: "T2"\r\n---\r\n\r\nNouveau CRLF.\r\n')
    _assert_crlf(note.read_bytes())


def test_append_note_by_path_crlf_reste_crlf(tmp_path):
    tools, vault = _live_tools(tmp_path)
    note = vault / "ac.md"
    note.write_bytes(b'---\r\ntitre: "T"\r\n---\r\n\r\nBody.\r\n')
    _index(tools, note, "ac.md")
    tools.append_note_by_path("ac.md", "\r\n## Ajout\r\n\r\nLigne.\r\n")
    after = note.read_bytes()
    _assert_crlf(after)
    assert b"## Ajout\r\n" in after


def test_insert_section_by_path_crlf_aligne_eol(tmp_path):
    tools, vault = _live_tools(tmp_path)
    note = vault / "ic.md"
    note.write_bytes(b'---\r\ntitre: "T"\r\n---\r\n\r\n## Cible\r\n\r\nX.\r\n')
    _index(tools, note, "ic.md")
    tools.insert_section_by_path("ic.md", "## Cible", "Ligne", position="after")
    after = note.read_bytes()
    _assert_crlf(after)
    assert b"Ligne\r\n" in after, "content insere doit finir par CRLF (pas LF orphelin)"


def test_update_property_by_path_crlf_reste_crlf(tmp_path):
    tools, vault = _live_tools(tmp_path)
    note = vault / "pc.md"
    note.write_bytes(b'---\r\ntitre: "T"\r\nderniere-maj: 2026-01-01\r\n---\r\n\r\nBody.\r\n')
    _index(tools, note, "pc.md")
    tools.update_property_by_path("pc.md", "derniere-maj", "2026-06-07")
    after = note.read_bytes()
    _assert_crlf(after)
    assert b"derniere-maj: 2026-06-07" in after


# ====================== ERREURS ======================

def test_by_path_fichier_introuvable(tmp_path):
    tools, vault = _live_tools(tmp_path)
    res = tools.update_note_by_path("inexistant.md", "x")
    assert "introuvable" in res.lower()


def test_by_path_abs_hors_vault_refuse(tmp_path):
    tools, vault = _live_tools(tmp_path)
    res = tools.append_note_by_path(r"C:\Users\evil\note.md", "x")
    assert "REFUS" in res and "outside vault" in res


def test_by_path_index_inchange_si_introuvable(tmp_path):
    """Un by-path sur fichier absent ne doit RIEN ecrire ni reindexer."""
    tools, vault = _live_tools(tmp_path)
    before = tools._db._conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    tools.update_note_by_path("nope.md", "x")
    after = tools._db._conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    assert before == after


# ====================== WARNING prefixe accidentel ======================

def test_by_path_prefixe_vault_strip_avec_warn(tmp_path):
    """Un chemin avec prefixe vault/claude-forge/ accidentel est strip + signale [WARN]."""
    tools, vault = _live_tools(tmp_path)
    note = vault / "w.md"
    note.write_bytes(b'---\ntitre: "T"\n---\n\nBody.\n')
    _index(tools, note, "w.md")
    # Le vault de test s'appelle "vault" (tmp/vault), parent "tmp..." -> on passe le
    # prefixe "vault/" qui doit etre strip ; resolution sur w.md OK.
    res = tools.append_note_by_path("vault/w.md", "\najout.\n")
    assert "[WARN]" in res
    assert b"ajout." in note.read_bytes()


# ====================== INDEX synchronise (le but du chantier) ======================

def test_by_path_reindexe_le_contenu(tmp_path):
    """Apres un by-path, l'index reflete le nouveau contenu (pas de desync : tout passe MCP)."""
    tools, vault = _live_tools(tmp_path)
    note = vault / "r.md"
    note.write_bytes(b'---\ntitre: "T"\naliases:\n  - "ancien-alias"\n---\n\nBody.\n')
    _index(tools, note, "r.md")
    tools.update_note_by_path(
        "r.md", '---\ntitre: "T"\naliases:\n  - "nouvel-alias"\n---\n\nBody MAJ.\n'
    )
    # L'index doit resoudre le nouvel alias (preuve que index_note a tourne).
    assert tools._db.resolve_note("nouvel-alias") == "r.md"
    assert tools._db.resolve_note("ancien-alias") is None
