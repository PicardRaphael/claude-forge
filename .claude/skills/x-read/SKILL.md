---
name: x-read
description: ALWAYS invoke when the user types `/x-read <url>`, `/x-read timeline [N]`, or `/x-read @user [N]`. Reads X/Twitter content (tweets, timeline, user posts) from the authenticated personal account using cookies. Read-only enforced by construction — no write methods exposed. Use to capitalize tweets into forge-brain vault or fetch content blocked by Defuddle/WebFetch.
user-invokable: true
argument-hint: "<url> | timeline [N] | @user [N]"
allowed-tools: Bash, Read
---

# X-Read — Lecture Twitter/X en mode read-only

Lit du contenu X/Twitter (tweet, timeline, tweets d'un user) et le formate en markdown vault-ready.
Backend : `twitter-api-client` (Trevor Hobenshield). Cookies dans `~/.claude/secrets/x-cookies.json`.

## Dispatch des arguments

| Argument | Mode | Exemple |
|----------|------|---------|
| `https://x.com/...` | tweet par URL | `/x-read https://x.com/trq212/status/123` |
| `timeline [N]` | home feed | `/x-read timeline 30` |
| `@handle [N]` | tweets d'un user | `/x-read @bcherny 10` |
| (aucun) | demande de précision | `/x-read` |

## Étapes

### 1. Vérifier les prérequis

Vérifier que `~/.claude/secrets/x-cookies.json` existe :

```bash
python3 .claude/skills/x-read/reader.py check
```

Si le fichier n'existe pas -> afficher :
```
Cookies manquants. Guide setup : .claude/skills/x-read/references/cookie-setup.md
```

Vérifier que `twitter-api-client` est installé :
```bash
python3 -c "import twitter" 2>&1
```
Si erreur -> installer :
```bash
pip install "twitter-api-client>=0.10.20,<0.12.0"
```

### 2. Parser les arguments

Règles de dispatch (PAS de $ARGUMENTS dans des backticks -- utiliser des variables séparées) :
- Commence par `http` -> mode `tweet`, arg = URL
- Est `timeline` (seul ou suivi d'un nombre) -> mode `timeline`, arg = N (défaut 20)
- Commence par `@` -> mode `user`, arg = handle sans @, N (défaut 10)
- Vide -> poser la question : URL de tweet ? timeline ? @user ?

### 3. Appeler reader.py

Mode tweet :
```bash
python3 .claude/skills/x-read/reader.py tweet "https://x.com/..."
```

Mode timeline :
```bash
python3 .claude/skills/x-read/reader.py timeline 20
```

Mode user :
```bash
python3 .claude/skills/x-read/reader.py user "bcherny" 10
```

### 4. Formater en markdown vault-ready

L'output JSON de reader.py doit être rendu en markdown propre :

```markdown
## @auteur -- [Date]

> Contenu du tweet

Liens : [URL]
Médias : [si présents]
```

Pour une timeline ou une liste : un bloc `##` par tweet, séparés par `---`.

### 5. Proposer la sauvegarde

Si le contenu est intéressant pour capitalisation, proposer :
```
Voulez-vous sauvegarder ce tweet dans vault/claude-forge/0-Inbox/ ?
```

Si oui -> créer une note via forge-brain MCP (`create_note`) avec frontmatter minimal :
```yaml
titre: "[auteur] -- [date] -- [début du tweet]"
type: knowledge
tags: ["#type/knowledge", "#source/twitter"]
```

## Gotchas

- **Images attachées** — toujours utiliser mode `pretty` qui les télécharge. Sans téléchargement local, Claude ne peut pas voir les images des tweets.
- **Articles X (`x.com/i/article/...`)** — le tweet ne contient que le lien, pas le contenu. Pas accessible via API tweet seule.
- **URLs t.co** — pretty mode les expand automatiquement, mode tweet garde les t.co. Toujours préférer pretty.
- **Dossier downloads/** — gitignored, médias non commités.
- **Cookies = accès complet au compte X** -- JAMAIS commiter `x-cookies.json`. Le fichier est dans `~/.claude/secrets/` (hors repo, gitignore `secrets/` dans `~/.claude/.gitignore`)
- **`home_timeline` est sur `Account`, pas `Scraper`** -- reader.py utilise `Account(cookies=...)` UNIQUEMENT pour `home_latest_timeline`. Les méthodes write (`tweet`, `like`, `follow`) ne sont JAMAIS importées ni exposées dans le CLI
- **Rate limits X** -- ~50 requêtes/15 min selon endpoint. Si 429 -> attendre 15 min
- **Cookies expirent** -- si 401 Unauthorized -> refaire le setup via `references/cookie-setup.md`
- **JAMAIS `$ARGUMENTS` dans des backticks** -- construire la commande Bash avec des variables séparées pour chaque argument
- **Windows paths** -- toujours `Path.home()` en Python, pas de hardcode `C:\Users\...`
- **API twitter-api-client peut casser** -- pinner la version dans requirements.txt. Si une méthode n'existe plus, noter la version cassante dans la section Apprentissage
- **thread complet** -- pour un tweet en reply, `tweets_by_ids` retourne le tweet seul. Utiliser `tweet_details` si besoin du thread complet

## Apprentissage

- Mode `pretty` ajouté 2026-05-20 : Claude est multimodal, peut Read les images locales téléchargées. Sans téléchargement, images invisibles.
Capturer ici les patterns observés en production :

- Si `twitter-api-client` casse à une version -> noter version fonctionnelle dans requirements.txt avec pin
- Si X invalide les cookies plus tôt que 30j -> noter la durée observée
- Si `home_latest_timeline` n'est pas disponible sur `Account` -> noter la version et l'alternative
- Si `users_by_login` retourne un format différent -> documenter la structure JSON réelle
- Si le rate limit est plus bas que prévu -> noter l'endpoint et la limite réelle

## Références

- `references/cookie-setup.md` -- guide pas-à-pas récupération cookies depuis DevTools (Chrome/Edge/Firefox, Windows)
- Package : `twitter-api-client` (Trevor Hobenshield) -- Scraper (read public) + Account (read authenticated)
