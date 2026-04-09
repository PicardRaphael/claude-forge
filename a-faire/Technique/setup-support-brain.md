# Guide technique : Setup Support Brain

**Pour :** DevOps
**Temps estime :** 1 heure

---

## Architecture cible

```
Dossier reseau partage              Bitbucket (backup + versionning)
\\serveur\support-brain\     ←→     neot-v2/support-brain
  │  (script auto-sync)
  ├── CLAUDE.md
  ├── FAQ/
  ├── Process/
  ├── Solutions/
  ├── Escalade/
  └── Templates/
         │
   Supports ouvrent Claude Desktop
   pointent vers \\serveur\support-brain\
```

---

## Etape 1 — Creer le repo Bitbucket (5 min)

```bash
# Sur Bitbucket, creer le repo neot-v2/support-brain

git clone https://bitbucket.org/neot-v2/support-brain.git
cd support-brain

# Structure initiale
mkdir -p FAQ Process Solutions Escalade Templates
touch CLAUDE.md

git add -A
git commit -m "Init support-brain"
git push
```

---

## Etape 2 — Creer le dossier reseau partage (15 min)

Sur le serveur de fichiers :

1. Creer `\\serveur\support-brain\` (ou equivalent cloud : OneDrive, Google Drive partage)
2. Permissions : lecture + ecriture pour l'equipe support
3. Cloner le repo dans ce dossier :

```bash
cd \\serveur\support-brain\
git clone https://bitbucket.org/neot-v2/support-brain.git .
```

---

## Etape 3 — Script auto-sync (15 min)

Creer un script qui synchronise le dossier reseau avec Bitbucket :

### Option A — Task Scheduler Windows

```powershell
# sync-support-brain.ps1
$brainDir = "\\serveur\support-brain"

Push-Location $brainDir

# Pull les changements des autres
git pull --ff-only 2>&1

# Push les changements locaux (notes creees par Claude)
git add -A
$changes = git diff --cached --name-only
if ($changes) {
    git commit -m "Auto-sync: $($changes.Count) fichier(s) modifie(s)"
    git push
}

Pop-Location
```

Planifier toutes les 15 minutes via Task Scheduler.

### Option B — Git auto-commit plugin (si Obsidian est utilise)

Si le vault est aussi ouvert dans Obsidian, le plugin **Git** fait le sync automatiquement.

---

## Etape 4 — Installer Claude Desktop sur les postes (15 min/poste)

1. Telecharger Claude Desktop : https://claude.com/download
2. Installer
3. Se connecter avec le compte Claude Team de l'employe
4. Pointer vers le dossier partage :
   - Cowork → "Open folder" → `\\serveur\support-brain\`

Le plugin "Support Neoteem" sera auto-installe si le marketplace GitHub est configure (voir `setup-github-orga.md`).

---

## Etape 5 — CLAUDE.md initial

Raphael redigera le contenu. Le DevOps n'a qu'a s'assurer que le fichier est present et que le sync fonctionne.

---

## Structure du plugin Cowork "Support Neoteem"

Le plugin est sur GitHub (voir `setup-github-orga.md`). Il contient des **skills** uniquement (pas d'agents, rules, hooks — Cowork n'en a pas besoin).

```
claude-support-plugin/
├── plugin.json              # Manifest
└── skills/                  # Skills auto-chargees dans Cowork
    ├── ticket-triage/
    │   └── SKILL.md         # Triage automatique
    ├── knowledge-search/
    │   └── SKILL.md         # Recherche dans le vault support
    ├── escalation/
    │   └── SKILL.md         # Matrice d'escalade
    └── capitalize/
        └── SKILL.md         # Ecrire la solution dans le vault
```

**Difference avec le plugin dev (Claude Code) :**

| | Plugin Support (Cowork) | Plugin Dev (Claude Code) |
|---|---|---|
| Heberge sur | GitHub (obligatoire) | Bitbucket (suffit) |
| Contient | Skills uniquement | Skills + Agents |
| Rules/Hooks | Non (pas dans Cowork) | Dans chaque repo, pas le plugin |
| Auto-update | Marketplace sync 30 min | Poll git URL 1h |
| Public cible | Non-technique | Developpeurs |

Les skills du plugin support seront definies avec l'equipe support selon leurs besoins reels. Raphael les creera.

---

## Monitoring

### Verifier le sync

```powershell
# Dernier sync
git -C "\\serveur\support-brain" log --oneline -5

# Fichiers modifies non synces
git -C "\\serveur\support-brain" status
```

### Alertes

Si le sync echoue (conflit git, permissions...), le script doit alerter. Ajouter a la fin du script :

```powershell
if ($LASTEXITCODE -ne 0) {
    # Envoyer alerte (email, Google Chat webhook, etc.)
}
```

---

## Securite

- Le dossier reseau ne contient PAS de donnees clients (FAQ, process, solutions generiques)
- Les permissions fichier limitent l'acces a l'equipe support
- Git versionne tout — rollback possible a tout moment
- Claude Desktop ne peut ecrire QUE dans le dossier pointe (pas ailleurs sur le serveur)
