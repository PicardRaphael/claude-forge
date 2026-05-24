---
titre: "Paths relatifs dans .mcp.json — portabilité cross-machine"
resume: "Utiliser des paths relatifs au cwd du repo dans .mcp.json pour qu'un MCP serveur custom (wrapper Node) marche chez tous les collaborateurs sans modif manuelle"
aliases:
  - "mcp paths relatifs"
  - "mcp.json portable"
  - "mcp cross-machine"
  - "wrapper mcp paths"
  - "claude code mcp portabilité"
domaine: claude-code
type: technique
derniere-maj: 2026-05-24
auteur: claude
sources:
  - "Session 2026-05-20 — fix .mcp.json ia_back paths absolus Jérôme"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/mcp"
---

## Le problème

Un `.mcp.json` qui référence un wrapper Node custom avec **paths absolus hardcodés** ne marche que chez l'auteur original :

```json
// ❌ Cassé chez tous sauf Jérôme
{
  "mcpServers": {
    "postgres": {
      "command": "node",
      "args": [
        "C:/Users/jerome.arrighi_neote/Repositories/neot-v2/ia_back/mcp-postgres-wrapper.mjs",
        "postgresql://..."
      ],
      "env": {
        "PGSSLCERT": "C:/Users/jerome.arrighi_neote/Repositories/neot-v2/ia_back/certs/postgresql.crt"
      }
    }
  }
}
```

## La solution

Paths **relatifs au cwd du repo** (Claude Code lance le MCP depuis le dossier où `.mcp.json` vit) :

```json
// ✅ Marche chez tout le monde
{
  "mcpServers": {
    "postgres": {
      "command": "node",
      "args": [
        "./mcp-postgres-wrapper.mjs",
        "postgresql://..."
      ],
      "env": {
        "PGSSLCERT": "./certs/postgresql.crt",
        "PGSSLKEY": "./certs/postgresql.key",
        "PGSSLROOTCERT": "./certs/root.crt"
      }
    }
  }
}
```

## Pourquoi ça marche

1. Claude Code lance les commandes MCP avec **cwd = dossier du `.mcp.json`** (en général la racine du repo)
2. Node.js résout `./fichier.mjs` par rapport au cwd du process
3. `fs.readFileSync(process.env.PGSSLCERT)` avec `./certs/...` est résolu pareil

## Vérification

Pour confirmer le cwd où Claude lance le MCP :

```javascript
// Dans le wrapper, ajouter au début :
console.error(`MCP cwd: ${process.cwd()}`);
```

Doit afficher la racine du repo ia_back (ou autre repo selon le `.mcp.json`).

## Limites

- **Symlinks** : si le repo est cloné via symlink ou jonction, certains comportements Windows peuvent différer
- **Cross-repo** : si un repo A veut utiliser le wrapper d'un repo B (ex: neo_ia veut le wrapper postgres de ia_back), utiliser `../ia_back/mcp-postgres-wrapper.mjs` — fragile si les repos ne sont pas en sibling
- **Pas de variable d'env Claude Code** : à ma connaissance, pas de `${WORKSPACE_FOLDER}` ou équivalent dans `.mcp.json`. Les paths relatifs sont la seule option clean.

## Quand utiliser

- ✅ Wrapper MCP custom dans le même repo (ex: `mcp-postgres-wrapper.mjs` dans ia_back)
- ✅ Certificats / fichiers config dans le repo
- ✅ Repo partagé en équipe ou cloné sur plusieurs machines
- ❌ Référence à un binaire système global (utiliser le PATH ou un absolute path système)
- ❌ Référence à des fichiers utilisateur dans `~/.claude/` (utiliser absolute path explicite)

## Anti-patterns

- ❌ `C:/Users/jerome.arrighi_neote/...` — paths user hardcodés
- ❌ `~/dev/projet/...` — `~` n'est pas expandé dans `.mcp.json` JSON pur
- ❌ Dupliquer le wrapper et les certs dans chaque repo qui en a besoin — préférer paths relatifs `../autre-repo/`

## Cas Neoteem

`ia_back/.mcp.json` : paths relatifs ✅ (fix 2026-05-20)
- `./mcp-postgres-wrapper.mjs`
- `./certs/postgresql.crt`, `./certs/postgresql.key`, `./certs/root.crt`

`neo_ia/.mcp.json.postgres-optional` : template avec `../ia_back/` pour utilisation ponctuelle.

## Note de sécurité critique

Même avec des paths relatifs portables, **ne JAMAIS committer la connection string avec password en clair** dans `.mcp.json`. Voir [[erreur-password-postgres-clair-mcp-json]] — leak credential découvert dans cette même session.

Pattern correct : `"args": ["./wrapper.mjs", "${PG_CONNECTION_STRING}"]` avec `.env` gitignored.

## Liens

- [[erreur-password-postgres-clair-mcp-json]] — Erreur sécu connexe découverte
- **ia_back** (Neoteem) — Application concrète
- [[comment-creer-hook]] — Enforcement déterministe
- [[harness-engineering]] — Pattern foundational
