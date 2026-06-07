---
titre: "update_property yaml.dump corrompt le frontmatter"
resume: "Historique : yaml.dump() round-trippait tout le YAML, puis le fix regex 1-ligne cassait les arrays (tags/aliases/sources) en items orphelins. RÉSOLU 7 juin 2026 (commit 2ff0538) : splice chirurgical + IO byte-exact (newline=\"\"). update_property/bulk sont array-safe."
aliases:
  - "erreur yaml dump"
  - "yaml corruption frontmatter"
  - "update_property bug"
  - "yaml round-trip corruption"
  - "update_property casse array tags"
  - "bulk_update_property destructif array"
type: erreur
derniere-maj: 2026-06-07
auteur: claude
tags:
  - "#type/erreur"
  - "#erreur/infra"
  - "#domaine/claude-code"
---

## Ce qui s est passe

`update_property` dans `brain.py` utilisait `yaml.safe_load()` + `yaml.dump()` pour modifier une seule propriete. Le round-trip complet corrompait silencieusement le frontmatter :
- Cles reordonnees alphabetiquement
- Dates re-quotees (`2026-05-10` → `'2026-05-10'`)
- Resumes longs wrappes sur 2 lignes
- Commentaires YAML detruits

## Pourquoi c etait une erreur

Modifier 1 propriete ne devrait pas toucher les autres. Le round-trip YAML est un anti-pattern connu — PyYAML ne preserve pas l'ordre ni le style.

## Fix

Remplace par regex ciblee : cherche `^{name}:.*$` et remplace la ligne. Si la propriete n existe pas, l ajoute a la fin du frontmatter. Zero impact sur les autres proprietes.

## Alternative consideree

`ruamel.yaml` preserve l'ordre et le style, mais ajoute une dependance externe. La regex suffit pour les cas simples (proprietes scalaires).

## AJOUT 2026-06-07 — Le fix regex casse les proprietes MULTI-LIGNES (arrays)

Le fix ci-dessus precise « regex suffit pour les cas simples (proprietes scalaires) ». Chantier 2/5 normalisation tags (7 juin 2026) a heurte empiriquement la limite : sur une propriete au format **liste YAML multi-lignes**, le fix actuel corrompt.

**OBSERVE** (vu directement, note `erreur-pipeline-trop-long-frustration`) : `update_property(name="tags", value="#a, #b")` sur un frontmatter au format
```
tags:
  - "#a"
  - "#b"
```
matche `^tags:.*$` (la ligne `tags:` vide), y injecte la string CSV `tags: #a, #b`, et **laisse les items `- "#a"` orphelins en dessous** → double declaration de la cle, frontmatter casse. La regex ligne-unique ne sait pas qu'une liste YAML s'etend sur les lignes suivantes.

**INFERE du schema** (jamais teste cette session) : `bulk_update_property(name, value)` prend une `value` scalaire et l'ecrit sur N notes — sur un array il ecraserait toute la liste par cette unique valeur (destructif). Param scalaire → meme angle mort, amplifie. A confirmer empiriquement avant de s'y fier.

### Etat outil

Le cas array est **NON corrige cote outil** (pas seulement non documente) — `update_property`/`bulk_update_property` restent inutilisables pour les proprietes multi-valeurs (tags surtout). Pour patcher `brain.py` : detecter le format liste (ligne `name:` suivie de `  - `) et reconstruire le bloc complet, pas la ligne unique.

### Contournement valide (chantier 2/5)

Pour une transformation de masse de tags : **script Python deterministe en session principale** (cf `.claude/scripts/normalize-tags.py`) qui parse les 2 formats reels du vault (liste YAML + inline array `[...]`), preserve CRLF + guillemets + ordre, avec dry-run + `--show` avant/apres. Conforme doctrine MCP-only (la garde `vault-cat-guard` vise les dumps de LECTURE sous-agent, pas un script d'ecriture deterministe en session principale — cf [[pattern-mcp-brief-then-direct]]). Pour une note isolee : `update_note` (reecriture complete maitrisee), jamais `update_property` sur un array.

### Gotcha annexe — les agregats (`get_tags`, `lint_vault`) retardent apres ecriture raw

Apres ecriture **hors MCP** (script raw), les vues **agregees** accusent un **delai de reindexation** :
- `get_tags` : vu UNE fois divergeant de `find_by_property`, puis resorbe.
- `lint_vault` (compteur de wikilinks brises) : chantier 2/5 LOT A — affichait 132→133 (+1) et **ne s'est pas restabilise** apres un re-run. Or le diff git etait **100 % tag-only** (0 wikilink touche, 0 ligne hors `  - "#..."`, ajout comme suppression) ET `lint` rapportait **0 frontmatter casse** → l'edit ne pouvait PAS, par construction, creer ou casser un lien. Le compteur a derive seul. Indice corroborant : `context-actuel` capturait une baseline 131 le meme matin → ces compteurs fluctuent (131/132/133) independamment des edits de tags.

Ce n'est PAS un cache casse : `find_by_property` et `get_property` refletent le disque immediatement ; seuls les agregats globaux trainent.

### Cicatrice — notes au format yaml.dump sautees par un rename suppose-guillemets-doubles

Les notes qu'`update_property` a round-trippe gardent une signature : **cles triees alpha + guillemets SIMPLES** (`'#tag'`) + items parfois non indentes. Chantier 2/5 LOT E1 : le script de rename suppose les guillemets DOUBLES (`val.startswith('"')`) → sur une apostrophe simple, le tag n'est pas reconnu → la note est **sautee proprement** (le script n'ecrit que si un changement matche, donc zero corruption — coherent avec « 0 frontmatter casse »). Une seule note touchee (`MOC-Techniques`, `#type/techniques` non fusionne), detectee par le `get_tags` reindexe (residu unique de tous les mappings) et corrigee via `update_note`. Lecon : un rename de masse base sur le format dominant (double-quote) saute silencieusement les cicatrices single-quote — verifier le residu via l'agregat reindexe APRES, pas seulement le diff. Reformater globalement ces notes = chantier de format distinct (hors normalisation tags).

### Meta — face a une consigne chiffree, la preuve directe bat le proxy compteur

Quand une consigne chiffree (« lint 132 inchange ») est violee par un **compteur agrege** : ne pas chasser le delta dans une **liste tronquee** (`lint_vault` affiche top 50 sur N → comparaison baseline↔courant impossible par construction, fantome). Produire une **preuve directe** de l'invariant reel vise par la consigne (intention = « ne casser aucun lien ») : `git diff --unified=0` filtre prouve que seules des lignes `  - "#tag"` ont bouge → un tel diff ne peut ni creer ni casser un wikilink. La preuve git bat le proxy compteur. Surfacer le compteur a l'utilisateur (cf [[feedback_ecart_consigne_chiffree_surfacer]]) **avec le fait prouve**, sans sur-affirmer l'origine (« pre-existant » n'est pas prouve ; « mon edit n'y est pour rien » l'est). Ne PAS `git stash` pour mesurer l'etat commite : le round-trip declenche la normalisation CRLF→LF (`.gitattributes`) — effet de bord a eviter quand on differe le commit CRLF.

