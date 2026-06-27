# Baseline Rules — config-guardian

Référence détaillée des 5 checks pour chaque repo Neoteem.

## Check 1 — Permissions git

### Règle
`Bash(git commit *)` et `Bash(git push *)` doivent être dans `allow` (directement ou via `Bash(git *)`).

### Par repo
Identique pour les 3 repos : ia_back, neo_ia, neoteem-brain.

### Algorithme de vérification

```
1. Lire settings.json (projet) → extraire permissions.allow[]
2. Lire settings.local.json (projet) → merger allow[]
3. Lire ~/.claude/settings.json (global) → extraire permissions.deny[]
4. git_allowed = any(p matches "Bash(git *)" or "Bash(git commit *)" for p in allow)
5. git_denied = any(p matches "Bash(git *)" or "Bash(git commit *)" for p in global_deny)
6. Si git_denied → CRITIQUE (deny global écrase tout)
7. Si git_allowed → OK
8. Sinon → CRITIQUE
```

### Formats acceptés comme "allow"
- `Bash(git *)` — wildcard complet ✓
- `Bash(git commit *)` + `Bash(git push *)` — explicite ✓
- `Bash(git commit*)` sans espace — WARN (format non standard)
- `Bash(git:*)` — WARN (deux-points = format incorrect)

---

## Check 2 — Hooks cohérence stack

### Stacks attendues

| Repo | Stack | Interpréteur attendu |
|------|-------|---------------------|
| ia_back | TypeScript/Bun | `bun` |
| neo_ia | Python/uv | `python` ou `uv run` |
| neoteem-brain | Python | `python3` |

### Hooks orphelins
Fichier dans `<repo>/.claude/hooks/` mais absent de `settings.json` → **CRITIQUE**

### Hooks fantômes
Référencé dans `settings.json` mais fichier absent sur disque → **CRITIQUE**

### Stack mismatch
Hook wired qui utilise le mauvais interpréteur → **WARN**

Exemple : un hook `validate.py` dans ia_back wired avec `python3` au lieu de `bun` → WARN.

### Comment vérifier
1. `Glob("<repo>/.claude/hooks/*")` → liste des fichiers hooks
2. `Read("<repo>/.claude/settings.json")` → extraire les `command:` dans hooks
3. Croiser : fichiers ∩ wired = OK, fichiers \ wired = orphelin, wired \ fichiers = fantôme
4. Pour chaque hook wired : vérifier que `command:` commence par l'interpréteur attendu

---

## Check 3 — Rules obligatoires

### Rules requises dans `<repo>/.claude/rules/`

| Fichier | Description |
|---------|-------------|
| `check-before-create.md` | Checklist avant création composant |
| `learn-from-mistakes.md` | Rule apprentissage erreurs |
| `quality-gates.md` | Gates qualité pipeline |

### Statuts
- 3/3 présentes → **OK**
- 2/3 présentes → **WARN**
- 1/3 ou 0/3 présentes → **CRITIQUE**

---

## Check 4 — MCP tools dans les agents

### Règle générale
Tout agent doit avoir une clé `tools:` dans son frontmatter YAML.
Absence de `tools:` → **CRITIQUE** (MCP non injecté).

### Baseline par repo

#### ia_back
Tous les agents → doivent avoir au moins un tool dont le nom commence par `mcp__context7__` dans `tools:`

Agents DB (détecter par nom : `db-inspector`, `schema-mapper`, `validator`, ou contenu de la description) → doivent aussi avoir `mcp__postgres__query`

#### neo_ia
Tous les agents → doivent avoir au moins un tool dont le nom commence par `mcp__context7__` dans `tools:`

#### neoteem-brain
`vault-enricher` → doit avoir au moins un tool dont le nom commence par `mcp__claude_ai_Atlassian__` dans `tools:`

### Comment détecter les agents DB (ia_back)
Pattern de nommage : agent dont le nom ou la description contient `db`, `database`, `postgres`, `schema`, `inspect`, `validate`.

### Statuts par agent
- Tous les MCP attendus présents → **OK**
- Un MCP manquant → **CRITIQUE** (l'agent ne pourra pas utiliser le service)

---

## Check 5 — Mémoire compounding (pattern Boris)

### 5a — memory: project dans les agents
Chaque agent `.claude/agents/*.md` doit avoir `memory: project` dans son frontmatter.
- Absent → **CRITIQUE**

### 5b — Section Gotchas dans CLAUDE.md
`Read("<repo>/CLAUDE.md")` → chercher un titre `## Gotchas` ou `### Gotchas` (insensible à la casse).
- Absent → **WARN**

### 5c — Mention mémoire/apprentissage dans CLAUDE.md
CLAUDE.md doit mentionner la mémoire ou l'apprentissage :
Chercher les mots-clés : `memory`, `mémoire`, `apprentissage`, `learn`, `MEMORY.md`, `update CLAUDE.md`.
- Absent → **WARN**

### 5d — Feedback rules présentes
Compter les fichiers dans `.claude/agent-memory/` (tous sous-dossiers inclus).
- 0 fichiers → **WARN** (pattern Boris non initié)
- >= 1 fichier → **OK**

### Résumé check 5
4 sous-checks → afficher chacun séparément dans le tableau (5a, 5b, 5c, 5d).
