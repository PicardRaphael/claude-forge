---
description: "Dispatch table: which agent or skill to invoke based on user situation"
---

# Comportement proactif — Dispatch

| Situation | Action |
|-----------|--------|
| Besoin flou / "comment automatiser X" | Invoquer `cc-advisor` |
| "J'ai un projet X" / URL GitHub | Invoquer `repo-inspector` (mode=analyze) |
| "Analyse les skills/agents/rules de X" / audit config | Agent `repo-inspector` (mode=audit, PAS Explore) — scope `.claude/` UNIQUEMENT, inclut audit qualité-design transverse (skills à diviser/fusionner/kill, hooks redondants, cohérence canoniques forge 22 mai) |
| "Analyse mon repo X et propose config CC" / "propose-moi le meilleur setup" | **Méthode 6 étapes [[methode-analyser-repo]]** — scan archi + code RÉEL + patterns récurrents + audit `.claude/` en parallèle. JAMAIS s'arrêter à `.claude/` |
| "Analyse ia_back" / "analyse neo_ia" / multi-repo | Agent `repo-inspector` (mode=audit) par repo, en parallele |
| "Optimise / améliore mon CLAUDE.md" | Invoquer `claudemd-optimizer` |
| "Quoi de neuf / est-ce que X existe" | Invoquer `cc-news` |
| "Crée un agent / skill / hook" | Vérifier l'existant → créer |
| Skill à optimiser | Lire l'existant → améliorer |
| "Audite le vault / vérifie les notes" | Skill `/vault-audit` ou agent `vault-maintainer` |
| "Configure Cowork / Dispatch / tâche planifiée" | Skill `cc-cowork-ref` |
| Amélioration de prompt / description | Skill `cc-prompt-ref` |
| "Crée un prompt pour X" | Skill `craft-prompt` (Claude, Gemini, tout LLM) |
| Début de session / reprise | `/recap` pour snapshot contexte |
| Fin de session / capitalisation | `/done` pour metacognition — decisions, faits, preferences, erreurs |
| Livrable majeur prêt (skill, agent, archi) | Agent `devils-advocate` AVANT de livrer |
| Problème complexe résolu (multi-étapes) | `/reasoning-cache` pour sauvegarder le raisonnement |
| "Optimise cette skill" / maintenance skills | `/skill-evolve [nom]` ou `/skill-evolve all` |
| Review stratégique / remise en question | `/forge-review` (mensuel via /schedule) |

## Séquence canonique AVANT tout dispatch créateur/analyste — OBLIGATOIRE

Avant d'invoquer `agent-creator`, `skill-creator`, `hook-creator`, `claudemd-optimizer`, `repo-inspector`, `cc-advisor`, `evolve`, `skill-evolve`, `spec` — la session principale DOIT briefer le sub-agent avec la séquence canonique :

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
- **JAMAIS Grep/Read brut sur le vault** — utiliser CLI Obsidian (`obsidian search`, `obsidian read`)
- **JAMAIS un seul agent pour multi-repo** — 1 agent par repo, en parallele
- **JAMAIS s'arrêter à l'audit `.claude/` quand l'user demande "analyse mon repo / propose-moi config CC"** — c'est la méthode 6 étapes [[methode-analyser-repo]] : scan archi (étape 1) + scan code pour patterns récurrents (étape 5) sont OBLIGATOIRES en parallèle de l'audit `.claude/`. Sinon propositions théoriques déconnectées du repo réel.
