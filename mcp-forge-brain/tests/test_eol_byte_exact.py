"""Tests regression EOL byte-exact — update_note, insert_section, append_note, move_note.

Chantier 6 Trou A : le fix #2 (newline="") n'avait ete pose que sur update_property/bulk.
Ces 4 outils ecrivaient encore via la couche texte Windows, qui traduit \\n -> \\r\\n :
un fichier LF etait integralement reecrit en CRLF (diff full-file, 166 notes LF du vault
exposees). Ces tests VERROUILLENT : une note LF reste LF apres l'operation, une note CRLF
reste CRLF, sans \\r\\r\\n parasite ni LF orphelin. Tests LIVE (write_bytes/read_bytes) :
ils passent par read_text/write_text reels et attrapent la traduction d'EOL que les tests
sur string pure ne voient pas. Cf erreur-mcp-yaml-dump-corruption + feedback
gate-zero-diff-test-live-byte-exact.
"""

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
    # Zero LF orphelin : tout \n doit etre precede d'un \r.
    assert after.replace(b"\r\n", b"").count(b"\n") == 0, "LF orphelin introduit dans un fichier CRLF"


# ====================== update_note ======================

def test_update_note_lf_reste_lf(tmp_path):
    tools, vault = _live_tools(tmp_path)
    note = vault / "u-lf.md"
    note.write_bytes(b'---\ntitre: "T"\n---\n\nBody initial LF.\n')
    _index(tools, note, "u-lf.md")
    # content fourni en LF -> doit rester LF byte-exact.
    tools.update_note("u-lf", '---\ntitre: "T2"\n---\n\nNouveau body LF.\n')
    after = note.read_bytes()
    _assert_lf(after)
    assert b'titre: "T2"' in after


def test_update_note_crlf_reste_crlf(tmp_path):
    tools, vault = _live_tools(tmp_path)
    note = vault / "u-crlf.md"
    note.write_bytes(b'---\r\ntitre: "T"\r\n---\r\n\r\nBody CRLF.\r\n')
    _index(tools, note, "u-crlf.md")
    # content fourni en CRLF -> doit rester CRLF byte-exact.
    tools.update_note("u-crlf", '---\r\ntitre: "T2"\r\n---\r\n\r\nNouveau CRLF.\r\n')
    after = note.read_bytes()
    _assert_crlf(after)
    assert b'titre: "T2"' in after


# ====================== insert_section ======================

def test_insert_section_lf_reste_lf(tmp_path):
    tools, vault = _live_tools(tmp_path)
    note = vault / "i-lf.md"
    note.write_bytes(b'---\ntitre: "T"\n---\n\n## Section A\n\nContenu A.\n')
    _index(tools, note, "i-lf.md")
    tools.insert_section("i-lf", "## Section A", "Ligne inseree.", position="after")
    after = note.read_bytes()
    _assert_lf(after)
    assert b"Ligne inseree." in after
    assert b"## Section A\n" in after  # marker matche malgre l'absence de \r


def test_insert_section_crlf_reste_crlf(tmp_path):
    tools, vault = _live_tools(tmp_path)
    note = vault / "i-crlf.md"
    note.write_bytes(b'---\r\ntitre: "T"\r\n---\r\n\r\n## Section A\r\n\r\nContenu A.\r\n')
    _index(tools, note, "i-crlf.md")
    # content insere SANS EOL final -> le code doit l'aligner sur le CRLF du fichier.
    tools.insert_section("i-crlf", "## Section A", "Ligne inseree.", position="after")
    after = note.read_bytes()
    _assert_crlf(after)
    assert b"Ligne inseree.\r\n" in after, "content insere doit finir par CRLF (pas LF orphelin)"
    assert b"## Section A\r\n" in after  # marker matche malgre le \r


def test_insert_section_marker_matche_sur_crlf(tmp_path):
    """Le marker doit matcher meme quand la ligne porte un \\r\\n (rstrip \\r\\n)."""
    tools, vault = _live_tools(tmp_path)
    note = vault / "i-m.md"
    note.write_bytes(b'---\r\ntitre: "T"\r\n---\r\n\r\n## Cible\r\n\r\nX.\r\n')
    _index(tools, note, "i-m.md")
    res = tools.insert_section("i-m", "## Cible", "INSERE", position="before")
    assert "introuvable" not in res and "non aligne" not in res, f"marker non matche: {res}"
    after = note.read_bytes()
    _assert_crlf(after)
    assert b"INSERE\r\n## Cible\r\n" in after


