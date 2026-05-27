---
name: vault-audit
description: Audits and optionally fixes notes in the forge-brain Obsidian vault. Use when the user asks to audit, check quality, find orphans, fix frontmatter, normalize tags, or score notes. Use PROACTIVELY after cc-news capitalisation or note creation to verify vault quality.
argument-hint: "[fix] [--top N] [--full] [--note NAME]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
user-invokable: true
effort: high
memory: project
---

Audits the forge-brain Obsidian vault (96+ notes) for quality issues and applies deterministic corrections on demand.

## Usage

```
/vault-audit             — audit report (top 10 worst notes)
/vault-audit fix         — audit + deterministic fixes
/vault-audit --full      — audit all notes (verbose)
/vault-audit --top 20    — audit top 20 worst
/vault-audit --note "Opus 4.7"  — audit single note
/vault-audit fix --dry-run      — show what would be fixed, no writes
```

Compatible avec `/loop` pour monitoring périodique.

## Étapes

### 1. Accès vault via MCP

Le MCP forge-brain (auto-start, port 8091) fournit search, read, backlinks, tags.
audit.py accède directement au filesystem pour le scoring (pas besoin du MCP).

### 2. Lancer l'audit

```bash
python3 .claude/skills/vault-audit/scripts/audit.py [options]
```

Options disponibles :
- `--vault-path PATH` — chemin absolu vers le vault (détecté automatiquement sinon)
- `--output json|table` — format de sortie (défaut : table markdown)
- `--top N` — afficher les N pires notes (défaut : 10)
- `--full` — afficher toutes les notes
- (filtrer une note seule : pas encore supporté — utiliser `--full | grep "NomNote"`)

### 3. Si $ARGUMENTS contient "fix" : lancer les corrections déterministes

```bash
python3 .claude/skills/vault-audit/scripts/fix.py [--dry-run] [--note "NomNote"]
```

Corrections appliquées automatiquement :
- Ajout des champs frontmatter manquants (valeurs vides/défaut)
- Ajout `auteur: claude` si absent
- Ajout section `## Liens` si absente
- Ajout `[[MOC-*]]` si dossier a un MOC connu et section Liens présente
- Initialisation `derniere-maj` à aujourd'hui si vide

**Non corrigé automatiquement (suggestions seulement) :**
- Aliases pauvres (< 4) — jugement LLM requis, trop risqué en `/loop`
- Resume non informatif — réécriture LLM
- Wikilinks cassés — renommage fichier ou suppression
- Tags sémantiquement incorrects — vérification manuelle

### 4. Présenter le rapport

Afficher le tableau markdown produit par `audit.py`.
Commenter les 3-5 problèmes les plus fréquents.
Proposer les étapes suivantes (fix? corrections manuelles prioritaires?).

### 5. (Optionnel) Enrichissement assisté

Pour les notes grade D avec aliases pauvres ou resume vide :
1. Lire la note : `Read("vault/claude-forge/<path>")`
2. Proposer 4 aliases (synonymes FR, termes EN, noms techniques, termes recherche)
3. Proposer un résumé informatif (40+ chars, distinct du titre)
4. Attendre confirmation avant d'écrire

## Rubrique de scoring

| Critère | Poids | Détail |
|---------|-------|--------|
| Frontmatter complet (7 champs) | 30 | titre, resume, aliases, type, derniere-maj, auteur, tags |
| Aliases ≥ 4 | 15 | synonymes FR, termes EN, noms techniques, termes recherche |
| Resume informatif | 10 | > 40 chars, distinct du titre |
| Tags #type/X + #domaine/Y | 10 | les deux requis sauf type=leader/knowledge/erreur |
| Wikilinks internes (pas markdown) | 10 | pas de `[texte](note.md)`, utiliser `[[wikilink]]` |
| Lien MOC dans ## Liens | 10 | ex. `[[MOC-Claude-Code]]` selon dossier |
| Sections template respectées | 10 | ## Liens minimum |
| derniere-maj < 30 jours | 5 | warning si > 30 jours |

