---
aliases:
  - refonte 26 mai 2026
  - synthese refonte 3 repos
  - audit tripartite Will ECC Boris application
  - migrations Haiku fusions agents
  - session 26 mai 3 repos
resume: "Synthèse refonte 26 mai 2026 — application du verdict audit tripartite Will×ECC×Boris sur forge + ia_back + neo_ia. 15 actions appliquées + 12 skills forge + 3 auditors user-scope. Référence anti-drift future."
derniere-maj: 2026-05-26
tags:
  - "#type/synthese"
  - "#domaine/claude-code"
  - "#statut/canonique"
---

# Refonte 26 mai 2026 — 3 repos forge × ia_back × neo_ia

## Contexte déclencheur

Session de refonte massive suite à :
1. Analyse vidéo Will (Anthropic Applied AI, talk CwC London) — doctrine agent client minimum
2. Analyse article @sairahul1 — pattern Software Factory 7-agents
3. Découverte ECC Affaan Mustafa (hackathon winner Anthropic, 154K stars) — pattern setup dev personnel
4. Confirmation NBER 34836 + Google/MIT arXiv 2512.08296 — chiffres durs scaling agent systems
5. Audit tripartite Agent Teams `forge-audit-doctrines` (3 teammates will/ecc/boris-auditor)
6. Validation Raphael "fais tout, j'en ai marre des demi-mesures"

## Doctrine appliquée

Voir notes canoniques :
- [[will-vs-ecc-deux-doctrines-anthropic]] — résolution paradoxe minimum vs maximum agents
- [[effort-opus-47-doctrine-anthropic-2026]] — calibration effort par TYPE de tâche
- [[google-mit-scaling-agent-systems-2025]] — threshold 45% + sequential -39/-70% + parallel +81%
- [[ecc-pattern-personal-dev-setup]] — pattern dev perso
- [[software-factory-pattern-2026]] — pattern 7-agents communauté
- [[agent-teams-natif-anthropic]] — orchestrateur officiel
- [[context-drift-throw-vs-patch]] — règle Sairahul throw vs patch

## Actions appliquées — par repo

### Forge (claude-forge)

**Avant** : 13 agents / 35 skills / 9 hooks
**Après** : 11 agents / 47 skills / 9 hooks

| Action | Path | Statut |
|---|---|---|
| CLAUDE.md v3.3 (permissions cross-repo totales + workflow langage naturel + doctrine effort calibrée) | `CLAUDE.md` | ✅ |
| Fix project-auditor tools (retirer Write/Edit, ajouter disallowedTools) | `.claude/agents/project-auditor.md` | ✅ (puis supprimé par fusion) |
| Fusion 3 agents read-only → `repo-inspector` (modes audit/analyze/scan) | `.claude/agents/repo-inspector.md` | ✅ |
| Suppression `project-analyzer.md`, `project-auditor.md`, `codebase-scanner.md` | `.claude/agents/` | ✅ |
| 12 skills nouvelles (capitalisation MEMORY → skills exécutables) | `.claude/skills/*/SKILL.md` | 🔄 en cours |

**Skills nouvelles forge (12)** :
- git-multi-repo (validé feedback_git_C_pas_cd)
- python-script-refactor-masse (validé 308L économisées)
- auditor-empirical-verify (post-dispatch grep/diff)
- windows-hooks-cross-machine (py launcher + path absolu)
- da-blocking-arbitrage (DA verdict protocol)
- arxiv-verification (URL swap + YYMM + venues)
- methode-pivoter-doctrine (skill exécutable de la note canonique)
- audit-thematique-clusters (sub-agents par cluster)
- mcp-brief-then-direct (pattern MCP brief)
- cross-repo-propagation (décisions naming cross-repo)
- web-search-canonical-source (single source provider)
- agentshield-like-scanner (signature ECC, pipeline red/blue/auditor)

### ia_back

**Avant** : 16 agents / 30 skills / 14 hooks
**Après** : 13 agents / 32 skills / 14 hooks

| Action | Path | Statut |
|---|---|---|
| `codebase-analyst` sonnet → Haiku (économie ~5x) | `.claude/agents/codebase-analyst.md:6` | ✅ |
| `repo-functions-analyzer` sonnet → Haiku | `.claude/agents/repo-functions-analyzer.md:10` | ✅ |
| Fusion `validator` + `code-reviewer` → `reviewer.md` | `.claude/agents/reviewer.md` | ✅ |
| Suppression `validator.md` + `code-reviewer.md` | `.claude/agents/` | ✅ |
| Conversion `architect-quick` → skill `architect-sanity-check` | `.claude/skills/architect-sanity-check/SKILL.md` | ✅ |
| Suppression `architect-quick.md` | `.claude/agents/` | ✅ |
| Copie skill `/done` adaptée (vault double forge-brain + neoteem-brain, Bun/Hono/postgres.js) | `.claude/skills/done/SKILL.md` | ✅ |
| Section `## Gotchas` compounding ajoutée | `CLAUDE.md` (fin) | ✅ |

### neo_ia

**Avant** : 14 agents / 30 skills / 13 hooks
**Après** : 12 agents / 33 skills / 13 hooks

