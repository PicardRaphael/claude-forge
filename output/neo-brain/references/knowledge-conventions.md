# Conventions Knowledge — neoteem-brain

## Frontmatter obligatoire

Chaque note creee dans `Knowledge/` doit avoir :

```yaml
---
titre: "Titre descriptif"
resume: "1 ligne — la reponse courte ou le fait principal"
aliases:
  - "synonyme, formulation alternative, terme metier equivalent"
type: knowledge          # ou knowledge-qa, knowledge-synthesis
cree: YYYY-MM-DD
sources:
  - "note-source-1"
  - "note-source-2"
auteur: claude
repo: nom-du-repo        # le repo depuis lequel la decouverte a ete faite
derniere-maj: YYYY-MM-DD
tags:
  - "#type/knowledge"
  - "#domaine/xxx"       # syndic, gerance, compta, bdd, archi...
---
```

### resume (obligatoire)

Une seule ligne qui permet de trier les resultats de recherche sans lire la note. Doit repondre a "de quoi parle cette note ?" en 15 mots max.

### aliases (obligatoire)

Synonymes, formulations alternatives, noms techniques, abreviations. L'index Obsidian les indexe — les recherches CLI trouvent les notes via leurs aliases.

## Sous-dossiers

| Dossier | Usage | Prefixe | Exemple |
|---|---|---|---|
| `Knowledge/questions/` | Reponse a une question metier precise | `q-` | `q-rapprochement-bancaire.md` |
| `Knowledge/syntheses/` | Croisement de 2+ notes existantes | `s-` | `s-couverture-bdd-complete.md` |
| `Knowledge/explorations/` | Decouverte faite depuis le code | `e-` | `e-cycle-vie-locataire.md` |

## Nommage

- `kebab-case` uniquement
- Francais sauf noms techniques (tables, fonctions, variables)
- Pas d'accents dans les noms de fichiers

## Wikilinks

- **Obligatoires** — une note sans lien est un bug
- Utiliser `[[nom-note]]` (pas de chemin, pas d'extension)
- Toujours lier vers les notes sources qui ont inspire la decouverte

## Zones protegees

| Dossier | Permission |
|---|---|
| `00-Hub/` | Lecture seule (MOCs geres par vault-linker) |
| `01-Domaines/` | Lecture seule |
| `02-BDD/` | Lecture seule |
| `03-Apps/` | Lecture seule |
| `04-Projets/` | Lecture seule |
| `05-Decisions/` | Lecture seule |
| `Knowledge/` | Lecture + ecriture |
| `Templates/` | Lecture seule |
