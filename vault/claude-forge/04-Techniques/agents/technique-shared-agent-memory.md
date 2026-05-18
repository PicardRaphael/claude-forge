---
titre: "Memoire partagee agents — memory: project via git"
resume: "Pattern pour partager les apprentissages agents entre devs : memory: project stocke dans .claude/agent-memory/, commite, 200L injectees au demarrage"
aliases:
  - shared agent memory
  - memoire partagee agents
  - agent-memory git
  - memory project scope
  - memoire equipe claude code
  - apprentissage partage agents
type: knowledge
derniere-maj: 2026-05-13
auteur: claude
sources:
  - "https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-agent-memory.md"
  - "https://code.claude.com/docs/en/best-practices"
tags:
  - "#type/knowledge"
  - "#domaine/tech"
  - "#technique/agents"
  - "#outil/claude-code"
---

## 3 scopes de memoire agent

| Scope | Emplacement | Git | Partage | Usage |
|-------|------------|-----|---------|-------|
| `user` | `~/.claude/agent-memory/<name>/` | Non | Non | Connaissances cross-projet, perso |
| `project` | `.claude/agent-memory/<name>/` | **Oui** | **Oui** | Connaissances projet, equipe |
| `local` | `.claude/agent-memory-local/<name>/` | Non | Non | Overrides perso projet |

## Comment ca marche

1. Agent declare `memory: project` dans son frontmatter YAML
2. Au demarrage, les **200 premieres lignes** de `MEMORY.md` sont injectees dans le system prompt
3. L'agent peut lire/ecrire dans son dossier memoire (Read, Write, Edit auto-enabled)
4. Si MEMORY.md depasse 200L, deplacer le detail dans des fichiers thematiques (ex: `migration-gotchas.md`)
5. `git commit` les changements memoire → tous les devs en beneficient

## Structure recommandee

```
.claude/
├── agent-memory/
│   ├── architect/
│   │   ├── MEMORY.md          ← index (< 200L)
│   │   └── planning-patterns.md
│   ├── vue-dev/
│   │   ├── MEMORY.md
│   │   └── migration-gotchas.md
│   ├── code-reviewer/
│   │   └── MEMORY.md
│   └── test-writer/
│       └── MEMORY.md
├── memory/
│   └── MEMORY.md              ← memoire projet globale (pas agent-specific)
```

## Best practices

### Combiner static + dynamic
- **Skills** = connaissances statiques (conventions, patterns) → chargees au demarrage
- **Agent-memory** = connaissances dynamiques (gotchas decouverts, corrections) → evoluent
- Les deux se completent : la skill dit "comment faire", la memoire dit "ce qu'on a appris en faisant"

### Instruire l'agent explicitement
Ajouter dans le body de l'agent :
```
Avant de commencer, consulte ta memoire (.claude/agent-memory/<ton-nom>/MEMORY.md).
Apres avoir termine, mets a jour ta memoire avec ce que tu as appris.
```

### Regle des 200 lignes
- MEMORY.md = index compact (< 200L)
- Detail dans des fichiers thematiques
- Sinon les lignes apres 200 ne sont pas injectees au demarrage

### Git workflow
1. Agent ecrit dans sa memoire
2. Dev review le diff (`.claude/agent-memory/`)
3. Commit avec le reste du travail
4. Prochain dev → git pull → memoire a jour

## Lien avec learn-from-mistakes

La rule `learn-from-mistakes` doit instruire les agents d'ecrire dans 3 endroits :
1. **Agent-memory** (`.claude/agent-memory/<agent>/`) — gotchas specifiques a l'agent
2. **Skills sections Apprentissage** — patterns reutilisables par tous les agents
3. **CLAUDE.md gotchas** — erreurs de workflow critiques

Les 3 sont commites → partage equipe.

## Liens

- [[technique-dreaming-cross-session]] — review automatique cross-session (Managed Agents)
- [[lojii]] — premier projet avec cette architecture
- [[pattern-figma-mcp-claude-code]] — autre pattern deploye sur lojii
