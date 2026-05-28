---
description: "Scan memory feedbacks before starting tasks, update memory after significant sessions"
---

# Discipline memoire — OBLIGATOIRE

## En debut de tache

Avant de commencer une tache substantielle, scanner la memoire pour les feedbacks pertinents :
- Feedbacks lies au TYPE de tache (skill → feedback_skill_*, agent → feedback_agent_*)
- Feedbacks lies au PROJET concerne (ia_back, neo_ia, neoteem-brain, bdd)
- Erreurs passees documentees (feedback_major_mistakes)

Ne pas attendre de se souvenir — relire proactivement.

## En fin de session

Si la session a produit un apprentissage non trivial :
- Feedback recu → creer/mettre a jour un fichier memoire feedback_*
- Decouverte technique → creer/mettre a jour un fichier memoire reference_*
- Contexte projet change → mettre a jour le fichier memoire project_*

## Frontière mémoire ↔ vault (CANONIQUE)

| Type d'info | Où ? | Exemple |
|-------------|------|---------|
| Feedback relation Raphael | `memory/feedback_*.md` | "ne pas éditer directement les skills" |
| Préférence utilisateur | `memory/user_*.md` | profil holistique, comment travailler |
| Référence technique | `memory/reference_*.md` | pattern neo-brain, permissions limitation |
| **Contexte projet STABLE** | **`vault/1-Projets/<nom>/`** | stack, repos, scope, contraintes |
| Phase projet ÉPHÉMÈRE | `memory/project_*.md` | "en cours de refacto", "prochain sprint" |
| Erreur significative | les DEUX | `memory/feedback_*` + `Knowledge/erreurs/` |
| Savoir technique réutilisable | `vault/` uniquement | techniques, modèles, leaders |
| Question technique résolue | `vault/Knowledge/questions/` | — |
| Exploration technique | `vault/Knowledge/explorations/` | — |

**Règle clé :** `vault/1-Projets/` = source canonique pour le contexte projet stable. `memory/project_*.md` = uniquement la phase en cours et les décisions temporaires. Si une info est dans les deux → la supprimer de memory, garder le vault.

## Triade memory/vault/memory-physique (3 acteurs)

Avant de créer un nouveau fichier dans `memory/`, distinguer les 3 acteurs et appliquer le workflow décision :

- **`MEMORY.md`** = table des matières + déclencheurs critiques (≤ 50 entrées tier-1)
- **vault canoniques** = source de vérité doctrinale (règles énoncées, réutilisables)
- **`memory/*.md`** = exceptions empiriques uniquement (≤ 100 fichiers cible)

### Workflow décision (4 étapes obligatoires)

1. `mcp__forge-brain__search_brain` sur le sujet du feedback envisagé
2. Canonique vault existe → **POINTEUR 1 ligne** dans MEMORY.md, pas de fichier feedback
3. Cas empirique précis non couvert vault → feedback `memory/*.md` ciblé (tier-1 ou tier-2)
4. Sujet majeur sans canonique ET pattern récurrent (2-3 incidents) → **promouvoir vault d'abord** (créer note canonique), puis pointeur. 1 incident isolé → garder en feedback jusqu'à récurrence.

Détails complets + exemples PASS/FAIL + cibles empiriques : [[pattern-maintenance-hybride-corpus-accumulatif]] section "Architecture cognitive — trois acteurs".

### Anti-patterns spécifiques

- Création feedback sans `search_brain` vault préalable → doublon mécanique
- Feedback memory qui réécrit la canonique vault → la doctrine vit dans vault
- Promotion vault prématurée (1 incident isolé) → attendre 2-3 récurrences

## Forge Brain — via MCP forge-brain

Accès vault UNIQUEMENT via MCP forge-brain (auto-start SessionStart, port 8091).
JAMAIS CLI Obsidian, Grep ou Read brut sur le vault.
Outils : `search_brain`, `read_note`, `list_notes`, `vault_stats`, `create_note`, `append_note`, `update_property`.

## Anti-patterns

- "Je sais deja" → non, relire les feedbacks. Le contexte change.
- "C'est rapide, pas besoin" → c'est justement quand on va vite qu'on oublie.
- Mettre a jour la memoire 3 sessions trop tard → le detail est perdu.
