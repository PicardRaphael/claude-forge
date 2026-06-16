---
titre: "Memoire partagee agents — CLAUDE.md + auto memory"
resume: "4 scopes CLAUDE.md canoniques Anthropic (managed/user/project/local) + auto memory dans ~/.claude/projects/<project>/memory/ (machine-local, premieres 200L ou 25KB chargees en user message apres system prompt)"
aliases:
  - shared agent memory
  - memoire partagee agents
  - claude.md scopes
  - 4 scopes claude code
  - auto memory anthropic
  - memoire equipe claude code
  - apprentissage partage agents
type: knowledge
derniere-maj: 2026-06-16
auteur: claude
sources:
  - "https://code.claude.com/docs/en/memory"
  - "https://code.claude.com/docs/en/best-practices"
  - "https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-agent-memory.md"
tags:
  - "#type/knowledge"
  - "#domaine/tech"
  - "#domaine/agents"
  - "#domaine/claude-code"
---

## 4 scopes CLAUDE.md (canonique Anthropic)

Verbatim docs : "CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself."

| Scope | Emplacement | Git | Partage | Usage |
|-------|-------------|-----|---------|-------|
| **Managed policy** | macOS `/Library/Application Support/ClaudeCode/CLAUDE.md` ; Linux/WSL `/etc/claude-code/CLAUDE.md` ; Windows `C:\Program Files\ClaudeCode\CLAUDE.md` | Deploye via MDM/Group Policy | Org entier | Standards entreprise, compliance |
| **User** | `~/.claude/CLAUDE.md` | Non | Non | Preferences perso cross-projets |
| **Project** | `./CLAUDE.md` ou `./.claude/CLAUDE.md` | **Oui** | **Oui** | Standards equipe, architecture, conventions |
| **Local** | `./CLAUDE.local.md` | Non (.gitignore) | Non | Sandbox URLs, preferences perso projet |

Les fichiers sont charges **en entier** (pas tronques) et concatenes du root vers le working directory. `CLAUDE.local.md` est appendu apres `CLAUDE.md` dans chaque dossier.

Imports `@path/to/file` permettent de modulariser (max 5 hops recursifs).

> [!note] Audit 23 mai 2026
> La version anterieure de cette note citait "3 scopes : user / project / local" avec un chemin `.claude/agent-memory-local/` qui **n'existe pas** dans la doc Anthropic. La vraie hierarchie est 4 scopes CLAUDE.md (managed/user/project/local). Voir [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]].

## Auto memory (separe de CLAUDE.md)

Mecanisme distinct : Claude ecrit ses propres notes au fil des sessions.

| Aspect | Detail |
|--------|--------|
| Emplacement | `~/.claude/projects/<project>/memory/` |
| Versionning | Machine-local. PAS partage entre machines ou cloud envs |
| Chargement | Premieres **200 lignes ou 25KB** du `MEMORY.md` (la plus petite limite). Au-dela = pas charge au lancement |
| Format | `MEMORY.md` (index compact) + fichiers topiques charges a la demande |
| Activation | On par defaut. Toggle via `/memory` ou `autoMemoryEnabled` ou `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` |
| Version requise | Claude Code v2.1.59+ |

Le `<project>` path = repo Git. Worktrees + sous-repertoires partagent un seul dossier auto memory.

