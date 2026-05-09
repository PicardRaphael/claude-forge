"""Git operations: pull main, commit per-user branch, push on schedule."""

import subprocess
from pathlib import Path

from src.config import GitConfig


class GitSync:
    def __init__(self, vault_path: Path, config: GitConfig):
        self._vault = vault_path
        self._cfg = config
        self._active_branches: set[str] = set()

    def _git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(self._vault), *args],
            capture_output=True,
            text=True,
            timeout=60,
        )

    def pull(self):
        self._git("checkout", self._cfg.main_branch)
        self._git("pull", self._cfg.remote, self._cfg.main_branch)

    def commit_file(self, rel_path: str, username: str, action: str, note_name: str):
        branch = f"mcp/{username}"
        self._active_branches.add(branch)

        result = self._git("branch", "--list", branch)
        if branch not in result.stdout:
            self._git("branch", branch, self._cfg.main_branch)

        self._git("checkout", branch)
        self._git("add", rel_path)
        self._git("commit", "-m", f"mcp({username}): {action} {note_name}")

    def push_all(self):
        current = self._git("branch", "--show-current").stdout.strip()
        for branch in self._active_branches:
            self._git("push", self._cfg.remote, branch)
        if current:
            self._git("checkout", current)

    def get_active_branches(self) -> set[str]:
        return self._active_branches.copy()
