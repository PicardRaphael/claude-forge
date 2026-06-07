"""MCP tools for forge-brain vault — backed by SQLite FTS5."""

import logging
import re
from pathlib import Path
from src.database import BrainDB
from src.indexer import parse_note, _WIKILINK_RE
from src.usage_log import log_call, stats as _compute_usage_stats

import yaml

log = logging.getLogger(__name__)


_WINDOWS_ABS_RE = re.compile(r"^[A-Za-z]:[/\\]")

# Folders excluded from lint_vault (Karpathy immutable + system folders + templates)
_LINT_EXCLUDE_PREFIXES = ("raw/", "Templates/", ".obsidian/", ".claude/", "Archive/")

# Wikilink targets ignored as broken (structural false-positives)
_LINT_EXCLUDE_WIKILINK_PREFIXES = (
    "feedback_",      # memory/feedback_* live outside vault (perso memory)
    "reference_",     # same
    "user_",          # same
    "project_",       # same
)
_LINT_EXCLUDE_WIKILINK_EXACT = {
    # Example wikilinks cited in methodo notes as syntax demo
    "note", "note a", "note b", "note c", "note 1", "note 2", "note 3", "note 4",
    "erreur-foo", "raisonnement-<date>-<sujet>", "wikilink", "nom de note",
    "claude.md", "memory",
    # Self-references in _index (relative paths Obsidian doesn't resolve)
    # filtered via path-strip in caller
    # Agents living in .claude/agents/ (outside vault)
    "agent-creator", "skill-creator", "hook-creator", "claudemd-optimizer",
    "project-auditor", "project-analyzer", "self-updater", "vault-maintainer",
    "devils-advocate", "devils-advocate-pipeline", "outcomes-grader", "python-dev",
    "expand", "forge-review", "changelog-vault", "obsidian-markdown",
    "forge-brain-proactive",
}


def _is_lint_excluded_wikilink(stem_lower: str) -> bool:
    """Check if a wikilink target is a structural false-positive."""
    if stem_lower in _LINT_EXCLUDE_WIKILINK_EXACT:
        return True
    for prefix in _LINT_EXCLUDE_WIKILINK_PREFIXES:
        if stem_lower.startswith(prefix):
            return True
    return False

