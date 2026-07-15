---
derniere-maj: 2026-06-16
aliases:
  - "comment creer un agent"
  - "creer subagent claude code"
  - "best practices agents"
  - "sonnet opus split agents"
  - "frontmatter agent effort model"
  - "2-agent justin young"
  - "doctrine agents forge"
  - "permissionmode-enum-valid-values"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#doctrine/2026"
---
﻿---
titre: "Comment créer un agent Claude Code parfait"
resume: "Note canonique pour créer un agent Claude Code — frontmatter complet, 2-agent architecture Justin Young (sans split modèles), Sonnet/Opus split doctrine forge cohérente avec Cat Wu + Brad Abrams, convention 8 couleurs forge, anti-patterns CTO orchestrator."
aliases:
  - "comment creer agent"
  - "creer un agent claude code"
  - "create claude code agent"
  - "agent parfait"
  - "agent best practices"
  - "2-agent architecture"
  - "harness agent"
  - "convention couleurs agents"
  - "frontmatter agent"
  - "sonnet opus split"
derniere-maj: 2026-05-27
auteur: claude
type: technique
sources:
  - "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents"
  - "Justin Young (MTS Anthropic) — Initializer + Coding agent (sans split modèles)"
  - "Cat Wu — Code with Claude London 19 mai 2026 (Opus 4.7 + xhigh)"
  - "Brad Abrams — Code with Claude SF 6 mai 2026 (Advisor Strategy)"
  - "docs.claude.com/agents"
  - "Böckeler — martinfowler.com/articles/harness-engineering.html (Guides+Sensors 2 avril 2026)"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/agents"
  - "#doctrine/2026"
---
# Comment créer un agent Claude Code parfait

