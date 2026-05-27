---
name: pas-de-meta-commentaire-doctrine-composants
description: "JAMAIS de meta-commentaire / justification / source dans hook, agent, skill, CLAUDE.md, rule. Directives nues uniquement. Le pourquoi vit dans le vault canonique."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72a20014-5e49-4c73-a59e-6512f642233a
---

JAMAIS de meta-commentaire, justification, ou mention de source dans le contenu directif d'un hook, agent, skill, CLAUDE.md, ou rule. Directives nues uniquement.

**Anti-patterns concrets observés** :
- `*Ces 5 lignes biaisent vers la prudence plutôt que la vitesse. Pour les tâches triviales, utiliser le jugement. Source : Karpathy 26 jan 2026 + doctrine forge. Ne comptent pas dans le budget des Interdits absolus ci-dessous.*` → bruit, raison Raphael 24 mai 2026
- `"D'après Karpathy / Anthropic / Boris Cherny..."` dans le corps → bruit
- `"(Cette section vient de la doctrine 22 mai 2026)"` → bruit
- `"Source : [[note-canonique]]"` en pied de section → bruit
- Explications du POURQUOI une règle existe dans le composant lui-même → bruit

**Why :** Claude exécute des directives, pas des dissertations. La justification dilue le signal et fait perdre des tokens d'attention sur ce qui doit être appliqué. Le pourquoi vit dans le vault canonique (`vault/claude-forge/04-Techniques/`, `Knowledge/`), pas dans le composant qui consomme la règle. Décision Raphael 24 mai 2026 après avoir vu une ligne italique de justification ajoutée dans 3 CLAUDE.md (claude-forge, ia_back, neo_ia).

**How to apply :**
- Hook, agent, skill, CLAUDE.md, rule = directives nues
- Sources, raisonnements, mappings, historique de décision → vault canonique UNIQUEMENT
- Si tentation d'ajouter "parce que..." dans un composant → STOP, ça part dans le vault
- Exceptions OK : 1-2 mots entre parenthèses pour désambiguïser un terme (ex: `"acceptEdits (pas auto)"`), JAMAIS une phrase complète de justification
- S'applique aussi aux frontmatter YAML : description = trigger, pas explication
- S'applique aussi aux commentaires de code dans hook scripts : commenter le WHY non-obvious OK, justifier la doctrine NON

**Test simple :** si la phrase commence par "Ces ... biaisent / Source : / D'après / Note : / (Cette section ...)" → supprimer, c'est du vault.

**Source canonique vault :** [[erreur-meta-commentaires-composants]] (Knowledge/erreurs/).
