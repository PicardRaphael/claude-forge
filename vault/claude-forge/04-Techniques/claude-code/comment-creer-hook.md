---
titre: "Comment créer un hook Claude Code parfait"
resume: "Note canonique pour créer un hook Claude Code — 29 events officiels (docs Anthropic), timeouts par type (600s/30s/60s), exit codes 0/1/2, hookSpecificOutput, doctrine 'If a rule must hold every time, make it a hook'. Lint/security/scope OUI, workflow NON (doctrine 22 mai)."
aliases:
  - "comment creer hook"
  - "creer un hook claude code"
  - "create claude code hook"
  - "hook parfait"
  - "hook best practices"
  - "29 events hooks"
  - "exit codes hooks"
  - "hookSpecificOutput"
  - "asyncRewake"
  - "guides sensors fowler"
derniere-maj: 2026-05-24
auteur: claude
type: technique
sources:
  - "https://code.claude.com/docs/en/hooks"
  - "docs.claude.com — features-overview"
  - "Birgitta Böckeler — martinfowler.com/articles/harness-engineering.html (2 avril 2026)"
  - "github.com/trailofbits/claude-code-config"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/hooks"
  - "#doctrine/2026"
---
# Comment créer un hook Claude Code parfait

> Note canonique forge — création de hooks selon doctrine Anthropic 22-23 mai 2026 + Böckeler.

---

