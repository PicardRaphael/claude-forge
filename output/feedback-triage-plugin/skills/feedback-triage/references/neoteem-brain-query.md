# Neoteem Brain — Reference pour le triage

## Acces via skill Cowork

La skill `/neo-brain` est deja installee comme plugin dans Cowork (plugin Neoteem brain). Elle sait interroger le vault `neoteem-brain`.

**Invocation :**
```
/neo-brain cherche "charges copropriete" dans le vault
```

Ou en langage naturel :
```
/neo-brain explique moi la notion de vote en AG de copropriete
```

La skill gere elle-meme la strategie d'acces (CLI si disponible, fallback sur lecture directe des .md si sandbox).

## Quand consulter le brain

| Situation | Action |
|-----------|--------|
| Feedback mentionne un terme metier inconnu | `/neo-brain cherche "<terme>"` |
| Doute sur si le comportement agent est correct | Chercher la regle metier dans le brain |
| Feedback sur un domaine specifique (syndic, gerance, compta) | Chercher dans le domaine concerne |
| Besoin de comprendre les liens entre entites | Demander au brain les relations |

## Mode Query — Token-smart

Pour le triage, utiliser le **Mode Query** (pas le Mode Exploration) :
1. Une recherche ciblee d'abord
2. Si besoin, lire la note la plus pertinente
3. Ne pas lire tout le vault — juste le minimum pour comprendre

La skill `/neo-brain` gere ca automatiquement.

## Organisation du vault (pour info)

| Dossier | Contenu |
|---------|---------|
| `01-Domaines/` | Regles metier (syndic, gerance, compta) |
| `02-BDD/` | Tables, fonctions PG, schemas |
| `03-Apps/` | Documentation des applications (neochat, neodoc, neomail, ia_back) |
| `Knowledge/` | Connaissances accumulees, syntheses, explorations |

## Fallback si la skill echoue

Si `/neo-brain` n'est pas disponible dans la session, chercher directement dans les fichiers .md du vault monte :
- Le vault est dans `neoteem-brain/` (sous le dossier autorise Cowork)
- Utiliser Grep/Read sur les .md
- Limiter aux dossiers `01-Domaines/`, `02-BDD/`, `Knowledge/` pour le triage

## Gotchas

- Ne pas ecrire dans le vault pendant le triage (lecture seule)
- Limiter les recherches pour economiser les tokens
- Si une info est mal comprise, chercher aussi dans les aliases (la skill le fait automatiquement)
