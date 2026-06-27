# Axes d'analyse — skill-evolve

Criteres detailles pour les 4 axes d'evaluation d'une SKILL.md.

---

## Axe 1 — Efficacite

Objectif : la skill fait-elle ce qu'elle est censee faire, et le fait-elle bien ?

### Description et declenchement

| Signal positif | Signal negatif |
|----------------|----------------|
| Triggers naturels presents ("use when", "use for", phrases utilisateur) | Description vague — "helps with X" sans triggers specifiques |
| Une seule ligne, en anglais, < 1024 chars | Description multi-ligne ou en francais |
| Troisieme personne ("Analyzes...", "Processes...") | Premiere personne ("I can...") ou deuxieme ("You can...") |
| Triggers negatifs presents si overlap possible | Pas de disambiguation avec skills similaires |

### Workflow

| Signal positif | Signal negatif |
|----------------|----------------|
| Etapes sequentielles claires avec dependances | Etapes non ordonnees ou implicites |
| Conditions d'arret definies (si X absent, bail) | Le workflow continue sans validation des inputs |
| Output format specifie | "Afficher les resultats" sans format |
| Section Gotchas presente | Pas de Gotchas, ou Gotchas evidents |

### Gotchas

Un bon Gotcha :
- Nomme une erreur SPECIFIQUE que Claude fait sur ce sujet
- Donne la solution concrete (pas juste "faire attention")
- N'enonce pas l'evident (ex: "ne pas effacer les fichiers" n'est pas un Gotcha utile)

Exemples de bons Gotchas :
- "Pas de $ARGUMENTS dans backticks shell — extraire dans une variable"
- "Ne pas confondre avec /evolve — rediriger si l'utilisateur veut analyser un projet"
- "Obsidian CLI peut echouer si Obsidian est ferme — toujours faire le pre-check"

---

## Axe 2 — Evolution

Objectif : la skill tire-t-elle parti des techniques et patterns les plus recents ?

### Techniques vault

Chercher dans `04-Techniques/` du vault :
- Pattern "scripts > instructions" : les validations critiques sont-elles dans des scripts Python/Bash plutot que dans des instructions en langage naturel ?
- Pattern "progressive disclosure" : le SKILL.md renvoie-t-il vers references/ pour les details ?
- Pattern "checklist" : les workflows complexes utilisent-ils des checklists que Claude coche ?
- Pattern "plan-validate-execute" : y a-t-il une phase de validation avant execution ?

### Configuration

| Check | Signal d'obsolescence |
|-------|----------------------|
| `model:` | sonnet avec `effort: medium` — devrait etre `high` |
| `effort:` | `max` — supprime depuis v2.1.91, utiliser `high` ou `xhigh` |
| `allowed-tools:` | Agent dans une skill qui devrait rester legere |
| `disable-model-invocation:` | Absent sur une skill slash-command pure |

### Integration memoire

La skill a-t-elle une section Apprentissage ?
La section Apprentissage est-elle vide depuis plusieurs sessions alors que la skill est active ?

---

## Axe 3 — Cross-pollination

Objectif : beneficier des patterns qui ont fonctionne dans d'autres skills.

### Patterns a checker

Pour chaque pattern, verifier s'il est pertinent pour la skill analysee et present/absent :

| Pattern | Skill de reference | Applicable si... |
|---------|--------------------|-----------------|
| Fallback vault (CLI -> Glob) | forge-brain, vault-audit | skill utilise le vault |
| Validation $ARGUMENTS avec bail | evolve, skill-evolve | skill prend des arguments |
| Sections "Ce qui est bien" / "Ce qui a ete ecarte" | evolve, skill-evolve | skill produit des recommandations |
| git log pour contexte historique | skill-evolve | skill analyse des composants forge |
| scripts Python pour operations deterministes | vault-audit | skill fait des validations critiques |
| Format tableau pour sweep multi-items | skill-evolve | skill analyse plusieurs elements |
| Pre-check avant chaque outil externe | forge-brain (MCP) | skill utilise un outil externe |

### Comment identifier d'autres patterns

1. Identifier le type de workflow de la skill cible
2. Chercher des skills avec un workflow similaire dans `.claude/skills/`
3. Lire leur SKILL.md pour identifier les patterns utiles
4. Evaluer si ces patterns s'appliquent sans changer l'objectif de la skill

---

## Axe 4 — Simplification

Objectif : la skill est-elle aussi courte que possible sans perdre de valeur ?

### Signaux de sur-specification

| Anti-pattern | Solution |
|--------------|----------|
| Instructions qui enoncent l'evident | Supprimer. "Ne pas effacer les fichiers" n'est pas utile. |
| Etape qui repete une autre etape | Fusionner ou supprimer la redondance |
| Exemple qui illustre ce que le titre dit deja | Supprimer l'exemple si le titre est suffisant |
| Section "Configuration requise" pour des outils standard | Supprimer si les outils sont en allowed-tools |
| Gotchas trop generiques | Remplacer par des Gotchas specifiques ou supprimer |

### Signaux de sur-longueur

- SKILL.md > 500 lignes : identifier les sections candidates pour references/
  - Criteres d'evaluation detailles -> references/
  - Grilles de scoring -> references/
  - Exemples exhaustifs -> references/
  - Historique / changelog -> supprimer

### Questions de simplification

- Si je supprime cette section, est-ce que Claude ferait une erreur ? Non -> supprimer.
- Est-ce que cette instruction existe parce que Claude l'oublie vraiment ? Non -> supprimer.
- Est-ce que cette etape est dans le workflow parce que c'est important ou parce que "au cas ou" ? Si "au cas ou" -> supprimer.
