#!/usr/bin/env python3
"""Retire les lignes d'index (MEMORY.md + _index_archive.md) dont le (slug.md) est dans la purge list."""
import re
import sys
from pathlib import Path

REPO = Path(r"C:\Users\raphael.picard_neote\Documents\claude-forge")
MEM = REPO / "memory"
purge = [l.strip() for l in (REPO / ".claude" / "_purge_list.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
purge_set = set(purge)

def clean_index(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    kept = []
    removed = 0
    for line in lines:
        m = re.search(r"\((feedback_[a-z0-9_]+)\.md\)", line)
        if m and m.group(1) in purge_set:
            removed += 1
            continue
        kept.append(line)
    path.write_text("".join(kept), encoding="utf-8")
    return removed

r1 = clean_index(MEM / "MEMORY.md")
r2 = clean_index(MEM / "_index_archive.md")
print(f"MEMORY.md: {r1} lignes retirees")
print(f"_index_archive.md: {r2} lignes retirees")
print(f"Total: {r1 + r2} (attendu 50)")
