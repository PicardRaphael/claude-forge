# Templates Story & Sous-tâche — neoteem-back-ts

> Format validé avec Raphael (9 juin 2026, hiérarchie révisée 10 juin). Mix **PO-Neoteem** (émojis + couleurs ADF) + **GitHub** (checklists). Destiné à un double lecteur : **humain** (lisible) + **Claude Code / agents** (BRIEF auto-suffisant). Source de vérité du format des tickets de ce projet. Miroir : `references/templates.md` de la skill forge `neoteem-back-ts`.

## Hiérarchie Jira Neoteem

**Epic (thème permanent, PO) → Story (brique de travail) → Sous-tâche (US).**
Les epics sont **figés une fois pour toutes** — on n'en crée jamais. Liste, descriptions, routage et protocole de création Jira : `.claude/skills/spec/references/epics-jira.md` (référentiel embarqué dans la skill, copié à l'identique dans chaque repo). Ce qu'on produit ici = des **stories** rattachées à ces epics, avec leurs **sous-tâches**.

## Règles d'or (héritées de la skill `spec` PO)

1. **Suivre le template à la lettre** : sections dans l'ordre, ne pas renommer.
2. **Omettre une section vide** : pas de titre vide, pas de « N/A », pas de placeholder.
3. **Omettre plutôt qu'inventer** : aucune règle métier / critère / contrainte non confirmé par le CDC, le code ou l'utilisateur.
4. **Rattachement à deux niveaux** : (a) toute story se rattache à un **epic existant** (`references/epics-jira.md` de la skill spec) — epic pas évident → demander, jamais choisir en silence ; (b) **sous-tâche-dans-une-story-existante AVANT story neuve** — si le besoin s'inscrit dans une story en cours (`doc/stories/s*/` + Jira), proposer une sous-tâche rattachée, pas une story. Règle PO : « pas de tickets pour rien ».
5. **Story-chantier = brique TOTALE** : elle couvre le cycle complet jusqu'à la mise en service réelle — y compris les sous-tâches de coordination (bascule prod, décommissionnement de l'ancien système) dont l'exécution est devops mais le suivi vit dans la story. Close seulement quand la brique rend son service en production (ex. migration ia_back : « ia_back décommissionné », pas « un remplaçant existe »).
6. **Livrable GÉNÉRÉ = critère de done CHIFFRÉ.** Si une sous-tâche produit un artefact généré (schéma introspecté, client OpenAPI…), son critère de done contient la liste FERMÉE attendue (« exactement N tables : … ») et l'assertion de comptage en test — sinon le done n'est pas prouvable (incident US1 : 37 tables générées pour 17 attendues, aucun critère écrit ne comptait).

## Étiquettes (convention tous projets)
`IA-DEV` (systématique) + `neoteem-back-ts` (étiquette projet) + label de domaine (`setup`/`agent`/`db`/`migration`/`test`/`qualité`/`mcp`/`obs`) + label transverse (`one-shot`/`récurrent`).

---

## TEMPLATE STORY (brique de travail — rattachée à un epic Jira permanent)

```markdown
# STORY — <Titre lisible Jira>

🏷️ IA-DEV · neoteem-back-ts · <one-shot|récurrent>
↳ Epic : <nom epic [IA]> ([N2-…](https://neoteem.atlassian.net/browse/N2-…))
Source : <CDC §X> · Dépend de : <…> · Bloque : <…>

## 🎯 Objectif
<Le pourquoi — 2-3 phrases. Quel résultat global.>

## 💡 Contexte
<Ce qu'il faut savoir pour comprendre la story. Décisions actées pertinentes.>

## 📦 Périmètre (sous-tâches)
| # | Sous-tâche | Label | one-shot/réc. |
|---|------------|-------|---------------|
| US1 | … | setup | one-shot |

## 🔀 Dépendances & parallélisation
<OBLIGATOIRE — dit ce qui peut être développé en même temps. Format :
 séquence imposée (US1→US2…), groupes parallélisables (US5/US6/US7 en parallèle), clôture.
 Une sous-tâche est parallélisable si elle ne touche ni les mêmes packages ni les mêmes tables que l'autre.>

## 🚫 Hors-périmètre
<Ce qui n'est PAS dans la story — renvoie aux autres stories/epics.>

## ✅ Seuil de sortie (Definition of Done)
- [ ] <critère vérifiable 1 — commande/test qui prouve>
- [ ] <critère vérifiable 2>

## 🔒 Sécurité  (section omise si non pertinente)
<Points sécu gravés dès cette story.>

## 🧭 Méthode
<Étiquettes, BRIEF auto-suffisant, parent d'abord, organisation fichiers.>
```

