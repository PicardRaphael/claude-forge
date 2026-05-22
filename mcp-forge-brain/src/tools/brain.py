"""MCP tools for forge-brain vault — backed by SQLite FTS5."""

import re
from pathlib import Path
from src.database import BrainDB
from src.indexer import parse_note

import yaml


class BrainTools:
    def __init__(self, db: BrainDB, vault_path: Path, git_sync=None):
        self._db = db
        self._vault = vault_path
        self._git = git_sync

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

    def read_note(self, file: str, max_lines: int = 0) -> str:
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
        if max_lines > 0:
            lines = content.split("\n")
            if len(lines) > max_lines:
                return "\n".join(lines[:max_lines]) + f"\n\n... ({len(lines) - max_lines} lignes tronquees)"
        return content

    def read_note_by_path(self, path: str) -> str:
        full_path = self._vault / path
        if not full_path.exists():
            return f"Fichier introuvable: {path}"
        return full_path.read_text(encoding="utf-8", errors="replace")

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
        full_path = self._vault / path
        if full_path.exists():
            return f"Note existe deja: {path}"
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        parsed = parse_note(full_path.stem, path, content)
        alias_warning = ""
        if len(parsed.aliases) < 4:
            alias_warning = f" WARNING: seulement {len(parsed.aliases)} aliases (minimum recommande: 4)"
        self._db.index_note(parsed, full_path.stat().st_mtime)
        if self._git and self._git._cfg.auto_commit:
            self._git.commit_file(path, username, "create", full_path.stem)
        return f"Note creee: {path}{alias_warning}"

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

    def update_property(self, file: str, name: str, value: str, username: str = "anonymous") -> str:
        path = self._db.resolve_note(file)
        if not path:
            return f"Note '{file}' introuvable."
        full_path = self._vault / path
        content = full_path.read_text(encoding="utf-8", errors="replace")

        fm_re = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
        fm_match = fm_re.match(content)
        if fm_match:
            fm_text = fm_match.group(1)
            prop_re = re.compile(rf"^{re.escape(name)}:.*$", re.MULTILINE)
            if prop_re.search(fm_text):
                fm_text = prop_re.sub(f"{name}: {value}", fm_text)
            else:
                fm_text = fm_text.rstrip() + f"\n{name}: {value}"
            content = f"---\n{fm_text}\n---\n{content[fm_match.end():]}"
        else:
            content = f"---\n{name}: {value}\n---\n\n{content}"

        full_path.write_text(content, encoding="utf-8")
        parsed = parse_note(full_path.stem, path, content)
        self._db.index_note(parsed, full_path.stat().st_mtime)
        if self._git and self._git._cfg.auto_commit:
            self._git.commit_file(path, username, "update", full_path.stem)
        return f"Propriete '{name}' mise a jour dans: {path}"


def register_tools(mcp, tools: BrainTools):
    """Register all brain tools on the MCP server."""

    @mcp.tool()
    def search_brain(query: str, limit: int = 5, context: bool = True) -> str:
        """Recherche dans le vault forge-brain.

        Args:
            query: terme de recherche (ex: "context engineering", "agents autonomes", "erreur")
            limit: nombre max de resultats (default 5)
            context: si True, retourne les lignes autour de chaque match
        """
        return tools.search_brain(query, limit, context)

    @mcp.tool()
    def read_note(file: str, max_lines: int = 0) -> str:
        """Lit une note par son nom ou alias (resolution wikilink).

        Args:
            file: nom de la note ou alias (ex: "Raphael-Picard", "Claude-Forge", "vibe coding")
            max_lines: si > 0, tronque la note apres N lignes (economise des tokens)
        """
        return tools.read_note(file, max_lines)

    @mcp.tool()
    def read_note_by_path(path: str) -> str:
        """Lit une note par son chemin exact dans le vault.

        Args:
            path: chemin relatif (ex: "1-Projets/Neoteem/Neoteem.md", "04-Techniques/patterns/Workflow Boris.md")
        """
        return tools.read_note_by_path(path)

    @mcp.tool()
    def get_backlinks(file: str) -> str:
        """Liste les notes qui pointent vers cette note.

        Args:
            file: nom de la note sans chemin ni extension
        """
        return tools.get_backlinks(file)

    @mcp.tool()
    def get_tags() -> str:
        """Liste tous les tags du vault tries par frequence."""
        return tools.get_tags()

    @mcp.tool()
    def get_property(file: str, name: str) -> str:
        """Lit une propriete du frontmatter YAML d'une note.

        Args:
            file: nom de la note ou alias
            name: nom de la propriete (ex: "derniere-maj")
        """
        return tools.get_property(file, name)

    @mcp.tool()
    def create_note(path: str, content: str) -> str:
        """Cree une nouvelle note dans le vault.

        Args:
            path: chemin relatif (ex: "07-Support/faq/faq-sujet.md")
            content: contenu complet (frontmatter YAML + body markdown)
        """
        return tools.create_note(path, content)

    @mcp.tool()
    def append_note(file: str, content: str) -> str:
        """Ajoute du contenu a la fin d'une note existante.

        Args:
            file: nom de la note ou alias
            content: contenu markdown a ajouter
        """
        return tools.append_note(file, content)

    @mcp.tool()
    def update_note(file: str, content: str) -> str:
        """Remplace EN ENTIER le contenu d'une note existante (frontmatter + body).

        Args:
            file: nom de la note ou alias
            content: nouveau contenu complet (frontmatter YAML + body markdown)
        """
        return tools.update_note(file, content)

    @mcp.tool()
    def insert_section(file: str, marker: str, content: str, position: str = "after") -> str:
        """Insere du contenu avant/apres une section markdown reperee par son header exact.

        Args:
            file: nom de la note ou alias
            marker: ligne header complete (ex: "## COMMENT")
            content: contenu markdown a inserer
            position: "before" ou "after" le marker (default "after")
        """
        return tools.insert_section(file, marker, content, position)

    @mcp.tool()
    def list_notes(folder: str = "", limit: int = 50) -> str:
        """Liste les notes d'un dossier du vault.

        Args:
            folder: prefixe de chemin (ex: "1-Projets/Neoteem", "Knowledge/erreurs"). Vide = tout le vault.
            limit: nombre max (default 50)
        """
        return tools.list_notes(folder, limit)

    @mcp.tool()
    def vault_stats() -> str:
        """Statistiques du vault : nombre de notes, tags, wikilinks, aliases, repartition par dossier."""
        return tools.vault_stats()

    @mcp.tool()
    def update_property(file: str, name: str, value: str) -> str:
        """Modifie une propriete du frontmatter YAML d'une note.

        Args:
            file: nom de la note ou alias
            name: nom de la propriete
            value: nouvelle valeur
        """
        return tools.update_property(file, name, value)
