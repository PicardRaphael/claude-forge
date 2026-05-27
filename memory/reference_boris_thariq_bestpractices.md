---
name: boris-thariq-bestpractices
description: Reference EXHAUSTIVE des best practices CC — Boris Cherny (72 tips + 6 tips 4.7), Thariq Shihipar (9 categories skills), Anthropic officiel (docs agents/skills/hooks). TOUT est ici, ne JAMAIS re-chercher.
type: reference
originSessionId: 7344c917-42fa-4a63-8a92-bc680e8d28e4
---
## Sources (consolide 17 avril 2026)

- howborisusesclaudecode.com (72 tips, jan-avr 2026)
- Boris thread 16 avr 2026 : 6 tips Opus 4.7 (threads.com/@boris_cherny)
- Thariq Shihipar LinkedIn "Lessons from Building Claude Code: How We Use Skills" (17 mars 2026)
- code.claude.com/docs/en/best-practices (officiel CC)
- platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices (officiel skills)
- claudefa.st/blog/guide/development/opus-4-7-best-practices (guide communautaire 4.7)

---

## 1. CLAUDE.md

- Boris : ~100 lignes (~2.5k tokens). L'equipe Anthropic documente erreurs, best practices, style, design guidelines, PR templates
- "Anytime we see Claude do something incorrectly we add it to the CLAUDE.md"
- "After correcting Claude, explicitly ask it to update CLAUDE.md"
- Anthropic : "For each instruction, ask: Would removing this cause Claude to make mistakes? Yes: Keep / No: Remove"
- **Inclure** : commandes non devinables, style different des defaults, tests, conventions repo, archi, gotchas, path aliases
- **Exclure** : ce que Claude sait deja, docs detaillees (link instead), info qui change souvent, descriptions file-by-file
- Emphasis OK ("IMPORTANT", "YOU MUST") pour ameliorer adherence
- Si trop long → instructions ignorees. "Bloated CLAUDE.md causes Claude to ignore your actual instructions"
- Gotchas section = **highest-signal content** (Thariq)
- `@path/to/import` syntax pour importer d'autres fichiers depuis CLAUDE.md
- Locations : `~/.claude/CLAUDE.md` (global), `./CLAUDE.md` (projet), `./CLAUDE.local.md` (perso), parent/child dirs

---

## 2. Agents

### Configuration frontmatter
- `permissionMode: plan` (read-only) ou `acceptEdits` (write)
- `disallowedTools: Write, Edit` sur agents read-only (double protection)
- `effort: high` sur TOUS les sonnet. JAMAIS medium (Boris: "high for everything")
- `memory: project` sur TOUS les agents — accumulation cross-sessions
- `color` : optionnel, aide visuelle dans le task panel
- `model: opus` pour raisonnement profond, `model: sonnet` pour execution

### Patterns de delegation
- Chaque agent = contexte isole → empeche contamination d'approches echouees
- **Writer/Reviewer pattern** : un Claude ecrit, un autre review (contexte frais = pas de biais)
- "Use subagents for investigation" — subagents explorent, rapportent summary, contexte principal reste propre
- Verification subagent apres implementation (Boris: `verify-app`)

### Opus 4.7 — Subagent management
- 4.7 spawn MOINS de subagents par defaut
- "Do not spawn a subagent for work you can complete directly in a single response"
- Fan-out parallele = **explicite** : "Spawn a specialist for each of: X, Y, Z"
- Positive framing > negative : "Add tests to criteria" > "Don't skip tests"
- **Mandatory plan reading** : chaque sub-agent doit lire le plan COMPLET comme premiere action
- Plan-driven architecture : "the plan IS the prompt" — intent + contraintes + criteres acceptance + fichiers + verification

### Effort levels (Opus 4.7)
| Phase | Effort | Rationale |
|-------|--------|-----------|
| Session principale (planning) | xhigh (defaut 4.7) | Quality compounds into execution |
| Subagents (execution) | high | Specialists working from clear plans |
| Verification | xhigh (si opus) ou high (si sonnet = max) | Catch drift before it ships |
| Exploratory/docs | medium | Cost-sensitive, low stakes |
| Deep evals | max | Correctness-critical (diminishing returns) |

