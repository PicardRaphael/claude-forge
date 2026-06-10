---
derniere-maj: 2026-06-07
---
﻿---
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
derniere-maj: 2026-05-27
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

> ⚠️ **Pivot 6 juin 2026** : `hook-creator` est désormais une **skill** (`.claude/skills/hook-creator/`). Invoquer via `Skill(hook-creator)` depuis la session principale. L'agent `hook-creator` est supprimé. `cc-hooks-ref` reste comme référence technique (29 events, formats JSON) — la skill `hook-creator` y accède via MCP vault.


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
#### Ratio adverse/happy ≥ 3:1 pour hooks sécu/contrôle

Un hook de sécurité ou de contrôle (security-guard, delegate-guard, scope-guard) DOIT avoir une suite de tests **majoritairement adverse** : ≥ 75% de tentatives de bypass, ≤ 25% de happy path. Le happy path seul est trompeur — il prouve que le légitime passe, jamais que l'illégitime est bloqué.

**Piège du 3:1 artificiel** : ne pas gonfler le ratio avec des tests hors-scope. Un hook ne promet de couvrir qu'un périmètre déclaré. Tester 30 patterns que le hook n'a jamais prétendu attraper (ex : `dd`, `mkfs`, base64 sur un security-guard qui ne couvre que 6 regex `rm`/`git`) = 30 confirmations sans valeur. Le vrai 3:1 = **≥ 3 variations de bypass par pattern réellement claimed**.

**Trois catégories de tests à distinguer** :
| Catégorie | Compte dans le 3:1 ? | Exemple |
|-----------|---------------------|---------|
| Adverse in-scope (false negative tenté) | OUI | espaces multiples, tabs, ordre des flags, casse, chemin équivalent |
| Adverse in-scope (false positive / over-block) | OUI | commande légitime que le regex trop large bloque |
| Caractérisation de bug/faiblesse | OUI (épingle le comportement, ne le masque PAS) | substring match qui accorde un bypass indu |
| Happy path | NON (≤ 25%) | commande bénigne passe, légitime passe |
| Gap hors-scope (connu, volontaire) | NON — **un seul** test énumérant | patterns non couverts par design |

**Caractérisation, pas masquage** : si un test révèle un vrai bug dans le hook, NE PAS l'aplatir pour faire passer le test. Épingler le comportement ACTUEL (`assert ok is True  # current buggy behavior`), documenter pourquoi dans le docstring, et lister le bug dans le résumé. Quand le hook est durci, on inverse l'assertion.

**Docstring de scope obligatoire** : en tête du fichier de test, lister (1) le périmètre déclaré du hook, (2) ce que les tests NE vérifient PAS (gaps hors-scope), pour qu'un futur lecteur sache que l'omission est délibérée.

**Testabilité** : un hook doit exposer sa logique en fonctions pures importables (`is_dangerous`, `required_agent`) avec le traitement stdin dans un `main()` gardé par `if __name__ == "__main__"`. Sinon `importlib` déclenche les effets de bord (lecture stdin, `sys.exit`) à l'import. Référence : `delegate-guard.py` (structuré) vs security-guard avant refactor 27 mai (logique au niveau module → non importable).

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

Catalogue de hooks réutilisables cross-repo. Lors d'un audit `.claude/` (via `repo-inspector` mode=audit/analyze, `cc-advisor`), proposer ces hooks au repo audité si applicable et absent.

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

### Faux positifs de scope — émergent à l'usage, pas à la conception

Un hook-garde qui matche **trop large** (par nom de fichier, regex, ou scope de périmètre) produit des faux positifs **invisibles à la conception** — ils n'apparaissent qu'à l'usage réel, sur un cas que le concepteur n'avait pas en tête. Pattern récurrent forge (5 incidents) :

| Hook | Faux positif | Cause |
|------|-------------|-------|
| `vault-cat-guard` | bloque `cat memory/` si la commande contient « vault » | match sur mot-clé, pas chemin (cf [[feedback_vault_cat_guard_faux_positif_memory]]) |
| garde hors-vault | attrape le plan file `~/.claude/plans/` | périmètre strict sans exception plan mode (cf [[erreur-hook-garde-hors-vault-bloque-plan-file]]) |
| `meta-commentary-detector` | flagge le mot « source: » légitime | regex source trop large (cf [[critique-2026-05-24-regex-source-faux-positifs]]) |
| `vault-before-specialist` | scope gonflé + TTL 60min | `is_specialist` trop permissif (cf [[erreur-vault-before-specialist-ttl-scope]]) |
| `delegate-guard` | bloque Edit d'une **note vault** `04-Techniques/agents/agents-architecture.md` | match `agents/*.md` PAR NOM → confond note vault et sous-agent `.claude/agents/` |

