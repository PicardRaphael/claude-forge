---
titre: "Pattern Figma MCP + Claude Code"
resume: "Plugin officiel figma@claude-plugins-official : 8 skills officielles, workflow design-to-code pixel-perfect, distribution équipe via enabledPlugins"
aliases:
  - figma mcp
  - figma claude code
  - figma plugin claude
  - design-to-code figma
  - pixel-perfect figma
  - figma skills mcp
type: knowledge
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://help.figma.com/hc/en-us/articles/39166810751895-Figma-skills-for-MCP"
  - "https://github.com/figma/mcp-server-guide"
  - "https://help.figma.com/hc/en-us/articles/39888612464151-Claude-Code-and-Figma-Set-up-the-MCP-server"
  - "https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/"
  - "https://docs.claude.com/en/docs/claude-code/mcp"
tags:
  - "#type/knowledge"
  - "#domaine/tech"
  - "#domaine/claude-code"
  - "#domaine/figma"
---

## Plugin officiel

```bash
claude plugin install figma@claude-plugins-official
```

Le plugin inclut le MCP server + les skills + les rules. Le MCP seul (`.mcp.json`) ne donne que les tools bruts sans les skills guidées.

### Distribution équipe

Dans `.claude/settings.json` (commit) :
```json
"enabledPlugins": {
  "figma@claude-plugins-official": true
}
```

Quand un collègue ouvre le projet, Claude Code lui propose d'installer le plugin automatiquement.

### Setup MCP fallback (sans plugin)

Dans `.mcp.json` :
```json
"figma": { "type": "http", "url": "https://mcp.figma.com/mcp" }
```

Ou desktop : `claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp`

## 8 Skills officielles du plugin

Source : https://help.figma.com/hc/en-us/articles/39166810751895-Figma-skills-for-MCP

| Skill | Rôle |
|-------|------|
| **figma-use** | Écrire sur le canvas Figma (frames, composants, variables, auto layout) |
| **figma-use-figjam** | Écrire sur un board FigJam (stickies, sections, connectors) |
| **figma-use-slides** | Écrire dans Figma Slides |
| **figma-code-connect** | Lier composants Figma publiés ↔ code via Code Connect |
| **figma-create-new-file** | Créer un fichier Figma vierge |
| **figma-generate-diagram** | Générer un diagramme dans FigJam |
| **figma-generate-library** | Générer une component library |
| **figma-generate-design** | Générer un fichier Figma design depuis le code (code→design) |

⚠️ Correction 2026-05-23 : la liste précédente contenait des noms inventés (`figma-implement-design`, `figma-create-design-system-rules`, `figma-code-connect-components`) — ceux-ci n'existent PAS dans la liste officielle Figma. Liste vérifiée verbatim help.figma.com.

## Workflow pixel-perfect officiel

1. **`get_design_context(nodeId)`** — données structurées du node (layout, tokens, variables)
2. **`get_metadata(fileKey)`** — si trop gros, mapper les nodes d'abord
3. **`get_screenshot(nodeId)`** — référence visuelle
4. **Télécharger les assets** (`download_figma_images`)
5. **Implémenter** en traduisant vers les conventions du projet
6. **Valider** 1:1 contre la maquette avant de marquer terminé

### Limite tokens Claude Code

Claude Code limite les réponses MCP : **warning à 10 000 tokens, max default 25 000 tokens**.

> Verbatim docs.claude.com : *"Claude Code displays a warning when MCP tool output exceeds 10,000 tokens, and the default maximum is 25,000 tokens."*

Override possible via env var `MAX_MCP_OUTPUT_TOKENS=50000`. Annotation `anthropic/maxResultSizeChars` outrepasse pour le contenu texte. Pas d'override possible pour images (seule solution = augmenter `MAX_MCP_OUTPUT_TOKENS`).

## Intégration avec les agents projet

Skills du plugin **globales** — s'ajoutent aux skills projet sans conflit. Pour les agents :
- Ajouter une des skills figma dans le frontmatter `skills:` de l'agent
- Mentionner dans le body : "Quand un lien Figma est dans le ticket, utiliser `figma-code-connect` ou `figma-generate-design`"

## Rate limits

Source : https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/

| Plan / Seat | Limite |
|------|--------|
| Starter / View / Collab seat | **6 tool calls / mois** (hard cap, écriture exemptée) |
| Pro Dev/Full seat | Per-minute (Tier 1 Figma REST API) |
| Organization Dev/Full seat | **200 calls / jour** |
| Enterprise Dev/Full seat | **600 calls / jour** |

Note : tools en écriture (write to Figma files) sont **exemptés** du cap mensuel Starter.

## Liens

- [[lojii]] — premier projet configuré avec le plugin Figma
- [[workflow-claude-code-optimal]]
