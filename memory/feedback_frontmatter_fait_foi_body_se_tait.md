---
name: frontmatter-fait-foi-body-se-tait
description: "Frontmatter d'un agent/skill fait foi. Le body ne doit JAMAIS re-commenter ni contredire un champ frontmatter (effort, model, memory). Grep le champ dans le body après modif."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f598fcbc-1e1f-4161-bd42-75eddf13fbdf
---

Le frontmatter d'un composant (agent, skill) est la source de vérité unique pour ses champs (`effort`, `model`, `memory`, `permissionMode`). Le body NE DOIT PAS re-commenter ni re-justifier ces champs.

**Why:** Double faute classique = le body affirme une valeur que le frontmatter dément (cas réel 27 mai : `devils-advocate.md` avait `effort: high` en frontmatter mais le body disait `effort: xhigh — la pensée adversariale exige une profondeur maximale`). C'est (1) une contradiction interne qui drift quand l'un évolue sans l'autre, et (2) du meta-commentaire doctrinal dans un composant (viole [[pas-de-meta-commentaire-doctrine-composants]], bloqué par le hook meta-commentary-detector). Le pourquoi vit dans le vault, pas dans le body.

**How to apply:** Après toute création/modif d'agent ou skill, `grep` la valeur du champ frontmatter dans le body. Si elle apparaît avec une justification → la supprimer (ne pas la "corriger" en alignant la valeur — le frontmatter parle seul, le body se tait). Règle capitalisée dans la canonique vault [[comment-creer-agent]] section "Frontmatter vs body : alignement obligatoire".