Sub-agents peuvent maintenir leur propre auto memory ([docs sub-agents](https://code.claude.com/docs/en/sub-agents#enable-persistent-memory)).

## CLAUDE.md vs auto memory

| | CLAUDE.md | Auto memory |
|---|---|---|
| Qui ecrit | Toi | Claude |
| Contenu | Instructions, regles | Apprentissages, patterns |
| Scope | Project / user / org | Per repo, partage entre worktrees |
| Charge dans | Chaque session | Chaque session (200 lignes ou 25KB) |
| Usage | Standards coding, workflows, archi | Build commands, debugging insights, preferences |

Utiliser CLAUDE.md pour guider explicitement, auto memory pour laisser Claude apprendre des corrections.

## `.claude/rules/` (modularite project)

Pour gros projets, decouper en `.claude/rules/<topic>.md`. Path-scoped via frontmatter :

```markdown
---
paths:
  - "src/api/**/*.ts"
---
```

Les rules sans `paths` se chargent en session, comme `.claude/CLAUDE.md`. Les rules avec `paths` chargees quand Claude lit un fichier matching.

## Best practices

### Combiner static + dynamic + skills

- **Skills** (`/skills`) = workflows reutilisables on-demand (charges quand invoque)
- **CLAUDE.md + rules** = standards persistants charges chaque session
- **Auto memory** = apprentissages dynamiques

### Taille CLAUDE.md

Target < 200 lignes. Au-dela, adherence se degrade. Utiliser path-scoped rules pour modulariser.

### Specificite

"Use 2-space indentation" > "Format code properly". "Run `npm test` before committing" > "Test your changes".

### Manage CLAUDE.md a l'echelle

- **Managed policy** : org-wide instructions deployees via `managed-settings.json` `claudeMd` key ou fichier
- **`claudeMdExcludes`** : skip CLAUDE.md des autres equipes dans un monorepo
- **InstructionsLoaded hook** : debug exactement quels fichiers sont charges

## Git workflow (pour project + .claude/rules/)

1. Tu (ou Claude) edites `CLAUDE.md` ou `.claude/rules/X.md`
2. Review du diff
3. Commit
4. Prochain dev → git pull → instructions a jour

L'auto memory ne se commit pas (machine-local).

## Lien avec learn-from-mistakes

La rule `learn-from-mistakes` doit instruire d'ecrire dans :
1. **Auto memory** (`~/.claude/projects/<project>/memory/`) — apprentissages Claude
2. **Skills sections Apprentissage** — patterns reutilisables
3. **CLAUDE.md gotchas** — erreurs critiques team-shared

## Liens

- [[technique-dreaming-cross-session]] — review automatique cross-session (Managed Agents, Research Preview)
- [[lojii]] — projet avec memoire partagee
- [[pattern-figma-mcp-claude-code]] — autre pattern lojii
- [[comment-ecrire-claudemd]] — best practices CLAUDE.md

---

## AJOUT 16 juin 2026 — Agent persistent memory (`memory:` frontmatter) + diagnostic « CC ne retient rien »

> Source primaire vérifiée : [code.claude.com/docs/en/sub-agents § Enable persistent memory](https://code.claude.com/docs/en/sub-agents) + [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory). Déclenché par la plainte récurrente d'équipe « Claude Code ne retient rien d'une session à l'autre ».

### Le diagnostic de la plainte (à donner aux collègues)

CC démarre **toujours** sur un contexte vierge (verbatim : *« Each Claude Code session begins with a fresh context window »*). La frustration « il ne retient rien » vient d'une **confusion entre deux mécanismes** :

- **Auto memory** (`~/.claude/projects/<project>/memory/`) = **machine-locale, NON partagée** (verbatim : *« Auto memory is machine-local. Files are not shared across machines or cloud environments »*). Elle « retient » mais seulement sur **ta** machine — d'où l'impression d'équipe qu'il n'y a pas de mémoire.
- **La vraie mémoire d'équipe = des fichiers COMMITTÉS** : `CLAUDE.md` + `.claude/rules/` (déjà couverts plus haut) **et désormais** l'agent persistent memory en scope `project`.

**Réponse en une phrase** : *commitez `CLAUDE.md` + `.claude/rules/` (mémoire d'équipe de base), et ajoutez `memory: project` sur vos agents pour qu'ils accumulent des apprentissages partagés via git.* L'auto-memory locale reste un bonus par-machine, pas la mémoire d'équipe.

### Agent persistent memory — le `memory:` frontmatter (NET-NEUF vs le reste de cette note)

Champ frontmatter d'un sous-agent → répertoire de mémoire persistant cross-conversations. **3 scopes** :

| Scope | Emplacement | Git / partagé | Quand |
|---|---|---|---|
| `user` | `~/.claude/agent-memory/<name-of-agent>/` | Non | apprentissages cross-projets |
| `project` | `.claude/agent-memory/<name-of-agent>/` | **Oui — committable** | **scope recommandé par défaut** (verbatim : *« makes subagent knowledge shareable via version control »*) |
| `local` | `.claude/agent-memory-local/<name-of-agent>/` | Non (gitignore) | project-specific non committé |

Quand activé : le system prompt de l'agent inclut des instructions read/write + **les 200 premières lignes ou 25KB du `MEMORY.md`** du répertoire (même cap que l'auto-memory) ; Read/Write/Edit auto-activés. Configurable aussi via `/agents` (étape « Configure memory »).

**Limite** : c'est par-AGENT, pas une mémoire de session globale. Il faut le prompter (« consulte ta mémoire avant de commencer », « sauvegarde ce que tu as appris »). Doctrine forge déjà alignée : tous nos agents ont `memory: project` (cf `feedback_memory_mandatory`).

### Frontière critique des deux MEMORY.md (cause du gotcha forge > 38k chars)

Ne pas confondre :
- `~/.claude/projects/.../memory/MEMORY.md` (**auto-memory**, local, **capé 200L/25KB** au chargement) ;
- `memory/MEMORY.md` du repo forge, **committé**, chargé **EN ENTIER** via `@import` dans CLAUDE.md (non capé).

C'est précisément pourquoi le CLAUDE.md forge s'alarme quand `MEMORY.md` dépasse ~38k chars : il est full-loaded à chaque session, pas tronqué. La discipline « MEMORY.md tier-1 + archive tier-2 » répond à ça.

### Mise en place concrète dans nos repos Claude Code (recette collègues)

1. **`CLAUDE.md` à la racine** committé : standards équipe, archi, conventions (< 200 lignes, sinon découper en `.claude/rules/`).
2. **`.claude/rules/*.md`** committés pour la modularité (path-scoped via `paths:` si besoin).
3. **`memory: project`** sur les agents `.claude/agents/*.md` → apprentissages accumulés et partagés via git.
4. **Auto-memory** : laissée ON par machine (bonus perso), ne PAS compter dessus pour l'équipe.
5. **Optionnel — MCP memory server** si on veut une mémoire requêtable (graphe/FTS) plutôt que du markdown chargé : voir section suivante.

### MCP memory servers (alternative requêtable)

- **Officiel `@modelcontextprotocol/server-memory`** (primaire) : knowledge graph local entities/relations/observations, persisté JSONL (`MEMORY_FILE_PATH` à fixer sur un chemin stable). Install : `claude mcp add memory -- npx -y @modelcontextprotocol/server-memory`. Limite : `search_nodes` keyword-only (pas de vector), pas de contrôle d'accès.
- **`basic-memory`** (basicmachines, à confirmer via README) : Markdown + index SQLite local, `claude mcp add basic-memory -- uvx basic-memory mcp`.
- **Notre pattern forge-brain** = vault Obsidian + MCP (co-écrit humain/IA, Markdown structuré, FTS5/BM25, pas de cap 200L car on-demand) — c'est la version aboutie de « MCP memory server » pour un Lead. Pattern Karpathy LLM wiki (gist 4 avr 2026) ; noter que l'association « Obsidian = l'IDE » vient de commentaires secondaires, pas du gist primaire.

### Cowork — la mémoire change de mécanique (à dire aux collègues sur Desktop/Cowork)

Tout ce qui précède (CLAUDE.md, `.claude/rules/`, `memory:` agent, hooks) suppose le **CLI**. En **Cowork** (sandbox Desktop), trois différences cassent les réflexes CLI :

- **`CLAUDE.md` n'est PAS chargé** → la mémoire d'instructions d'équipe passe par les **project / folder Instructions** (l'équivalent Cowork de CLAUDE.md). C'est là qu'on met les standards partagés.
- **Zéro hooks, pas de MCP stdio** → aucun enforcement déterministe natif ; mémoire requêtable d'équipe = **MCP remote HTTPS** (un serveur vault distant, pas un binaire local). Cf [[cowork-skills-reliability]] (matrice CLI/Desktop/Cowork + 4 leviers d'enforcement).
- **Écriture vault impossible en run planifié (headless)** → en tâche Cowork planifiée, on peut LIRE le vault mais pas y ÉCRIRE de façon fiable ; toute mémoire d'apprentissage qui doit persister entre runs va en **fichiers locaux**, jamais en notes vault (sinon casse silencieuse). Cf [[cowork-write-vault-headless-impossible]].

Réponse collègues, version Cowork : *mettez vos standards dans les project Instructions (pas un CLAUDE.md), branchez un MCP remote HTTPS si vous voulez une mémoire d'équipe requêtable, et ne comptez pas sur l'écriture vault en run planifié.*

`derniere-maj` → 2026-06-16.
