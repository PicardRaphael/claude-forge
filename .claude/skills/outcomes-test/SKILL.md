---
name: outcomes-test
description: Evaluate a deliverable against a RUBRIC.md using a separate grader agent. Complements devil's advocate with objective, measurable criteria checking. Use when verifying skills, agents, hooks, or specs against defined success criteria.
argument-hint: "<path-to-deliverable> [path-to-rubric]"
allowed-tools: Agent, Read, Glob, Grep
user-invokable: true
---

# Outcomes Test

Évalue un livrable contre un rubric markdown via un subagent grader dédié (contexte séparé, pas de biais auto-évaluation). Complémentaire au devil's advocate : DA critique l'inattendu, Outcomes vérifie les critères objectifs mesurables.

## Rôle

Produire un rapport d'évaluation structuré (PASS/FAIL/PARTIAL par critère, score global, corrections suggérées) sans modifier aucun fichier du livrable.

## Flow

### Étape 1 — Parser les arguments

`$ARGUMENTS` peut contenir :
- Un chemin vers un fichier ou dossier : `/path/to/deliverable`
- Deux chemins séparés par espace : `/path/to/deliverable /path/to/RUBRIC.md`

Extraire le chemin livrable et (optionnel) le chemin rubric.

### Étape 2 — Trouver le rubric

Si un chemin rubric est fourni → l'utiliser directement.

Sinon, chercher `RUBRIC.md` dans cet ordre :
1. Même dossier que le livrable
2. Dossier parent immédiat
3. Racine du projet (`.claude/`)

Si aucun RUBRIC.md trouvé → **ne pas bloquer, ne pas écrire**. Afficher en stdout un rubric proposé adapté au type de livrable (détecter depuis l'extension et le contenu) en utilisant les templates de `references/rubric-templates.md`. Message :

```
Aucun RUBRIC.md trouvé. Voici un rubric suggéré pour ce type de livrable.
Copiez-le dans RUBRIC.md dans le dossier du livrable, puis relancez /outcomes-test.

---
[rubric proposé]
---
```

### Étape 3 — Préparer le contexte pour le grader

Lire le contenu du livrable. Si le livrable est un dossier, lire récursivement les fichiers `.md` et fichiers de code (paginer si > 500 lignes par fichier).

Lire le contenu du RUBRIC.md.

### Étape 4 — Lancer l'agent grader

Invoquer `outcomes-grader` avec UNIQUEMENT :
- Le contenu complet du rubric
- Le contenu complet du livrable
- Le chemin du livrable (pour contexte dans le rapport)

Ne pas passer le contexte de la session en cours, d'autres fichiers, ou des opinions. Le grader reçoit un contexte propre.

Prompt au grader :
```
Évalue le livrable suivant contre le rubric fourni.

## Rubric
[contenu RUBRIC.md]

## Livrable : [chemin]
[contenu livrable]
```

### Étape 5 — Afficher le rapport

Le rapport retourné par le grader suit ce format. L'afficher tel quel en stdout :

```markdown
# Outcomes Test — [nom livrable]

## Score global : [PASS|FAIL] ([score]%)

### Critères MUST
| Critère | Statut | Justification |
|---------|--------|---------------|
| [critère] | PASS | [preuve] |
| [critère] | FAIL | [ce qui manque] |
| [critère] | PARTIAL | [présent vs absent] |

### Critères SHOULD ([x]/[total])
| Critère | Statut | Justification |
|---------|--------|---------------|

### Critères NICE ([x]/[total])
| Critère | Statut | Justification |
|---------|--------|---------------|

## Corrections suggérées
[uniquement si score < 80% ou MUST échoué]
- [critère FAIL] : [action corrective précise]
```

## Calcul du score

- **Gate MUST** : 1 seul FAIL → résultat global FAIL, score non calculé
- **Si tous les MUSTs sont PASS ou PARTIAL** :
  - `score = (SHOULD_ok / SHOULD_total × 65) + (NICE_ok / NICE_total × 35)`
  - PARTIAL compte pour 0.5
  - Seuil de succès : **80%**
- Résultat global : PASS si score ≥ 80% ET aucun MUST FAIL

## Gotchas

- **Le grader DOIT être un subagent** — contexte séparé obligatoire pour éviter le biais d'auto-évaluation. Ne jamais évaluer inline dans cette skill.
- **La skill NE modifie RIEN** — évalue uniquement. Les corrections suggérées sont affichées, jamais appliquées.
- **Rubric vague = évaluation bruitée** — si un critère n'est pas testable objectivement ("code propre"), signaler que le rubric doit être révisé.
- **Complémentaire au DA, pas un remplaçant** — DA pour critique adversariale de l'inattendu, Outcomes pour vérification des critères prédéfinis.
- **Paginer les gros livrables** — si > 500 lignes, lire par chunks avec offset/limit. Ne jamais s'arrêter au milieu.
- **Ne pas déduire le rubric depuis le type de fichier seul** — lire le contenu pour confirmer le type (un `.md` peut être un agent, une spec, une note vault, etc.).

## Exemples d'usage

```
/outcomes-test .claude/skills/outcomes-test
/outcomes-test .claude/agents/outcomes-grader.md
/outcomes-test .claude/skills/my-skill RUBRIC.md
/outcomes-test src/feature.py
```

## Références

- `references/rubric-templates.md` — 4 templates RUBRIC par type (skill, agent, hook, CLAUDE.md)

## Apprentissage

Après utilisation en session :
- Si un rubric s'avère trop vague (trop de PARTIAL non actionnable) → noter le pattern dans la mémoire projet
- Si le grader rate des critères évidents → noter le contexte pour affiner le prompt grader
- Si un nouveau type de livrable revient souvent → ajouter un template dans `references/rubric-templates.md`
