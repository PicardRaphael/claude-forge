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

### Gotcha annexe — `get_tags` retarde apres ecriture raw

Apres ecriture **hors MCP** (script raw), l'agregat `get_tags` accuse un **delai de reindexation** de quelques secondes (vu UNE fois divergeant de `find_by_property`, puis resorbe). Ce n'est PAS un cache casse : `find_by_property` et `get_property` refletent le disque immediatement ; seul l'agregat global traine, puis se met a jour. Pour un avant/apres fiable juste apres ecriture : se fier a `find_by_property` par tag, ou relancer `get_tags` apres un court delai.

## Liens

- [[erreur-mcp-stopwords-semantiques]]
- [[sqlite-fts5-vault]]
- [[pattern-mcp-brief-then-direct]] — doctrine MCP-only (garde = dumps lecture sous-agent)
- [[vault-edit-gotchas-outillage]] — autres gotchas ecriture vault (insert_section misparente)
