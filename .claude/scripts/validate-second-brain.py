#!/usr/bin/env python3
"""Validate cross-platform second-brain contracts and adapters."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    news_contract = ROOT / "docs/second-brain/news-refresh.md"
    capture_contract = ROOT / "docs/second-brain/session-capture.md"
    for path in (news_contract, capture_contract):
        if not path.is_file() or path.stat().st_size < 1000:
            fail(f"missing or implausibly short contract: {path}")

    claude_news = (ROOT / ".claude/skills/cc-news/SKILL.md").read_text(encoding="utf-8")
    codex_news = (ROOT / ".agents/skills/cc-news/SKILL.md").read_text(encoding="utf-8")
    claude_done = (ROOT / ".claude/skills/done/SKILL.md").read_text(encoding="utf-8")
    codex_done = (ROOT / ".agents/skills/done/SKILL.md").read_text(encoding="utf-8")
    if "docs/second-brain/news-refresh.md" not in claude_news + codex_news:
        fail("news adapters do not reference the shared contract")
    if "docs/second-brain/session-capture.md" not in claude_done + codex_done:
        fail("done adapters do not reference the shared contract")

    stale_refs = list((ROOT / ".agents/skills/cc-news/references").glob("*.md"))
    if stale_refs:
        fail(f"stale Codex news copies remain: {stale_refs}")

    state = load_json(ROOT / ".claude/skills/cc-news/references/freshness-state.json")
    if not isinstance(state, dict) or state.get("schema_version") != 1:
        fail("unsupported freshness schema")
    for key in ("last_complete_run", "last_attempted_run"):
        checkpoint = date.fromisoformat(state[key])
        if checkpoint > date.today():
            fail(f"freshness checkpoint is in the future: {key}")

    allowed_statuses = {"complete", "partial", "failed", "never"}
    domains = state.get("domains")
    if not isinstance(domains, dict) or not domains:
        fail("freshness state has no domains")
    for name, domain in domains.items():
        if domain.get("status") not in allowed_statuses:
            fail(f"invalid freshness status for {name}")
        checked = date.fromisoformat(domain["verified_at"])
        if checked > date.today():
            fail(f"domain checkpoint is in the future: {name}")
        if domain["status"] == "partial" and not domain.get("pending_range"):
            fail(f"partial domain has no pending range: {name}")

    claude_state = domains["claude-code"]
    semver = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
    if not semver.fullmatch(claude_state["latest_version"]):
        fail("invalid Claude Code latest_version")
    if not semver.fullmatch(claude_state["content_checkpoint"]):
        fail("invalid Claude Code content_checkpoint")

    claude_triggers = load_json(ROOT / ".claude/.skill-triggers.json")
    codex_triggers = load_json(ROOT / ".codex/.skill-triggers.json")
    for skill in ("cc-news", "done"):
        if claude_triggers[skill] != codex_triggers[skill]:
            fail(f"trigger drift for {skill}")

    hooks = load_json(ROOT / ".codex/hooks.json")
    hook_blob = json.dumps(hooks, ensure_ascii=False)
    if ".codex/hooks/memory-recall.py" not in hook_blob:
        fail("Codex memory recall is not registered")
    if "C:\\\\Users\\\\rapha" in hook_blob:
        fail("Codex hooks still contain a user-specific absolute path")

    claude_md = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    if "@AGENTS.md" not in claude_md:
        fail("CLAUDE.md does not import the common contract")

    for eval_path in (
        ROOT / ".claude/skills/cc-news/evals/evals.json",
        ROOT / ".claude/skills/done/evals/evals.json",
    ):
        payload = load_json(eval_path)
        if len(payload.get("cases", [])) < 3:
            fail(f"not enough eval cases: {eval_path}")

    print("[OK] second-brain contracts, adapters, state, triggers and hooks are coherent")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, OSError, TypeError, ValueError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1)
