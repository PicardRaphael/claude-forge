"""Cross-process lock based on exclusive file creation."""

from __future__ import annotations

import os
import time
from pathlib import Path

from forge_cognition.domain.errors import ConflictError


class FileLock:
    def __init__(self, path: Path, timeout_seconds: float) -> None:
        self.path = path
        self.timeout_seconds = timeout_seconds
        self._fd: int | None = None

    def __enter__(self) -> FileLock:
        deadline = time.monotonic() + self.timeout_seconds
        self.path.parent.mkdir(parents=True, exist_ok=True)
        while True:
            try:
                self._fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(self._fd, str(os.getpid()).encode("ascii"))
                return self
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise ConflictError("mutation lock timeout")
                time.sleep(0.02)

    def __exit__(self, *_args: object) -> None:
        if self._fd is not None:
            os.close(self._fd)
            self._fd = None
        self.path.unlink(missing_ok=True)
