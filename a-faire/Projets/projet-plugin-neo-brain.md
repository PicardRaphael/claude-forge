# Projet : Plugin neo-brain — Connexion vault pour tous les repos

**Date :** 9 avril 2026
**Porteur :** Raphael Picard

---

## Le probleme

Pour qu'un dev ait le contexte metier quand il code, il faut copier le kit `neo-brain` dans le `.claude/skills/` de chaque repo. Aujourd'hui :
- 2 repos connectes (ia_back, neoteem-brain)
- ~126 repos pas connectes
- A chaque mise a jour du kit → recopier dans chaque repo manuellement

## La solution

Un **plugin Bitbucket** `neo-brain`. Chaque repo le reference dans son `settings.json` — plus besoin de copier.

```
AUJOURD'HUI :
  ia_back/.claude/skills/neo-brain/     ← copie locale
  neoteem-brain/.claude/skills/neo-brain/ ← copie locale
  neo_ia → pas connecte
  bdd → pas connecte
  ws → pas connecte

DEMAIN :
  Bitbucket: neot-v2/neo-brain-plugin/  ← source unique
  
  ia_back/settings.json → enabledPlugins: "neo-brain@neoteem-plugins"
  neo_ia/settings.json  → enabledPlugins: "neo-brain@neoteem-plugins"
  bdd/settings.json     → enabledPlugins: "neo-brain@neoteem-plugins"
  ws/settings.json      → enabledPlugins: "neo-brain@neoteem-plugins"
  = 1 source, tous les repos connectes
```

## Ce que ca change

| Avant | Apres |
|-------|-------|
| Copier le kit dans chaque repo | 3 lignes dans settings.json |
| MAJ = recopier partout | 1 push Bitbucket = tous a jour (poll 1h) |
| 2 repos connectes au vault | Tous les repos connectes |
| Dev code sans contexte metier | Dev code avec le vault |

## Ce que contient le plugin

```
neo-brain-plugin/
├── plugin.json
└── skills/
    └── neo-brain/
        ├── SKILL.md                    # Skill complete (search, read, capitalize)
        ├── scripts/
        │   └── obsidian-cli.sh         # Wrapper CLI Windows
        └── references/
            ├── obsidian-cli-commands.md
            └── knowledge-conventions.md
```

C'est exactement le kit standalone qui existe deja dans `neoteem-brain/neo-brain/`, mis dans un format plugin.

## Prerequis

| Action | Qui | Effort |
|--------|-----|--------|
| Creer repo Bitbucket `neot-v2/neo-brain-plugin` | DevOps | 5 min |
| Packager le kit existant en plugin | Raphael | 30 min |
| Ajouter `enabledPlugins` dans les repos | DevOps ou Raphael | 2 min/repo |

**Pas besoin de GitHub.** Bitbucket suffit (Claude Code poll toutes les heures).

**Cout supplementaire :** zero
