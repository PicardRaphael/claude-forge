---
titre: "Outcome-First Prompting"
resume: "Technique OpenAI GPT-5.5 (avril 2026), reconduite et chiffrée par le guide GPT-5.6 (juil. 2026) : définir le résultat attendu, critères de succès et contraintes dures, sans prescrire le processus étape par étape"
aliases:
  - "outcome first prompting"
  - "outcome-first"
  - "prompting par résultat"
  - "result-first prompting"
  - "prompting GPT-5.5"
  - "specification par outcome"
domaine: technique
type: technique
derniere-maj: 2026-07-16
auteur: claude
sources:
  - "https://developers.openai.com/api/docs/guides/prompt-guidance"
tags:
  - "#type/technique"
  - "#domaine/prompt-engineering"
---

## Description

Technique recommandée par OpenAI dans le GPT-5.5 Prompting Guide (avril 2026). Au lieu de prescrire un processus étape par étape, on définit ce que le modèle doit atteindre, en laissant le modèle choisir le chemin.

> "Legacy prompts often over-specify the process because earlier models needed more help staying on track. With GPT-5.5, that can add noise, narrow the model's search space, or lead to overly mechanical answers."
> — [OpenAI GPT-5.5 Prompting Guide](https://developers.openai.com/api/docs/guides/prompt-guidance) (verbatim canonique — version forge précédente "The prompt patterns you spent months perfecting for GPT-5.2..." était fabriquée, corrigée 2026-05-23)

Renverse l'approche dominante 2023-2025 (chain-of-thought, step-by-step instructions).

## Structure d'un prompt Outcome-First

### Structure officielle OpenAI (7 headers)

Le doc OpenAI propose une structure de 7 headers :
1. `Role`
2. `# Personality`
3. `# Goal`
4. `# Success criteria`
5. `# Constraints`
6. `# Output`
7. `# Stop rules`

### Synthèse forge (5 éléments)

Synthèse pratique pour usage courant (paraphrase forge, pas verbatim OpenAI) :

1. **Outcome / état final** — Quel résultat exact est attendu ?
2. **Critères de succès** — Comment évaluer que c'est réussi ?
3. **Contraintes dures uniquement** — Ce qui ne peut PAS être fait (limites absolues)
4. **Contexte et outils disponibles** — Ce que le modèle peut utiliser
5. **Condition d'arrêt** — Quand s'arrêter, même si ce n'est pas parfait

## Quand utiliser

- Modèles frontier 2026+ (GPT-5.x, Claude Opus 4.7, Gemini 2.5 Pro)
- Tâches complexes où le processus optimal n'est pas connu à l'avance
- Agents autonomes avec multiple steps
- Remplace : step-by-step instructions, chain-of-thought explicite, least-to-most prompting

## Ce qu'on ne fait plus (deprecated)

- "Let's think step by step" — le modèle raisonne déjà internement
- Prescrire le chemin étape par étape — "hyper-littéralisme" sur les modèles frontier
- Process-first instructions — activement dégradant sur GPT-5.5

## Exemple

**Avant (process-first, déprécié) :**
```
1. Analyse le code
2. Identifie les bugs
3. Propose des corrections
4. Explique chaque correction
```

**Après (outcome-first) :**
```
Outcome: Un rapport des bugs critiques avec corrections prêtes à merger.
Succès: Chaque bug a une correction testée et une explication d'une ligne.
Contraintes: Ne modifier que les fichiers src/, pas les tests.
Arrêt: Après 5 bugs ou 30 minutes de recherche.
```

## Liens

- [[Context Engineering]] — Paradigme de structuration du contexte
- [[deprecated-techniques-2026]] — Techniques désormais contre-productives
- [[over-specification-paradox]] — Seuil S*=0.509 au-delà duquel spécifier nuit
- [[forge-prompt-machine]] — 12 principes FORGE, checklist prompts
- [[MOC-Techniques]]

## AJOUT 2026-07-16 — Challengée + confirmée (GPT-5.6 + Mollick/Wharton)

Doctrine challengée et **confirmée** le 16 juillet 2026 (verdict doctrine-impact-check : DOCTRINE_REINFORCE, run cc-news) par deux sources convergentes :

- **Guide officiel GPT-5.6** (9 juil. 2026, developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6) : la technique s'étend telle quelle à GPT-5.6. Chiffres neufs des évals internes coding-agent OpenAI : system prompts plus légers = **+10-15 % de score, -41-66 % de tokens, -33-67 % de coût**. Guidances additionnelles : éviter ALWAYS/NEVER/MUST sauf vrais invariants ; migration = **baseline fraîche** (porter le stack de prompts GPT-5/5.5 peut activement nuire) ; nouveau paramètre `text.verbosity` ; « Pro Mode » pour compute ponctuel à fort enjeu. Cf [[GPT-5.6]].
- **Ethan Mollick** (7 juil. 2026, X, backing Wharton Prompting Science Reports 1-4) : « les prompt tricks perdent leur intérêt » — spécifier objectifs/outputs/critères de qualité/tests, traiter l'IA comme un collaborateur managé. Convergence indépendante côté recherche académique. Cf [[Ethan Mollick]].
