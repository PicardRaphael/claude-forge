---
description: "Scan memory feedbacks before starting tasks, update memory after significant sessions"
---

# Discipline memoire — OBLIGATOIRE

## En debut de tache

Avant de commencer une tache substantielle, scanner la memoire pour les feedbacks pertinents :
- Feedbacks lies au TYPE de tache (skill → feedback_skill_*, agent → feedback_agent_*)
- Feedbacks lies au PROJET concerne (ia_back, neo_ia, neoteem-brain, bdd)
- Erreurs passees documentees (feedback_major_mistakes)

Ne pas attendre de se souvenir — relire proactivement.

## En fin de session

Si la session a produit un apprentissage non trivial :
- Feedback recu → creer/mettre a jour un fichier memoire feedback_*
- Decouverte technique → creer/mettre a jour un fichier memoire reference_*
- Contexte projet change → mettre a jour le fichier memoire project_*

## Frontière mémoire ↔ vault (CANONIQUE)

| Type d'info | Où ? | Exemple |
|-------------|------|---------|
| Feedback relation Raphael | `memory/feedback_*.md` | "ne pas éditer directement les skills" |
| Préférence utilisateur | `memory/user_*.md` | profil holistique, comment travailler |
| Référence technique | `memory/reference_*.md` | pattern neo-brain, permissions limitation |
| **Contexte projet STABLE** | **`vault/1-Projets/<nom>/`** | stack, repos, scope, contraintes |
| Phase projet ÉPHÉMÈRE | `memory/project_*.md` | "en cours de refacto", "prochain sprint" |
| Erreur significative | les DEUX | `memory/feedback_*` + `Knowledge/erreurs/` |
| Savoir technique réutilisable | `vault/` uniquement | techniques, modèles, leaders |
| Question technique résolue | `vault/Knowledge/questions/` | — |
| Exploration technique | `vault/Knowledge/explorations/` | — |

**Règle clé :** `vault/1-Projets/` = source canonique pour le contexte projet stable. `memory/project_*.md` = uniquement la phase en cours et les décisions temporaires. Si une info est dans les deux → la supprimer de memory, garder le vault.

## Profil Raphaël — foyer unique et preuve

Le foyer unique des faits personnels et préférences de collaboration est
`memory/user_raphael_profile.md`. Lire le contrat complet
`docs/second-brain/session-capture.md` avant toute mise à jour.

| Signal | Action |
|---|---|
| fait ou préférence explicite, durable, non sensible | enrichir/corriger le profil existant |
| hypothèse ou interprétation | proposer sous « À confirmer », ne pas écrire comme fait |
| phase temporaire d'un projet | `memory/project_*.md`, jamais le profil |
| santé, finance, secret, localisation précise, nouvelle donnée familiale | ne pas écrire sans « mémorise ceci » explicite |

Une occurrence explicite suffit pour un fait sur soi ; le seuil de 2–3
occurrences reste réservé aux règles générales et feedbacks. Garder une
provenance courte (date + `explicit`/`confirmed`), gérer les contradictions en
remplaçant l'état actif et permettre « oublie X » sans argumenter.

`/done` est le writer de fin de session. Les hooks peuvent signaler une anomalie
déterministe, mais ne décident ni n'écrivent de mémoire à partir du transcript.

## Triade memory/vault/memory-physique (3 acteurs)

Avant de créer un nouveau fichier dans `memory/`, distinguer les 3 acteurs et appliquer le workflow décision :

- **`MEMORY.md`** = table des matières + déclencheurs critiques (≤ 50 entrées tier-1)
- **vault canoniques** = source de vérité doctrinale (règles énoncées, réutilisables)
- **`memory/*.md`** = exceptions empiriques uniquement (WARNING 180 / CRITICAL 220 via hook `memory-saturation-watcher`, base post-migration 7 juil. ~135 ; mesuré 85 au 29 juil. 2026)

### Workflow décision (4 étapes obligatoires)

1. `mcp__forge-brain__search_brain` sur le sujet du feedback envisagé
2. Canonique vault existe → **POINTEUR 1 ligne** dans MEMORY.md, pas de fichier feedback
3. Cas empirique précis non couvert vault → feedback `memory/*.md` ciblé (tier-1 ou tier-2)
4. Sujet majeur sans canonique ET pattern récurrent (2-3 incidents) → **promouvoir vault d'abord** (créer note canonique), puis pointeur. 1 incident isolé → garder en feedback jusqu'à récurrence.

Détails complets + exemples PASS/FAIL + cibles empiriques : [[pattern-maintenance-hybride-corpus-accumulatif]] section "Architecture cognitive — trois acteurs".

### Découverte technique → ENRICHIR l'existant avant de créer

Réflexe valable au-delà de la mémoire, pour TOUTE découverte importante (nouveau pattern, gotcha, doctrine affinée) destinée au vault :

1. `mcp__forge-brain__search_brain` sur le sujet.
2. **Une note/section couvre déjà le sujet → ENRICHIR cette note** (`insert_section`/`append_note`/Edit), pas créer une note neuve.
3. Créer une note neuve UNIQUEMENT si aucune note existante n'est le bon foyer.
4. Si la découverte affine plusieurs canoniques → enrichir chacune + relier par pointeur (éviter deux notes qui décrivent le même réflexe sans se connaître = futur drift). **Chercher ACTIVEMENT tous les foyers impactés** (`search_brain` large + grep `.claude/`), pas seulement les 2-3 évidents — un enrichissement partiel laisse du drift résiduel.

Cohérent avec [[pattern-maintenance-hybride-corpus-accumulatif]] (un concept = un foyer canonique). Cas observé 5 juin 2026 : le pattern « checklist Tasks natif » a enrichi `comment-creer-skill` + `comment-creer-agent` au lieu d'une note séparée orpheline.

### Anti-patterns spécifiques

- Création feedback sans `search_brain` vault préalable → doublon mécanique
- Feedback memory qui réécrit la canonique vault → la doctrine vit dans vault
- Promotion vault prématurée (1 incident isolé) → attendre 2-3 récurrences

## Forge Brain — via MCP forge-brain

Protocole d'accès vault (MCP forge-brain uniquement, outils, quand consulter) : source unique `.claude/rules/forge-brain-proactive.md`. Pas de recopie ici (single-source).

## Anti-patterns

- "Je sais deja" → non, relire les feedbacks. Le contexte change.
- "C'est rapide, pas besoin" → c'est justement quand on va vite qu'on oublie.
- Mettre a jour la memoire 3 sessions trop tard → le detail est perdu.
- Créer un `feedback_*` pour une préférence personnelle → mettre à jour le profil.
- Inférer une préférence puis la présenter comme un fait → garder « À confirmer ».