| Action | Path | Statut |
|---|---|---|
| `codebase-analyst` opus → Haiku (anomalie corrigée) | `.claude/agents/codebase-analyst.md:6` | ✅ |
| Fusion `code-reviewer` + `security-reviewer` → `reviewer.md` | `.claude/agents/reviewer.md` | ✅ |
| Suppression `code-reviewer.md` + `security-reviewer.md` | `.claude/agents/` | ✅ |
| Conversion `architect-quick` → skill `architect-sanity-check` | `.claude/skills/architect-sanity-check/SKILL.md` | ✅ |
| Conversion `build-error-resolver` → skill `/build-fix` | `.claude/skills/build-fix/SKILL.md` | ✅ |
| Suppression `architect-quick.md` + `build-error-resolver.md` | `.claude/agents/` | ✅ |
| Copie skill `/done` adaptée (Python NeoChat/NeoDoc/NeoMail + monorepo) | `.claude/skills/done/SKILL.md` | ✅ |
| Section `## Gotchas` compounding ajoutée (avec note HybridToolSelector OATS) | `CLAUDE.md` (fin) | ✅ |
| Fix typo path `neot-2` → `neot-v2` | `.claude/settings.json:240` | ✅ |
| Contradiction parallélisme tranchée (verbatim Google/MIT) | `.claude/rules/agent-limits.md:67` | ✅ |
| Fix drift doc Lazy Expansion + OATS état prod | `.claude/skills/neoia-tools/SKILL.md` | ✅ |

### User scope (`~/.claude/agents/`)

**Capitalisation 3 auditors tripartites cross-repo** :
- `will-auditor.md` — doctrine Anthropic Applied AI (agent client minimum) ✅
- `ecc-auditor.md` — doctrine ECC hackathon winner (setup dev personnel) ✅
- `boris-auditor.md` — doctrine Boris Cherny (compounding pragmatique) ✅

Réutilisables sur tout audit futur forge / ia_back / neo_ia / autre repo. Activation : *"Crée une agent team avec will-auditor, ecc-auditor, boris-auditor pour auditer X"*.

## Actions sécu manuelles Raphael

| Action | Path | Statut |
|---|---|---|
| Rotation token Google Chat ia_back | `ia_back/.claude/settings.json:5` | ⏳ TODO Raphael |
| Remplacer `Edit(./**)` par scopes explicites | `ia_back/.claude/settings.json:19-22` | ⏳ TODO Raphael |
| Suppression manuelle `build-error-resolver.md` neo_ia | déjà fait | ✅ |

## Workflow agentique final

### Feature → langage naturel
> "J'ai besoin d'un endpoint qui retourne X"

→ session principale orchestre : `/spec` → architect-deep (Opus xhigh) → dev (Sonnet high) → reviewer (Opus high fusionné) → outcomes-grader → toi commit

### Bug → langage naturel
> "Il y a un bug sur Y"

→ debugger → dev → test-writer → reviewer → toi commit

### Audit repo → langage naturel
> "Audite mon repo"

→ `repo-inspector` (forge) en mode audit
OU
> "Audite avec lentilles Will/ECC/Boris"

→ Agent Team `forge-audit-doctrines` recréée avec les 3 user-scope auditors

## Doctrine effort calibrée portefeuille

| Niveau | Agents concernés |
|---|---|
| Opus xhigh | architect-deep, dev-lead (neo_ia L), refactor-pg-function, repo-inspector (forge), project-analyzer (déprécié, fusionné) |
| Opus high | devils-advocate, outcomes-grader, reviewer (fusionné), api-designer, responsable-ia, will/ecc/boris-auditor |
| Sonnet high | agent-creator, skill-creator, hook-creator, claudemd-optimizer, dev, dev-app, python-dev, test-writer |
| Sonnet medium | vault-maintainer, self-updater |
| Haiku high | codebase-analyst (ia_back + neo_ia), repo-functions-analyzer (ia_back) |

## Chiffres finaux

| Repo | Agents avant | Agents après | Économie tokens estimée |
|---|---|---|---|
| forge | 13 | 11 | ~5x sur scans (repo-inspector mode scan = Read/Glob/Grep, possible Haiku candidate) |
| ia_back | 16 | 13 | Migration Haiku × 2 → ~50-100k tokens/jour récupérés |
| neo_ia | 14 | 12 | Migration Haiku × 1 + fusion reviewer |

## Anti-drift — Si quelqu'un challenge ces choix dans 3 mois

1. Lire cette note + [[will-vs-ecc-deux-doctrines-anthropic]] + [[effort-opus-47-doctrine-anthropic-2026]]
2. Re-lancer audit tripartite via `~/.claude/agents/will-auditor.md` + `ecc-auditor.md` + `boris-auditor.md` en Agent Team
3. Si verdict diverge avec ce snapshot → appliquer [[methode-pivoter-doctrine]]
4. Mettre à jour cette note `derniere-maj` + section "Drift détecté" en bas

## Liens

- [[will-vs-ecc-deux-doctrines-anthropic]]
- [[effort-opus-47-doctrine-anthropic-2026]]
- [[google-mit-scaling-agent-systems-2025]]
- [[ecc-pattern-personal-dev-setup]]
- [[affaan-mustafa-ecc-hackathon-winner]]
- [[agent-teams-natif-anthropic]]
- [[software-factory-pattern-2026]]
- [[methode-pivoter-doctrine]]
- [[audit-tripartite-doctrinal-pattern]] (feedback memory)
