#!/usr/bin/env python3
"""Tests adverses security-guard durci (audit 10 juin 2026).

Scope claimed : rm -rf/-fr toute cible, git branch -D, push --force/-f,
reset --hard sans cible, clean -f. Fail-closed sur payload corrompu.
Hors scope (volontaire) : dd, mkfs, base64, suppression via Python/node.
"""

import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).with_name("security-guard.py")


def run(cmd: str | None) -> int:
    payload = (
        '{"tool_input": {"command": ' + repr_json(cmd) + "}}"
        if cmd is not None
        else "pas-du-json"
    )
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
    )
    return proc.returncode


def repr_json(s: str) -> str:
    import json

    return json.dumps(s)


ADVERSE = [  # attendu exit 2
    "rm -rf ./x",
    "rm -rf ~/Documents",
    "rm -rf $HOME/tmp",
    "rm -fr dossier",
    "rm -rf .",
    "git branch -D feature",
    "git branch -f -D x",
    "git push --force origin main",
]
LEGIT = [  # attendu exit 0
    "rm fichier.txt",
    "rm -f fichier.txt",
    "git branch -d feature",
    "git push origin develop",
    "echo hello",
    "git branch -f develop master",
]

failed = 0
for cmd in ADVERSE:
    code = run(cmd)
    status = "OK" if code == 2 else "FAIL"
    if code != 2:
        failed += 1
    print(f"[{status}] ADVERSE exit={code} :: {cmd}")
for cmd in LEGIT:
    code = run(cmd)
    status = "OK" if code == 0 else "FAIL"
    if code != 0:
        failed += 1
    print(f"[{status}] LEGIT   exit={code} :: {cmd}")

code = run(None)  # payload corrompu → fail-closed
status = "OK" if code == 2 else "FAIL"
if code != 2:
    failed += 1
print(f"[{status}] FAIL-CLOSED exit={code} :: payload corrompu")

print(f"\n{'TOUS VERTS' if failed == 0 else f'{failed} ECHEC(S)'}")
sys.exit(1 if failed else 0)
