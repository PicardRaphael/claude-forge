---
name: session-multi-chantiers-piege
description: "Ne JAMAIS enchaîner 4+ chantiers indépendants dans une seule session — la fatigue de fin produit des erreurs avec même signature (claims faux, paths hardcodés, fichiers manquants)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8957d13-cb6a-43d0-ae69-71bb7fa375a2
---

Cf [[context-management]] (doctrine : /clear entre tâches non liées, "kitchen sink session = piège #1", Document & Clear, /compact proactif sous 40-60%, subagents pour isolation de contexte).

**Cas empirique(s) :**

- Session 2026-05-20, 30+ tours avec 4 chantiers indépendants enchaînés (running-notes + decompose-ticket + x-read + MCP postgres) → cette session a re-prouvé empiriquement le piège #1 de Boris ("sessions fourre-tout"). Le DA a identifié 3 erreurs avec exactement la même signature "fin de session fatiguée" :
  1. `certs/README.md` annoncé créé mais inexistant (claim faux)
  2. x-read description "Read-only enforced by construction" alors que le code dit le contraire
  3. decompose-ticket ia_back : 19 paths Windows hardcodés (3ème récidive d'une erreur déjà documentée 2×)

Voir [[critique-session-2026-05-20-running-notes-decompose-xread-mcp]] dans le vault.
