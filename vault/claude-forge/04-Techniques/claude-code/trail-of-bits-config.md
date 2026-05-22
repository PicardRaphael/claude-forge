---
titre: "Trail of Bits — Configuration Claude Code entreprise sécurité publique"
resume: "github.com/trailofbits/claude-code-config : config CC entreprise sécu publique. Anti-rationalization Stop hook (pattern inédit, Haiku check cop-outs) + sandbox 3-tier (/sandbox builtin + devcontainer + dropkit DO droplets). Référence canonique pour repos sensibles"
aliases:
  - "Trail of Bits"
  - "trailofbits"
  - "Trail of Bits config"
  - "anti-rationalization Stop hook"
  - "claude-code-config"
  - "ToB config CC"
  - "sandbox 3-tier Claude Code"
derniere-maj: 2026-05-22
auteur: claude
type: setup-public
sources:
  - "https://github.com/trailofbits/claude-code-config"
tags:
  - "#type/setup-public"
  - "#domaine/claude-code"
  - "#domaine/securite"
  - "#projet/forge"
---

# Trail of Bits — Configuration Claude Code entreprise sécurité publique

## QUI / QUOI

**Trail of Bits** — Société de cybersécurité (NYC, ~150 personnes), spécialisée audit de sécurité, blockchain, cryptographie appliquée. Reconnue pour son rigueur technique et ses publications de recherche.

**Le repo** : https://github.com/trailofbits/claude-code-config

C'est l'une des **rares configurations Claude Code d'entreprise publiques complètes**. Cible : repos sensibles (sécu, crypto, audits). Standard très haut. Référence canonique pour quiconque doit configurer Claude Code dans un environnement où une erreur coûte cher.

Source **secondaire** (couche 3 — pas Anthropic, pas Karpathy). Mais référence empirique de **production** sécu, donc poids fort sur les questions de sandbox et d'enforcement.

## POURQUOI EST PERTINENT

Trail of Bits a publié **deux patterns inédits** que personne d'autre n'avait formalisé publiquement :

1. **Anti-rationalization Stop hook** — un hook qui détecte quand Claude rationalise du travail incomplet ("issues pre-existing", "out of scope", "too many to fix") et force la continuation
2. **Sandbox 3-tier** — `/sandbox` builtin + devcontainer + dropkit DO droplets, avec règles de routing claires

Ces deux patterns sont **directement réutilisables** pour tout repo sensible.

Trail of Bits a aussi pris position publiquement sur **MCP vs Skills** :
> Sécurité-sensitive → **skills par défaut** (in-repo, code-reviewable), **MCP désactivé** en projet par défaut
> Cross-ecosystem (clients externes) → MCP OK

C'est la doctrine la plus prudente sur MCP en environnement sensible.

## ARCHITECTURE

### Structure du repo (observée)

```
trailofbits/claude-code-config/
├── README.md                # Stop hook inline + doctrine
├── .claude/
│   ├── settings.json        # config canonique
│   ├── hooks/               # incl. anti-rationalization
│   ├── skills/              # in-repo, code-reviewable
│   └── commands/
└── (pas de MCP servers actifs par défaut)
```

### Choix doctrine clés

| Dimension | Trail of Bits |
|-----------|--------------|
| Skills vs MCP | **Skills par défaut**, MCP off par défaut |
| Sandbox | **3 niveaux** explicites par criticité |
| Stop hook | Anti-rationalization Haiku |
| Permissions | Restrictives, allow-list explicite |
| Hooks | Computational sensors (cf [[martin-fowler]]) prioritaires |

## COMPOSANTS NOTABLES

### 1. Anti-rationalization Stop hook (pattern inédit)

**Type** : `Stop` hook avec `"type": "prompt"`, modèle **Haiku** (fast model).

**Mécanique** : évaluateur LLM intercepte la réponse finale de Claude avant validation. Le hook envoie le contenu à Haiku avec un prompt qui détecte les cop-outs.

**Patterns bloqués** (verbatim cité par README) :
> "claiming issues are 'pre-existing' or 'out of scope', saying 'too many issues' to fix, deferring to unrequested 'follow-ups'"

**Réponse de rejet** :
```json
{"ok": false, "reason": "You are rationalizing incomplete work. [specific issue]. Go back and finish."}
```

Le `reason` est injecté **comme prochaine instruction** → force la continuation. Pas un blocage stérile, une redirection ciblée.

**Réponse d'approbation** :
```json
{"ok": true}
```

**Gotcha critique** (verbatim) :
> "The prompt must demand 'raw JSON only' — without that instruction, Haiku wraps results in markdown fences, silently breaking the hook's JSON parsing."

→ Sans `"raw JSON only"` dans le prompt Haiku, le hook échoue **silencieusement** (markdown fences invalident le parse JSON).

