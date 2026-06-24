---
description: "Délègue toute modification de composant à sa skill créatrice. delegate-guard.py bloque (exit 2) les écritures directes des 4 types : CLAUDE.md, agents, skills, hooks."
---

# Délégation aux spécialistes — OBLIGATOIRE

Ne JAMAIS écrire directement les fichiers que des skills créatrices savent produire. Le hook `delegate-guard.py` (PreToolUse Write|Edit|MultiEdit) bloque l'écriture directe et force le passage par la bonne skill — qui applique automatiquement la checklist d'écriture parfaite.

| Fichier modifié              | Skill à invoquer                 | Bloqué par delegate-guard |
| ---------------------------- | -------------------------------- | ------------------------- |
| `CLAUDE.md`                  | `claudemd-creator`               | **Oui — exit 2**          |
| `agents/*.md`                | `subagent-creator`               | **Oui — exit 2**          |
| `skills/<nom>/SKILL.md`      | `skill-creator`                  | **Oui — exit 2**          |
| `hooks/*.py`                 | `hook-creator`                   | **Oui — exit 2**          |
| Critiquer un livrable majeur | `devils-advocate`                | Non — rule conditionnelle |
| Évoluer/optimiser une skill  | `skill-evolve` → `skill-creator` | via skill-creator         |

## La règle vaut CROSS-REPO — le hook, non

La règle de comportement s'applique **quel que soit le repo cible** : éditer un `SKILL.md`/agent/hook/`CLAUDE.md` dans ia_back, neo_ia, migration_script ou tout autre repo → invoquer la skill créatrice, exactement comme dans forge. Forge peut écrire partout (permissions cross-repo), mais « écrire partout » n'autorise jamais le raccourci de la rédaction à la main.

⚠️ `delegate-guard.py` ne fire que sur les fichiers **sous forge/** (test `is_inside_forge`). Hors forge, **aucun blocage technique** — c'est la discipline qui tient la couverture. Incident 24 juin : 9 `SKILL.md` écrits à la main dans `migration_script` (repo d'équipe) sans déclencher le guard. Décision Raphael : pas de durcissement du hook (on ne livre pas de hook bloquant à un repo d'équipe, cf [[config-repo-equipe-vs-forge]]) → engagement de comportement. Cf `memory/feedback_ecrire_partout_invoquer_skill_creatrice.md`.

## Comment le hook reconnaît une skill légitime (détection 2026-06-06)

Les skills créatrices ne sont PAS des sous-agents : `agent_type` et `agent_id` sont `null` quand elles tournent. Le hook lit donc le champ **`attributionSkill`** dans le transcript de session (écrit par Claude Code, vérifié sur CC 2.1.167).

**Bypass STRICT** : `attributionSkill` doit correspondre à la skill propriétaire du fichier — `claudemd-creator` ne débloque que `CLAUDE.md`, `skill-creator` que les `SKILL.md`, etc. Une skill active ne peut pas débloquer un type de fichier qu'elle ne possède pas.

## Exceptions du hook

- Correction de typo < 20 caractères (Edit/MultiEdit) → warning, pas de blocage
- Skills externes/kepano (`json-canvas`, `defuddle`, `obsidian-markdown`, `obsidian-bases`, `obsidian-cli`) → non protégées (copies read-only)
- `delegate-guard.py` lui-même + fichiers `test_*.py` → exemptés (anti self-lock)
- Fichier hors du projet claude-forge → jamais bloqué

## Frontière modification ≠ analyse

Le hook protège la **modification** (écriture), JAMAIS l'analyse/lecture. Lire un composant pour l'auditer est libre : le vault et les rules portent la même méthode. Seule l'écriture risque un format cassé, donc seule l'écriture est forcée vers la skill.

## INTERDIT — ne jamais contourner le hook

Si le hook bloque, la réponse n'est JAMAIS de le contourner (injecter `CLAUDE_AGENT`, passer par un script Python externe, Write au lieu d'Edit). On corrige le hook ou on invoque la skill. Contourner un garde-fou de scope = anti-pattern absolu.

## Pourquoi

Les skills créatrices appliquent les best practices automatiquement (description une ligne, name=dossier, pas de BOM, exit 2 vs exit 1, adaptation OS). L'édition directe a produit des composants non conformes à 3 reprises (2026-04-26).
