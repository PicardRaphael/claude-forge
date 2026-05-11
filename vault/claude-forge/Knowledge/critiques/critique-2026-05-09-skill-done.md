---
titre: "Critique — Skill /done (metacognition fin de session)"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-09
auteur: claude
resume: ""
aliases: []
tags: []
---

# Critique adversariale — Skill `/done`

## Intention declaree
Extraire automatiquement decisions/faits/preferences/erreurs de la conversation courante en fin de session pour mettre a jour memoire et vault.

## Bloquants

1. **Frontmatter non-conforme** — `model: opus`, `effort: high`, `memory: project`, `user-invokable: true` sont des champs d'agent. Sur une skill, ils sont ignores silencieusement. Fausse promesse de comportement Opus xhigh.
2. **Encodage path memoire fragile** — l'algo de derivation du project-id (a partir du chemin Windows) n'est pas specifie. Va casser sur paths avec espaces ou drive non-standard.
3. **Doublon non justifie avec `/recap`** — le dispatch existant utilise deja `/recap` pour reprise/snapshot session. Difference avec `/done` non documentee.

## Avertissements

- `ls ~/.claude/projects/*/memory/` cross-projet → faux positifs de dedup, risque d'updater un fichier d'un autre projet.
- Pas de garde anti-hallucination sur session vide ou courte. Le LLM va remplir 4 listes meme sans matiere.
- Reimplementation partielle de l'auto-memory CC native.
- Skill manuelle sans Stop hook = oubli previsible → compounding meurt.
- Maintenance double (chemins, formats, templates) sans tests automatises.
- Filtre OBLIGATOIRE sous-specifie (frontiere "pattern de code" vs "fait technique" floue).

## Nitpicks

- Rapport final 5 sections = trop verbose pour fin de session.
- Section Apprentissage manuelle redondante avec auto-memory.

## Si je devais le faire marcher

1. Nettoyer frontmatter (retirer model/effort/memory/user-invokable).
2. Splitter en agent `session-distiller` + Stop hook + skill `/done` comme alias manuel.
3. Encodage path robuste via `$CLAUDE_PROJECT_DIR` + fonction explicite testee.
4. Dedup memoire scopee projet courant uniquement.
5. Clarifier ou fusionner `/done` et `/recap`.
6. Garde anti-hallucination si conversation < 10 messages utiles.
7. Rapport 4 lignes max, detail dans `last-done.md`.
8. Smoke test sur session synthetique avant livraison.

## Verdict

**Decision : BLOQUER** — 3 bloquants, 6 avertissements, 2 nitpicks. La skill telle quelle livre la moitie d'un systeme (extraction sans trigger fiable) avec un frontmatter qui ne fait pas ce qu'il pretend faire.

## Liens