**Leçons structurelles** :
- **Matcher par chemin complet**, jamais par nom de fichier ou mot-clé isolé (un nom `agents-*.md` existe dans le vault ET dans `.claude/agents/`).
- **Tester adverse AVANT** : le cas heureux ne révèle jamais le faux positif. Lister les fichiers/commandes légitimes qui ressemblent à la cible.
- **Exception explicite en tête** du hook pour les cas légitimes connus (plan file, memory/, notes vault).
- **Contournement runtime** : pour modifier le CONTENU d'une note vault bloquée par un faux positif de nom, passer par les outils MCP forge-brain (`insert_section`/`update_note`), pas par Edit direct — JAMAIS contourner par env var/script (cf rule delegate-to-specialists).
- Corollaire : « les vrais faux positifs émergent à l'usage » → traiter chaque blocage inattendu comme un signal de scope trop large, pas comme un cas à contourner.

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

## ADAPTATION OS + STACK — RÈGLE D'OR (source: research LLM juin 2026)

Un hook exécute du **code réel** — il est OS-spécifique ET stack-spécifique. **DEMANDER avant de générer, jamais supposer.**

### Questions obligatoires avant tout hook

1. **OS** : Windows / macOS / Linux / cross-machine (repo partagé plusieurs OS) ?
2. **Stack** : Python / TypeScript-JS / Go / Rust / autre ?

### Matrice OS

| | Windows | macOS / Linux | Cross-machine |
|---|---|---|---|
| **Interpréteur Python** | `py "..."` (launcher) | `python3 "..."` | wrapper qui détecte l'OS |
| **Shebang** | ignoré | `#!/usr/bin/env python3` + `chmod +x` | shebang + appel explicite |
| **Chemins** | jamais `C:\...` (Bash mange `\`) | `/` natif | toujours `${CLAUDE_PROJECT_DIR}` + slashs |
| **Notification audio** | `rundll32 user32.dll,MessageBeep` | `afplay` / `paplay` | conditionner sur l'OS |
| **`shell:` du hook** | `powershell` possible | `bash` | `bash` (défaut) |

### Matrice STACK — lint / test / format

| Stack | Lint | Format | Test | Extensions |
|---|---|---|---|---|
| **Python** | `ruff` / `pyflakes` | `ruff format` / `black` | `pytest` | `.py` |
| **TypeScript / JS** | `eslint` | `prettier` | `vitest` / `jest` | `.ts .tsx .js` |
| **Go** | `go vet` | `gofmt` | `go test` | `.go` |
| **Rust** | `clippy` | `rustfmt` | `cargo test` | `.rs` |

### Règles cross-machine universelles

```python
# Résolution chemin via __file__, jamais en dur
_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)
```

- Toujours `${CLAUDE_PROJECT_DIR}` + slashs, jamais de chemin absolu OS-spécifique
- **Fail-open** : toute exception → `sys.exit(0)` silencieux (sauf hook sécu où fail dur est voulu)
- `shutil.which("ruff")` avant d'appeler un outil — skip proprement s'il manque
- Pour cross-machine : wrapper Python qui détecte l'OS plutôt que commande shell dans settings.json

---

## PATTERNS — 5 usages types

### Pattern A — Sécurité (PreToolUse, exit 2)
```python
#!/usr/bin/env python3
import json, sys, re
data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")
DANGER = [r"\brm\s+-rf\b", r"git\s+push.*--force", r"git\s+branch\s+-D\b"]
for pat in DANGER:
    if re.search(pat, cmd):
        print(f"BLOQUÉ : pattern destructeur. Demande explicitement.", file=sys.stderr)
        sys.exit(2)   # exit 2 = blocage RÉEL
sys.exit(0)
```

### Pattern B — Qualité / lint (PostToolUse Write|Edit|MultiEdit)
PostToolUse ne peut pas annuler (action déjà faite) — il renvoie un feedback que Claude corrige.
Toujours le triplet `Write|Edit|MultiEdit` dans le matcher (sans MultiEdit = trou architectural).

### Pattern C — Injection de contexte (UserPromptSubmit → stdout → contexte)
```python
#!/usr/bin/env python3
import sys
print("RAPPEL : si une skill couvre ce sujet, invoque-la avant d'agir.")
sys.exit(0)  # stdout ajouté au contexte sur UserPromptSubmit
```

### Pattern D — Vérification subagent (SubagentStop, exit 0 + JSON)
```python
#!/usr/bin/env python3
import json, sys, os
d = json.load(sys.stdin)
if d.get("stop_hook_active"): sys.exit(0)  # anti-boucle OBLIGATOIRE
tp = d.get("agent_transcript_path", "")
try:
    with open(os.path.expanduser(tp)) as f:
        if any('"name": "Skill"' in l for l in f):
            sys.exit(0)
    print(json.dumps({"decision":"block","reason":"Invoque la skill requise puis termine."}))
    sys.exit(0)  # exit 0 + JSON (pas exit 2 — sinon JSON ignoré)
