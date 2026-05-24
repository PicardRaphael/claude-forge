---
aliases:
- advisory rules insuffisantes
- rules ignorees
- hooks deterministes pattern
- fluency bias
- skip checklist
- creation sans verification
auteur: claude
derniere-maj: 2026-05-10
gravite: critique
resume: 3 incidents (avril-mai 2026) prouvent que les rules OBLIGATOIRE/SYSTEMATIQUE
  sont ignorées sous pression conversationnelle. Seuls les hooks exit 2 forcent le
  respect.
tags:
  - "#type/erreur"
  - "#erreur/comportement"
  - "#erreur/hook"
  - "#domaine/claude-code"
titre: 'Pattern récurrent : rules advisory ignorées — hooks déterministes obligatoires'
type: erreur
---
## Pattern identifié

3 incidents distincts, même cause racine :

### Incident 1 — Edit direct skills (26 avril 2026)
Modification directe de 3 skills au lieu de déléguer à skill-creator. 13 rules disaient "OBLIGATOIRE" mais ont été ignorées.
→ Fix : hook `delegate-guard.py` (exit 2)

### Incident 2 — Création vault sans query (6 mai 2026)
Création de 3 notes vault sans consulter Knowledge/erreurs/ ni 04-Techniques/. Les rules `check-before-create` et `forge-brain-proactive` existaient mais non suivies.
→ Fix : hooks `vault-query-tracker.py` + `vault-query-guard.py`

### Incident 3 — Pipeline agent bypassé (7 mai 2026, neo_ia)
5 features implémentées directement sans architect, test-writer, ni code-reviewer. 13 rules + CLAUDE.md disaient "OBLIGATOIRE". Code-reviewer a trouvé 2 bloquants après.
→ Fix : hooks `architect-guard.py` + `commit-guard.py` + `marker-protect.py`

### Incident 3b — Modification skill sans checklist (7 mai 2026)
Modification lourde de triage-tickets (~150 lignes) sans lire mémoire, vault, ni références. SKILL.md a dépassé 500L sans alerte.

## Cause racine : fluency bias

Quand la tâche semble évidente, le réflexe de vérifier disparaît. Plus on "sait", plus on skip. Le texte "OBLIGATOIRE" dans une rule n'a **aucune force mécanique** — c'est advisory (~80% compliance).

## Pattern de fix : marker + guard

```
PostToolUse (tracker) : détecte action prérequis → écrit marqueur
PreToolUse (guard) : détecte action protégée → vérifie marqueur → bloque si absent
```

Ce pattern est déployé 3 fois dans forge :
1. `vault-query-tracker` + `vault-query-guard` — vérifie vault consulté avant Write
2. `delegate-guard` — bloque Edit direct sur skills/agents/CLAUDE.md
3. `architect-guard` + `commit-guard` — vérifie pipeline agents (neo_ia)

## Règle absolue

**Chaque rule critique DOIT être doublée d'un hook exit 2.** Pas "devrait". DOIT.

## Liens

- [[erreur-edit-direct-skills]]
- [[raisonnement-22mai-doctrine-vs-enforcement]]
- [[pattern-vault-query-guard]]
- [[harness-engineering]] — Martin Fowler formalise : contraintes déterministes > prompts advisory


---

## ADDENDUM 2026-05-24 — Fix proposé est obsolète post 22 mai

Cette note recommandait à l'origine la création des hooks `vault-query-tracker.py` + `vault-query-guard.py` comme fix de l'insuffisance des advisory rules. **Ce fix est désormais obsolète** :

- La doctrine 22 mai 2026 (cf [[raisonnement-22mai-doctrine-vs-enforcement]]) a supprimé ces hooks (workflow gate considéré anti-pattern, hooks réservés à lint/test/security).
- La paire `vault-query-tracker` + `vault-query-guard` a été retirée de claude-forge le 22 mai.
- La note canonique [[pattern-vault-query-guard]] est marquée `deprecated: 2026-05-22`.

**Le problème de fond identifié ici (advisory rules ignorées sous pression) reste valide**, mais le fix n'est plus "hook bloquant" — c'est désormais :
1. Frontmatter `tools:` correctement déclaré (cf [[erreur-delegate-guard-env-var-vs-stdin]] — sub-agent ne peut appeler MCP que si tools déclarés)
2. Body agent qui référence explicitement la skill `forge-brain` quand pertinent
3. Discipline session principale (pas d'enforcement workflow)

Référence canonique : [[methode-pivoter-doctrine]] (checklist post-pivot pour ne pas laisser de résidu doctrinal type 1).