> ⚠️ **Ordre canonique pour TOUTE création/modification de hook** : suivre A→B→C→D→E (analyser réel → lire canoniques EN ENTIER → croiser → plan d'écarts → exécuter). Cf [[methode-analyser-repo]] section **ORDRE CANONIQUE**. Pas de prescription avant analyse du réel.

## QUOI — Définition

**Hook** = commande shell, endpoint HTTP, ou prompt LLM exécuté automatiquement par Claude Code sur un événement du lifecycle. Verbatim docs Anthropic :

> "Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code's lifecycle."
> — [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)

Permet :
- **Validation déterministe** (bloquer une action invalide)
- **Sensor** (observer + collecter signaux)
- **Side-effect** (formater, notifier, logger)

**Verbatim Anthropic** (doctrine canonique) :

> "If a rule must hold every time, make it a hook rather than a prompt instruction."
> — docs Anthropic features-overview

C'est l'arbitrage central. Une règle dans CLAUDE.md ou une skill = **advisory** (compliance partielle, observée empiriquement autour de ~80% sur forge, ordre de grandeur indicatif sans mesure Anthropic publique). Un hook bloquant = **100% sur ce qu'il détecte mécaniquement**.

**Taxonomie Böckeler/Fowler (2 avril 2026)** :

| Type | Nature | Force |
|------|--------|-------|
| **Guides** | Inferential (prompts, rules) | Moyen — compliance partielle |
| **Sensors** | Computational (hooks, tests) | Fort — 100% sur ce qu'ils détectent |

Verbatim Böckeler : "the harness is everything in an AI agent **except the model itself**" — guides steer before action, sensors catch problems after. Source : [martinfowler.com/articles/harness-engineering.html](https://martinfowler.com/articles/harness-engineering.html)

---

## POURQUOI — Le problème résolu

Sans hooks, on accumule des règles advisory dans CLAUDE.md. Conséquences :
- **Compliance partielle** sur règles critiques (le LLM peut "oublier" ou être manipulé)
- **Trust-then-verify gap** — la règle existe mais rien ne la vérifie
- **Récurrence d'erreurs** — la session suivante refait l'erreur

Avec hooks bloquants sur règles critiques :
- **100% compliance** sur ce que le hook détecte mécaniquement
- **Détection précoce** (PreToolUse avant action)
- **Side-effects automatiques** (format, notify, log)

**Note honnêteté intellectuelle** : "~80% compliance advisory" = ordre de grandeur empirique observé sur forge, **pas une mesure Anthropic publique**. Le chiffre exact varie selon : longueur CLAUDE.md, position de la règle, ALL-CAPS, contexte de la session.

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

### Les 29 events officiels (source vérifiée verbatim docs Anthropic 23 mai 2026)

Source : [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) — section "Lifecycle events".

| # | Event | Bloquant | Phase |
|---|-------|----------|-------|
| 1 | `SessionStart` | ❌ | Lifecycle session |
| 2 | `Setup` | ❌ | Setup initial |
| 3 | `UserPromptSubmit` | ❌ | Prompt utilisateur reçu |
| 4 | `UserPromptExpansion` | ✅ exit 2 | Expansion du prompt |
| 5 | `PreToolUse` | ✅ exit 2 | Avant tout outil — intercepter Write/Edit/MultiEdit/Bash via `matcher` |
| 6 | `PermissionRequest` | ✅ | Avant demande permission |
| 7 | `PermissionDenied` | ❌ | Après refus auto-mode (`{retry: true}` pour relancer) |
| 8 | `PostToolUse` | ❌ | Après outil — formatage, lint, notifications |
| 9 | `PostToolUseFailure` | ❌ | Après échec outil |
| 10 | `PostToolBatch` | ❌ | Après lot d'appels outils |
| 11 | `Notification` | ❌ | Notification utilisateur |
| 12 | `SubagentStart` | ❌ | Sub-agent démarre |
| 13 | `SubagentStop` | ✅ (Stop) | Sub-agent finit |
| 14 | `TaskCreated` | ❌ | Task créée |
| 15 | `TaskCompleted` | ❌ | Task terminée |
| 16 | `Stop` | ✅ JSON block | Fin de turn (avec `decision: "block"` + `reason`) |
| 17 | `StopFailure` | ❌ (output ignoré) | Échec Stop hook |
| 18 | `TeammateIdle` | ❌ | Coéquipier inactif |
| 19 | `InstructionsLoaded` | ❌ | Chargement CLAUDE.md/rule |
| 20 | `ConfigChange` | ❌ | Config modifiée |
| 21 | `CwdChanged` | ❌ | Répertoire courant modifié |
| 22 | `FileChanged` | ❌ | Fichier modifié détecté |
| 23 | `WorktreeCreate` | ✅ (non-zero abort) | Création worktree |
| 24 | `WorktreeRemove` | ❌ | Suppression worktree |
| 25 | `PreCompact` | ❌ | Avant compression contexte |
| 26 | `PostCompact` | ❌ | Après compression contexte |
| 27 | `Elicitation` | ❌ | Prompt saisie utilisateur |
| 28 | `ElicitationResult` | ❌ | Résultat saisie |
| 29 | `SessionEnd` | ❌ | Fin session |

**Pour intercepter une écriture de fichier** : utiliser `PreToolUse` avec `matcher: "Write|Edit|MultiEdit"` (triplet obligatoire, cf [[feedback_multiedit_matcher_blind_spot]]). Il n'existe **PAS** d'événements `PreEdit`/`PostEdit`/`PreWrite`/`PostWrite`/`PreBash`/`PostBash` séparés — tout passe par `PreToolUse`/`PostToolUse` avec matcher.

**`asyncRewake`** = option de retour d'un hook (réveille la session plus tard), **PAS un event**.

**`exit 1` n'est PAS bloquant** côté tools (seul `exit 2` l'est). Exception `WorktreeCreate` : tout non-zero abort.

### Exit codes (verbatim docs)

> "**Exit 0** means success. Claude Code parses stdout for JSON output fields..."
> "**Exit 2** means a blocking error. Claude Code ignores stdout and any JSON in it. Instead, stderr text is fed back to Claude as an error message."
> "For most hook events, only exit code 2 blocks the action. Claude Code treats exit code 1 as a non-blocking error and proceeds with the action, even though 1 is the conventional Unix failure code. If your hook is meant to enforce a policy, use `exit 2`."

| Exit code | Effet |
|-----------|-------|
| **0** | Silent success |
| **1** | Visible (stderr remonté à user, NON bloquant) |
| **2** | **BLOCKING** — l'action Claude est annulée |
| Autre | Non-bloquant — `<hook name> hook error` + première ligne stderr |

**Exception WorktreeCreate** : tout non-zero abort.

### Timeouts (verbatim docs 23 mai 2026)

> "`timeout` | no | Seconds before canceling. Defaults: 600 for `command`, `http`, and `mcp_tool`; 30 for `prompt`; 60 for `agent`. UserPromptSubmit lowers the `command`, `http`, and `mcp_tool` default to 30"

| Type hook | Timeout défaut | Note |
|-----------|---------------|------|
| `command` | **600s** | 30s pour UserPromptSubmit |
| `http` | **600s** | 30s pour UserPromptSubmit |
| `mcp_tool` | **600s** | 30s pour UserPromptSubmit |
| `prompt` (LLM-based, ex: anti-rationalization Trail of Bits) | **30s** | — |
| `agent` | **60s** | — |

Hook qui dépasse son timeout = killed.

### hookSpecificOutput

Format JSON spécifique selon event. Permet :
- Retour structuré au-delà de exit code
- Métadonnées additionnelles
- `decision: "block"` + `reason: "..."` pour Stop hook (sinon boucle infinie)

### `once: true` — règle CRITIQUE (verbatim docs)

> "`once` | no | If `true`, runs once per session then is removed. **Only honored for hooks declared in skill frontmatter; ignored in settings files and agent frontmatter**"

**Conséquence pratique** :
- `once: true` dans **skill frontmatter** → honoré
- `once: true` dans `.claude/settings.json` → **silencieusement ignoré**
- `once: true` dans agent frontmatter → **silencieusement ignoré**

→ Pour un Stop hook dans `settings.json`, utiliser `decision: "block"` + `reason: "..."` (pas `once: true`).

### asyncRewake

Réveille la session à un timing futur. Utile pour scheduling, polling externe.

---

## QUAND — Critère d'application (doctrine 22 mai forge)

### Créer un hook quand :

✅ **Lint / format** — règle déterministe sur le code (PostToolUse Write/Edit/MultiEdit)
✅ **Security** — credentials, secrets, IDOR, scope cross-repo (PreToolUse)
✅ **Scope guard** — empêcher accès hors-repo (PreToolUse Bash)
✅ **Validation déterministe** — pré-condition vérifiable mécaniquement
✅ **Notification side-effect** — logger, webhook, telemetry (PostToolUse)
✅ **Format frontmatter** — vérifier YAML valide

**Note** : la phrase "Hooks are deterministic and are recommended for lint, test, and security" parfois citée comme verbatim Anthropic n'apparaît pas textuellement sur `code.claude.com/docs/en/hooks` (vérifié 23 mai 2026). C'est une **paraphrase pédagogique** du principe "hook bloquant pour règle 100% déterministe", convergente avec la doctrine officielle.

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
- Pour notifier en fin de turn → `Stop` (avec `decision: "block"` + `reason` ou skill `once: true`)
- Pour bloquer un prompt user → `UserPromptExpansion` (exit 2)
- Pour réveiller la session plus tard → retour `asyncRewake` depuis un autre hook

### Étape 3 — Implémenter le script
- **Même stack que le projet** (Python si Python, Node si Node) — cf [[feedback_hooks_same_stack]]
- **Chemins absolus** dans settings.json (Windows alias MS Store sinon)
- **Timeout < limite par type** — sinon killed
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
- 1-2 hooks (lint/format PostToolUse)
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
- **Hooks composés** : plusieurs hooks imparfaits qui ensemble couvrent les trous ("swiss cheese defense" — concept général cybersécurité repris dans l'écosystème Claude Code)
- **asyncRewake** pour scheduling autonome

---

## POURQUOI CETTE OPTIM — Gain mesurable

| Optim | Gain |
|-------|------|
| Hook bloquant vs rule advisory | 100% compliance vs compliance partielle (verbatim Anthropic : "If a rule must hold every time, make it a hook") |
| Triplet matcher complet | 0 trou MultiEdit (vs blind spot avant) |
| Stack identique au projet | Pas de dep manager parallèle, debug plus simple |
| Chemins absolus settings | Marche multi-poste sans réécrire |
| Stop hook anti-rationalization | Haiku check rapide, prévient erreurs cascadées (Trail of Bits) |
| Sensors (Böckeler) | LangChain harness changes : 52.8% → 66.5% Terminal Bench (Vivek Trivedy LangChain blog 17 fév 2026, modèle GPT-5.2-Codex) |

---

## HOOKS TRANSVERSAUX — Catalogue à proposer en audit repo

Catalogue de hooks réutilisables cross-repo. Lors d'un audit `.claude/` (via `project-auditor`, `project-analyzer`, `cc-advisor`), proposer ces hooks au repo audité si applicable et absent.

| Hook | Cas d'usage | Quand proposer en audit |
|------|-------------|-------------------------|
| `meta-commentary-detector.py` | Bloque justifications/sources/attributions dans CLAUDE.md, skills, agents, hooks, rules. Convertit doctrine "pas de meta" en enforcement 100%. | Tout repo avec CLAUDE.md > 50L OU vault canonique séparé |
| `delegate-guard.py` | Force délégation aux agents spécialisés (skill-creator, agent-creator, hook-creator, claudemd-optimizer) sur édit direct. | Tout repo avec >5 skills OU >5 agents |
| `repo-scope-guard.py` | Empêche Bash `cd ../../autre-repo`. Sécurité scope cross-repo. | Repos voisins partageant un dossier parent (ex: neot-v2/*) |
| `vault-query-guard.py` | Bloque Write si vault canonique pas consulté récemment (60min marker). | Repos avec vault canonique externe (forge-brain, neoteem-brain) |
| `credentials-detector` (lint pattern) | Grep secrets connus avant Write/Edit. | TOUT repo sans exception |
| `multiedit-triplet-checker` | Vérifie matcher `Write|Edit|MultiEdit` complet dans settings.json. | Repos avec hooks PreToolUse existants (audit de cohérence) |

### Comment proposer en audit

Après identification d'un écart entre règle advisory et compliance observée :

```
Tu as une règle X en CLAUDE.md/skill mais pas de hook qui l'enforce.
Veux-tu ajouter un hook `<nom>` qui transforme advisory → 100% ?
Précédent : repo Y l'utilise depuis Z. Coût : ~N lignes Python + entry settings.json.
```

Format : présenter UN hook par écart identifié, avec justification empirique. Pas de batch "tiens, ajoute ces 6 hooks". Sélectif.

### Anti-patterns proposition hooks transversaux

- ❌ Proposer un hook workflow agentique (cf doctrine 22 mai)
- ❌ Proposer un hook sans avoir vu l'écart empirique (proposition pour proposition)
- ❌ Proposer N hooks d'un coup (batch overwhelm)
- ❌ Ne PAS proposer alors qu'un trou évident existe (régression de la posture Jarvis)

### Référence forge

Source canonique du catalogue : cette section. Pour le détail d'implémentation de chaque hook, voir `.claude/hooks/<nom>.py` du repo claude-forge (référence) ou la note dédiée si elle existe.

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
- ❌ **`once: true` dans settings.json ou agent frontmatter** — silencieusement ignoré, utiliser `decision: "block"` + `reason`
- ❌ **Bash heredoc dans hook** Windows — boucle quoting Git Bash
- ❌ **Settings paths hardcodés** multi-poste — chemins relatifs ou env vars (cf [[erreur-settings-paths-hardcodes-multi-poste]])

### Architecture
- ❌ **Hook qui dépasse son timeout par type** — killed sans warning (600s command/http/mcp_tool, 30s prompt, 60s agent)
- ❌ **Hook qui consume tokens LLM** (Haiku check inutile sur tous les events) — réserver aux cas critiques
- ❌ **Hooks non testés adverses** — cas heureux ne suffit pas (cf [[feedback_tests_adverses_obligatoires]])
- ❌ **Hook qui modifie le filesystem du repo en cours de turn** — race condition avec Write/Edit Claude. Si un hook PostToolUse formate un fichier que Claude vient d'écrire, Claude peut ne pas voir la version formatée et écraser sur le tour suivant. Solution : formater silencieusement (exit 0) ET informer Claude via stderr du changement.

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
- [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) — spec complète 29 events
- [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code) — config minimaliste

### Böckeler / Fowler
- [martinfowler.com/articles/harness-engineering.html](https://martinfowler.com/articles/harness-engineering.html) — Guides+Sensors 2 avril 2026
- Concept "Agent = Model + Harness" : popularisé par Hashimoto (5 fév 2026), formalisé par LangChain, repris par Böckeler

### Patterns reconnus
- **Lint PostToolUse** : prettier/black auto sur write
- **Format frontmatter YAML** validation
- **Scope guard PreToolUse Bash** : empêcher `cd ../../autre-repo`
- **Credentials detector** : grep secrets avant write

---

## SOURCES — Verbatim avec URLs

### Anthropic officiel
- [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) — spec 29 events, timeouts, exit codes, `once: true` scope
- docs.claude.com features-overview — "If a rule must hold every time, make it a hook"

### Doctrine forge 22 mai 2026
- [[raisonnement-22mai-doctrine-vs-enforcement]] — pivot
- [[critique-2026-05-21-refonte-hooks-16-vers-6]] — historique pivot
- [[erreur-hooks-workflow-enforcement]] — anti-pattern documenté

### Böckeler / Fowler
- [martinfowler.com/articles/harness-engineering.html](https://martinfowler.com/articles/harness-engineering.html) — Guides+Sensors taxonomy 2 avril 2026
- Hashimoto [mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey) — popularisation "harness engineering"

### Trail of Bits
- [github.com/trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)
- Anti-rationalization pattern (inédit)

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
- **`once: true` honoré UNIQUEMENT en skill frontmatter** — ignoré silencieusement dans settings.json et agent frontmatter
- **Stop hook sans `decision: "block"` + `reason`** dans settings.json = potentielle boucle (utiliser `additionalContext` non supporté, préférer `decision`)
- **MultiEdit absent du matcher** = trou (cf [[feedback_multiedit_matcher_blind_spot]])
- **`agent_type` détection** : via stdin JSON, JAMAIS via env var (cf [[reference_agent_type_hook_detection]])

### Pièges architecture
- **Timeouts par type** : 600s command/http/mcp_tool, 30s prompt, 60s agent (UserPromptSubmit abaisse 600s→30s pour command/http/mcp_tool)
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
- 29 events hooks
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
- [[Birgitta Böckeler]]
- [[Mitchell Hashimoto]]
- Trail of Bits config publique — note canonique forge sur leur setup (à créer)

### Knowledge / erreurs / refs
- [[raisonnement-22mai-doctrine-vs-enforcement]]
- [[erreur-hooks-workflow-enforcement]]
- [[critique-2026-05-21-refonte-hooks-16-vers-6]]
- [[erreur-claude-agent-env-var-dead-code]]
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

**Fin note canonique `comment-creer-hook.md`** — révisée 23 mai 2026 post-audit thématique vault.


## Critiques DA

- [[critique-2026-05-22-guard-ddl-ban]] — Verdict KEEP sur guard-ddl-ban.py avec 3 corrections mineures. Différenciation clé : gate security légitime (DDL prod = irréversible) ≠ workflow agentique sur méta-doctrine.