**Grades :** A ≥ 90 | B ≥ 75 | C ≥ 60 | D < 60

## MOC par dossier

| Dossier | MOC attendu |
|---------|-------------|
| 01-Claude-Code | [[MOC-Claude-Code]] |
| 02-Concurrents | [[MOC-Concurrents]] |
| 03-Modeles | [[MOC-Modeles]] |
| 04-Techniques | [[MOC-Techniques]] |
| 05-Leaders | [[MOC-Leaders]] |
| 06-Industrie | [[MOC-Industrie]] |
| 07-Prompts | [[MOC-Prompts]] |
| 0-Inbox | aucun (zone de brouillon) |
| 1-Projets | aucun — wikilink vers projet parent obligatoire |
| 2-Casquettes | aucun — wikilink vers [[Raphael-Picard]] obligatoire |

## Gotchas

**Le fix est déterministe, pas intelligent.** `fix.py` n'invente pas d'aliases ni ne réécrit les resumes. Ces enrichissements nécessitent un jugement LLM — les proposer interactivement, ne jamais les appliquer automatiquement (surtout en mode `/loop`).

**Ne pas confondre notes orphelines et notes sans valeur.** Les MOCs dans `00-Hub/` auront toujours des backlinks. Les templates dans `Templates/` sont exclus du scan. Une note "orpheline" peut être intentionnellement standalone (ex. Bienvenue.md).

**Wikilinks cassés ≠ erreur d'alias.** Un `[[Nom Note]]` peut pointer vers une note qui a changé de nom. Vérifier avant de supprimer le lien — souvent c'est un renommage à faire.

**`property:set` via CLI Obsidian échoue si la valeur contient `:`**. Limitation connue du parser YAML de la CLI (documentée dans forge-brain/SKILL.md). Pour `derniere-maj`, `fix.py` réécrit le frontmatter directement via Python — plus fiable.

**audit.py infère le vault depuis le chemin du script** (`scripts/ → vault-audit/ → skills/ → .claude/ → projet/ → vault/claude-forge`). Si la skill est dans un autre projet, passer `--vault-path` explicitement.

**En `/loop`, utiliser le mode audit seul (sans "fix")**. Le mode fix en boucle non supervisée peut produire des frontmatter partiellement corrects si la note a une structure inhabituelle. Réserver le fix aux sessions interactives.

**Le score 30 pts "frontmatter complet" est proportionnel** (30 - 5×nombre_champs_manquants). Une note avec 2 champs manquants obtient 20/30, pas 0. Cela évite les notes noyées inutilement en grade D.

**Templates non uniformes.** La section obligatoire varie par type (leader → "## Profil", technique → "## Description"). `audit.py` vérifie uniquement `## Liens` (présente dans tous les templates) pour éviter les faux positifs. Le script peut être enrichi si nécessaire.

## Exemples

```
# Audit rapide (top 10)
/vault-audit

# Audit complet en JSON (pour pipeline)
/vault-audit --full --output json

# Voir ce que fix ferait (sans écrire)
/vault-audit fix --dry-run

# Corriger une note spécifique
/vault-audit fix --note "Opus 4.7"

# Monitoring hebdomadaire
/loop 7d /vault-audit --top 5
```

## Apprentissage

Après chaque audit significatif :
- Si un pattern d'erreur revient sur > 10 notes → documenter dans `Knowledge/erreurs/`
- Si le score moyen monte suite aux corrections → noter dans mémoire projet
- Si le script manque un cas edge → ouvrir un fix dans `scripts/audit.py` et mettre à jour ce SKILL.md
- Sauvegarder les statistiques de qualité dans la mémoire projet pour tracking progression

```
# Format mémoire projet
project_vault_quality.md :
  - Date : YYYY-MM-DD
  - Notes : N total
  - Score moyen : XX/100
  - Grade A : X | B : X | C : X | D : X
  - Orphelines : N
  - Wikilinks cassés : N
```
