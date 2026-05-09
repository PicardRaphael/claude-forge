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

## Forge Brain — via CLI Obsidian

Toujours utiliser la CLI Obsidian pour interagir avec le vault :

Toujours utiliser la CLI Obsidian pour interagir avec le vault :
```bash
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" search query="..."
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh vault="claude-forge" read file="..."
```
JAMAIS Grep/Read brut sur le vault. Fallback si Obsidian ferme.

## Anti-patterns

- "Je sais deja" → non, relire les feedbacks. Le contexte change.
- "C'est rapide, pas besoin" → c'est justement quand on va vite qu'on oublie.
- Mettre a jour la memoire 3 sessions trop tard → le detail est perdu.
