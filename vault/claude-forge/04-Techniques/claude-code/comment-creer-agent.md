---
titre: "Comment créer un agent Claude Code parfait"
resume: "Note canonique pour créer un agent Claude Code — frontmatter, critère d'existence d'un subagent, 6 niveaux d'enforcement, doctrine Sonnet/Opus, nesting depth 3, et interdiction absolue de contourner delegate-guard."
aliases:
  - "comment creer un agent"
  - "creer subagent claude code"
  - "best practices agents"
  - "sonnet opus split agents"
  - "frontmatter agent effort model"
  - "2-agent justin young"
  - "doctrine agents forge"
  - "permissionmode-enum-valid-values"
  - "convention couleurs agents"
type: technique
auteur: claude
derniere-maj: 2026-09-05
sources:
  - "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents"
  - "https://code.claude.com/docs/en/sub-agents"
  - "https://code.claude.com/docs/en/agent-sdk/subagents"
  - "Justin Young (MTS Anthropic) — Initializer + Coding agent (sans split modèles)"
  - "Cat Wu — Code with Claude London 19 mai 2026"
  - "Brad Abrams — Code with Claude SF 6 mai 2026 (Advisor Strategy)"
  - "Böckeler — martinfowler.com/articles/harness-engineering.html (2 avril 2026)"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/agents"
  - "#doctrine/2026"
---
# Comment créer un agent Claude Code parfait

> Note canonique forge — création d'agents selon doctrine Anthropic + Justin Young + Cat Wu + Brad Abrams + Böckeler/Fowler.

---

> ⚠️ **Ordre canonique pour TOUTE création/modification d'agent** : suivre A→B→C→D→E (analyser réel → lire canoniques EN ENTIER → croiser → plan d'écarts → exécuter). Cf [[methode-analyser-repo]] section **ORDRE CANONIQUE**. Pas de prescription avant analyse du réel.

## QUOI — Définition

**Agent Claude Code** = sous-instance Claude spécialisée par un fichier `.claude/agents/<nom>.md`, avec frontmatter contrôlant son modèle, ses outils, son contexte, ses permissions. Invoqué via le `Agent` tool depuis la session principale.

