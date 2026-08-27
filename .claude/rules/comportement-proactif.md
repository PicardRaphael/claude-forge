---
description: "Dispatch table: which agent or skill to invoke based on user situation"
---

# Comportement proactif — Dispatch

| Situation | Action |
|-----------|--------|
| Besoin flou / "comment automatiser X" | Invoquer `cc-advisor` |
| "Je veux créer/construire qqch pour résoudre un problème" (besoin → quelle brique ?) | Consulter la grille `[[methode-monter-systeme-workflow]]` (arbre besoin → Skill/Workflow/Agent/Framework/Hook/MCP + 4 patterns de robustesse + 3 archétypes) AVANT de choisir/proposer la brique |
| "J'ai un projet X" / URL GitHub | Invoquer `repo-inspector` (mode=analyze) |
| "Analyse les skills/agents/rules de X" / "audite mon repo" / audit config (simple) | Agent `repo-inspector` (mode=audit, PAS Explore) — scope `.claude/` UNIQUEMENT, inclut audit qualité-design transverse (skills à diviser/fusionner/kill, hooks redondants, cohérence canoniques forge 22 mai) |
| "audit à fond / complet / approfondi" · "sous tous les angles / 3 lentilles / tripartite" · "mon setup .claude est-il bon" · "optimise / nettoie ma config" | Agent `repo-inspector` (mode=audit, lentilles tripartites intégrées : Discipline Boris / Minimalisme Will / Couverture ECC). Anciens agents boris-auditor/ecc-auditor/will-auditor absorbés dans repo-inspector. |
| "Analyse mon repo X et propose config CC" / "propose-moi le meilleur setup" | **Méthode 6 étapes [[methode-analyser-repo]]** — scan archi + code réel en parallèle de l'audit `.claude/` (détail : Anti-patterns en bas de page) |
| "Analyse ia_back" / "analyse neo_ia" / multi-repo | Agent `repo-inspector` (mode=audit) par repo, en parallele |
| "Optimise / améliore mon CLAUDE.md" | Invoquer `claudemd-creator` |
| "Quoi de neuf / est-ce que X existe" | Invoquer `cc-news` ; demande manuelle = correction bornée des assertions actives existantes, créations proposées en batch |
| "Crée un agent / skill / hook" | Vérifier l'existant → créer |
| Skill à optimiser | Lire l'existant → améliorer |
| "Audite le vault / vérifie les notes" | Skill `/vault-audit` |
| "Configure Cowork / Dispatch / tâche planifiée" | Skill `cc-cowork-ref` |
| Amélioration de prompt / description | Skill `cc-prompt-ref` |
| "Crée un prompt pour X" | Skill `craft-prompt` (Claude, Gemini, tout LLM) |
| Début de session / reprise | `/recap` pour snapshot contexte |
| Fin de session / capitalisation / "mémorise ce que tu apprends sur moi" | `/done` — profil explicite, mémoire, décisions et contexte ; hypothèses proposées |
| Livrable majeur prêt (skill, agent, archi) | Agent `devils-advocate` AVANT de livrer |
| ↳ Plan de modifs structurelles issu d'un audit (KILL hook/skill, retrait outil sécu, refonte enforcement, suppression composant) | `devils-advocate` sur le PLAN AVANT application. Cosmétique/désync/typo → NON. « Déjà validé » / « carte blanche » ≠ dispense |
| Problème complexe résolu (multi-étapes) | `/reasoning-cache` pour sauvegarder le raisonnement |
| "Optimise cette skill" / maintenance skills | `/skill-evolve [nom]` ou `/skill-evolve all` |
| Review stratégique / remise en question | `/forge-review` (mensuel via /schedule) |
| "Évolutions / prochaines features d'un projet" | Skill `/evolve [path]` |
| "Conçois une routine / loop récurrent à spécifier" | Skill `loop-forge` |

## Séquence canonique AVANT tout dispatch créateur/analyste — OBLIGATOIRE

Avant d'invoquer `subagent-creator`, `skill-creator`, `hook-creator`, `claudemd-creator`, `repo-inspector`, `cc-advisor`, `evolve`, `skill-evolve` — la session principale DOIT briefer le sub-agent avec la séquence canonique :

```
1. ANALYSER le RÉEL du repo (faits bruts, code, .claude/ existant)
2. LIRE canoniques EN ENTIER via MCP forge-brain (read_note SANS max_lines)
3. CROISER analyse ⨯ canoniques → écarts mesurables
4. PLAN basé sur écarts (pas sur idéologie)
5. EXÉCUTER après validation
```

Source canonique : [[methode-analyser-repo]] + `.claude/rules/sequence-canonique-modification.md`.

**Brief minimum à inclure dans tout prompt sub-agent créateur** :
> "Suivre la séquence A→B→C→D→E de `.claude/rules/sequence-canonique-modification.md`. Lire les canoniques vault EN ENTIER via MCP forge-brain (`read_note` sans `max_lines`) AVANT toute prescription. Analyser le repo réel d'abord."

## Registre des opérations coûteuses — avant un fan-out d'agents connexes

Avant de dispatcher plusieurs agents sur des sous-tâches connexes, tenir un registre léger des opérations **coûteuses** déjà faites (`search_brain`/web, lecture de gros fichier, audit, requête DB) sous la forme `op + cible → artefact où est le résultat`, et l'**injecter dans le brief de chaque agent** pour qu'aucun ne refasse ce que la session principale (ou un agent précédent) a déjà fait. Une ligne par opération, jamais le contenu — un pointeur. À consulter/transmettre uniquement avant des opérations coûteuses (la coordination ne doit pas coûter plus qu'elle n'économise). Hypothèse en validation : [[relais-inter-agents-fiable]] + `memory/feedback_registre-relais-agents.md`.

## Posture Jarvis — innovation proactive

Ne pas attendre qu'on demande. À chaque occasion, PROPOSER :
- **Après une recherche (cc-news, vault, web)** → croiser avec l'existant, proposer des combinaisons inédites
- **Pendant /recap** → si un pattern émerge, le signaler avec une proposition
- **Après un apprentissage** → "ce qu'on vient d'apprendre pourrait aussi s'appliquer à..."
- **Après une erreur** → pas juste documenter, proposer comment transformer l'erreur en avantage
- **Quand une technique est mentionnée** → chercher si X+Y ensemble donnerait Z

Remettre en question Raphael si une meilleure approche existe. Remettre en question ses propres conclusions.

## Anti-patterns de dispatch

- **JAMAIS `Explore` pour auditer un projet** — Explore = recherche rapide read-only, PAS un audit
- **JAMAIS `general-purpose` pour > 8 operations** — decouper en agents paralleles
- **JAMAIS Grep/Read brut sur le vault** → voir `.claude/rules/forge-brain-proactive.md` (source canonique de la règle)
- **JAMAIS un seul agent pour multi-repo** — 1 agent par repo, en parallele
- **JAMAIS s'arrêter à l'audit `.claude/` quand l'user demande "analyse mon repo / propose-moi config CC"** — c'est la méthode 6 étapes [[methode-analyser-repo]] : scan archi (étape 1) + scan code pour patterns récurrents (étape 5) sont OBLIGATOIRES en parallèle de l'audit `.claude/`. Sinon propositions théoriques déconnectées du repo réel.
