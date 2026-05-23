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
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://code.claude.com/docs/en/memory"
  - "https://code.claude.com/docs/en/best-practices"
  - "https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-agent-memory.md"
tags:
  - "#type/knowledge"
  - "#domaine/tech"
  - "#technique/agents"
  - "#outil/claude-code"
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
