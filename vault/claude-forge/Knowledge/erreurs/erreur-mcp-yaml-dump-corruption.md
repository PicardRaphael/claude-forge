---
titre: "update_property yaml.dump corrompt le frontmatter"
resume: "yaml.dump() round-trippe tout le YAML (reordonne cles, re-quote dates) ET le fix regex qui l'a remplace casse les proprietes MULTI-LIGNES/arrays (tags) : items orphelins, double declaration. update_property/bulk inutilisables sur array."
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

### Meta — face a une consigne chiffree, la preuve directe bat le proxy compteur

Quand une consigne chiffree (« lint 132 inchange ») est violee par un **compteur agrege** : ne pas chasser le delta dans une **liste tronquee** (`lint_vault` affiche top 50 sur N → comparaison baseline↔courant impossible par construction, fantome). Produire une **preuve directe** de l'invariant reel vise par la consigne (intention = « ne casser aucun lien ») : `git diff --unified=0` filtre prouve que seules des lignes `  - "#tag"` ont bouge → un tel diff ne peut ni creer ni casser un wikilink. La preuve git bat le proxy compteur. Surfacer le compteur a l'utilisateur (cf [[feedback_ecart_consigne_chiffree_surfacer]]) **avec le fait prouve**, sans sur-affirmer l'origine (« pre-existant » n'est pas prouve ; « mon edit n'y est pour rien » l'est). Ne PAS `git stash` pour mesurer l'etat commite : le round-trip declenche la normalisation CRLF→LF (`.gitattributes`) — effet de bord a eviter quand on differe le commit CRLF.

## Liens

- [[erreur-mcp-stopwords-semantiques]]
- [[sqlite-fts5-vault]]
- [[pattern-mcp-brief-then-direct]] — doctrine MCP-only (garde = dumps lecture sous-agent)
- [[vault-edit-gotchas-outillage]] — autres gotchas ecriture vault (insert_section misparente)
