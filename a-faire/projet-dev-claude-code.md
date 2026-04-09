# Projet : Dev Tools Neoteem — Claude Code

**Public :** Equipe developpement (technique)
**Outil :** Claude Code (CLI terminal)
**Statut :** Partiellement en place (ia_back, neoteem-brain)

---

## Objectif

Les developpeurs ont un kit Claude Code partage avec :
1. **Agents specialises** (architect, dev, test-writer, code-reviewer, etc.)
2. **Skills de reference** (conventions API, SQL, architecture hexagonale)
3. **Connexion au vault** (neoteem-brain = contexte metier)
4. **Mise a jour automatique** des outils quand on les ameliore

---

## Architecture

```
Bitbucket (repos de code)              GitHub (plugin dev tools)
  neot-v2/ia_back/                       neoteem/claude-dev-tools/
    ├── .claude/                           ├── agents/
    │   ├── settings.json ──────────────→    │   ├── architect.md
    │   │   enabledPlugins:                  │   ├── code-reviewer.md
    │   │   "dev-tools@neoteem-tools"        │   ├── test-writer.md
    │   ├── rules/                           │   └── ...
    │   └── skills/neo-brain/              ├── skills/
    └── src/                                 │   ├── sql-best-practices/
                                             │   ├── architecture-rules/
                                             │   └── ...
                                           └── plugin.json
```

---

## Ce qui existe deja

| Repo | Agents | Skills | Rules | Hooks | Statut |
|------|--------|--------|-------|-------|--------|
| ia_back | 11 | 16+ | 4 (knowledge-first) | 4 + git pre-push | Complet |
| neoteem-brain | 4 (Agent Teams) | 7 + ticket-analyzer | 10 | 3 + git pre-push | Complet |
| neo_ia | - | - | - | push notify | Basique |
| bdd | - | - | - | - | Pas configure |

---

## Ce qu'apporte le plugin partage

### Aujourd'hui (sans plugin)

Chaque repo a sa propre copie des agents/skills dans `.claude/`. Quand on corrige un agent :
1. Corriger dans ia_back
2. Copier dans neoteem-brain
3. Copier dans neo_ia
4. Copier dans bdd
5. ... x128 repos

### Demain (avec plugin GitHub)

Un seul endroit (GitHub). Tous les repos referencent le meme plugin :
```json
// settings.json de chaque repo Bitbucket
{
  "enabledPlugins": { "dev-tools@neoteem-tools": true }
}
```

Quand on corrige un agent → push GitHub → tous les repos ont la MAJ.

---

## Contenu du plugin "Dev Tools Neoteem"

### Agents partages

| Agent | Model | Role |
|-------|-------|------|
| architect | opus | Design et review architecture |
| dev | sonnet | Implementation feature |
| test-writer | sonnet | Tests unitaires et integration |
| code-reviewer | sonnet | Review code qualite |
| debugger | opus | Diagnostic et fix bugs |
| performance-engineer | sonnet | Optimisation SQL/API |
| security-auditor | sonnet | Audit securite endpoints |

### Skills partagees

| Skill | Role |
|-------|------|
| architecture-rules | Conventions hexagonale Neoteem |
| sql-best-practices | Regles SQL PostgreSQL |
| api-conventions | Conventions REST API |
| neo-brain | Connexion vault Obsidian (wrapper CLI inclus) |
| add-endpoint | Guide creation endpoint |
| connect-table | Guide connexion table Drizzle |

### Rules partagees

| Rule | Role |
|------|------|
| cto-mindset | Orchestration, esprit critique |
| agent-delegation | Routing : qui appeler quand |
| database-rules | BDD immutable, MCP read-only |
| skill-navigator | Knowledge-first, choix des skills |

---

## Distribution aux devs

### Methode 1 — settings.json + Bitbucket (recommandee, zero GitHub)

```json
{
  "extraKnownMarketplaces": {
    "neoteem-tools": {
      "source": { "source": "git-url", "url": "https://bitbucket.org/neot-v2/claude-dev-tools.git" }
    }
  },
  "enabledPlugins": { "dev-tools@neoteem-tools": true }
}
```

Claude Code poll le repo au demarrage + toutes les heures. Push sur Bitbucket → les devs recoivent la MAJ automatiquement. **Pas besoin de GitHub pour les devs.**

### Methode 2 — Managed settings (admin orga, force totale)

L'admin pousse le plugin via les managed settings → tous les devs le recoivent automatiquement, meme sur les repos qui n'ont pas de settings.json.

---

## Mise a jour automatique

```
Dev ameliore un agent
  → Push sur GitHub neoteem/claude-dev-tools
  → Claude Code detecte le changement au prochain demarrage (ou poll 1h)
  → Tous les devs ont la nouvelle version
```

**Pas besoin de copier dans 128 repos.** Un seul push.

---

## Prerequis

| Prerequis | Qui | Quand |
|-----------|-----|-------|
| Repo Bitbucket `neot-v2/claude-dev-tools` cree | DevOps | Semaine 1 |
| Extraire agents/skills de ia_back vers le plugin | Raphael | Semaine 1 |
| Ajouter `enabledPlugins` dans les repos Bitbucket | DevOps | Semaine 2 |
| Former les devs (30 min) | Raphael | Semaine 3 |

---

## KPIs attendus

| Metrique | Avant | Apres (estime) |
|----------|-------|----------------|
| Temps setup Claude Code nouveau repo | 1h+ (copier .claude/) | 0 (plugin auto) |
| Coherence agents entre repos | Variable | 100% identique |
| Temps deploiement correction agent | 30 min x N repos | 1 push (5 min) |
| Devs avec contexte metier (neo-brain) | 2 | Tous |
