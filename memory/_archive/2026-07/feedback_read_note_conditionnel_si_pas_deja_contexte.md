---
name: read-note-conditionnel-si-pas-deja-contexte
description: Avant chaque read_note canonique audit/jugement, vérifier si déjà en contexte session. Si oui = citer + wikilink, ne pas re-lire. Application directe règle tokens/contexte.
metadata:
  type: feedback
---

# read_note conditionnel — si pas déjà en contexte

## Règle

Avant chaque `mcp__forge-brain__read_note` sur une canonique vault (audit/jugement/recommandation), **scanner mentalement le transcript de la session courante** :

- Canonique déjà lue EN ENTIER ce tour ou un tour précédent ? → **citer directement le passage + wikilink**, ne pas re-read_note
- Canonique citée seulement via `search_brain` (extraits ~10 lignes) ? → `read_note` EN ENTIER obligatoire (extraits insuffisants pour audit)
- Canonique jamais touchée ? → `read_note` EN ENTIER

La doctrine "read_note EN ENTIER avant audit" (CLAUDE.md L14) reste stricte — la nuance "si pas déjà en contexte" est un garde-fou contre le double-pay tokens, pas une dérogation.

## Why

CLAUDE.md L14 prescrit `read_note EN ENTIER` avant audit/jugement. CLAUDE.md L19 prescrit "tokens/contexte = ressource ultra-précieuse, fichiers obsolètes/doctrine périmée dégradent chaque tâche".

Sans la nuance "si pas déjà en contexte", L14 et L19 entrent en tension implicite : re-read_note d'une canonique 2000+ tokens déjà chargée en contexte = double-pay sans gain informationnel. Le contenu est encore frais, pas dégradé.

Exemples concrets de gaspillage évitable :
- Tour 1 : `read_note pattern-mcp-brief-then-direct` (3200 tokens chargés)
- Tour 3 : audit d'un autre composant → tentation re-`read_note pattern-mcp-brief-then-direct` → 3200 tokens dupliqués alors que le contenu du tour 1 est cité-able

Anti-pattern symétrique : "j'ai vu la note il y a 5 messages mais je re-read_note pour être sûr" → non, le contexte session n'a pas muté, le contenu n'est pas dégradé.

## How to apply

Avant tout `read_note` audit/jugement :

1. Quick scan transcript courant : la canonique cible a-t-elle déjà fait l'objet d'un `read_note` (pas juste `search_brain`) ?
2. Si OUI :
   - Citer le passage pertinent avec section / ligne
   - Wikilink `[[note-canonique]]` pour traçabilité
   - Pas de re-read_note
3. Si NON ou tronqué (max_lines / offset partiel) :
   - `read_note` EN ENTIER (sans `max_lines`)
4. Si DOUTE (la note a peut-être été modifiée pendant la session — création/AMEND vault ce tour) :
   - re-read_note légitime (le contexte a muté)

Cas frontière : `read_section` ciblée d'une note dont d'autres sections ont été lues précédemment → légitime si question précise et section_id différent (cf rule `read-section-preference.md`).

Anti-pattern à éviter : appliquer la nuance comme excuse pour skip canonique jamais lue. "Je connais déjà cette canonique de mémoire" = FAUX → savoir interne LLM ≠ contexte session courant. La règle reste : EN ENTIER chargé dans le transcript, sinon `read_note`.

## Liens

- [[pattern-mcp-brief-then-direct]] — canonique du pattern brief enrichi (la nuance "déjà en contexte" est l'extension naturelle côté session principale)
- [[feedback_brief_prescrit_travail_deja_fait_veille]] — feedback voisin (vérifier ce qui a déjà été fait avant d'exécuter)
- [[consolidate-searches]] — règle anti-doublon recherches (ne pas chercher 2× la même info)
- CLAUDE.md L14 — doctrine `read_note EN ENTIER avant audit/jugement si pas déjà en contexte`
- CLAUDE.md L19 — règle absolue tokens/contexte = ressource ultra-précieuse
