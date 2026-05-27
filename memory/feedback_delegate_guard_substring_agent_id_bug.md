---
name: delegate-guard-substring-agent-id-bug
description: "delegate-guard.py L143-145 accorde le bypass à tout agent_id CONTENANT un nom de spécialiste (substring match, pas exact). Bug over-permissif, à durcir en exact-match."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f598fcbc-1e1f-4161-bd42-75eddf13fbdf
---

`delegate-guard.py` (lignes 143-145) vérifie le bypass spécialiste avec un **substring match** sur `agent_id` : `for specialist in ALLOWED_SPECIALISTS: if specialist in agent_id`. Conséquence : un `agent_id="totally-unrelated-skill-creator-suffix"` obtient le bypass alors qu'il n'est pas un vrai spécialiste.

**Why:** Découvert 27 mai (Phase 2 tests adverses). C'est une faille over-permissive : la protection de délégation peut être contournée par un agent_id arbitraire contenant `skill-creator`/`agent-creator`/`hook-creator`/`claudemd-optimizer` comme sous-chaîne. Surface d'attaque réelle FAIBLE car `agent_id` est fixé par le harness Anthropic, pas par l'utilisateur — mais le code est incorrect par construction. Le check `agent_type` (L135) fait du exact-match correct ; seul `agent_id` (L143-145) a la faille.

**How to apply:** Test `test_weakness_agent_id_substring_grants_bypass` (test_delegate_guard.py) épingle le comportement ACTUEL (assert ok is True). Quand on durcit : remplacer le substring match L143-145 par exact-match (`if agent_id in ALLOWED_SPECIALISTS`, déjà fait L140) → supprimer la boucle substring, et inverser l'assertion du test. À faire via hook-creator (délégation). Voir [[tests-adverses-obligatoires]] : c'est exactement le type de bug que les tests adverses révèlent et que le happy path masque.