# ====================== append_note ======================

def test_append_note_lf_reste_lf(tmp_path):
    tools, vault = _live_tools(tmp_path)
    note = vault / "a-lf.md"
    note.write_bytes(b'---\ntitre: "T"\n---\n\nBody.\n')
    _index(tools, note, "a-lf.md")
    # content ajoute en LF -> aucune traduction CRLF.
    tools.append_note("a-lf", "\n## Ajout\n\nLigne LF.\n")
    after = note.read_bytes()
    _assert_lf(after)
    assert b"## Ajout\n" in after


def test_append_note_crlf_reste_crlf(tmp_path):
    tools, vault = _live_tools(tmp_path)
    note = vault / "a-crlf.md"
    note.write_bytes(b'---\r\ntitre: "T"\r\n---\r\n\r\nBody.\r\n')
    _index(tools, note, "a-crlf.md")
    # content ajoute en CRLF -> reste CRLF byte-exact (appelant = autorite EOL).
    tools.append_note("a-crlf", "\r\n## Ajout\r\n\r\nLigne CRLF.\r\n")
    after = note.read_bytes()
    _assert_crlf(after)
    assert b"## Ajout\r\n" in after


# ====================== move_note (self-link + backlink rewrite) ======================

def test_move_note_self_link_lf_reste_lf(tmp_path):
    """Note LF avec self-link reecrit lors d'un rename de stem -> reste LF."""
    tools, vault = _live_tools(tmp_path)
    note = vault / "old-stem.md"
    # self-link [[old-stem]] dans le corps -> sera reecrit en [[new-stem]].
    note.write_bytes(b'---\ntitre: "T"\n---\n\nVoir [[old-stem]] ici.\n')
    _index(tools, note, "old-stem.md")
    tools.move_note("old-stem", "new-stem.md", update_wikilinks=True)
    moved = vault / "new-stem.md"
    after = moved.read_bytes()
    _assert_lf(after)
    assert b"[[new-stem]]" in after  # self-link reecrit
    assert b"[[old-stem]]" not in after


def test_move_note_self_link_crlf_reste_crlf(tmp_path):
    tools, vault = _live_tools(tmp_path)
    note = vault / "old-c.md"
    note.write_bytes(b'---\r\ntitre: "T"\r\n---\r\n\r\nVoir [[old-c]] ici.\r\n')
    _index(tools, note, "old-c.md")
    tools.move_note("old-c", "new-c.md", update_wikilinks=True)
    moved = vault / "new-c.md"
    after = moved.read_bytes()
    _assert_crlf(after)
    assert b"[[new-c]]" in after
    assert b"[[old-c]]" not in after


def test_move_note_backlink_lf_reste_lf(tmp_path):
    """Un backlink LF pointant vers la note deplacee -> reecrit sans conversion CRLF."""
    tools, vault = _live_tools(tmp_path)
    target = vault / "cible-old.md"
    target.write_bytes(b'---\ntitre: "Cible"\n---\n\nContenu cible.\n')
    _index(tools, target, "cible-old.md")
    backlink = vault / "source.md"
    backlink.write_bytes(b'---\ntitre: "Src"\n---\n\nJe pointe vers [[cible-old]].\n')
    _index(tools, backlink, "source.md")
    tools.move_note("cible-old", "cible-new.md", update_wikilinks=True)
    after_bl = backlink.read_bytes()
    _assert_lf(after_bl)
    assert b"[[cible-new]]" in after_bl  # backlink mis a jour
    assert b"[[cible-old]]" not in after_bl


def test_move_note_backlink_crlf_reste_crlf(tmp_path):
    tools, vault = _live_tools(tmp_path)
    target = vault / "cible-co.md"
    target.write_bytes(b'---\r\ntitre: "Cible"\r\n---\r\n\r\nContenu.\r\n')
    _index(tools, target, "cible-co.md")
    backlink = vault / "src-c.md"
    backlink.write_bytes(b'---\r\ntitre: "Src"\r\n---\r\n\r\nPointe vers [[cible-co]].\r\n')
    _index(tools, backlink, "src-c.md")
    tools.move_note("cible-co", "cible-cn.md", update_wikilinks=True)
    after_bl = backlink.read_bytes()
    _assert_crlf(after_bl)
    assert b"[[cible-cn]]" in after_bl
    assert b"[[cible-co]]" not in after_bl
