# Templates Epic & Story — neoteem-back-ts

> Format validé avec Raphael (9 juin 2026). Mix **PO-Neoteem** (émojis + couleurs ADF) + **GitHub** (checklists). Destiné à un double lecteur : **humain** (lisible) + **Claude Code / agents** (BRIEF auto-suffisant). Source de vérité du format des tickets de ce projet.

## Règles d'or (héritées de la skill `spec` PO)

1. **Suivre le template à la lettre** : sections dans l'ordre, ne pas renommer.
2. **Omettre une section vide** : pas de titre vide, pas de « N/A », pas de placeholder.
3. **Omettre plutôt qu'inventer** : aucune règle métier / critère / contrainte non confirmé par le CDC, le code ou l'utilisateur.
4. **Story-dans-un-epic-existant AVANT epic neuf** : toute nouvelle feature se confronte d'abord aux epics existants (`doc/epics/e*/`) — si elle s'inscrit dans une brique en cours, proposer une story rattachée, pas un epic. Un epic ne se crée que pour une **nouvelle brique fonctionnelle large** (règle PO : « pas d'epics pour rien »).
5. **Epic = brique TOTALE** : il couvre le cycle complet jusqu'à la mise en service réelle — y compris les stories de coordination (bascule prod, décommissionnement de l'ancien système) dont l'exécution est devops mais le suivi vit dans l'epic. L'epic n'est clos que quand la brique rend son service en production (ex. E1 : « ia_back décommissionné », pas « un remplaçant existe »).

## Étiquettes (convention tous projets)
`IA-DEV` (systématique) + `neoteem-back-ts` (étiquette projet) + label de domaine (`setup`/`agent`/`db`/`migration`/`test`/`qualité`/`mcp`/`obs`) + label transverse (`one-shot`/`récurrent`).

---

## TEMPLATE EPIC (Markdown — produit en `.md`, créé dans Jira par un humain)

```markdown
# EPIC — <Titre lisible Jira>

🏷️ IA-DEV · neoteem-back-ts · <one-shot|récurrent>
Source : <CDC §X> · Dépend de : <…> · Bloque : <…>

## 🎯 Objectif
<Le pourquoi — 2-3 phrases. Quel résultat global.>

## 💡 Contexte
<Ce qu'il faut savoir pour comprendre l'epic. Décisions actées pertinentes.>

## 📦 Périmètre (stories)
| # | Story | Label | one-shot/réc. |
|---|-------|-------|---------------|
| S1 | … | setup | one-shot |

## 🔀 Dépendances & parallélisation
<OBLIGATOIRE — dit ce qui peut être développé en même temps. Format :
 séquence imposée (S1→S2…), groupes parallélisables (S5/S6/S7 en parallèle), clôture.
 Une story est parallélisable si elle ne touche ni les mêmes packages ni les mêmes tables que l'autre.>

## 🚫 Hors-périmètre
<Ce qui n'est PAS dans l'epic — renvoie aux autres epics.>

## ✅ Seuil de sortie (Definition of Done)
- [ ] <critère vérifiable 1 — commande/test qui prouve>
- [ ] <critère vérifiable 2>

## 🔒 Sécurité  (section omise si non pertinente)
<Points sécu gravés dès cet epic.>

## 🧭 Méthode
<Étiquettes, BRIEF auto-suffisant, parent d'abord, organisation fichiers.>
```

---

## TEMPLATE STORY / SOUS-TÂCHE (Markdown — BRIEF auto-suffisant pour Claude Code)

```markdown
# STORY — <S#> <Titre>

🏷️ IA-DEV · neoteem-back-ts · <label domaine> · <one-shot|récurrent>
↳ Epic : <titre epic parent>
🔀 Dépend de : <S# ou « aucune »> · Parallélisable avec : <S#/S# ou « aucune »>

## 🎯 Objectif
<Ce que la story livre, du point de vue résultat.>

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
Branche `<type>/<N°ticket>` (type : bug / user story / hotfix) → PR vers **`develop`**.

## 📎 Références  (section omise si vide)
<Liens CDC (doc/), notes, tickets liés.>
```

---

## Rendu ADF / Jira (quand on pousse via MCP Atlassian — non auth actuellement)

- Chaque section = `heading` level 3 : émoji en texte normal + libellé en `textColor` **`#00b8d9`** + `:`.
- Séparateur `rule` entre sections. Listes = `bulletList`. Checklists → `taskList`/`taskItem` ADF.
- Encadré **choix techniques** (panel `warning` fond `#fffae6`) en fin de toute sous-tâche technique : « Les choix techniques sont indicatifs. Le développeur reste maître de son implémentation. »
- Style de référence Jira : ticket N2-98153 (structure ADF), N2-111159 (panel).
- Palette émoji : 🎯 Objectif · 💡 Contexte · ⚙️ Description/Périmètre · 🔍 Recherche · 🚧 Frontières · ✅ Critères/Tests · 🧪 Points d'attention · 🌿 Branche · 📎 Documents · 📦 Périmètre · 🚫 Hors-périmètre · 🔒 Sécurité · 🧭 Méthode.

## Décision de conception (9 juin 2026)
**Pas de section Tests séparée des critères de done.** Le test EST le critère de done — les fusionner en UNE section « ✅ Critères de done — TDD » évite la duplication et la désynchronisation. L'en-tête « écrire les tests AVANT » rend le TDD explicite pour le test-writer sans créer deux sources de vérité. Un agent lit un seul endroit pour savoir « qu'est-ce qui prouve que c'est fini ».
