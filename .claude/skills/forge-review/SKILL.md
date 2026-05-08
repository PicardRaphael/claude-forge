---
name: forge-review
description: Monthly strategic review that challenges forge's status quo -- reads CLAUDE.md, rules, top skills, and all agents then delivers a frank KILL/EVOLVE/KEEP/MISSING verdict with evidence. Use when questioning whether the current setup is still optimal.
argument-hint: "[--output path/to/report.md]"
user-invokable: true
allowed-tools: Read, Glob, Grep, Bash
effort: high
memory: project
---

# forge-review -- Scheduled Status Quo Challenger

NOT a conformity audit (self-check does that). NOT an external project analysis (evolve does that).
This is a frank strategic challenge: is forge still on the best path, or are we running on habit?

## When to run

```
/forge-review                                              -- interactive report in chat
/forge-review --output output/forge-review-2026-05.md     -- persist for comparison
/schedule monthly /forge-review --output output/forge-review-YYYY-MM.md
```

## Differentiation

| If the user wants... | Correct skill |
|---|---|
| Vault note quality, orphans, frontmatter | vault-audit |
| YAML conformity, lengths, kebab-case | self-check |
| External project product/architecture evolution | evolve |
| Strategic challenge of forge own .claude/ setup | **forge-review** |

---

## Phase 1 -- Inventory with evidence

Collect all components and attach evidence before making any verdict. No evidence = no verdict.

### 1a. Component list

```bash
# All skills
find .claude/skills/ -name "SKILL.md" | sort

# All agents
ls .claude/agents/*.md 2>/dev/null

# All rules
ls .claude/rules/*.md 2>/dev/null

# CLAUDE.md line count
wc -l CLAUDE.md
```

### 1b. Last-modified dates per component

```bash
# Skills by last commit date (top 15 most recent)
git log --pretty=format:'%ai' --name-only -- '.claude/skills/*/SKILL.md' \
  | grep -v '^$' | paste - - | sort -rk1 | head -20

# Agents by last modified
git log --pretty=format:'%ai %s' -- '.claude/agents/' | head -20

# Rules by last modified
git log --pretty=format:'%ai %s' -- '.claude/rules/' | head -20
```

### 1c. Reference counts (cross-references)

A component with zero cross-references is a KILL candidate.

```bash
# Skills with zero references in agents/rules/CLAUDE.md
for skill_dir in .claude/skills/*/; do
  name=$(basename "$skill_dir")
  refs=$(grep -rw "$name" .claude/agents/ .claude/rules/ CLAUDE.md 2>/dev/null | wc -l)
  echo "$refs $name"
done | sort -n | head -20
```

### 1d. Core document reads

