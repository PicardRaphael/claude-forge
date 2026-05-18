---
titre: "Pattern Figma MCP + Claude Code"
resume: "Plugin officiel figma@claude-plugins-official : 7 skills, workflow design-to-code pixel-perfect, distribution equipe via enabledPlugins"
aliases:
  - figma mcp
  - figma claude code
  - figma plugin claude
  - design-to-code figma
  - pixel-perfect figma
  - figma-implement-design
  - figma-create-design-system-rules
  - figma skills mcp
type: knowledge
derniere-maj: 2026-05-13
auteur: claude
sources:
  - "https://help.figma.com/hc/en-us/articles/39166810751895-Figma-skills-for-MCP"
  - "https://github.com/figma/mcp-server-guide"
  - "https://help.figma.com/hc/en-us/articles/39888612464151-Claude-Code-and-Figma-Set-up-the-MCP-server"
tags:
  - "#type/knowledge"
  - "#domaine/tech"
  - "#outil/claude-code"
  - "#outil/figma"
---

## Plugin officiel

```bash
claude plugin install figma@claude-plugins-official
```

Le plugin inclut le MCP server + les skills + les rules. Le MCP seul (`.mcp.json`) ne donne que les tools bruts sans les skills guidees.

### Distribution equipe

Dans `.claude/settings.json` (commite) :
```json
"enabledPlugins": {
  "figma@claude-plugins-official": true
}
```

Quand un collegue ouvre le projet, Claude Code lui propose d'installer le plugin automatiquement.

### Setup MCP fallback (sans plugin)

Dans `.mcp.json` :
```json
"figma": { "type": "http", "url": "https://mcp.figma.com/mcp" }
```

Ou desktop : `claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp`

## 7 Skills du plugin

| Skill | Role | Quand l'utiliser |
|-------|------|-----------------|
| **figma-implement-design** | Convertit un design Figma en code pixel-perfect | Implementer un composant depuis une maquette |
| **figma-create-design-system-rules** | Analyse le codebase et genere un fichier de conventions design | Debut de projet, onboarding, conventions team |
| **figma-code-connect-components** | Lie composants Figma publies ↔ code via Code Connect | Dev Mode, navigation design→code |
| **figma-use** | Ecrire sur le canvas Figma (frames, composants, variables, auto layout) | Creer/modifier du contenu Figma depuis Claude |
| **figma-use-figjam** | Ecrire sur un board FigJam (stickies, sections, connectors) | Brainstorm, diagrams |
| **figma-create-new-file** | Creer un fichier Figma vierge | Premier pas avant figma-use |
| **figma-generate-design** | Genere des ecrans Figma depuis le code (code→design) | Synchro code→Figma |

## Workflow pixel-perfect officiel

1. **`get_design_context(nodeId)`** — donnees structurees du node (layout, tokens, variables)
2. **`get_metadata(fileKey)`** — si trop gros, mapper les nodes d'abord
3. **`get_screenshot(nodeId)`** — reference visuelle
4. **Telecharger les assets** (`download_figma_images`)
5. **Implementer** en traduisant vers les conventions du projet
6. **Valider** 1:1 contre la maquette avant de marquer termine

### Limite tokens

Claude Code limite les reponses MCP a **25 000 tokens**. Si `get_design_context` depasse → utiliser `get_metadata` d'abord puis fetch node par node.

## `figma-create-design-system-rules`

- **N'a PAS besoin d'URL Figma** par defaut — analyse le codebase
- **Peut prendre une URL Figma** si on la passe en input → analyse codebase + design system
- **Genere un fichier de conventions** (tokens, composants, nommage) dans `rules/` ou `instructions/`
- **Attention** : peut proposer d'ecrire dans les skills existantes du projet. Verifier la destination avant d'accepter → preferer un nouveau fichier `rules/design-system.md`

## Integration avec les agents projet

Les skills du plugin sont **globales** — elles s'ajoutent aux skills projet sans conflit. Mais pour que les agents les utilisent automatiquement :
- Ajouter `figma-implement-design` dans le frontmatter `skills:` de `vue-dev` et `architect`
- Mentionner dans le body : "Quand un lien Figma est dans le ticket, utiliser `figma-implement-design`"

## Rate limits

| Plan | Limite |
|------|--------|
| Starter / View / Collab | **6 tool calls / mois** |
| Professional / Organization / Enterprise (Dev ou Full seat) | Per-minute (Tier 1 Figma REST API) |

## Liens

- [[lojii]] — premier projet configure avec le plugin Figma
- [[pattern-architect-first-pipeline]] — pipeline qui integre le design Figma
