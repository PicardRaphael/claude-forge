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

    def read_note(self, file: str) -> str:
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
        return full_path.read_text(encoding="utf-8", errors="replace")

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
        self._db.index_note(parsed, full_path.stat().st_mtime)
        if self._git and self._git._cfg.auto_commit:
            self._git.commit_file(path, username, "create", full_path.stem)
        return f"Note creee: {path}"

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
            try:
                fm = yaml.safe_load(fm_match.group(1))
                if not isinstance(fm, dict):
                    fm = {}
            except yaml.YAMLError:
                fm = {}
            fm[name] = value
            new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
            content = f"---\n{new_fm}\n---\n{content[fm_match.end():]}"
        else:
            fm = {name: value}
            new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
            content = f"---\n{new_fm}\n---\n\n{content}"

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
    def read_note(file: str) -> str:
        """Lit une note par son nom ou alias (resolution wikilink).

        Args:
            file: nom de la note ou alias (ex: "Raphael-Picard", "Claude-Forge", "vibe coding")
        """
        return tools.read_note(file)

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
