# Guide technique : Plugin neo-brain (Bitbucket)

**Pour :** DevOps + Raphael
**Temps estime :** 30 minutes

---

## Etape 1 — Creer le repo Bitbucket (5 min)

```bash
# Creer le repo sur Bitbucket : neot-v2/neo-brain-plugin
git clone https://bitbucket.org/neot-v2/neo-brain-plugin.git
cd neo-brain-plugin
```

## Etape 2 — Structurer le plugin (10 min)

```bash
mkdir -p skills/neo-brain/scripts skills/neo-brain/references

cat > plugin.json << 'EOF'
{
  "name": "neo-brain",
  "version": "1.0.0",
  "description": "Connect any Neoteem repo to the neoteem-brain Obsidian vault for business context"
}
EOF
```

Copier les fichiers depuis le kit existant :

```bash
# Depuis neoteem-brain/neo-brain/
cp neoteem-brain/neo-brain/SKILL.md          skills/neo-brain/SKILL.md
cp neoteem-brain/neo-brain/scripts/*         skills/neo-brain/scripts/
cp neoteem-brain/neo-brain/references/*      skills/neo-brain/references/
```

```bash
git add -A
git commit -m "Init neo-brain plugin"
git push
```

## Etape 3 — Connecter un repo (2 min par repo)

Ajouter dans le `settings.json` du repo cible :

```json
{
  "extraKnownMarketplaces": {
    "neoteem-plugins": {
      "source": { "source": "git-url", "url": "https://bitbucket.org/neot-v2/neo-brain-plugin.git" }
    }
  },
  "enabledPlugins": { "neo-brain@neoteem": true }
}
```

Commit et push le settings.json. C'est tout.

## Etape 4 — Verification

```bash
cd mon-repo
claude
# Puis demander :
# "Cherche dans le vault ce qu'est un tantieme"
# Claude doit utiliser neo-brain pour chercher
```

## Mise a jour

Quand Raphael ameliore le plugin (nouvelle commande, fix wrapper, etc.) :

```bash
cd neo-brain-plugin
# Modifier les fichiers
git add -A && git commit -m "Fix: ..." && git push
```

Claude Code sur chaque repo detecte le changement au prochain demarrage ou dans l'heure. Zero action sur les repos.

## Migration depuis le kit copie

Pour les repos qui ont deja `neo-brain` copie dans `.claude/skills/` (ia_back, neoteem-brain) :

1. Ajouter le `enabledPlugins` dans settings.json
2. Supprimer `.claude/skills/neo-brain/` du repo
3. Commit et push

Le plugin remplace la copie locale.

## Pre-requis par poste dev

- Obsidian ouvert avec le vault neoteem-brain
- CLI Obsidian activee (Settings → General → Enable CLI)
- Le wrapper `obsidian-cli.sh` gere automatiquement Windows Git Bash
