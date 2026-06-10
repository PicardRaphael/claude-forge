---
titre: "Critique DA — Doctrine pas de meta-commentaires dans composants"
resume: "Devils-advocate sur la règle universelle 'pas de justification/source/meta dans hook/agent/skill/CLAUDE.md/rule' imposée 24 mai 2026. Verdict : valider avec 6 amendements. 2 BLOCKING : claude-forge/CLAUDE.md viole déjà la règle (7 infractions), 'désambiguïsation courte' sans frontière mesurable."
aliases:
  - "critique meta-commentaires doctrine"
  - "DA meta-commentaires 24 mai"
  - "critique 24 mai meta"
derniere-maj: 2026-05-24
auteur: claude
type: critique
tags:
  - "#type/critique"
  - "#domaine/claude-code"
  - "#domaine/doctrine"
---

# Critique DA — Doctrine pas de meta-commentaires dans composants

## Verdict

**Bloquants : 2** | **Avertissements : 3** | **Nitpicks : 2**

**Décision : VALIDER AVEC AMENDEMENTS** — saine sur le fond mais inapplicable en l'état.

## BLOCKING 1 — claude-forge/CLAUDE.md viole déjà la règle

7 infractions documentées sur 105 lignes du CLAUDE.md de référence :

| Ligne | Contenu | Type |
|-------|---------|------|
| L3 | `Version : 3.2 (5 lignes Karpathy en ouverture)` | Justification historique |
| L51 | `Pivot doctrinal complet : [[raisonnement-22mai-doctrine-vs-enforcement]]` | Mention source |
| L54 | `max toujours disponible mai 2026 mais prone overthinking — utiliser avec prudence` | Note pédagogique |
| L55 | `Sonnet exécution, Opus jugement (validé 21 mai)` | Justification parenthésée |
| L74 | `"Give Claude a way to verify its output" = tip #1 Boris` | Mention source |
| L87 | `Vault forge-brain (pattern Karpathy strict depuis 22 mai)` | Justification + source titre |
| L99 | `Au-delà, dégradation quadratique (UCL 2601.00880)` | Source académique |

La règle est promulguée mais le composant de référence ne s'y conforme pas. Cas exact du drift silencieux. La doctrine est rhétorique tant que claude-forge/CLAUDE.md n'est pas purgé.

## BLOCKING 2 — "désambiguïsation courte" sans frontière mesurable

Exception "1-2 mots entre parenthèses" subjective :
- `(jamais medium)` = 2 mots → clarifie ou justifie ?
- `(toujours opus pour jugement)` = 4 mots → clarifie ou justifie ?
- `(validé 21 mai)` = 3 mots → justifie historiquement
- `(pas auto, bug v2.1.79)` = 4 mots → clarifie + justifie

Sans règle de comptage stricte, chaque session de purge tranche différemment → drift à chaque audit.

## AVERTISSEMENTS

1. **Test lexical rate les meta-cachés** : `"= tip #1 Boris"` ne commence pas par "Source :" mais finit par attribution. `"(UCL 2601.00880)"` en parenthèse finale. Test "commence par..." rate ces cas.

2. **Vault canonique pas toujours à portée** :
   - Sub-agents non-réentrants ne peuvent pas appeler MCP forge-brain
   - Collaborateur Neoteem ouvrant `ia_back/CLAUDE.md` sans Claude → pas de vault accessible
   - Un dev qui maintient un CLAUDE.md lit le CLAUDE.md, pas un vault distant
   
   Transfert de charge maintenance vers humain qui n'a pas accès au pourquoi au moment voulu.

3. **2 emplacements codification = règle silencieuse** :
   - `memory/feedback_pas_de_meta_commentaire_doctrine.md` — chargé conditionnellement
   - `vault/Knowledge/erreurs/...` — consulté seulement si `search_brain` matche
   
   Aucun lu systématiquement en début de session. Sans rule dans `.claude/rules/`, règle non chargée d'office.

