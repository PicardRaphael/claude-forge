---
name: audit-transverse-periodique-hooks-gardes-ecriture
description: Les hooks sont des gardes en ÉCRITURE, pas des scanners périodiques. Composant créé/édité avant l'existence d'un hook (ou via un chemin qui le contourne) conserve ses résidus indéfiniment. Un audit transverse ponctuel reste nécessaire même quand un hook veille. Le hook lui-même est l'oracle de classification (le passer en scan sur tout le scope = vérité, pas opinion). (27 mai)
metadata:
  type: feedback
---

Un hook PreToolUse (ex : `meta-commentary-detector`) ne rejette qu'au moment de l'écriture future. Tout composant créé ou édité AVANT l'existence du hook — ou via un chemin qui le contourne — garde ses non-conformités sans jamais être re-scanné.

**Pourquoi :** audit transverse claude-forge 27 mai — 5 résidus sur 78 composants (94% conformes), dont 2 meta-commentaires que le hook détecte mais qui étaient passés (skills pré-hook). 9 sessions avaient adapté ce qu'elles touchaient, jamais audité le reste.

**How to apply :** Après plusieurs sessions de transformation, lancer un audit transverse ponctuel — ne pas supposer que "le hook veille donc tout est propre". Méthode : passer le hook lui-même en mode scan sur TOUT son scope (`check_content` sur chaque fichier) → c'est l'oracle de classification, distingue vraie violation vs faux positif sans opinion. Compléter par les critères que le hook ne couvre pas : wikilinks morts (croiser `[[X]]` avec existence vault via MCP), imports orphelins (pyflakes), couleurs agents vs convention, path resolution par contexte ([[resolution-path-3-contextes]]).

Cf [[erreur-meta-commentaires-composants]] (distinction attribution-source vs label structurel), [[cartographie-exhaustive-avant-delegation]].
