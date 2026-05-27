---
name: plugin-structure-cowork-claude-code
description: Structure obligatoire d'un plugin Cowork/Claude Code pour upload ZIP — .claude-plugin/plugin.json manifest + skills/ agents/ hooks/ au meme niveau
type: reference
originSessionId: 93007560-25b1-48eb-931d-043e24658f78
---
# Plugin Cowork/Claude Code — Structure obligatoire

## Erreur frequente

Zipper juste un dossier de skill et uploader dans Cowork donne :
```
Invalid plugin: missing .claude-plugin/plugin.json
```

Une skill seule n'est PAS un plugin. Il faut une structure de plugin autour.

## Structure minimale

```
mon-plugin/
  .claude-plugin/
    plugin.json          ← OBLIGATOIRE — manifest du plugin
  skills/
    nom-skill/
      SKILL.md
      references/
  agents/                ← optionnel
  commands/              ← optionnel (deprecated, prefer skills)
  hooks/                 ← optionnel
```

## Format plugin.json

```json
{
  "name": "nom-plugin",
  "version": "1.0.0",
  "description": "Description courte du plugin",
  "author": { "name": "Nom auteur" },
  "license": "MIT",
  "keywords": ["tag1", "tag2"]
}
```

**ATTENTION** : `author` DOIT etre un objet `{ "name": "..." }`, PAS une string. Une string cause :
```
Validation errors: author: Invalid input: expected object, received string
```

## Zipper correctement

Zipper le CONTENU du dossier plugin, pas le dossier lui-meme :

```bash
# CORRECT
cd mon-plugin/
powershell -Command "Compress-Archive -Path .claude-plugin,skills -DestinationPath ../mon-plugin.zip -Force"

# INCORRECT (cree un niveau supplementaire)
powershell -Command "Compress-Archive -Path mon-plugin -DestinationPath mon-plugin.zip"
```

Verifier le contenu du zip :
```
mon-plugin.zip/
  .claude-plugin/plugin.json
  skills/nom-skill/SKILL.md
```

Et PAS :
```
mon-plugin.zip/
  mon-plugin/.claude-plugin/plugin.json  ← mauvais
```

## Upload Cowork

Claude Desktop → Cowork → Customize → Plugins personnels → + → Upload ZIP

## Chaque skill dans skills/

Chaque skill est un dossier avec son SKILL.md et ses references. Le nom du dossier = le `name` dans le frontmatter YAML.
