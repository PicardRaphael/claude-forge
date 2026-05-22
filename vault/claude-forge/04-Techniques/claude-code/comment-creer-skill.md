---
titre: "Comment créer une skill Claude Code parfaite"
resume: "Note canonique pour créer une skill Claude Code selon les 9 catégories Thariq, structure progressive disclosure, frontmatter trigger 3e personne, < 500L SKILL.md, agentskills.io spec ouverte."
aliases:
  - "comment creer skill"
  - "creer une skill"
  - "create skill claude code"
  - "skill parfaite"
  - "skill best practices"
  - "9 categories thariq"
  - "progressive disclosure skill"
  - "SKILL.md structure"
  - "frontmatter skill"
  - "agentskills.io"
derniere-maj: 2026-05-22
auteur: claude
type: technique
sources:
  - "https://www.claude.com/blog/skills-explained"
  - "Thariq Shihipar LinkedIn 17 mars 2026 — 9 catégories"
  - "github.com/anthropics/skills"
  - "agentskills.io"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/skills"
  - "#doctrine/2026"
---

# Comment créer une skill Claude Code parfaite

> Note canonique forge — création de skills selon doctrine Anthropic + Thariq mai 2026.

---

## QUOI — Définition

**Skill** = bundle markdown qui enseigne à Claude **comment faire** une tâche précise et réutilisable. Structure :

```
.claude/skills/<nom-kebab-case>/
├── SKILL.md          # Description + body (< 500 lignes)
├── scripts/          # Optionnel : scripts exécutables
├── references/       # Optionnel : doc détaillée déportée
└── assets/           # Optionnel : templates, exemples
```

**Verbatim Anthropic** :

