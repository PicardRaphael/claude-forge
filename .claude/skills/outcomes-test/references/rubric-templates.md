# Rubric Templates — par type de livrable

Utilisé par la skill `/outcomes-test` quand aucun RUBRIC.md n'est trouvé.
Copier le template correspondant dans un fichier `RUBRIC.md` dans le dossier du livrable.

---

## Template 1 — Skill Claude Code

```markdown
# Rubric — Skill Claude Code : [Nom]

## Critères obligatoires (MUST)
- [ ] Description une seule ligne en anglais (jamais `>-` ni `|`)
- [ ] `name` frontmatter = nom exact du dossier, kebab-case
- [ ] SKILL.md < 500 lignes
- [ ] Pas de `$ARGUMENTS` dans des backtick shell
- [ ] Pas de README.md dans le dossier

## Critères souhaitables (SHOULD)
- [ ] Section Gotchas présente avec au moins 3 entrées
- [ ] Si > 300 lignes : contenu détaillé déporté dans references/
- [ ] `allowed-tools` déclarés dans le frontmatter
- [ ] Section Apprentissage présente (skills métier)
- [ ] Skills référencées dans `skills:` frontmatter si skill métier

## Critères bonus (NICE)
- [ ] Exemples d'usage concrets dans le body
- [ ] Gestion d'erreur explicite documentée
- [ ] `argument-hint` renseigné si la skill prend des arguments
```

---

## Template 2 — Agent Claude Code

```markdown
# Rubric — Agent Claude Code : [Nom]

## Critères obligatoires (MUST)
- [ ] `permissionMode` défini (plan, acceptEdits, ou bypassPermissions)
- [ ] Mémoire persistante absente ou explicitement justifiée
- [ ] Description = trigger en anglais, une seule ligne
- [ ] Modèle cohérent : opus pour jugement/analyse, sonnet pour exécution

## Critères souhaitables (SHOULD)
- [ ] `effort` correct : `high` par défaut des deux côtés ; `medium`/`low` si la tâche est mécanique ; `xhigh` seulement si un gain a été mesuré sur ce type de tâche
- [ ] Skills pertinentes listées dans `skills:` frontmatter ET référencées dans le body
- [ ] `disallowedTools` inclut Write/Edit si agent read-only
- [ ] Body explique clairement le rôle et les étapes

## Critères bonus (NICE)
- [ ] `maxTurns` configuré si agent à durée bornée
- [ ] Isolation worktree mentionnée si parallélisme prévu
- [ ] Exemples d'invocation dans le body
```

---

## Template 3 — Hook Claude Code

```markdown
# Rubric — Hook Claude Code : [Nom]

## Critères obligatoires (MUST)
- [ ] `event` valide (PreToolUse, PostToolUse, Stop, SubagentStop, NotificationHook)
- [ ] `matcher` cohérent avec l'event (tool name ou regex valide)
- [ ] Pas de chemin hardcodé user-specific (pas de `/home/username/` ou `C:\Users\nom\`)

## Critères souhaitables (SHOULD)
- [ ] `description` claire expliquant le comportement et le déclencheur
- [ ] `once: true` si le hook ne doit s'exécuter qu'une fois par session
- [ ] `async: true` si le hook est non-bloquant (vérification qualité, notification)

## Critères bonus (NICE)
- [ ] Tests manuels documentés (comment vérifier que le hook fonctionne)
- [ ] Comportement en cas d'erreur documenté (exit code 0/1/2)
- [ ] `timeout` configuré si le hook peut être lent
```

---

## Template 4 — Code Implementation (générique)

```markdown
# Rubric — Implementation : [Feature]

## Critères obligatoires (MUST)
- [ ] Types complets (pas de any/untyped)
- [ ] Linter clean (0 errors)
- [ ] Tests unitaires existent et passent
- [ ] Pas de credentials/secrets hardcodés
- [ ] Pas de DDL si base gérée séparément

## Critères souhaitables (SHOULD)
- [ ] Tests d'intégration pour les endpoints
- [ ] Error handling explicite (pas de catch générique)
- [ ] CHANGELOG mis à jour

## Critères bonus (NICE)
- [ ] Coverage > 80% sur fichiers modifiés
- [ ] Implementation notes à jour
```

---

## Template 5 — CLAUDE.md

```markdown
# Rubric — CLAUDE.md : [Projet]

## Critères obligatoires (MUST)
- [ ] < 200 lignes (sweet spot 150-300 mots selon UCL 2601.00880)
- [ ] Section Gotchas présente avec les erreurs comportementales clés
- [ ] Pas de duplication avec .claude/rules/ (routing dans rules/, pas CLAUDE.md)

## Critères souhaitables (SHOULD)
- [ ] Commandes build/test/lint documentées
- [ ] Conventions de code mentionnées
- [ ] Structure du repo décrite (si non évidente)

## Critères bonus (NICE)
- [ ] Section mémoire ou workflow de session documenté
- [ ] Priorité des sources d'information définie
- [ ] Liens vers rules/ critiques référencés
```
