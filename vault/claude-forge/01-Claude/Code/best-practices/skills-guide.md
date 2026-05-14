---
titre: "Guide complet des Skills Claude Code"
resume: "Guide de reference pour creer des skills Claude Code — format YAML, 9 categories Thariq, pattern d'activation directive, gotchas et budget /doctor"
aliases:
  - "skills guide"
  - "guide skills CC"
  - "skills claude code"
  - "skills format"
  - "skills best practices"
  - "9 categories skills"
domaine: claude-code
type: technique
derniere-maj: 2026-05-14
auteur: claude
sources:
  - "https://code.claude.com/docs/en/skills"
  - "https://www.linkedin.com/pulse/lessons-from-building-claude-code-how-we-use-skills-thariq-shihipar-iclmc"
  - "https://howborisusesclaudecode.com"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/skills"
---

## Anatomie d'une Skill

Une skill est un **dossier**, pas un fichier. `SKILL.md` est le hub ; le reste (references/, scripts/, examples/) fait le vrai travail.

```
my-skill/
  SKILL.md           # Instructions principales (requis)
  references/        # Documentation lourde, chargee a la demande
  scripts/           # Scripts executables par Claude
  examples/          # Exemples de sortie
```

### Progressive disclosure

Au demarrage, Claude ne voit que ~100 tokens de metadata YAML (nom + description). Le SKILL.md complet ne charge que quand la tache matche. Les fichiers references/ chargent ensuite a la demande.

## Frontmatter YAML

| Champ | Description |
|-------|-------------|
| `name` | Nom d'affichage, defaut = nom du dossier. Lowercase + tirets, max 64 chars |
| `description` | Ce que ca fait et QUAND l'utiliser. **Tronque a 1 536 chars** |
| `when_to_use` | Contexte de declenchement additionnel. Ajoute a description, compte dans les 1 536 |
| `model` | Override modele : `sonnet`, `opus`, `haiku`, `inherit` |
| `effort` | Override effort : `low`, `medium`, `high`, `xhigh` |
| `context` | `fork` = executer dans un subagent forke |
| `paths` | Globs qui limitent quand la skill s'active |
| `hooks` | Hooks scopes au cycle de vie de cette skill |
| `disable-model-invocation` | `true` = seul l'utilisateur peut invoquer |
| `user-invocable` | `false` = cachee du menu `/`, seul Claude peut invoquer |
| `allowed-tools` | Outils sans permission quand la skill est active |
| `shell` | `bash` (defaut) ou `powershell` pour les blocs `!command` |

### Substitutions

`$ARGUMENTS`, `$ARGUMENTS[N]`, `$N`, `$name`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`

## Les 9 categories de skills (Thariq Shihipar)

Apres avoir catalogue des centaines de skills internes chez Anthropic, l'equipe a identifie 9 categories recurrentes.

| # | Categorie | Quand | Exemples |
|---|-----------|-------|----------|
| 1 | **Library & API Reference** | Usage correct de libs, CLIs, SDKs. Gotchas + snippets | `billing-lib`, `frontend-design` |
| 2 | **Product Verification** | Tester/verifier que le code marche. Playwright, tmux | `signup-flow-driver`, `checkout-verifier` |
| 3 | **Data Fetching & Analysis** | Connexion data/monitoring, credentials, workflows | `funnel-query`, `grafana` |
| 4 | **Business Process** | Automatiser workflows repetitifs en une commande | `standup-post`, `weekly-recap` |
| 5 | **Code Scaffolding** | Generer du boilerplate pour le codebase specifique | `new-migration`, `create-app` |
| 6 | **Code Quality & Review** | Enforcer qualite, review avec scripts deterministes | `adversarial-review`, `code-style` |
| 7 | **CI/CD & Deployment** | Fetch, push, deploy. Peut referencer d'autres skills | `babysit-pr`, `deploy-service` |
| 8 | **Runbooks** | Symptomes → investigation structuree | `service-debugging`, `oncall-runner` |
| 9 | **Infrastructure Operations** | Maintenance routine, actions destructives avec garde-fous | `resource-orphans`, `cost-investigation` |

## 9 principes de creation (Thariq)

1. **Don't State the Obvious** — Info qui pousse Claude hors de sa pensee par defaut
2. **Gotchas section** — Le contenu le plus valuable. Construite a partir des echecs reels
3. **File System = Context Engineering** — Utiliser le dossier entier, pas juste SKILL.md
4. **Avoid Railroading** — Objectifs et contraintes, PAS des etapes prescriptives
5. **Think Through Setup** — Config dans `config.json`, `AskUserQuestion` pour prompts structures
6. **Description = Trigger** — Decrire QUAND invoquer, pas resumer la fonctionnalite
7. **Memory & Data** — Logs append-only, JSON, SQLite ; `${CLAUDE_PLUGIN_DATA}` pour persistence
8. **Store Scripts** — Fournir scripts et libs pour que Claude compose au lieu de reconstruire
9. **On Demand Hooks** — Hooks actives seulement quand la skill est appelee

## Activation et fiabilite

### Le probleme d'activation

Audit de 214 skills communautaires : **73% etaient silencieusement cassees** (jamais declenchees). Cause #1 : descriptions vagues sans phrases de declenchement (68%).

### Formule directive (100% activation sans hook)

```
# MAUVAIS (passif, vague)
Helps with Docker configuration and containers.

# BON (directif, specifique)
ALWAYS invoke this skill when reviewing code changes before committing.
Use for pull request reviews, diff reviews, and any time the user says
'check', 'review', or 'audit' code. DO NOT write security feedback
without invoking this skill first.
```

### Budget et /doctor

Les descriptions partagent un budget = **1% du context window** (configurable via `skillListingBudgetFraction`). Quand sature, des skills sont silencieusement droppees.

`/doctor` diagnostique si le budget deborde et quelles skills sont affectees.

### Comportement post-compaction

Apres auto-compaction, CC re-attache jusqu'a 5 000 tokens par skill, max 25 000 combines. Les skills plus anciennes peuvent etre completement droppees.

## Gotchas

- SKILL.md < 500 lignes / ~5 000 tokens — au-dela, l'attention du modele decay
- Description tronquee a 1 536 chars — mettre le cas d'usage cle EN PREMIER
- Ne pas keyword-stuffer la description — utiliser des verbes d'intention semantique
- Context rot commence a ~300-400K tokens sur le modele 1M
- Skills dans `.claude/skills/` = PAS visibles dans Cowork. Utiliser `~/.claude/skills/` ou plugin
- `skillOverrides` dans settings permet de controler la visibilite sans editer SKILL.md

## Liens

- [[hooks-guide]] — Enforcement deterministe pour les skills critiques
- [[claudemd-guide]] — Quand une section CLAUDE.md devient une skill
- [[cowork-skills-reliability]] — Problemes specifiques Cowork
- [[Thariq Shihipar]] — Auteur du framework 9 categories
- [[Boris Cherny]] — Skills = composabilite
- [[harness-engineering]] — Skills dans le paradigme harness
