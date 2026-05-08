---
titre: "Neoteem = Agentic Engineering — Mapping Karpathy"
resume: "Validation externe du workflow Neoteem par le framework Karpathy (Sequoia AI Ascent 2026). Mapping complet neo_ia + ia_back + forge vs concepts Software 3.0."
aliases:
  - "karpathy neoteem"
  - "agentic engineering neoteem"
  - "software 3.0 neoteem"
type: synthese
derniere-maj: 2026-05-06
auteur: claude
sources:
  - "[[agentic-engineering-karpathy]]"
  - "[[vibe-coding-setup-complet]]"
  - "Session claude-forge 2026-05-06"
tags:
  - "#type/synthese"
  - "#domaine/neoteem"
  - "#domaine/claude-code"
---

# Neoteem = Agentic Engineering

Le framework "From Vibe Coding to Agentic Engineering" de Karpathy (Sequoia AI Ascent, mai 2026) valide externement l'architecture que Neoteem a deployee sur neo_ia et ia_back.

## Mapping complet

### 1. Plan-driven execution

| Karpathy | neo_ia | ia_back | forge |
|----------|--------|---------|-------|
| "Plan Mode → iterate → auto-accept → one-shot" | `architect-first` rule obligatoire | CTO rule orchestre | Plan Mode avant toute implem |
| Specs avant execution | architect agent (opus high) | architect agent (opus high) | check-before-create rule |
| Deleguer macro-actions | 9 agents specialises | 11 agents specialises | Agents par responsabilite |

### 2. Agents paralleles isoles

| Karpathy | neo_ia | ia_back | forge |
|----------|--------|---------|-------|
| Worktrees git isoles | Agents en worktrees | Agents en worktrees | `/batch`, background agents |
| Multi-sessions paralleles | Routing rules/ dispatch | Routing rules/ dispatch | Session principale orchestre |
| Isolation = securite | `permissionMode: acceptEdits` | `permissionMode: acceptEdits` | `disallowedTools` sur read-only |

### 3. Humain = operateur, pas typist

| Karpathy | Neoteem |
|----------|---------|
| "You can outsource your thinking, but you can't outsource your understanding" | Raphael review systématique, franc-parler |
| Agentic engineer = supervise, ne code pas | Session principale orchestre, PAS d'agent CTO orchestrateur |
| Taste reste humain | feedback `no-cto-agent` — decision validee en production |
| System design judgment | architect-first meme pour taille S |

### 4. Verification des outputs

| Karpathy | neo_ia | ia_back | forge |
|----------|--------|---------|-------|
| "Give Claude a way to verify its output" = tip #1 | test-writer systematique | test-writer systematique | Gate dans pipeline obligatoire |
| Boucle eval | code-reviewer apres chaque implem | code-reviewer apres chaque implem | Pipeline architect → dev → test → review |
| Verifiabilite = levier principal | Tests + review + lint | Tests + review + lint | **Manque : evals formalisees** |

### 5. LLM Knowledge Bases

| Karpathy | Neoteem |
|----------|---------|
| Wikis compiles par agents | neo-brain vault (682+ notes) |
| Sources brutes → syntheses, pages concepts, cross-links | Templates atomiques, MOCs, aliases-as-semantic-search |
| Contradictions documentees | Knowledge/erreurs/ dans forge-brain |
| Connaissance persistante cross-sessions | Auto Memory + forge-brain + shared-learnings rule |

### 6. Context = Programme (Software 3.0)

| Karpathy | Neoteem |
|----------|---------|
| Context window = programme | CLAUDE.md ~100L max (Boris: "si je l'enleve, Claude fait des erreurs? Non → couper") |
| Progressive disclosure | Skills SKILL.md < 500L + references/ |
| Prompts = code | Skills metier NeoChat/NeoDoc/NeoMail = prompt programming |
| Agent-native interfaces | MCP servers, APIs, CLIs, schemas structures |

### 7. Jagged Intelligence → Guardrails

| Karpathy | Neoteem |
|----------|---------|
| Modeles inegaux, pas de manuel | Effort `high` minimum partout (jamais medium sur sonnet) |
| Empirical familiarity | 100% opus — teste et valide meilleur que sonnet |
| Guardrails selon domaine | Gates qualite, security-auditor sur endpoints critiques |

## Ce que Neoteem fait que Karpathy ne mentionne pas

### Memory Compounding
Boucle d'apprentissage persistante :
- Auto Memory locale (feedback par session)
- forge-brain vault (knowledge partageable)
- `Knowledge/erreurs/` (erreurs documentees = ne pas refaire)
- shared-learnings rule (apprentissages → skills commitees)
- Discipline memoire (relire avant agir)

C'est notre equivalent du "RL reward signal" de Karpathy — la boucle de verification est humaine et persistante. Les labs utilisent le RL automatise ; nous utilisons le feedback humain capitalise.

### Cross-project patterns
Un pattern valide sur neo_ia est deploye sur ia_back (et inversement) via forge. Les labs ne partagent pas explicitement cette mecanique de propagation entre repos.

## Ce qui manque (gap a combler)

### Evals formalisees
Karpathy : "la verifiabilite est LE levier". On a les gates (test-writer, code-reviewer) mais pas de suite d'evals automatisees qui mesurent la qualite des outputs agents sur la duree.

**Plan propose :**
1. Eval set par agent : inputs connus → outputs attendus → scoring
2. Metriques tracees : taux de correction post-review, temps de cycle, regressions
3. Dashboard Langfuse : suivi qualitatif par semaine
4. Feedback loop : evals qui echouent → enrichissent le prompt agent

### Agent-native infrastructure complete
Karpathy insiste sur le headless setup. Nos repos sont bons (CLI, MCP, APIs) mais certains workflows restent humain-natifs (Jira manual, Google Drive navigation).

## Liens

- [[agentic-engineering-karpathy]] — framework complet
- [[vibe-coding-setup-complet]] — pattern setup
- [[Boris Cherny]] — workflow fleet commander
- [[Opus 4.7]] — effort levels
