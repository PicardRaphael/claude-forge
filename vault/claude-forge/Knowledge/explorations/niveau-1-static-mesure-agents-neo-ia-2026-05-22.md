---
titre: "Mesure statique Niveau 1 agents neo_ia 2026-05-22"
resume: "Mesure statique des 14 agents neo_ia contre seuils canoniques (lines, mots, tools, skills, sections H2). Capacite vs usage : Niveau 1 = carte, pas verdict. 4 agents flaggés (architect-deep + 3 dev-app) candidats audit Niveau 2 transcripts JSONL avant refactor."
aliases:
  - "niveau 1 mesure agents neo_ia"
  - "mesure statique agents neo ia"
  - "audit agents neo_ia 2026-05-22"
  - "carte surcharge agents"
  - "candidats refactor agents neo_ia"
  - "dette technique agents"
derniere-maj: 2026-05-22
auteur: claude
type: knowledge
domaine: claude-code
sources:
  - "Methode Niveau 1/2/3 partagee par Raphael session 22 mai"
  - "[[comment-creer-agent]] — sonnet/opus split, harness > model"
  - "[[methode-analyser-repo]] — A->B->C->D->E"
  - "Cat Wu — Code with Claude London 19 mai 2026 — '6-8 ops/agent max'"
  - "Verdict advisor() forge 2026-05-22 — Niveau 1 = carte pas verdict"
tags:
  - "#type/exploration"
  - "#domaine/claude-code"
  - "#projet/neo_ia"
  - "#domaine/agents"
  - "#meta"
---

# Mesure statique Niveau 1 agents neo_ia 2026-05-22

> Note exploration — mesure statique des 14 agents neo_ia contre seuils canoniques. Capacite (frontmatter) != usage (transcripts).

## Methode

3 niveaux de mesure agent (canonique Raphael 22 mai) :

| Niveau | Source | Effort | Verdict |
|--------|--------|--------|---------|
| **1 — Statique** | `wc`, `grep` sur `.md` | Immediat | **Carte/indication** |
| **2 — Empirique** | Transcripts JSONL `~/.claude/projects/<repo>/subagents/<id>.jsonl` | 5 min/agent | **Verdict usage reel** |
| **3 — Agregee** | Hook PostSubagentStop + CSV | Lourd | **Tendances mensuelles** |

Seuils Niveau 1 (indicatifs) :
- Lignes > 200 = agent qui en fait probablement trop
- Tools > 8 = scope large
- Skills > 6 = lourdeur cognitive
- Sections H2 > 8 = workflow trop decoupe
- Mots > 1500 = prompt trop charge

## Resultats neo_ia (14 agents)

| Agent | Lignes | Mots | Tools | Skills | H2 | Seuils dépassés |
|-------|--------|------|-------|--------|-----|-----------------|
| architect-deep | 211 | 1518 | 10 | 8 | 11 | **5/5** (lines, mots, tools, skills, sections) |
| codebase-analyst | 189 | 1030 | 4 | 6 | 10 | 1 (sections) |
| dev-neochat | 158 | 946 | 11 | 8 | 10 | 3 (tools, skills, sections) |
| dev-neodoc | 151 | 880 | 11 | 7 | 9 | 3 (tools, skills, sections) |
| code-reviewer | 135 | 847 | 5 | 4 | 7 | 0 |
| dev-lead | 127 | 791 | 11 | 6 | 9 | 2 (tools, sections) |
| test-writer | 121 | 812 | 8 | 5 | 7 | 0 |
| dev-shared-utils | 108 | 546 | 11 | 6 | 7 | 1 (tools) |
| outcomes-grader | 93 | 599 | 0 | 0 | 5 | 0 |
| dev-neomail | 92 | 604 | 11 | 8 | 8 | 3 (tools, skills, sections) |
| security-reviewer | 87 | 474 | 7 | 3 | 5 | 0 |
| dev-shared-tools | 65 | 370 | 11 | 3 | 5 | 1 (tools) |
| build-error-resolver | 57 | 305 | 0 | 1 | 3 | 0 |
| architect-quick | 57 | 353 | 3 | 0 | 6 | 0 |

## Patterns systemiques observes

### Pattern 1 — tools=11 partage sur 7 agents

`Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__docs-langchain__search_docs_by_lang_chain` = bloc copie sur dev-neochat, dev-neodoc, dev-neomail, dev-shared-tools, dev-shared-utils, dev-lead, architect-deep.

Signal : "tool set par defaut copie" pas "decision par agent".

### Pattern 2 — architect-deep = 5/5 seuils

Seul agent depassant simultanement les 5 seuils Niveau 1. Accumule roles : analyse + plan + risk + alternatives + DA + check coverage.

### Pattern 3 — Trio dev-app duplique

`dev-neochat` / `dev-neodoc` / `dev-neomail` partagent : 11 tools, 7-8 skills, 8-10 sections H2. Pattern symetrique (logique car 3 apps similaires) mais opportunity de skill partagee `neo-ia-dev-app-base` extraite.

## Limite cruciale — capacite vs usage

**Niveau 1 mesure ce que l'agent PEUT faire (frontmatter declarative)**, pas ce qu'il FAIT (transcripts reels).

Verdict advisor 2026-05-22 (verbatim) :
> "Niveau 1 = indication, pas verdict. Cat Wu '6-8 ops/agent' = ops dans transcript reel, PAS tools listes dans frontmatter. Tu conflates capacite avec usage."

Retirer un tool sans savoir si l'agent l'utilise 1/10 invocations → 10% des invocations cassent silencieusement.

## Reconciliation avec canonique

[[comment-creer-agent]] ne fixe PAS de hard limit sur tools=N ou lines=N. Le seul seuil concret = "max 6-8 ops/agent" (Cat Wu) = ops transcript. Le `> 200L` du tableau Niveau 1 est emprunte a [[comment-ecrire-claudemd]] ou c'est explicitement "target, pas hard".

Donc : Niveau 1 = **signal**, pas **diagnostic**.

## Action recommandee

Plan d'instrumentation (pas refactor a l'aveugle) :

### Court terme — Niveau 2 ciblé (~20 min)

Lire transcripts JSONL des **4 agents flaggés Niveau 1** (architect-deep, dev-neochat, dev-neodoc, dev-neomail) pour 2-3 invocations recentes. Compter ops reelles. Si > 6-8 ops typique → candidat split confirme. Si < 6 ops → false positive Niveau 1.

### Moyen terme — Niveau 3 instrumentation

Hook `PostSubagentStop` qui logge `.claude/agent-metrics.csv` avec :
- agent name
- duration_ms
- tokens utilises
- nb tool_calls
- success/fail

Analyse mensuelle des tendances. Pattern Boris/Anthropic interne pour mesurer +200% PRs Cat Wu.

**Doctrine 22 mai** : ce hook = observabilite (sensor Fowler), pas workflow gate. Autorise.

### Capitalisation

Cette note documente la **carte** (Niveau 1). La transformer en verdict requiert Niveau 2 (usage) puis Niveau 3 (tendances).

## Anti-pattern detecte

**Mon propre** : j'ai voulu promouvoir Niveau 1 en verdict structurel ("Bloc B refactor 7 agents tools=11"). Advisor a coupe court :
> "C'est un fait Niveau 1 transforme en verdict. Bloc B sans Niveau 2 reproduit le pattern F1/F2 (claims non verifies) a plus grande echelle."

Lecon : **mesure statique != verdict**. Toujours croiser avec usage avant refactor.

## Liens

- [[comment-creer-agent]] — canonique source (Sonnet/Opus, harness, ops 6-8 Cat Wu)
- [[methode-analyser-repo]] — methode A->B->C->D->E
- [[workflow-claude-code-optimal]] — harness > model, advisor 5x Angela Jiang
- [[feedback_audit_claims_after_brief]] — verifier empirique AVANT relayage
- [[critique-2026-05-22-doctrine-drift-guard]] — precedent : workaround sans instrumentation = anti-pattern
- [[feedback_drizzle_postgresjs_drift]] — drift code != .claude (similaire structure)

## Sources