> Note canonique forge — création d'agents selon doctrine Anthropic + Justin Young + Cat Wu + Brad Abrams + Böckeler/Fowler mai 2026.

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
effort: low | medium | high | xhigh | max
color: red | orange | yellow | green | blue | purple | cyan | pink
memory: project
permissionMode: acceptEdits | auto | plan | default | dontAsk | bypassPermissions
disallowedTools: <outils interdits, ex Write, Edit>
skills: <skills mobilisées, optionnel>
maxTurns: <nombre, optionnel>
---
```

### Règles frontmatter critiques
### Frontmatter vs body : alignement obligatoire

**Le frontmatter fait foi. Le body ne doit JAMAIS le contredire.**

- Un champ frontmatter (`effort`, `model`, `memory`, `permissionMode`, etc.) est la source de vérité unique pour sa valeur.
- Le body de l'agent NE DOIT PAS re-commenter ni re-justifier un champ frontmatter (ex : ligne `effort: xhigh — la pensée adversariale exige une profondeur maximale`). C'est à la fois redondant et une source de drift quand l'un évolue sans l'autre.
- Double faute classique : le body affirme une valeur (`xhigh`) que le frontmatter dément (`high`). Le composant se contredit lui-même.
- Le **pourquoi** d'un choix de frontmatter vit dans le vault (cette note, CLAUDE.md), pas dans le body de l'agent — cf [[feedback_pas_de_meta_commentaire_doctrine]]. Le hook `meta-commentary-detector` bloque ce type de commentaire doctrinal.

**Règle de vérification** : après toute modification d'agent, `grep` la valeur du champ frontmatter dans le body. Si elle apparaît avec une justification → la supprimer. Le frontmatter parle, le body se tait.

Cas réel 27 mai 2026 : `devils-advocate.md` avait `effort: high` en frontmatter mais le body affirmait `effort: xhigh`. Fix = suppression des 2 lignes de body, frontmatter conservé.


1. **`name`** = nom du fichier sans `.md`, kebab-case
2. **`description`** = trigger directive 3e personne (comme skills)
3. **`model`** :
   - `sonnet` = `claude-sonnet-4-6` (exécution)
   - `opus` = `claude-opus-4-7` (jugement)
   - `haiku` = `claude-haiku-4-5` (tâches courtes ultra-rapides)
4. **`effort`** (verbatim docs Anthropic 23 mai 2026) :
   - Options : `low`, `medium`, `high`, `xhigh`, `max`
   - "Available levels depend on the model"
   - `max` **TOUJOURS DISPONIBLE** (mai 2026). Ce qui est déprécié = `budget_tokens` manuel, remplacé par adaptive thinking
   - Doctrine forge : `high` partout par défaut, `xhigh` réservé architect/dev-lead/refactor-pg, `max` avec prudence (prone overthinking observé)
5. **`memory: project`** = OBLIGATOIRE sur TOUS les agents forge (gère mémoire automatique)
6. **`permissionMode`** = OBLIGATOIRE forge :
   - `acceptEdits` pour créateurs (skill-creator, agent-creator, hook-creator, claudemd-optimizer)
   - `auto` pour exécutants (dev, code-reviewer, test-writer)
   - `plan` pour agents qui doivent **toujours passer par un plan validé** avant action
7. **`disallowedTools: Write, Edit`** sur agents read-only (force délégation)

### Politique modèles forge (doctrine inférée cohérente avec Anthropic)

> **Important honnêteté** : la politique "Sonnet exécution / Opus jugement" est une **doctrine forge inférée** par pattern observé en sessions. **Cohérente avec** :
> - **Cat Wu** (Code with Claude London 19 mai 2026) : "Opus 4.7 tips — delegate, write full-context briefs, use the new `xhigh` effort level"
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
| **pink** | Meta-créateurs (skill-creator, agent-creator — forge only) |

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

### Étape 3 — Déléguer à `agent-creator`

> ⚠️ **Pivot 6 juin 2026** : `agent-creator` est désormais une **skill** nommée `subagent-creator` (`.claude/skills/subagent-creator/`). Invoquer via `Skill(subagent-creator)` depuis la session principale. Le hard block `delegate-guard.py` sur `agents/*.md` a été retiré — enforcement advisory. `cc-agents-ref` supprimée : la doctrine vit dans `subagent-creator` + vault [[comment-creer-agent]].

Côté forge : agent `agent-creator` génère le `.md` conforme. Hook `delegate-guard.py` bloque l'édit direct.

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

> ⚠️ **Correction doc officielle 9 juin 2026** (source : code.claude.com/docs/en/sub-agents) : pour les **agents project-scope du repo courant**, `skills:` frontmatter précharge le **CONTENU COMPLET** de chaque skill dans le contexte du sub-agent au démarrage (« The full skill content is injected, not just the description »). La Cause 2 ci-dessous et la table Héritage (« précharge les *descriptions* seulement ») sont **périmées pour ce scope**. Limitations toujours vraies dans leurs contextes : Agent Teams teammates (skills frontmatter ignorées) et agents user-scope cross-repo (skills non résolues) — cf [[pattern-mcp-brief-then-direct]]. **Conséquence pratique** : agent project-scope avec `skills:` → body dit « skills préchargées, applique-les » + pointer uniquement les `references/` non préchargés. Ne PAS ajouter `Skill` aux `tools:` pour le préchargement (inutile) — seulement si l'agent doit invoquer d'autres skills à la demande. Skills avec `disable-model-invocation: true` non préchargeables ; skill manquante = warning debug log, skip silencieux.

## POURQUOI un subagent n'invoque pas ses skills — 3 causes cumulées

Le problème le plus fréquent. Source : research LLM juin 2026 + empirique forge.

### Cause 1 — `Skill` absent de `tools:` (mécanique)
Sans l'outil `Skill` dans `tools:`, le subagent **ne peut physiquement pas** invoquer de skill. À vérifier en premier.

### Cause 2 — `skills:` précharge, ne force pas
Le champ `skills:` injecte les *descriptions* dans le system prompt (issue #32910) — ce n'est pas une invocation forcée. "Description présente" ≠ "skill invoquée". L'invocation reste probabiliste, comme sur le thread principal.

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
| Skills | ❌ `skills:` = précharge les *descriptions* seulement |
| Outil `Skill` | ❌ Doit être dans `tools:` sinon impossible mécaniquement |
| Outils (Read, Bash…) | ❌ Définis par `tools:` — sans explicite, comportement variable |
| MCP servers | ⚠️ Instable — souvent « No such tool available » |
| CLAUDE.md / rules | ⚠️ Variable (Explore/Plan sautent CLAUDE.md) |
| AskUserQuestion | ❌ Filtré hors subagents (issues #12890 #18721 #20275) |
| Task tool (sous-subagent) | ❌ Pas de subagents imbriqués |
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
- [ ] `model` adapté (haiku explore, sonnet implémentation, opus orchestration/jugement)
- [ ] `disallowedTools` pour couper les raccourcis qui font zapper les skills
- [ ] `memory: project` + `permissionMode` obligatoires (forge)

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
- `memory: project` partout
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
- ❌ **Agent qui invoque un autre agent (ré-entrance)** : risque de boucle infinie ou tool_use partagés conflictuels. Si nécessaire, passer par la session principale qui orchestre. Mise en garde forge — pas doctrine Anthropic explicite.

### Frontmatter
- ❌ **Pas de `memory: project`** — mémoire pas gérée (règle forge)
- ❌ **Pas de `permissionMode`** — auto-mode bloque (règle forge)
- ❌ **`effort: max` par défaut** — coût massif, réserver à cas justifiés
- ❌ **`effort: xhigh` partout** — réservé architect/dev-lead/refactor-pg (règle forge)
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
- ❌ **Édit direct `.md` agent** — délégation obligatoire à `agent-creator` (hook bloque)

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
- **Cat Wu** (Head of Product Claude Code) : Opus 4.7 tips, xhigh effort level
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

Un agent généré par `agent-creator` doit adapter ses mécanismes selon l'environnement cible. Cette matrice complète [[cowork-skills-reliability]] côté agents.

| Mécanisme | Claude Code CLI | Code Desktop | Cowork |
|---|---|---|---|
| **Hooks (PreToolUse/PostToolUse)** | ✅ Fiable | ⚠️ Partiel | ❌ Silent no-op |
| **`context: fork` / `agent:` frontmatter** | ⚠️ Ignoré si invoqué via Skill tool | ⚠️ Idem | ⚠️ Idem — utiliser Task tool explicite à la place |
| **MCP local (stdio) dans `tools:`** | ✅ Effectif en session principale | ✅ | ❌ Décoratif en sub-agent ET inaccessible Cowork |
| **MCP remote HTTPS** | ✅ | ✅ | ✅ Seul type viable |
| **`disallowedTools`** | ✅ | ✅ | ✅ |
| **`permissionMode`** | ✅ | ✅ | ✅ |
| **`memory: project`** | ✅ | ✅ | ⚠️ Comportement moins documenté |
| **AskUserQuestion** | ❌ Non dispo en sub-agent (issue #18721) | ❌ Idem | ❌ Idem — ESCALADE vers session principale |

### Stratégie de génération selon la cible

**Si `agent-creator` génère un agent pour CLI / Code Desktop :**
- Hooks complémentaires ok (PreToolUse guard, PostToolUse validation)
- MCP local (stdio) dans `tools:` ok en session principale
- `context: fork` / `agent:` à éviter si l'agent sera invoqué via Skill tool (ignoré)
- Pattern complet disponible

**Si `agent-creator` génère un agent pour Cowork :**
- ❌ **Ne pas émettre de hooks** dans la skill/agent générée — silent no-op
- ❌ **Ne pas compter sur MCP stdio** — remote HTTPS uniquement
- ✅ Description directive + script-output gating + AskUserQuestion gate (session principale)
- ✅ Checklist "à voix haute" obligatoire dans l'output pour remplacer les guards déterministes
- ✅ Utiliser Task tool explicite au lieu de `context: fork`

**Rappel universel :**
`AskUserQuestion` n'est jamais disponible dans un sub-agent (CLI, Desktop, Cowork) — pattern ESCALADE obligatoire. Voir section dédiée AJOUT 24 mai 2026.

## GOTCHAS — Pièges observés

### Pièges modèle / effort
- **`effort: max` toujours disponible** mai 2026 (verbatim docs) — utiliser avec prudence (prone overthinking)
- **`xhigh` partout = coût massif** — réservé architect/dev-lead/refactor-pg (forge)
- **Opus 4.7 plus littéral** — être explicite sur scope et parallélisme (observation forge)
- **Modèle IDs exacts** : sonnet→`claude-sonnet-4-6`, opus→`claude-opus-4-7`, haiku→`claude-haiku-4-5`

### Pièges permissions
- **agents de plugins** : `hooks`, `mcpServers`, `permissionMode` sont **ignorés pour les agents de plugins** (sécurité) — s'applique uniquement aux agents `.claude/agents/` du repo courant.
- **`permissionMode` OBLIGATOIRE** côté forge — sans, auto-mode bloque (cf [[feedback_permissionmode_mandatory]])
- **`permissions.allow`** : non hérité par sub-agents (cf [[reference_subagent_permissions]])
- **Worktree access + MCP tools** : OK depuis v2.1.101

### Pièges memory
- **`memory: project`** OBLIGATOIRE forge — gère mémoire automatiquement, pas besoin scripts manuels (cf [[feedback_memory_mandatory]])

### Pièges skills
- **Skills dans `skills:` non référencées dans body** = orphelines, jamais activées (cf [[feedback_skills_referenced_in_body]])

### Pièges environnement / invocation
- **`context: fork` / `agent:` ignorés via Skill tool** — si l'agent est invoqué via le Skill tool (pas directement via Agent tool), ces directives frontmatter sont silencieusement ignorées. Utiliser une instruction explicite `Task tool` dans le body à la place
- **Agent ciblant Cowork** : ne jamais émettre de hooks ni de MCP stdio dans un agent généré pour Cowork — ils sont des no-ops (voir [[cowork-skills-reliability]] matrice enforcement)

### Pièges délégation
- **Édit direct bloqué** par hook `delegate-guard.py` — utiliser `agent-creator`
- **Sub-agent commit autonome** — mettre "PAS DE COMMIT" en TOP du prompt en gras (cf [[feedback_subagent_autocommit]])
- **Repo externe** : pas de git autonome (cf [[feedback_never_commit_foreign_repos]])

### Pièges Windows
- **Python path absolu** dans hooks référencés par agent (Windows alias MS Store sinon)
- **Heredoc Bash Windows** : boucle quoting Git Bash (cf [[erreur-da-heredoc-bash-silencieux]])

### Pièges forge
- **Vault check obligatoire** avant création (cf [[forge-brain-proactive]])
- **DA après création majeure** (cf [[devils-advocate-pipeline]])
- **Convention couleurs cross-repo** stricte (forge)

---

## ALIASES — Findability

Aliases déclarés en frontmatter (10) :
- comment creer agent
- creer un agent claude code
- create claude code agent
- agent parfait
- agent best practices
- 2-agent architecture
- harness agent
- convention couleurs agents
- frontmatter agent
- sonnet opus split

---

## WIKILINKS

### Notes canoniques sœurs
- [[comment-creer-skill]]
- [[comment-creer-hook]]
- [[comment-ecrire-claudemd]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[mcp-vs-skills-doctrine]]

### Fiches leaders (à créer)
- [[Justin Young]]
- [[Cat Wu]]
- [[Brad Abrams]]
- [[Noah Zweben]]
- [[Daisy Hollman]]
- Fiona Fung (Head of Engineering Anthropic) — fiche à créer
- [[Jeremy Hadfield]]
- [[Erik Schluntz]]
- [[Birgitta Böckeler]]
- [[Mitchell Hashimoto]]
- [[Addy Osmani]]

### Knowledge / erreurs / refs
- [[feedback_no_cto_agent]]
- [[feedback_memory_mandatory]]
- [[feedback_permissionmode_mandatory]]
- [[feedback_skills_referenced_in_body]]
- [[feedback_agent_tools_restriction]]
- [[feedback_subagent_autocommit]]
- [[feedback_never_commit_foreign_repos]]
- [[reference_subagent_permissions]]
- [[erreur-da-heredoc-bash-silencieux]]

### Forge custom
- [[agent-creator]] — agent forge dédié
- [[devils-advocate-pipeline]] — rule DA après création
- [[agents-color-convention]] — rule couleurs cross-repo
- [[forge-brain-proactive]] — rule vault check

---

**Fin note canonique `comment-creer-agent.md`** — révisée 23 mai 2026 post-audit thématique vault.

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

`derniere-maj` à mettre à jour après ce ajout.


## Anti-patterns

- [[erreur-seuils-canoniques-agents-inventes-2026-05-22]] — 4/5 seuils "canoniques" agents Claude Code cités dans le vault étaient des mythes (extrapolations, confusion). Seuls CLAUDE.md<200L et SKILL.md<500L sont vraiment canoniques.


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

## AJOUT 24 mai 2026 (suite) — Wildcard MCP `mcp__server__*` dans `tools:`

**Verbatim Anthropic docs** ([code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions) section MCP) :

> * `mcp__puppeteer` matches any tool provided by the `puppeteer` server
> * `mcp__puppeteer__*` wildcard syntax that also matches all tools from the `puppeteer` server
> * `mcp__puppeteer__puppeteer_navigate` matches the `puppeteer_navigate` tool provided by the `puppeteer` server

### Application forge

Au lieu de lister explicitement chaque outil MCP forge-brain (21 outils en mai 2026 — search_brain, read_note, list_notes, find_by_property, get_backlinks, get_tags, vault_stats, lint_vault, read_section, read_note_resolved, get_property, create_note, append_note, insert_section, update_note, update_property, bulk_update_property, move_note, delete_note, usage_stats, read_note_by_path), utiliser **un seul token wildcard** :

```yaml
# ❌ AVANT (restrictif, oublie potentiel)
tools: Read, Write, Edit, Bash, mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__get_backlinks

# ✅ APRÈS (wildcard syntaxe Anthropic officielle)
tools: Read, Write, Edit, Bash, mcp__forge-brain__*
```

### Avantages

- **Pas d'oubli** : si Anthropic ajoute des outils au MCP, l'agent y accède automatiquement
- **Plus court** : 1 token au lieu de 7-10 (gain frontmatter token budget)
- **Sémantiquement plus juste** : "cet agent peut interagir avec le vault" plutôt que "cet agent peut faire ces 3 actions précises"

### Quand préférer le wildcard `mcp__server__*`

- Sub-agent qui doit lire ET écrire dans le vault (ex: vault-maintainer)
- Sub-agent qui pourrait nécessiter outil non anticipé au moment de l'écriture (la majorité)
- Skill /spec ou /done qui orchestre plusieurs étapes vault

### Quand préférer la liste explicite

- Sub-agent **read-only** sur le vault → lister uniquement `mcp__forge-brain__search_brain, mcp__forge-brain__read_note` (et ajouter `disallowedTools: Write, Edit` pour sécu)
- Agent sécu-critique où chaque tool doit être justifié (ex: agent qui n'a PAS le droit de `delete_note`)
- Documentation explicite "cet agent ne fait QUE X et Y"

### Application 24 mai 2026

Tous les 14 agents+skills forge convertis du listing explicite (3-7 tools) vers `mcp__forge-brain__*`. Gain principal : vault-maintainer (7 outils listés → 1 wildcard).

### Wildcard pour d'autres MCP

Pattern transposable à TOUT serveur MCP :
- `mcp__context7__*` (au lieu de `mcp__context7__resolve-library-id, mcp__context7__query-docs`)
- `mcp__docs-langchain__*`
- `mcp__obsidian-brain__*` (neoteem-brain)
- etc.

### Sources

- [Anthropic Permissions docs section MCP](https://code.claude.com/docs/en/permissions#mcp)
- [Anthropic Permission rule syntax](https://code.claude.com/docs/en/permissions#permission-rule-syntax)


### Précision token cost (24 mai 2026)

**Risque token réel ≠ syntaxe `tools:` frontmatter.**

| Niveau | Impact token | Source |
|--------|-------------|--------|
| Liste vs wildcard dans `tools:` agent | **Négligeable** (~40 chars diff) | Frontmatter parsé une fois |
| Ajouter un MCP server à `.mcp.json` / `mcpServers` | **Énorme** (toutes les tool defs chargées en context principal) | Anthropic docs |
| 50+ tools cumulés MCP toutes sources | **"le modèle se perd"** | [[Thariq Shihipar]] verbatim |

**Conséquence pour forge** :
- Wildcard `mcp__forge-brain__*` (21 outils) **OK** — pas plus coûteux que lister 5 outils dans `tools:`. Les définitions des 21 outils sont chargées **une fois** au démarrage du MCP server (whether listed in agent or not).
- Garder le nombre de MCP servers actifs **modeste** (≤ 5-7 sur un repo) — c'est là que se joue le vrai coût.
- Si un MCP server a > 20 outils, considérer un split (ex: `forge-brain-read` + `forge-brain-write`) plutôt que limiter via `tools:` du sub-agent.

**Anti-pattern** : croire que lister 3 outils explicites au lieu de wildcard "économise des tokens". Faux — économise des chars frontmatter (négligeable). Le payload tools defs reste identique.


---

## AJOUT 24 mai 2026 (suite 2) — Pattern MCP brief-then-direct
**Source canonique** : [[pattern-mcp-brief-then-direct]] (nouvelle note 24 mai).

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
3. Préciser le scope du filet ("filet : mcp__forge-brain__* si doute sur X")

Cf [[pattern-mcp-brief-then-direct]] pour exemples concrets + transposition cross-MCP (obsidian-brain, postgres, langfuse, context7).

## AJOUT 27 mai 2026 — Brief sub-agent et accès vault : cause-racine empirique
Vérifié empiriquement (Chantier A étape 2b, 27 mai 2026) : le `mcp__forge-brain__*` du `tools:` d'un sub-agent est **décoratif** — le MCP n'est PAS connecté dans son contexte (`No such tool available`). Un sub-agent à qui on ordonne « lire EN ENTIER via MCP » fallback sur `cat`/`find`/`grep`/`Read` du vault → viole la doctrine MCP-only.

**Règle pour agent-creator** : ne JAMAIS écrire « lis via MCP » dans le body d'un creator. Écrire « le contenu canonique te vient inline dans le brief ; sinon ESCALADE ; jamais cat/find/grep/Read le vault ». Filet MCP subordonné à l'escalade. Les 6 creators forge (agent-creator, skill-creator, hook-creator, claudemd-optimizer, repo-inspector, responsable-ia) ont été durcis selon cette règle le 27 mai.

Enforcement structurel : hook `vault-cat-guard.py`. Voir [[hook-intercepte-mcp-et-read-tools]] (preuve d'interception) et [[pattern-mcp-brief-then-direct]] (cause-racine complète).


## AJOUT 27 mai 2026 — Self-modification d'un creator buggé via bypass de matcher

Cas de figure : un creator (ex `agent-creator`) est le **verrou de bootstrap** ET porte lui-même un bug structurel à corriger. `delegate-guard.py` route tout `.claude/agents/*.md` vers `agent-creator` — donc l'édit direct est bloqué, et `agent-creator` ne peut pas se réparer lui-même par délégation (il EST l'agent requis).

**Mécanisme de bypass propre** (exploite la spec du matcher, ne viole ni ne désactive le hook) :

1. `Write` vers `<fichier>.md.new` — le suffixe `.new` fait que `is_agent_md` (qui exige `parts[-1].endswith(".md")`) retourne False → delegate-guard ne tire pas.
2. `Bash mv <fichier>.md.new <fichier>.md` — `Bash` n'est pas dans le matcher `Edit|Write|MultiEdit` → delegate-guard ne tire pas.
3. `Read`/grep de vérification (frontmatter intact, contenu attendu en place — `Write` fichier entier remplace l'`Edit` ciblé, donc vérifier le frontmatter systématiquement).

**Quand l'utiliser** : UNIQUEMENT quand le creator concerné est le verrou de bootstrap d'une cascade et qu'aucun autre creator ne peut le modifier. JAMAIS en routine — la délégation reste la règle. Validation `advisor` préalable obligatoire pour ce type d'exception.

Cas d'école empirique : Chantier A étape 2b (27 mai 2026), durcissement MCP des 6 creators — `agent-creator` durci en premier par ce mécanisme, puis les 5 autres en cascade via `agent-creator` durci. Voir aussi [[hook-intercepte-mcp-et-read-tools]] section exceptions delegate-guard.


## AJOUT 5 juin 2026 — Étapes séquentielles obligatoires → checklist Tasks natif (anti-oubli)

Quand un agent exécute un **processus multi-phases dont aucune étape ne doit être sautée** (audit par dimensions, pipeline vérifiable, revue structurée), lui demander de matérialiser sa progression avec le système **Tasks natif** (`TaskCreate` → `TaskUpdate` pending→in_progress→completed) plutôt que de tenir l'ordre de tête.

### Pourquoi

Opus 4.8 **interprète littéralement et ne généralise pas seul** : sur un long enchaînement, une phase peut être oubliée si rien ne la matérialise en tâche cochable. La tâche est le signal explicite qui force le pas-à-pas. (Remplace l'ancien `TodoWrite`.)

### Quand l'appliquer

- ✅ Agent qui audite/revoit selon N dimensions fixes (1 tâche par dimension)
- ✅ Agent pipeline (spec → draft → verify) où chaque phase est vérifiable
- ❌ Agent mono-jugement (1 verdict, 1 critique) — la checklist est du bruit

À écrire dans le body de l'agent (instruction de comportement), pas en frontmatter. Cohérent avec le pattern jumeau côté skills — voir [[comment-creer-skill]] section « checklist Tasks natif ». Cas d'usage : la skill `loop-forge` ([[concevoir-loops-travail]]) pilote son questionnaire ainsi.

## AJOUT 27 mai 2026 (suite) — Agent ou skill ? Le critère de densité d'écriture MCP

**Question-réflexe avant toute création d'agent** : ton composant doit-il faire N× écritures MCP (vault, base, fichiers) en boucle ?

- **Oui → SKILL** (tourne en session principale, MCP effectif), pas agent. En sous-agent le MCP est décoratif (`No such tool available`) : un métier d'écriture MCP dense y est littéralement impossible.
- **Non (analyse + 0-1 écriture rare) → agent OK.** Le mode dégradé (renvoyer le livrable en texte, la session principale persiste) reste viable.

Cas empirique : `vault-maintainer` killé le 27 mai 2026 — doublon mort-né de la skill `/vault-audit` (qui fait le même métier de maintenance vault en session principale, MCP effectif). Cf [[pattern-mcp-brief-then-direct]] section "Exception : quand le doublon révèle un agent mort-né (KILL > faire marcher)".


---

## AJOUT 7 juin 2026 — Résolution modèle (ordre exact vérifié) + invocation explicite + champs frontmatter récents

Source primaire revérifiée : [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents), 7 juin 2026.

### Ordre de résolution du modèle d'un subagent (verbatim docs)

Quand Claude invoque un subagent, le modèle est résolu dans CET ordre :

1. La variable d'env **`CLAUDE_CODE_SUBAGENT_MODEL`** (si définie)
2. Le **paramètre `model` per-invocation** (passé à l'invocation)
3. Le **`model` du frontmatter** de la définition
4. **`inherit`** (défaut — même modèle que la conversation principale)

> ⚠️ Piège : le paramètre per-invocation **précède** le frontmatter (pas l'inverse). Une source secondaire pouvait inverser frontmatter et param — l'ordre vérifié est env > param > frontmatter > inherit. `model` accepte aussi un ID complet (`claude-opus-4-8`, `claude-sonnet-4-6`) ou `inherit`.

### Invocation explicite — 3 patterns (du ponctuel au session-wide)

- **Langage naturel** : nommer le subagent dans le prompt ; Claude décide de déléguer.
- **@-mention** (garantit l'exécution pour UNE tâche) : taper `@` puis choisir dans la typeahead. Syntaxe exacte : **`@"code-reviewer (agent)"`** (le format est `@"<name> (agent)"`). Le message complet va quand même à Claude qui écrit le prompt de tâche ; le @-mention contrôle QUEL subagent, pas le prompt reçu.
- **Session-wide** : `--agent <name>` (flag CLI) ou le setting `agent` → toute la session prend le system prompt + restrictions d'outils + modèle de ce subagent.

### Champs frontmatter récents (à connaître, doc à jour 7 juin)

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

## AJOUT 16 juin 2026 — AMENDE : sous-agents imbriqués POSSIBLES (v2.1.172) — la table de capacités est périmée

### Coût économique — pourquoi l'anti-pattern reste valide (couche design, amendé 18 juin 2026)

Depuis v2.1.172, le nesting n'est plus une impossibilité technique. La reco « pas d'agent orchestrateur » reste valide pour une raison **économique vérifiée** : multi-agents = **+200-500% de tokens** (incidents réels documentés 8-47k$). Sur abonnement, chaque agent parallèle consomme le quota Nx plus vite.

- **Profondeur utile réelle = 2-3, jamais 5** (verbatim Boris + retours prod) — le nesting est fait pour gérer le contexte (pousser le bruit loin de la conversation), PAS pour orchestrer.
- **Pour orchestrer BEAUCOUP d'agents** (ex. loop multi-stories) → outil **Workflow** (orchestration hors-contexte), pas un arbre d'agents imbriqués.
- Session principale + CLAUDE.md = orchestrateur ; agents = travailleurs spécialisés. Pattern Boris testé 5 fois.

Source : [[feedback_no_cto_agent]] — amende couche FACTUELLE 18 juin 2026. Cf [[amende-vs-pivot-couche-factuelle-design]].

> Cette note est la **source amont** du claim « pas de subagents imbriqués » (citée par [[anti-reentrance-sub-agents-pattern-escalade]], `subagent-creator` SKILL, [[limites-subagents-claude-code]]). Corrigée ici pour éviter le drift résiduel. Source primaire : [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) + changelog v2.1.172.

### Correction de la table de capacités

La ligne **« Task tool (sous-subagent) | ❌ Pas de subagents imbriqués »** est **fausse depuis CC v2.1.172 (10 juin 2026)**. À lire désormais :

> **Task/Agent tool (sous-subagent) | ✅ POSSIBLE depuis v2.1.172** — foreground n'importe quelle profondeur (auto-limité), background plafonné 5 niveaux. **Par défaut hérité** (un agent qui omet `tools:` reçoit `Agent`). Pour bloquer : `tools:` explicite sans `Agent`, ou `disallowedTools: Agent`.

### Ce qui ne change PAS (couche design — toujours canonique forge)

L'anti-pattern **« Agent CTO orchestrateur — la session principale orchestre »** reste valide : c'est un **choix d'architecture** (contexte propre, coût maîtrisé, debugging lisible), pas une impossibilité technique. Le nesting est désormais permis mais s'active **sélectivement** pour le seul cas mûr (reviewer→verifier par finding, fan-out hiérarchique où l'intermédiaire est du bruit) — détail et arbitrage dans [[anti-reentrance-sub-agents-pattern-escalade]] § AJOUT 16 juin.

### Règle de génération mise à jour

Pour tout agent généré : **`tools:` explicite obligatoire** (déjà la règle forge) — ce qui le protège AUSSI du nesting non voulu. N'ajouter `Agent` aux `tools:` d'un agent QUE si son rôle est de dispatcher (ex `repo-inspector`), et le documenter. La syntaxe `Agent(type)` en `tools:` n'agit comme allowlist que sur un agent **main-thread** (`--agent`) ; en sous-agent la parenthèse est ignorée.

`derniere-maj` → 2026-06-16.


---

## AJOUT 15 juillet 2026 — Persona/rôle de dialogue ≠ subagent : ne pas ranger les rôles dans `.claude/agents/`

Un « rôle » qui pilote le DIALOGUE (checkpoints humains, questions, ton persistant — ex. `@dev`/`@docu` du repo bdd) n'est PAS un subagent : `AskUserQuestion`, `EnterPlanMode` et `ScheduleWakeup` sont **officiellement indisponibles en subagent** (doc sub-agents, vérifié 15 juil. 2026 — « depend on the main conversation's UI »). Le ranger dans `.claude/agents/` l'enregistre comme subagent natif → collision namespace (typeahead `@` spawn isolé, interactivité cassée). Pattern correct : dossier inerte `.claude/roles/` + routage CLAUDE.md. Doctrine complète, grille persona/skill/subagent/Agent Teams et cas réel bdd : [[pattern-personas-session-principale]].