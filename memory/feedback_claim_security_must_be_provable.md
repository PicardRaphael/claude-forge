---
name: claim-security-must-be-provable-by-code
description: "Tout claim sécu (\"read-only\", \"by construction\") doit être prouvable structurellement par le code, sinon \"by discipline\""
metadata:
  type: feedback
  originSessionId: a8957d13-cb6a-43d0-ae69-71bb7fa375a2
---

Cf [[hooks-conformite-audit-passif-continu]] (doctrine "by construction vs by discipline" — la conformité prouvable par le code est canonique vault).

**Cas empirique x-read 2026-05-20** : description disait "Read-only enforced by construction" mais `reader.py` importait `Account` class avec `tweet()/like()/follow()` accessibles en RAM. Read-only **par discipline** (CLI ne route pas), pas **par construction**. DA a tagué BLOCKING. Vecteur d'attaque concret : prompt injection sur tweet capté → demande à Claude d'invoquer une write method existante en RAM. Voir [[critique-session-2026-05-20-running-notes-decompose-xread-mcp]].
