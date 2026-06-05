#!/usr/bin/env python3
"""Deterministic I/O helper for the align-vault-skills loop.

The LLM does the semantic comparison (vault doctrine vs component prose); this
script owns everything deterministic and therefore unstable-in-an-LLM:
  - kill-switch check
  - date resolution (no Date.now in skill)
  - state journal load / init / merge / save
  - composite idempotence-key generation (readable, NOT hashes)
  - coverage accounting
  - writing the report .md and the state .json (avoids Windows heredoc breakage)

Subcommands
-----------
  check          -> kill-switch + state; prints JSON {stop, state_path, date,
                    resolved, ignored, components}. The skill calls this FIRST.
  filter         -> read candidate gaps from a JSON file, drop those whose key
                    is already in resolved/ignored, print the NEW gaps as JSON.
  write-report   -> read final gaps + coverage from a JSON file, write the
                    report .md AND merge nothing into state; print report path.
  resolve        -> add keys (from --keys) to state.resolved, save.
  ignore         -> add keys (from --keys) to state.ignored, save.

Idempotence key = "<component>::<note>::<direction>" (e.g.
"cc-features-ref::goal::descendant"). Deterministic, human-auditable, and stable
across runs — an LLM-computed hash would not be, breaking the reproducibility
PASS criterion by construction.

All paths are resolved relative to the repo root (parent of .claude/), never cwd.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Repo root = .claude/skills/align-vault-skills/scripts/ -> up 4
REPO_ROOT = Path(__file__).resolve().parents[4]
STATE_PATH = REPO_ROOT / ".claude" / "_alignment-state.json"
STOP_FLAG = REPO_ROOT / ".claude" / ".alignment-loop.stop"
TODO_DIR = REPO_ROOT / "TODO"

EMPTY_STATE = {"resolved": [], "ignored": []}


def resolve_date() -> str:
    """YYYY-MM-DD from the system clock via the OS, not a hardcoded value."""
    try:
        out = subprocess.run(
            ["date", "+%Y-%m-%d"], capture_output=True, text=True, timeout=5
        )
        d = out.stdout.strip()
        if d:
            return d
    except Exception:
        pass
    return datetime.now().strftime("%Y-%m-%d")


def load_state() -> dict:
    if not STATE_PATH.exists():
        return dict(EMPTY_STATE)
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return dict(EMPTY_STATE)
    return {
        "resolved": list(data.get("resolved", [])),
        "ignored": list(data.get("ignored", [])),
    }


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "resolved": sorted(set(state.get("resolved", []))),
        "ignored": sorted(set(state.get("ignored", []))),
    }
    STATE_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def make_key(component: str, note: str, direction: str) -> str:
    """Composite readable idempotence key. Direction in {descendant, montant}."""
    c = (component or "").strip()
    n = (note or "").strip()
    d = (direction or "").strip()
    return f"{c}::{n}::{d}"


def known_keys(state: dict) -> set:
    return set(state.get("resolved", [])) | set(state.get("ignored", []))


def cmd_check(_args) -> int:
    state = load_state()
    if not STATE_PATH.exists():
        save_state(state)  # materialize an empty journal on first run
    print(
        json.dumps(
            {
                "stop": STOP_FLAG.exists(),
                "stop_flag": str(STOP_FLAG),
                "state_path": str(STATE_PATH),
                "date": resolve_date(),
                "resolved": state["resolved"],
                "ignored": state["ignored"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _read_gaps(path: str) -> list:
    gaps = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(gaps, dict):
        gaps = gaps.get("gaps", [])
    return gaps


def cmd_filter(args) -> int:
    """Keep only gaps whose key is NOT already in resolved/ignored."""
    state = load_state()
    seen = known_keys(state)
    gaps = _read_gaps(args.gaps)
    out = []
    for g in gaps:
        key = g.get("key") or make_key(
            g.get("component", ""), g.get("note", ""), g.get("direction", "")
        )
        g["key"] = key
        if key not in seen:
            out.append(g)
    print(json.dumps({"new_gaps": out, "count": len(out)}, ensure_ascii=False, indent=2))
    return 0


def cmd_write_report(args) -> int:
    """Write TODO/alignment-report-<date>.md from a JSON payload.

    Payload shape:
      {"date": "...", "coverage": {"expected": N, "scanned": N, "components": [...]},
       "verdict": {"coverage": bool, "reproducibility": "...", "sample": "...",
                   "pass": bool, "notes": "..."},
       "new_gaps": [{component, direction, note, action, key}, ...]}
    """
    payload = json.loads(Path(args.payload).read_text(encoding="utf-8"))
    date = payload.get("date") or resolve_date()
    cov = payload.get("coverage", {})
    verdict = payload.get("verdict", {})
    gaps = payload.get("new_gaps", [])

    lines = []
    lines.append(f"# Alignment report — {date}")
    lines.append("")
    lines.append("> Généré par la skill `align-vault-skills` (loop hebdo). "
                 "Lecture seule : aucun composant modifié. Raphaël déclenche les dispatches.")
    lines.append("")

    # Verification verdict block
    expected = cov.get("expected", 0)
    scanned = cov.get("scanned", 0)
    cov_ok = verdict.get("coverage", scanned == expected and expected > 0)
    overall = "PASS" if verdict.get("pass") else "FAIL"
    lines.append("## Vérification")
    lines.append("")
    lines.append(f"- **Verdict global :** {overall}")
    lines.append(f"- **Couverture :** {scanned}/{expected} composants scannés "
                 f"({'OK' if cov_ok else 'INCOMPLET'})")
    lines.append(f"- **Reproductibilité :** {verdict.get('reproducibility', 'non vérifiée ce cycle')}")
    lines.append(f"- **Échantillon (0 faux positif) :** {verdict.get('sample', 'non vérifié ce cycle')}")
    if verdict.get("notes"):
        lines.append(f"- **Notes :** {verdict['notes']}")
    lines.append("")

    # Gaps
    lines.append(f"## Nouveaux écarts ({len(gaps)})")
    lines.append("")
    if not gaps:
        lines.append("_Aucun nouvel écart. Le set d'écarts traités/ignorés couvre l'état actuel._")
    else:
        lines.append("| # | Composant cible | Sens | Note vault | Action suggérée |")
        lines.append("|---|---|---|---|---|")
        for i, g in enumerate(gaps, 1):
            comp = g.get("component", "?")
            direction = g.get("direction", "?")
            note = g.get("note", "?")
            action = g.get("action", "?").replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {i} | {comp} | {direction} | {note} | {action} |")
        lines.append("")
        lines.append("### Clés d'idempotence (à archiver dans l'état après traitement)")
        lines.append("")
        for g in gaps:
            lines.append(f"- `{g.get('key', '')}`")
    lines.append("")

    TODO_DIR.mkdir(parents=True, exist_ok=True)
    report_path = TODO_DIR / f"alignment-report-{date}.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"report_path": str(report_path), "gap_count": len(gaps)},
                     ensure_ascii=False))
    return 0


def cmd_resolve(args) -> int:
    state = load_state()
    state["resolved"].extend(args.keys)
    save_state(state)
    print(json.dumps({"resolved_total": len(set(state["resolved"]))}, ensure_ascii=False))
    return 0


def cmd_ignore(args) -> int:
    state = load_state()
    state["ignored"].extend(args.keys)
    save_state(state)
    print(json.dumps({"ignored_total": len(set(state["ignored"]))}, ensure_ascii=False))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Deterministic I/O for align-vault-skills.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="kill-switch + state + date")

    sp = sub.add_parser("filter", help="drop already-known gaps")
    sp.add_argument("--gaps", required=True, help="path to candidate gaps JSON")

    sp = sub.add_parser("write-report", help="write the markdown report")
    sp.add_argument("--payload", required=True, help="path to report payload JSON")

    sp = sub.add_parser("resolve", help="mark keys resolved")
    sp.add_argument("--keys", nargs="+", required=True)

    sp = sub.add_parser("ignore", help="mark keys ignored")
    sp.add_argument("--keys", nargs="+", required=True)

    args = p.parse_args()
    return {
        "check": cmd_check,
        "filter": cmd_filter,
        "write-report": cmd_write_report,
        "resolve": cmd_resolve,
        "ignore": cmd_ignore,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
