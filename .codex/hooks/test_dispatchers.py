#!/usr/bin/env python3
"""Tests des dispatchers pre-bash-guards / pre-write-guards + chrono vs gardes séparées."""

import json
import subprocess
import sys
import time
from pathlib import Path

HOOKS = Path(__file__).parent


def run(script: str, payload: dict) -> int:
    proc = subprocess.run(
        [sys.executable, str(HOOKS / script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
    )
    return proc.returncode


def bash_payload(cmd: str) -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


def write_payload(path: str) -> dict:
    return {
        "tool_name": "Edit",
        "tool_input": {
            "file_path": path,
            "old_string": "un ancien contenu substantiel de plus de vingt caracteres",
            "new_string": "un nouveau contenu substantiel de plus de vingt caracteres aussi",
        },
    }


failed = 0


def check(label: str, code: int, expected: int) -> None:
    global failed
    ok = code == expected
    if not ok:
        failed += 1
    print(f"[{'OK' if ok else 'FAIL'}] {label} exit={code} attendu={expected}")


# pre-bash-guards : la commande dangereuse est construite par concaténation
danger = "rm " + "-r" + "f ./x"
check("bash ADVERSE (suppression récursive)", run("pre-bash-guards.py", bash_payload(danger)), 2)
check("bash ADVERSE (branche -D)", run("pre-bash-guards.py", bash_payload("git branch " + "-D feat")), 2)
check("bash LEGIT (echo)", run("pre-bash-guards.py", bash_payload("echo bonjour")), 0)
check("bash LEGIT (git status)", run("pre-bash-guards.py", bash_payload("git status")), 0)

# pre-write-guards : SKILL.md forge protégé par delegate-guard
skill = str(HOOKS.parent / "skills" / "recap" / "SKILL.md")
check("write ADVERSE (SKILL.md direct)", run("pre-write-guards.py", write_payload(skill)), 2)
check("write LEGIT (fichier hors scope)", run("pre-write-guards.py", write_payload(str(HOOKS.parent.parent / "memory" / "x.md"))), 0)

# Chrono : dispatcher vs 3 spawns séparés
t0 = time.perf_counter()
run("pre-bash-guards.py", bash_payload("echo x"))
t_dispatcher = (time.perf_counter() - t0) * 1000
t0 = time.perf_counter()
for g in ["commit-herestring-guard.py", "security-guard.py", "vault-cat-guard.py"]:
    run(g, bash_payload("echo x"))
t_separate = (time.perf_counter() - t0) * 1000
print(f"\nChrono Bash : dispatcher={t_dispatcher:.0f}ms vs 3 gardes séparées={t_separate:.0f}ms (gain {t_separate - t_dispatcher:.0f}ms)")

print("TOUS VERTS" if failed == 0 else f"{failed} ECHEC(S)")
sys.exit(1 if failed else 0)
