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

## Forge Brain — via CLI Obsidian

Le vault forge-brain est la memoire LONGUE. La memoire projet (MEMORY.md) est la memoire COURTE.
- Info specifique a la relation avec Raphael → memoire projet
- Info technique reutilisable par n'importe qui → forge-brain vault
- Erreur significative → les DEUX (memoire + Knowledge/erreurs/)
- Question technique resolue → Knowledge/questions/
- Exploration technique → Knowledge/explorations/

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
