---
titre: "Comparaison skill officielle Anthropic claude-code-setup vs vault forge"
resume: "Skill officielle Anthropic 'claude-automation-recommender' (plugin claude-code-setup) vs notes canoniques forge. Forge plus profond sur doctrine ; skill officielle utile pour table 'codebase signal → MCP/Skill/Hook/Subagent' et commandes bash détection stack."
aliases:
  - "comparaison skill officielle anthropic"
  - "claude-code-setup vs forge"
  - "automation recommender comparaison"
  - "skill officielle vs vault forge"
derniere-maj: 2026-07-27
auteur: claude
type: comparaison
sources:
  - "Plugin Anthropic claude-code-setup v1.0.0 — claude-automation-recommender skill"
  - "Vault forge — methode-analyser-repo + 7 canoniques claude-code"
tags:
  - "#type/comparaison"
  - "#domaine/claude-code"
  - "#meta"
---
# Comparaison skill officielle Anthropic `claude-code-setup` vs vault forge

> Note méta — pourquoi le vault forge n'absorbe pas la skill officielle, et quels 3 bits valait la peine de reprendre.

## QUOI

Skill officielle Anthropic `claude-automation-recommender` du plugin `claude-code-setup` v1.0.0. Analyse un codebase et recommande des automations Claude Code par catégorie (Hooks / Skills / Subagents / MCP / Plugins).

**Location** : `~/.claude/plugins/cache/claude-plugins-official/claude-code-setup/1.0.0/skills/claude-automation-recommender/`

## CE QUE FAIT LA SKILL OFFICIELLE

1. **Phase 1 — Détection stack** :
   - `ls -la package.json pyproject.toml Cargo.toml go.mod pom.xml`
   - `cat package.json | grep -E '"(react|vue|angular|next|express|fastapi|django|prisma|supabase|stripe)"'`
   - Détection signaux : Language/Framework, Frontend stack, Database, Tests, CI

2. **Phase 2 — Recommandations par catégorie** :
   - **MCP Servers** : table "Codebase Signal → MCP" (Supabase → Supabase MCP, GitHub → GitHub MCP, etc.)
   - **Skills** : table avec skills officielles et plugins
   - **Hooks** : table (Prettier → PostToolUse format, .env → block, etc.)
   - **Subagents** : table (>500 files → code-reviewer, auth/payments → security-reviewer)
   - **Plugins** : recommandations bundle

3. **Phase 3 — Output report** : format markdown structuré avec "Why" justifié par signal détecté

## CE QUE LE VAULT FORGE A EN PLUS

| Domaine | Vault forge | Skill officielle |
|---------|-------------|------------------|
| Pipeline doctrine | architect → dev → reviewer → test (avec critères skip) | Subagents génériques |
| Modèles | Sonnet/Opus/Haiku split avec sources (Cat Wu, Brad Abrams) | "Use Haiku for speed" générique |
| Effort levels | `low/medium/high/xhigh/max` avec doctrine forge (xhigh réservé architect/dev-lead/refactor-pg) | Pas mentionné |
| Harness engineering | Hashimoto (popularise) → LangChain → Böckeler chaîne complète | Pas mentionné |
| 2-agent architecture | Justin Young verbatim (initializer + coding, harness identique, pas de split modèles) | Pas mentionné |
| Advisor Strategy | Brad Abrams verbatim "close to Opus-level intelligence at much lower prices" | Pas mentionné |
| 9 catégories Thariq | Post Anthropic mars 2026 "Lessons from Building Claude Code" | Pas mentionné |
| Hooks events | 30 events officiels avec table bloquant/non-bloquant | Liste partielle |
| Hook timeouts | 600s/30s/60s par type (command/prompt/agent) | Pas mentionné |
| `once: true` règle | Skill frontmatter UNIQUEMENT | Pas mentionné |
| Description SKILL.md | 1024 chars spec MAIS ~250 chars pratique (system reminder tronque) | Pas mentionné |
| Lethal trifecta | Simon Willison juin 2025 verbatim, éléments corrigés | Pas mentionné |
| Doctrine 22 mai | Hooks lint/security/scope only, JAMAIS workflow | Pas mentionné |
| Pattern Karpathy LLM Wiki | 3-layers raw/wiki/schema + Ingest/Query/Lint + 2 fichiers obligatoires | Pas mentionné |
| Méthode A→B→C→D→E | Ordre canonique analyser réel → lire canoniques → croiser | Phase 1 → 2 → 3 simple |
| Trail of Bits patterns | Anti-rationalization Stop hook, 3-tier sandbox | Pas mentionné |
| Erreurs documentées | Knowledge/erreurs/ avec verbatim et corrections | Pas mentionné |

**Conclusion** : le vault forge est 15× plus profond doctrinalement. La skill officielle est utile comme **starter pack** pour quelqu'un qui découvre, pas comme référence pour un expert.

## CE QUE J'AI REPRIS DE LA SKILL OFFICIELLE (intégré dans methode-analyser-repo)

### 1. Commandes bash détection stack — Étape 1 enrichie