except Exception:
    sys.exit(0)
```

### Pattern E — Survie compaction (SessionStart compact → additionalContext)
Réinjecter le contexte critique après compaction via `additionalContext` dans hookSpecificOutput.

---

## CHECKLIST HOOK PARFAIT — 4 dimensions

### 0. Décision — Faut-il vraiment un hook ?

- [ ] La règle doit tenir **à 100% mécaniquement** ? → hook. Sinon → rule/CLAUDE.md (advisory)
- [ ] C'est du lint / sécurité / scope / format / logging / injection de rappel ? → hook OK
- [ ] C'est du workflow agentique (architect-first, TDD, commit gates, markers TTL) ? → STOP, utiliser agent/skill à la place
- [ ] Les hooks ne fonctionnent **PAS** dans Desktop app / Cowork → confirmer que la cible est bien le CLI

### 1. Fonctionnement

- [ ] Bon événement : PreToolUse (bloquer), PostToolUse (réagir), Stop/SubagentStop (forcer)
- [ ] **exit 2 pour bloquer** (PreToolUse) — jamais exit 1 (ne bloque JAMAIS, bug n°1)
- [ ] **exit 0 + JSON `{"decision":"block","reason":"..."}` pour Stop/SubagentStop** (garde le reason riche)
- [ ] `stop_hook_active` vérifié sur Stop/SubagentStop (anti-boucle infinie — cap natif 8 blocages)
- [ ] Choix UNIQUE : code retour OU JSON, pas les deux
- [ ] Triplet matcher `Write|Edit|MultiEdit` si PostToolUse écriture (sans MultiEdit = trou)

### 2. Adaptation OS & stack (demander d'abord, jamais supposer)

- [ ] OS demandé et confirmé (Windows / mac / Linux / cross-machine)
- [ ] Stack demandée (Python / TS / Go / Rust…)
- [ ] Interpréteur adapté (`py` Windows, `python3` mac/linux)
- [ ] Outils lint/test de la BONNE stack (`ruff`/`pytest` vs `eslint`/`tsc`)
- [ ] `${CLAUDE_PROJECT_DIR}` + slashs — jamais `C:\...`
- [ ] Chemins via `__file__` dans le script Python
- [ ] `shutil.which()` avant appel outil — fail-open si absent
- [ ] Fail-open (`sys.exit(0)` sur exception) — sauf hook sécu

### 3. Performance & robustesse

- [ ] Rapide (< 500 ms — gate chaque appel d'outil)
- [ ] `timeout` défini dans settings.json
- [ ] Testé en déclenchant réellement le pattern (bloqué, pas juste warné)
- [ ] Enregistrement vérifié via `/hooks`
- [ ] Si distribué en plugin et Stop hook KO → installer depuis `.claude/hooks/` (bug #10412)

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


---

## AJOUT 24 mai 2026 — Pattern SubagentStop suggesteur "hooks suggest, humans approve"

**Verbatim Anthropic** (PubNub Part II + doctrine officielle) :

> "Hooks suggest, humans approve: the hook prints 'Use the architect-review subagent on X.' A human pastes it to proceed, preventing runaway chains and forcing a quick glance."

### Pattern d'usage

Hook `SubagentStop` qui **détecte** des signaux dans la sortie du sub-agent et **imprime en stderr** une suggestion non-bloquante (exit 0). La session principale voit, décide.

**Cas d'usage** :
- Détecter `## ESCALADE REQUISE` ou `## AMBIGUÏTÉ DÉTECTÉE` dans la sortie sub-agent → suggérer action suivante
- Compter le nombre d'invocations sub-agent par type → métriques observability
- Lire un fichier d'état (queue.json, STATUS) → suggérer prochain agent du pipeline

### Implémentation déployée 24 mai 2026

- **neo_ia** : `.claude/hooks/escalade-detector.py` (Python) — détecte 3 markers, écrit suggestion stderr
- **ia_back** : `.claude/hooks/escalade-detector.ts` (Bun/TypeScript) — équivalent
- Settings.json : enregistrement dans `SubagentStop` (async possible, non-bloquant obligatoire)