## NUANCES

- **Anthropic publie-t-il sans meta ?** Non vérifié empiriquement (vault interrogé seulement). Si Anthropic eux-mêmes mettent des `// because` en commentaire, doctrine forge plus stricte qu'eux. À vérifier WebFetch.
- **Le problème réel est peut-être le bruit, pas la nature du meta**. Formulation plus étroite possible : *"JAMAIS de ligne qui relativise/contextualise les règles immédiatement précédentes."* Interdit l'erreur exacte sans surcontraindre.

## 6 AMENDEMENTS RECOMMANDÉS

1. **Définir empiriquement frontière désambiguïsation** : règle ≤3 mots stricte, comptable
2. **Purger CLAUDE.md de claude-forge** : 7 infractions L3, L51, L54, L55, L74, L87, L99
3. **Créer `.claude/rules/no-meta-commentary.md`** chargée systématiquement
4. **Garde-fou anti-purge agressive** : vérifier que le pourquoi est dans le vault AVANT supprimer une mention source/date
5. **Vérifier empiriquement Anthropic** via WebFetch sur leurs CLAUDE.md publics
6. **Appliquer [[methode-pivoter-doctrine]]** : seuls 3 CLAUDE.md touchés, pas agents/skills/hooks/rules existants

## Précédents vault

- [[critique-2026-05-22-doctrine-drift-guard]] — même pattern : règle promulguée sans purger composants existants
- [[methode-pivoter-doctrine]] — checklist 5 étapes pour pivoter sans drift résiduel (NON appliquée pour doctrine 24 mai)
- [[feedback_doctrine_drift_pattern]] — risque exact soulevé ici

## Conclusion

Sans les 6 amendements, la doctrine sera oubliée en 2 semaines ou appliquée différemment à chaque audit.

## Méthode de chasse aux méta-notes (validé empiriquement 2026-06-09)

L'AVERTISSEMENT 1 (« test lexical rate les méta-cachés ») confirmé sur un vrai livrable « au présent pur » (CDC neoteem-back-ts). Leçon de méthode pour purger un livrable de ses méta-notes :

1. **Une méta-note est une catégorie SÉMANTIQUE, pas lexicale.** Un `grep`/`search_brain` n'attrape que les tournures anticipées (« Source : », dates). Il sert à s'orienter, jamais à PROUVER l'absence de méta-note. Ne jamais conclure « zéro méta-note » sur la foi d'un grep.
2. **Les méta-notes se cachent dans ce qui a été RÉDIGÉ pendant la session courante**, pas dans le doc ancien déjà nettoyé. Réflexe : relire en lecture sémantique (30 s/section) toutes les sections écrites ou modifiées CETTE session, en cherchant « ce qu'on faisait avant / maintenant on / tranché / reformulé / ancienne doctrine ».
3. **Patterns récurrents à traquer** : flèche de reformulation `« X » → « Y »` (avant→après explicite) ; référence à une « ancienne doctrine » / « jusqu'ici » ; parenthèse contrastive « (on l'évitait déjà — ici on grave…) » ; titre de section qui narre le processus (« décisions, pas options ouvertes »).
4. **Distinguer méta-note vs justification-au-présent légitime.** Le « pourquoi » d'une règle au présent (« neverthrow car agent-proof ») est de la spec, pas une méta-note. Une DATE factuelle (artefact daté à régénérer, release cible) n'est pas du changelog. Seule la **trace de délibération / d'historique** est interdite.

Cas 2026-06-09 : un advisor a pointé 2 sections (propres) ; la lecture sémantique guidée a trouvé 2 vraies méta-notes AILLEURS (§7.2 « Cible reformulée X→Y », « ancienne doctrine PG-first »). Le grep et l'advisor les avaient ratées — seule la relecture sémantique des sections session-authored les a sorties.

Cf [[feedback_pas_de_meta_commentaire_doctrine]] (le QUOI : la règle) — cette section porte le COMMENT (la méthode de vérification).
