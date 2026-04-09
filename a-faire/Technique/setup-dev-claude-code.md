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

Si certains agents/skills sont identiques entre plusieurs repos, les extraire dans un plugin :

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
