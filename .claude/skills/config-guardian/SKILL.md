---
name: config-guardian
description: Scan ia_back, neo_ia, and neoteem-brain for Claude Code config drift against baseline rules. Use when auditing multi-repo setup consistency.
user-invokable: true
allowed-tools: Read, Glob, Grep, Agent, Bash
model: sonnet
effort: high
---

# config-guardian — Audit de configuration multi-repo

Scanne ia_back, neo_ia et neoteem-brain pour détecter les écarts par rapport à la baseline Claude Code.
**Diagnostic uniquement** — aucune correction automatique.

## Repos cibles

| Alias | Chemin |
|-------|--------|
| ia_back | `C:/Users/raphael.picard_neote/Documents/neot-v2/ia_back` |
| neo_ia | `C:/Users/raphael.picard_neote/Documents/neot-v2/neo_ia` |
| neoteem-brain | `C:/Users/raphael.picard_neote/Documents/neot-v2/neoteem-brain` |

## Étapes d'exécution

### Étape 1 — Collecter les données

Lancer le script de collecte :

```bash
python3 .claude/skills/config-guardian/scripts/scan.py all
```

Le script retourne un JSON avec tous les faits bruts par repo :
permissions allow/deny, hooks wired vs disque, rules présentes, agents avec leur frontmatter, état CLAUDE.md, compteur agent-memory.

### Étape 2 — Exécuter les 5 checks

Analyser le JSON produit par le script selon la baseline définie dans `references/baseline-rules.md`.
Pour les checks nécessitant une lecture de contenu (ex: frontmatter multi-ligne des agents), utiliser Read directement.

Pour chaque résultat, assigner un statut :
- **OK** — conforme
- **WARN** — écart non bloquant (ex: format alternatif valide, fichier optionnel manquant)
- **CRITIQUE** — écart bloquant (ex: hook fantôme, deny git, agent sans memory)

### Étape 3 — Produire le rapport

Afficher le rapport directement (ne pas sauvegarder dans un fichier).

Format par repo :

```
## [repo] — [nb_ok]/[total] checks OK

| Check | Statut | Détail |
|-------|--------|--------|
| Permissions git | OK/WARN/CRITIQUE | ... |
| Hooks cohérence stack | OK/WARN/CRITIQUE | ... |
| Rules obligatoires | OK/WARN/CRITIQUE | ... |
| MCP tools agents | OK/WARN/CRITIQUE | ... |
| Mémoire compounding | OK/WARN/CRITIQUE | ... |
```

Terminer par un résumé global :

```
## Résumé global

### CRITIQUE (à corriger en priorité)
- [repo] : [problème] → [action recommandée]

### WARN (à surveiller)
- [repo] : [problème] → [action recommandée]

### Score global : X/15 checks OK
```

## Gotchas

- **Merge des permissions** : `deny` dans `~/.claude/settings.json` global écrase `allow` dans le settings projet. Toujours vérifier les deux niveaux + global et merger dans l'ordre : global deny > projet allow. Ne pas conclure "git autorisé" si le global a un deny.
- **Format permission Bash** : accepter `Bash(git *)`, `Bash(git commit *)` ET `Bash(git push *)` comme OK. `Bash(git:*)` (deux-points au lieu d'espace) = WARN format incorrect. Regex : `Bash\(git[ *]`.
- **Hooks orphelins vs fantômes** : orphelin = fichier présent dans hooks/ mais absent de settings.json. Fantôme = wired dans settings.json mais fichier absent sur disque. Les deux sont CRITIQUE.
- **Section Gotchas CLAUDE.md** : chercher titre `## Gotchas` ou `### Gotchas` (insensible à la casse). Ne pas exiger un format exact du contenu.
- **MCP tool names** : les noms `mcp__context7__*`, `mcp__postgres__query`, `mcp__claude_ai_Atlassian__*` sont les attendus de la baseline — ne pas les remettre en question. Vérifier leur présence dans le frontmatter `tools:` de chaque agent.
- **agents sans tools:** : certains agents n'ont pas de clé `tools:` dans leur frontmatter — c'est CRITIQUE (pas juste WARN) car le MCP ne sera pas injecté.
- **neoteem-brain agents/** : si le dossier agents/ est absent ou vide, reporter comme WARN (pas de baseline agents pour ce repo à ce jour) sauf pour vault-enricher qui doit exister.
- **Lecture parallèle** : lancer toutes les lectures d'un même repo en parallèle. 3 repos × ~8 lectures = utiliser Agent ou batch de Read/Glob.

## Apprentissage — Sauvegarder en mémoire projet

Après chaque audit, sauvegarder :
- **Écarts détectés** par repo (pour suivre la progression entre sessions)
- **Patterns récurrents** — si un même type d'erreur revient sur 2+ repos
- **Configs validées** — noter quand un repo passe TOUT en OK (milestone)

## Références

- `references/baseline-rules.md` — détail complet des 5 checks par repo
