---
name: analyse-qualification-tickets
description: 'End-to-end analysis and qualification of Neoteem SC/SD support tickets. Use PROACTIVELY when a SC or SD ticket number is mentioned (SC-97184, SD-3525), when user asks how to respond to a client, or wants to know what to do with a ticket. Queries neoteem-brain vault for known issues and technical context. Not for general LOJII questions without a ticket number.'
---

# Analyse et Qualification des Tickets Support LOJII

Traitement end-to-end d'un ticket SC/SD : analyse fonctionnelle → réponse client → création N2 si escalade nécessaire.

---

## Configuration Jira

Voir `../triage-tickets/config.json` pour les parametres partages.

| Champ | Source |
|-------|--------|
| Cloud ID | Variable config ou env |
| Site | neoteem.atlassian.net |
| Projets support | SC (Syndic), SD (Gerance) |
| Projet dev | N2 (NEOTEEM) |
| Rapporteur | accountId dans config |

### Custom fields du Module N2 (parent)

| Champ Jira | Rôle | Utilisé pour |
|------------|------|--------------|
| customfield_10085 | PO Responsable | Intervention BDD |
| customfield_10081 | FRONT Dév Responsable | BUG/BLOQUANT front |
| customfield_10082 | BACK Dév Responsable | BUG/BLOQUANT back |

**Ne jamais utiliser l'assigné du Module** — ce n'est pas le bon responsable.

---

## Vault neoteem-brain — via skills brain

Ce skill s'appuie sur les **skills neoteem-brain** (installées séparément) pour accéder au vault. Ne pas réimplémenter l'accès vault — utiliser les skills telles quelles.

| Phase | Skill(s) à utiliser | Ce qu'on cherche |
|-------|---------------------|-----------------|
| Phase 1 — classification | **neo-brain** (dev) principal, **neo-brain-support** en complément | Dev : bugs techniques dans le code/BDD → aide à trancher Bug vs Support vs SR. Support : problèmes connus déjà documentés. |
| Phase 1 — réponse client (si Support) | **neo-brain-support** | FAQ, procédures reformulées en langage non-technique → réponse prête à copier-coller |
| Phase 2 — qualification N2 (si Bug) | **neo-brain** (dev) | Module technique, FRONT vs BACK, table PG, endpoint → aide à remplir le N2 |

**Le vault ne remplace PAS Jira.** Le vault donne le contexte et le diagnostic rapide. Jira donne les tickets réels, les actions (création N2, transitions, PJ, sprint IDs). Workflow : vault d'abord → Jira ensuite.

Si les skills brain ne sont pas disponibles dans la session → noter "Vault non consulté" et continuer en mode dégradé (Jira seul).

---

## Gotchas

Ajouter une ligne à chaque fois que Claude rate quelque chose.

- **Domaine ≠ symptôme** : deux tickets sur le même écran (ex: Gmail) peuvent être des bugs distincts. Ne citer un ticket similaire que si le symptôme exact correspond — pas juste le domaine fonctionnel.
- **Chercher dans SC ET SD** quel que soit le projet du ticket analysé. Un même bug remonte dans les deux projets.
- **N2 existant sur le même symptôme** : ne jamais créer de doublon. Indiquer la clé N2 existante à lier et appliquer le RACCOURCI.
- **Root cause transverse** : identifier le déclencheur du problème (relance, AG, sinistre…), pas l'écran où il apparaît. En cas de doute, choisir l'écran visible pour l'utilisateur.
- **Affectation N2** : lire les custom fields du Module parent uniquement. Ne jamais lire l'assigné du Module.
- **OCR — compte 401** : la case "Lettré" se coche automatiquement si équilibré. Ne JAMAIS cocher manuellement — génère des factures parasites.
- **Sprint BLOQUANT** : toujours le sprint en cours. Les BUG ne vont jamais dans le sprint en cours.
- **Version corrigée** : toujours la même version que le sprint cible. Vérifier sur un ticket N2 existant du sprint pour trouver le nom exact — ne pas inventer.
- **Demande d'évolution hors sujet** : si la demande d'évolution ne correspond pas au sujet du ticket SC/SD, demander au client d'ouvrir un nouveau ticket.
- **Transition D.O.R.** : créer le ticket N2 puis appeler `getTransitionsForJiraIssue` pour trouver l'ID de transition "D.O.R." avant d'appeler `transitionJiraIssue`. Exception : Intervention BDD → statut "À spécifier".
- **Sprint ID et fixVersion ID** : ces champs requièrent des IDs numériques. Les récupérer en lisant un ticket N2 existant dans le sprint cible (champs `sprint` et `fixVersions`).
- **Correspondance sprint ↔ version** : Kanban 2.15 → Version 2.15, Kanban 2.16 → Version 2.16, etc. Toujours aligner.
- **Type de lien SC/SD ↔ N2** : toujours "Relates" (relates to). Ne jamais utiliser "is caused by" ou autre.
- **Copie des PJ** : toujours copier les pièces jointes du SC/SD vers le N2 via `copy_attachments` juste après la création.
- **Description N2** : reprendre la description du ticket SC/SD source à l'identique dans le N2.
- **Commentaire N2** : résumer tous les commentaires du SC/SD sur le N2 pour que le dev ait le contexte complet sans ouvrir le ticket support.
- **Validation obligatoire** : toujours présenter la fiche N2 complète et attendre la confirmation de Valéry avant de créer.

