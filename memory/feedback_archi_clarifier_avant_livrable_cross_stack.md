---
name: archi-clarifier-avant-livrable-cross-stack
description: "Clarifier archi (qui parle a qui) AVANT redaction livrable cross-stack, pas apres"
metadata:
  type: feedback
---

Avant de rediger un commentaire / ticket / spec / BRIEF qui implique plusieurs backs Neoteem (neo_ia, ia_back, front, BDD, webservices Jerome), poser la question d'archi en PREMIER : "qui parle a qui, qui est expose au front, qui porte le metier". Ne pas commencer la redaction en supposant l'archi.

**Why:** Session 28 mai 2026, commentaire ticket comparatif devis. J'ai suppose front <-> neo_ia direct, puis ia_back <-> front, puis encore une variation. Raphael a du corriger 3 fois (V7 -> V9 -> V10) avant que l'archi soit bonne : neo_ia expose front pour IA uniquement, ia_back jamais expose front, actions metier hors scope des deux (webservices Jerome). Une AskUserQuestion en V1 sur "qui parle a qui dans cette feature" aurait economise 6 iterations. Cf canonique [[archi-backs-neoteem]].

**How to apply:** Des qu'un livrable implique >=2 composants backend Neoteem, premiere action = AskUserQuestion ou question explicite "quel back parle au front pour cette feature / qui orchestre quoi / quelles actions sont metier vs IA". Pas de V1 sans cette clarification. S'applique a tout livrable cross-stack : commentaire Jira, /spec, BRIEF sub-agent, doc archi, propositions techniques. Reference vault : [[archi-backs-neoteem]].
