---
name: session-multi-chantiers-piege
description: "Ne JAMAIS enchaîner 4+ chantiers indépendants dans une seule session — la fatigue de fin produit des erreurs avec même signature (claims faux, paths hardcodés, fichiers manquants)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8957d13-cb6a-43d0-ae69-71bb7fa375a2
---

Ne JAMAIS enchaîner plus de 2-3 chantiers indépendants dans une seule session Claude Code. Au-delà, /clear entre chantiers.

**Why:** Session 2026-05-20 30+ tours avec 4 chantiers (running-notes + decompose-ticket + x-read + MCP postgres). DA a identifié 3 erreurs avec exactement la même signature "fin de session fatiguée" :
1. `certs/README.md` annoncé créé mais inexistant (claim faux)
2. x-read description "Read-only enforced by construction" alors que code dit le contraire
3. decompose-ticket ia_back : 19 paths Windows hardcodés (3ème récidive d'erreur déjà documentée 2x)

Boris Cherny a explicitement listé "sessions fourre-tout = piège #1". Cette session l'a re-prouvé empiriquement.

**How to apply:**
- Détecter mentalement quand on bascule sur un sujet non-relié au précédent → proposer /clear ou /compact "garder le plan"
- Au-delà de 20 tours sur sujets multiples → forcer une pause, dumper le plan dans un .md, /clear
- 1 chantier = 1 session = 1 commit = 1 DA = 1 push, pas tout enchaîné
- Si l'utilisateur enchaîne plusieurs demandes non-reliées, suggérer activement de séparer ("ça mériterait une session dédiée — on continue ou on /clear avant ?")
- En fin de session longue, le risque d'erreur monte fortement → toute "finition rapide" doit être traitée comme suspecte (audit ls/cat/grep)

Voir [[critique-session-2026-05-20-running-notes-decompose-xread-mcp]] dans le vault.