---

## TEMPLATE SOUS-TÂCHE (US — BRIEF auto-suffisant pour Claude Code)

```markdown
# SOUS-TÂCHE — <US#> <Titre>

🏷️ IA-DEV · neoteem-back-ts · <label domaine> · <one-shot|récurrent>
↳ Story : <titre story parent>
🗂️ Repo cible : <repo où l'US s'implémente — neoteem-back-ts / neo_ia / lojii…>
🔀 Dépend de : <S# ou « aucune »> · Parallélisable avec : <S#/S# ou « aucune »>

## 🎯 Objectif
<Ce que la sous-tâche livre, du point de vue résultat.>

## ⚙️ Périmètre technique
<Fichiers/packages concernés, ce qu'on fait concrètement. Choix indicatifs — le dev reste maître.>

## 🔍 Recherche §0 (AVANT de coder)
<`use context7` sur : <technos concernées> → dernière version stable + API à jour.
 Consigne : jamais coder de mémoire.>

## 🚧 Frontières à respecter (CDC §16)
<Imports interdits, frontières hexagonales, conventions @neoteem/.>

## ✅ Critères de done — TDD (écrire les tests AVANT le code)
<Ces critères SONT des tests. Le test-writer les écrit d'abord (rouges) ; le dev code jusqu'au vert.
 Un seul endroit = pas de duplication entre « tests à écrire » et « done ».>
- [ ] **test** : <nom du test — ce qu'il vérifie, comment il prouve>
- [ ] **test** : <…>
- [ ] **vérif** : <commande qui prouve — ex. `turbo build` → exit 0>
- [ ] **mutation** : <si cœur métier touché, StrykerJS score relevé>

## 🌿 Branche / PR
Branche `<type>/<N°ticket>` (type : `bug` / `us` / `hotfix`) → PR vers **`develop`**.

## 📎 Références  (section omise si vide)
<Liens CDC (doc/), notes, tickets liés.>
```

---

## Rendu ADF / Jira (quand on pousse via MCP Atlassian)

- Chaque section = `heading` level 3 : émoji en texte normal + libellé en `textColor` **`#00b8d9`** + `:`.
- Séparateur `rule` entre sections. Listes = `bulletList`. Checklists → `taskList`/`taskItem` ADF.
- **La description ADF d'une STORY reprend TOUTES les sections du `.md` — dont 🔀 Dépendances & parallélisation** (étapes, US parallélisables, séquences) : visible d'un coup d'œil dans Jira sans ouvrir le `.md`. Jamais résumer au seul périmètre. Chaque US du périmètre = lien vers son ticket (N2-…).
- **La description ADF d'une SOUS-TÂCHE mentionne le 🗂️ Repo cible** (en en-tête, comme le `.md`) : un lecteur Jira sait dans quel repo l'US s'implémente sans deviner depuis les étiquettes. Feature multi-repo → préciser le repo cible PAR sous-tâche, jamais un repo global implicite.
- Encadré **choix techniques** (panel `warning` fond `#fffae6`) en fin de toute sous-tâche technique : « Les choix techniques sont indicatifs. Le développeur reste maître de son implémentation. »
- Style de référence Jira : ticket N2-98153 (structure ADF), N2-111159 (panel).
- Palette émoji : 🎯 Objectif · 💡 Contexte · ⚙️ Description/Périmètre · 🔍 Recherche · 🚧 Frontières · ✅ Critères/Tests · 🧪 Points d'attention · 🌿 Branche · 📎 Documents · 📦 Périmètre · 🚫 Hors-périmètre · 🔒 Sécurité · 🧭 Méthode · 🗂️ Repo cible.

## Décision de conception (9 juin 2026)
**Pas de section Tests séparée des critères de done.** Le test EST le critère de done — les fusionner en UNE section « ✅ Critères de done — TDD » évite la duplication et la désynchronisation. L'en-tête « écrire les tests AVANT » rend le TDD explicite pour le test-writer sans créer deux sources de vérité. Un agent lit un seul endroit pour savoir « qu'est-ce qui prouve que c'est fini ».