---

## 3. Skills (Thariq — 9 categories)

1. **Library & API Reference** — gotchas libs, SDK usage
2. **Product Verification** — tester/verifier output correctness
3. **Data Fetching & Analysis** — monitoring, data stacks
4. **Business Process Automation** — workflows repetitifs en commandes
5. **Code Scaffolding & Templates** — boilerplate generation
6. **Code Quality & Review** — standards org, adversarial review
7. **CI/CD & Deployment** — deploy workflows, babysit PR
8. **Runbooks** — symptom → investigation → rapport structure
9. **Infrastructure Operations** — maintenance avec guardrails destructifs

### Regles d'ecriture (Thariq + Anthropic)
- **SKILL.md < 500 lignes** — deporter dans references/
- **Description = TRIGGER, pas resume** — "quand cette skill doit s'activer ?"
- **Troisieme personne** pour descriptions skills (pas "I can..." ni "You can..."). Note: agents utilisent "Use when..." = OK
- **Gotchas section = highest-signal content** — peupler depuis les vrais echecs, updater continuellement
- **Don't state the obvious** — Claude sait deja beaucoup. Focus sur ce qu'il ne sait PAS
- **Progressive disclosure** — SKILL.md = table of contents, refs chargees a la demande. Token cost = 0 tant que pas lu
- **References max 1 niveau de profondeur** — SKILL.md → ref. Pas SKILL.md → ref → sous-ref
- **Fichiers longs (>100 lignes) : table des matieres en haut** pour que Claude voie le scope meme en preview
- **Avoid railroading** — goal + constraints, pas step-by-step rigide (sauf operations fragiles : DB migrations)
- **Scripts > generation de code** pour operations deterministes — plus fiable, save tokens
- **Config user dans config.json** dans le dossier skill. Si absent, Claude demande via AskUserQuestion
- **Tester avec tous les modeles** (haiku, sonnet, opus) — ce qui marche sur opus peut manquer de detail pour haiku
- **Naming : gerund form** prefere (processing-pdfs, testing-code) ou action-oriented (process-pdfs)
- **Avoid vague names** : helper, utils, tools = mauvais
- **Feedback loops** : run validator → fix errors → repeat. Pattern : plan-validate-execute
- **Checklist pattern** pour workflows complexes : Claude copie et coche au fur et a mesure

### Distribution
- Check dans `.claude/skills/` pour petites equipes
- **Plugin marketplace interne** pour scale — chaque skill ajoutee = context cost
- Flow : sandbox GitHub → share Slack → traction organique → PR marketplace

---

## 4. Rules (.claude/rules/)

- Fichiers markdown dans `.claude/rules/`
- Charges automatiquement quand CLAUDE.md dit "Consulter .claude/rules/"
- Frontmatter optionnel avec `globs` pour auto-attach a certains fichiers
- Rules = advisory (comme CLAUDE.md). Pour deterministe → utiliser hooks
- Cas d'usage : delegation routing, CTO mindset, database rules, testing rules, changelog

---

## 5. Hooks

- Boris : "actions that must happen every time with zero exceptions"
- **CLAUDE.md = advisory, Hooks = deterministic** — difference fondamentale
- Types de hooks :
  | Hook | Use case |
  |------|----------|
  | SessionStart | Charger contexte dynamiquement |
  | PreToolUse | Logger, bloquer (guardrails) |
  | PostToolUse | Format/lint apres Write/Edit, notifications apres push |
  | PermissionRequest | Router vers WhatsApp/Opus pour approval |
  | Stop | Nudge Claude to keep going |
  | PostCompact | Re-injecter instructions critiques apres compression |
  | WorktreeCreate | Support VCS non-git (Mercurial, Perforce) |
- **On-demand hooks via skills** : `/careful` bloque rm -rf, DROP TABLE, force-push. Active uniquement pour la session
- Meme langage que le projet (Thariq: hooks = scripts dans le stack du repo)

---

## 6. Memory

