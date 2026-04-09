# Guide technique : Setup Claude Code pour les repos dev

**Pour :** DevOps + Raphael
**Temps estime :** 15 min par repo

---

## Principe

Chaque repo a sa propre configuration `.claude/` adaptee a son stack. Le point commun : **tous se connectent au vault neoteem-brain** via le kit `neo-brain`.

Pas besoin de GitHub. Tout fonctionne avec Bitbucket.

---

## Connecter un repo au vault

### 1. Copier le kit neo-brain

Le kit est a la racine du vault : `neoteem-brain/neo-brain/`

```bash
cd mon-repo
mkdir -p .claude/skills
cp -r /chemin/vers/neoteem-brain/neo-brain .claude/skills/neo-brain
```

### 2. Verifier

```bash
cd mon-repo
bash .claude/skills/neo-brain/scripts/obsidian-cli.sh vault="neoteem-brain" search query="test" limit=3
```

Si ca retourne des resultats → c'est connecte.

### 3. Documentation complete

Voir `neoteem-brain/neo-brain/README.md` pour :
- Configuration des agents (ajouter `neo-brain` dans `skills:`)
- Permissions Bash si necessaire
- Verification

---

## Plugin partage Bitbucket (optionnel)

Si certains composants sont identiques entre plusieurs repos, les extraire dans un plugin Bitbucket.

### Structure d'un plugin Claude Code

```
claude-dev-tools/
├── plugin.json              # Manifest (nom, version, description)
├── skills/                  # Skills auto-chargees par Claude selon contexte
│   ├── ma-skill/
│   │   ├── SKILL.md         # Contenu + frontmatter YAML
│   │   └── references/      # Fichiers de reference (progressive disclosure)
│   └── ...
├── agents/                  # Subagents specialises
│   ├── mon-agent.md         # Frontmatter : name, description, model, tools, skills, color
│   └── ...
├── hooks/                   # Scripts declenches sur des evenements
│   └── hooks.json           # Ou dans settings.json
├── .mcp.json                # Serveurs MCP (optionnel)
└── .lsp.json                # Serveurs LSP (optionnel)
```

### Composants expliques

**Skills** = connaissances et workflows que Claude charge automatiquement selon le contexte. Exemples :
- Conventions API REST de l'entreprise
- Regles SQL PostgreSQL
- Guide de creation d'endpoint
- Connexion au vault neoteem-brain (neo-brain)

Format : dossier avec `SKILL.md` (frontmatter YAML + contenu markdown). La `description` dans le frontmatter determine QUAND Claude charge la skill.

**Agents** = sous-agents specialises que Claude delegue des taches. Exemples :
- architect : design et review d'architecture
- dev : implementation de features
- test-writer : ecriture de tests
- code-reviewer : review de code
- debugger : diagnostic et correction de bugs

Format : fichier `.md` avec frontmatter YAML (name, description, model, tools, skills, effort, color, memory).

**Hooks** = scripts qui se declenchent automatiquement sur des evenements. Exemples :
- PreToolUse/Write : bloquer les imports interdits
- PostToolUse/Write : lancer le linting apres edition
- PostToolUse/Bash : notification Google Chat apres git push
- Stop : son de notification quand Claude termine

Format : scripts Python/TS/bash references dans `settings.json` ou `hooks.json`.

**Rules** = regles markdown chargees automatiquement a chaque session (ou conditionnellement par dossier). Exemples :
- Routing : qui appeler quand (quel agent pour quel besoin)
- Conventions : architecture hexagonale, patterns, database rules
- Workflows : pipeline de qualite (dev → test → review → validate)

Format : fichiers `.md` dans `.claude/rules/` du repo (pas dans le plugin — les rules sont specifiques a chaque repo).

### Creer le repo plugin

```bash
# Sur Bitbucket : neot-v2/claude-dev-tools
git clone https://bitbucket.org/neot-v2/claude-dev-tools.git
cd claude-dev-tools

mkdir -p skills agents
cat > plugin.json << 'EOF'
{
  "name": "dev-tools-neoteem",
  "version": "1.0.0",
  "description": "Agents et skills partages pour les repos Neoteem"
}
EOF
```

Raphael remplira les skills et agents ensuite. Les rules et hooks restent dans chaque repo (specifiques au stack).

### Referencer dans chaque repo

```json
// .claude/settings.json du repo
{
  "extraKnownMarketplaces": {
    "neoteem-tools": {
      "source": { "source": "git-url", "url": "https://bitbucket.org/neot-v2/claude-dev-tools.git" }
    }
  },
  "enabledPlugins": { "dev-tools-neoteem@neoteem-tools": true }
}
```

Claude Code poll le repo au demarrage + toutes les heures. Push sur Bitbucket → tous les devs ont la MAJ.

### Ce qui va dans le plugin vs dans le repo

| Composant | Plugin (partage) | Repo (specifique) |
|-----------|-----------------|-------------------|
| Skills communes (conventions, neo-brain) | Oui | Non |
| Agents communs (architect, reviewer) | Oui | Non |
| Skills specifiques au stack (drizzle, hono) | Non | Oui |
| Agents specifiques au repo | Non | Oui |
| Rules (routing, workflows) | Non | Oui — toujours dans le repo |
| Hooks (linting, securite) | Non | Oui — specifiques au stack |

---

## Repos a configurer (priorite)

| Repo | Stack | Priorite | Statut |
|------|-------|----------|--------|
| ia_back | Bun/Hono/Drizzle | Fait | .claude/ complet |
| neoteem-brain | Obsidian/Python | Fait | .claude/ complet |
| neo_ia | Python/FastAPI | Haute | A configurer |
| bdd | PL/pgSQL | Haute | A configurer |
| ws | Go | Haute | A configurer |
| lojii (neot-v2) | Node.js | Moyenne | A evaluer |
| Autres | Variable | Basse | Selon besoin |

---

## Pre-requis par poste dev

- Claude Code installe : `npm install -g @anthropic-ai/claude-code`
- Obsidian installe + vault neoteem-brain ouvert (pour la CLI)
- Python 3.10+ (pour les hooks)
- `git config core.hooksPath .githooks` sur chaque repo (notifications Google Chat)
