---
titre: "Erreur — Meta-commentaires de justification dans les composants exécutables"
resume: "Anti-pattern observé 24 mai 2026 : ajout d'une ligne italique justifiant la doctrine (source, raisonnement, mapping) dans le contenu directif d'un CLAUDE.md / hook / agent / skill / rule. Dilue le signal, fait perdre des tokens d'attention."
aliases:
  - "meta commentaire composant"
  - "justification dans CLAUDE.md"
  - "source dans hook"
  - "ne pas justifier dans skill"
  - "pas de doctrine dans agent"
  - "directives nues"
derniere-maj: 2026-05-24
auteur: claude
type: erreur
sources:
  - "Décision Raphael 24 mai 2026 sur 3 CLAUDE.md modifiés (claude-forge, ia_back, neo_ia)"
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#sujet/prompt-engineering"
  - "#doctrine/2026"
---

# Erreur — Meta-commentaires de justification dans les composants exécutables

## Ce qui s'est passé

Le 24 mai 2026, après avoir ajouté les 5 lignes Karpathy en tête de 3 CLAUDE.md (claude-forge, ia_back, neo_ia), j'ai inséré sous le bloc une ligne italique de justification :

```
*Ces 5 lignes biaisent vers la prudence plutôt que la vitesse. Pour les tâches triviales, utiliser le jugement. Source : Karpathy 26 jan 2026 + doctrine forge. Ne comptent pas dans le budget des Interdits absolus ci-dessous.*
```

Raphael a immédiatement demandé la suppression : *"c'est totalement inutile jamais dans hook agent skill claude.md ..."*

## Pourquoi c'était une erreur

**Claude exécute des directives, pas des dissertations.** Une justification dans le composant lui-même :
- Dilue le signal des règles qu'elle prétend renforcer
- Consomme des tokens d'attention sur du contenu non-actionnable
- Fait croire que le rappel pédagogique aide alors qu'il bruite
- Crée un précédent : si on tolère une ligne, il y en aura 5 dans 3 mois

Le POURQUOI d'une règle vit dans le vault canonique. Le composant exécutable applique la règle, point.

## Comportements à proscrire

Anti-patterns concrets à JAMAIS reproduire dans hook, agent, skill, CLAUDE.md, rule :

1. **Lignes italiques de soupape** : *"Ces guidelines biaisent vers X..."*, *"À utiliser avec jugement..."*
2. **Mentions de source** : *"Source : Karpathy"*, *"D'après Anthropic"*, *"Cf doctrine 22 mai 2026"*
3. **Justifications historiques** : *"(Cette règle existe parce que le 21 mai...)"*
4. **Mappings explicatifs en pied** : *"Cette section condense les 4 principes X..."*
5. **Notes pédagogiques** : *"Note : ces 5 lignes ne comptent pas dans le budget des Critiques..."*

## À faire à la place

| Mauvais (composant) | Bon (séparation) |
|---------------------|------------------|
| `*Source : Karpathy + doctrine forge*` dans CLAUDE.md | Directive nue dans CLAUDE.md, source dans [[comment-ecrire-claudemd]] |
| Commentaire `# Pour éviter le bug du 21 mai` dans hook | Code du hook nu, raison dans `Knowledge/erreurs/<nom>.md` |
| Section "Pourquoi cette skill existe" dans SKILL.md | SKILL.md = trigger + instructions, pourquoi dans note canonique |
| Tableau "Mapping forge ⨯ Karpathy" dans CLAUDE.md | Tableau dans la canonique, CLAUDE.md = 5 puces nues |

## Exceptions tolérées

- **Désambiguïsation courte** : 1-2 mots entre parenthèses pour clarifier un terme (`"acceptEdits (pas auto)"`, `"effort: high (jamais medium)"`). JAMAIS une phrase complète.
- **Commentaire WHY non-obvious dans code** : si un hook contient un workaround spécifique d'une lib, 1 ligne de commentaire OK (cf règle CLAUDE.md générale "WHY non-obvious"). MAIS pas pour justifier une doctrine.
- **Description frontmatter** : c'est un trigger (« quand utiliser »), pas une justification. Reste actionnable.

## Distinction attribution-source vs label-structurel

Toute occurrence d'un nom propre (Boris, Anthropic, Karpathy) dans un composant n'est PAS une violation. Distinguer deux usages :

- **Attribution-source (INTERDITE)** : pose un nom externe comme JUSTIFICATION d'une directive. Format typique `directive = source/tip`. Exemples : `"Give Claude a way to verify its output" = tip #1 Boris`, `Doctrine Anthropic "xhigh partout" = biais tokens illimités`. Le `= X` légitime la règle par une autorité → le pourquoi doit vivre dans le vault, pas dans le composant. À retirer (garder la directive nue).
- **Label structurel (AUTORISÉ)** : utilise un nom comme ÉTIQUETTE de section pour la navigation. Exemples : `## Workflow Boris`, `## Doctrine pivot 22 mai 2026`. C'est un repère de structure, pas une justification. À garder.

Test : si on retire le nom, perd-on de l'information actionnable ? Pour un label de section, non (c'est juste un repère) → garder. Pour une attribution-source, la directive reste entière sans le `= source` → retirer le `= source`.

Le hook `meta-commentary-detector` ne bloque QUE les attributions-source (pattern `= tip/source/d'après` en fin de ligne directive), pas les titres de section. Cohérent avec cette distinction. Cf faux positifs déjà corrigés dans [[critique-2026-05-24-regex-source-faux-positifs]].

## Test simple

Si la phrase ajoutée commence par :
- "Ces ... biaisent / sont calibrées / représentent..."
- "Source : ..."
- "D'après ..."
- "Note : ..."
- "(Cette section ..."
- "Cf doctrine ..."

→ SUPPRIMER. Ça part dans le vault canonique, pas dans le composant.

## Liens

- [[comment-ecrire-claudemd]] — canonique CLAUDE.md
- [[comment-creer-hook]] — canonique hooks
- [[comment-creer-agent]] — canonique agents
- [[comment-creer-skill]] — canonique skills
- [[feedback_pas_de_meta_commentaire_doctrine]] — memory feedback associée