- `memory: project` sur tous les agents → MEMORY.md auto-loaded
- `~/.claude/CLAUDE.md` = memoire globale (tous projets)
- `./CLAUDE.md` = memoire projet
- Thariq : skills stockent etat persistant dans `${CLAUDE_PLUGIN_DATA}`
- learn-from-mistakes rule = "Every mistake becomes a rule" (Boris Cherny)
- Auto Memory native CC : feedback, project, user, reference types
- Format feedback : regle + **Why:** + **How to apply:**

---

## 7. Plan Mode & Workflow (Boris)

- "Never let Claude write a single line of code until the plan is approved"
- 4 phases : Explore → Plan → Implement → Commit
- Plan mode = Shift+Tab (cycle Ask → Plan → Auto)
- "Have another Claude review the plan as a staff engineer"
- Skip plan pour trivial (typo, log line, rename). Plan pour : scope incertain, multi-fichiers, code inconnu
- Ctrl+G : ouvrir le plan dans l'editeur pour l'editer avant implementation

### Boris Opus 4.7 workflow
- 5 terminaux + 5-10 sessions cloud en parallele, chacun dans son worktree git
- Effort xhigh pour la plupart, max pour les plus durs
- `/go` skill : self-test end-to-end → `/simplify` → ouvrir PR
- `/recap` pour retrouver le contexte apres pause
- `/fewer-permission-prompts` pour nettoyer les permissions
- Auto mode pour taches longues non-interactives
- "Take time to adjust workflow — nice improvement with old patterns, significant leap once adjusted"

---

## 8. Opus 4.7 — Comportement specifique

### 9 changements comportement
1. **Instruction-following litteral** — fait exactement ce qu'on dit, ni plus ni moins
2. **Moins de subagents spontanes** — fan-out doit etre explicite
3. **Moins de tool calls inutiles** — plus efficient
4. **Longueur de reponse calibree** — ni trop court ni trop long
5. **Ton direct** — moins de hedging ("I think...", "Perhaps...")
6. **Adaptive thinking** — pas de budget_tokens, calibre depuis effort level
7. **xhigh par defaut** — nouveau level entre high et max
8. **Auto mode** — classifier model approuve/bloque les commandes
9. **Task budgets** (beta) — token target pour boucle agentique complete

### Prompts 4.7 — Migration depuis 4.6
- **Explicit over implicit** — si 4.6 inferait "ajouter des tests", l'ecrire dans les criteres
- **Batch questions** — 3 questions en 1 tour > 3 tours (overhead par tour)
- **Front-load file paths** — passer les chemins exacts save des tool calls
- **State parallelism explicitly** — defaut = reponse unique
- **Assumption surfacing** — "state key assumptions before implementing"
- **Positive framing > negative** — "Add tests" > "Don't skip tests"
- Ne JAMAIS dire "don't nitpick" dans un review → 4.7 obelit litteralement, masque des bugs

### Token awareness
- Meme input = **1.0 a 1.35x plus de tokens** que 4.6 (nouveau tokenizer)
- xhigh + deeper reasoning = sessions plus couteuses
- Controles : task budgets, conciseness prompting, effort levels

---

## 9. Patterns avances

### Verification (Boris tip #1 — "2-3x more capable needs 2-3x more verification")
- Backend → run server, test end-to-end
- Frontend → Claude Chromium extension (browser control)
- Desktop → Computer Use
- Skill `/go` : chains test → simplify → PR automatiquement

### Context management
- `/clear` entre taches non liees
- `/compact <instructions>` pour compaction dirigee
- `/btw` pour questions rapides sans polluer le contexte
- `Esc + Esc` ou `/rewind` pour revenir a un checkpoint
- `CLAUDE_CODE_AUTO_COMPACT_WINDOW=400000` : force compaction a 400k (degradation commence 300-400k)

### Parallel sessions
- Worktrees git : "single biggest productivity unlock" (Boris)
- Desktop app : sessions isolees avec worktrees natifs
- Agent Teams : coordination automatisee multi-sessions
- Fan-out : `claude -p "task" --allowedTools "Edit,Bash(git commit *)"` dans une boucle

### MCP servers recommandes (Boris)
- Playwright : browser testing + UI verification
- PostgreSQL/MySQL : schema queries directes
- Slack : bug reports, thread context
- Figma : design-to-code workflows