- Methode Niveau 1/2/3 partagee par Raphael session forge 22 mai 2026
- [Cat Wu — Code with Claude London 19 mai 2026](https://anthropic.com) — "6-8 ops/agent max" sur transcripts reels
- [Anthropic engineering — Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Justin Young 2-agent architecture
- Verdict advisor() forge 22 mai 2026 — "Niveau 1 = carte pas verdict"


## UPDATE 2026-05-23 — Niveau 2 effectue + decision finale

### Niveau 2 — Transcripts JSONL analysés

n=35 invocations analysees (architect-deep n=1, dev-neochat n=31, dev-neodoc n=2, dev-neomail n=1).

| Agent | Invocations | Ops mean | Ops median (p50) | p75 | p90 | Max | Verdict Cat Wu (>6-8 ops) |
|-------|-------------|----------|------------------|-----|-----|-----|---------------------------|
| architect-deep | 1 | **6** | - | - | - | 6 | OK — sous seuil. Faux positif Niveau 1. |
| dev-neochat | 31 | 42.8 | **27** | 52 | 116 | 198 | Pattern outlier (p90/p10 = 19×). Pas surcharge steady state. |
| dev-neodoc | 2 | 40.5 | - | - | - | 57 | n trop petit pour verdict |
| dev-neomail | 1 | 80 | - | - | - | 80 | n=1, pas un pattern |

### Reconciliation Niveau 1 / Niveau 2

| Agent | Niveau 1 (capacite) | Niveau 2 (usage) | Verdict final |
|-------|---------------------|------------------|---------------|
| architect-deep | 5/5 seuils depasses | 6 ops typique | **Faux positif Niveau 1**. Capacite riche, usage propre. Pas a toucher. |
| dev-neochat | 3 seuils | mediane 27 ops, p90=116 | **Pattern outlier**. Invocations parfois trop larges, pas l'agent. |
| dev-neodoc | 3 seuils | n=2 (donnees pauvres) | **Verdict reporte** — Niveau 3 requis |
| dev-neomail | 3 seuils | n=1 (1 invocation Feature 06+10 enorme) | **Verdict reporte** — Niveau 3 requis |

### Lecon empirique

> "Niveau 1 = carte. Niveau 2 = verdict pour echantillon. Niveau 3 = verdict statistique."
> — Verdict advisor() forge 2026-05-23

**Le diagnostic Niveau 1 a flagge architect-deep comme worst case (5/5 seuils), mais Niveau 2 montre 6 ops typiques = sous le seuil canonique Cat Wu**. Sans Niveau 2, refactor architect-deep aurait casse un agent qui fonctionne bien.

### Decisions prises 2026-05-23

#### 1. Pas de refactor split d'agents (option a rejetee)

Mass refactor sur n=1/2/31 donnees pauvres = reproduction du pattern F1/F2 (claims non verifies a echelle plus large). Advisor verdict KEEP architect-deep + report verdict dev-neodoc/dev-neomail.

#### 2. Option (b) deployee — scope invocations (rule update)

Ajout 1 ligne dans `.claude/rules/agent-delegation.md` neo_ia :
> "Quand tu invoques dev-* via Agent, scope la description sur une seule tache atomique (~30 LOC). Pas de description multi-feature type 'refacto X + Y + Z + tests'. Mesure Niveau 2 montre distribution p50=27 p90=116 = outliers d'invocations trop larges."

Coût : 0 risque, 0 modif structurelle. Si (b) suffit → (a) jamais necessaire.

#### 3. Niveau 3 instrumentation deployee

Hook `SubagentStop` `.claude/hooks/agent-metrics-logger.py` qui logge `.claude/agent-metrics.csv` (gitignored) :

```
timestamp, agent_id, subagent_type, duration_ms, ops_total, tokens_input, tokens_output, tokens_total, success, turns
```

Append-only, observabilite Fowler sensor, autorise doctrine 22 mai. Laisser tourner 1-2 semaines avant reanalyse.

Pattern Boris/Anthropic interne pour "+200% PRs Cat Wu measure".

### Liens additionnels

- [[feedback_audit_claims_after_brief]] — Niveau 1 verdict prematu reproduirait F1/F2
- [[critique-2026-05-22-doctrine-drift-guard]] — anti-pattern : workaround sans instrumentation
- [[raisonnement-22mai-doctrine-vs-enforcement]] — hooks lint/security/scope/**observabilite** autorise

### Pour la prochaine session

Reanalyser `.claude/agent-metrics.csv` neo_ia dans 1-2 semaines avec n=50+ invocations. Critere verdict statistique : si p50 > 8 ops sur > 20 invocations dev-* malgre rule scope → split confirme. Sinon → rule scope suffit.