**Timeout défaut** : 30s.

**Convergence forge** : doctrine **"hooks > rules"** ([[comment-creer-hook]]). Le anti-rationalization hook = sensor inferential (cf [[martin-fowler]] taxonomy) qui complète les hooks computationnels.

### 2. Sandbox 3-tier (par niveau de risque)

| Tier | Mécanique | Quand utiliser |
|------|-----------|----------------|
| **Tier 1** | `/sandbox` builtin Claude Code | Tâches standard, dev iteration rapide |
| **Tier 2** | **Devcontainer** (.devcontainer/) | Tâches qui touchent dépendances, build, FS local |
| **Tier 3** | **Dropkit DO droplets** (DigitalOcean ephemeral) | Tâches sensibles, exécution non-fiable, exposition réseau |

Le pattern : **escalader le sandbox selon le risque**, ne pas tout faire au tier max (coûts), ne pas tout faire au tier min (sécurité).

Convergence avec Thariq Shihipar (Anthropic) "Designing multi-agent systems: when to split, **when to sandbox**, what to ship" : la décision de sandbox = décision architecturale, pas réflexe.

### 3. Position MCP / Skills

Doctrine ToB (verbatim ou paraphrase fidèle du README) :
- **Skills par défaut** — code dans le repo, reviewable, versionnable, pas de surface d'attaque externe
- **MCP désactivé** par défaut sur projet — chaque MCP server = ~5-8k tokens + surface réseau + dépendance externe
- **MCP autorisé** uniquement cross-ecosystem (clients externes Trail of Bits qui doivent intégrer outils tiers)

C'est la position **la plus prudente publique** sur MCP. Convergente avec Ronacher (cf `recherche-mcp-vs-skills-cli.md`, "Sentry MCP ~8k tokens upfront").

### 4. Hooks computational prioritaires

Trail of Bits implémente la recommandation #3 de Böckeler/Fowler (cf [[martin-fowler]]) : prioriser **computational sensors d'abord** (linters, validators, deterministes), puis **inferential** (anti-rationalization Haiku) en couche supplémentaire.

## VERBATIM NOTABLES

> "claiming issues are 'pre-existing' or 'out of scope', saying 'too many issues' to fix, deferring to unrequested 'follow-ups'"
> *(Patterns bloqués par l'anti-rationalization hook)*

> "The prompt must demand 'raw JSON only' — without that instruction, Haiku wraps results in markdown fences, silently breaking the hook's JSON parsing."
> *(Gotcha critique du hook)*

## ALIGNEMENT FORGE

Trail of Bits = **modèle pour forge** sur tout ce qui touche sécurité et enforcement déterministe :

| Forge | Trail of Bits |
|-------|--------------|
| Hooks delegate-guard / vault-query-guard | Anti-rationalization hook |
| MCP forge-brain (1 seul, local-first) | Skills par défaut, MCP minimal |
| Pas de sandbox tiered | À copier : `/sandbox` + devcontainer en option |
| Permissions allow-list | Aligné |

**Action à envisager pour forge** : implémenter un anti-rationalization Stop hook pour la session principale, surtout sur les chantiers longs où la fatigue de session pousse à abandonner ("trop d'erreurs", "out of scope", "follow-up plus tard"). Note : convergent avec memory `feedback_recurring_meta_anti_pattern` (Jarvis franchise) et `feedback_stop_over_verifying`.

## WIKILINKS

- [[comment-creer-hook]] — Stop hooks officiels, exit codes, pattern Trail of Bits
- [[martin-fowler]] — sensor inferential = anti-rationalization
- [[mcp-vs-skills-doctrine]] — position ToB sur MCP / Skills
- [[methode-analyser-repo]] — Trail of Bits comme référence pour repos sensibles
- [[workflow-claude-code-optimal]] — intégration tiered sandbox dans le pipeline
- [[comment-creer-skill]] — skills par défaut = doctrine ToB

## SOURCES

- **Repo officiel** : https://github.com/trailofbits/claude-code-config
- **README** (avec hook inline) : https://github.com/trailofbits/claude-code-config/blob/main/README.md
- **Trail of Bits blog** : https://blog.trailofbits.com/ (chercher tag claude-code / agents)

---

## NOTE D'HIÉRARCHIE DES SOURCES

Source **secondaire** (couche 3). Pour les décisions de doctrine Claude Code (Skills officielle, hooks officiels), suivre Anthropic. Pour les **patterns d'enforcement sécurité concrets**, Trail of Bits est la référence empirique la plus solide publique en mai 2026.

Limites :
- Pas d'audit indépendant du repo (Trail of Bits est lui-même l'audit)
- Patterns testés en interne ToB, pas benchmarkés cross-org
- Sandbox 3-tier suppose stack DigitalOcean / devcontainer — adapter selon stack cible
