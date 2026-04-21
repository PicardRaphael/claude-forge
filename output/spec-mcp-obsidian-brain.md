# MCP Obsidian Brain — Spec de dev

## Contexte

Claude Cowork tourne dans un sandbox Linux isole qui ne peut pas executer la CLI Obsidian directement (elle a besoin de l'instance Obsidian ouverte sur la machine Windows). Ce MCP local sert de pont : il tourne sur la machine, appelle la CLI Obsidian, et expose les resultats comme tools MCP.

**Stack :** Python + FastMCP
**Prerequis :** Obsidian ouvert avec le vault `neoteem-brain` + CLI activee (Settings → General → Enable CLI)
**Consommateurs :** Claude Cowork + Claude Code (via connecteur MCP)

---

## Wrapper CLI — Regle absolue

Sur Windows + Git Bash, `obsidian` resout vers `Obsidian.exe` (GUI) au lieu de `Obsidian.com` (console/CLI). Le MCP doit utiliser le bon binaire.

Resolution du binaire (dans l'ordre) :
1. `C:\Program Files\Obsidian\Obsidian.com`
2. `%LOCALAPPDATA%\Programs\Obsidian\Obsidian.com`
3. Fallback : `obsidian` dans le PATH

Voir le script `scripts/obsidian-cli.sh` dans le repo neoteem-brain pour reference.

---

## Tools MCP a implementer

### 1. `search_brain`

Recherche full-text dans le vault via l'index Obsidian (aliases, noms de fichiers, contenu).

**Parametres :**
| Param | Type | Requis | Description |
|-------|------|--------|-------------|
| query | string | oui | Terme de recherche |
| limit | int | non | Nombre max de resultats (default 5) |
| context | bool | non | Si true, retourne les lignes autour du match (default true) |

**Logique :**
```python
cmd = context and "search:context" or "search"
result = run_obsidian_cli(f'vault="neoteem-brain" {cmd} query="{query}" limit={limit}')
```

**Retour :** resultats de recherche avec noms de fichiers et extraits

---

### 2. `read_note`

Lit le contenu complet d'une note par son nom (resolution wikilink).

**Parametres :**
| Param | Type | Requis | Description |
|-------|------|--------|-------------|
| file | string | oui | Nom de la note (sans chemin, sans extension) |

**Logique :**
```python
result = run_obsidian_cli(f'vault="neoteem-brain" read file="{file}"')
```

**Retour :** contenu markdown de la note

---

### 3. `read_note_by_path`

Lit une note par son chemin exact dans le vault.

**Parametres :**
| Param | Type | Requis | Description |
|-------|------|--------|-------------|
| path | string | oui | Chemin depuis la racine du vault (ex: `02-BDD/tables/t-acteur.md`) |

**Logique :**
```python
result = run_obsidian_cli(f'vault="neoteem-brain" read path="{path}"')
```

**Retour :** contenu markdown de la note

---

### 4. `get_backlinks`

Liste les notes qui pointent vers une note donnee.

**Parametres :**
| Param | Type | Requis | Description |
|-------|------|--------|-------------|
| file | string | oui | Nom de la note |

**Logique :**
```python
result = run_obsidian_cli(f'vault="neoteem-brain" backlinks file="{file}" counts')
```

**Retour :** liste de notes avec nombre de liens

---

### 5. `get_tags`

Liste tous les tags du vault avec leur nombre d'occurrences.

**Parametres :** aucun

**Logique :**
```python
result = run_obsidian_cli('vault="neoteem-brain" tags sort=count counts')
```

**Retour :** liste de tags tries par frequence

---

## Implementation

### Structure du projet

```
mcp-obsidian-brain/
  pyproject.toml
  src/
    server.py              # point d'entree FastMCP
    obsidian.py            # wrapper CLI (resolution binaire + subprocess)
    tools/
      brain.py             # les 5 tools ci-dessus
```

### Dependances

```
fastmcp>=2.0
```

Pas d'autre dependance. Le MCP appelle la CLI via subprocess, c'est tout.

### Wrapper CLI (obsidian.py)

```python
import subprocess
import os
import shutil
from pathlib import Path


def resolve_obsidian_bin() -> str:
    """Resout le binaire Obsidian CLI selon l'OS."""
    # Windows : Obsidian.com (console) prioritaire sur Obsidian.exe (GUI)
    if os.name == "nt":
        candidates = [
            Path("C:/Program Files/Obsidian/Obsidian.com"),
            Path(os.environ.get("LOCALAPPDATA", ""), "Programs/Obsidian/Obsidian.com"),
        ]
        for candidate in candidates:
            if candidate.exists():
                return str(candidate)

    # Fallback : obsidian dans le PATH
    obsidian = shutil.which("obsidian")
    if obsidian:
        return obsidian

    raise FileNotFoundError(
        "Obsidian CLI introuvable. "
        "Verifier que Obsidian est installe et que 'cli' est active dans les settings."
    )


OBSIDIAN_BIN = resolve_obsidian_bin()


def run_obsidian_cli(args: str) -> str:
    """Execute une commande Obsidian CLI et retourne le stdout."""
    cmd = f'"{OBSIDIAN_BIN}" {args}'
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Obsidian CLI error: {result.stderr}")
    return result.stdout
```

### Server (server.py)

```python
from fastmcp import FastMCP

mcp = FastMCP(
    name="obsidian-brain",
    instructions="Acces au vault neoteem-brain via la CLI Obsidian. "
                 "Utilise search_brain pour chercher des concepts metier, "
                 "read_note pour lire une note, get_backlinks pour les liens."
)

from tools.brain import register_tools
register_tools(mcp)

if __name__ == "__main__":
    mcp.run()
```

### Tools (brain.py)

```python
from obsidian import run_obsidian_cli


def register_tools(mcp):

    @mcp.tool()
    def search_brain(query: str, limit: int = 5, context: bool = True) -> str:
        """Recherche dans le vault neoteem-brain. Utilise l'index Obsidian (aliases, contenu, noms)."""
        cmd = "search:context" if context else "search"
        return run_obsidian_cli(
            f'vault="neoteem-brain" {cmd} query="{query}" limit={limit}'
        )

    @mcp.tool()
    def read_note(file: str) -> str:
        """Lit une note par son nom (resolution wikilink, sans chemin ni extension)."""
        return run_obsidian_cli(f'vault="neoteem-brain" read file="{file}"')

    @mcp.tool()
    def read_note_by_path(path: str) -> str:
        """Lit une note par son chemin exact (ex: 02-BDD/tables/t-acteur.md)."""
        return run_obsidian_cli(f'vault="neoteem-brain" read path="{path}"')

    @mcp.tool()
    def get_backlinks(file: str) -> str:
        """Liste les notes qui pointent vers cette note avec le nombre de liens."""
        return run_obsidian_cli(f'vault="neoteem-brain" backlinks file="{file}" counts')

    @mcp.tool()
    def get_tags() -> str:
        """Liste tous les tags du vault tries par frequence."""
        return run_obsidian_cli('vault="neoteem-brain" tags sort=count counts')
```

---

## Deploiement

### Service Windows (production)

```powershell
# Installer comme service Windows via nssm (Non-Sucking Service Manager)
nssm install obsidian-brain "C:\Python313\python.exe" "-m" "src.server"
nssm set obsidian-brain AppDirectory "C:\chemin\vers\mcp-obsidian-brain"
nssm start obsidian-brain
```

Ou via Task Scheduler au demarrage de la session.

### Configuration Cowork

Ajouter comme connecteur MCP dans Cowork (meme methode que MCP JIRA - NEOTEEM).

### Configuration Claude Code

```json
{
  "mcpServers": {
    "obsidian-brain": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "C:\\chemin\\vers\\mcp-obsidian-brain"
    }
  }
}
```

---

## Contraintes

- **Obsidian doit tourner** — la CLI communique avec l'instance ouverte, pas avec le filesystem
- **Read-only** — ce MCP ne fait que de la lecture. Pas de create, append, ou property:set
- **Timeout 30s** — si Obsidian ne repond pas en 30s, le tool echoue proprement
- **Un seul vault** — hardcode sur `neoteem-brain`. Si besoin d'un autre vault plus tard, ajouter un parametre `vault`
- **Windows seulement** — le wrapper de resolution binaire est prevu pour Windows. Adapter si macOS/Linux dans l'equipe

---

## Test rapide

```bash
# Verifier que la CLI marche
python -c "from src.obsidian import run_obsidian_cli; print(run_obsidian_cli('vault=\"neoteem-brain\" search query=\"test\" limit=3'))"

# Lancer le serveur
python -m src.server

# Tester via Claude : "Cherche 'charges copropriete' dans le brain"
```
