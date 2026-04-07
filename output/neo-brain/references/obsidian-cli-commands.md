# Commandes CLI Obsidian — Reference

Toutes les commandes utilisent le prefixe `obsidian vault="neoteem-brain"`.

## Lecture

| Commande | Description |
|---|---|
| `search query="..." limit=N` | Recherche plein texte via l'index Obsidian (pas le filesystem) |
| `search:context query="..." limit=N` | Recherche avec lignes de contexte autour du match |
| `read file="nom-note"` | Lire une note. `file=` resout comme un wikilink (nom seul) |
| `read path="chemin/exact/note.md"` | Lire une note par chemin exact |
| `backlinks file="nom-note" counts` | Lister les notes pointant vers celle-ci |
| `tags sort=count counts` | Lister tous les tags avec nombre d'occurrences |

## Ecriture

| Commande | Description |
|---|---|
| `create path="Knowledge/..." content="..." silent` | Creer une note. `silent` evite d'ouvrir dans Obsidian |
| `append file="nom-note" content="..."` | Ajouter du contenu en fin de note |
| `property:set name="cle" value="val" file="nom-note"` | Modifier une propriete frontmatter |

## Regles

- `file=` resout comme un wikilink : nom seul, sans chemin ni extension
- `path=` est le chemin exact depuis la racine du vault
- `limit=` par defaut varie selon la commande, toujours le preciser pour controler le volume
- L'index Obsidian est ~70 000x plus economique en tokens que lire les fichiers directement
- La CLI communique avec l'instance Obsidian ouverte — pas de mode headless
