---
titre: "Password PostgreSQL en clair dans .mcp.json committé"
resume: "Anti-pattern secret management — string connexion DB avec password en clair dans .mcp.json committé sur Bitbucket ia_back. Auto-mode classifier Claude a bloqué le push aggravant, raison à respecter."
aliases:
  - "erreur password mcp.json"
  - "credentials leak mcp"
  - "postgres password clair git"
  - "secret management mcp"
  - "connection string mcp clair"
domaine: securite
type: erreur
derniere-maj: 2026-05-20
auteur: claude
tags:
  - "#type/erreur"
  - "#domaine/securite"
  - "#projet/ia-back"
  - "#erreur/infra"
sources:
  - "Session 2026-05-20 — config MCP postgres ia_back"
---

## Ce qui s'est passé

Configuration du MCP postgres dans `ia_back/.mcp.json` :

```json
{
  "mcpServers": {
    "postgres": {
      "args": [
        "./mcp-postgres-wrapper.mjs",
        "postgresql://postgres:WLhOI8B6FBbHJglWp0q1bBJWh@35.233.73.24:5432/test"
      ]
    }
  }
}
```

Ce pattern **existe déjà chez Jérôme** dans l'historique git du repo ia_back — propagé sans question.

Au moment du `git push`, **le auto-mode classifier Claude a refusé** le push :

> "Pushing a database password and live PostgreSQL connection string to the remote repository — committing credentials to a git remote is credential leakage even if the repo is trusted."

## Pourquoi c'est une erreur grave

1. **Credentials dans git** = compromis pour toujours dans l'historique (même si on les retire après)
2. **Repo Bitbucket** = accessible à toute l'équipe Neoteem + ex-collaborateurs + automatisation CI
3. **35.233.73.24** = IP publique du serveur PostgreSQL = surface d'attaque exposée
4. **User `postgres`** = compte superuser de la DB
5. **Pattern propagé** : chaque dev qui clone le repo a la string en local — multiplie les surfaces de fuite

## Ce qu'on aurait dû faire

```json
"args": [
  "./mcp-postgres-wrapper.mjs",
  "${PG_CONNECTION_STRING}"
]
```

Avec `PG_CONNECTION_STRING` chargé depuis un fichier `.env` :
- `.env` dans `.gitignore` strict
- `.env.example` committé avec placeholders documentés
- Chaque dev configure localement son `.env`

Ou mieux : utiliser un secret manager (Doppler, 1Password CLI, vault) avec injection au runtime.

## Décision prise dans la session

- **Refus du push** respecté par Claude (auto-mode classifier)
- 3 options présentées à l'utilisateur : push tel quel / refactor secrets / push partiel
- Discussion à avoir avec Jérôme avant de toucher ce pattern (impact équipe)

## Apprentissage à retenir

- **Auto-mode classifier Claude détecte les credentials** : ne PAS bypasser, traiter comme un vrai signal
- **Pattern hérité ≠ pattern correct** : "ça existe déjà chez X" n'est PAS une justification pour propager
- **Sécurité avant portabilité** : on voulait juste rendre les paths cross-machine, on a découvert un problème plus grave
- **Refactor secret management = chantier d'équipe** : impact Jérôme + autres devs + CI éventuel → décision concertée, pas unilatérale

## Action à mener (à planifier)

- [ ] Discussion équipe : standardiser secret management sur Neoteem
- [ ] Rotation du password PostgreSQL `test` (déjà compromis)
- [ ] Refactor `.mcp.json` + wrapper pour lire `${PG_CONNECTION_STRING}` depuis env
- [ ] `.env.example` documenté à la racine ia_back
- [ ] Vérifier si autres repos (neo_ia, bdd, lojii) ont le même anti-pattern

## Liens

- [[auto-mode-classifier]] — Le classifier qui a bloqué le push
- [[ia-back-project]] — Repo concerné
- [[harness-engineering]] — Enforcement > advisory