### Anti-pattern

❌ **SubagentStop bloquant** (exit 2) = workflow gate déguisé, viole doctrine 22 mai. Le hook DOIT être exit 0 toujours.
❌ **Forcer l'invocation du prochain sub-agent** depuis le hook = anti-pattern. Le hook suggère, l'humain (ou la session principale qui lit le stderr) décide.

### Configuration settings.json type

```json
"SubagentStop": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "uv run python .claude/hooks/escalade-detector.py"
      }
    ]
  }
]
```

### Sources

- [PubNub Best Practices Part II](https://www.pubnub.com/blog/best-practices-claude-code-subagents-part-two-from-prompts-to-pipelines/) — Pipeline architect → implementer avec SubagentStop suggester
- [Anthropic Hooks reference](https://code.claude.com/docs/en/hooks)
- [[anti-reentrance-sub-agents-pattern-escalade]] — Format markers détectés
- [[raisonnement-22mai-doctrine-vs-enforcement]] — doctrine non-bloquante respectée


---

## AJOUT 27 mai 2026 — Résolution de path dans un hook : `__file__`, jamais `os.environ["CLAUDE_PROJECT_DIR"]`
Quand un hook Python doit résoudre la racine du repo (pour cibler `<repo>/memory/`, lire un fichier du repo, etc.), le mécanisme correct est `__file__` :

```python
_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))  # .claude/hooks/
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)                 # .claude/
repo_root = os.path.dirname(_CLAUDE_DIR)                 # <repo>/
```

**JAMAIS `os.environ["CLAUDE_PROJECT_DIR"]`** : non garanti peuplé dans le process du hook (prior art forge : `grep CLAUDE_PROJECT_DIR .claude/hooks/` → 0 match, tous les hooks utilisent `__file__` ou stdin JSON). L'expansion de `${CLAUDE_PROJECT_DIR}` dans la string `command` de settings.json n'implique PAS sa présence dans `os.environ` du process enfant — les deux sont indépendants.

`__file__` est aussi supérieur à `git rev-parse` pour un hook : **robuste au cwd**. Un hook peut être déclenché avec un cwd imprévisible ; `__file__` pointe toujours vers l'emplacement réel du script (prouvé 27 mai : `session-reminder.py` lancé depuis `/tmp` trouve quand même sa mémoire, là où `git rev-parse` aurait échoué hors-repo).

Distinct de [[reference_agent_type_hook_detection]] (détection du TYPE d'agent via stdin JSON) — ici il s'agit de résolution de CHEMIN. Table complète des 4 contextes : [[resolution-path-3-contextes]].

Appliqué 27 mai : hook `session-reminder.py` migré de `glob.glob("~/.claude/projects/*/...")` vers chemin déterministe `__file__`-based (chantier mémoire portable, cf [[architecture-decision-memoire-portable-import]]).

## AJOUT 27 mai 2026 — Brief sub-agent et accès vault

Un sub-agent ne peut pas lire le vault : le `mcp__forge-brain__*` de son frontmatter est décoratif (MCP non connecté en sous-agent, `No such tool available` — vérifié Chantier A 27 mai). Tout brief sub-agent impliquant le vault contient les extraits canoniques **inline** + « si manque, ESCALADE ; jamais cat/find/grep/Read le vault ». Ne jamais écrire « lis via MCP » dans le body d'un creator.

Enforcement : hook `vault-cat-guard.py` (PreToolUse Bash|Read) bloque l'accès brut au vault dans les 2 contextes, exempte vault-maintainer. Preuve d'interception : [[hook-intercepte-mcp-et-read-tools]]. Cause-racine complète : [[pattern-mcp-brief-then-direct]].



---

## AJOUT 7 juin 2026 — Correction count events (30) + fiabilité handlers http/mcp + champ `continue` universel

Source primaire revérifiée le 7 juin 2026 : [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks).

### Count events : 30 (et non 29)

La doc Anthropic liste désormais **30 events**. Le tableau « 29 events » plus haut ratait **`MessageDisplay`** (#12 dans la liste à jour, entre `Notification` et `SubagentStart`). Liste complète à jour : SessionStart, Setup, UserPromptSubmit, UserPromptExpansion, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, PostToolBatch, Notification, **MessageDisplay**, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, Elicitation, ElicitationResult, SessionEnd.

> Le compte d'events bouge par version CC — toujours revérifier à la source primaire avant de citer un chiffre exact (29 = instantané 23 mai, 30 = 7 juin).

### Handlers http / mcp_tool : ÉCHOUENT OUVERT (non-bloquant)

Nuance critique pour l'enforcement DUR, vérifiée verbatim :
- **http** : « Non-2xx status: non-blocking error, execution continues » et « Connection failure or timeout: non-blocking error, execution continues ». Pour bloquer, il faut renvoyer un 2xx avec un body JSON bloquant — le code de statut seul ne bloque jamais.
- **mcp_tool** : « If the named server is not connected, or the tool returns `isError: true`, the hook produces a non-blocking error and execution continues. »

**Conséquence** : pour une politique qui DOIT tenir même sous panne réseau/serveur déconnecté, utiliser un handler **`command` + `exit 2`** (déterministe, local). `http`/`mcp_tool`/`prompt`/`agent` = jugement nuancé, **jamais** garantie d'enforcement. Cf le feedback `mcp-transport-stdio-http-crashloop` (MCP non fiable en contexte headless).

### Champ `continue: false` — universel, précède tout

`{"continue": false, "stopReason": "..."}` fonctionne **sur tous les events** et **précède tout champ de décision event-spécifique** (verbatim : « Takes precedence over any event-specific decision fields »). `stopReason` est montré à l'utilisateur (pas à Claude). Distinct du `decision: "block"` (event-spécifique Stop/SubagentStop/PostToolUse) : `continue:false` arrête tout le traitement, quel que soit l'event.

**Source de cet ajout** : réconciliation du doc `Important/reference-hooks-claude-code.md` (déplacé/supprimé après absorption des deltas dans cette canonique, 7 juin 2026 — enrich-first cf [[feedback_lire_fichier_entier_avant_verdict]]).


---

## AJOUT 10 juin 2026 — Répartition des checks par event : PostToolUse = rapide, Stop = lourd (mesuré en production)

Incident fondateur : US1 neoteem-back-ts, ~1h30 au lieu de ~30 min. Causes mesurées : `tsc --noEmit` en PostToolUse (~1s × chaque Write), 3 hooks Python chaînés sur chaque Bash (~1,4s de pur démarrage interpréteur), et l'agent dev qui relançait lint/tests après chaque fichier.

### La règle de placement (état de l'art convergent Boris + guides hooks 2026)

| Check | Event | Pourquoi |
|---|---|---|
| Format/lint d'UN fichier (biome, ruff, prettier) | PostToolUse (< 500 ms, async si possible) | Boris : « PostToolUse hook pour formater automatiquement — évite que l'agent relance le lint lui-même » |
| **Typecheck, suite de tests, analyse lourde** | **Stop UNIQUEMENT** (une fois par tour, `stop_hook_active` guard, erreurs → `decision: block`) | « Don't put tsc --noEmit in a PostToolUse hook. 50 edits × 10-30s = 25 min de wall-clock perdues » (Wiegold, mai 2026) |
| Sécurité/scope (bloquer une commande) | PreToolUse exit 2 | inchangé |

Seuil ressenti : un PostToolUse qui ajoute > 500 ms à chaque edit rend la session poussive.

### Coût du spawn interpréteur (mesuré Windows, 10 juin 2026)

`uv run python` ≈ 450-640 ms · `py` (launcher) ≈ 454 ms · `python` direct ≈ 236-253 ms · hooks empilés sur un matcher large (ex. 3 hooks sur chaque Bash) = coûts ADDITIFS. Leviers : interpréteur direct quand les hooks n'utilisent que la stdlib (caveat : alias MS Store → vérifier `python --version` par poste), fusionner les hooks chaînés d'un même matcher en un dispatcher unique (1 spawn au lieu de N), `timeout` partout (anti-freeze).

### Gotcha vérifié : `git diff --name-only HEAD` rate les fichiers NEUFS

Un hook Stop qui découvre « ce qui a changé » via git diff manque les fichiers non trackés (ceux que l'agent vient de créer). Ajouter `git ls-files --others --exclude-standard`. Découvert par test adverse (fichier cassé neuf → hook silencieux).

### Sources

- [How Boris Uses Claude Code](https://howborisusesclaudecode.com/) — PostToolUse format hook, vérification en fin de tâche (Stop hook / background agent / ralph loop)
- [Thomas Wiegold — Claude Code Hooks](https://thomas-wiegold.com/blog/claude-code-hooks/) — le piège tsc en PostToolUse, split par event
- [Pixelmojo — 6 production patterns](https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns) — seuil 500 ms, lourd sur Stop only
- Application : neoteem-back-ts d3b4e20 (typecheck → Stop), neo_ia 17fa987 (python direct + timeouts)