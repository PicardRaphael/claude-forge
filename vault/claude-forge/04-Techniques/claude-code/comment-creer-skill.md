---
derniere-maj: 2026-06-06
resume: Note canonique pour créer une skill Claude Code selon les 9 catégories Thariq (post Anthropic mars 2026), structure progressive disclosure, frontmatter trigger 3e personne, < 500L SKILL.md, limite description 1024 chars spec / 1536 listing (pas 250), interview 3 rounds obligatoires, evals obligatoires, agentskills.io spec ouverte.
---
﻿---
titre: "Comment créer une skill Claude Code parfaite"
resume: "Note canonique pour créer une skill Claude Code selon les 9 catégories Thariq (post Anthropic mars 2026), structure progressive disclosure, frontmatter trigger 3e personne, < 500L SKILL.md, limite pratique description ~250 chars pour auto-invocation, agentskills.io spec ouverte."
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
derniere-maj: 2026-05-27
auteur: claude
type: technique
sources:
  - "https://www.claude.com/blog/skills-explained"
  - "Thariq Shihipar — post Anthropic 'Lessons from Building Claude Code: How We Use Skills' (mars 2026)"
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

> ⚠️ **Ordre canonique pour TOUTE création/modification de skill** : suivre A→B→C→D→E (analyser réel → lire canoniques EN ENTIER → croiser → plan d'écarts → exécuter). Cf [[methode-analyser-repo]] section **ORDRE CANONIQUE**. Pas de prescription avant analyse du réel.

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
description: <trigger directive 3e personne, max 1024 chars spec — viser < 250 chars pour auto-invocation fiable>
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
3. **`description` — DEUX limites importantes** :
   - **Spec officielle** : 1024 chars max (au-delà tronquée)
   - **Limite pratique auto-invocation** : **~250 chars** — le système reminder `/skills` injecté à chaque turn tronque les descriptions au-delà → tout ce qui dépasse devient **invisible à Claude pour l'auto-trigger**
   - **Conséquence** : viser < 250 chars dans la `description` pour garantir l'auto-trigger fiable. Le détail va dans le body
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

## QUAND — 9 catégories Thariq

Source : Thariq Shihipar (Anthropic Claude Code team) — post Anthropic **"Lessons from Building Claude Code: How We Use Skills"** (mars 2026, date exacte à confirmer ~13-19 mars). Référence tierce : [dev.to article framework 19 mars 2026](https://dev.to/minatoplanb/how-anthropic-actually-uses-skills-in-claude-code-a-9-category-framework-1kel).

Verbatim contexte : *"Anthropic runs hundreds of Skills internally, organized into 9 categories"*.

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

Insight Thariq : "most teams only use 2-3 of these categories — not because the others aren't useful, but because they didn't know they existed". Et : "Skills with a Gotchas section measurably improve Claude's accuracy".

---

## WORKFLOW — Création étape par étape

### Étape 1 — Identifier le besoin
- La tâche est-elle **réutilisable** (cross-sessions, cross-repos) ?
- Entre-t-elle dans 1 des 9 catégories Thariq ?
- Sinon → CLAUDE.md ou rule suffit

### Étape 2 — Déléguer à `skill-creator`

> ⚠️ **Pivot 6 juin 2026** : `skill-creator` est désormais une **skill** (`.claude/skills/skill-creator/`), pas un agent. Invoquer via `Skill(skill-creator)` depuis la session principale. Le hard block `delegate-guard.py` sur `SKILL.md` a été retiré — enforcement advisory. Voir [[delegate-to-specialists]].

Côté repo externe : utiliser `mcp-builder` ou `skill-creator` officiel Anthropic.

Côté forge : agent `skill-creator` génère SKILL.md conforme. Hook `delegate-guard.py` BLOQUE l'édit direct de `SKILL.md`.

Côté repo externe : utiliser `mcp-builder` ou `skill-creator` officiel Anthropic.

### Étape 3 — Frontmatter trigger

Écrire la **description comme un trigger directive 3e personne**. Tester mentalement : "si je tape X dans une session, est-ce que Claude devrait activer cette skill ?"

**Limites description (corrigées juin 2026) :**
- ≤ **1024 chars** spec officielle (hard limit)
- description + `when_to_use` ≤ **1536 chars** combiné dans le skill listing
- Viser court et dense — triggers concrets en premier
- Le "250 chars" anciennement cité était une estimation empirique du system reminder dans un contexte donné, pas une limite de troncature CC. Limites canoniques : 1024 / 1536.

Écrire la **description comme un trigger directive 3e personne**. Tester mentalement : "si je tape X dans une session, est-ce que Claude devrait activer cette skill ?"

**Cibler < 250 chars** dans la description pour garantir l'auto-trigger (limite pratique system reminder).

### Étape 4 — Body progressive disclosure
- SKILL.md < 500 lignes
- Instructions claires et directives
- Déporter détail vers `references/`
- Scripts pour opérations déterministes

### Étape 4bis — Evals A/B (OBLIGATOIRES)

Les evals sont **obligatoires** pour toute skill créée ou optimisée. Sans mesure → pas de preuve que la skill améliore les résultats (SkillsBench : auto-généré sans eval = –1.3pp en moyenne).

- 2–3 test cases validés par l'utilisateur → `evals/evals.json`
- Spawner simultanément `with_skill` + `baseline` via Task tool
- Générer le eval viewer AVANT de juger soi-même
- Description optimization loop : ~20 trigger queries, best_description sur score test
- Seule exception : skill de connaissance pure subjective → éval qualitative uniquement

Détail complet : `.claude/skills/skill-creator/references/eval-workflow.md`

### Étape 5 — Test en session fraîche
Tester la skill dans une session vierge avec un prompt qui devrait l'activer. Si elle ne s'active pas → description pas assez directive **ou** trop longue (>250 chars système reminder).

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
- Frontmatter trigger optimisé (3e personne, directive, < 250 chars, mots-clés réels users)
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
| Description trigger directive < 250 chars | Auto-activation fiable (au-delà : invisible reminder `/skills`) |
| < 500L SKILL.md + references/ | Body chargé seulement à l'activation, references seulement à la demande |
| Progressive disclosure | 5k tokens budget par skill, 25k combiné post-compaction (limites Anthropic) |
| scripts/ pour ops déterministes | Fiabilité 100% vs compliance partielle LLM sur ops répétitives |
| agentskills.io | 1 skill = utilisable sur ~40 produits |

---

## CHECKLIST SKILL PARFAITE — 6 dimensions (source: research LLM juin 2026)

> Checklist complète pour valider une skill avant livraison. Couvre discovery, body, structure, évaluation, optimisation, packaging. Hedges : chiffres Seleznov/SkillsBench non vérifiés primaire — directions solides.

### 1. Discovery / activation
- [ ] Description = identifiant domaine + "ALWAYS invoke when…" + contrainte négative ("Do not X directly")
- [ ] 3e personne ; contient le QUOI et le QUAND ; phrases de trigger concrètes incl. cas où l'utilisateur ne nomme pas la skill
- [ ] `name` kebab-case, ≤64 chars, pas "claude"/"anthropic", gérondif préféré
- [ ] Description ≤ 250 chars pratique (auto-trigger system reminder) / ≤ 1024 chars spec / description+when_to_use ≤ 1536 chars combiné dans le listing
- [ ] UNE SEULE LIGNE YAML — jamais `>-` ni `|` (casse la découverte)
- [ ] Pas de XML tags dans la description
- [ ] Inclut near-miss exclusions pour éviter l'over-trigger

### 2. Body / exécution
- [ ] SKILL.md body < 500 lignes ; references une seule profondeur ; ToC si > 100 lignes
- [ ] Voix impérative ; expliquer le *pourquoi* plutôt que ALL-CAPS MUST ; réserver ALWAYS/NEVER aux étapes fragiles/critiques uniquement
- [ ] Scripts : préciser si EXÉCUTER vs LIRE ; pas de constantes magiques
- [ ] Gestion d'erreur explicite ; chemins forward-slash uniquement ; packages listés
- [ ] Boucles de validation pour opérations quality-critical ; checklist copiable pour workflows multi-étapes

### 3. Structure / enforcement (par environnement cible)
- [ ] **CLI** → hooks ok (PreToolUse/PostToolUse)
- [ ] **Desktop** → best-effort hooks, script-output gating préféré
- [ ] **Cowork** → ZÉRO hooks ; script-output gating + slash entry + MCP remote HTTPS validation
- [ ] Skills side-effecting (deploy/commit/send/delete) : `disable-model-invocation: true` + `allowed-tools` whitelist + AskUserQuestion gate (session principale, pas sub-agent)
- [ ] Type MCP adapté à la surface (stdio CLI/Desktop ; remote HTTPS Cowork)
- [ ] Scripts enforceables uniquement via leur OUTPUT — Claude doit lire/agir sur la sortie
- [ ] Routing pointers dans CLAUDE.md/.claude/rules (CLI/Desktop) ou project Instructions (Cowork) — jamais dupliquer le contenu dans CLAUDE.md

### 4. Évaluation
- [ ] ≥ 3 task evals ; ~20 trigger queries (8–10 should-fire, 8–10 near-miss should-NOT-fire ; substantielles, pas one-step)
- [ ] Baseline-without-skill vs with-skill ; 3–5 trials par case ; runs isolés ; noter outcomes pas paths
- [ ] Lire les transcripts, pas juste les outputs
- [ ] Générer le eval viewer AVANT de juger soi-même (`--static` sur Cowork/headless)
- [ ] Tester sur Haiku/Sonnet/Opus effectivement utilisés

### 5. Optimisation / audit (mode amélioration skill existante)
Détecter et corriger :
- [ ] Description tronquée / over-budget (> 250 chars pratique, > 1024 spec)
- [ ] Description passive (non-directive)
- [ ] Chaînes de references > 1 niveau de profondeur
- [ ] References mortes ou cassées
- [ ] "Why" manquant (tout ALL-CAPS sans explication = yellow flag)
- [ ] ALL-CAPS excessif (> 2-3 = bruit)
- [ ] Exclusions near-miss manquantes
- [ ] SKILL.md > 500 lignes
- [ ] Skill flat-file qui devrait être un dossier (avec scripts/ + references/)
- [ ] Doctrine dupliquée/divergente entre skills
- [ ] Assertions non-discriminantes dans evals
- [ ] YAML multi-ligne (Prettier mangling)
- Scorer chaque violation avec fichier + fix en une ligne ; boucler jusqu'à propre

### 6. Packaging / distribution
- [ ] Packager en `.skill` si distribution souhaitée
- [ ] Bundler en plugin pour distribution équipe
- [ ] Confirmer l'emplacement par surface : `.claude/skills/` (projet) / `~/.claude/skills/` (user) / plugin-bundled
- [ ] **Cowork** : enregistrer via UI, garder total actif < 30
- [ ] Conserver le nom à l'update (pas de `-v2`) ; copier dans temp dir avant d'éditer une skill installée read-only

---

## Questions interview (3 rounds, via AskUserQuestion — ≤4 questions/round)

> Extraire d'abord depuis l'historique de conversation. Ne poser QUE ce qui n'est pas déductible. Stopper tôt si les réponses sont évidentes.

**Round 1 — Intent (toujours)**
1. Que doit permettre cette skill à Claude ? (texte libre)
2. **Environnement cible ?** → CLI / Desktop app / Cowork / Portable (doit marcher partout) — *question de branchement : détermine l'enforcement strategy*
3. Créer une nouvelle skill, ou optimiser/auditer une existante ?

**Round 2 — Déclenchement & frontières**
4. Quand doit-elle se déclencher (phrases/contextes) ? Quand explicitement PAS (near-misses) ?
5. A-t-elle des side-effects (deploy/commit/send/delete) ? → si oui → `disable-model-invocation: true` + slash-only + approval gate

**Round 3 — Forme & outillage**
6. SKILL.md unique, ou dossier avec scripts + references ? (Recommander scripts si logique déterministe répétée ; references si doc > 300 lignes)
7. Quels outils/MCP nécessaires ? (Brancher sur env : stdio MCP pour CLI/Desktop seulement ; remote HTTPS pour Cowork)
8. Modèle(s) cible ? (Haiku = plus de guidance, Opus = moins)
9. Mettre en place des evals ? (Recommandé OUI pour outputs objectivement vérifiables)

## ANTI-PATTERNS

### Description / frontmatter
- ❌ Description en 1ère personne ("I help...") — toujours 3e personne directive
- ❌ Description **> 250 chars** = tronquée par system reminder `/skills` → invisible à Claude pour auto-trigger
- ❌ Description **> 1024 chars** = tronquée spec officielle
- ❌ Keyword stuffing dans description — cf [[e-descriptions-keyword-stuffing]]
- ❌ `name` ≠ nom du dossier — invalide
- ❌ **Description qui copie le body** : la description est un TRIGGER ("Use when X"), pas un résumé du contenu. Si la description = première ligne du body, c'est faux. Description directive ≠ description descriptive.

### Structure
- ❌ **Édit direct SKILL.md sans passer par la skill `skill-creator`** — advisory : rien ne bloque techniquement, mais les best practices (checklist 6 dimensions, interview, evals) sont appliquées automatiquement par la skill
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
- **[github.com/anthropics/skills](https://github.com/anthropics/skills)** — skills officielles (incluant `skill-creator`, `mcp-builder`, `pdf`, `frontend-design`, etc.). Compte exact à vérifier sur le repo (le sous-dossier `skills/` n'est pas toujours listé par WebFetch automatique).

### Référence Karpathy
- **`karpathy/nanochat/.claude/skills/read-arxiv-paper/SKILL.md`** — ~40 lignes, atomique (single skill public Karpathy)

### Référence écosystème
- **Stripe**, **Vercel**, **Cloudflare**, **Sentry**, **OpenAI**, **HashiCorp**, **Figma**, **Netlify** — skills publics
- **Simon Willison** `simonw/llm`

### Spec ouverte
- **[agentskills.io](https://agentskills.io)** — ~40 produits
- Cursor, Codex, Gemini CLI, Goose, Copilot, Roo, Kiro, Letta, Spring AI, Snowflake Cortex, Tabnine, Mistral Vibe, etc.

---

## SOURCES — Verbatim avec URLs

### Anthropic officiel
- [claude.com/blog/skills-explained](https://www.claude.com/blog/skills-explained) — doctrine MCP/Skills
- [github.com/anthropics/skills](https://github.com/anthropics/skills) — skills officielles
- docs Anthropic features-overview — budget 5k/25k tokens

### Thariq Shihipar (Anthropic)
- **Post Anthropic mars 2026** "Lessons from Building Claude Code: How We Use Skills" — 9 catégories. Référence tierce : [dev.to article framework](https://dev.to/minatoplanb/how-anthropic-actually-uses-skills-in-claude-code-a-9-category-framework-1kel)
- **Code with Claude SF 6-7 mai 2026** — Agent SDK Workshop + HTML markdown talks
- **Verbatim compute allocators** : "All of us are becoming these compute allocators now" (ChatPRD How I AI)

### Lisa Crofoot (Anthropic)
- **Code with Claude London 19 mai 2026** — frontend-design skill, catégorie 5 (Code Scaffolding)

### Simon Willison
- [simonwillison.net/2025/Oct/16/claude-skills/](https://simonwillison.net/2025/Oct/16/claude-skills/) — "Skills maybe a bigger deal than MCP"

### Spec
- [agentskills.io](https://agentskills.io) — ~40 produits

---

## GOTCHAS — Pièges observés

### Pièges frontmatter
- **Limites description** : ≤ 1024 chars spec (hard limit) ; description + `when_to_use` ≤ 1536 chars combiné dans le listing. ~~Le "250 chars" anciennement cité~~ était une estimation du system reminder dans un contexte donné — pas une limite de troncature CC. Limites canoniques : **1024 / 1536**.
- **Evals obligatoires** : toute skill créée ou optimisée doit passer par les evals A/B (with_skill vs baseline). Sans mesure = pas de validation.
- **Interview 3 rounds obligatoires** : ne pas bypasser l'interview, même si l'objectif semble évident. Une question peut être skippée uniquement si la réponse est explicite dans le contexte.
- **Description YAML une seule ligne** : jamais `>-` ni `|` — convention forge (évite bugs parsing dans plusieurs outils, pas spec Anthropic stricte)
- **`name` kebab-case = dossier** exact
- **Description 3e personne directive** sinon trigger défaillant
- **Spec 1024 chars MAIS limite pratique ~250 chars** pour auto-invocation (system reminder tronque)

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
- [[eval-pattern-anthropic-skill-creator]]

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
- `.claude/rules/check-before-create.md` — rule pré-création (hors vault)

---

**Fin note canonique `comment-creer-skill.md`** — révisée 23 mai 2026 post-audit thématique vault.


## Gotchas

- [[erreur-subagent-bypass-delegate-guard]] — Quand skill-creator est instruit d'éditer un SKILL.md, il peut tenter de contourner le hook delegate-guard via staging file. Anti-pattern : sub-agents cherchent des bypass.


---

## AJOUT 24 mai 2026 — Reliability auto-invocation ~50% sans formule directive

**Verbatim audit communautaire** (214 skills audités, [DEV.to](https://dev.to/thestack_ai/i-audited-214-claude-code-skills-73-were-silently-broken-2m9a)) :

> "73% silencieusement cassées — jamais déclenchées. Même avec YAML valide, le déclenchement autonome atteint ~50% de succès."

### Causes top 3 d'échec d'activation

| Cause | Fréquence |
|-------|-----------|
| Descriptions vagues sans phrases de déclenchement | 68% |
| Descriptions < 20 mots | 41% |
| Collision entre skills (descriptions qui se chevauchent) | ~15% |

### Formule directive (Anthropic-validée)

```
ALWAYS invoke when [trigger]. <description essentielle>. DO NOT [action concurrente] without invoking first.
```

**Exemple appliqué 24 mai 2026 sur 10 skills critiques ia_back + neo_ia** :

```yaml
# AVANT (passif)
description: Complete procedure to add a new REST endpoint. Use when user says 'ajoute un endpoint'...

# APRÈS (directif)
description: ALWAYS invoke when user says 'ajoute un endpoint', 'crée une route', 'new endpoint'. Complete procedure to add a new REST endpoint with Zod schemas, Hono routes, postgres.js queries, and tests. DO NOT write endpoint code without invoking first.
```

### Contraintes critiques

- **≤ 1024 chars** : limite frontmatter Anthropic (au-delà tronquée)
- **≤ 250 chars idéal** : limite pratique auto-invocation (`/skills` reminder injecté à chaque turn tronque)
- **Triggers concrets** : phrases utilisateur exactes (FR + EN), pas marketing copy
- **Bad** : "A powerful Git automation skill."
- **Good** : "ALWAYS invoke when user wants to commit changes, write a commit message, or open a PR. DO NOT use git commands manually without invoking first."

### Le pattern le plus fiable : hook Skill Activation

Quand auto-invocation reste à ~50% malgré description parfaite, hook `UserPromptSubmit` qui injecte `Use Skill(name)` dans le prompt avant que Claude le voie. **Garantie 100% activation**. Voir [[cowork-skills-reliability]] section "Skill Activation Hook".

### Sources

- [Audit 214 skills communautaires](https://dev.to/thestack_ai/i-audited-214-claude-code-skills-73-were-silently-broken-2m9a)
- [Why Claude Code Skills Don't Trigger](https://dev.to/lizechengnet/why-claude-code-skills-dont-trigger-and-how-to-fix-them-in-2026-o7h)
- [[cowork-skills-reliability]] — checklist 9 étapes diagnostic
- [Skills docs Anthropic](https://code.claude.com/docs/en/skills)


---

## AJOUT 24 mai 2026 (suite) — Wildcard MCP `mcp__server__*` dans `allowed-tools:`

**Verbatim Anthropic docs** ([code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions) section MCP) :

> * `mcp__puppeteer__*` wildcard syntax that also matches all tools from the `puppeteer` server

### Application forge

Pour skills qui accèdent au vault forge-brain, utiliser **wildcard** au lieu de lister 5-7 outils :

```yaml
# ❌ AVANT
allowed-tools: Read, Write, Edit, Bash, mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__create_note, mcp__forge-brain__append_note, mcp__forge-brain__update_property

# ✅ APRÈS
allowed-tools: Read, Write, Edit, Bash, mcp__forge-brain__*
```

### Bénéfices identiques aux agents

- Pas d'oubli si MCP évolue (21 outils en mai 2026, plus à venir)
- Token budget frontmatter optimisé
- Sémantiquement plus juste

### Application 24 mai 2026

6 skills forge converties au wildcard : cc-news, done, reasoning-cache, forge-review, recap, skill-evolve. Plus la skill `/spec` (3 repos) qui avait déjà besoin d'accès large.

### Voir aussi

Section identique dans [[comment-creer-agent]] (AJOUT 24 mai suite) pour le champ `tools:` des agents — même syntaxe wildcard, même justification.

### Sources

- [Anthropic Permissions docs section MCP](https://code.claude.com/docs/en/permissions#mcp)


---

## AJOUT 24 mai 2026 (suite 2) — Pattern MCP brief-then-direct
Pour les skills qui ont `mcp__server__*` dans `allowed-tools:` et qui sont **invoquées par sub-agents** (pas par session principale directement), le pattern s'applique aussi :

- Session principale qui dispatch le sub-agent → brief enrichi avec contexte MCP
- Sub-agent invoque la skill avec le contexte
- Skill exécute + peut re-consulter MCP en filet si besoin (terme non couvert)

Section body standardisée identique à celle des agents — voir [[pattern-mcp-brief-then-direct]] pour template complet.

Skills concernées forge : `forge-brain`, `done`, `cc-news`, `reasoning-cache`, `recap`, `skill-evolve`, `forge-review`, `obsidian-markdown`.
Skills concernées neo_ia/ia_back : toutes celles qui ont des MCP dans allowed-tools (typiquement context7, postgres, langfuse).


## AJOUT 27 mai 2026 — Brief sub-agent et accès vault : cause-racine empirique

Le pattern brief-then-direct n'est pas qu'une optimisation tokens : c'est une **nécessité structurelle**. Vérifié empiriquement (Chantier A étape 2b, 27 mai 2026) : le `mcp__forge-brain__*` du `tools:`/`allowed-tools:` d'un sub-agent est **décoratif** — le serveur MCP n'est PAS connecté dans son contexte (`No such tool available`). Un sub-agent à qui on ordonne « lire les canoniques via MCP » fallback sur `cat`/`find`/`grep`/`Read` du vault → viole la doctrine MCP-only.

**Règle pour skill-creator** : ne JAMAIS écrire « lis via MCP » dans le body d'un creator. Écrire « le contenu canonique te vient inline dans le brief ; sinon ESCALADE ; jamais cat/find/grep/Read le vault ». Filet MCP subordonné à l'escalade.

Enforcement structurel : hook `vault-cat-guard.py` (PreToolUse Bash|Read) bloque l'accès brut au vault. Voir [[hook-intercepte-mcp-et-read-tools]] (preuve que PreToolUse intercepte MCP + Read) et [[pattern-mcp-brief-then-direct]] (cause-racine complète).


---

## AJOUT 26 mai 2026 — Pattern eval Anthropic (skills critiques)

Plugin officiel `anthropics/claude-plugins-official/plugins/skill-creator` introduit une infra eval A/B absente de forge. Détails complets : [[eval-pattern-anthropic-skill-creator]].

### Architecture A/B

```
<skill-name>-workspace/
└── iteration-1/
    ├── eval-name/
    │   ├── with_skill/outputs/      # Run AVEC la skill
    │   ├── without_skill/outputs/   # Run SANS (baseline)
    │   ├── grading.json             # assertions[] passed + evidence
    │   └── timing.json              # tokens + duration_ms
    └── benchmark.json               # agrégat
```

### Workflow itératif (5 étapes)

1. Spawner simultanément runs `with_skill` ET `baseline`
2. Rédiger assertions pendant les runs
3. Grader → agréger → analyser (`benchmark.json`)
4. Lire `feedback.json` → améliorer skill
5. Recommencer jusqu'à convergence

### Quand utiliser

**Skills CRITIQUES uniquement (5-6 max)** — pas systématique. Critères : skill réutilisée cross-repos, skill de scaffolding haut-impact, skill sécu. Pour skills basiques : pas d'eval formelle.

### Gap mesurable forge

`outcomes-grader` + `outcomes-test` forge = notation d'un livrable contre RUBRIC.md → **évaluation ponctuelle**. Pattern Anthropic = **benchmark itératif A/B** avec baseline explicite, timing, et boucle d'optimisation. Gap = pas de mesure de delta avant/après skill.

### Décision forge : PAS de skill `/skill-eval`

`run_loop.py` + viewer HTML = dépendances Python lourdes + maintenance. Pour skills critiques (5-6), faire l'éval **manuellement** en suivant ce pattern lors de `/skill-evolve`. Si forge passe à 100+ skills → reconsidérer.

---

## AJOUT 27 mai 2026 — Pattern "skill qui propose un diff à valider"

Une skill de capitalisation (ou toute skill qui produit du contenu durable) peut PROPOSER des blocs prêts-à-écrire (diff visible) au lieu de demander à l'utilisateur de tout rédiger. Mais l'écriture reste sous gate humaine explicite, item par item.

### Le pattern

1. Détecter les items capitalisables (après filtre anti-bruit).
2. Vérifier les doublons (`search_brain`) AVANT de proposer — doublon → bloc d'AMENDEMENT (`read_note` + passage à ajouter), pas une création.
3. Générer le bloc prêt-à-écrire au format cible (feedback MEMORY.md / note vault Obsidian / ADR).
4. Présenter chaque bloc : type + chemin cible + contenu, puis `[v]alider / [m]odifier / [i]gnorer`.
5. Écrire SEULEMENT après validation explicite.

### Pourquoi ce pattern (vs écriture auto)

Importe la COUVERTURE (proposer auto, rattraper ce qu'on oublie de capitaliser) sans céder le CONTRÔLE (humain valide avant écriture). La proposition réduit l'effort cognitif sans retirer la décision. Différence clé vs un background review qui écrit en silence : le diff est relu, jamais un overwrite silencieux. Anti sur-généralisation : 1 occurrence = item ponctuel, jamais une "règle". "Rien à proposer" est une réponse honnête valide.

Référence d'implémentation : skill `done` (étapes 3 génération de blocs + 4 boucle de validation). Croisement Phase 4 Hermes.

### Corollaire — skill de jugement LLM n'est pas testable unitairement

Une skill qui orchestre du jugement LLM (métacognition, capitalisation, arbitrage) n'a pas de test unitaire pertinent : un smoke test ne validerait que le parsing YAML, pas la skill. La validation se fait par **exécution réelle sur un cas représentatif** (ex : lancer `/done` sur une session ayant produit ≥1 apprentissage, vérifier que les blocs proposés sont corrects et que rien n'est écrit sans validation). Ce n'est pas de la dette tracée — c'est un choix de design assumé. Distinguer du code déterministe (scripts/ de skill, hooks, MCP) qui lui doit être testé, avec ratio adverse pour les composants critiques.


---

## AJOUT 5 juin 2026 — Étapes séquentielles obligatoires → checklist Tasks natif (anti-oubli)

Quand une skill enchaîne des **étapes séquentielles dont aucune ne doit être sautée** (questionnaire multi-blocs, pipeline de phases, checklist de validation), piloter la progression avec le système **Tasks natif** plutôt que de confier l'ordre au seul fil de raisonnement.

### Mécanique

```
TaskCreate(1 tâche par étape)  →  statut pending
TaskUpdate(étape N)            →  in_progress en débutant
TaskUpdate(étape N)            →  completed AVANT de passer à N+1
```

Ne jamais avancer à l'étape N+1 tant que N n'est pas `completed`. Dépendances explicites via `addBlockedBy` si l'ordre est strict.

### Pourquoi

Opus 4.8 **interprète littéralement et ne généralise pas seul** : il n'infère pas « applique cette étape aussi aux suivantes » et peut sauter un bloc d'un questionnaire long si rien ne matérialise la checklist. La tâche cochée est le signal explicite qui force le pas-à-pas. (Remplace l'ancien `TodoWrite`, déprécié depuis Opus 4.8.)

### Quand l'appliquer

- ✅ Skill-questionnaire (ex `loop-forge` 9 blocs, `spec` interview) — 1 tâche par bloc
- ✅ Skill-pipeline à phases vérifiables (audit par cluster, vagues parallèles)
- ❌ Skill mono-action (1 transformation, 1 lookup) — la checklist est du bruit

Consolide ce qui était dispersé (`audit-puis-vagues-paralleles`, `cowork-skills-reliability` principe #9 « checklist obligatoire si la skill saute des étapes », changelog Opus 4.8). Réf : [[concevoir-loops-travail]] (cas d'usage `loop-forge`).

## AJOUT 27 mai 2026 — Résolution de path dans une skill : `git rev-parse`, jamais `${CLAUDE_PROJECT_DIR}`

Quand une skill doit résoudre la racine du repo (pour cibler `<repo>/memory/`, `<repo>/docs/`, etc.) dans un bloc Bash, le mécanisme correct est :

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
```

**JAMAIS `${CLAUDE_PROJECT_DIR}`** : cette variable du harness est **vide dans le shell lancé par une skill** (vérifié empiriquement 27 mai : `echo "[$CLAUDE_PROJECT_DIR]"` → `[]`). Elle n'est peuplée que dans la string `command` de settings.json (expansion harness), pas dans l'environnement du process. Utiliser `${CLAUDE_PROJECT_DIR}/memory` dans une skill produit un chemin `/memory` faux et silencieux.

Table complète des 4 contextes (skill / hook / settings / .mcp.json) avec preuve par ligne : [[resolution-path-3-contextes]].

Appliqué 27 mai : skills `/done` et `/recap` migrées vers `$(git rev-parse --show-toplevel)/memory` (chantier mémoire portable, cf [[architecture-decision-memoire-portable-import]]).


---

## AJOUT 7 juin 2026 — SkillsBench (chiffres vérifiés) : une skill curée vaut un upgrade de modèle

Source : **SkillsBench** — *Benchmarking How Well Agent Skills Work Across Diverse Tasks*, [arXiv:2602.12670](https://arxiv.org/abs/2602.12670) (soumis 13 fév 2026, v3 13 mars 2026, **arXiv-only cs.AI — aucune venue confirmée**). 84 tâches / 11 domaines / 7 configs modèle-agent / 7 308 trajectoires. Stanford/CMU/Berkeley/Oxford/BenchFlow. Vérifié source primaire le 7 juin 2026 (Check YYMM + titre + venue via skill `arxiv-verification`).

### Chiffres décisionnels (vérifiés)

- **Skills curées = +16,2 pp de pass rate moyen** (verbatim abstract : « Curated Skills raise average pass rate by 16.2 percentage points »), range +13,6 à +23,3 pp selon la config (gain normalisé ~21,5 %). Forte variance → l'efficacité d'une skill dépend du couple modèle-agent, pas uniforme.
- **Argument massue (corps du papier) : Haiku 4.5 + Skills (27,7 %) > Opus 4.5 SANS Skills (22,0 %).** Un petit modèle + la bonne connaissance procédurale dépasse un gros modèle sans guidance. → **une skill bien construite vaut mieux qu'un upgrade de tier de modèle** (implication coût/déploiement majeure).
- **Claude Code + Opus 4.5 = meilleur gain (+23,3 pp)** — intégration native de la spec Agent Skills.
- **Best config absolue** : Gemini CLI + Gemini 3 Flash, 48,7 % pass rate avec Skills.
- **Résolution L0→L3** : le plus gros gain vient de L2→L3 (ajout d'exemples de code exécutables + ressources de référence). Full Skills L3 = 45,5 % vs 16,4 % sans, quand le contexte suffit. → **valide scripts/ + references/ comme leviers de performance, pas juste d'organisation.**

### Skills auto-générées par le modèle = inefficaces (–1,3 pp)

Quand un modèle génère sa propre connaissance procédurale avant de résoudre : **–1,3 pp en moyenne** vs baseline sans skill. Seul Opus 4.6 progresse (+1,4 pp) ; Codex+GPT-5.2 régresse (–5,6 pp). → **Une skill efficace exige une expertise humaine curée que le modèle ne sait pas auto-générer fiablement.** C'est la justification structurelle d'un workflow interview + evals A/B (skill-creator) plutôt que « demande à Claude d'écrire une skill ».

### Convergence avec la formule directive

Cohérent avec le finding Seleznov (community research, 650 trials, Fisher's exact + logistic regression — **non Anthropic-officiel, non vérifié primaire ici**) : description directive ~100 % activation vs ~77 % passive vs ~50 % non-optimisée. La convergence SkillsBench (benchmark) + Seleznov (community) + doctrine « pushy description » Anthropic est forte sur l'activation ; le step-following (exécution) n'a pas été testé au même niveau de rigueur.

**Source de cet ajout** : réconciliation du rapport `Important/skill.md` (supprimé après absorption, 7 juin). Le rapport était ~85 % subsumé (anatomie skill-creator, matrice 3 environnements, checklist 6 dimensions, question set 3 rounds déjà présents) ; seuls les chiffres SkillsBench précis manquaient. Chiffres vérifiés à la source avant propagation (cf [[feedback_lire_fichier_entier_avant_verdict]] + skill `arxiv-verification`).
