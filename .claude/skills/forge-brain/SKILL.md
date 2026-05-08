---
name: forge-brain
description: Search, read, and write to the forge-brain Obsidian vault — persistent infinite memory for AI tools, techniques, prompts, industry news, mistakes, and everything learned. Use PROACTIVELY at session start, before creating any skill/agent/hook/prompt, before answering technical questions, after cc-news, and after significant mistakes.
---

# Forge Brain

Knowledge base Obsidian de claude-forge. Stocke tout ce que j'apprends : Claude Code, concurrents, modèles, techniques, leaders, industrie.

**Vault** : `vault/claude-forge/`

## Quand utiliser — Le vault est un RÉFLEXE

| Situation | Action |
|-----------|--------|
| Début de session | Chercher les notes récentes pour rappel contexte |
| **Avant de créer skill/agent/hook/prompt** | **Chercher best practices + erreurs passées + prompts réutilisables** |
| **Analyse de repo / projet** | **Chercher patterns, concurrents, techniques pertinentes** |
| Question sur feature/outil | Chercher dans le vault AVANT de répondre |
| Après cc-news | Créer/mettre à jour les notes avec les découvertes |
| Nouvelle info apprise | Créer une note atomique |
| **Erreur significative commise** | **Créer note dans `Knowledge/erreurs/` avec template `erreur.md`** |
| Info potentiellement datée | Vérifier la note existante + `derniere-maj` |

## CLI — RÈGLE ABSOLUE (Windows)

**Ne JAMAIS appeler `obsidian` directement.** Toujours utiliser le wrapper :
```bash
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh <command>
```

### Pre-check (OBLIGATOIRE)

```bash
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh version 2>/dev/null
```
- Succès → utiliser la CLI (via le wrapper)
- Échec → fallback vers `Read`/`Write`/`Glob`/`Grep` directement sur les fichiers du vault

## Commandes courantes

```bash
# Rechercher
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" search query="Opus 4.7" limit=10

# Lire une note
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" read file="Opus 4.7"

# Lister les tags
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" tags

# Propriétés d'une note
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" property:get file="Opus 4.7" property=derniere-maj
```

## Créer une note

**La CLI ne supporte pas les `:` dans content=** (casse le parser YAML). Toujours utiliser `Write` :

1. Lire le template correspondant : `Read("vault/claude-forge/Templates/<type>.md")`
2. Créer la note avec `Write` en suivant le template
3. Ajouter le wikilink dans le MOC correspondant

## Structure du vault

```
00-Hub/           — Home + 6 MOCs (index par thème)
01-Claude-Code/   — features/, changelog/, best-practices/, hooks/, skills/, agents/
02-Concurrents/   — gemini-cli/, codex/, copilot/, cursor/, xai/
03-Modeles/       — claude/, gpt/, gemini/, grok/
04-Techniques/    — prompt-engineering/, context-engineering/, patterns/
05-Leaders/       — Fiches personnes clés
06-Industrie/     — Market, funding, événements, tendances
07-Prompts/       — system-prompts/, agent-prompts/, skill-prompts/, templates-prompts/
Knowledge/        — explorations/, syntheses/
Templates/        — 10 templates (feature, changelog, best-practice, leader, technique, modele, concurrent, deprecation, knowledge, prompt)
```

## Templates (OBLIGATOIRE)

Toujours lire le template AVANT de créer une note :

| Dossier cible | Template |
|---|---|
| `01-Claude-Code/features/` | `Templates/feature.md` |
| `01-Claude-Code/changelog/` | `Templates/changelog.md` |
| `01-Claude-Code/best-practices/` | `Templates/best-practice.md` |
| `02-Concurrents/` | `Templates/concurrent.md` |
| `03-Modeles/` | `Templates/modele.md` |
| `04-Techniques/` | `Templates/technique.md` |
| `05-Leaders/` | `Templates/leader.md` |
| `06-Industrie/` | `Templates/knowledge.md` |
| `07-Prompts/` | `Templates/prompt.md` |
| `Knowledge/` | `Templates/knowledge.md` |

## Frontmatter obligatoire

```yaml
---
titre: "Titre lisible"
resume: "1 ligne"
aliases:
  - "synonyme"
domaine: claude-code | gemini | openai | copilot | cursor | xai | technique | industrie
type: feature | changelog | deprecation | best-practice | technique | leader | modele | concurrent | knowledge
derniere-maj: YYYY-MM-DD
auteur: claude
sources:
  - "URL ou [[wikilink]]"
tags:
  - "#type/<type>"
  - "#domaine/<domaine>"
---
```

## Règles

1. **1 concept = 1 note** — atomique, jamais de dump monolithique
2. **Wikilinks** partout — `[[Opus 4.7]]`, `[[Boris Cherny]]`
3. **MOC à jour** — chaque nouvelle note doit être linkée dans son MOC
4. **derniere-maj** — mettre à jour à chaque édition
5. **Ne jamais modifier Templates/** — lecture seule
6. **Vault ≠ mémoire projet** — le vault stocke du savoir référence, pas du feedback/projet

## Gotchas

- **CLI wrapper obligatoire Windows** — ne jamais appeler `obsidian` directement, toujours `bash .claude/skills/forge-brain/scripts/obsidian-cli.sh`. L'exécutable résolu sur Windows est `Obsidian.exe` au lieu de `.com`, le wrapper corrige ça.
- **Colons dans `content=` cassent la CLI** — le parser YAML interprète les `:` comme séparateurs. Pour créer des notes avec frontmatter, toujours utiliser `Write` directement sur le fichier vault.
- **Fallback Read/Glob si Obsidian fermé** — faire un pre-check `version` avant toute commande CLI. Si échec, basculer vers `Read`/`Write`/`Glob`/`Grep` sur les fichiers du vault directement.
- **Aliases minimum 4-6 par note** — standard neoteem-brain : inclure synonymes FR/EN et variantes techniques (ex : "Opus 4.7", "claude-opus-4-7", "opus47", "Claude Opus").

## Apprentissage

Après chaque session significative utilisant le vault :
- Vérifier que les notes créées/modifiées sont correctement linkées
- Mettre à jour les MOCs si de nouvelles notes ont été ajoutées
- Si un pattern de recherche revient souvent, créer une note synthèse dans `Knowledge/syntheses/`