---

## 10. Anti-patterns a eviter

- **Kitchen sink session** — taches non liees dans le meme contexte → `/clear`
- **Correcting over and over** — apres 2 corrections echouees → `/clear` + meilleur prompt
- **Over-specified CLAUDE.md** — trop long = instructions ignorees → pruner
- **Trust-then-verify gap** — pas de verification = bugs caches → toujours tests/screenshots
- **Infinite exploration** — "investigate" sans scope → utiliser subagents
- **Vague multi-turn prompts** — 4.7 anti-pattern → tout dans le premier tour
- **Negative framing sur 4.7** — "don't skip X" = moins efficace que "always do X"

---

## Audit Neoteem (17 avril 2026)

Repos ia_back + neo_ia confirmes alignes sur TOUS les points :
- CLAUDE.md concis + gotchas ✓
- Architect-first = plan-driven ✓
- memory: project tous agents ✓
- learn-from-mistakes rule ✓
- Hooks deterministes ✓
- Verification gates (test-writer → code-reviewer → validator) ✓
- disallowedTools + permissionMode ✓
- effort: high subagents, xhigh session ✓
- Skills < 500L avec progressive disclosure ✓
- Descriptions = triggers ✓
- Writer/Reviewer = architect → dev → code-reviewer ✓
- Explicit parallelism dans rules ✓
- Positive framing dominant ✓
- Literal instructions (tables, workflows, gates) ✓
- Seul bonus non implemente : skill `/go` (test → simplify → PR)

---

## Adaptation Neoteem mai 2026 — pattern Boris adapté

**Contexte** : 21-22 mai 2026, frustration utilisateur 4h/feature. Tentative initiale "copier Boris à 100%" → DA a démontré que ça ne marche pas (Boris solo + expert, Neoteem équipe + juniors). Pivot vers adaptation.

### Différences clés Boris pur vs adapté Neoteem

| Élément | Boris pur (solo + expert) | Adapté Neoteem (équipe) |
|---------|---------------------------|-------------------------|
| Architect | Plan Mode natif CC (interactif) | Agent architect + marker (filet collègues) |
| Effort agents | high par défaut, xhigh ad hoc | xhigh RÉSERVÉ : architect + dev-lead + refactor-pg-function. Tout le reste = high |
| TDD | Red-green minimal "five tokens" | TDD obligatoire + bypass typo/config/doc via `.tdd-bypass` |
| Pipeline | Linéaire libre | Conditionnel selon scope (gates obligatoires sur critères) |
| Parallélisation | Worktrees N sessions | Séquentiel pour cohérence équipe |
| Plan Mode | OUI (Boris pattern) | NON (pas de trace persistante vérifiable hook) |

### Seuils concrets à appliquer sur tout nouveau repo

- Architect routing taille S/M/L en tête du prompt
- Mode mini-plan S : 5 lignes en < 60s
- Architect NE LIT PAS repos voisins par défaut
- Test-writer MAX 3 tests par comportement
- Phase REFACTOR test-writer SUPPRIMÉE (fusionnée code-reviewer light)
- Effort `high` partout sauf jugement profond
- Skills agents : 3-4 core max (pas 9)
- Gates conditionnels : security/perf/validator/outcomes-grader SI critères

**Référence canonique** : [[pipeline-boris-adapte-neoteem]] (vault forge-brain)
**Raisonnement complet** : [[raisonnement-revirement-pipeline-mai-2026]]
**Erreur évitée** : [[erreur-pipeline-trop-long-frustration]]

### Citation Willison qui a débloqué la doctrine

Simon Willison, Pragmatic Engineer Summit mars 2026 : *"use red-green TDD, it's like five tokens, and that works"*. Pas d'angoisse couverture exhaustive. Tests discriminants, pas tests exhaustifs.

### Gains mesurés (sessions 21-22 mai)

- Feature M neo_ia : 30-45 min → 12-18 min (~50%)
- Feature CRUD ia_back : 4 h → ~1 h 30 (~60%)
- Feature S triviale (typo/rename) : 15-20 min → 3-5 min (~75%)
