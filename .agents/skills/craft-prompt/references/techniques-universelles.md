# Techniques Prompt — Universelles (tout LLM)

_Techniques valables pour Claude, Gemini, GPT, et tout modele de langage_

## Structure optimale d'un prompt

```
1. ROLE — Qui es-tu (1-2 phrases)
2. CONTEXTE — Ce que tu dois savoir (background)
3. TACHE — Ce que tu dois faire (objectif mesurable)
4. FORMAT — Comment structurer la reponse
5. EXEMPLES — 1-3 paires input/output
6. CONTRAINTES — Ce qu'il ne faut PAS faire
7. VERIFICATION — Comment valider ta reponse
```

## Techniques par categorie

### Clarifier l'objectif

| Technique | Description | Exemple |
|---|---|---|
| **Outcome Delegation** | Definir les criteres de succes, pas les etapes | "Le resultat doit contenir X, Y, Z" vs "Fais etape 1, 2, 3" |
| **Persona** | Assigner un role expert | "Tu es un avocat fiscaliste avec 20 ans d'experience" |
| **Audience** | Preciser pour qui | "Explique comme a un stagiaire" vs "Explique a un senior" |
| **Scope** | Borner explicitement | "Concentre-toi UNIQUEMENT sur X. Ignore Y." |

### Ameliorer le raisonnement

| Technique | Description | Exemple |
|---|---|---|
| **Chain-of-Thought** | Raisonner etape par etape | "Reflechis etape par etape avant de repondre" |
| **Tree-of-Thought** | Explorer plusieurs chemins | "Propose 3 approches. Evalue chacune. Choisis la meilleure." |
| **Graph of Thoughts** | Raisonnement en graphe avec fusion | Branches independantes → fusionner les conclusions |
| **Self-Verification** | Verifier sa propre reponse | "Avant de repondre, verifie que X et Y sont corrects" |
| **Reflexion** | Analyser les erreurs passees | "Examine ce qui a echoue et pourquoi avant de reessayer" |
| **Decomposition** | Decouper en sous-problemes | "Decompose ce probleme en 3 parties independantes" |

### Controler le format

| Technique | Description | Exemple |
|---|---|---|
| **Few-shot** | Exemples input/output | 2-5 exemples du format exact attendu |
| **Template** | Fournir un squelette | "Remplis ce template : Titre: ..., Resume: ..., Actions: ..." |
| **Negative Examples** | Montrer ce qu'il ne faut PAS faire | "NE PAS faire comme ceci : [mauvais exemple]" |
| **Format Mirroring** | Ecrire le prompt dans le format attendu | Si tu veux des bullets, ecris en bullets |

### Gerer le contexte

| Technique | Description | Quand |
|---|---|---|
| **Context Engineering** | Gerer tout ce qui entre dans la fenetre, pas juste le prompt | Toujours en production |
| **Progressive Disclosure** | Charger l'info en couches (metadata → body → references) | Architecture agentique |
| **Dynamic Tool Loading** | Charger uniquement les outils pertinents | Agents avec 20+ outils |
| **Context Compaction** | Resumer les traces pour liberer de l'espace | Agents long-horizon |
| **Separation of Concerns** | System prompt (stable) vs User prompt (variable) | APIs, chatbots |

### Prompt Patterns avances

| Pattern | Description | Quand |
|---|---|---|
| **Plan-Execute-Verify** | 1. Plan → 2. Execute → 3. Verifie | Operations critiques |
| **Draft-Critique-Refine** | 1. Draft → 2. Critique → 3. Ameliore | Redaction, code |
| **Parallel Fan-Out** | Lancer N sous-taches en parallele → fusionner | Research, analyse multi-source |
| **Guard Rails** | Contraintes negatives explicites | Securite, compliance |
| **Escalation** | "Si tu n'es pas sur, dis-le au lieu de deviner" | Decisions critiques |

## Anti-patterns (tout LLM)

| Anti-pattern | Pourquoi c'est mauvais | Fix |
|---|---|---|
| Prompt de 2000 mots | Dilue le signal dans le bruit | Couper a l'essentiel |
| "Sois exhaustif et detaille" | Encourage le remplissage | Donner un format precis |
| Contraintes uniquement negatives | Le modele ne sait pas quoi faire | Ajouter ce qu'il DOIT faire |
| Pas d'exemples | Le modele devine le format | Ajouter 1-3 exemples |
| Instructions contradictoires | Le modele oscille | Prioriser explicitement |
| "CRITICAL! MUST! ALWAYS!" | Overtrigger sur les modeles recents | Instructions normales suffisent |
| Copier la doc du framework | Gaspille du contexte | Le modele connait deja |
| Pas de critere de succes | Impossible de verifier | "Le resultat est bon si..." |

## Checklist avant livraison d'un prompt

- [ ] L'objectif est clair et mesurable
- [ ] Le role/persona est defini
- [ ] Au moins 1 exemple est fourni
- [ ] Le format de sortie est explicite
- [ ] Les contraintes negatives sont presentes
- [ ] Un moyen de verification est inclus
- [ ] Le prompt est testable (pas ambigu)
- [ ] Le prompt est concis (chaque phrase apporte du signal)
