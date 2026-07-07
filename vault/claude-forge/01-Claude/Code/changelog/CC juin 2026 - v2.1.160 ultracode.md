---
titre: "CC juin 2026 — v2.1.155→2.1.160 (workflow→ultracode)"
resume: "Drop CC post-Opus 4.8 : le mot-déclencheur des Dynamic Workflows passe de 'workflow' à 'ultracode' (2.1.160), Claude in Chrome via /chrome (2.1.157), Auto Mode Bedrock/Vertex/Foundry (2.1.158), durcissements sécu écriture fichiers shell/git config"
aliases:
  - "CC v2.1.160"
  - "ultracode workflow keyword"
  - "Claude in Chrome /chrome"
  - "CC changelog juin 2026"
  - "workflow trigger renamed ultracode"
type: changelog
domaine: claude-code
derniere-maj: 2026-06-24
auteur: claude
sources:
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
  - "https://www.anthropic.com/news"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
  - "#domaine/anthropic"
---

## Contexte

Drop CC postérieur au changelog vault du 28 mai (v2.1.154 Opus 4.8 + Dynamic Workflows). Versions 2.1.155 → 2.1.160. **Source primaire vérifiée** (raw GitHub CHANGELOG + anthropic.com/news) — les claims d'aggregateurs non confirmés (crédits programmatiques 15 juin, /powerup, PermissionDenied hook) sont écartés (cf [[erreur-4-fabrications-vault-prompt-engineering-2026-05-23]] pattern hallucination chiffrée aggregateurs).

## v2.1.160 — le changement qui impacte forge

### Conséquence : skill `deep-research` — opt-in strict requis

La skill `deep-research` est un **harness Workflow** (fan-out multi-agents). L'invoquer via le Skill tool retourne `Workflow({ name: "deep-research", args: ... })` — et le tool Workflow n'est déclenché qu'avec opt-in explicite (`ultracode`, demande directe « use a workflow », ou session ultracode-on).