## Liens

- [[erreur-mcp-stopwords-semantiques]]
- [[sqlite-fts5-vault]]
- [[pattern-mcp-brief-then-direct]] — doctrine MCP-only (garde = dumps lecture sous-agent)
- [[vault-edit-gotchas-outillage]] — autres gotchas ecriture vault (insert_section misparente)


## RÉSOLU 2026-06-07 — Chantier 5 limite #2 : `update_property` array-safe (commit `2ff0538` forge)

Le cas array est désormais **CORRIGÉ côté outil**. Les sections ci-dessus (« NON corrigé côté outil », contournement script Python obligatoire) sont **périmées** pour `brain.py` à partir de ce commit. Le script `normalize-tags.py` reste valable pour une transformation de masse, mais `update_property`/`bulk_update_property` sont maintenant utilisables sur les arrays.

### Le fix réel (2 bugs, pas 1)

1. **Cause racine confirmée** : la regex `^{name}:.*$` (MULTILINE) ne remplaçait que la ligne-clé → items `- ...` orphelins. Remplacée par un **splice chirurgical** : helper pur `_set_property_in_frontmatter(content, name, value)` qui remplace le **span complet** de la propriété (ligne-clé + toutes ses continuations indentées/`- items`/vides jusqu'à la prochaine clé top-level). Rendu calibré sur le **style maison réel** (lu via MCP : bloc, items 2 espaces, guillemets doubles, dates scalaires non quotées). **Jamais `yaml.safe_dump`** (il reformaterait tout le frontmatter — c'était le bug d'origine de cette note).

2. **2e bug découvert au test live (le piège caché)** : `write_text` (mode texte Windows, `newline=None`) **convertit `\n` → `\r\n`** à l'écriture. Comme `read_text` aplatit déjà tout en LF à la lecture, un fichier **LF était intégralement réécrit en CRLF** = diff full-file. **Mesure réelle : le vault est mixte — 301 CRLF, 166 LF, 2 mixtes.** Donc bug **ACTIF** (pas latent) : un `bulk_update_property` aurait reformaté jusqu'à 166 notes LF d'un coup. Fix : `read_text(..., newline="")` + `write_text(..., newline="")` → le helper devient **seule autorité EOL**, le zéro-diff tient **par construction** (LF reste LF, CRLF reste CRLF, BOM préservé).

### Validations (gate Raphael : ZÉRO diff collatéral, pas « minimisé »)

- Signature `value: str | list[str]` — FastMCP transmet les `list` **nativement** (prouvé empiriquement : probe `bulk_update_property` sur notes inexistantes → `0/N introuvable`, garde `isinstance` non déclenché ; schéma JSON généré = `{"type":"array"}`). Le gotcha [[reference_workflow_args_array_gotcha]] (Dynamic Workflows) ne s'applique PAS aux tools MCP typés.
- Garde anti-YAML-cassé : refuse d'écrire si le frontmatter résultant ne reparse pas (`yaml.safe_load`) ou si la propriété ne porte pas la valeur voulue.
- 17 tests dédiés (`tests/test_update_property_arrays.py`) : splice chirurgical, scalaire non quoté, array bloc, reindex CRLF in-memory propre (pas de `\r` dans l'index SQLite), live byte-exact LF + CRLF, idempotence. **155/155** suite complète MCP verte.

### Découvertes annexes HORS-SCOPE (notées, pas corrigées — à traiter si récurrence)

- **`parse_note` (indexer.py) + BOM en tête** : `_FRONTMATTER_RE` exige `^---`. Un BOM UTF-8 en tête fait échouer le match → frontmatter **ignoré silencieusement** (tags/aliases vides à l'index, **sans warning**). **0 note du vault affectée aujourd'hui** (les 469 scannées sont sans BOM en tête ; le BOM trouvé dans `comment-creer-skill` est en milieu de fichier = double-frontmatter, autre anomalie). Le splice, lui, **préserve** un BOM en tête. Cf feedback mémoire `bom-skillmd-casse-frontmatter`.
- **`append_note` (`open(..., "a")` sans `newline=""`)** : même pattern de traduction EOL que l'ancien `update_property` — pourrait coller du CRLF dans un fichier LF. Non vérifié, non corrigé.
