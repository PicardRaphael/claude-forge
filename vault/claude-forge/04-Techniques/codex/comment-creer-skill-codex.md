---
titre: "Skills Codex — divergences vs le standard Agent Skills"
resume: "Note canonique forge — les Skills côté OpenAI Codex : ce qui DIFFÈRE du standard ouvert Agent Skills (déjà documenté ailleurs). Frontmatter name+description only, 4 scopes (.agents/skills), sidecar agents/openai.yaml, cap listing 2%/8000 chars, allow_implicit_invocation. Portabilité byte-identique CC↔Codex NON prouvée. Vérifié doc officielle au 15 juil. 2026."
aliases:
  - "skills codex"
  - "SKILL.md codex"
  - "creer skill codex"
  - "agents/openai.yaml"
  - ".agents/skills"
  - "scopes skills codex"
  - "skill portable claude code codex"
derniere-maj: 2026-07-15
auteur: claude
type: technique
sources:
  - "https://learn.chatgpt.com/docs/build-skills (ex developers.openai.com/codex/skills, redirect 308)"
  - "https://raw.githubusercontent.com/openai/codex/main/codex-rs/skills/src/assets/samples/openai-docs/SKILL.md"
  - "https://agentskills.io/specification"
  - "https://blog.fsck.com/2025/12/19/codex-skills/ (Jesse Vincent, hands-on)"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#domaine/skills"
  - "#doctrine/2026"
---
# Skills Codex — divergences vs le standard Agent Skills

> Note canonique forge — Codex s'appuie sur le **standard ouvert Agent Skills** (créé par Anthropic, publié en open standard le 18 déc. 2025, adopté par ~40 produits). **Le standard lui-même est documenté ailleurs — ne pas le re-décrire ici.** Cette note ne couvre QUE ce qui est **spécifique à Codex**. Vérifié sur `learn.chatgpt.com/docs/build-skills` au **15 juil. 2026**.

