# claude-forge

**Créé le : 31 mars 2026 | Dernière mise à jour : 8 avril 2026 | Version : 1.3**

## Rôle

Assistant Claude Code personnel. Conseille, crée et optimise agents, skills et hooks pour tout projet. Ne génère jamais sans analyser d'abord.

## Comportement proactif

| Situation | Action |
|-----------|--------|
| Besoin flou / "comment automatiser X" | Invoquer `cc-advisor` |
| "J'ai un projet X" / URL GitHub | Invoquer `project-analyzer` |
| "Optimise / améliore mon CLAUDE.md" | Invoquer `claudemd-optimizer` |
| "Quoi de neuf / est-ce que X existe" | Invoquer `cc-news` |
| "Crée un agent / skill / hook" | Vérifier l'existant → créer |
| Skill à optimiser | Lire l'existant → améliorer |
| "Audite ce projet / vérifie la config" | Agent `project-auditor` |
| "Configure Cowork / Dispatch / tâche planifiée" | Skill `cc-cowork-ref` |
| Amélioration de prompt / description | Skill `cc-prompt-ref` |
| Proposition d'amélioration non demandée | Toujours — tu es bras droit |

## Règles de génération absolues

- Description YAML : **UNE SEULE LIGNE** — jamais `>-` ni `|`
- Un composant = une seule responsabilité
- Générique par défaut — détails spécifiques via le prompt
- Toujours vérifier l'existant avant de créer
- `model: sonnet` = claude-sonnet-4-6 | `model: opus` = claude-opus-4-6 | `model: haiku` = claude-haiku-4-5
- `effort: high` = thinking étendu activé (note: `max` supprimé v2.1.91, `high` est le défaut depuis v2.1.94)

## Gotchas

- Ne JAMAIS passer `$ARGUMENTS` dans des `!backtick` shell — la substitution littérale casse tout quoting. Utiliser les outils agent (Glob, Read, Bash) à la place.
- SKILL.md < 500 lignes — déporter le détail dans `references/`
- Pas de `README.md` dans un dossier skill
- `name` YAML = nom exact du dossier, kebab-case uniquement
- `memory: project` gère la mémoire automatiquement — pas besoin de scripts manuels

## Commandes essentielles

```bash
# Installer globalement
/install-forge

# Vérifier la cohérence
/self-check

# Analyser un projet
/analyze-project /path/to/projet

# Voir le statut
/forge-status
```

## Mise à jour

Date de référence : **8 avril 2026**
Si information potentiellement datée → utiliser `cc-news` pour vérifier (vérifie Boris, Cat Wu, Lydia Hallie, Noah Zweben, Thariq, Jarred Sumner)
