---
name: plugin-admin-absorbe-readonly
description: Quand un plugin existe en version read-only ET admin (write), enabler l'admin remplace fonctionnellement le read-only. Desinstaller le read-only sans perte de fonctionnalite, gain tokens.
metadata:
  type: feedback
---

**Constat empirique 28 mai 2026** — audit plugins neoteem-brain.

5 plugins neoteem-brain existaient enabled simultanement :
- `neoteem-brain-dev` (read-only, ~90 tokens)
- `neoteem-brain-dev-ia` (admin, read+write, ~120 tokens) — admin a lui seul (description verbatim "Full vault access read+write")
- `neoteem-brain-support` (read-only, ~100 tokens)
- `neoteem-brain-dev-admin` (admin, lazy-load)
- `neoteem-brain-support-admin` (admin, lazy-load)

L'admin etant un sur-ensemble du read-only, garder les deux = doublon fonctionnel + tokens cost double.

**Why** : economie 190 tokens / session sur forge sans perte de capacite.

**How to apply** :
1. Pour tout couple `<X>` + `<X>-admin` enabled : verifier empiriquement que l'admin couvre les meme tools que le read-only (`allowed-tools:` dans SKILL.md).
2. Si oui, desinstaller le read-only ; garder l'admin.
3. ATTENTION : la skill du read-only et celle de l'admin ont des `name:` differents (`neo-brain` vs `neo-brain-dev-admin`). Si une rule/agent reference la skill read-only par son name, mettre a jour pour pointer vers l'admin.

**Cas inverse** : un plugin peut s'appeler `<X>-ia` ET etre admin a lui seul (cf `neoteem-brain-dev-ia` qui a write access via MCP obsidian-brain). Le suffixe n'est pas un indicateur fiable. Toujours lire la description.

Lien : [[reference_plugins_scoping_mecanisme]].
