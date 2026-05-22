---
titre: "Critique — Capitalisation blog Anthropic large codebases + tweet Thariq"
resume: "Devil's advocate sur 5 livrables vault (4 nouvelles notes + 1 enrichie) issus du blog Anthropic Large Codebases et tweet Thariq running-implementation-notes — KEEP/EVOLVE par note + 3 vérifications factuelles"
aliases:
  - "critique large codebases capitalisation"
  - "critique running implementation notes"
  - "critique subagent explore then edit"
  - "critique agent manager role"
  - "critique codebase maps"
  - "DA verdict 2026-05-20"
type: critique
derniere-maj: 2026-05-20
auteur: devils-advocate
tags:
  - "#type/critique"
  - "#domaine/claude-code"
sources:
  - "Session vault 2026-05-20"
  - "Blog Anthropic — How Claude Code works in large codebases (14 mai 2026)"
  - "Tweet Thariq — implementation-notes.html (18 mai 2026)"
---

## Contexte

Session 2026-05-20 — Raphael partage 5 sources externes (1 blog Anthropic accessible via defuddle + 4 tweets X dont 1 seul accessible). Je crée 4 notes + enrichis 1 dans le vault. Le devil's advocate critique avant déploiement sur ia_back + neo_ia.

## Verdict par livrable

### 1. `running-implementation-notes.md` → **KEEP**

Pattern distinct, valeur unique, source autorisée (Thariq, 758k vues). Déploie sans hésiter sur ia_back + neo_ia.

**Fix mineur** : retirer le wikilink `[[expand]]` qui pointe vers une skill, pas une note vault (orphelin).

### 2. `subagent-explore-then-edit.md` → **EVOLVE bloquant**

Le gotcha "`disallowedTools: Write, Edit` casse l'écriture du fichier final" est FACTUEL mais les fixes proposés sont les **mauvais** :
- Note propose : "autoriser uniquement Write" ou "main agent écrit"
- Fix éprouvé en production : **MCP `forge-brain:create_note`** (vu sur devils-advocate.md qui a `disallowedTools: Write, Edit` ET utilise MCP pour sauver ses critiques)

**Avant de s'appuyer sur cette note comme référence** :
1. Ajouter MCP comme **fix #1**
2. Wikilink vers [[erreur-da-heredoc-bash-silencieux]] (2026-05-11) qui documente précisément ce problème (2/4+ critiques DA perdues à cause de heredoc Bash)

### 3. `agent-manager-role.md` → **EVOLVE**

Section "Application à Neoteem" viole la frontière mémoire/vault (rule `memory-discipline.md` : contexte projet → `1-Projets/<nom>/`).

**Fix** : scinder
- Garder dans `01-Claude/Code/best-practices/` uniquement le contenu **généralisable** (3 niveaux, responsabilités, gouvernance)
- Déporter section "Application Neoteem" vers `1-Projets/Neoteem/agent-manager-neoteem.md`

### 4. `codebase-maps-pattern.md` → **EVOLVE**

Table "Application aux repos Neoteem" = **audit fantôme** (aucun CODEBASE-MAP.md n'existe sur les repos, aucun audit réel n'a été fait).

**Fix** :
- Soit retirer la table
- Soit la requalifier explicitement "Hypothèses à valider via audit"
- Soit scinder vers `1-Projets/` comme pour `agent-manager-role.md`

### 5. `hooks-guide.md` (enrichi) → **KEEP**

Claims factuels vérifiés. Ajout cohérent.

## Confirmation des 3 points factuels

### 1. `learning-reminder.py` existe-t-il vraiment ?

**OUI, vérifié.** Path : `C:/Users/raphael.picard_neote/Documents/claude-forge/.claude/hooks/learning-reminder.py`. Présent avec 3 autres hooks. Claim hooks-guide enrichi est **factuel**.

### 2. `running-implementation-notes` distinct de SDD ?

**OUI, distinction réelle**, pas MERGE :

| Pattern | Quand | Outil |
|---------|-------|-------|
| `pattern-spec-driven-development` | **Avant** le code | interview AskUserQuestion → SPEC.md → nouvelle session |
| `pattern-sdd-triangle` | **Après** le code | outil Plumb, pre-commit hook qui sync spec↔code↔tests |
| `running-implementation-notes` | **Pendant** le code | fichier vivant maintenu par Claude (seul des 3 sur cette phase) |

**Avertissement** : ajouter dans `pattern-spec-driven-development.md` une mention "Variante légère pendant l'implémentation : voir [[running-implementation-notes]]" pour navigabilité bidirectionnelle.

### 3. Gotcha disallowedTools Write/Edit factuel ?

**FACTUEL mais incomplet** (voir verdict #2 ci-dessus).

## Patterns de fragilité à mémoriser (compounding)

Trois anti-patterns récurrents observés sur cette session :

1. **Note technique générale + section "Application à Neoteem"** = viole frontière mémoire/vault. Contexte projet appartient à `1-Projets/<nom>/`.
2. **Table "Recommandations par repo" sans audit réel** = audit fantôme. À requalifier en hypothèses ou scinder.
3. **Note sur pattern enforcement sans citer `Knowledge/erreurs/`** = compounding raté. Toute note sur hooks/agents/skills DOIT chercher dans `Knowledge/erreurs/` avant rédaction.

## Statut sauvegarde

Critique sauvegardée par l'orchestrateur (session principale) car le DA agent ne peut pas écrire fichier final (disallowedTools Write/Edit + MCP forge-brain non exposé dans contexte agent — preuve vivante du gotcha critiqué).

## Liens

- [[running-implementation-notes]] — Note KEEP, fix mineur wikilink `[[expand]]`
- [[subagent-explore-then-edit]] — Note EVOLVE bloquant, fix MCP
- [[agent-manager-role]] — Note EVOLVE, scinder vers 1-Projets
- [[codebase-maps-pattern]] — Note EVOLVE, audit fantôme
- [[comment-creer-hook]] — Note KEEP
- [[erreur-da-heredoc-bash-silencieux]] — Erreur référencée
- [[pattern-spec-driven-development]]
- [[pattern-sdd-triangle]]
- [[devils-advocate-pipeline]] — Process suivi