> Pré-requis (doctrine commune, à lire d'abord, PAS recopiée ici) : [[comment-creer-skill]] (anatomie SKILL.md, progressive disclosure, description trigger), [[mcp-vs-skills-doctrine]] (skill vs MCP vs bash), [[Agent Skills Spec]] (spec ouverte, agentskills.io adopté par Codex + CC).

---

## CERTAIN — Noyau commun

Codex ET Claude Code s'appuient sur le même standard. `agentskills.io` liste explicitement **CC et Codex** parmi les clients. Structure de dossier identique au standard : `SKILL.md` + `scripts/` + `references/` + `assets/` (chargés à la demande, une profondeur, < 500 lignes de body recommandé). Progressive disclosure : le listing initial charge `name + description + path` ; le body ne se charge qu'à la sélection.

---

## Divergence 1 — Frontmatter : `name` + `description` UNIQUEMENT (CERTAIN)

Codex ne documente QUE deux champs :
```md
---
name: skill-name
description: Explain exactly when this skill should and should not trigger.
---

Skill instructions for Codex to follow.
```
Le standard définit 6 champs (`+ license, compatibility, metadata, allowed-tools` optionnels), mais **Codex ne documente pas les 4 optionnels**. `name` ≤ 64 chars kebab, = nom du dossier parent. `description` ≤ 1024 chars. *À vérifier* : que Codex applique les mêmes contraintes exactes que la spec sur les champs optionnels.

Observation : la skill officielle `openai-docs` a une `description` **très longue** (bien > 250 chars, sous 1024). Codex ne semble pas soumis à la limite pratique ~250 chars de Claude Code (system reminder `/skills`) — son garde-fou est ailleurs (cap listing, cf divergence 4).

---

## Divergence 2 — 4 scopes, chemin `.agents/skills` (CERTAIN)

Codex scanne (du plus local au plus global) :

| Scope | Chemin |
|-------|--------|
| REPO | `$CWD/.agents/skills`, `$CWD/../.agents/skills`, `$REPO_ROOT/.agents/skills` |
| USER | `$HOME/.agents/skills` |
| ADMIN | `/etc/codex/skills` |
| **SYSTEM** | bundlé avec Codex par OpenAI (built-ins) |

- Chemin = **`.agents/skills`** (neutre cross-LLM), PAS `.claude/skills`. Willison notait `~/.codex/skills` en déc. 2025 — la convention a évolué vers `~/.agents/skills`.
- Le 4e scope **SYSTEM** (built-ins OpenAI) n'a pas d'équivalent nommé côté CC.
- **Pas de précédence/override documentée** : collision de nom → Codex ne fusionne pas, **les deux apparaissent dans le sélecteur**. Symlinks de dossiers suivis.

---

## Divergence 3 — Sidecar `agents/openai.yaml` (CERTAIN, hors standard)

Fichier propre à Codex (non lu par CC), pour l'UI et les dépendances :
```
my-skill/
├── SKILL.md
├── scripts/  references/  assets/
└── agents/
    └── openai.yaml
```
```yaml
interface:
  display_name: "Nom user-facing"
  icon_small: "./assets/small-logo.svg"
  brand_color: "#3B82F6"
  default_prompt: "Prompt d'accompagnement"
dependencies:
  tools:
    - type: "mcp"
      value: "openaiDeveloperDocs"
      transport: "streamable_http"
      url: "https://developers.openai.com/mcp"
policy:
  allow_implicit_invocation: false
```
`allow_implicit_invocation: false` désactive le matching implicite par description (l'invocation explicite `$skill` marche toujours).

---

## Divergence 4 — Invocation + cap listing (CERTAIN)

- **Invocation** : explicite (`/skills`, ou `$skill-name` dans le prompt) + implicite (matching par `description`). Front-loader les trigger words. Signal de déclenchement primaire = la `description` YAML.
- **Cap listing Codex** : le listing initial des skills tient dans **au plus 2 % de la fenêtre de contexte, ou 8000 chars si contexte inconnu**. Dégradation : Codex **raccourcit les descriptions d'abord**, puis **omet des skills avec un warning**. C'est un axe DIFFÉRENT des recommandations du standard (< 5000 tokens body / < 500 lignes). Pas de cap par-skill ni de nombre max documenté.
- Création : `$skill-creator`, `$skill-installer` (curated), ou **Record & Replay** (macOS) qui transforme une démo en skill.

---

## Divergence 5 — Portabilité CC ↔ Codex : NON prouvée (À-VÉRIFIER)

**Le noyau standard est partagé (CERTAIN), mais « un SKILL.md tourne à l'identique dans CC et Codex sans modif » n'est confirmé par AUCUNE source primaire.** Divergences concrètes : répertoires différents (`.agents/skills` vs `.claude/skills` + plugins), champs documentés différents, sidecar `openai.yaml` propre à Codex. Le seul test hands-on (Jesse Vincent, fsck.com 19/12/2025) ne confirme PAS l'interop et souligne des approches différentes.

> **Capitaliser comme « noyau standard partagé + divergences tool-specific », JAMAIS comme « SKILL.md portable byte-identique ».** Le champ `compatibility` du standard existe précisément pour signaler le produit visé — preuve que le standard anticipe des divergences.

---

## Principes de design (guidance OpenAI)

- « Keep each skill focused on one job. »
- « Prefer instructions over scripts unless you need deterministic behavior or external tooling. »
- Distribution : `$skill-installer` pour le local ; **plugins** pour la réutilisation partagée.
- Position Surface Map : `... → skills → plugins → MCP → ...` (cf [[workflow-codex-optimal]]).

---

## ANTI-PATTERNS

- ❌ **Croire une skill CC portable telle quelle dans Codex** — noyau commun oui, byte-identique non prouvé.
- ❌ **Ranger les skills dans `.claude/skills` côté Codex** — c'est `.agents/skills`.
- ❌ **Compter sur une précédence entre scopes** — non documentée ; collision = doublon visible.
- ❌ **Ignorer le cap listing 2%/8000** — trop de skills → certaines omises silencieusement (warning).
- ❌ **Recopier la spec Agent Skills dans cette note** — elle vit dans [[comment-creer-skill]] / [[Agent Skills Spec]] (single-source).

---

## SOURCES

- `learn.chatgpt.com/docs/build-skills[.md]` (doc Codex, 15/07/2026).
- `raw.githubusercontent.com/openai/codex/main/codex-rs/skills/src/assets/samples/openai-docs/SKILL.md` (skill échantillon réelle).
- `agentskills.io/specification` (standard).
- `blog.fsck.com/2025/12/19/codex-skills/` (Jesse Vincent, hands-on — *secondaire*).
- Contexte SkillsBench (Codex+GPT-5.2 régresse −5,6 pp sur skills auto-générées) : voir [[comment-creer-skill]] AJOUT 7 juin.

---

## WIKILINKS

- [[workflow-codex-optimal]] — note maître
- [[comment-creer-skill]] — le standard + anatomie (doctrine commune, PAS recopiée ici)
- [[Agent Skills Spec]] — spec ouverte cross-LLM
- [[mcp-vs-skills-doctrine]] — skill vs MCP vs bash
- [[subagents-cloud-codex]] — skills liées à un subagent (champ skills.config)
- [[Simon Willison]] — reverse-eng, skills cross-LLM
