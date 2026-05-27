---
name: neoteem-brain-vault-pipeline
description: neoteem-brain doit suivre le pipeline complet repo-analyzer → vault-linker → sync-checker. Ne jamais s'arreter apres la creation des notes.
type: feedback
originSessionId: 424370ce-3cf7-4ae9-bb8b-d6ff1e01fec1
---
Quand on analyse un repo dans neoteem-brain, le pipeline complet est OBLIGATOIRE :
1. repo-analyzer (analyse + création notes via obsidian-cli)
2. vault-linker (wikilinks + MOCs + Knowledge)
3. sync-checker (vérif aliases double couverture + intégrité + rapport)

**Why:** Claude s'arrêtait systématiquement après repo-analyzer. Notes créées sans wikilinks, sans aliases support, sans MOC mis à jour. Le vault devenait un tas de fichiers au lieu d'un knowledge graph.

**How to apply:**
- Rule `vault-workflow.md` impose le pipeline
- Rule `use-obsidian-cli.md` interdit Write direct sur le vault
- Rule `aliases-obligatoires.md` impose double couverture (technique + support) avec mapping déterministe
- `frontmatter-enricher` supprimé, absorbé par sync-checker + rule aliases
- repo-analyzer a maintenant obsidian-cli et obsidian-markdown dans ses skills