Read in full (in parallel):
- CLAUDE.md
- All .claude/rules/*.md
- .claude/agent-memory/skill-creator/MEMORY.md (project memory index)

---

## Phase 2 -- Per-component verdict

For each component, apply the 3 questions. Require evidence before concluding.

**Q1 -- Would removing this cause real problems?**
Evidence required: ref count + last-modified date.
If refs=0 AND last-modified > 60 days: lean KILL. Both conditions must hold.

**Q2 -- Is there a technique that makes this 10x better?**
Cross-reference forge-brain before asserting improvement exists:
```bash
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" \
  search query="<component topic> best practices 2026" limit=5
```
If forge-brain returns nothing concrete: label KEEP with note "no newer technique found".

**Q3 -- Habit or genuinely best approach?**
Signals of cargo cult:
- Identical content in a rule AND in CLAUDE.md (duplication)
- Skill description that does not trigger anything specific
- Rule that predates a hook that now enforces the same behavior deterministically
- Agent with permissionMode: plan whose only function is to read files Claude can read directly

### Verdict labels

| Label | Meaning | Evidence threshold |
|-------|---------|-----------|
| KILL | Remove -- dead weight | refs=0 AND last-modified > 60 days |
| EVOLVE | Works, but 10x better exists | forge-brain confirms newer technique |
| KEEP | Genuinely solid | Referenced, recent, best technique confirmed |
| MISSING | Gap vs baseline checklist | Grounded in references/baseline.md or forge-brain |

---

## Phase 3 -- MISSING check vs baseline

Compare forge against `references/baseline.md`. Any absent item = MISSING candidate.
Verify each MISSING claim against forge-brain before asserting it -- do not invent gaps from vague LLM memory.

```bash
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" \
  search query="<potential missing component> claude code" limit=5
```

---

## Phase 4 -- Report format

Tone: frank, zero hedging. Every verdict ends with evidence in parentheses.

Banned words: "perhaps", "might", "could be considered", "it may be worth", "potentially".
Evidence format: (last modified: YYYY-MM-DD, N cross-references)

```markdown
# forge-review -- YYYY-MM-DD

## Delta vs YYYY-MM (if previous report exists)
- KILL items actioned: [list] / [total from previous KILL]
- KILL items still pending: [list]
- New items since last review: [list]

---

## KILL (remove these)
- **rule/X** -- [reason in one sentence] (last modified: YYYY-MM-DD, 0 cross-references)
- **skill/Y** -- [reason] (last modified: YYYY-MM-DD, 0 agent references, duplicates Z)

## EVOLVE (works but 10x better is achievable)
- **skill/Z** -- [current weakness] >> [concrete improvement] (last modified: YYYY-MM-DD, forge-brain:[[Note]])
- **CLAUDE.md Section X** -- [issue] >> [proposed direction] (N lines, duplicates rule/Y)

## KEEP (genuinely good -- do not touch)
- **agent/A** -- [why solid] (N cross-references, last modified: YYYY-MM-DD)
- **rule/B** -- [why it holds] (...)

## MISSING (should exist, does not)
- **[type/name]** -- [gap it fills] (source: baseline.md item X)

## Verdicts discarded
[Minimum 2 items considered for KILL or EVOLVE but not flagged -- prove the curation was deliberate]

---
Scope: N skills | N agents | N rules | CLAUDE.md
Forge-brain queries: N
Generated: YYYY-MM-DD
```

---

## Phase 5 -- Output

**Interactive mode (default):** Print the report in chat.

**File mode (`--output path`):** Write the report to the given path for month-over-month comparison.

```bash
# Check for previous reports before writing
ls output/forge-review-*.md 2>/dev/null | sort | tail -3
```

If previous reports exist, populate the Delta section. This is the primary value of file mode -- it tracks whether KILL verdicts actually get actioned.

---

## Gotchas

**MISSING without baseline evidence is hallucination.** Every MISSING item must map to a specific entry in `references/baseline.md` or a forge-brain query result. No free-form "I think forge should have X" verdicts.

**Read-only on .claude/ and vault/. Output/ is the only exception.** Never write to .claude/skills/, .claude/agents/, .claude/rules/, CLAUDE.md, or vault files. Reports may be written to output/ only (file mode). The user decides what to action on the verdicts.

**KILL requires two independent signals.** refs=0 alone is insufficient (new components start at 0). last-modified > 60 days alone is insufficient (some rules are intentionally stable). Both must hold simultaneously.

**60-day threshold is a default, not a hard rule.** Skills designed for infrequent use (install-forge, forge-review itself) should not be flagged on stale-date alone. Use judgment: if the use case is monthly/annual by design, last-modified is not a KILL signal.

**Do not inline-rewrite components.** Flag with the correct delegation target:
- SKILL.md rewrite: "EVOLVE -- delegate to skill-creator"
- agents/*.md rewrite: "EVOLVE -- delegate to agent-creator"
- CLAUDE.md rewrite: "EVOLVE -- delegate to claudemd-optimizer"

**Forge-brain pre-check is mandatory for EVOLVE verdicts.** If forge-brain returns no evidence of a better technique, the label stays KEEP with a note.

**Verdicts discarded is mandatory.** At minimum 2 items. Without it, the list looks generated, not curated.

**Do not confuse with vault-audit and self-check.** They are complementary:
- vault-audit: note quality in Obsidian (aliases, frontmatter, wikilinks)
- self-check: .claude/ config conformity (YAML format, line counts, naming)
- forge-review: strategic value of each component (should it exist at all?)

**Second-notice pattern.** If a KILL item from the previous report was not actioned, include it in the next review's KILL list with label "(second notice)". Three reviews without action = escalate to direct conversation.

---

## References

- `references/baseline.md` -- canonical checklist of what forge should have (source of truth for MISSING verdicts)

---

## Apprentissage

After each review, save to project memory what was actioned vs ignored:

```
# Format memoire projet -- project_forge_review.md
Date: YYYY-MM-DD
KILL identified: N | actioned: N | still pending: [list]
EVOLVE identified: N | actioned: N
MISSING identified: N | built: N
Pattern: [recurring theme -- e.g. "rules consistently stale after 90 days"]
```
