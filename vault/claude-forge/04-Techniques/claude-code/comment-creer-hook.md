---
titre: "Comment créer un hook Claude Code parfait"
resume: "Note canonique pour créer un hook Claude Code — 25+ events officiels, timeout 60s, exit codes 0/1/2, hookSpecificOutput, doctrine 'If a rule must hold every time, make it a hook'. Lint/security/scope OUI, workflow NON (doctrine 22 mai)."
aliases:
  - "comment creer hook"
  - "creer un hook claude code"
  - "create claude code hook"
  - "hook parfait"
  - "hook best practices"
  - "25+ events hooks"
  - "exit codes hooks"
  - "hookSpecificOutput"
  - "asyncRewake"
  - "guides sensors fowler"
derniere-maj: 2026-05-22
auteur: claude
type: technique
sources:
  - "https://code.claude.com/docs/en/hooks"
  - "docs.claude.com — features-overview"
  - "Martin Fowler — Guides+Sensors taxonomy 2 avril 2026"
  - "github.com/trailofbits/claude-code-config"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/hooks"
  - "#doctrine/2026"
---

# Comment créer un hook Claude Code parfait

> Note canonique forge — création de hooks selon doctrine Anthropic 22 mai 2026 + Fowler/Böckeler.

---

## QUOI — Définition

**Hook** = commande shell exécutée automatiquement par Claude Code sur un événement du lifecycle. Permet :
- **Validation déterministe** (bloquer une action invalide)
- **Sensor** (observer + collecter signaux)
- **Side-effect** (formater, notifier, logger)

**Verbatim Anthropic** (doctrine canonique) :

> "If a rule must hold every time, make it a hook rather than a prompt instruction."
> — docs Anthropic features-overview

C'est l'arbitrage central. Une règle dans CLAUDE.md ou une skill = advisory ~80% compliance. Un hook bloquant = 100%.

**Taxonomie Fowler / Böckeler (2 avril 2026)** :

| Type | Nature | Force |
|------|--------|-------|
| **Guides** | Inferential (prompts, rules) | Moyen — ~80% |
| **Sensors** | Computational (hooks, tests) | Fort — 100% sur ce qu'ils détectent |

---

## POURQUOI — Le problème résolu

Sans hooks, on accumule des règles advisory dans CLAUDE.md. Conséquences :
- **~80% compliance** sur règles critiques
- **Trust-then-verify gap** — la règle existe mais rien ne la vérifie
- **Récurrence d'erreurs** — la session suivante refait l'erreur

Avec hooks bloquants sur règles critiques :
- **100% compliance** sur ce que le hook détecte
- **Détection précoce** (PreToolUse avant action)
- **Side-effects automatiques** (format, notify, log)

---

## COMMENT — Structure et configuration