**Concept "Agent = Model + Harness"** :
- Popularisé par **Mitchell Hashimoto** (5 février 2026, [mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey)) — terme "harness engineering"
- Formalisé par **LangChain**
- Repris par **Birgitta Böckeler** (Thoughtworks, 2 avril 2026, [martinfowler.com/articles/harness-engineering.html](https://martinfowler.com/articles/harness-engineering.html))
- Verbatim Böckeler : "the harness is everything in an AI agent **except the model itself**" — guides steer before action, sensors catch problems after

Le **harness** = tout ce qui n'est pas le modèle : prompt système, outils disponibles, hooks, validation, état partagé.

**Stat harness > modèle** :
- LangChain : **52.8% → 66.5%** Terminal Bench avec **harness changes seuls**. Source : **Vivek Trivedy, LangChain blog 17 février 2026** ([langchain.com/blog/improving-deep-agents-with-harness-engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)). Modèle = **GPT-5.2-Codex** (pas Claude). Böckeler 2 avril 2026 cite ce résultat sans le revendiquer.
- ForgeCode Terminal-Bench 2.0 ≈ **79.8%** (Nicolas Bustamante — [nicolasbustamante.com/blog/model-harness-fit](https://nicolasbustamante.com/blog/model-harness-fit)). Comparaison à Claude Code et spread "+21.8 pts" **non sourcés directement chez Addy Osmani** ([addyosmani.com/blog/agent-harness-engineering/](https://addyosmani.com/blog/agent-harness-engineering/) qualitatif uniquement).

Le harness compte autant que le modèle.

---

## POURQUOI — Le problème résolu

Sans agents spécialisés, la session principale fait tout :
- **Pollution contexte** — recherches massives consomment le contexte principal
- **Pas de boundaries** — pas de restriction d'outils par rôle
- **Pas de modèle adapté** — code review = Sonnet, mais jugement archi = Opus
- **Pas de parallélisation** — 1 thread principal séquentiel

Avec agents :
- **Délégation focalisée** — 1 rôle = 1 agent
- **Boundaries explicites** (`allowed-tools`, `disallowedTools`)
- **Modèles adaptés** (Sonnet exécution, Opus jugement — doctrine forge)
- **Parallélisation** (multi-agents simultanés)

---

## COMMENT — Frontmatter complet

### Frontmatter de référence

```yaml
---
name: <nom-exact-du-fichier-sans-md>
description: <trigger directive 3e personne, max ~500 chars>
tools: <outils autorisés, séparés par virgule>
model: sonnet | opus | haiku
effort: low | medium | high | xhigh
color: red | orange | yellow | green | blue | purple | cyan | pink
# memory: project  # OPTIONNEL : besoin durable, scope et revision explicites
permissionMode: acceptEdits | auto | plan | default | dontAsk | bypassPermissions
disallowedTools: <outils interdits, ex Write, Edit>
skills: <skills mobilisées, optionnel>
maxTurns: <nombre, optionnel>
---
```

### Frontmatter vs body : alignement obligatoire

**Le frontmatter fait foi. Le body ne doit JAMAIS le contredire.**

- Un champ frontmatter (`effort`, `model`, `memory`, `permissionMode`, etc.) est la source de vérité unique pour sa valeur.
- Le body de l'agent NE DOIT PAS re-commenter ni re-justifier un champ frontmatter (ex : ligne `effort: xhigh — la pensée adversariale exige une profondeur maximale`). C'est à la fois redondant et une source de drift quand l'un évolue sans l'autre.
- Double faute classique : le body affirme une valeur (`xhigh`) que le frontmatter dément (`high`). Le composant se contredit lui-même.
- Le **pourquoi** d'un choix de frontmatter vit dans le vault (cette note, CLAUDE.md), pas dans le body de l'agent — cf [[feedback_pas_de_meta_commentaire_doctrine]]. Le hook `meta-commentary-detector` bloque ce type de commentaire doctrinal.

**Règle de vérification** : après toute modification d'agent, `grep` la valeur du champ frontmatter dans le body. Si elle apparaît avec une justification → la supprimer. Le frontmatter parle, le body se tait.

Cas réel 27 mai 2026 : `devils-advocate.md` avait `effort: high` en frontmatter mais le body affirmait `effort: xhigh`. Fix = suppression des 2 lignes de body, frontmatter conservé.

### Règles frontmatter critiques

1. **`name`** = nom du fichier sans `.md`, kebab-case
2. **`description`** = trigger directive 3e personne (comme skills)
3. **`model`** — les alias `sonnet`/`opus`/`haiku` pointent vers la génération courante, PAS vers un ID figé :
   - `sonnet` → génération Sonnet courante (exécution)
   - `opus` → génération Opus courante (jugement)
   - `haiku` → génération Haiku courante (tâches courtes ultra-rapides)
   - **Préférer l'alias à l'ID complet** dans un agent : l'alias survit aux montées de version, l'ID complet meurt silencieusement. Un agent qui épingle un ID de génération révolue continuera de « marcher » longtemps après la disparition du modèle, en repli invisible. IDs exacts d'une génération donnée : les vérifier dans les docs, jamais de mémoire. Doctrine de repli forge : [[feedback_preference_modele_opus]].
4. **`effort`** :
   - Options acceptées par le produit : `low`, `medium`, `high`, `xhigh`, `max`
   - "Available levels depend on the model"
   - **Doctrine forge** : `high` par défaut ; `medium`/`low` pour le mécanique ; `xhigh` seulement après gain mesuré ; **`max` JAMAIS en frontmatter** (coût massif, overthinking observé). `max` reste une valeur produit valide — c'est la doctrine forge qui l'exclut d'un composant versionné.
   - **Le réglage dépend de la génération** : `xhigh` était calibré sur les Opus 4.7/4.8 coding-agentic ; `high` est le bon défaut sur les générations suivantes. Grille par modèle : [[effort-opus-47-doctrine-anthropic-2026]] et [[doctrine-par-modele-opus5-fable5]]. Le sweep d'effort est à REFAIRE à chaque changement de génération — un réglage hérité ne se transpose pas.
5. **Mémoire persistante** = absente par défaut. L'activer seulement pour un apprentissage durable propre à l'agent, avec scope et révision explicites
6. **`permissionMode`** = optionnel ; le déclarer quand il clarifie un profil de risque :
   - `acceptEdits` pour créateurs (subagent-creator, skill-creator, hook-creator, claudemd-creator)
   - `auto` pour exécutants (dev, code-reviewer, test-writer)
   - `plan` pour agents qui doivent **toujours passer par un plan validé** avant action
7. **`disallowedTools: Write, Edit`** sur agents read-only (force délégation)

### Politique modèles forge (doctrine inférée cohérente avec Anthropic)

> **Important honnêteté** : la politique "Sonnet exécution / Opus jugement" est une **doctrine forge inférée** par pattern observé en sessions. **Cohérente avec** :
> - **Cat Wu** (Code with Claude London 19 mai 2026) : conseils de délégation et de brief complet, introduction du niveau `xhigh` (le conseil a survécu aux générations suivantes, le numéro de version non)
> - **Brad Abrams** (Code with Claude SF 6 mai 2026, Advisor Strategy talk) : executor model (Haiku) + advisor model (Opus implicite)
>
> Aucune doctrine Anthropic verbatim n'énonce explicitement "Sonnet = exécution, Opus = jugement". C'est une généralisation forge.

| Modèle | Rôle forge | Exemples |
|--------|-----------|----------|
| **Sonnet** | Exécution | dev, code-reviewer, test-writer, python-dev |
| **Opus** | Jugement | architect, devils-advocate, project-auditor, outcomes-grader |
| **Haiku** | Checks rapides | classifiers, anti-rationalization |

### Convention couleurs forge (cross-repo)

> **Note** : convention forge perso, pas Anthropic. Anthropic accepte `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` comme valeurs valides (verbatim docs frontmatter), mais ne prescrit pas leur usage.

| Couleur | Catégorie forge |
|---------|-----------|
| **red** | Sécurité / Critique (devils-advocate, audits sécu) |
| **orange** | Review / Validation (code review, optim SQL) |
| **yellow** | Test / Évaluation / Debug |
| **green** | Développement (implem features) |
| **blue** | Architecture / Design (architect, API design) |
| **purple** | Analyse / Stratégie (codebase analyzer, schema mapping) |
| **cyan** | Infra / Maintenance (refactoring, migration) |
| **pink** | Meta-créateurs (skill-creator, subagent-creator — forge only) |

**Règle cross-repo forge** : même rôle = même couleur sur TOUS les repos. Un `architect` est toujours `blue`.

---

## QUAND — Critère d'application

### Le test en une phrase (source: research LLM juin 2026)

> « Est-ce que cette tâche a besoin d'un contexte frais isolé OU de tourner en parallèle, ET n'a pas besoin de poser des questions ni du contexte de la conversation ? » Si non → ce n'est pas un subagent.

Un subagent résout exactement **deux** problèmes :
1. **Isolation de contexte** — sortir le travail bruyant (lire 40 fichiers, explorer) du transcript principal. Le subagent renvoie un résumé, pas le détail.
2. **Parallélisme** — lancer plusieurs workers simultanément.

**NE PAS créer de subagent quand :**
- La tâche doit poser des questions → `AskUserQuestion` non disponible en subagent (filtré, issues #12890 #18721 #20275)
- La tâche a besoin du contexte de conversation → le subagent démarre vierge
- La tâche a besoin du MCP → non garanti (`No such tool available` fréquent)
- Juste pour "faire propre" → une skill ou section CLAUDE.md suffit, sans les inconvénients
- Workers doivent communiquer entre eux → Agent Teams, pas subagents
- Comportement déterministe obligatoire → hook, pas subagent

### Créer un agent quand :
- Un **rôle dev récurrent** émerge (architect, dev-feature, code-reviewer, test-writer, debugger, sécu-auditor)
- Une **boundary** est nécessaire (lecture seule, outils restreints, modèle dédié)
- **Parallélisation** souhaitée (multi-agents en parallèle)
- **Délégation focalisée** pour éviter pollution contexte

### NE PAS créer un agent quand :
- Pour une procédure réutilisable → **Skill**
- Pour un accès données → **MCP**
- Pour une règle 100% → **Hook**
- Si la session principale suffit (S/M tasks simples)

### Anti-pattern majeur : agent CTO orchestrateur
- ❌ **JAMAIS d'agent orchestrateur** — la session principale orchestre via rules (cf [[feedback_no_cto_agent]])

---

## WORKFLOW — Création étape par étape

### Étape 1 — Identifier le rôle
Lister les rôles dev récurrents du repo. Chaque rôle distinct = candidat agent.

### Étape 2 — Définir boundaries
- Outils nécessaires (`tools`)
- Outils interdits (`disallowedTools`)
- Skills mobilisées (`skills`)
- Modèle adapté (sonnet/opus/haiku)
- Effort niveau (high défaut)

### Étape 3 — Déléguer à `subagent-creator`

> ⚠️ **Pivot 6 juin 2026** : l'ancien agent `agent-creator` est devenu la **skill** `subagent-creator` (`.claude/skills/subagent-creator/`). Invoquer via `Skill(subagent-creator)` depuis la session principale. `cc-agents-ref` supprimée : la doctrine vit dans `subagent-creator` + cette note.

**Le hook `delegate-guard.py` BLOQUE l'édition directe de `.claude/agents/*.md`** (exit 2), et route vers `subagent-creator`. Vérifié sur le code le 5 septembre 2026 : `delegate-guard.py` est branché via le dispatcher `pre-write-guards.py` (PreToolUse `Write|Edit|MultiEdit`) — il n'apparaît pas directement dans `settings.json`, ce qui a déjà fait conclure à tort qu'il était débranché. Le blocage est réel et il est dur.

### Étape 4 — Référencer skills dans le body
**Si tu mets une skill dans `skills:` frontmatter, tu DOIS la référencer dans le body avec instructions d'usage.** Sinon orpheline = jamais activée (cf [[feedback_skills_referenced_in_body]]).

### Étape 5 — Tester en isolation
Invoquer l'agent depuis session vierge. Vérifier :
- Trigger marche (description directive efficace)
- Outils suffisants (rien ne manque)
- Outils restreints respectés (disallowedTools)

### Étape 6 — DA si livrable majeur (CONDITIONNEL)
Côté forge : `devils-advocate` UNIQUEMENT si livrable majeur (agent orchestrant, agent sécu, agent cross-repos). Doctrine 22 mai : pas de gates systématiques (cf [[raisonnement-22mai-doctrine-vs-enforcement]] + [[feedback_pipeline_quality_gates]]). DA reste **conditionnel ciblé**.

---

## APPELS — Composants mobilisés

- [[comment-creer-skill]] — skills injectées via `skills:` frontmatter
- [[comment-creer-hook]] — hooks qui encadrent les agents
- [[comment-ecrire-claudemd]] — où mentionner les agents du repo
- [[workflow-claude-code-optimal]] — comment agents s'inscrivent dans le workflow
- [[methode-analyser-repo]] — méthode pour identifier les rôles → agents
- [[multi-agent-handoff-loss-pattern]] — pourquoi le single-agent d'abord : le threshold 45 % est le seuil de rentabilité du handoff (séquentiel dégrade, error amplification 17x vs 4.4x)

---

## POURQUOI un subagent n'invoque pas ses skills — 3 causes cumulées

Le problème le plus fréquent. Source : research LLM juin 2026 + empirique forge.

### Cause 1 — `Skill` absent de `tools:` (mécanique)
Sans l'outil `Skill` dans `tools:`, le subagent **ne peut physiquement pas** invoquer de skill. À vérifier en premier.

### Cause 2 — `skills:` précharge, ne force pas
Le champ `skills:` injecte le **contenu complet** des skills de projet au démarrage — ce préchargement n'est toutefois pas une invocation forcée. "Description présente" ≠ "skill invoquée". L'invocation reste probabiliste, comme sur le thread principal.

### Cause 3 — Le subagent préfère le raccourci direct
Si le subagent a tous les outils pour produire le résultat sans passer par la skill (Bash, connaissance propre), il le fait. La skill devient un détour optionnel qu'il s'autorise à zapper.

### Verdict
`skills:` dans le frontmatter ne garantit jamais l'invocation. Pour la forcer → voir section enforcement ci-dessous.

---

## Enforcement — 6 niveaux (du mou au dur)

### Niveau 1 — Ordre impératif numéroté (indispensable, probabiliste)
L'invocation de la skill = **ÉTAPE 1 bloquante** dans le body avec raison explicite :
> « ÉTAPE 1 — OBLIGATOIRE AVANT TOUT. Invoque la skill `xxx` (outil Skill). Ne génère rien avant. Raison : sans elle tu produis du format obsolète qui ne se déclenche jamais. »

### Niveau 2 — Critique inliné dans le body (le plus fiable côté contenu)
**Si une connaissance DOIT toujours être présente, ne la mets pas dans une skill zappable — mets-la dans le system prompt.** Le body de l'agent est TOUJOURS chargé ; une skill est un détour optionnel. Les 5-6 règles non-négociables vivent inline ; la skill devient la référence détaillée.

### Niveau 3 — Script-output gating
Un script de validation que l'agent doit lancer ; la sortie le bloque. La règle non-négociable vit dans le code, pas dans la prose. Déterministe.

### Niveau 4 — Hook SubagentStop (enforcement dur, CLI uniquement)
Se déclenche quand le subagent finit. Parse le transcript JSONL pour détecter si la skill a été invoquée. Exit 0 + JSON `{"decision":"block","reason":"..."}` pour forcer la continuation.

```python
import json, sys, os
data = json.load(sys.stdin)
if data.get("stop_hook_active"):   # anti-boucle infinie : OBLIGATOIRE
    sys.exit(0)
tp = data.get("agent_transcript_path") or data.get("transcript_path")
used = False
try:
    with open(os.path.expanduser(tp)) as f:
        for line in f:
            if '"name": "Skill"' in line and "ma-skill" in line:
                used = True
    if not used:
        print(json.dumps({"decision": "block",
          "reason": "Tu n'as pas invoqué ma-skill. Invoque-la via l'outil Skill puis termine."}))
        sys.exit(0)   # exit 0 + JSON (PAS exit 2, sinon JSON ignoré)
except Exception:
    pass
sys.exit(0)
```

**Pièges hooks critiques :**
- `exit 2` bloque PreToolUse ; **`exit 1` ne bloque JAMAIS**
- Pour Stop/SubagentStop : **exit 0 + JSON** `decision:block` (exit 2 = JSON ignoré)
- Toujours vérifier `stop_hook_active` → anti-boucle infinie (cap natif 8 blocages)
- Bug #10412 : Stop hooks exit 2 via plugin échouent → installer depuis `.claude/hooks/`
- PostToolUse `matcher:"Skill"` ne se déclenche pas fiablement (issue #43630) → parser transcript

### Niveau 5 — UserPromptSubmit (rappel injecté)
Hook UserPromptSubmit imprime un rappel d'activation sur stdout (ajouté au contexte) avant que le modèle agisse.

### Niveau 6 — `disallowedTools` (couper les raccourcis)
Si l'agent zappe la skill parce qu'il fait le travail directement → restreindre ses outils (`disallowedTools: Bash`) pour que la skill soit le seul chemin viable.

---

## Héritage — Ce qu'un subagent reçoit (et ne reçoit PAS)

| Élément | Hérité ? |
|---|---|
| Contexte de conversation | ❌ Contexte frais — ne reçoit que le brief passé |
| Skills | ✅ `skills:` précharge le contenu complet des skills de projet déclarées |
| Outil `Skill` | ❌ Doit être dans `tools:` sinon impossible mécaniquement |
| Outils (Read, Bash…) | ❌ Définis par `tools:` — sans explicite, comportement variable |
| MCP servers | ⚠️ Instable — souvent « No such tool available » |
| CLAUDE.md / rules | ⚠️ Variable (Explore/Plan sautent CLAUDE.md) |
| AskUserQuestion | ❌ Filtré hors subagents (issues #12890 #18721 #20275) |
| Sous-agents imbriqués | ✅ supportés jusqu'à depth 3 par défaut ; limiter la profondeur et fournir des briefs complets |
| Hooks settings | ✅ S'appliquent (SubagentStart/SubagentStop existent) |
| Mémoire (`memory:`) | ✅ Persiste entre sessions |

**Deux règles d'or :**
- Vault = thread principal ; inline = subagent (MCP non garanti dans un subagent)
- Interview sur le thread principal → réponses dans le brief → subagent exécute sans questions

---

## Checklist subagent quasi-parfait

**Décision (avant de créer)**
- [ ] Besoin d'isolation de contexte OU de parallélisme ?
- [ ] Pas besoin de poser des questions (sinon → skill/thread principal) ?
- [ ] Pas besoin du MCP ni du contexte conversation (sinon → brief inline) ?

**Frontmatter**
- [ ] `name` kebab-case = nom du fichier sans `.md`
- [ ] `description` directive 3e personne — déclencheur de délégation
- [ ] `tools:` explicite — inclut `Skill` si l'agent doit invoquer des skills
- [ ] `model` adapté (haiku explore, sonnet implémentation, opus orchestration/jugement), déclaré par ALIAS et non par ID figé
- [ ] `effort` sans `max` — `high` par défaut
- [ ] `disallowedTools` pour couper les raccourcis qui font zapper les skills
- [ ] mémoire persistante absente ou justifiée ; permissions au moindre privilège

**Body / system prompt**
- [ ] Responsabilité unique
- [ ] Workflow impératif numéroté, étapes bloquantes
- [ ] Invocation des skills = ÉTAPE 1 explicite avec outil Skill + raison
- [ ] Critique inliné dans le body (pas seulement dans une skill zappable)
- [ ] Étapes à sortie visible (anti-skip validation)
- [ ] Body court + skills courtes (injectées en entier → anti-saturation contexte)
- [ ] Expliquer le pourquoi ; majuscules réservées aux 1-2 étapes fragiles

**Fiabilité d'invocation des skills**
- [ ] `Skill` dans `tools:` (sinon impossible mécaniquement)
- [ ] Ordre impératif dans le body
- [ ] Hook SubagentStop qui parse le transcript (exit 0 + JSON decision:block)
- [ ] `stop_hook_active` vérifié (anti-boucle)

**Accès / MCP / questions**
- [ ] Pas de dépendance MCP dans le subagent → brief inline
- [ ] Pas de questions dans un subagent → interview sur thread principal avant délégation

## OPTIMISATION — 3 niveaux

### Niveau basique
- 1 agent par rôle critique (architect, dev, reviewer)
- Tous Sonnet effort high
- mémoire persistante partout sans besoin ni révision
- `permissionMode: acceptEdits`

### Niveau avancé
- Sonnet/Opus split appliqué (jugement vs exécution, doctrine forge)
- `disallowedTools` sur read-only (project-auditor, code-reviewer)
- Skills injectées + référencées dans body
- Convention couleurs cross-repo forge

### Niveau expert : 2-agent architecture Justin Young (Anthropic)

**Pattern Justin Young — verbatim source officielle** :
Source : [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

```
┌─────────────────┐         ┌──────────────────┐
│  Initializer    │────────►│  Coding Agent    │
│  Agent          │  spec   │  (implementation)│
└─────────────────┘         └──────────────────┘
```

- **Initializer agent** : reçoit un prompt initial différent, produit la spec/contexte structuré
- **Coding agent** : reçoit la spec, implémente
- **Footnote 1 verbatim** : *"The system prompt, set of tools, and overall agent harness was otherwise identical"*
- **Pas de split modèles** dans l'article — seul Opus 4.5 mentionné comme baseline failure sans harness
- Le seul **différentiateur** entre les 2 agents = leurs initial user prompts

> ⚠️ Erreur historique forge : avant audit 23 mai 2026, cette doctrine était présentée comme "Init = Opus, Coding = Sonnet". **Extrapolation forge non sourcée**. Le 2-agent architecture est canonique, le split modèles n'est pas chez Justin Young — cohérent avec doctrine forge Sonnet/Opus split via d'autres sources (Cat Wu, Brad Abrams) mais pas verbatim Justin Young.

Démontré sur tâches **long-running** où la séparation init / exécution améliore qualité.

### Pattern Advisor Strategy (Brad Abrams, Anthropic Product Lead Claude)

Source : [Code with Claude SF — "Caching, harnesses, and advisors: Building on Claude at GitHub scale"](https://claude.com/code-with-claude/session/sf-caching-harnesses-and-advisors-building-on-claude-at-github-scale) (talk avec Mario Rodriguez, GitHub CPO).

```
┌──────────────┐  query   ┌────────────────┐
│  Executor    │─────────►│  Advisor       │
│  (Haiku)     │◄─────────│  (Opus)        │
│              │  advice  │                │
└──────────────┘          └────────────────┘
```

- **Executor model** : smaller (ex: Haiku), exécute la majorité des appels
- **Advisor model** : larger (Opus), consulté ponctuellement quand l'executor demande conseil
- **Verbatim Brad Abrams** : *"We get close to Opus-level intelligence at much lower prices because we're being very conservative about the tokens that advisor actually sends"*
- Pattern utilisé chez **GitHub Copilot** à scale

→ Pas un chiffre "5×" comme parfois cité (coquille propagée depuis live blog Simon Willison "Angela Kiang" → "Angela Jiang"). Le verbatim Abrams ne donne pas de multiplicateur précis.

---

## POURQUOI CETTE OPTIM — Gain mesurable

| Optim | Gain |
|-------|------|
| Sonnet/Opus split | Coût ~5× réduit sur exécution (Sonnet), qualité préservée sur jugement (Opus) — observation forge |
| 2-agent architecture Justin Young | Long-running tasks : qualité préservée par séparation init/coding |
| Advisor Strategy (Brad Abrams) | "Close to Opus-level intelligence at much lower prices" (verbatim) — pattern GitHub Copilot |
| LangChain harness changes | 52.8% → 66.5% Terminal Bench avec même modèle, harness seul (Vivek Trivedy 17 fév 2026, GPT-5.2-Codex) |
| `disallowedTools` read-only | Empêche modifications accidentelles, force délégation |
| Skills injectées + référencées | Auto-activation contextualisée, ~0 token gaspillé |

---

## ANTI-PATTERNS

### Architecture
- ❌ **Agent CTO orchestrateur** — session principale orchestre (cf [[feedback_no_cto_agent]])
- ❌ **Agent doc** — pas d'agent dédié à la doc, l'agent qui code update aussi
- ❌ **Agent monolithique** — découper en plusieurs rôles distincts
- ❌ **Agent qui invoque un autre agent (ré-entrance)** : techniquement permis jusqu'à depth 3, mais coûteux et illisible à déboguer. Par défaut, passer par la session principale qui orchestre. Choix d'architecture forge — pas une impossibilité technique.

### Frontmatter
- ❌ **Mémoire persistante par défaut** — accumule des biais et du contexte périmé
- ❌ **Permissions rituelles** — choisir le mode selon le risque réel
- ❌ **`effort: max` en frontmatter** — interdit par la doctrine forge (coût massif, overthinking)
- ❌ **`effort: xhigh` par défaut** — step-up mesuré uniquement
- ❌ **ID de modèle figé** — préférer l'alias `opus`/`sonnet`/`haiku`, sinon l'agent meurt en silence à la génération suivante
- ❌ **Description en 1ère personne** — toujours 3e personne directive
- ❌ **Pas de `color`** — convention forge

### Skills / tools
- ❌ **Skills dans `skills:` mais pas dans body** = orphelines (cf [[feedback_skills_referenced_in_body]])
- ❌ **`Bash` sur agent orchestrateur** — retirer pour forcer délégation (cf [[feedback_agent_tools_restriction]])
- ❌ **Pas de `disallowedTools` sur read-only** — risque modifs accidentelles

### Comportement
- ❌ **Agent qui commit dans repo externe** sans demande explicite (cf [[feedback_never_commit_foreign_repos]])
- ❌ **Sous-agent qui commit** malgré instruction "pas de commit" en fin de prompt → mettre en TOP en gras (cf [[feedback_subagent_autocommit]])
- ❌ **Sub-agent permissions** : `permissions.allow` toujours non hérité (cf [[reference_subagent_permissions]])
- ❌ **Édit direct `.md` agent** — délégation obligatoire à `subagent-creator` (le hook bloque en exit 2)

---

## ⛔ INTERDIT — contourner `delegate-guard`

**Il n'existe pas de contournement légitime du garde-fou de délégation.** Ni `Write` vers un suffixe temporaire suivi d'un `mv`, ni script Python externe, ni variable d'environnement, ni `Bash` pour échapper au matcher `Write|Edit|MultiEdit`.

Le hook le dit lui-même dans son message de blocage : *« Do NOT attempt to bypass via env vars or external scripts. »* La rule `delegate-to-specialists.md` le redit : « Si le hook bloque, la réponse n'est JAMAIS de le contourner. On corrige le hook ou on invoque la skill. Contourner un garde-fou de scope = anti-pattern absolu. »

> **Correction 5 septembre 2026** — cette note a documenté pendant plusieurs mois un « mécanisme de bypass propre » (écrire un fichier à suffixe temporaire puis le renommer, pour que ni `is_agent_md` ni le matcher ne tirent), présenté comme exploitant la spec du matcher plutôt que la violant. **Cette section était une faute** : une canonique de création de composants enseignait pas à pas comment neutraliser un garde-fou de sécurité. Elle est retirée, sans être effacée de l'historique — elle est archivée ici comme erreur, pas comme technique.

**Le cas réel qu'elle prétendait résoudre** — un creator qui est lui-même le verrou de bootstrap et porte un bug à corriger — se traite autrement :
1. Invoquer la skill créatrice appropriée : `subagent-creator` peut écrire des agents, y compris un autre creator.
2. Si le verrou est authentiquement circulaire (le composant ne peut pas se réparer lui-même), **corriger le hook** pour qu'il exprime l'exception, ou basculer le mode de permission — les deux laissent une trace revue.
3. Jamais un chemin détourné qui laisse le garde-fou intact en apparence et inopérant en fait.

Le principe général : un garde-fou qu'on sait contourner ne protège plus personne, et une doctrine qui documente le contournement le rend routinier. Cf [[delegate-guard-pattern]] et `delegate-to-specialists.md`.

---

## EXEMPLES CONCRETS — Repos externes

### Référence Anthropic
- **`anthropics/claude-code-action`** — workflow d'agent GitHub Action
- **Justin Young 2-agent** : [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (Initializer + Coding, harness identique)
- **Brad Abrams Advisor Strategy** : Code with Claude SF, talk avec GitHub
- **Anthropic team** internalement : +300% PRs équipe sur 3 mois (Noah Zweben, CwC London — verbatim Every : "weekly PR throughput went up 300%, from around 500 in January to roughly 1,150 in March")

### Référence harness
- **LangChain** : 52.8% → 66.5% Terminal Bench (Vivek Trivedy 17 fév 2026, GPT-5.2-Codex)
- **ForgeCode** (Bustamante) : 79.8% Terminal-Bench 2.0
- **Cognition Labs Devin** — harness avancé multi-agents

### Référence Trail of Bits
- [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)
- Anti-rationalization Stop hook : agent Haiku check cop-outs sur la session principale
- 3-tier sandbox boundaries

### Référence Karpathy
- `karpathy/nanochat/.claude/skills/` — Karpathy publie peu d'agents publics, focus skills atomiques

---

## SOURCES — Verbatim avec URLs

### Anthropic officiel
- [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Justin Young 2-agent architecture (initializer + coding, harness identique)
- [code.claude.com/docs/en/agent-sdk/subagents](https://code.claude.com/docs/en/agent-sdk/subagents) — frontmatter spec, effort levels
- [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) — créer custom subagents
- [Code with Claude SF — Caching/Harnesses/Advisors](https://claude.com/code-with-claude/session/sf-caching-harnesses-and-advisors-building-on-claude-at-github-scale) — Brad Abrams + Mario Rodriguez

### Code with Claude London 19 mai 2026
- **Cat Wu** (Head of Product Claude Code) : tips de délégation et brief complet, introduction du niveau `xhigh`
- **Noah Zweben** : "weekly PR throughput went up 300%, from around 500 in January to roughly 1,150 in March"
- **Lisa Crofoot** : "scaffolding holds Claude back" (single source à confirmer)
- **Daisy Hollman** : "You should be running agents overnight" / "red squigglies for agents"
- **Fiona Fung** (Head of Engineering Anthropic) : "Pick your noisiest workflow…and ask if it's still serving its purpose" + "In technical debates, code wins"
- **Jeremy Hadfield** : Dreaming feature

### Code with Claude SF 6-7 mai 2026
- **Erik Schluntz** : Vibe Coding in Prod (PM guidance, leaf nodes, human core, verifiable checkpoints) — "22 000 LOC en 1 jour" est une analogie cognitive, pas une métrique brute
- **Thariq Shihipar** : Agent SDK Workshop, compute allocators verbatim "All of us are becoming these compute allocators now" (ChatPRD How I AI)
- **Brad Abrams** : Advisor Strategy

### Hashimoto / Böckeler / Bustamante
- [mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey) — popularisation "harness engineering" (5 fév 2026)
- [martinfowler.com/articles/harness-engineering.html](https://martinfowler.com/articles/harness-engineering.html) — Böckeler Guides+Sensors 2 avril 2026
- [langchain.com/blog/improving-deep-agents-with-harness-engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering) — Vivek Trivedy 17 fév 2026
- [nicolasbustamante.com/blog/model-harness-fit](https://nicolasbustamante.com/blog/model-harness-fit) — ForgeCode 79.8%
- [addyosmani.com/blog/agent-harness-engineering/](https://addyosmani.com/blog/agent-harness-engineering/) — Addy Osmani qualitatif

---

## Matrice enforcement par environnement (CLI / Desktop / Cowork)

> Source : recherche LLM (Claude.ai juin 2026) + vault empirique forge. Cohérent avec [[cowork-skills-reliability]] section matrice. Numéros d'issues = indicatifs, non vérifiés primaire.

Un agent généré par `subagent-creator` doit adapter ses mécanismes selon l'environnement cible. Cette matrice complète [[cowork-skills-reliability]] côté agents.

| Mécanisme | Claude Code CLI | Code Desktop | Cowork |
|---|---|---|---|
| **Hooks (PreToolUse/PostToolUse)** | ✅ Fiable | ⚠️ Partiel | ❌ Silent no-op |
| **`context: fork` / `agent:` frontmatter** | ⚠️ Ignoré si invoqué via Skill tool | ⚠️ Idem | ⚠️ Idem — utiliser Task tool explicite à la place |
| **MCP local (stdio) dans `tools:`** | ✅ Effectif en session principale | ✅ | ❌ Décoratif en sub-agent ET inaccessible Cowork |
| **MCP remote HTTPS** | ✅ | ✅ | ✅ Seul type viable |
| **`disallowedTools`** | ✅ | ✅ | ✅ |
| **`permissionMode`** | ✅ | ✅ | ✅ |
| **Mémoire persistante** | opt-in | opt-in | opt-in selon support de la plateforme |
| **AskUserQuestion** | ❌ Non dispo en sub-agent (issue #18721) | ❌ Idem | ❌ Idem — ESCALADE vers session principale |

### Stratégie de génération selon la cible

**Si `subagent-creator` génère un agent pour CLI / Code Desktop :**
- Hooks complémentaires ok (PreToolUse guard, PostToolUse validation)
- MCP local (stdio) dans `tools:` ok en session principale
- `context: fork` / `agent:` à éviter si l'agent sera invoqué via Skill tool (ignoré)
- Pattern complet disponible

**Si `subagent-creator` génère un agent pour Cowork :**
- ❌ **Ne pas émettre de hooks** dans la skill/agent générée — silent no-op
- ❌ **Ne pas compter sur MCP stdio** — remote HTTPS uniquement
- ✅ Description directive + script-output gating + AskUserQuestion gate (session principale)
- ✅ Checklist "à voix haute" obligatoire dans l'output pour remplacer les guards déterministes
- ✅ Utiliser Task tool explicite au lieu de `context: fork`

**Rappel universel :**
`AskUserQuestion` n'est jamais disponible dans un sub-agent (CLI, Desktop, Cowork) — pattern ESCALADE obligatoire. Voir section dédiée AJOUT 24 mai 2026.

## GOTCHAS — Pièges observés

### Pièges modèle / effort
- **`effort: max` existe côté produit mais est interdit en frontmatter forge** — coût massif, overthinking observé
- **`xhigh` par défaut = coût massif** — step-up mesuré uniquement, jamais un réglage de confort. Le niveau juste dépend de la génération : cf [[effort-opus-47-doctrine-anthropic-2026]].
- **Un modèle plus littéral demande un scope explicite** — observation forge stable d'une génération à l'autre : être explicite sur le scope et le parallélisme attendu plutôt que compter sur la généralisation
- **Ne jamais épingler un ID de modèle dans un agent** — utiliser l'alias `sonnet`/`opus`/`haiku`. Un ID figé devient faux en silence ; c'est exactement ce qui a laissé des IDs de génération 4.x prescrits dans cette note jusqu'au 5 septembre 2026.

### Pièges permissions
- **agents de plugins** : `hooks`, `mcpServers`, `permissionMode` sont **ignorés pour les agents de plugins** (sécurité) — s'applique uniquement aux agents `.claude/agents/` du repo courant.
- **`permissionMode` optionnel** — utile lorsqu'il rend explicite un profil de risque
- **`permissions.allow`** : non hérité par sub-agents (cf [[reference_subagent_permissions]])
- **Worktree access + MCP tools** : OK depuis v2.1.101

### Pièges memory
- **Mémoire persistante opt-in** — le vault et les décisions projet restent canoniques

### Pièges skills
- **Skills dans `skills:` non référencées dans body** = orphelines, jamais activées (cf [[feedback_skills_referenced_in_body]])

### Pièges environnement / invocation
- **`context: fork` / `agent:` ignorés via Skill tool** — si l'agent est invoqué via le Skill tool (pas directement via Agent tool), ces directives frontmatter sont silencieusement ignorées. Utiliser une instruction explicite `Task tool` dans le body à la place
- **Agent ciblant Cowork** : ne jamais émettre de hooks ni de MCP stdio dans un agent généré pour Cowork — ils sont des no-ops (voir [[cowork-skills-reliability]] matrice enforcement)

### Pièges délégation
- **Édit direct bloqué** par hook `delegate-guard.py` (exit 2) — utiliser `subagent-creator`, jamais un chemin de contournement
- **Sub-agent commit autonome** — mettre "PAS DE COMMIT" en TOP du prompt en gras (cf [[feedback_subagent_autocommit]])
- **Repo externe** : pas de git autonome (cf [[feedback_never_commit_foreign_repos]])
- **Sub-agents bloqués en write cross-repo** — les écritures `SKILL.md`/`agents/*.md`/hooks/`CLAUDE.md` d'un autre repo se font en session principale (le hook lit l'`attributionSkill` de la session principale, pas du transcript sub-agent)

### Pièges Windows
- **Python launcher `py`** dans les hooks référencés par agent (l'alias MS Store intercepte `python` nu)
- **Heredoc Bash Windows** : boucle quoting Git Bash (cf [[erreur-da-heredoc-bash-silencieux]])

### Pièges forge
- **Vault check obligatoire** avant création (cf [[forge-brain-proactive]])
- **DA après création majeure** (cf [[devils-advocate-pipeline]])
- **Convention couleurs cross-repo** stricte (forge)

---

## WIKILINKS

### Notes canoniques sœurs
- [[comment-creer-skill]]
- [[comment-creer-hook]]
- [[comment-ecrire-claudemd]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[mcp-vs-skills-doctrine]]

### Fiches leaders
- [[Justin Young]]
- [[Cat Wu]]
- [[Brad Abrams]]
- [[Noah Zweben]]
- [[Daisy Hollman]]
- [[Jeremy Hadfield]]
- [[Erik Schluntz]]
- [[Birgitta Böckeler]]
- [[Mitchell Hashimoto]]
- [[Addy Osmani]]

### Knowledge / erreurs / refs
- [[feedback_no_cto_agent]]
- [[feedback_skills_referenced_in_body]]
- [[feedback_agent_tools_restriction]]
- [[feedback_subagent_autocommit]]
- [[feedback_never_commit_foreign_repos]]
- [[reference_subagent_permissions]]
- [[erreur-da-heredoc-bash-silencieux]]
- [[erreur-seuils-canoniques-agents-inventes-2026-05-22]] — 4/5 seuils « canoniques » agents cités dans le vault étaient des mythes (extrapolations, confusion). Seuls CLAUDE.md < 200L et SKILL.md < 500L sont vraiment canoniques.

### Forge custom
- [[delegate-guard-pattern]] — le garde-fou de délégation et ses exceptions légitimes
- [[devils-advocate-pipeline]] — rule DA après création
- [[forge-brain-proactive]] — rule vault check

---

## AJOUT 23 MAI 2026 — Alternative orchestration via PTC

Pour les tâches **multi-tools déterministes** (orchestration sans jugement à chaque étape), **Programmatic Tool Calling (PTC)** est une alternative au pattern sub-agents qui évite le "token tax" du contexte qui gonfle.

### Pattern complémentaire (pas concurrent)

- **Sub-agent (Justin Young 2-agent)** : initializer + coding agent. Chaque sub-agent peut faire du jugement contextuel. Résultats re-entrent dans contexte orchestrateur.
- **PTC** : Claude écrit Python qui orchestre N tool calls dans sandbox. Seul output final entre dans contexte. 1 inference vs N inferences.

### Quand préférer PTC

- ✅ Orchestration déterministe (loops, conditionals, data transformations)
- ✅ Filtrage / agrégation de gros volumes avant decision
- ✅ Réduction token consumption critique (workloads scale)
- ❌ PAS quand jugement contextuel requis à chaque étape

### Quand préférer sub-agents

- ✅ Tâches nécessitant jugement à chaque étape
- ✅ Multi-step reasoning chained
- ✅ Long-running avec context différencié par sub-agent

### Détail technique complet

Voir [[programmatic-tool-calling]] — note canonique avec config API, métriques, gotchas, comparaison détaillée.

### Sources

- [Docs Anthropic PTC](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)
- [[programmatic-tool-calling]] — note canonique forge

---

## AJOUT 24 mai 2026 — AskUserQuestion ne fonctionne PAS en sub-agent

**Verbatim Anthropic** (GitHub issue [#18721](https://github.com/anthropics/claude-code/issues/18721)) :

> "The `AskUserQuestion` tool is currently unavailable within a subagent context. If a subagent encounters a decision point requiring human input, it cannot prompt the user directly."

**Conséquence pratique** :
- ❌ Ajouter `AskUserQuestion` au frontmatter `tools:` d'un sub-agent ne suffit PAS — le tool est ignoré
- ✅ **Pattern correct** : sub-agent retourne output structuré, session principale appelle `AskUserQuestion`

### Pattern AMBIGUÏTÉ DÉTECTÉE (à inclure dans body de chaque sub-agent dev/architect/test-writer/code-reviewer/api-designer)

```markdown
## Si AMBIGU détecté — STOP + format ESCALADE

Tu ne peux PAS appeler `AskUserQuestion` directement (limitation Anthropic sub-agents — issue #18721). Si tu rencontres une ambiguïté (specs floues, options multiples valides, contraintes contradictoires, breaking change détecté), tu **arrêtes immédiatement** et retournes ce format structuré à la session principale qui, elle, peut appeler AskUserQuestion :

\`\`\`markdown
## AMBIGUÏTÉ DÉTECTÉE — escalade session principale

**Contexte** : <ce que tu as compris de la tâche>
**Ambiguïté** : <ce qui n'est pas clair>
**Options identifiées** :
  (1) <option 1 avec tradeoffs>
  (2) <option 2 avec tradeoffs>
**Ta recommandation** : <option N + raison courte>
**Question pour l'utilisateur** : <formulation courte et claire à poser via AskUserQuestion>
**État actuel** : <fichiers touchés jusqu'ici, branche, dirty/clean>
\`\`\`

La session principale lit ce bloc, invoque `AskUserQuestion`, te re-dispatche avec la réponse.

**Pas de devinette.** Mieux vaut escalader 2 fois que produire du code sur une mauvaise interprétation.
```

### Différence avec ESCALADE REQUISE (hors-scope)

Pattern jumeau de [[anti-reentrance-sub-agents-pattern-escalade]] :
- **ESCALADE REQUISE** = hors-scope (autre agent doit prendre la suite)
- **AMBIGUÏTÉ DÉTECTÉE** = info manquante (user doit clarifier)

Les deux escaladent vers session principale qui orchestre. Aucun ne nécessite `AskUserQuestion` dans le sub-agent.

### Application dans repos forge

Déployé 24 mai 2026 sur 15 sub-agents (9 neo_ia + 5 ia_back + 1 forge devils-advocate). Hook `SubagentStop` `escalade-detector` (neo_ia .py + ia_back .ts) détecte les markers et imprime suggestion en stderr (non-bloquant, pattern Anthropic "hooks suggest, humans approve").

### Sources

- [GitHub issue #18721 AskUserQuestion subagent limitation](https://github.com/anthropics/claude-code/issues/18721)
- [[anti-reentrance-sub-agents-pattern-escalade]] — pattern jumeau hors-scope
- [[pattern-spec-driven-development]] — workflow Thariq interview AskUserQuestion (en SESSION PRINCIPALE)

---

## AJOUT 24 mai 2026 (suite) — Wildcard MCP `mcp__server__*` dans `tools:` et coût token réel

**Verbatim Anthropic docs** ([code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions) section MCP) :

> * `mcp__puppeteer` matches any tool provided by the `puppeteer` server
> * `mcp__puppeteer__*` wildcard syntax that also matches all tools from the `puppeteer` server
> * `mcp__puppeteer__puppeteer_navigate` matches the `puppeteer_navigate` tool provided by the `puppeteer` server

### Doctrine forge : opérations exactes, pas wildcard

La syntaxe wildcard existe et est officielle, mais **forge ne l'utilise pas sur le vault** : une capacité de lecture ne doit jamais pré-approuver les mutations. Les agents déclarent les opérations MCP exactes dont ils ont besoin.

```yaml
# ❌ Trop large sur un MCP qui peut muter le vault
tools: Read, Write, Edit, Bash, mcp__forge-brain__*

# ✅ Opérations exactes — un agent read-only ne peut pas delete_note
tools: Read, Glob, Grep, mcp__forge-brain__search_brain, mcp__forge-brain__read_note
```

### Quand le wildcard reste défendable

- Serveur MCP strictement read-only (aucun outil mutateur à exposer)
- Prototype jetable où la surface est sans conséquence

### Précision token cost (24 mai 2026)

**Risque token réel ≠ syntaxe `tools:` frontmatter.**

| Niveau | Impact token | Source |
|--------|-------------|--------|
| Liste vs wildcard dans `tools:` agent | **Négligeable** (~40 chars diff) | Frontmatter parsé une fois |
| Ajouter un MCP server à `.mcp.json` / `mcpServers` | **Énorme** (toutes les tool defs chargées en context principal) | Anthropic docs |
| 50+ tools cumulés MCP toutes sources | **"le modèle se perd"** | [[Thariq Shihipar]] verbatim |

**Conséquence pour forge** :
- Déclarer les opérations MCP exactes : une capacité de lecture ne doit jamais pré-approuver les mutations du vault.
- Garder le nombre de MCP servers actifs **modeste** (≤ 5-7 sur un repo) — c'est là que se joue le vrai coût.
- Si un MCP server a > 20 outils (forge-brain en expose 22), considérer un split (`forge-brain-read` + `forge-brain-write`) plutôt que limiter via `tools:` du sub-agent.

**Anti-pattern** : croire que lister 3 outils explicites au lieu de wildcard "économise des tokens". Faux — économise des chars frontmatter (négligeable). Le payload tools defs reste identique. On liste pour le **moindre privilège**, pas pour le budget.

### Sources

- [Anthropic Permissions docs section MCP](https://code.claude.com/docs/en/permissions#mcp)
- [Anthropic Permission rule syntax](https://code.claude.com/docs/en/permissions#permission-rule-syntax)

---

## AJOUT 24 mai 2026 (suite 2) — Pattern MCP brief-then-direct

**Source canonique** : [[pattern-mcp-brief-then-direct]].

### Body section standardisée à inclure dans tout sub-agent ayant accès MCP

```markdown
## MCP — accès direct (filet de sécurité)

Tu reçois normalement un brief enrichi de la session principale avec les éléments MCP pertinents déjà extraits (vault, DB, docs, traces).

**Si pendant l'exécution tu rencontres un doute non couvert par ton brief** (terme inconnu, décision technique conflictuelle, pattern incertain, valeur précise non fournie), tu peux re-consulter directement le MCP via `mcp__<server>__*`.

**Pas systématique** — la session principale t'a déjà briefé. C'est un filet de sécurité, pas une exploration parallèle. Anti-pattern : scanner par réflexe (coût tokens × N agents).

**Quand l'utiliser** :
- ✅ Terme/acronyme non défini dans le brief
- ✅ Conflit entre 2 approches mentionnées
- ✅ Valeur précise nécessaire (ex : type colonne DB)
- ❌ Re-vérifier ce que le brief dit clairement
- ❌ "Au cas où" sans déclencheur précis
```

### Côté session principale — brief enrichi obligatoire

Avant tout dispatch de sub-agent ayant accès MCP :
1. Consulter MCP pertinent (vault canoniques + feedbacks + erreurs + DB schéma + docs)
2. Synthétiser dans le prompt (puces ciblées, wikilinks aux notes lues)
3. Préciser le scope du filet et les opérations de lecture exactes autorisées

Cf [[pattern-mcp-brief-then-direct]] pour exemples concrets + transposition cross-MCP (obsidian-brain, postgres, langfuse, context7).

---

## AJOUT 27 mai 2026 — Brief sub-agent et accès vault : cause-racine empirique

Vérifié empiriquement (Chantier A étape 2b, 27 mai 2026) : les permissions MCP déclarées dans `tools:` d'un sub-agent pouvaient être **décoratives** — le MCP n'est PAS connecté dans son contexte (`No such tool available`). Un sub-agent à qui on ordonne « lire EN ENTIER via MCP » fallback sur `cat`/`find`/`grep`/`Read` du vault → viole la doctrine MCP-only.

**Règle pour `subagent-creator`** : ne JAMAIS écrire « lis via MCP » dans le body d'un creator. Écrire « le contenu canonique te vient inline dans le brief ; sinon ESCALADE ; jamais cat/find/grep/Read le vault ». Filet MCP subordonné à l'escalade. Les creators forge ont été durcis selon cette règle le 27 mai.

Enforcement structurel : hook `vault-cat-guard.py` (branché via le dispatcher `pre-bash-guards.py`). Voir [[hook-intercepte-mcp-et-read-tools]] (preuve d'interception) et [[pattern-mcp-brief-then-direct]] (cause-racine complète).

---

## AJOUT 27 mai 2026 (suite) — Agent ou skill ? Le critère de densité d'écriture MCP

**Question-réflexe avant toute création d'agent** : ton composant doit-il faire N× écritures MCP (vault, base, fichiers) en boucle ?

- **Oui → SKILL** (tourne en session principale, MCP effectif), pas agent. En sous-agent le MCP est décoratif (`No such tool available`) : un métier d'écriture MCP dense y est littéralement impossible.
- **Non (analyse + 0-1 écriture rare) → agent OK.** Le mode dégradé (renvoyer le livrable en texte, la session principale persiste) reste viable.

Cas empirique : `vault-maintainer` killé le 27 mai 2026 — doublon mort-né de la skill `/vault-audit` (qui fait le même métier de maintenance vault en session principale, MCP effectif). Cf [[pattern-mcp-brief-then-direct]] section "Exception : quand le doublon révèle un agent mort-né (KILL > faire marcher)".

---

## AJOUT 5 juin 2026 — Étapes séquentielles obligatoires → checklist Tasks natif (anti-oubli)

Quand un agent exécute un **processus multi-phases dont aucune étape ne doit être sautée** (audit par dimensions, pipeline vérifiable, revue structurée), lui demander de matérialiser sa progression avec le système **Tasks natif** (`TaskCreate` → `TaskUpdate` pending→in_progress→completed) plutôt que de tenir l'ordre de tête.

### Pourquoi

Un modèle qui **interprète littéralement et ne généralise pas seul** peut oublier une phase sur un long enchaînement si rien ne la matérialise en tâche cochable. La tâche est le signal explicite qui force le pas-à-pas. (Remplace l'ancien `TodoWrite`.)

### Quand l'appliquer

- ✅ Agent qui audite/revoit selon N dimensions fixes (1 tâche par dimension)
- ✅ Agent pipeline (spec → draft → verify) où chaque phase est vérifiable
- ❌ Agent mono-jugement (1 verdict, 1 critique) — la checklist est du bruit

À écrire dans le body de l'agent (instruction de comportement), pas en frontmatter. Cohérent avec le pattern jumeau côté skills — voir [[comment-creer-skill]] section « checklist Tasks natif ». Cas d'usage : la skill `loop-forge` ([[concevoir-loops-travail]]) pilote son questionnaire ainsi.

---

## AJOUT 7 juin 2026 — Résolution modèle (ordre exact vérifié) + invocation explicite + champs frontmatter récents

Source primaire revérifiée : [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents), 7 juin 2026.

### Ordre de résolution du modèle d'un subagent (verbatim docs)

Quand Claude invoque un subagent, le modèle est résolu dans CET ordre :

1. La variable d'env **`CLAUDE_CODE_SUBAGENT_MODEL`** (si définie)
2. Le **paramètre `model` per-invocation** (passé à l'invocation)
3. Le **`model` du frontmatter** de la définition
4. **`inherit`** (défaut — même modèle que la conversation principale)

> ⚠️ Piège : le paramètre per-invocation **précède** le frontmatter (pas l'inverse). Une source secondaire pouvait inverser frontmatter et param — l'ordre vérifié est env > param > frontmatter > inherit. `model` accepte aussi un ID complet ou `inherit` — mais préférer l'alias (`sonnet`/`opus`/`haiku`), cf § Règles frontmatter critiques.

### Invocation explicite — 3 patterns (du ponctuel au session-wide)

- **Langage naturel** : nommer le subagent dans le prompt ; Claude décide de déléguer.
- **@-mention** (garantit l'exécution pour UNE tâche) : taper `@` puis choisir dans la typeahead. Syntaxe exacte : **`@"code-reviewer (agent)"`** (le format est `@"<name> (agent)"`). Le message complet va quand même à Claude qui écrit le prompt de tâche ; le @-mention contrôle QUEL subagent, pas le prompt reçu.
- **Session-wide** : `--agent <name>` (flag CLI) ou le setting `agent` → toute la session prend le system prompt + restrictions d'outils + modèle de ce subagent.

### Champs frontmatter récents

> **Mise à jour vérifiée le 28 août 2026 (Claude Code 2.1.248)** — Le frontmatter accepte aussi `experimental.cacheTtl: "5m" | "1h"`. Ce TTL de cache de prompt s'applique par agent uniquement lorsqu'aucun réglage de TTL de subagent n'est déjà configuré. Source primaire : [CHANGELOG officiel Claude Code](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#21248).

La table frontmatter officielle inclut désormais : `isolation: worktree` (run dans un git worktree temporaire branché par défaut sur la default branch, auto-nettoyé si aucun changement), `background: true` (toujours run en background task), `initialPrompt`, `maxTurns`, `mcpServers`. Le `--agents` flag (CLI-defined subagents en JSON éphémère) accepte les mêmes champs.

**Scoped identifier plugin** : un subagent dans un sous-dossier de plugin `agents/review/security.md` (plugin `my-plugin`) s'enregistre comme `my-plugin:review:security`. Hors plugin, le sous-dossier n'affecte PAS l'identité (seul le champ `name` compte ; noms doivent être uniques sur tout l'arbre, sinon un fichier est gardé et l'autre écarté sans warning).

**Source de cet ajout** : réconciliation du doc `Important/reference-subagents-claude-code.md` (supprimé après absorption, 7 juin). Le doc était déjà ~95% subsumé par cette canonique (6 niveaux enforcement, 3 causes, table héritage, issues #43630/#32910/#18721 déjà présents) ; seuls la résolution modèle (corrigée vs le doc), le @-mention exact et les champs récents manquaient. Cf [[feedback_lire_fichier_entier_avant_verdict]].

---

## AJOUT 10 juin 2026 — Agents dev : vérifications par LOTS, jamais après chaque fichier

Anti-pattern observé en production (US1 neoteem-back-ts, ticket ×3-4 plus lent) : un agent dev dont le prompt dit « boucle jusqu'au vert » ou liste « lint/format » comme étape relance lint + typecheck + tests **après chaque fichier écrit** — et relance des vérifs sans aucun nouveau changement. Pire : il lance le formateur À LA MAIN alors qu'un hook PostToolUse formate déjà chaque écriture (100 % redondant).

**Règles à graver dans tout agent dev (et toute rule dev-discipline)** :
1. Écrire l'ENSEMBLE des changements d'une étape du plan, PUIS vérifier (tests ciblés sur le package/module touché — jamais le workspace entier en cours de dev, c'est le rôle du gate /go).
2. Relancer une vérification sans nouveau changement depuis la précédente = interdit.
3. Si un hook PostToolUse formate/lint déjà → l'agent ne lance JAMAIS le formateur manuellement en cours de route (une passe finale au plus).
4. Le typecheck lourd vit dans un hook Stop (cf [[comment-creer-hook]] AJOUT 10 juin), pas dans la boucle de l'agent.

Cohérent avec Boris (« give Claude a way to verify its work » = un check CIBLÉ qui rend pass/fail — pas une relance permanente de tout) et le budget anti-lourdeur des pipelines /feature. Appliqué : agent `dev` neoteem-back-ts + 5 agents `dev-*` neo_ia + rule `dev-discipline` § Vérifications par lots.

---

## AJOUT 16 juin 2026 — Sous-agents imbriqués POSSIBLES (v2.1.172) : la table de capacités était périmée

### Coût économique — pourquoi l'anti-pattern reste valide (couche design)

Depuis v2.1.172, le nesting n'est plus une impossibilité technique. La reco « pas d'agent orchestrateur » reste valide pour une raison **économique vérifiée** : multi-agents = **+200-500% de tokens** (incidents réels documentés 8-47k$). Sur abonnement, chaque agent parallèle consomme le quota Nx plus vite.

- **Profondeur utile réelle = 2-3, jamais 5** (verbatim Boris + retours prod) — le nesting est fait pour gérer le contexte (pousser le bruit loin de la conversation), PAS pour orchestrer.
- **Pour orchestrer BEAUCOUP d'agents** (ex. loop multi-stories) → outil **Workflow** (orchestration hors-contexte), pas un arbre d'agents imbriqués.
- Session principale + CLAUDE.md = orchestrateur ; agents = travailleurs spécialisés. Pattern Boris testé 5 fois.

Source : [[feedback_no_cto_agent]] — amende couche FACTUELLE 18 juin 2026. Cf [[amende-vs-pivot-couche-factuelle-design]].

> Cette note est la **source amont** du claim « pas de subagents imbriqués » (citée par [[anti-reentrance-sub-agents-pattern-escalade]], `subagent-creator` SKILL, [[limites-subagents-claude-code]]). Corrigée ici pour éviter le drift résiduel. Source primaire : [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) + changelog v2.1.172.

### Ce qui ne change PAS (couche design — toujours canonique forge)

L'anti-pattern **« Agent CTO orchestrateur — la session principale orchestre »** reste valide : c'est un **choix d'architecture** (contexte propre, coût maîtrisé, debugging lisible), pas une impossibilité technique. Le nesting est désormais permis mais s'active **sélectivement** pour le seul cas mûr (reviewer→verifier par finding, fan-out hiérarchique où l'intermédiaire est du bruit) — détail et arbitrage dans [[anti-reentrance-sub-agents-pattern-escalade]] § AJOUT 16 juin.

### Règle de génération

Pour tout agent généré : **`tools:` explicite obligatoire** (déjà la règle forge) — ce qui le protège AUSSI du nesting non voulu. **Par défaut hérité** : un agent qui omet `tools:` reçoit `Agent`. Pour bloquer : `tools:` explicite sans `Agent`, ou `disallowedTools: Agent`. N'ajouter `Agent` aux `tools:` d'un agent QUE si son rôle est de dispatcher (ex `repo-inspector`), et le documenter. La syntaxe `Agent(type)` en `tools:` n'agit comme allowlist que sur un agent **main-thread** (`--agent`) ; en sous-agent la parenthèse est ignorée.

---

## AJOUT 15 juillet 2026 — Persona/rôle de dialogue ≠ subagent

Un « rôle » qui pilote le DIALOGUE (checkpoints humains, questions, ton persistant — ex. `@dev`/`@docu` du repo bdd) n'est PAS un subagent : `AskUserQuestion`, `EnterPlanMode` et `ScheduleWakeup` sont **officiellement indisponibles en subagent** (doc sub-agents, vérifié 15 juil. 2026 — « depend on the main conversation's UI »). Le ranger dans `.claude/agents/` l'enregistre comme subagent natif → collision namespace (typeahead `@` spawn isolé, interactivité cassée). Pattern correct : dossier inerte `.claude/roles/` + routage CLAUDE.md. Doctrine complète, grille persona/skill/subagent/Agent Teams et cas réel bdd : [[pattern-personas-session-principale]].

---

## AJOUT 27 juillet 2026 — nesting subagents depth 3 + caps quantitatifs (CC v2.1.212-219)

Changement de paysage sub-agents dans la fenêtre 17-24 juillet 2026 (source : [[CC juillet 2026 - Opus 5 + v2.1.212-220]]) :

- **Nesting par défaut jusqu'à depth 3** (v2.1.219, 24 juil.) : un sub-agent peut spawner des sub-agents, sur 3 niveaux. `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` pour revenir à l'ancien comportement. Flip-flop assumé : la v2.1.217 (21 juil.) avait DÉSACTIVÉ le nesting par défaut, revert 3 jours après — Anthropic choisit les garde-fous quantitatifs plutôt que l'interdiction.
- **Caps par session** : 200 spawns de subagents + 200 WebSearch (v2.1.212) ; **20 subagents concurrents** max (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, v2.1.217).
- **Paramètre `mode` du Task tool DÉPRÉCIÉ (ignoré)** (v2.1.212) — les subagents héritent du permission mode parent ; le frontmatter agent peut l'overrider. Toute doctrine/brief qui passait `mode` à l'invocation est à nettoyer.
- v2.1.203 avait déjà rendu les sub-agents « moins enclins à re-déléguer leur tâche entière à un autre sub-agent ».

Impact doctrine forge : le pattern hiérarchique profond devient officiellement supporté — mais la doctrine forge (orchestration en session principale, 1 niveau de délégation, brief riche) reste valide par défaut : depth 3 = capacité, pas recommandation. Cf [[anti-reentrance-sub-agents-pattern-escalade]] pour la relance/escalade.

---

## AJOUT 5 septembre 2026 — audit de doctrine : ce que cette note portait de faux

Onze écarts corrigés en une passe, tous prouvés sur le code ou les sources plutôt que supposés :

1. **Double frontmatter précédé d'un BOM** — un second bloc YAML laissait `titre`/`resume`/`auteur`/`type`/`sources` hors du frontmatter parsé. `lint_vault` ne le détecte pas (`broken_yaml` reste à 0). Défaut borné à exactement 2 notes du vault : celle-ci et [[comment-creer-skill]] — les deux canoniques de création de composants.
2. **IDs de modèles morts** prescrits comme « IDs exacts » — remplacés par la règle « alias, jamais ID figé », la seule qui survive aux générations.
3. **`effort: max`** présenté comme utilisable — la doctrine forge l'interdit en frontmatter.
4. **« Le hard block `delegate-guard` a été retiré — enforcement advisory »** : FAUX. Le hook bloque en `exit 2`. Il n'apparaît pas dans `settings.json` parce qu'il est branché via le dispatcher `pre-write-guards.py` — ce qui avait fait conclure à tort qu'il était débranché.
5. **Une section enseignait le contournement du garde-fou** — retirée et remplacée par l'interdiction explicite. C'était le défaut le plus grave : la canonique de création de composants documentait pas à pas comment neutraliser une protection.
6. **`agent-creator`** (nom mort depuis le pivot du 6 juin) employé dans sept passages — aligné sur `subagent-creator`.
7. Faux marqueur de fin de note suivi de 356 lignes de contenu.
8. Deux résidus d'édition demandant de mettre à jour `derniere-maj`.
9. « 21 outils MCP » → 22.
10. Section wildcard MCP dont l'exemple contredisait sa propre conclusion — réécrite pour dire ce que forge fait vraiment (opérations exactes, moindre privilège).
11. Observations attachées à une version de modèle précise — regénéralisées.

**Leçon de méthode** : les faits périmés d'une canonique ne se voient pas à la lecture d'un extrait. Ils apparaissent en croisant la note EN ENTIER avec le code réel. Le point 4 est le contre-exemple utile — vérifier qu'une garde MANQUE exige la même rigueur que vérifier qu'elle existe : un grep sur le mauvais fichier avait produit un faux négatif, corrigé en remontant au dispatcher. Cf [[feedback_diagnostic_empirique_avant_affirmer_garde]] et `sequence-canonique-modification.md`.
