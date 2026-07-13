---
name: repo-autonomy-mandatory
description: Chaque repo doit etre autonome sans claude-forge. claude-forge est personnel a Raphael, les collegues doivent pouvoir continuer sans.
type: feedback
originSessionId: a553b6f6-4880-433c-9a32-d422a31d3f1f
---
Chaque repo projet (neo_ia, ia_back, neoteem-brain, bdd) doit etre AUTONOME. Ne JAMAIS creer de dependance vers claude-forge.

**Why:** claude-forge est personnel a Raphael. Si il quitte l'entreprise, les collegues doivent pouvoir continuer a travailler avec Claude Code sans claude-forge. Les skills/agents/hooks doivent vivre dans le repo du projet.

**How to apply:** Quand on cree un composant utile pour un projet :
1. Le creer directement DANS le repo cible (neo_ia, ia_back, etc.)
2. Optionnellement garder une copie dans claude-forge comme version perso
3. Ne JAMAIS utiliser additionalDirectories vers claude-forge dans les repos projet
4. La version projet doit etre self-contained (pas de ref a forge-brain, pas de skills forge)