- « Recherches ultra poussées / prends ton temps » ≠ opt-in (règle stricte).
- Sans opt-in explicite → faire les WebSearch/WebFetch en parallèle soi-même (sources primaires d'abord, vérifier les claims actionnables).
- Raison : un Workflow peut spawner des dizaines d'agents et brûler beaucoup de tokens — l'utilisateur doit l'avoir demandé explicitement, pas inféré.

Cf [[llm-deep-research-version-numbers-hallucinated]] pour la qualité du contenu produit par deep-research.

- **`workflow` → `ultracode`** : le mot-déclencheur des Dynamic Workflows est renommé. Dire « workflow » dans un prompt ne déclenche plus un dynamic workflow ; c'est désormais `ultracode`. ⚠️ Impacte tout setup forge qui s'appuyait sur le mot « workflow » comme déclencheur.
- Prompt de confirmation **avant écriture** dans les fichiers de démarrage shell et `~/.config/git/` (durcissement sécu).
- Mode `acceptEdits` demande confirmation avant d'écrire un fichier de config de build exécutable.
- Fix copier-sélection sur **WSL/Windows** (PowerShell interop au lieu d'OSC 52) — pertinent machine forge.
- Corrections : sessions background, `agents list`, Windows, IME, voice mode.

## v2.1.158 — Auto Mode cloud providers

- **Auto Mode sur Bedrock, Vertex et Foundry** pour Opus 4.7 et 4.8. Opt-in via `CLAUDE_CODE_ENABLE_AUTO_MODE=1`.

## v2.1.157 — Plugins + Chrome

- Plugins dans `.claude/skills` **chargés automatiquement**.
- `claude plugin init <name>` pour scaffolder un plugin.
- **Claude in Chrome** : sélection du navigateur connecté via `/chrome` → « Select browser… ».
- `EnterWorktree` peut basculer entre worktrees en cours de session.

## v2.1.156

- Correction des erreurs API liées aux blocs thinking sur Opus 4.8.

## Confirmé source primaire anthropic.com/news (industrie)

- **1er juin 2026** : Anthropic dépose confidentiellement son S-1 auprès de la SEC (process IPO).
- **28 mai 2026** : Series H 65 Md$ à 965 Md$ post-money (déjà tracé) + Opus 4.8.

## Écarté (non confirmé en source primaire)

- ❌ Système de crédits programmatiques 15 juin (20$/100$/200$ par tier) — absent du changelog ET de anthropic.com/news. Claim aggregateur (blog.mean.ceo, InfoWorld) non vérifiable. À surveiller, pas à capitaliser.
- ❌ `/powerup`, hook `PermissionDenied`, `CLAUDE_CODE_NO_FLICKER` dans cette plage — absents du changelog réel 2.1.154→160.

## Liens

- [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] — drop précédent
- [[Code with Claude 2026]] — keynote, higher order prompts
- [[MOC-Claude-Code]]

---

## AJOUT 16 juin 2026 — v2.1.161 → v2.1.178 (Fable 5, sous-agents imbriqués, permissions param)

> Source primaire vérifiée : [code.claude.com/docs/en/changelog](https://code.claude.com/docs/en/changelog) (fetch 16 juin). Drop postérieur au v2.1.160 ci-dessus.

### Le plus structurant pour forge

- **v2.1.172 (10 juin)** — **Sous-agents imbriqués** : « Sub-agents can now spawn their own sub-agents (up to 5 levels deep) ». Foreground = toute profondeur (auto-limité) ; background plafonné 5. ⚠️ **Invalide la prémisse « pas de nesting »** de [[anti-reentrance-sub-agents-pattern-escalade]] + [[limites-subagents-claude-code]] + [[comment-creer-agent]] (amendées 16 juin). Piège d'audit : un agent qui omet `tools:` hérite `Agent` et nest par défaut.
- **v2.1.178 (15 juin)** — Syntaxe permission **`Tool(param:value)`** (wildcard `*`), ex `Agent(model:opus)` pour bloquer un sous-agent Opus. Auto mode évalue les spawns de sous-agents AVANT lancement. Specs MCP `mcp__*` dans `disallowedTools` de sous-agent ne sont plus silencieusement ignorées.
- **v2.1.169 (8 juin)** — `--safe-mode` (désactive TOUTES les customisations pour troubleshoot), `/cd` (change de cwd sans casser le prompt cache), `disableBundledSkills`, hook `post-session` (self-hosted runners), fenêtre SIGTERM→SIGKILL configurable.
- **v2.1.166 (6 juin)** — `fallbackModel` (jusqu'à 3 replis), glob dans deny-rules tool-name, **`SendMessage` cross-session durci** (messages relayés ne portent plus l'autorité utilisateur).
- **v2.1.163 (4 juin)** — **`Stop`/`SubagentStop` hooks → `hookSpecificOutput.additionalContext`** (feedback sans erreur de hook) ; skills : échappement `\$` pour un `$` littéral devant un chiffre (pertinent gotcha « jamais `$ARGUMENTS` en backticks ») ; `requiredMinimumVersion`/`requiredMaximumVersion` ; `/plugin list`.

### Modèle

- **v2.1.170 (9 juin)** — **Claude Fable 5** : « a Mythos-class model that we've made safe for general use ». 1M contexte par défaut. Cf [[Fable 5]]. Suspendu par directive export-control US le 12 juin.
- v2.1.173/174/176 — fixes Fable 5 (`[1m]` suffix normalisé, banner crédits, fallback auto mode vers meilleur Opus si Opus 4.8 absent).
- **v2.1.175 (12 juin)** — `enforceAvailableModels` (managed) : l'allowlist contraint aussi le modèle Default.

### Autres

- v2.1.161 — parallel tool calls : un Bash échoué n'annule plus les autres du batch. v2.1.162 — Windsurf renommé « Devin Desktop ». v2.1.176 — titres de session dans la langue de conversation (`language`).

`derniere-maj` → 2026-06-16.


---

## AJOUT 24 juin 2026 — v2.1.179 → v2.1.190 (auto mode terraform/git, sandbox credentials, bash auto-respond)

> Source primaire vérifiée : [code.claude.com/docs/en/changelog](https://code.claude.com/docs/en/changelog) (fetch 24 juin). Drop postérieur à l'AJOUT 16 juin (s'arrêtait à v2.1.178).

### Le plus structurant pour forge

- **v2.1.183 (19 juin)** — **Auto mode safety durci** : les commandes git destructives (`git reset --hard`, `git checkout -- .`, `git clean -fd`, `git stash drop`) sont bloquées si tu n'as pas demandé à jeter le travail local ; `git commit --amend` bloqué si le commit n'a pas été fait par l'agent dans la session ; **`terraform destroy` / `pulumi destroy` / `cdk destroy` bloqués** sauf demande explicite sur la stack. ⚠️ Renforce mécaniquement l'interdit forge « rm -rf / force push main sauf demande explicite » côté auto mode. Aussi : `attribution.sessionUrl` pour omettre le lien claude.ai des commits/PR ; warning si modèle déprécié couvre désormais les modèles en frontmatter d'agent.
- **v2.1.181 (17 juin)** — **Foreground subagents plafonnés à 5 niveaux** comme les background (avant : profondeur illimitée). Complète l'amendement v2.1.172 (cf AJOUT 16 juin). `/config key=value` en interactif/`-p`/Remote Control (ex `/config thinking=false`). Bundled Bun → 1.4.
- **v2.1.187 (23 juin)** — **`sandbox.credentials`** : empêche les commandes sandboxées de lire les fichiers de credentials / variables d'env secrètes. Restrictions de modèle org-configurées (model picker, `--model`, `/model`, `ANTHROPIC_MODEL`). Fix des boucles de structured output (`--json-schema` et workflow `agent({schema})`). Fix profondeur sous-agent : un sous-agent resumé restaure sa profondeur de spawn d'origine, un sous-agent forké compte dans le cap.
- **v2.1.186 (22 juin)** — **`!` bash auto-respond** : une commande bash `!` déclenche désormais automatiquement une réponse de Claude à sa sortie (`"respondToBashCommands": false` pour désactiver). `claude mcp login <name>` / `claude mcp logout <name>` (auth MCP en CLI). Filtrage par statut (`f`) dans `/workflows`. **Agent Teams** : fix des deny-rules `Agent(type)` et restrictions `Agent(x,y)` non appliquées aux spawns de sous-agents nommés. `/review <pr>` utilise le même moteur que `/code-review medium`.

### Loops — aucune nouveauté structurante (machinerie stable)

Vérifié source primaire : depuis le 5 juin, **rien de structurant sur `/loop` et `/goal`**, uniquement des fixes — `/goal` evaluator ne tire plus pendant que des shells/sous-agents tournent (2.1.143), Ctrl+C annule un wakeup `/loop` en idle (2.1.145), CC arrête de promouvoir `/loop` en sessions remote où les loops ne gardent pas le conteneur vivant (2.1.162). **Aucune durée d'expiration de `/loop` n'apparaît dans le changelog** — le « 7 jours » d'aggregateurs n'est pas confirmé en source primaire ; la note canonique [[concevoir-loops-travail]] reste à jour (3 types, 4 briques, vérif tip #1, READ/WRITE cross-repo, garde-fous).

### Autres

- v2.1.185 (20 juin) — hint stall « Waiting for API response · will retry in… » (déclenche à 20s au lieu de 10s). v2.1.190 (24 juin) — fixes & fiabilité.

`derniere-maj` → 2026-06-24.