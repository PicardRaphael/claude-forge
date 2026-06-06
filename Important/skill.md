# Designing a Near-Perfect Meta-Skill for Claude Code: Create + Optimize Other Skills

## TL;DR
- **Build it as a SKILL (not a subagent), modeled directly on Anthropic's own `skill-creator`** — a clarifying-question interview up front, a draft→test→review→iterate loop that spawns paired with-skill/baseline subagents, an eval-viewer-before-you-judge rule, and a separate description-optimization loop — then add the one thing Anthropic's skill-creator lacks: a **target-environment branch (CLI vs Desktop-app vs Cowork)** that changes which enforcement mechanisms the generated skill is allowed to rely on.
- **The enforcement surfaces differ sharply**: hooks and local/stdio MCP work reliably only in the **CLI**; in the **Desktop app** and **Cowork** hooks are unreliable-to-broken (issues #27398, #40495, #47993, #57209), Cowork only supports **remote HTTPS MCP** (#23424) and unreliably scans `~/.claude/skills` (#50669), and only **~30 skills** display at once (#13343). A generated skill must therefore fall back from hooks → **script-output gating + directive descriptions + slash-command entry + MCP-side validation** as it moves from CLI to Cowork.
- **Reliability of 90–100% comes from the description, not infrastructure**: Seleznov's 650-trial study found directive descriptions ("ALWAYS invoke… Do not X directly") hit **100% activation vs 77% for passive descriptions** (and ~50% for unoptimized "coin-flip" descriptions), and SkillsBench found curated skills add **+16.2pp on average (range +13.6 to +23.3pp)**. Critically, SkillsBench also found that **AI-self-authored skills give negligible-to-negative benefit (–1.3pp average)** — which is the entire justification for a structured, human-in-the-loop meta-skill rather than "ask Claude to write a skill."

## Key Findings

### 1. Anthropic's `skill-creator` is the canonical blueprint — and it is itself a high-quality skill
The official `skill-creator` (in `anthropics/skills`, also shipped as the `skill-creator` plugin and inside Claude.ai/Cowork) is a **485-line, 32 KB SKILL.md** whose description is itself directive: *"Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals…"* It demonstrates the patterns it preaches: progressive disclosure (`scripts/`, `references/schemas.md`, `agents/grader.md|comparator.md|analyzer.md`, `assets/eval_review.html`, `eval-viewer/generate_review.py`), "explain the why" over heavy-handed MUSTs, and environment-adaptive instructions.

### 2. Clarifying questions are a first-class phase, and skills CAN pause to ask
Skills become interactive via the **AskUserQuestion** tool (added v2.0.21; 1–4 questions, 2–4 options each, "Other"/free-text allowed, ~60s timeout, cannot be called from subagents). Community "interview"/elicitation skills lock the tool list to `allowed-tools: AskUserQuestion, Write` to force questioning before implementation. Slash-command `argument-hint` and `$ARGUMENTS`/`$0` substitution provide a lighter-weight input path.

### 3. The three-environment enforcement matrix is the novel core (see table in Details)
Hooks fire reliably only in the CLI. Cowork spawns the CLI with `--setting-sources user`, which silently excludes plugin-scoped hooks (#27398), and a deeper sandbox path mismatch means **user hooks, managed settings, and env overrides are all silent no-ops** in Cowork (#40495). SessionStart hooks don't fire in Cowork (#47993), forcing the "throwaway boot-up message" workaround. The Desktop app's own worktree/session flow bypasses documented hooks (#57209).

### 4. Routing: one rule, one place, at the matching scope
`.claude/rules/` (v2.0.64+) auto-loads every `.md` at the same priority as CLAUDE.md; path-scoped rules load only for matching files. Skill-specific rules belong **inside the skill**; only cross-skill **routing pointers** belong in CLAUDE.md/.claude/rules. Duplicating skill content into CLAUDE.md dilutes priority and creates divergence.

### 5. Skill vs subagent: it should be a skill that spawns subagents
Anthropic's skill-creator is a skill that spawns grader/comparator subagents for evals. A skill is "loaded instructions + scripts the parent runs"; a subagent "forks the parent" with its own context/model/tools. The create+optimize meta-skill wants the doctrine/checklist/workflow of a skill plus the option to delegate eval runs to subagents — exactly the skill-creator pattern.

### 6. The eval harness is what gets you to 90–100%
Generate ~20 realistic trigger queries (8–10 should-fire, 8–10 near-miss should-not-fire), run baseline-without-skill vs with-skill in paired subagents, grade with exact-field-name assertions, aggregate to `benchmark.json` with mean±stddev, and **generate the eval viewer BEFORE judging outputs yourself**. SkillsBench's own takeaway underscores the payoff: **Claude Haiku 4.5 with Skills (27.7%) outperforms Opus 4.5 without Skills (22.0%)** — a well-built skill is worth more than a model-tier upgrade.

## Details

### A. Full annotated breakdown of Anthropic's `skill-creator`

**Frontmatter / description.** `name: skill-creator`; the description packs both *what* (create/modify/optimize/eval/benchmark) and *when* (multiple concrete triggers), modeling the "pushy" directive style the body itself recommends to combat undertriggering. The skill-creator's own canonical example of pushiness is verbatim: *"Make sure to use this skill whenever the user mentions dashboards, data visualization, or internal metrics, even if they do not explicitly ask for a dashboard"* — and it **explicitly flags all-caps MUST/ALWAYS/NEVER as a "yellow flag" to reframe** with reasoning.

**High-level loop (stated at top):** decide what the skill does → write a draft → create test prompts and run claude-with-the-skill → help the user evaluate qualitatively + quantitatively (draft evals while runs happen in the background; use `eval-viewer/generate_review.py`) → rewrite from feedback → repeat → expand the test set and rerun. The skill explicitly tells Claude to **detect where the user already is** in this loop and jump in, and to stay flexible ("just vibe with me" is allowed).

**Communication calibration.** A whole section warns that users range from non-technical to expert and to gate jargon ("JSON", "assertion") on context cues — a humane-design touch.

**Phase 1 — Capture Intent (the question set):**
1. What should this skill enable Claude to do?
2. When should this skill trigger (what user phrases/contexts)?
3. What's the expected output format?
4. Should we set up test cases? (Recommended default: yes for objectively verifiable outputs like file transforms/data extraction/fixed workflows; no for subjective outputs like writing style/art.)
If the conversation already contains a workflow ("turn this into a skill"), extract steps/tools/corrections/IO from history first, then ask the user to fill gaps.

**Phase 2 — Interview & Research:** proactively probe edge cases, IO formats, example files, success criteria, dependencies; research via subagents/MCP in parallel if available. Don't write test prompts until this is ironed out.

**Phase 3 — Write SKILL.md:** name; **directive description** (all "when to use" lives here, "pushy" phrasing); optional `compatibility`; body. Embeds the anatomy diagram, three-level progressive-disclosure model, "keep SKILL.md <500 lines," domain-organization-by-reference-file pattern, "Principle of Lack of Surprise" (no malware/misleading skills), imperative writing, output-format/example patterns, and the "explain the why instead of musty MUSTs" doctrine.

**Phase 4 — Test cases:** write 2–3 realistic prompts, show them to the user for sign-off, save to `evals/evals.json` with assertions left empty.

**Phase 5 — Run evals (the structurally critical phase):** for each test case **spawn two subagents in the same turn** — one with-skill, one baseline. Baseline = no skill (new skill) or a snapshot of the old skill (`cp -r` to `skill-snapshot/`, improving an existing skill). Results go in `<skill>-workspace/iteration-N/eval-<id>/{with_skill,without_skill|old_skill}/outputs/`. Write `eval_metadata.json` per eval with a descriptive name.

**Phase 6 — Draft assertions while runs are in progress** (objectively verifiable, descriptively named, script-checkable where possible; don't force assertions on subjective skills).

**Phase 7 — Capture timing** from each task-completion notification (`total_tokens`, `duration_ms`) into `timing.json` immediately — it's the only chance to capture it.

**Phase 8 — Grade, aggregate, launch viewer:** grader subagent reads `agents/grader.md`, writes `grading.json` whose expectations array must use exactly `text`, `passed`, `evidence` (the viewer depends on these names); `python -m scripts.aggregate_benchmark` produces `benchmark.json`/`benchmark.md` (pass_rate, time, tokens, mean±stddev, delta); analyst pass via `agents/analyzer.md` surfaces non-discriminating assertions, high-variance/flaky evals, time/token tradeoffs; launch `eval-viewer/generate_review.py` (with `--previous-workspace` for iter 2+; `--static` for headless/Cowork).

**Phase 9 — Read feedback & improve:** read `feedback.json`; improvement doctrine = **generalize (don't overfit), keep it lean (read transcripts not just outputs), explain the why (ALL-CAPS MUST is a "yellow flag"), bundle repeated work** (if all subagents independently wrote the same helper script, put it in `scripts/`).

**Phase 10 — Description optimization** (separate `scripts/run_loop.py`): generate **20 trigger queries** (8–10 should-trigger with varied phrasing/uncommon cases; 8–10 should-not-trigger **near-misses** — never trivially irrelevant); review them with the user via `assets/eval_review.html`; run the loop (60/40 train/held-out split, 3 runs per query for a reliable trigger rate, up to 5 iterations, selects `best_description` by **test** score to avoid overfitting). Crucial nuance: **simple one-step queries won't trigger any skill** because Claude handles them directly — eval queries must be substantive.

**Phase 11 — Package** (`python -m scripts.package_skill`) → `.skill` file (only if `present_files`/filesystem available).

**Platform variations baked into the skill** (this is the seed of the three-environment idea): parallel subagents (CLI ✓, Claude.ai ✗, Cowork ✓ with serial fallback on timeout); browser eval viewer (CLI ✓, Claude.ai/Cowork ✗ → `--static`); baseline runs and quantitative benchmarking (skipped on Claude.ai); description optimization needs `claude -p` (CLI/Cowork only). The skill even shouts in all-caps: *"GENERATE THE EVAL VIEWER BEFORE evaluating inputs yourself"* because Cowork otherwise skips it.

**Related skills.** `skill-installer`/`install-skills` (discover/browse/install community skills, pick the right install path per agent), `getting-started`/onboarding skills, and "skilljacking"-style meta-skills that bottle a just-performed workflow into a skill file. The official Claude.ai/Cowork "Plugin Create" plugin builds plugins from templates.

### B. The three-environment enforcement matrix (mid-2026, CC ~v2.1.16x, Opus 4.8)

| Mechanism | Claude Code CLI | Claude Code in Desktop app | Claude Cowork |
|---|---|---|---|
| **PreToolUse/PostToolUse hooks** | ✅ Works | ⚠️ Partial/unreliable (Desktop bypasses some documented hook paths, e.g. WorktreeCreate #57209) | ❌ Broken — user hooks silent no-op (#40495); plugin hooks excluded by `--setting-sources user` (#27398) |
| **SessionStart / UserPromptSubmit / Stop hooks** | ✅ Works (Stop-hook quirks exist) | ⚠️ Unreliable | ❌ SessionStart doesn't fire (#47993); plugin Stop hooks never/again fire (#29767, #51420) |
| **Skills auto-activation (directive description)** | ✅ Works | ✅ Works | ✅ Works (subject to scan/limit bugs below) |
| **Slash-command / explicit invocation** | ✅ Works | ✅ Works | ✅ Works (`/` lists skills) |
| **`disable-model-invocation` / `user-invocable`** | ✅ Works (note bug #26251 where slash invoke is refused) | ✅ Likely | ⚠️ Likely, less tested |
| **Local/stdio MCP** | ✅ Works | ✅ Works (proxied by Desktop) | ❌ Not accessible (#23424) — remote HTTPS only; workaround = supergateway/mcp-remote bridge |
| **Remote HTTPS MCP** | ✅ Works | ✅ Works | ✅ Works (only supported MCP type) |
| **Skills from project `.claude/skills`** | ✅ Works | ✅ Works | ⚠️ Mount/scan bugs on some setups |
| **Skills from `~/.claude/skills`** | ✅ Works | ✅ Works | ❌ Unreliable scan — only UI-registered skills load (#50669); Windows mount issues (#26998) |
| **Plugin-bundled skills** | ✅ Works | ✅ Works | ⚠️ Sometimes not mounted (#31542) |
| **30-skill display limit** | ⚠️ Truncates at ~30 (#13343) | ⚠️ Same | ⚠️ Same + "Showing 30 of N" |
| **CLAUDE.md / .claude/rules** | ✅ Loads | ✅ Loads | ❌ Not reliably loaded in sandbox — use Cowork folder/project **Instructions** instead |
| **Bash / scripts** | ✅ Full (OS sandbox optional via bubblewrap) | ✅ Full | ✅ Inside sandboxed Linux VM (bubblewrap; mounted folders only; egress-limited) |
| **Subagents / Task tool** | ✅ Works | ✅ Works | ✅ Works (serial fallback on timeout) |
| **Scheduled automations** | ⚠️ via `/schedule`/cron triggers | ⚠️ | ✅ `/schedule` (computer must be awake + app open) |
| **`context: fork` + `agent:`** | ⚠️ Ignored when invoked via Skill tool (#17283, #49559) | ⚠️ Same | ⚠️ Same |

**Per-environment recommended enforcement strategy a generated skill should adopt:**
- **CLI:** Hooks are the strong enforcement layer — use PreToolUse to block, PostToolUse to validate/format, plus directive description + script-output gating. Local stdio MCP and CLAUDE.md/.claude/rules routing all work. This is the only surface where you can guarantee deterministic event-driven enforcement.
- **Desktop app:** Treat hooks as best-effort; do NOT rely on them for safety. Lean on directive description, slash-command entry for side-effecting actions (`disable-model-invocation: true`), and script-output gating. Local MCP works (proxied), so MCP-side validation is viable.
- **Cowork:** Assume hooks, CLAUDE.md/.claude/rules, and local MCP all fail. Enforcement = (1) directive description for activation, (2) **script-output gating** (the script prints the verdict and Claude must act on it), (3) **remote HTTPS MCP-side validation** for anything that must be deterministic, (4) Cowork **project/folder Instructions** as the CLAUDE.md substitute, (5) slash-command + AskUserQuestion approval gates for side effects, (6) the `--static` eval-viewer path. Keep total enabled skills under ~30 and install via the UI so they're scanned.

### C. Recommended question set for the meta-skill (with the environment branch)

Ask these via **AskUserQuestion** (batch into ≤4-question rounds; offer a "Recommended" option; stop early when answers are obvious from context). Do NOT over-ask — extract from conversation history first.

**Round 1 — Intent (always):**
1. What should this skill let Claude do? (free text)
2. **Target environment?** → **CLI / Desktop app / Cowork / Portable (must work everywhere)**. *This is the branching question that determines the enforcement strategy and which mechanisms the generated skill may use.*
3. Create new, or optimize/audit an existing skill?

**Round 2 — Triggering & boundaries:**
4. When should it trigger (phrases/contexts)? When should it explicitly NOT trigger (near-misses)?
5. Does it have side effects (deploy/commit/send/delete)? → if yes, recommend `disable-model-invocation: true` + slash-command-only + approval gate.

**Round 3 — Shape & tooling:**
6. Single-file SKILL.md, or scripts + references? (Recommend scripts when deterministic reliability/repeated code; references for docs >300 lines.)
7. What tools/MCP does it need? (Branch on environment: stdio MCP only offered for CLI/Desktop; remote HTTPS for Cowork.)
8. Target model(s)? (Test on the ones you'll use — Haiku needs more guidance, Opus needs less.)
9. Set up evals? (Recommended yes for objectively verifiable outputs.)

Keep it to ~2–3 rounds; the skill-creator deliberately interviews then stops.

### D. Recommended architecture for the create+optimize meta-skill

**Form:** a **SKILL** named in gerund/noun form (e.g., `creating-skills` or `skill-forge`), `user-invocable: true`, auto-invocable on directive description, that **spawns subagents** for eval runs (don't make it a standalone subagent — you want the doctrine/checklist resident and the ability to detect where the user is in the loop). Use `context: fork`/`agent:` cautiously since they're currently ignored when invoked via the Skill tool (#17283, #49559) — issue an explicit "use the Task tool to launch a subagent" instruction in the body as the reliable path.

**Directive description (Seleznov template):** *"Skill-authoring expert. ALWAYS invoke this skill when the user wants to create, write, scaffold, edit, audit, optimize, benchmark, or test a Claude Agent Skill / SKILL.md, or asks why a skill isn't triggering. Do not hand-write SKILL.md directly — use this skill first."*

**Workflow steps:** (1) detect entry point + ask Round-1 questions incl. **environment**; (2) interview; (3) draft SKILL.md with a directive description and environment-appropriate enforcement; (4) write 2–3 task evals + ~20 trigger-eval queries; (5) run paired with-skill/baseline (subagents on CLI/Cowork; inline self-run on Claude.ai); (6) grade + aggregate + **generate eval viewer first**; (7) read feedback, improve (generalize/lean/why/bundle); (8) run description-optimization loop; (9) audit pass (optimization mode); (10) package + tell the user where each surface requires the skill to live.

**Why a skill that spawns subagents, not "ask Claude to write a skill":** SkillsBench's self-generated-skills condition found AI-authored skills give **–1.3pp average benefit** ("models cannot reliably author the procedural knowledge they benefit from consuming"; only Opus 4.6 reached +1.4pp, GPT-5.2 Codex degraded –5.6pp). The structured interview + measurement loop is precisely what converts an unreliable one-shot generation into a curated, benchmarked artifact.

**Scripts to bundle:** `init_skill.py` (scaffold), `package_skill.py` (.skill), `run_loop.py`/`run_eval.py` (description optimization via `claude -p`), `aggregate_benchmark.py`, `eval-viewer/generate_review.py` (with `--static`), plus a new **`audit_skill.py`** (see checklist) and **`detect_environment.py`** (reads env signals like `CLAUDE_CODE_IS_COWORK`, presence of subagents/browser, MCP type) to auto-confirm the environment branch.

**References:** `references/enforcement-matrix.md` (the table above), `references/schemas.md`, `agents/grader.md|analyzer.md|comparator.md`.

### E. Routing guidance (CLAUDE.md / .claude/rules vs the skill)
- **Rule of one place, matching scope.** A given rule lives in exactly one location. Skill-specific behavior stays in the skill body/references. Cross-skill **routing** (e.g., "for any PDF task, use the pdf skill; for spreadsheets, use xlsx") is the only thing that belongs in CLAUDE.md or `.claude/rules/`.
- **`.claude/rules/` (v2.0.64+)** auto-loads all `.md` at CLAUDE.md priority; add a `paths:` frontmatter to scope a rule to matching files so it doesn't saturate priority. Prefer rules files over a 300+ line CLAUDE.md.
- **Don't duplicate** skill content into CLAUDE.md — it dilutes priority ("when everything is high priority, nothing is") and diverges over time.
- **Environment routing:** CLI/Desktop use CLAUDE.md/.claude/rules for routing pointers; **Cowork uses project/folder Instructions** as the reliable equivalent (CLAUDE.md isn't loaded in the sandbox). When a generated skill needs to be discoverable in Cowork, register it via the UI and keep the active set under ~30.

### F. Enriched "near-perfect skill" checklist (with environment + optimization-mode additions)

**1. Discovery / activation**
- Directive description: domain identifier + "ALWAYS invoke when…" + negative constraint ("Do not X directly") (Seleznov: 100% vs 77% passive vs ~50% unoptimized).
- Third-person; what AND when; concrete trigger phrases incl. cases where the user doesn't name the skill.
- Name: kebab-case, ≤64 chars, no "claude"/"anthropic", gerund preferred.
- Description fits the char budget (official cap 1024 chars; Claude Code truncates the combined description+`when_to_use` at ~1536 chars in the skill listing); single-line in YAML (Prettier multi-line breaks discovery); no XML tags.
- Includes near-miss exclusions so it doesn't over-trigger.

**2. Body / execution**
- SKILL.md body <500 lines; references one level deep; ToC for files >100 lines.
- Imperative voice; explain the *why* instead of all-caps MUST; reserve "ALWAYS/exactly this script" for fragile/critical steps only.
- Scripts solve problems (no punting, no voodoo constants); state whether to **execute** vs **read** each script.
- Explicit error handling; forward-slash paths only; list required packages (API has no network install).
- Validation/feedback loops for quality-critical operations; copyable checklist for multi-step workflows.

**3. Structure / enforcement (environment-specific)**
- Choose enforcement per target: **CLI** → hooks OK; **Desktop/Cowork** → script-output gating + slash entry + MCP-side validation.
- Side-effecting skills: `disable-model-invocation: true` + `allowed-tools` whitelist + AskUserQuestion approval gate.
- MCP type matches surface (stdio for CLI/Desktop; remote HTTPS for Cowork).
- Scripts enforce only via their OUTPUT — never assume a script forces Claude to read it.
- Routing pointers in CLAUDE.md/.claude/rules (CLI/Desktop) or project Instructions (Cowork); never duplicate skill content.

**4. Evaluation**
- ≥3 task evals; ~20 trigger queries (8–10 should-fire, 8–10 near-miss should-not-fire; substantive, not one-step).
- Baseline-without-skill vs with-skill; 3–5 trials per case; isolate each run; grade outcomes not paths.
- Read transcripts, not just outputs; generate the eval viewer BEFORE judging.
- Test on Haiku/Sonnet/Opus you'll actually use.

**5. Optimization / audit mode (new)**
- Detect: truncated/over-budget descriptions; passive (non-directive) descriptions; multi-level (>1-deep) reference chains; dead/broken references; missing "why"; ALL-CAPS overuse; missing exclusions; oversized SKILL.md (>500 lines); flat-file skills that should be folders; duplicate/diverging doctrine across skills; non-discriminating assertions; Prettier-mangled multi-line YAML.
- Score and surface each violation with file + one-line fix; re-run until clean.

**6. Packaging / distribution (new)**
- Package as `.skill`; bundle as a plugin for team distribution.
- Confirm where the skill must live to work in each surface: `.claude/skills` (project) / `~/.claude/skills` (user) / plugin-bundled; **Cowork: register via UI** so it's scanned, keep active set <30.
- Preserve name on update (no `-v2`); copy to a writeable temp dir before editing read-only installed skills.

## Recommendations
1. **Ship v1 as a CLI-first skill that clones the skill-creator workflow**, adding the environment question and the audit mode. Reuse skill-creator's scripts (`init_skill.py`, `package_skill.py`, `run_loop.py`, `aggregate_benchmark.py`, `generate_review.py`) rather than reinventing them. Benchmark: every generated skill should pass its own 20-query trigger eval at ≥90% on the target model before you call it done.
2. **Branch enforcement on environment.** If target is CLI, allow hooks; if Desktop/Cowork, the generator must refuse to emit hook-dependent enforcement and instead emit script-output gating + slash entry + (Cowork) remote-MCP validation. Threshold to revisit: if Anthropic fixes #40495/#27398 (Cowork hooks), relax this and allow hooks in Cowork.
3. **Always generate the eval viewer before self-judging**, and on Cowork always pass `--static`. Put it in the TodoList as the skill-creator does.
4. **Default side-effecting skills to manual-only** (`disable-model-invocation: true`) regardless of environment.
5. **Run the audit mode on the meta-skill itself** before shipping — dogfood the optimization path.
6. **Keep routing pointers thin and in one place**; migrate any >300-line CLAUDE.md into path-scoped `.claude/rules/`.
7. **Set the activation target explicitly**: because a weak-model-with-skill beats a strong-model-without-skill (Haiku+skill 27.7% > Opus-no-skill 22.0% on SkillsBench), the meta-skill's value bar is the activation rate and the with-vs-without delta — instrument both.

## Caveats and open-bug flags
- **Cowork enforcement is largely undocumented and inferred from open GitHub issues**, not official docs. Behavior is version-dependent and changing fast (CC ~v2.1.16x). Treat the Cowork column as "broken until proven working in your build."
- **Open bugs to track:** #40495 / #27398 (Cowork hooks), #47993 (Cowork SessionStart), #57209 (Desktop WorktreeCreate hook), #23424 (Cowork local MCP), #50669 / #26998 / #31542 / #26131 (Cowork skill scanning/mounting), #13343 (30-skill limit), #17283 / #49559 (`context: fork`/`agent:` ignored via Skill tool), #26251 (`disable-model-invocation` refuses slash invoke), Prettier multi-line YAML description breakage.
- **Description char-budget conflict:** the official best-practices page states description max **1024 chars**; the Help Center states **200**. In Claude Code specifically, the combined description+`when_to_use` is truncated at ~1536 chars in the skill listing. Verify against your target surface; keep descriptions tight regardless, and beware the `SLASH_COMMAND_TOOL_CHAR_BUDGET` (~16K total) truncation that hides skills.
- **`context: fork`/`agent:` cannot be relied on** when a skill is invoked via the Skill tool — emit an explicit Task-tool instruction instead.
- **Seleznov's directive-description finding is community research** (rigorous: 650 trials, N=3/cell, Fisher's exact test, logistic regression, Cochran-Mantel-Haenszel stratified analysis) but not Anthropic-official; SkillsBench (+16.2pp avg, arXiv:2602.12670, 84 tasks/11 domains/7 configs/7,308 trajectories) is benchmark data. Both align with Anthropic's own "pushy description" guidance, so the convergence is strong, but execution-level (step-following) reliability has not been controlled-tested at the same rigor.
- **The `when_to_use` frontmatter field appears in the codebase but is undocumented** — rely on a detailed `description` instead until it's officially supported.
- Scheduled tasks and Cowork sessions only run while the computer is awake and the Desktop app is open — no cloud execution.