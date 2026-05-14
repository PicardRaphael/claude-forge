---
name: expand
description: Expand a rough user prompt into a precise specification with scope, deliverables, success criteria, and verification steps. Use when the user types /expand or when a prompt is ambiguous and needs clarification before execution.
argument-hint: "[rough prompt to expand]"
---

Tu prends un prompt brut et tu le transformes en spécification précise. Ne jamais exécuter le prompt original — seulement l'expander.

## Process

1. **Analyser** le prompt brut ($ARGUMENTS)
2. **Identifier** :
   - Livrable concret attendu
   - Définition de "terminé" (quand c'est fini ?)
   - Scope : ce qui est IN et ce qui est OUT
   - Questions critiques non-résolues (max 3)
   - Critères de vérification
3. **Présenter** la spec expansée dans ce format :

```
## Spec expansée

**Livrable :** [quoi exactement]
**Terminé quand :** [condition mesurable]
**Scope IN :** [ce qu'on fait]
**Scope OUT :** [ce qu'on ne fait PAS]
**Vérification :** [comment vérifier que c'est bon]
**Questions :** [si ambiguïté, 1-3 questions max — omettre si le prompt est clair]
```

4. **Attendre validation** avant d'exécuter quoi que ce soit

## Gotchas

- Ne PAS exécuter le prompt original — l'objectif est uniquement de produire la spec, pas d'agir
- Si le prompt est déjà précis (> 50 mots avec scope clair et condition de fin mesurable), dire "Prompt déjà précis, j'exécute directement" et passer à l'exécution
- Max 3 questions — pas un interrogatoire. Si une question est juste "nice to know", la supprimer
- Garder la spec < 10 lignes — la concision est une fonctionnalité, pas un compromis
- "Scope OUT" explicite = la moitié de la valeur. Forcer l'écriture même si évident
- Ne pas reformuler le prompt — transformer en spec actionnelle. "Crée X" → Livrable + Terminé quand + Scope

## Apprentissage

Après utilisation, noter si la spec produite a évité des allers-retours. Sauvegarder les patterns de prompts améliorés dans la mémoire projet.

## Vault

[[prompt-rewriter-pattern]] — analyse du pattern et alternatives