# Markdown code block / inline code masking: protect [[...]] inside code from rewrite
_CODE_FENCE_RE = re.compile(r"^```[^\n]*\n.*?^```", re.MULTILINE | re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")


def _rewrite_wikilinks(content: str, old_stem: str, new_stem: str) -> tuple[str, int]:
    """Rewrite [[old_stem]] -> [[new_stem]] preserving variants:
    - [[stem]], [[stem|alias]], [[stem#section]], [[stem|alias#section]]
    - ![[stem]] (embeds, leading ! preserved)
    - [[Stem]] (case-insensitive match — Obsidian resolves case-insensitive)

    SKIPS wikilinks inside code blocks (``` fences) and inline code (`...`).
    Returns (new_content, count_rewritten).
    """
    if old_stem == new_stem:
        return content, 0

    # Mask code blocks and inline code with placeholders so the rewrite skips them
    masked_segments: list[str] = []

    def mask(match):
        masked_segments.append(match.group(0))
        return f"\x00CODE{len(masked_segments) - 1}\x00"

    masked = _CODE_FENCE_RE.sub(mask, content)
    masked = _INLINE_CODE_RE.sub(mask, masked)

    # Case-insensitive match on the stem only (preserves the rest of the wikilink)
    pattern = re.compile(
        r"(?P<bang>!?)\[\[(?P<stem>" + re.escape(old_stem) + r")(?P<rest>[\]|#])",
        re.IGNORECASE,
    )

    count = 0

    def replace(m):
        nonlocal count
        count += 1
        return f"{m.group('bang')}[[{new_stem}{m.group('rest')}"

    rewritten = pattern.sub(replace, masked)

    # Unmask
    for i, segment in enumerate(masked_segments):
        rewritten = rewritten.replace(f"\x00CODE{i}\x00", segment)

    return rewritten, count



def _normalize_path(vault: Path, path: str) -> tuple[str, str | None]:
    """Strip vault prefix if user passed it accidentally. Reject absolute paths.

    Returns (normalized_relative_path, warning_or_None).
    Raises ValueError on absolute paths not matching the vault root (security: prevents
    writing outside the vault if a caller passes `C:\\foo\\bar.md`).
    """
    p = path.replace("\\", "/")

    # Reject Windows absolute path unless it points inside the vault
    if _WINDOWS_ABS_RE.match(p):
        try:
            vault_abs = vault.resolve()
            abs_p = Path(p).resolve()
            rel = abs_p.relative_to(vault_abs)
            return str(rel).replace("\\", "/"), f"Absolute path resolved to vault-relative '{rel}'"
        except (ValueError, OSError):
            raise ValueError(f"Absolute path outside vault refused: {path}")

    # Reject Unix absolute path that's not stripping to a known vault prefix
    if p.startswith("/"):
        # Try to strip to find vault path inside it
        vault_abs_str = str(vault.resolve()).replace("\\", "/")
        if p.startswith(vault_abs_str + "/"):
            return p[len(vault_abs_str) + 1:], f"Absolute path stripped to vault-relative"
        # Otherwise just strip leading slashes (legacy permissive behavior)
        p = p.lstrip("/")

    vault_name = vault.name
    vault_parent = vault.parent.name
    prefixes = [
        f"{vault_parent}/{vault_name}/",
        f"{vault_name}/",
        f"./{vault_parent}/{vault_name}/",
        f"./{vault_name}/",
    ]
    for prefix in prefixes:
        if p.startswith(prefix):
            normalized = p[len(prefix):]
            return normalized, f"Path prefix '{prefix}' stripped (passed absolute, expected vault-relative)"
    return p, None


_FM_BLOCK_RE = re.compile(r"^(---\s*\n)(.*?)(\n---\s*\n)", re.DOTALL)
_TOP_KEY_RE = re.compile(r"^[^\s#][^:]*:")


def _render_yaml_value(name: str, value: str | list) -> str:
    """Rend UNE propriete frontmatter dans le style maison du vault forge-brain.

    Calibre sur le frontmatter reel (lu via MCP) :
    - liste  -> bloc multi-ligne, items indentes 2 espaces, valeurs entre guillemets doubles
    - scalaire -> `name: value` sur une ligne, non quote (sauf si caracteres ambigus YAML)

    JAMAIS yaml.safe_dump : il indente les items en colonne 0, change le quoting et
    echappe l'unicode (\\xE9), ce qui casse l'exigence zero-diff sur un bulk.
    """
    if isinstance(value, list):
        if not value:
            return f"{name}: []"
        lines = [f"{name}:"]
        for item in value:
            s = str(item).replace('"', '\\"')
            lines.append(f'  - "{s}"')
        return "\n".join(lines)
    # Scalaire : non quote par defaut (style vault : dates, type, auteur nus).
    s = str(value)
    # Quote uniquement si la valeur contient un caractere qui casserait le parsing
    # YAML scalaire nu (ex: ': ', '#', commence par un indicateur, multi-ligne).
    needs_quote = (
        s != s.strip()
        or ": " in s
        or s.startswith(("- ", "? ", "#", "&", "*", "!", "|", ">", "@", "`", '"', "'", "[", "{"))
        or "\n" in s
        or s == ""
    )
    if needs_quote:
        return f'{name}: "{s.replace(chr(92), chr(92) * 2).replace(chr(34), chr(92) + chr(34))}"'
    return f"{name}: {s}"


def _set_property_in_frontmatter(content: str, name: str, value: str | list) -> str:
    """Insere/remplace UNE propriete dans le frontmatter, par splice chirurgical.

    Pur : pas d'IO, pas de DB, pas de git. Tout le contenu HORS du span de la
    propriete ciblee reste byte-for-byte identique (exigence zero-diff collatéral).

    - Remplace le span complet de la propriete : ligne-clé + toutes ses continuations
      (lignes indentees, items `- ...`, lignes vides) jusqu'a la prochaine clé top-level.
      C'est le fix : ne remplacer que la ligne-clé laissait les items orphelins.
    - Clé absente -> ajout en fin de frontmatter.
    - Frontmatter absent -> creation d'un frontmatter minimal.

    Leve ValueError si le frontmatter resultant ne reparse pas ou si la propriete
    ne porte pas la valeur voulue (refus d'ecrire un YAML casse).

    Preserve byte-for-byte le BOM UTF-8 eventuel et le style de fin de ligne
    (CRLF vs LF) du fichier d'origine.
    """
    rendered = _render_yaml_value(name, value)

    # Detacher un BOM UTF-8 eventuel (le vault en contient — PowerShell Out-File) :
    # le `---` du frontmatter doit etre matche en tete, et le BOM sera reattache.
    bom = ""
    if content.startswith("﻿"):
        bom = "﻿"
        content = content[1:]

    # Detecter le style de fin de ligne pour le restituer a l'identique.
    # On normalise en \n pour le traitement interne, on re-emet avec l'EOL d'origine.
    crlf = "\r\n" in content
    work = content.replace("\r\n", "\n") if crlf else content

    def _restore(text: str) -> str:
        return bom + (text.replace("\n", "\r\n") if crlf else text)

    m = _FM_BLOCK_RE.match(work)
    if not m:
        # Pas de frontmatter : en creer un minimal en tete.
        return _restore(f"---\n{rendered}\n---\n\n{work}")

    open_fence, fm_body, close_fence = m.group(1), m.group(2), m.group(3)
    rest = work[m.end():]

    lines = fm_body.split("\n")
    key_re = re.compile(rf"^{re.escape(name)}:")

    start = None
    for i, line in enumerate(lines):
        if key_re.match(line):
            start = i
            break

    if start is None:
        # Clé absente : ajout en fin de frontmatter (apres la derniere ligne non vide).
        end_idx = len(lines)
        while end_idx > 0 and lines[end_idx - 1].strip() == "":
            end_idx -= 1
        new_lines = lines[:end_idx] + rendered.split("\n") + lines[end_idx:]
    else:
        # Etendre le span aux continuations jusqu'a la prochaine clé top-level.
        end = start + 1
        while end < len(lines):
            ln = lines[end]
            if ln.strip() == "":
                end += 1
                continue
            if _TOP_KEY_RE.match(ln):
                break
            end += 1
        # Ne pas absorber les lignes vides finales qui precedent une autre clé / la fin.
        while end > start + 1 and lines[end - 1].strip() == "":
            end -= 1
        new_lines = lines[:start] + rendered.split("\n") + lines[end:]

    new_fm_body = "\n".join(new_lines)

    # Garde : refuser d'ecrire un YAML casse (ceinture + bretelles).
    try:
        parsed = yaml.safe_load(new_fm_body)
    except yaml.YAMLError as e:
        raise ValueError(f"Refus : le frontmatter resultant ne parse pas ({e}).")
    if not isinstance(parsed, dict) or name not in parsed:
        raise ValueError(f"Refus : propriete '{name}' absente du frontmatter resultant.")
    expected = list(value) if isinstance(value, list) else str(value)
    got = parsed[name]
    got_norm = [str(x) for x in got] if isinstance(got, list) else (str(got) if got is not None else "")
    exp_norm = [str(x) for x in expected] if isinstance(expected, list) else expected
    if got_norm != exp_norm:
        raise ValueError(
            f"Refus : '{name}' = {got_norm!r} apres splice, attendu {exp_norm!r}."
        )

    return _restore(f"{open_fence}{new_fm_body}{close_fence}{rest}")


class BrainTools:
    def __init__(self, db: BrainDB, vault_path: Path, git_sync=None, sessions_db=None):
        self._db = db
        self._vault = vault_path
        self._git = git_sync
        self._sessions = sessions_db

    def search_sessions(
        self,
        query: str,
        limit: int = 20,
        project: str = "",
        role: str = "",
        since: str = "",
    ) -> str:
        if self._sessions is None:
            return "Recherche transcripts desactivee (sessions.enabled=false dans config.yaml)."
        results = self._sessions.search(query, limit=limit, project=project, role=role, since=since)
        if not results:
            return f"Aucun message de session trouve pour '{query}'."
        lines = []
        for r in results:
            ts = (r.get("timestamp") or "")[:19]
            lines.append(
                f"### [{r['role']}] {ts} — {r['project']}\n"
                f"{r['snippet']}\n"
                f"_session {r['session_id'][:8]} · {r['path']}_\n"
            )
        return "\n".join(lines)

    def search_brain(self, query: str, limit: int = 5, context: bool = True) -> str:
        results = self._db.search(query, limit=limit, context=context)
        if not results:
            return f"Aucun resultat pour '{query}'."
        lines = []
        for r in results:
            if context and r.get("context"):
                lines.append(f"### {r['file_stem']} ({r['path']})\n{r['context']}\n")
            else:
                lines.append(f"- {r['file_stem']} ({r['path']})")
        return "\n".join(lines)

    def read_note(self, file: str, max_lines: int = 0, offset: int = 0, limit_chars: int = 0) -> str:
        """Lit une note. Pagination optionnelle pour grosses notes (CHANGELOG, log).

        Args:
            file: nom de la note ou alias
            max_lines: tronquer apres N lignes (legacy)
            offset: nombre de caracteres a sauter au debut (pagination)
            limit_chars: nombre max de caracteres a retourner (pagination)
        """
        path = self._db.resolve_note(file)
        if not path:
            suggestions = self._db.suggest_notes(file, limit=5)
            if suggestions:
                suggest_list = ", ".join(suggestions)
                return f"Note '{file}' introuvable. Notes similaires : {suggest_list}"
            return f"Note '{file}' introuvable (ni par nom, ni par alias, ni par recherche)."
        full_path = self._vault / path
        if not full_path.exists():
            return f"Note '{file}' indexee mais fichier manquant: {path}"
        content = full_path.read_text(encoding="utf-8", errors="replace")
        total_chars = len(content)

        # Char-based pagination (priority over max_lines if both set)
        if offset > 0 or limit_chars > 0:
            if offset >= total_chars:
                return f"offset={offset} depasse la taille de la note ({total_chars} chars)."
            end = offset + limit_chars if limit_chars > 0 else total_chars
            chunk = content[offset:end]
            header = f"[chars {offset}-{min(end, total_chars)}/{total_chars}]\n"
            if end < total_chars:
                header += f"[suite : appeler avec offset={end}, limit_chars={limit_chars}]\n"
            return header + "\n" + chunk

        if max_lines > 0:
            lines = content.split("\n")
            if len(lines) > max_lines:
                return "\n".join(lines[:max_lines]) + f"\n\n... ({len(lines) - max_lines} lignes tronquees)"
        return content

    def read_note_by_path(self, path: str) -> str:
        normalized, warning = _normalize_path(self._vault, path)
        full_path = self._vault / normalized
        if not full_path.exists():
            return f"Fichier introuvable: {normalized}"
        content = full_path.read_text(encoding="utf-8", errors="replace")
        if warning:
            return f"[WARN] {warning}\n\n{content}"
        return content

    def get_backlinks(self, file: str) -> str:
        backlinks = self._db.get_backlinks(file)
        if not backlinks:
            return f"Aucun backlink vers '{file}'."
        lines = [f"- {bl['file_stem']} ({bl['count']} liens)" for bl in backlinks]
        return "\n".join(lines)

    def get_tags(self) -> str:
        tags = self._db.get_tags()
        if not tags:
            return "Aucun tag dans le vault."
        lines = [f"- {t['tag']} ({t['count']})" for t in tags]
        return "\n".join(lines)

    def get_property(self, file: str, name: str) -> str:
        value = self._db.get_property(file, name)
        if value is None:
            return f"Propriete '{name}' introuvable pour '{file}'."
        return value

    def create_note(self, path: str, content: str, username: str = "anonymous") -> str:
        normalized, prefix_warning = _normalize_path(self._vault, path)
        full_path = self._vault / normalized
        if full_path.exists():
            return f"Note existe deja: {normalized}"
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        parsed = parse_note(full_path.stem, normalized, content)
        warnings = []
        if prefix_warning:
            warnings.append(prefix_warning)
        if len(parsed.aliases) < 4:
            warnings.append(f"seulement {len(parsed.aliases)} aliases (minimum recommande: 4)")
        warnings.extend(parsed.lint_warnings)
        self._db.index_note(parsed, full_path.stat().st_mtime)
        if self._git and self._git._cfg.auto_commit:
            self._git.commit_file(normalized, username, "create", full_path.stem)
        if warnings:
            return f"Note creee: {normalized}\nWARN: " + " | ".join(warnings)
        return f"Note creee: {normalized}"

    def append_note(self, file: str, content: str, username: str = "anonymous") -> str:
        path = self._db.resolve_note(file)
        if not path:
            return f"Note '{file}' introuvable."
        full_path = self._vault / path
        with open(full_path, "a", encoding="utf-8") as f:
            f.write(content)
        new_content = full_path.read_text(encoding="utf-8", errors="replace")
        parsed = parse_note(full_path.stem, path, new_content)
        self._db.index_note(parsed, full_path.stat().st_mtime)
        if self._git and self._git._cfg.auto_commit:
            self._git.commit_file(path, username, "append", full_path.stem)
        return f"Contenu ajoute a: {path}"

    def update_note(self, file: str, content: str, username: str = "anonymous") -> str:
        """Remplace EN ENTIER le contenu d'une note existante (frontmatter + body).
        Pour ajouter en fin, utiliser append_note. Pour modifier 1 propriete frontmatter,
        utiliser update_property. Pour inserer a un endroit precis, utiliser insert_section.
        """
        path = self._db.resolve_note(file)
        if not path:
            return f"Note '{file}' introuvable."
        full_path = self._vault / path
        full_path.write_text(content, encoding="utf-8")
        parsed = parse_note(full_path.stem, path, content)
        self._db.index_note(parsed, full_path.stat().st_mtime)
        if self._git and self._git._cfg.auto_commit:
            self._git.commit_file(path, username, "update", full_path.stem)
        return f"Note mise a jour: {path}"

    def insert_section(
        self,
        file: str,
        marker: str,
        content: str,
        position: str = "after",
        username: str = "anonymous",
    ) -> str:
        """Insere du contenu avant/apres une section markdown reperee par son header exact.

        Args:
            file: nom de la note ou alias
            marker: ligne header complete (ex: "## COMMENT — Grille 6 etapes")
            content: contenu markdown a inserer
            position: "before" ou "after" le marker (default "after")
        """
        if position not in ("before", "after"):
            return f"Position invalide: '{position}'. Utiliser 'before' ou 'after'."
        path = self._db.resolve_note(file)
        if not path:
            return f"Note '{file}' introuvable."
        full_path = self._vault / path
        original = full_path.read_text(encoding="utf-8", errors="replace")
        if marker not in original:
            return f"Marker '{marker}' introuvable dans: {path}"
        lines = original.splitlines(keepends=True)
        out: list[str] = []
        inserted = False
        for line in lines:
            if not inserted and line.rstrip("\n") == marker.rstrip("\n"):
                if position == "before":
                    out.append(content if content.endswith("\n") else content + "\n")
                    out.append(line)
                else:
                    out.append(line)
                    out.append(content if content.endswith("\n") else content + "\n")
                inserted = True
            else:
                out.append(line)
        if not inserted:
            return f"Marker '{marker}' present mais non aligne (ligne entiere)."
        new_content = "".join(out)
        full_path.write_text(new_content, encoding="utf-8")
        parsed = parse_note(full_path.stem, path, new_content)
        self._db.index_note(parsed, full_path.stat().st_mtime)
        if self._git and self._git._cfg.auto_commit:
            self._git.commit_file(path, username, f"insert_{position}", full_path.stem)
        return f"Contenu insere {position} '{marker}' dans: {path}"

    def list_notes(self, folder: str = "", limit: int = 50) -> str:
        rows = self._db._conn.execute(
            "SELECT file_stem, path FROM notes WHERE path LIKE ? ORDER BY file_stem LIMIT ?",
            (f"{folder}%" if folder else "%", limit),
        ).fetchall()
        if not rows:
            return f"Aucune note dans '{folder or 'vault'}'."
        lines = [f"- {r['file_stem']} ({r['path']})" for r in rows]
        return f"{len(lines)} notes:\n" + "\n".join(lines)

    def vault_stats(self) -> str:
        total = self._db._conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        tags_count = self._db._conn.execute("SELECT COUNT(DISTINCT tag) FROM tags").fetchone()[0]
        links_count = self._db._conn.execute("SELECT COUNT(*) FROM links").fetchone()[0]
        aliases_count = self._db._conn.execute("SELECT COUNT(*) FROM aliases").fetchone()[0]
        folders = self._db._conn.execute(
            "SELECT SUBSTR(path, 1, INSTR(path, '/') - 1) as folder, COUNT(*) as cnt "
            "FROM notes WHERE INSTR(path, '/') > 0 GROUP BY folder ORDER BY cnt DESC"
        ).fetchall()
        lines = [f"**Vault forge-brain** : {total} notes, {tags_count} tags, {links_count} wikilinks, {aliases_count} aliases\n"]
        lines.append("| Dossier | Notes |")
        lines.append("|---------|-------|")
        for f in folders:
            lines.append(f"| {f['folder']} | {f['cnt']} |")
        return "\n".join(lines)

    def delete_note(self, file: str, force: bool = False, username: str = "anonymous") -> str:
        """Supprime une note du vault et de l'index. Refuse si backlinks > 0 sauf force=True.

        Args:
            file: nom de la note ou alias
            force: si True, supprime meme si des notes pointent vers elle (wikilinks brises)
        """
        path = self._db.resolve_note(file)
        if not path:
            return f"Note '{file}' introuvable."
        backlinks = self._db.get_backlinks(file)
        if backlinks and not force:
            sources = ", ".join(bl["file_stem"] for bl in backlinks[:5])
            return (
                f"REFUS: {len(backlinks)} backlinks vers '{file}' "
                f"(ex: {sources}). Utiliser force=True pour supprimer quand meme "
                f"(wikilinks deviendront brises)."
            )
        full_path = self._vault / path
        file_existed = full_path.exists()
        if file_existed:
            full_path.unlink()
        self._db.delete_note(path)
        if self._git and self._git._cfg.auto_commit and file_existed:
            self._git.commit_file(path, username, "delete", full_path.stem)
        msg = f"Note supprimee: {path}"
        if not file_existed:
            msg += " (WARN: entree DB nettoyee, fichier physique absent)"
        if force and backlinks:
            sources_full = ", ".join(bl["file_stem"] for bl in backlinks[:10])
            extra = f" (+ {len(backlinks) - 10})" if len(backlinks) > 10 else ""
            msg += (
                f"\nWARN: {len(backlinks)} wikilinks maintenant BRISES dans : {sources_full}{extra}. "
                f"Lancer lint_vault() pour cartographier."
            )
        return msg

    def move_note(self, file: str, new_path: str, update_wikilinks: bool = True, username: str = "anonymous") -> str:
        """Deplace une note vers un nouveau chemin et met a jour wikilinks dans les backlinks.

        Args:
            file: nom de la note ou alias
            new_path: chemin de destination (relatif au vault, ex: "Archive/old-note.md")
            update_wikilinks: si True, parcourt les backlinks et met a jour les wikilinks pointant
                              vers l'ancien stem si le nouveau stem differe. Default True.

        Wikilinks geres: [[stem]], [[stem|alias]], [[stem#section]], [[stem|alias#section]],
        ![[stem]] (embeds), [[Stem]] (case-insensitive), self-links dans la note deplacee.
        NOT geres: wikilinks dans blocs code (preserves volontairement, content litteral).
        Les wikilinks utilisant un ALIAS de la note (et non son stem) ne sont PAS modifies
        car ils restent valides via la resolution alias->note du MCP.
        """
        path = self._db.resolve_note(file)
        if not path:
            return f"Note '{file}' introuvable."
        normalized_new, prefix_warning = _normalize_path(self._vault, new_path)
        if not normalized_new.endswith(".md"):
            return f"REFUS: new_path doit terminer par .md (recu: {normalized_new})"
        old_full = self._vault / path
        new_full = self._vault / normalized_new
        if new_full.exists():
            return f"REFUS: la destination existe deja: {normalized_new}"
        if not old_full.exists():
            return f"Note '{file}' indexee mais fichier source manquant: {path}"

        old_stem = old_full.stem
        new_stem = new_full.stem

        # B4 fix: capture backlinks BEFORE any DB mutation (atomicity)
        backlinks_snapshot = self._db.get_backlinks(old_stem) if old_stem != new_stem else []

        # Move file on disk
        new_full.parent.mkdir(parents=True, exist_ok=True)
        old_full.rename(new_full)

        # Re-index moved note
        content = new_full.read_text(encoding="utf-8", errors="replace")

        # B1 self-link fix: rewrite wikilinks inside moved note BEFORE indexing
        self_link_count = 0
        if update_wikilinks and old_stem != new_stem:
            content_rewritten, self_link_count = _rewrite_wikilinks(content, old_stem, new_stem)
            if self_link_count > 0:
                new_full.write_text(content_rewritten, encoding="utf-8")
                content = content_rewritten

        parsed = parse_note(new_stem, normalized_new, content)
        # Old path needs to be removed from index first
        self._db.delete_note(path)
        self._db.index_note(parsed, new_full.stat().st_mtime)

        # Update wikilinks in backlink notes if stem changed
        updated_files = []
        skipped_codeblock = 0
        if update_wikilinks and old_stem != new_stem:
            for bl in backlinks_snapshot:
                bl_stem = bl["file_stem"]
                bl_path = self._db.resolve_note(bl_stem)
                if not bl_path or bl_path == normalized_new:
                    continue
                bl_full = self._vault / bl_path
                if not bl_full.exists():
                    continue
                bl_content = bl_full.read_text(encoding="utf-8", errors="replace")
                new_content, rewrite_count = _rewrite_wikilinks(bl_content, old_stem, new_stem)
                if rewrite_count > 0:
                    bl_full.write_text(new_content, encoding="utf-8")
                    bl_parsed = parse_note(bl_stem, bl_path, new_content)
                    self._db.index_note(bl_parsed, bl_full.stat().st_mtime)
                    updated_files.append(bl_stem)

        if self._git and self._git._cfg.auto_commit:
            self._git.commit_file(normalized_new, username, "move", new_stem)

        msg = f"Note deplacee: {path} -> {normalized_new}"
        if prefix_warning:
            msg += f"\n[WARN] {prefix_warning}"
        if self_link_count:
            msg += f"\nSelf-links reecrits: {self_link_count}"
        if updated_files:
            msg += f"\nWikilinks mis a jour dans {len(updated_files)} notes: {', '.join(updated_files[:10])}"
            if len(updated_files) > 10:
                msg += f" (+ {len(updated_files) - 10} autres)"
        # Warn if aliases of the moved note still contain the old stem
        if old_stem != new_stem and old_stem in parsed.aliases:
            msg += f"\nWARN: l'ancien stem '{old_stem}' est encore dans les aliases de la note deplacee. Considere update_property aliases."
        return msg

    def bulk_update_property(
        self,
        files: list[str],
        name: str,
        value: str | list,
        username: str = "anonymous",
    ) -> str:
        """Met a jour la meme propriete sur N notes en 1 appel (economie round-trips LLM).

        Args:
            files: liste de noms/aliases de notes
            name: nom propriete frontmatter
            value: nouvelle valeur

        Cas d'usage : update `derniere-maj` sur 16 leaders apres audit = 1 appel au lieu de 16.
        """
        if not isinstance(files, list):
            return "REFUS: files doit etre une liste de noms."
        if not files:
            return "REFUS: liste files vide."
        updated = []
        failed = []
        for file in files:
            try:
                result = self.update_property(file, name, value, username)
                if "introuvable" in result:
                    failed.append({"file": file, "reason": "introuvable"})
                else:
                    updated.append(file)
            except Exception as e:
                failed.append({"file": file, "reason": str(e)})
        msg = f"Bulk update: {len(updated)}/{len(files)} notes mises a jour ({name} = {value})"
        if updated:
            msg += f"\nOK: {', '.join(updated[:10])}"
            if len(updated) > 10:
                msg += f" (+ {len(updated) - 10})"
        if failed:
            msg += f"\nECHEC ({len(failed)}): " + ", ".join(f"{f['file']}({f['reason']})" for f in failed[:5])
        return msg

    def read_section(self, file: str, heading: str, include_subsections: bool = True) -> str:
        """Lit UNE section d'une note (header markdown jusqu'au prochain header de meme niveau).

        Args:
            file: nom de la note ou alias
            heading: header complet exact (ex: "## COMMENT", "### Workflow")
            include_subsections: si True, inclut sous-headers

        Cas d'usage : CHANGELOG 62k chars, section "2026-05-24" = ~2k chars.
        """
        path = self._db.resolve_note(file)
        if not path:
            return f"Note '{file}' introuvable."
        full_path = self._vault / path
        if not full_path.exists():
            return f"Note '{file}' indexee mais fichier manquant: {path}"
        content = full_path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines(keepends=True)

        heading_stripped = heading.strip()
        if not heading_stripped.startswith("#"):
            return f"REFUS: heading doit commencer par # (recu: {heading})"
        level = len(heading_stripped) - len(heading_stripped.lstrip("#"))

        out: list[str] = []
        in_section = False
        for line in lines:
            line_no_nl = line.rstrip("\n")
            if not in_section:
                if line_no_nl == heading_stripped:
                    in_section = True
                    out.append(line)
                    continue
            else:
                if line_no_nl.startswith("#"):
                    line_level = len(line_no_nl) - len(line_no_nl.lstrip("#"))
                    if line_level <= level:
                        break
                    if not include_subsections and line_level > level:
                        break
                out.append(line)

        if not out:
            return f"Heading '{heading}' introuvable dans: {path}"
        return "".join(out)

    def find_by_property(
        self,
        name: str,
        value: str = "",
        comparator: str = "eq",
        folder: str = "",
        limit: int = 50,
    ) -> str:
        """Cherche les notes dont une propriete frontmatter satisfait une condition.

        Args:
            name: nom de la propriete (ex: "derniere-maj", "type", "auteur")
            value: valeur de comparaison (ex: "2026-05-24", "knowledge", "claude")
            comparator: "eq" (egal), "ne" (different), "lt", "gt", "contains", "missing", "present"
            folder: prefixe path optionnel (ex: "Knowledge/erreurs")
            limit: nombre max de resultats

        Cas d'usage :
        - find_by_property("derniere-maj", "2026-04-24", "lt") -> notes stales
        - find_by_property("type", "deprecation") -> toutes les notes deprecations
        - find_by_property("statut", "doublon") -> tous les doublons marques
        - find_by_property("sources", comparator="missing") -> notes sans sources frontmatter
        """
        if comparator not in ("eq", "ne", "lt", "gt", "contains", "missing", "present"):
            return f"REFUS: comparator invalide '{comparator}'. Valides: eq, ne, lt, gt, contains, missing, present"

        rows = self._db._conn.execute(
            "SELECT file_stem, path, frontmatter FROM notes "
            "WHERE path LIKE ? ORDER BY file_stem",
            (f"{folder}%" if folder else "%",),
        ).fetchall()

        matches = []
        for r in rows:
            fm_raw = r["frontmatter"] or ""
            try:
                fm = yaml.safe_load(fm_raw) if fm_raw else {}
                if not isinstance(fm, dict):
                    fm = {}
            except yaml.YAMLError:
                fm = {}

            actual = fm.get(name)
            actual_str = "" if actual is None else (
                ", ".join(str(v) for v in actual) if isinstance(actual, list) else str(actual)
            )

            match = False
            if comparator == "missing":
                match = actual is None or actual_str == ""
            elif comparator == "present":
                match = actual is not None and actual_str != ""
            elif actual is None:
                continue
            elif comparator == "eq":
                match = actual_str == value
            elif comparator == "ne":
                match = actual_str != value
            elif comparator == "contains":
                match = value.lower() in actual_str.lower()
            elif comparator in ("lt", "gt"):
                match = (actual_str < value) if comparator == "lt" else (actual_str > value)

            if match:
                matches.append({"stem": r["file_stem"], "path": r["path"], "value": actual_str})
                if len(matches) >= limit:
                    break

        if not matches:
            scope = f" dans '{folder}'" if folder else ""
            return f"Aucune note avec {name} {comparator} '{value}'{scope}."
        lines = [f"# Notes avec {name} {comparator} '{value}' ({len(matches)} resultats)\n"]
        for m in matches:
            lines.append(f"- [[{m['stem']}]] ({m['path']}) — {name}: {m['value'][:80]}")
        return "\n".join(lines)

    def lint_vault(self, limit: int = 50) -> str:
        """Detecte les problemes de qualite dans le vault.

        Checks:
        - Notes avec aliases < 4 (standard forge)
        - Notes orphelines (0 backlink ET 0 wikilink sortant)
        - Notes sans tag
        - Notes avec frontmatter YAML casse (lint_warnings de parse_note)
        - Wikilinks brises (cibles inexistantes)

        Args:
            limit: nombre max de problemes par categorie (default 50)
        """
        rows = self._db._conn.execute(
            "SELECT n.id, n.file_stem, n.path, n.frontmatter FROM notes n"
        ).fetchall()

        low_aliases = []
        no_tags = []
        orphans = []
        broken_yaml = []
        broken_wikilinks = []

        # Build sets for fast lookup (case-insensitive — Obsidian resolves both ways)
        all_stems_lower = set()
        all_aliases_lower = set()
        for r in rows:
            all_stems_lower.add(r["file_stem"].lower())
        alias_rows = self._db._conn.execute("SELECT a.alias FROM aliases a").fetchall()
        for ar in alias_rows:
            all_aliases_lower.add(ar["alias"].lower())

        for r in rows:
            note_id = r["id"]
            stem = r["file_stem"]
            path = r["path"]

            # Karpathy layer 1 (immutable) + folders intentionally outside lint scope
            if any(path.startswith(p) for p in _LINT_EXCLUDE_PREFIXES):
                continue
            # log.md / CHANGELOG.md are append-only narrative traces — they cite dead
            # note names (between backticks) while documenting past repairs, which the
            # lint parses as broken wikilinks (false positives). Excluded from source scan.
            if stem in ("log", "CHANGELOG"):
                continue

            # Aliases count
            alias_count = self._db._conn.execute(
                "SELECT COUNT(*) FROM aliases WHERE note_id = ?", (note_id,)
            ).fetchone()[0]
            if alias_count < 4:
                low_aliases.append({"stem": stem, "path": path, "count": alias_count})

            # Tags count
            tag_count = self._db._conn.execute(
                "SELECT COUNT(*) FROM tags WHERE note_id = ?", (note_id,)
            ).fetchone()[0]
            if tag_count == 0:
                no_tags.append({"stem": stem, "path": path})

            # Backlinks + wikilinks
            backlink_count = self._db._conn.execute(
                "SELECT COUNT(DISTINCT source_id) FROM links WHERE target = ?", (stem,)
            ).fetchone()[0]
            wikilink_count = self._db._conn.execute(
                "SELECT COUNT(*) FROM links WHERE source_id = ?", (note_id,)
            ).fetchone()[0]
            if backlink_count == 0 and wikilink_count == 0:
                orphans.append({"stem": stem, "path": path})

            # YAML lint via re-parse (catches duplicated aliases)
            full_path = self._vault / path
            if full_path.exists():
                try:
                    content = full_path.read_text(encoding="utf-8", errors="replace")
                    parsed = parse_note(stem, path, content)
                    if parsed.lint_warnings:
                        broken_yaml.append({"stem": stem, "path": path, "warnings": parsed.lint_warnings})
                except Exception as e:
                    broken_yaml.append({"stem": stem, "path": path, "warnings": [str(e)]})

            # Broken wikilinks
            outgoing = self._db._conn.execute(
                "SELECT target FROM links WHERE source_id = ?", (note_id,)
            ).fetchall()
            for link in outgoing:
                target = link["target"]
                # Normalize: strip #section, strip leading folder paths, lowercase
                stem_only = target.split("#", 1)[0]
                if "/" in stem_only:
                    stem_only = stem_only.rsplit("/", 1)[-1]
                stem_only_lower = stem_only.lower().strip()
                if not stem_only_lower:
                    continue  # pure #section ref to current note
                # Skip known structural false-positives
                if _is_lint_excluded_wikilink(stem_only_lower):
                    continue
                if stem_only_lower not in all_stems_lower and stem_only_lower not in all_aliases_lower:
                    broken_wikilinks.append({"source": stem, "target": target})

        lines = ["# Lint vault forge-brain", ""]
        lines.append(f"## Notes avec aliases < 4 ({len(low_aliases)} total, top {min(limit, len(low_aliases))})")
        for item in low_aliases[:limit]:
            lines.append(f"- [[{item['stem']}]] ({item['count']} aliases) — {item['path']}")
        lines.append("")
        lines.append(f"## Notes sans tag ({len(no_tags)} total, top {min(limit, len(no_tags))})")
        for item in no_tags[:limit]:
            lines.append(f"- [[{item['stem']}]] — {item['path']}")
        lines.append("")
        lines.append(f"## Notes orphelines — 0 backlink + 0 wikilink ({len(orphans)} total, top {min(limit, len(orphans))})")
        for item in orphans[:limit]:
            lines.append(f"- [[{item['stem']}]] — {item['path']}")
        lines.append("")
        lines.append(f"## Frontmatter YAML casse ({len(broken_yaml)} total)")
        for item in broken_yaml[:limit]:
            warns = "; ".join(item["warnings"])
            lines.append(f"- [[{item['stem']}]] — {warns}")
        lines.append("")
        lines.append(f"## Wikilinks brises — cible inexistante ({len(broken_wikilinks)} total, top {min(limit, len(broken_wikilinks))})")
        for item in broken_wikilinks[:limit]:
            lines.append(f"- [[{item['source']}]] -> [[{item['target']}]] (n'existe pas)")
        return "\n".join(lines)

    def update_property(
        self, file: str, name: str, value: str | list, username: str = "anonymous"
    ) -> str:
        """Modifie UNE propriete frontmatter par splice chirurgical (array-safe).

        value peut etre un scalaire (str) ou une liste (str list) : une liste produit
        un array bloc YAML, preservant la structure des champs liste (tags/aliases/sources).
        Seul le span de la propriete ciblee change ; le reste du fichier reste byte-for-byte.
        """
        path = self._db.resolve_note(file)
        if not path:
            return f"Note '{file}' introuvable."
        full_path = self._vault / path
        # newline="" : IO byte-exact — pas de traduction \r\n<->\n par la couche texte.
        # Le helper est ainsi la SEULE autorite sur les fins de ligne (zero-diff garanti
        # par construction : un fichier LF reste LF, un CRLF reste CRLF).
        content = full_path.read_text(encoding="utf-8", errors="replace", newline="")

        try:
            new_content = _set_property_in_frontmatter(content, name, value)
        except ValueError as e:
            return f"REFUS: {e}"

        full_path.write_text(new_content, encoding="utf-8", newline="")
        parsed = parse_note(full_path.stem, path, new_content)
        self._db.index_note(parsed, full_path.stat().st_mtime)
        if self._git and self._git._cfg.auto_commit:
            self._git.commit_file(path, username, "update", full_path.stem)
        return f"Propriete '{name}' mise a jour dans: {path}"


def register_tools(mcp, tools: BrainTools):
    """Register all brain tools on the MCP server.

    All tools wrapped with usage_log.log_call() automatically (via _tool decorator below).
    """

    def _tool(fn):
        """Wrap fn with log_call before registering with @mcp.tool()."""
        wrapped = log_call(fn.__name__)(fn)
        return mcp.tool()(wrapped)

    @_tool
    def search_brain(query: str, limit: int = 5, context: bool = True) -> str:
        """Recherche dans le vault forge-brain.

        Args:
            query: terme de recherche (ex: "context engineering", "agents autonomes", "erreur")
            limit: nombre max de resultats (default 5)
            context: si True, retourne les lignes autour de chaque match
        """
        return tools.search_brain(query, limit, context)

    @_tool
    def read_note(file: str, max_lines: int = 0, offset: int = 0, limit_chars: int = 0) -> str:
        """Lit une note par son nom ou alias (resolution wikilink).

        Args:
            file: nom de la note ou alias (ex: "Raphael-Picard", "Claude-Forge", "vibe coding")
            max_lines: si > 0, tronque la note apres N lignes (legacy)
            offset: pagination char-based, sauter N chars depuis le debut (utile pour CHANGELOG, log)
            limit_chars: pagination char-based, retourner max N chars
        """
        return tools.read_note(file, max_lines, offset, limit_chars)

    @_tool
    def read_note_by_path(path: str) -> str:
        """Lit une note par son chemin exact dans le vault.

        Args:
            path: chemin relatif (ex: "1-Projets/Neoteem/Neoteem.md", "04-Techniques/patterns/Workflow Boris.md")
        """
        return tools.read_note_by_path(path)

    @_tool
    def get_backlinks(file: str) -> str:
        """Liste les notes qui pointent vers cette note.

        Args:
            file: nom de la note sans chemin ni extension
        """
        return tools.get_backlinks(file)

    @_tool
    def get_tags() -> str:
        """Liste tous les tags du vault tries par frequence."""
        return tools.get_tags()

    @_tool
    def get_property(file: str, name: str) -> str:
        """Lit une propriete du frontmatter YAML d'une note.

        Args:
            file: nom de la note ou alias
            name: nom de la propriete (ex: "derniere-maj")
        """
        return tools.get_property(file, name)

    @_tool
    def create_note(path: str, content: str) -> str:
        """Cree une nouvelle note dans le vault.

        Args:
            path: chemin relatif (ex: "07-Support/faq/faq-sujet.md")
            content: contenu complet (frontmatter YAML + body markdown)
        """
        return tools.create_note(path, content)

    @_tool
    def append_note(file: str, content: str) -> str:
        """Ajoute du contenu a la fin d'une note existante.

        Args:
            file: nom de la note ou alias
            content: contenu markdown a ajouter
        """
        return tools.append_note(file, content)

    @_tool
    def update_note(file: str, content: str) -> str:
        """Remplace EN ENTIER le contenu d'une note existante (frontmatter + body).

        Args:
            file: nom de la note ou alias
            content: nouveau contenu complet (frontmatter YAML + body markdown)
        """
        return tools.update_note(file, content)

    @_tool
    def insert_section(file: str, marker: str, content: str, position: str = "after") -> str:
        """Insere du contenu avant/apres une section markdown reperee par son header exact.

        Args:
            file: nom de la note ou alias
            marker: ligne header complete (ex: "## COMMENT")
            content: contenu markdown a inserer
            position: "before" ou "after" le marker (default "after")
        """
        return tools.insert_section(file, marker, content, position)

    @_tool
    def list_notes(folder: str = "", limit: int = 50) -> str:
        """Liste les notes d'un dossier du vault.

        Args:
            folder: prefixe de chemin (ex: "1-Projets/Neoteem", "Knowledge/erreurs"). Vide = tout le vault.
            limit: nombre max (default 50)
        """
        return tools.list_notes(folder, limit)

    @_tool
    def vault_stats() -> str:
        """Statistiques du vault : nombre de notes, tags, wikilinks, aliases, repartition par dossier."""
        return tools.vault_stats()

    @_tool
    def update_property(file: str, name: str, value: str | list[str]) -> str:
        """Modifie une propriete du frontmatter YAML d'une note (array-safe).

        Splice chirurgical : seule la propriete ciblee change, le reste du fichier
        reste byte-for-byte (pas de reformatage du frontmatter entier).

        Args:
            file: nom de la note ou alias
            name: nom de la propriete
            value: nouvelle valeur. SCALAIRE (str) -> ligne simple. LISTE (str list) ->
                   array bloc YAML, pour les champs liste tags/aliases/sources sans corruption.
                   Ex liste : value=["#type/index", "#domaine/claude-code"]
        """
        return tools.update_property(file, name, value)

    @_tool
    def delete_note(file: str, force: bool = False) -> str:
        """Supprime une note du vault et de l'index. Refuse si backlinks > 0 sauf force=True.

        Args:
            file: nom de la note ou alias
            force: si True, supprime meme si des notes pointent vers elle (wikilinks deviendront brises)
        """
        return tools.delete_note(file, force)

    @_tool
    def move_note(file: str, new_path: str, update_wikilinks: bool = True) -> str:
        """Deplace une note vers un nouveau chemin. Met a jour les wikilinks dans les backlinks
        si le stem change.

        Args:
            file: nom de la note ou alias
            new_path: chemin de destination relatif au vault (ex: "Archive/old-note.md")
            update_wikilinks: si True, parcourt les backlinks et remplace [[old-stem]] -> [[new-stem]]
                              (gere les variantes [[stem|alias]] et [[stem#section]]). Default True.
        """
        return tools.move_note(file, new_path, update_wikilinks)

    @_tool
    def lint_vault(limit: int = 50) -> str:
        """Detecte les problemes de qualite dans le vault (aliases<4, orphelines, sans tag,
        YAML casse, wikilinks brises). Layer raw/ exclu (Karpathy immutable).

        Args:
            limit: nombre max de problemes par categorie (default 50)
        """
        return tools.lint_vault(limit)

    @_tool
    def bulk_update_property(files: list[str], name: str, value: str | list[str]) -> str:
        """Met a jour la meme propriete sur N notes en 1 appel (economie round-trips LLM).

        Array-safe (delegue a update_property) : value scalaire OU liste.

        Args:
            files: liste de noms/aliases (ex: ["alpha", "bravo", ...])
            name: nom propriete frontmatter
            value: nouvelle valeur (scalaire str OU liste str pour un champ liste)

        Cas d'usage : update derniere-maj sur 16 leaders apres audit = 1 appel au lieu de 16.
        """
        return tools.bulk_update_property(files, name, value)

    @_tool
    def read_section(file: str, heading: str, include_subsections: bool = True) -> str:
        """Lit UNE section d'une note (header markdown jusqu'au prochain header de meme niveau).

        Args:
            file: nom de la note ou alias
            heading: header complet exact (ex: "## COMMENT", "### Workflow")
            include_subsections: si True, inclut sous-headers

        Cas d'usage : CHANGELOG 62k chars, section "2026-05-24" = ~2k chars (economie 30x).
        """
        return tools.read_section(file, heading, include_subsections)

    @_tool
    def find_by_property(
        name: str,
        value: str = "",
        comparator: str = "eq",
        folder: str = "",
        limit: int = 50,
    ) -> str:
        """Cherche notes dont une propriete frontmatter satisfait une condition (Dataview-equiv pour LLM).

        Args:
            name: nom propriete frontmatter (ex: "derniere-maj", "type", "statut")
            value: valeur (vide si comparator=missing/present)
            comparator: eq | ne | lt | gt | contains | missing | present
            folder: prefixe path optionnel (ex: "05-Leaders/prompt")
            limit: max resultats (default 50)

        Exemples :
        - notes stales : find_by_property("derniere-maj", "2026-04-24", "lt")
        - tous doublons : find_by_property("statut", "doublon")
        - notes sans sources : find_by_property("sources", comparator="missing")
        - type erreur : find_by_property("type", "erreur", folder="Knowledge/erreurs")
        """
        return tools.find_by_property(name, value, comparator, folder, limit)

    @_tool
    def usage_stats(days: int = 7) -> str:
        """Aggregate usage des outils MCP sur les N derniers jours (depuis logs/usage.jsonl).

        Args:
            days: fenetre de jours (default 7)
        """
        stats = _compute_usage_stats(days)
        if not stats:
            return f"Aucun usage enregistre sur les {days} derniers jours."
        lines = [f"# Usage MCP forge-brain — {days} derniers jours\n"]
        lines.append("| Tool | Calls | Total ms | Errors | Avg result chars |")
        lines.append("|------|-------|----------|--------|------------------|")
        sorted_tools = sorted(stats.items(), key=lambda kv: -kv[1]["calls"])
        for tool, s in sorted_tools:
            lines.append(f"| {tool} | {s['calls']} | {s['total_ms']} | {s['errors']} | {s['avg_result_chars']} |")
        return "\n".join(lines)

    @_tool
    def search_sessions(
        query: str,
        limit: int = 20,
        project: str = "",
        role: str = "",
        since: str = "",
    ) -> str:
        """Recherche dans l'historique brut des sessions Claude Code passees (transcripts .jsonl).

        Complement de search_brain : search_brain cherche le savoir CAPITALISE dans le vault,
        search_sessions cherche ce qui s'est dit en conversation mais n'a pas ete capitalise
        ("qu'a-t-on dit la semaine derniere sur X").

        Args:
            query: terme de recherche (FTS plein-texte sur le contenu des messages)
            limit: nombre max de resultats (default 20)
            project: filtre par nom de projet encode (ex: "claude-forge", "ia-back"). Vide = tous.
            role: filtre par role ("user" ou "assistant"). Vide = les deux.
            since: filtre temporel ISO (ex: "2026-05-20"). Vide = pas de borne.
        """
        return tools.search_sessions(query, limit, project, role, since)
