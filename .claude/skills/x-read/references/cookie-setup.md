# Récupérer cookies X — guide setup

## Pré-requis

- Être logged-in sur https://x.com avec ton compte personnel
- Chrome, Edge ou Firefox (Windows 11)

## Étape 1 — Ouvrir DevTools sur x.com

1. Va sur https://x.com (connecté)
2. `F12` ou `Ctrl+Shift+I` -> ouvre DevTools
3. Onglet **Application** (Chrome/Edge) ou **Stockage** (Firefox)
4. Sidebar gauche : **Cookies** -> `https://x.com`

## Étape 2 — Copier 2 cookies

| Name | Longueur | Description |
|------|----------|-------------|
| `auth_token` | ~40 chars hex | Jeton d'authentification principal |
| `ct0` | ~160 chars hex | CSRF token (requis en plus de auth_token) |

Clic droit sur la valeur -> **Copy Value** pour chaque.

## Étape 3 — Créer le fichier secrets

Le fichier vit **dans claude-forge** (pas dans `~/.claude/`) — protégé par `.gitignore` du repo.

Crée le dossier si nécessaire :
```
C:\Users\raphael.picard_neote\Documents\claude-forge\.claude\secrets\
```

Crée le fichier `x-cookies.json` à l'intérieur :
```json
{
  "ct0": "ta-valeur-ct0-ici",
  "auth_token": "ta-valeur-auth-token-ici"
}
```

## Étape 4 — Sécurité (OBLIGATOIRE)

Le `.gitignore` de claude-forge contient `/.claude/secrets/` — vérifier avec :
```bash
grep secrets .gitignore
```

**JAMAIS commiter `x-cookies.json`** — ces cookies donnent un accès complet à ton compte X (lecture ET écriture).

## Étape 5 — Vérifier le setup

```bash
python3 .claude/skills/x-read/reader.py check
```

Résultat attendu : `OK: cookies found and twitter-api-client installed`

Si `pip install twitter-api-client` manque :
```bash
pip install "twitter-api-client>=0.10.20,<0.12.0"
```

## Durée de vie des cookies

Les cookies expirent typiquement après ~30 jours d'inactivité ou si tu te déconnectes manuellement.
Si la skill retourne `401 Unauthorized` ou `ERROR: cookies not found` -> refaire étapes 1-3.

## Dépannage

| Erreur | Cause | Solution |
|--------|-------|----------|
| `ERROR: cookies not found` | Fichier absent | Créer le fichier (étape 3) |
| `ERROR: invalid JSON` | Syntaxe incorrecte | Vérifier guillemets et virgules |
| `401 Unauthorized` | Cookies expirés | Refaire étapes 1-3 |
| `429 Too Many Requests` | Rate limit X | Attendre 15 min |
| `ERROR: pip install twitter-api-client` | Package manquant | `pip install "twitter-api-client>=0.10.20,<0.12.0"` |
| `home_latest_timeline not available` | Version trop ancienne | `pip install "twitter-api-client>=0.10.20"` |