Skill officielle propose des commandes bash concrètes très pratiques :
```bash
ls -la package.json pyproject.toml Cargo.toml go.mod pom.xml 2>/dev/null
cat package.json 2>/dev/null | grep -E '"(react|vue|angular|next|express|fastapi|django|prisma|supabase|stripe)"'
ls -la .claude/ CLAUDE.md 2>/dev/null
ls -la src/ app/ lib/ tests/ components/ pages/ api/ 2>/dev/null
```

→ À intégrer dans [[methode-analyser-repo]] Étape 1.

### 2. Table "Codebase Signal → Outil"

Skill officielle a des tables très concrètes signal → outil. Adaptées au vault forge :

**MCP Servers** :
| Signal | MCP |
|--------|-----|
| Lib populaire (React, Express) | context7 (live doc) |
| Frontend UI testing | Playwright |
| Supabase | Supabase MCP |
| PostgreSQL/MySQL | Database MCP |
| GitHub repo | GitHub MCP |
| Linear | Linear MCP |
| Sentry | Sentry MCP |
| Memory cross-session | Memory MCP |

**Hooks** :
| Signal | Hook |
|--------|------|
| Prettier configuré | PostToolUse auto-format |
| ESLint/Ruff | PostToolUse auto-lint |
| TypeScript | PostToolUse type-check |
| Tests dir | PostToolUse run related tests |
| .env files | PreToolUse block .env edits |
| Lock files | PreToolUse block lock files |

**Subagents** :
| Signal | Subagent |
|--------|----------|
| Codebase > 500 files | code-reviewer parallèle |
| Auth/payments | security-reviewer |
| API project | api-documenter (OpenAPI) |
| Perf critique | performance-analyzer |
| Frontend lourd | ui-reviewer (a11y) |
| Manque tests | test-writer |

→ À intégrer dans [[methode-analyser-repo]] Étapes 3-4-5.

### 3. Decision framework "When to recommend X"

Skill officielle clarifie quand recommander quoi. Le vault forge l'a déjà dans [[mcp-vs-skills-doctrine]] (3 questions) + [[comment-creer-hook]] (quand créer / quand pas).

**Ajout utile** :
- MCP → "External service integration needed (databases, APIs)"
- Skill → "Document generation (docx, xlsx, pptx, pdf)" — angle skills officielles document-handling utile
- Plugins → "Need multiple related skills + team-wide standardization"

→ Déjà couvert dans vault forge, pas de nouveau bit à reprendre.

## CE QUE LE VAULT FORGE PEUT IMPORTER SANS RÉÉCRIRE

- **Plugin reference** : `anthropic-agent-skills` (skills bundle), `frontend-design` (Lisa Crofoot), `mcp-builder`, `docx/xlsx/pdf` skills documents
- **MCP officiels listés** : context7, Playwright, Supabase, GitHub, Linear, Sentry, Memory MCP — référence rapide

→ Note dédiée si besoin futur : `04-Techniques/claude-code/mcp-officiels-anthropic.md`.

## DOCTRINE FORGE

**On absorbe pas la skill officielle dans une nouvelle skill forge.** Le vault forge canonique reste la source de vérité. La skill officielle est citée comme :
- Référence externe ([[methode-analyser-repo]] section EXEMPLES)
- Starter pack pour newcomers à comparer avec doctrine forge
- Source des commandes bash et tables signal→outil intégrées chez nous

**Anti-pattern évité** : créer `repo-config-recommender` skill forge qui dupliquerait [[methode-analyser-repo]] = scope creep (`feedback_single_source_truth_vault_canonique`).

## WIKILINKS

- [[methode-analyser-repo]] — où les 3 bits sont intégrés
- [[mcp-vs-skills-doctrine]] — decision framework forge
- [[comment-creer-hook]] — quand créer hook (déjà couvert)
- [[comment-creer-skill]] — quand créer skill (déjà couvert)
- [[comment-creer-agent]] — quand créer agent (déjà couvert)
- [[feedback_single_source_truth_vault_canonique]] — anti-pattern duplication

## SOURCES

- Plugin officiel : `~/.claude/plugins/cache/claude-plugins-official/claude-code-setup/1.0.0/`
- Skill : `claude-automation-recommender/SKILL.md`
- References : `references/mcp-servers.md`, `references/skills-reference.md`, `references/hooks-patterns.md`, `references/subagent-templates.md`, `references/plugins-reference.md`


## Update 26 mai 2026 — veille étendue 11 plugins

Pattern absorption confirmé sur 11 plugins additionnels (cf [[plugins-officiels-veille-2026-05-26]]).

**Pattern doctrine reconduit** : *"On absorbe pas le plugin officiel dans une nouvelle skill forge"* — appliqué aux 11 plugins :
- 6 SKIP (stack non-match ou anti-pattern)
- 3 REFERENCE (notes vault, pas de skill forge)
- 2 ADAPT (enrichissement canonique existant, pas nouvelle skill)
  - skill-creator eval pattern → enrichi [[comment-creer-skill]]
  - code-review confidence scoring → enrichi la skill `da-blocking-arbitrage`

**Aucune nouvelle skill forge créée** — doctrine respectée. Single source of truth = vault canonique.