> "MCP connects Claude to data; Skills teach Claude what to do with that data."
> — [claude.com/blog/skills-explained](https://www.claude.com/blog/skills-explained)

**Progressive disclosure** : la `description` en frontmatter est chargée systématiquement. Le body de SKILL.md est chargé **uniquement à l'activation**. Les fichiers de `references/` chargés à la demande pendant exécution.

**Spec ouverte** : `agentskills.io` adoptée par ~40 produits (Cursor, Codex, Gemini CLI, Goose, Copilot, etc.). Une skill bien écrite est portable.

---

## POURQUOI — Le problème résolu

Sans skills, on accumule dans CLAUDE.md des instructions cross-repos (= bruit). Skills permettent :

- **Réutilisation cross-repos** (skill écrite 1×, utilisée partout)
- **Progressive disclosure** (budget contexte 5k tokens chacune, 25k combiné post-compaction)
- **Partage public** via agentskills.io (skill cross-tools)
- **Auto-trigger** via description directive (Claude détecte le besoin)

---

## COMMENT — Structure et frontmatter

### Frontmatter SKILL.md

```yaml
---
name: <nom-exact-du-dossier-kebab-case>
description: <trigger directive 3e personne, max 1024 chars>
allowed-tools: <optionnel — liste outils>
model: <optionnel — sonnet/opus/haiku>
---
```

**Règles frontmatter critiques** :

1. **`name`** = EXACTEMENT le nom du dossier kebab-case. Pas de variation.
2. **`description`** = **TRIGGER directive 3e personne** :
   - ❌ "I help you create skills"
   - ❌ "This skill creates skills"
   - ✅ "Use when creating a new Claude Code skill, modifying an existing one, or when the user asks 'comment créer une skill'"
3. **`description` ≤ 1024 caractères** — au-delà tronquée
4. **`description` = critère d'activation** — Claude lit toutes les descriptions à chaque turn pour décider quelle skill activer

### Body SKILL.md

```markdown
# <Nom skill>

<1-2 phrases — quand utiliser cette skill, le résultat attendu>

## <Section principale>

<Instructions claires, étape par étape, formulées comme directives>

## Étapes

1. <étape concrète>
2. <étape concrète>
...

## Gotchas

- <piège 1>
- <piège 2>

## Apprentissage (optionnel pour skills métier)

<À la fin d'une session utilisant cette skill, noter ce qui a marché/échoué>
```

**Règle 500 lignes** : SKILL.md < 500 lignes. Au-delà, déporter le détail dans `references/` (chargé à la demande).

### Quand utiliser scripts/

Pour les opérations déterministes (parsing, transformation, validation), un script (`.py`, `.sh`) est plus fiable que des instructions au LLM. La skill l'appelle via Bash.

### Quand utiliser references/

Pour la documentation longue, exemples massifs, ou détails à charger conditionnellement. SKILL.md cite `references/<file>.md` quand pertinent.

---

## QUAND — 9 catégories Thariq (LinkedIn 17 mars 2026)

Ordre verbatim de Thariq Shihipar (Anthropic) :

| # | Catégorie | Exemples |
|---|-----------|----------|
| 1 | **Library & API Reference** | Doc d'une lib interne, conventions API repo |
| 2 | **Product Verification** | Tester qu'une feature marche, smoke tests |
| 3 | **Data Fetching & Analysis** | Récupérer + analyser des metrics, logs |
| 4 | **Business Process & Team Automation** | Workflows équipe, runbooks process |
| 5 | **Code Scaffolding & Templates** | Générer composants standardisés (cf Lisa Crofoot) |
| 6 | **Code Quality & Review** | Checklists review, lint patterns custom |
| 7 | **CI/CD & Deployment** | Pipelines, rollback procedures |
| 8 | **Runbooks** | Incident response, on-call procedures |
| 9 | **Infrastructure Operations** | Provisioning, infra commands |

**Critère** : si ce que tu veux automatiser entre dans 1 de ces 9 catégories → skill légitime. Sinon, reconsidérer (peut-être agent, hook, ou simple CLAUDE.md).

---

## WORKFLOW — Création étape par étape

### Étape 1 — Identifier le besoin
- La tâche est-elle **réutilisable** (cross-sessions, cross-repos) ?
- Entre-t-elle dans 1 des 9 catégories Thariq ?
- Sinon → CLAUDE.md ou rule suffit

### Étape 2 — Déléguer à `skill-creator`
Côté forge : agent `skill-creator` génère SKILL.md conforme. Hook `delegate-guard.py` BLOQUE l'édit direct de `SKILL.md`.

Côté repo externe : utiliser `mcp-builder` ou `skill-creator` officiel Anthropic.

### Étape 3 — Frontmatter trigger
Écrire la **description comme un trigger directive 3e personne**. Tester mentalement : "si je tape X dans une session, est-ce que Claude devrait activer cette skill ?"

### Étape 4 — Body progressive disclosure
- SKILL.md < 500 lignes
- Instructions claires et directives
- Déporter détail vers `references/`
- Scripts pour opérations déterministes

### Étape 5 — Test en session fraîche
Tester la skill dans une session vierge avec un prompt qui devrait l'activer. Si elle ne s'active pas → description pas assez directive.

### Étape 6 — Devil's advocate (CONDITIONNEL)
Côté forge : `devils-advocate` UNIQUEMENT si livrable majeur (skill réutilisée cross-repos, skill sécu critique, skill métier complexe). Doctrine 22 mai : pas de gates systématiques (cf [[raisonnement-22mai-doctrine-vs-enforcement]]). DA reste **conditionnel**, pas réflexe.

---

## APPELS — Composants mobilisés

- [[mcp-vs-skills-doctrine]] — décider skill vs MCP vs Bash
- [[comment-creer-agent]] — quand l'instruction concerne un rôle, pas une procédure
- [[comment-creer-hook]] — quand la skill doit valoir 100% (= hook complémentaire)
- [[comment-ecrire-claudemd]] — où mentionner les skills custom du repo
- [[workflow-claude-code-optimal]] — comment skills s'inscrivent dans le workflow

---

## OPTIMISATION — 3 niveaux

### Niveau basique
- SKILL.md monolithique < 500L
- Pas de scripts, pas de references/
- Description claire mais pas optimisée pour trigger

### Niveau avancé
- Frontmatter trigger optimisé (3e personne, directive, mots-clés réels users)
- references/ pour détail
- scripts/ pour ops déterministes
- Section Gotchas + Apprentissage

### Niveau expert
- Skill publique sur `agentskills.io` (portable Cursor + Codex + Gemini CLI + ~40 produits)
- Composition avec MCP tools (la skill orchestre, MCP fournit data)
- Hooks complémentaires pour invariants
- Modèle dédié si workload spécifique (`model: opus` pour jugement)
- `allowed-tools` restreint pour sécu

---

## POURQUOI CETTE OPTIM — Gain mesurable

| Optim | Gain |
|-------|------|
| Description trigger directive | Auto-activation fiable, ~0 token gaspillé sur mauvaises activations |
| < 500L SKILL.md + references/ | Body chargé seulement à l'activation, references seulement à la demande |
| Progressive disclosure | 5k tokens budget par skill, 25k combiné post-compaction (limites Anthropic) |
| scripts/ pour ops déterministes | Fiabilité 100% vs compliance partielle LLM sur ops répétitives |
| agentskills.io | 1 skill = utilisable sur ~40 produits |

---

## ANTI-PATTERNS

### Description / frontmatter
- ❌ Description en 1ère personne ("I help...") — toujours 3e personne directive
- ❌ Keyword stuffing dans description — cf [[e-descriptions-keyword-stuffing]]
- ❌ `name` ≠ nom du dossier — invalide
- ❌ Description > 1024 caractères — tronquée
- ❌ **Description qui copie le body** : la description est un TRIGGER ("Use when X"), pas un résumé du contenu. Si la description = première ligne du body, c'est faux. Description directive ≠ description descriptive.

### Structure
- ❌ **SKILL.md monolithique > 500 lignes** — déporter dans `references/`
- ❌ **README.md dans le dossier skill** — non-standard
- ❌ **Skills orphelines** dans frontmatter d'un agent mais non référencées dans le body — jamais activées (cf [[feedback_non_invokable_skills_orphan]])
- ❌ **Édit direct SKILL.md** côté forge — délégation obligatoire à `skill-creator` (hook bloque)

### Contenu
- ❌ **STOP critique en gotchas fin** — critique < ligne 25 (cf [[erreur-stop-critique-position-gotcha-fin]])
- ❌ **Emphasis ALL-CAPS excessif** — 1-2 OK, 20 = bruit (cf [[feedback_emphasis_distinction]])
- ❌ **Description du code** au lieu de directives — la skill enseigne le HOW, pas le WHAT

### Architecture
- ❌ **Skill pour ce qu'un MCP ferait** (accès données) — confusion couches (cf [[mcp-vs-skills-doctrine]])
- ❌ **Skill pour ce qu'un agent ferait** (rôle long-running) — agent, pas skill
- ❌ **Skill métier sans section Apprentissage** — cf [[feedback_skills_memory_section]]

---

## EXEMPLES CONCRETS — Repos externes

### Référence Anthropic
- **[github.com/anthropics/skills](https://github.com/anthropics/skills)** — **17 skills officielles** incluant :
  - `skill-creator` (méta : skill qui crée des skills)
  - `mcp-builder` (créer des MCP servers)
  - `pdf` (manipulation PDF)
  - `frontend-design` (Lisa Crofoot)
  - et 13 autres

### Référence Karpathy
- **`karpathy/nanochat/.claude/skills/read-arxiv-paper/SKILL.md`** — seul skill public Karpathy
- ~40 lignes, atomique, démonstration "court + précis > long + générique"

### Référence écosystème
- **Stripe**, **Vercel**, **Cloudflare**, **Sentry**, **OpenAI**, **HashiCorp**, **Figma**, **Netlify** — skills publics
- **Simon Willison** `simonw/llm`

### Spec ouverte
- **[agentskills.io](https://agentskills.io)** — adopté par ~40 produits
- Cursor, Codex, Gemini CLI, Goose, Copilot, Roo, Kiro, Letta, Spring AI, Snowflake Cortex, Tabnine, Mistral Vibe, etc.

---

## SOURCES — Verbatim avec URLs

### Anthropic officiel
- [claude.com/blog/skills-explained](https://www.claude.com/blog/skills-explained) — doctrine MCP/Skills
- [github.com/anthropics/skills](https://github.com/anthropics/skills) — 17 skills officielles
- docs Anthropic features-overview — budget 5k/25k tokens

### Thariq Shihipar (Anthropic)
- **LinkedIn 17 mars 2026** — 9 catégories verbatim
- **Code with Claude SF 6-7 mai 2026** — Agent SDK Workshop + HTML markdown talks

### Lisa Crofoot (Anthropic)
- **Code with Claude London 19 mai 2026** — "scaffolding holds Claude back" (catégorie 5 critique)

### Simon Willison
- [simonwillison.net/2025/Oct/16/claude-skills/](https://simonwillison.net/2025/Oct/16/claude-skills/) — "Skills maybe a bigger deal than MCP"

### Spec
- [agentskills.io](https://agentskills.io) — ~40 produits

---

## GOTCHAS — Pièges observés

### Pièges frontmatter
- **Description YAML une seule ligne** : jamais `>-` ni `|` (forge)
- **`name` kebab-case = dossier** exact
- **Description 3e personne directive** sinon trigger défaillant
- **≤ 1024 chars** sinon tronquée

### Pièges structure
- **`README.md` dans dossier skill** = non-standard
- **`scripts/` doivent être exécutables** (+x sur Unix, .py avec shebang)
- **`references/` cités explicitement** dans SKILL.md (`voir references/foo.md`)
- **MultiEdit matcher** dans hook PreToolUse : "Write|Edit" sans MultiEdit = trou (cf [[feedback_multiedit_matcher_blind_spot]])

### Pièges contexte
- **`$ARGUMENTS` dans backticks** = substitution littérale qui casse quoting
- **Skills publiques sensibles** : pas de credentials, de paths absolus user-specific
- **Hot reload skills** : redémarrer la session pour prise en compte
- **Budget tokens 5k/25k** : surveiller avec `references/` plutôt que tout en SKILL.md

### Pièges forge
- **Édit direct bloqué par hook** `delegate-guard.py` — utiliser `skill-creator`
- **Vault check obligatoire** avant création (cf [[forge-brain-proactive]])
- **DA après création majeure** (cf [[devils-advocate-pipeline]])
- **Description en anglais** (convention forge)

---

## ALIASES — Findability

Aliases déclarés en frontmatter (10) :
- comment creer skill
- creer une skill
- create skill claude code
- skill parfaite
- skill best practices
- 9 categories thariq
- progressive disclosure skill
- SKILL.md structure
- frontmatter skill
- agentskills.io

---

## WIKILINKS

### Notes canoniques sœurs
- [[comment-creer-agent]]
- [[comment-creer-hook]]
- [[comment-ecrire-claudemd]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[mcp-vs-skills-doctrine]]
- [[pattern-vault-llm-karpathy]]

### Fiches leaders (à créer)
- [[Thariq Shihipar]]
- [[Lisa Crofoot]]
- [[Andrej Karpathy]]
- [[Simon Willison]]

### Knowledge / erreurs liées
- [[erreur-edit-direct-skills]]
- [[erreur-skill-monolithique-sans-references]]
- [[erreur-stop-critique-position-gotcha-fin]]
- [[e-descriptions-keyword-stuffing]]
- [[feedback_non_invokable_skills_orphan]]
- [[feedback_skills_memory_section]]
- [[feedback_emphasis_distinction]]
- [[feedback_multiedit_matcher_blind_spot]]
- [[feedback_skills_referenced_in_body]]

### Forge custom
- [[skill-creator]] — agent forge dédié
- [[devils-advocate-pipeline]] — rule DA après création
- [[forge-brain-proactive]] — rule vault check
- [[check-before-create]] — rule pré-création

---

**Fin note canonique `comment-creer-skill.md`** — 3/8 chantier 22 mai 2026.
