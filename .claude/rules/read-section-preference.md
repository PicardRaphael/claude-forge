# Préférence read_section vs read_note

## Règle

Quand consultation vault MCP forge-brain :

- **Question PRÉCISE** → `read_section` ciblée d'abord (plus économe tokens)
- **Question LARGE** → `read_note` entière acceptable (besoin contexte complet)
- **Doute sur pertinence section seule** → `read_note` entière (mieux redondance que info manquante)

## Critères de décision

- `read_section` si : question cible un aspect précis ET section_id identifiable depuis `search_brain`
- `read_note` si : scope large (architecture globale), première lecture d'une note, ou doute

## Exemples

- "Best practice description skill" → `read_section("comment-creer-skill", "description")`
- "Comment fonctionne living doctrine" → `read_note("doctrine-vivante")` entière
- "Sources inspiration PIVOT" → `read_section("doctrine-vivante", "Sources")` après amendement

## Application

- Workflow : `search_brain` → décision section/note → `read_section` OU `read_note`
- Pas de dogme. Optimisation cas par cas.
- Si après `read_section` info manquante : escalader à `read_note` entière

## Anti-patterns

- ❌ `read_note` systématique sur grosse note (CHANGELOG, log) quand 1 section suffit → gaspillage tokens
- ❌ `read_section` quand on ne connaît pas la structure de la note → reading partial qui rate le contexte
- ❌ Refuser `read_note` entière par dogme tokens quand le besoin est large → info manquante = retour Read

## Référence

Pattern complémentaire : [[pattern-mcp-brief-then-direct]] — la session principale brief sub-agents avec extraits ciblés, pas notes entières.