### Settings.json — où déclarer un hook

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<pattern outil ou type>",
        "hooks": [
          {
            "type": "command",
            "command": "<chemin absolu commande>"
          }
        ]
      }
    ]
  }
}
```

### Les 25+ events officiels (source vérifiée : `.claude/skills/cc-hooks-ref/SKILL.md`)

| Event | Bloquant | Phase |
|-------|----------|-------|
| `PreToolUse` | ✅ exit 2 | Avant tout outil — c'est ICI qu'on intercepte Write/Edit/MultiEdit/Bash via `matcher` |
| `PostToolUse` | ❌ | Après outil — formatage, lint, notifications |
| `PostToolUseFailure` | ❌ | Après échec outil |
| `Stop` | ✅ JSON block | Fin de turn (avec `once: true` sinon boucle) |
| `SubagentStart` / `SubagentStop` | ✅ (Stop) | Sub-agents lifecycle |
| `SessionStart` / `SessionEnd` | ❌ | Lifecycle session |
| `UserPromptSubmit` | ❌ | Prompt utilisateur reçu |
| `UserPromptExpansion` | ✅ exit 2 | Expansion du prompt (bloquable) |
| `PermissionRequest` | ✅ | Avant demande permission |
| `PermissionDenied` | ❌ | Après refus auto-mode (`{retry: true}` pour relancer) |
| `Notification` | ❌ | Notification utilisateur |
| `PreCompact` / `PostCompact` | ❌ | Avant / après compression contexte |
| `Setup` | ❌ | Setup initial |
| `TeammateIdle` | ❌ | Coéquipier inactif |
| `TaskCompleted` | ❌ | Tâche terminée |
| `ConfigChange` | ❌ | Config modifiée |
| `WorktreeCreate` / `WorktreeRemove` | ❌ (mais non-zero abort sur Create) | Worktrees |
| `InstructionsLoaded` | ❌ | Chargement CLAUDE.md/rule |
| `CwdChanged` | ❌ | Répertoire courant modifié |
| `FileChanged` | ❌ | Fichier modifié détecté |
| `PostToolBatch` | ❌ | Après lot d'appels outils |
| `Elicitation` / `ElicitationResult` | ❌ | Prompts saisie utilisateur |

**Pour intercepter une écriture de fichier** : utiliser `PreToolUse` avec `matcher: "Write|Edit|MultiEdit"` (triplet obligatoire, cf [[feedback_multiedit_matcher_blind_spot]]). Il n'existe **PAS** d'événements `PreEdit`/`PostEdit`/`PreWrite`/`PostWrite`/`PreBash`/`PostBash` séparés — tout passe par `PreToolUse`/`PostToolUse` avec matcher.

**`asyncRewake`** = option de retour d'un hook (réveille la session plus tard), **PAS un event**.

**`exit 1` n'est PAS bloquant** côté tools (seul `exit 2` l'est). Exception `WorktreeCreate` : tout non-zero abort.

### Exit codes

| Exit code | Effet |
|-----------|-------|
| **0** | Silent success |
| **1** | Visible (stderr remonté à user, NON bloquant) |
| **2** | **BLOCKING** — l'action Claude est annulée |
| Autre | Stderr remonté |

**Exception WorktreeCreate** : tout non-zero abort.

### Timeout

**60 secondes** (verbatim docs). Hook qui dépasse = killed.

### hookSpecificOutput

Format JSON spécifique selon event. Permet :
- Retour structuré au-delà de exit code
- Métadonnées additionnelles
- `decision: "block"` + `reason: "..."` pour Stop hook (sinon boucle infinie)

### asyncRewake

Réveille la session à un timing futur. Utile pour scheduling, polling externe.

---

## QUAND — Critère d'application (doctrine 22 mai forge)

### Créer un hook quand :

✅ **Lint / format** — règle déterministe sur le code (PostEdit/PostWrite)
✅ **Security** — credentials, secrets, IDOR, scope cross-repo (PreToolUse)
✅ **Scope guard** — empêcher accès hors-repo (PreToolUse Bash)
✅ **Validation déterministe** — pré-condition vérifiable mécaniquement
✅ **Notification side-effect** — logger, webhook, telemetry (PostToolUse)
✅ **Format frontmatter** — vérifier YAML valide

### NE PAS créer un hook quand (doctrine forge 22 mai 2026) :

❌ **Workflow agentique** (architect-first, TDD strict, commit gates) — anti-pattern Anthropic validé
❌ **Pipeline markers + guards** — anti-pattern, supprimé d'ia_back et neo_ia 22 mai
❌ **TTL sur markers** — existence seule suffit (cf [[feedback_marker_ttl_pattern]])
❌ **dispatch-guard CLAUDE_AGENT** — env var dead code (cf [[erreur-claude-agent-env-var-dead-code]])
❌ **Architect-guard allowlist** — supprimé (cf [[raisonnement-22mai-doctrine-vs-enforcement]])
❌ Pour ce qu'une **skill** ou un **rule** ferait (advisory)

### Référence doctrine forge

[[raisonnement-22mai-doctrine-vs-enforcement]] — pivot doctrinal du 22 mai 2026.

---

## WORKFLOW — Création étape par étape

### Étape 1 — Identifier la règle critique
- La règle DOIT-elle tenir 100% du temps ? Si non → CLAUDE.md ou skill
- La règle est-elle **déterministe** (vérifiable mécaniquement) ? Si non → impossible en hook

### Étape 2 — Choisir l'event
- Pour bloquer une écriture/édition → `PreToolUse` avec `matcher: "Write|Edit|MultiEdit"`
- Pour bloquer une commande Bash → `PreToolUse` avec `matcher: "Bash"`
- Pour formater après écriture → `PostToolUse` avec `matcher: "Write|Edit|MultiEdit"`
- Pour notifier en fin de turn → `Stop` (avec `once: true` sinon boucle)
- Pour bloquer un prompt user → `UserPromptExpansion` (exit 2)
- Pour réveiller la session plus tard → retour `asyncRewake` depuis un autre hook

### Étape 3 — Implémenter le script
- **Même stack que le projet** (Python si Python, Node si Node) — cf [[feedback_hooks_same_stack]]
- **Chemins absolus** dans settings.json (Windows alias MS Store sinon)
- **Timeout < 60s** — sinon killed
- **Exit code 2 pour bloquer**, **0 pour silent**, **1 pour visible non-bloquant**

### Étape 4 — Triplet matcher Write|Edit|MultiEdit
Pour les hooks PreToolUse sur les modifications de fichiers, **TOUJOURS** matcher `Write|Edit|MultiEdit`. Sans `MultiEdit`, trou architectural (cf [[feedback_multiedit_matcher_blind_spot]]).

### Étape 5 — Tests adverses
Tester :
- Cas heureux (le hook laisse passer ce qui doit passer)
- Cas adverses (le hook bloque ce qui doit être bloqué)
- Bypass tentatives (env var, heredoc, MultiEdit)

(cf [[feedback_tests_adverses_obligatoires]])

### Étape 6 — Déléguer à `hook-creator`
Côté forge : agent `hook-creator` génère la structure (pas bloqué par delegate-guard mais convention).

### Étape 7 — DA si livrable majeur (CONDITIONNEL, pas systématique)
Côté forge : `devils-advocate` UNIQUEMENT si livrable majeur (hook sécu critique, scope cross-repo). Doctrine 22 mai : pas de gates systématiques (cf [[raisonnement-22mai-doctrine-vs-enforcement]] + [[feedback_pipeline_quality_gates]]). DA reste **conditionnel ciblé**.

---

## APPELS — Composants mobilisés

- [[comment-ecrire-claudemd]] — où mentionner les hooks du repo
- [[comment-creer-agent]] — agents encadrés par hooks
- [[comment-creer-skill]] — skills complémentaires aux hooks
- [[workflow-claude-code-optimal]] — comment hooks s'inscrivent dans le workflow
- [[methode-analyser-repo]] — identifier les boundaries → hooks

---

## OPTIMISATION — 3 niveaux

### Niveau basique
- 1-2 hooks (lint/format PostEdit)
- Settings.json clean
- Chemins absolus
- Exit codes corrects

### Niveau avancé
- Triplet matcher Write|Edit|MultiEdit systématique
- Hooks security (scope guard, credentials detector)
- Tests adverses dans CI
- Stack identique au projet

### Niveau expert (Trail of Bits-style)
- **Anti-rationalization Stop hook** : Haiku check cop-outs sur session principale (Trail of Bits)
- **3-tier sandbox** : `/sandbox` builtin + devcontainer + dropkit DO
- **Hooks composés** : plusieurs hooks imparfaits qui ensemble couvrent les trous (Thariq "swiss cheese defense")
- **asyncRewake** pour scheduling autonome

---

## POURQUOI CETTE OPTIM — Gain mesurable

| Optim | Gain |
|-------|------|
| Hook bloquant vs rule advisory | 100% compliance vs ~80% (verbatim Anthropic) |
| Triplet matcher complet | 0 trou MultiEdit (vs blind spot avant) |
| Stack identique au projet | Pas de dep manager parallèle, debug plus simple |
| Chemins absolus settings | Marche multi-poste sans réécrire |
| Stop hook anti-rationalization | Haiku ~$0.001 par check, prévient erreurs cascadées (Trail of Bits) |
| Sensors (Fowler) | LangChain 52.8% → 66.5% Terminal Bench avec sensors seuls |

---

## ANTI-PATTERNS

### Doctrinaux (22 mai 2026 forge)
- ❌ **Hooks workflow agentique** (architect-first, TDD strict, commit gates)
- ❌ **Pipeline markers + guards** — supprimé d'ia_back et neo_ia 22 mai
- ❌ **TTL sur markers** — existence seule (cf [[feedback_marker_ttl_pattern]])
- ❌ **dispatch-guard CLAUDE_AGENT** — env var dead code
- ❌ **Architect-guard allowlist** — supprimé
- ❌ **Hooks user-level** pour workflow — toujours project-level

### Techniques
- ❌ **Matcher "Write|Edit"** sans MultiEdit — trou (cf [[feedback_multiedit_matcher_blind_spot]])
- ❌ **Chemin Python relatif** sur Windows — alias MS Store (cf [[feedback_python_path_windows]])
- ❌ **`exit 1` pour bloquer** — non bloquant, utiliser `exit 2`
- ❌ **Stop hook sans `once: true`** — boucle infinie (cf [[feedback_stop_hook_injection]])
- ❌ **Bash heredoc dans hook** Windows — boucle quoting Git Bash
- ❌ **Settings paths hardcodés** multi-poste — chemins relatifs ou env vars (cf [[erreur-settings-paths-hardcodes-multi-poste]])

### Architecture
- ❌ **Hook qui dépasse 60s** — killed sans warning
- ❌ **Hook qui consume tokens LLM** (Haiku check inutile sur tous les events) — réserver aux cas critiques
- ❌ **Hooks non testés adverses** — cas heureux ne suffit pas (cf [[feedback_tests_adverses_obligatoires]])

### Pédagogiques
- ❌ **Hook au lieu de skill** quand la règle est advisory (pas critique)
- ❌ **CLAUDE.md au lieu de hook** quand la règle est critique
- ❌ **Hook sans documentation** dans le repo (pourquoi il existe, quoi il bloque)

---

## EXEMPLES CONCRETS — Repos externes

### Trail of Bits (référence sécu)
[github.com/trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)
- **Anti-rationalization Stop hook** — pattern inédit : Haiku check cop-outs sur session principale
- **3-tier sandbox** : `/sandbox` builtin + devcontainer + dropkit DO
- Hooks lint/security uniquement, pas de workflow

### Anthropic officiel
- docs.claude.com/hooks — spec complète 29 events
- [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code) — config minimaliste, 3 slash commands

### Fowler / Böckeler
- [martinfowler.com](https://martinfowler.com) — Guides+Sensors 2 avril 2026
- Evidence LangChain : 52.8% → 66.5% Terminal Bench, harness changes seuls

### Patterns reconnus
- **Lint PostEdit** : prettier/black auto sur write
- **Format frontmatter YAML** validation
- **Scope guard PreToolUse Bash** : empêcher `cd ../../autre-repo`
- **Credentials detector** : grep secrets avant write

---

## SOURCES — Verbatim avec URLs

### Anthropic officiel
- [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) — spec 29 events
- docs.claude.com features-overview — "If a rule must hold every time, make it a hook"
- Timeout 60s, exit codes officiels

### Doctrine forge 22 mai 2026
- [[raisonnement-22mai-doctrine-vs-enforcement]] — pivot
- [[critique-2026-05-21-refonte-hooks-16-vers-6]] — historique pivot
- [[erreur-hooks-workflow-enforcement]] — anti-pattern documenté

### Martin Fowler / Birgitta Böckeler
- 2 avril 2026 — Guides+Sensors taxonomy
- "Agent = Model + Harness"
- LangChain evidence 52.8% → 66.5%

### Trail of Bits
- [github.com/trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)
- Anti-rationalization pattern (inédit)

### Thariq Shihipar
- Code with Claude SF 6-7 mai 2026 — Swiss cheese defense

---

## GOTCHAS — Pièges observés

### Pièges Windows
- **Path absolu Python obligatoire** dans settings.json (alias MS Store sinon, cf [[feedback_python_path_windows]])
- **Bash heredoc** : boucle quoting Git Bash (cf [[erreur-da-heredoc-bash-silencieux]])
- **Settings paths hardcodés** ne marchent pas multi-poste (cf [[erreur-settings-paths-hardcodes-multi-poste]])

### Pièges exit codes
- **`exit 1` n'est PAS bloquant** — seulement visible
- **`exit 2` est BLOQUANT** — l'action Claude est annulée
- **WorktreeCreate** : tout non-zero abort (exception)

### Pièges events
- **Stop hook sans `once: true`** = boucle infinie (cf [[feedback_stop_hook_injection]])
- **`additionalContext` non supporté** dans Stop hook — utiliser `decision: "block"` + `reason`
- **MultiEdit absent du matcher** = trou (cf [[feedback_multiedit_matcher_blind_spot]])
- **`agent_type` détection** : via stdin JSON, JAMAIS via env var (cf [[reference_agent_type_hook_detection]])

### Pièges architecture
- **Hook timeout 60s** strict
- **Hook qui consume tokens** (Haiku call) = coût caché, réserver
- **Sensors > Guides** : préférer hooks à rules quand critique

### Pièges délégation
- **Tests adverses obligatoires** (cf [[feedback_tests_adverses_obligatoires]])
- **DA AVANT push** sur hooks sécu critiques
- **Capturer $? immédiat** (pas via wrapper shell)

### Pièges classifier
- **Auto-mode classifier** : bloque self-modification de hooks via env var (cf [[reference_auto_mode_classifier]])
- **Secret en clair** dans .mcp.json/configs versionnés (cf [[feedback_secret_in_mcp_json]])

---

## ALIASES — Findability

Aliases déclarés en frontmatter (10) :
- comment creer hook
- creer un hook claude code
- create claude code hook
- hook parfait
- hook best practices
- 25+ events hooks
- exit codes hooks
- hookSpecificOutput
- asyncRewake
- guides sensors fowler

---

## WIKILINKS

### Notes canoniques sœurs
- [[comment-creer-skill]]
- [[comment-creer-agent]]
- [[comment-ecrire-claudemd]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[mcp-vs-skills-doctrine]]

### Fiches leaders (à créer)
- [[Martin Fowler]]
- [[Thariq Shihipar]]
- [[Trail of Bits config publique]]

### Knowledge / erreurs / refs
- [[raisonnement-22mai-doctrine-vs-enforcement]]
- [[erreur-hooks-workflow-enforcement]]
- [[critique-2026-05-21-refonte-hooks-16-vers-6]]
- [[erreur-claude-agent-env-var-dead-code]]
- [[raisonnement-22mai-doctrine-vs-enforcement]]
- [[feedback_marker_ttl_pattern]]
- [[feedback_multiedit_matcher_blind_spot]]
- [[feedback_hooks_same_stack]]
- [[feedback_python_path_windows]]
- [[feedback_stop_hook_injection]]
- [[feedback_tests_adverses_obligatoires]]
- [[erreur-da-heredoc-bash-silencieux]]
- [[erreur-settings-paths-hardcodes-multi-poste]]
- [[reference_agent_type_hook_detection]]
- [[reference_auto_mode_classifier]]
- [[feedback_secret_in_mcp_json]]

### Forge custom
- [[hook-creator]] — agent forge dédié
- [[devils-advocate-pipeline]] — rule DA après création

---

**Fin note canonique `comment-creer-hook.md`** — 5/8 chantier 22 mai 2026.
