---
name: no-doc-agent
description: Pas d'agent doc dedié. Le CTO évalue si la doc doit bouger, le dev met à jour ou crée le fichier.
type: feedback
---

Pas d'agent dédié à la documentation. C'est du bloat.

**Why:** La mise à jour de doc est ponctuelle, pas un workflow récurrent. Le `dev` agent a déjà Write dans ses tools.

**How to apply:** Après une feature significative, le CTO (session principale) évalue si `doc/` doit être mis à jour. Si oui, il délègue au `dev` qui peut modifier ou créer un nouveau fichier dans `doc/`. Ne jamais proposer un agent "doc-writer" ou "scribe".
