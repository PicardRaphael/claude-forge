#!/usr/bin/env python3
"""Quelles skills et quels agents servent reellement, d'apres .claude/_metrics/.

Croise les invocations journalisees par le hook metrics-tracker avec les skills
et agents declares, pour separer ce qui sert de ce qui coute sans servir.

Usage :
    py .claude/scripts/skills-usage.py [--days N]

Ce que ce rapport peut affirmer, et ce qu'il ne peut pas :

  - Il ne voit que la FENETRE COLLECTEE, affichee en tete. Un composant absent
    du rapport n'est pas mort : il est absent de cette fenetre. Le distinguer
    demande une fenetre assez longue, pas une lecture plus fine.
  - Les enregistrements anterieurs au champ `target` portent l'outil sans sa
    cible. Ils sont comptes a part, jamais fondus dans les totaux.
  - Une skill chargee par le modele sans passer par l'outil Skill (routage
    implicite depuis une description) n'apparait pas. Le journal compte les
    invocations explicites : appel d'outil ou commande tapee.
"""
import argparse
import collections
import json
import os
import sys
from datetime import datetime, timedelta, timezone

def _repo_root():
    """Racine du depot principal, meme depuis un worktree.

    Doit resoudre exactement comme metrics-tracker.py : l'analyse lit la ou le
    hook ecrit, sinon un lancement depuis un worktree ne verrait aucune donnee.
    """
    here = os.path.abspath(__file__)
    parts = here.replace("\\", "/").split("/")
    for i in range(len(parts) - 1, 0, -1):
        if parts[i] == "worktrees" and parts[i - 1] == ".claude":
            return "/".join(parts[: i - 1])
    return os.path.dirname(os.path.dirname(os.path.dirname(here)))


_REPO = _repo_root()

# Outils dont l'enregistrement designe une skill, une commande ou un agent.
_SKILL_TOOLS = ("Skill", "SlashCommand", "UserPrompt")
_AGENT_TOOLS = ("Agent", "Task")


def _normalise(target):
    """'.claude/worktrees/x:hook-creator' -> 'hook-creator'."""
    return str(target or "").split(":")[-1].strip()


def _declared():
    skills = sorted(
        d for d in os.listdir(os.path.join(_REPO, ".claude", "skills"))
        if os.path.isfile(os.path.join(_REPO, ".claude", "skills", d, "SKILL.md"))
    ) if os.path.isdir(os.path.join(_REPO, ".claude", "skills")) else []
    agents_dir = os.path.join(_REPO, ".claude", "agents")
    agents = sorted(
        f[:-3] for f in os.listdir(agents_dir) if f.endswith(".md")
    ) if os.path.isdir(agents_dir) else []
    return skills, agents


def _load(metrics_dir, days):
    """Enregistrements du journal, filtres sur les N derniers jours."""
    if not os.path.isdir(metrics_dir):
        return [], set()
    floor = None
    if days:
        floor = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    records, dates = [], set()
    for name in sorted(os.listdir(metrics_dir)):
        if not name.endswith(".jsonl"):
            continue
        day = name[: -len(".jsonl")]
        if floor and day < floor:
            continue
        path = os.path.join(metrics_dir, name)
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except ValueError:
                        continue
            dates.add(day)
        except OSError:
            continue
    return records, dates


def _tally(records, tools):
    """(invocations, jours distincts, sessions distinctes) par cible."""
    hits = collections.Counter()
    days = collections.defaultdict(set)
    sessions = collections.defaultdict(set)
    untargeted = collections.Counter()
    for rec in records:
        tool = rec.get("tool", "")
        if tool not in tools:
            continue
        target = _normalise(rec.get("target"))
        if not target:
            untargeted[tool] += 1
            continue
        hits[target] += 1
        days[target].add(str(rec.get("ts", ""))[:10])
        sessions[target].add(rec.get("session_id", ""))
    return hits, days, sessions, untargeted


def _report(label, hits, days, sessions, untargeted, declared):
    seen = {t for t in hits if t in declared}
    print(f"=== {label.upper()} VUS ({len(seen)}/{len(declared)} declares) ===")
    for target, n in hits.most_common():
        if target in declared:
            print(f"  {target:34s} {n:4d} inv.  {len(days[target]):3d} j  "
                  f"{len(sessions[target]):3d} sess.")
    hors = [(t, n) for t, n in hits.most_common() if t not in declared]
    if hors:
        print(f"  -- vus mais non declares ici (builtin, autre repo, renomme) --")
        for target, n in hors:
            print(f"  {target:34s} {n:4d} inv.")
    absents = [d for d in declared if d not in seen]
    if absents:
        print(f"  -- absents de la fenetre ({len(absents)}) : "
              f"pas une preuve de mort --")
        print("     " + ", ".join(absents))
    if untargeted:
        total = sum(untargeted.values())
        print(f"  -- {total} enregistrement(s) sans champ `target` "
              f"(anterieurs au champ) : {dict(untargeted)}")
    print()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=0,
                    help="ne garder que les N derniers jours (0 = tout)")
    args = ap.parse_args()

    metrics_dir = os.path.join(_REPO, ".claude", "_metrics")
    records, dates = _load(metrics_dir, args.days)

    if not records:
        print(f"Aucune metrique dans {metrics_dir}.")
        print("Le hook metrics-tracker alimente ce journal a partir de sa mise en")
        print("service ; il faut laisser passer quelques sessions avant de conclure.")
        return 0

    print(f"journal : {metrics_dir}")
    print(f"fenetre couverte : {min(dates)} -> {max(dates)} "
          f"({len(dates)} jour(s) avec donnees, {len(records)} enregistrements)")
    print("Un composant absent de cette fenetre n'est pas prouve mort.")
    print()

    skills, agents = _declared()
    _report("skills", *_tally(records, _SKILL_TOOLS), declared=skills)
    _report("agents", *_tally(records, _AGENT_TOOLS), declared=agents)

    volume = collections.Counter()
    for rec in records:
        try:
            volume[rec.get("tool", "")] += int(rec.get("estimated_tokens", 0))
        except (TypeError, ValueError):
            continue
    print("=== VOLUME D'I/O OUTILS (proxy chars/3.3, jamais les tokens API) ===")
    for tool, tokens in volume.most_common(12):
        print(f"  {tool:34s} ~{tokens:8d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