---

## RACCOURCI — N2 en cours sur le même symptôme

Si lors de l'étape 2, un N2 **non clôturé** est trouvé **sur exactement le même symptôme** ET que d'autres SC/SD y sont déjà rattachés → ne pas dérouler les vérifications LOJII ni créer de N2.

Produire directement :
1. Diagnostic court (problème + lien avec la vague en cours)
2. Réponse client prête à envoyer
3. Clé N2 existante à lier (afficher : clé, résumé, statut, assigné)

---

## PHASE 1 — Analyse fonctionnelle

### Étape 1 — Récupérer le ticket

Appeler `getJiraIssue` avec les champs : `summary, description, status, issuetype, priority, created, issuelinks, comment, assignee, attachment`.

Identifier : client, symptôme exact, pièces jointes, commentaires existants, N2 déjà liés.

Si le ticket a des captures d'écran ou des vidéos → utiliser `get_attachment_content` (MCP JIRA) pour lire les PJ et affiner le diagnostic. Les images aident souvent à trancher entre Bug et Support.

### Étape 1bis — Vérifier la qualité de la demande

Avant toute analyse, vérifier la présence de :
- Symptôme clairement décrit (message d'erreur, crash, données incorrectes, comportement inattendu)
- Exemple concret (N° copropriété, nom d'acteur, date, N° de lot…)
- Capture d'écran exploitable si le problème est visuel

Si un ou plusieurs éléments manquent → rédiger directement la réponse client demandant les précisions. Ne pas lancer les vérifications LOJII ni la qualification N2. Indiquer clairement à l'utilisateur ce qui manque.

### Étape 2 — Rechercher dans toutes les sources (en parallèle)

Consulter ces sources pour chaque ticket, quel que soit le type identifié :

1. **Vault neoteem-brain** (PRIORITAIRE) — via skills `neo-brain-support` + `neo-brain` (dev). Rechercher FAQ, procédures, problèmes connus, contexte technique. Si une note couvre le symptôme → l'utiliser directement pour le diagnostic et la réponse client.
2. **`learnings.md` du skill `triage-tickets`** — patterns de classification appris sur les vrais tickets.
3. **JQL — N2 en cours même symptôme** (TOUJOURS) — `references/jql-queries.md`. Vérifier s'il existe un N2 non clôturé sur le même problème. Données temps réel, le vault ne les a pas.
4. **JQL — Tickets SC/SD et N2 résolus** (FALLBACK — seulement si le vault n'a pas la réponse) — chercher dans SC ET SD quel que soit le projet du ticket analysé.
5. **Google Drive "02_clients partagés"** — via MCP Google Drive (doit être connecté). Si non disponible, le noter et continuer.

Si un N2 en cours sur le même symptôme est trouvé → appliquer le RACCOURCI.

### Étape 3 — Déterminer la voie de traitement (Bug vs Fonctionnel)

⚠️ **RÈGLE DE DÉCISION OBLIGATOIRE** — Avant de produire la synthèse, appliquer cette logique en 3 voies :

**VOIE A — Bug certain** : Les recherches montrent clairement un bug technique (messages d'erreur, crashs, données corrompues, comportement reproductible par d'autres clients). Ne PAS proposer de vérifications fonctionnelles ni de piste "comportement normal". Aller droit au but.
- **A1 — Avec N2 en cours** : un N2 non clôturé existe sur le même symptôme → diagnostic, lien vers le N2 existant, réponse client. Passer directement à la Phase 2 (liaison N2).
- **A2 — Sans N2 mais avec précédents** : pas de N2 en cours, mais des tickets SC/SD résolus ou des N2 clôturés existent sur le même symptôme → exploiter ces précédents pour proposer une solution ou un contournement connu. Indiquer la solution trouvée dans les anciens tickets (qui a répondu quoi, quelle correction a été apportée). Si le bug a été corrigé par le passé mais revient → signaler la régression et proposer la création d'un nouveau N2 en Phase 2.
- **A3 — Sans N2 et sans précédent** : bug nouveau jamais vu → diagnostic, proposer la création d'un N2 en Phase 2, réponse client informant que c'est remonté à l'équipe technique.

**VOIE B — Purement fonctionnel avec réponse connue** : Le vault neoteem-brain (`07-Support/`) ou les tickets résolus permettent de répondre avec certitude que c'est un comportement normal, une méconnaissance du logiciel ou une procédure documentée → donner **directement la réponse** avec les sources (note vault, tickets résolus). Ne PAS demander de vérifications dans LOJII. Ne PAS proposer de piste bug. Fournir l'explication claire + la réponse client prête à envoyer. Ne PAS passer en Phase 2.

**VOIE C — Doute entre bug et fonctionnel** : Les recherches ne permettent pas de trancher avec certitude → proposer **les deux pistes** côte à côte :
- **Piste Bug** : pourquoi ça pourrait être un bug (symptômes suspects, tickets similaires non résolus, absence de N2 connu) + vérifications à faire pour confirmer + qualification N2 provisoire
- **Piste Fonctionnel** : pourquoi ça pourrait être un comportement normal ou une méconnaissance (documentation existante, procédure connue) + réponse client si c'est le cas
- Indiquer clairement quelle vérification permettrait de trancher entre les deux pistes.

### Étape 3bis — Produire la fiche selon la voie retenue

1. **Diagnostic** : indiquer la voie retenue (A, B ou C) et pourquoi. Si voie C, présenter les deux pistes.

2. **Vérifications LOJII** :
   - Voie A1 : aucune vérification (bug confirmé, N2 en cours)
   - Voie A2 : aucune vérification si la solution des précédents est directement applicable. Sinon, vérifications minimales pour confirmer que le même correctif s'applique.
   - Voie A3 : vérifications pour reproduire/confirmer le bug (étapes de reproduction précises pour le N2)
   - Voie B : aucune vérification (réponse fonctionnelle connue avec sources)
   - Voie C : uniquement les vérifications qui permettent de trancher entre bug et fonctionnel. Chemin de navigation précis (Damier > Module > Sous-module), écrans et champs à contrôler.

3. **Réponse client** selon la voie :
   - Voie A1 → informer que c'est un problème identifié, remonté à l'équipe technique, en cours de traitement (ton professionnel, vouvoiement, formule de politesse, signature Valéry MARTIROSYAN)
   - Voie A2 → fournir la solution/contournement trouvé dans les précédents + informer si un N2 est créé pour régression (ton professionnel, vouvoiement, formule de politesse, signature Valéry MARTIROSYAN)
   - Voie A3 → informer que c'est un nouveau bug remonté à l'équipe technique (ton professionnel, vouvoiement, formule de politesse, signature Valéry MARTIROSYAN)
   - Voie B → réponse explicative prête à copier-coller avec sources et procédure (ton professionnel, vouvoiement, formule de politesse, signature Valéry MARTIROSYAN)
   - Voie C → rédiger deux versions de réponse (une si bug confirmé, une si fonctionnel) OU poser les questions qui permettent de trancher
   - Infos manquantes → questions précises à poser

4. **Alerte vault manquant** : si aucune note vault sur un sujet récurrent, signaler et proposer de créer la note pendant `/analyse`. Format :
   ```
   📝 Sujet non couvert par le vault :
   Aucune note trouvée sur [sujet]. Ce sujet revient dans les tickets (ex: SC-XXXXX).
   → Créer : 07-Support/[faq|proc|pb]-[sujet].md
   ```

---

## PHASE 2 — Qualification et création du ticket N2

Appliquer si le problème ne peut pas être résolu au niveau support.

### Étape 4 — Contexte technique vault + déterminer le type de ticket

Avant de classifier, interroger le vault **perspective dev** via skill `neo-brain` pour le contexte technique :
- Le module technique concerné (table PG, fonction, endpoint)
- Des bugs connus côté code sur le même sujet
- L'architecture du composant (FRONT vs BACK)

Ce contexte technique aide à : classifier BLOQUANT vs BUG, déterminer FRONT vs BACK, trouver le bon Module parent N2.

⚠️ **Lire `references/charte-qualification.md` pour les règles complètes.**

Résumé rapide :
- **BLOQUANT** → activité impossible + pas de contournement viable → Sprint en cours
- **BUG** → Highest (N+1) / Medium (N+2) / Lowest (N+3) — JAMAIS sprint en cours
- **Intervention BDD** → Sprint en cours, PO Responsable, statut À spécifier
- **Doute BLOQUANT/BUG** → BUG par défaut + arbitrage Chef Produit
- **Demande d'évolution** → vérifier si N2 ou AML

### Étape 5 — Récupérer sprint ID et fixVersion ID

Ne pas inventer ces valeurs — les récupérer depuis les tickets existants.

Sprint en cours et sprints futurs : requêtes dans `references/jql-queries.md`.

Pour chaque sprint cible, lire un ticket N2 existant de ce sprint pour obtenir :
- L'ID numérique du sprint (champ `sprint`)
- L'ID et le nom de la fixVersion (champ `fixVersions`)

### Étape 6 — Trouver le Module parent et le responsable

D'abord chercher le module dans le vault via skill `neo-brain` (plus rapide que JQL). Les notes `03-Apps/` contiennent souvent le mapping domaine → module N2.

Si le vault ne donne pas le module, chercher via JQL (requête dans `references/jql-queries.md`).

Récupérer les custom fields du Module via `getJiraIssue` :
```
fields: ["summary", "customfield_10081", "customfield_10082", "customfield_10085"]
```

**Déterminer FRONT ou BACK** à partir du symptôme décrit :
- FRONT (customfield_10081) : affichage, interface, bouton, rendu visuel, formulaire, navigation, champs non affichés correctement
- BACK (customfield_10082) : calcul, données incorrectes, traitement métier, API, synchronisation, BDD, export/import, génération de documents, envoi d'emails
- En cas de doute : indiquer les deux responsables et expliquer pourquoi le doute existe

**Pour Intervention BDD** : toujours affecter au PO Responsable (customfield_10085).

### Étape 7 — Présenter la qualification et demander confirmation

Présenter la fiche de sortie complète (voir section suivante). **TOUJOURS demander confirmation à Valéry avant de créer le ticket dans Jira.** Ne jamais créer le N2 sans validation explicite.

La fiche doit montrer exactement ce qui sera créé : titre, type, parent, assigné, sprint, version corrigée, priorité, statut initial — pour que Valéry puisse valider ou corriger avant exécution.

### Étape 8 — Créer le ticket N2 (après confirmation de Valéry)

#### 8.1 — Déterminer le sprint cible et la version corrigée

**Règle sprint/version** :
- **BLOQUANT sans contournement possible** → Sprint en cours (Kanban 2.15 actuellement)
- **BUG Highest** → Sprint N+1
- **BUG Medium** → Sprint N+2
- **BUG Lowest** → Sprint N+3
- **Intervention BDD** → Sprint en cours autorisé

**Correspondance sprint ↔ version corrigée** : le numéro de version suit le sprint.
- Sprint Kanban 2.15 → fixVersion = Version 2.15
- Sprint Kanban 2.16 → fixVersion = Version 2.16
- Sprint Kanban 2.17 → fixVersion = Version 2.17
- Et ainsi de suite.

Récupérer les IDs numériques du sprint et de la fixVersion depuis un ticket N2 existant dans le sprint cible (champs `sprint` et `fixVersions`). Ne jamais inventer ces valeurs.

#### 8.2 — Créer le ticket N2

Appeler `createJiraIssue` avec :

```json
{
  "project": "N2",
  "summary": "[Env] [Client] - [SC-XXXXX ou SD-XXXXX] - [Description courte]",
  "description": "[Copie intégrale de la description du ticket SC/SD source]",
  "issuetype": "BLOQUANT | BUG | Intervention BDD | Story",
  "priority": "Highest | Medium | Lowest",
  "parent": "N2-XXXXX",
  "assignee": { "accountId": "[accountId récupéré depuis le Module parent — FRONT ou BACK ou PO selon la charte]" },
  "reporter": { "accountId": "5f74464dac3a2d006fd1ffd2" },
  "customfield_10020": { "id": "[sprint ID numérique]" },
  "fixVersions": [{ "id": "[fixVersion ID correspondant au sprint]" }]
}
```

⚠️ La description du N2 doit reprendre le contenu du ticket SC/SD source à l'identique.

#### 8.3 — Copier les pièces jointes

Immédiatement après la création du N2, copier toutes les PJ du ticket source :
```
copy_attachments(source_issue: "SC-XXXXX", target_issue: "N2-XXXXX")
```

#### 8.4 — Lier les tickets (relates to)

Créer le lien entre le N2 et le ticket SC/SD source avec le type **"relates to"** (Relates) :
```
createIssueLink(type: "Relates", inwardIssue: "N2-XXXXX", outwardIssue: "SC-XXXXX")
```

⚠️ Toujours utiliser "Relates" (relates to), pas "is caused by" ni autre type de lien.

#### 8.5 — Ajouter le commentaire résumé sur le N2

Appeler `addCommentToJiraIssue` sur le ticket **N2** (pas sur le SC/SD) avec un résumé structuré des commentaires du ticket SC/SD source. Le développeur doit comprendre le contexte sans avoir à ouvrir le ticket support.

Format du commentaire N2 :
```
🔍 Résumé du ticket support [SC/SD-XXXXX]

📝 Contexte :
[Résumé clair du problème remonté par le client]

💬 Historique des échanges (SC/SD) :
- [Date] — [Auteur] : [Résumé du commentaire]
- [Date] — [Auteur] : [Résumé du commentaire]
...

🔁 Étapes de reproduction :
1. [Étape concrète]
2. [Étape concrète]
...

📊 Impact :
- Nombre de clients impactés : [si connu]
- Contournement : [oui/non — description si oui]
- Tickets similaires : [SC-XXXXX, SD-XXXXX si trouvés]
```

#### 8.6 — Transitionner le N2 vers le bon statut

**Par défaut → D.O.R.** :
1. `getTransitionsForJiraIssue` → identifier l'ID de la transition "D.O.R."
2. `transitionJiraIssue` → passer le ticket en D.O.R.

**Exceptions selon la charte** :
- **Intervention BDD** → statut **À spécifier**
- Autre cas particulier identifié pendant l'analyse → appliquer le statut approprié et justifier

#### 8.7 — Note interne sur le ticket SC/SD source

Poster la note interne via MCP JIRA :
```
add_internal_note(issue_key: "SC-XXXXX", body: "[message d'information]")
```
Ne jamais utiliser `addCommentToJiraIssue` (commentaire public) ni "Répondre au client".

Si BLOQUANT : rappeler les règles d'escalade (relance dev à 24h si pas EN COURS, escalade PO à 48h).

---

## Fiche de sortie

```
📋 ANALYSE DU TICKET [SC/SD-XXXXX]

🔍 Diagnostic :
- Client : [nom]
- Problème : [résumé clair du symptôme]
- Voie retenue : [A1 — Bug + N2 en cours / A2 — Bug + précédents connus / A3 — Bug nouveau / B — Fonctionnel connu / C — Doute bug/fonctionnel]
- Nature : [bug / comportement normal / méconnaissance / demande d'évolution]
- Tickets similaires : [SC-XXXXX, N2-XXXXX — ou "aucun"]
- Sources : [notes vault utilisées, tickets résolus si fallback utilisé]

🔧 Vérifications à faire dans LOJII :
[Voie A1] Aucune — bug confirmé, N2 en cours.
[Voie A2] Aucune ou minimales — solution/contournement trouvé dans les précédents : [tickets sources, solution appliquée]
[Voie A3] Étapes de reproduction : [étapes précises pour confirmer et documenter le bug]
[Voie B] Aucune — réponse fonctionnelle connue (voir sources ci-dessus).
[Voie C]
  🐛 Piste Bug : [vérifications pour confirmer le bug]
  📘 Piste Fonctionnel : [vérifications pour confirmer le comportement normal]
  ➡️ Ce qui permet de trancher : [vérification décisive]

💬 Réponse client :
[Voie A1] > [Réponse bug confirmé, en cours de traitement — prêt à copier-coller]
[Voie A2] > [Solution/contournement issu des précédents + info régression si applicable — prêt à copier-coller]
[Voie A3] > [Bug nouveau remonté à l'équipe technique — prêt à copier-coller]
[Voie B] > [Réponse fonctionnelle avec explication et sources — prêt à copier-coller]
[Voie C] > Version bug : [réponse si bug confirmé]
         > Version fonctionnel : [réponse si comportement normal]

📖 Documentation :
- [Notes vault utilisées, ou "Sujet non couvert — à créer"]

---

🔗 N2 existant à lier :
→ [Si trouvé] N2-XXXXX — "[résumé]" — Statut : [statut] — Assigné : [nom]
   ➡️ Lier ce N2 au ticket SC/SD — ne pas créer de doublon.
→ [Si aucun] Aucun N2 en cours. Qualification proposée ci-dessous.

📌 Qualification N2 :
- Type : [BLOQUANT / BUG / Intervention BDD]
- Titre suggéré : "[Env] [Client] - SC-XXXXX - [Description courte]"
- Description : [copie intégrale de la description SC/SD]
- Parent (Module) : [N2-XXXXX — Nom du module]
- Affecter à : [Prénom NOM — rôle FRONT/BACK/PO — source: customfield_100XX du Module parent]
- Priorité : [Highest / Medium / Lowest]
- Sprint cible : [Kanban X.XX]
- Version corrigée : [Version X.XX — alignée sur le sprint]
- Statut initial : [D.O.R. / À spécifier — selon la charte]
- Lien : relates to → [SC/SD-XXXXX]
- PJ : copie des pièces jointes du SC/SD

💬 Commentaire N2 (résumé des échanges SC/SD) :
> [Résumé structuré des commentaires du ticket source pour le dev]

💡 Justification : [Pourquoi ce type, cette priorité, ce parent, ce responsable, FRONT vs BACK]

⏱️ Priorité support :
- Traitement : [haute / moyenne / basse]
- Délai réponse client : [dans la journée / sous 24h / sous 48h / sous 1 semaine]
- Temps estimé : [X min]
- Urgence sans contournement ? [oui → sprint en cours / non → sprint N+X]
```

---

## Références

| Fichier | Quand le consulter |
|---------|-------------------|
| `references/charte-qualification.md` | Charte V1 — règles BLOQUANT/BUG/Intervention BDD, priorisation, escalade |
| `references/jql-queries.md` | Requêtes JQL (N2 en cours, SC/SD résolus en fallback, sprints, modules) |
| Vault `07-Support/` | Navigation LOJII, prerequis, procedures — via skills neoteem-brain |

### MCP utilisés

| MCP | Tools utilisés | Usage |
|-----|---------------|-------|
| **MCP JIRA - NEOTEEM** | `add_internal_note`, `copy_attachments`, `get_attachment_content`, `set_reporter` | Notes internes, copie PJ, lecture PJ, rapporteur |
| **MCP Atlassian** | `getJiraIssue`, `createJiraIssue`, `editJiraIssue`, `createIssueLink`, `addCommentToJiraIssue`, `getTransitionsForJiraIssue`, `transitionJiraIssue`, `searchJiraIssuesUsingJql` | CRUD tickets, liens, transitions, recherche JQL |
| **MCP obsidian-brain** | `search_brain`, `read_note`, `create_note`, `append_note`, `update_property` | Vault neoteem-brain (lecture + écriture) |

---

## Apprentissage — 3 couches de mémoire

| Quoi sauvegarder | Où | Comment |
|-----------------|-----|---------|
| Qualification réussie grâce au vault (pattern efficace) | **Mémoire projet Cowork** | Se capitalise naturellement |
| Sujet non couvert par le vault | **Vault neoteem-brain** | `create_note` via neo-brain-support (FAQ, procédure, problème connu) |
| Réponse vault incomplète ou incorrecte | **Vault neoteem-brain** | `append_note` pour corriger/enrichir |
| Contexte technique utile pour FRONT vs BACK | **Vault neoteem-brain** | `create_note` dans `Knowledge/` via neo-brain dev |
| Préférences Valéry, habitudes de qualification | **Mémoire projet Cowork** | Se capitalise naturellement |
