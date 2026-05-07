---
name: triage-tickets
description: 'Automatic triage of Neoteem SC/SD tickets in two modes. Batch mode classifies tickets (Bug/Support/Service Request) using neoteem-brain vault + Jira, posts internal notes, adds label. Review mode (/analyse) for interactive validation. Use PROACTIVELY when user says "lance le triage", "traite les tickets", or "/analyse". Composes with analyse-qualification-tickets for N2 qualification. Not for single ticket analysis or general questions.'
---

# Triage Automatique des Tickets Support

Trois phases : **Phase A** (batch automatique), **Phase C** (rétrospective auto-correctrice), **Phase B** (`/analyse` interactif).

Lire `config.json` et `learnings.md` avant toute action.

---

## Configuration

`config.json` est la seule chose à modifier pour ajuster le comportement. Il peut être placé dans un dossier partagé (OneDrive, Drive) et symlinké par chaque membre de l'équipe pour partager les mêmes paramètres.

| Paramètre | Rôle |
|-----------|------|
| `tickets_par_jour` | Nombre max de tickets par batch (défaut : 15) |
| `statuts_cibles` | Statuts Jira éligibles au triage |
| `label_a_ajouter` | Label posé sur chaque ticket traité |
| `date_recherche_support` | Date de début pour la recherche de tickets Support similaires |

---

## Vault neoteem-brain — via skills brain

Ce skill s'appuie sur les **skills neoteem-brain** (installées séparément) pour accéder au vault.

| Phase | Skill(s) | Ce qu'on cherche |
|-------|----------|-----------------|
| Batch | `neo-brain` (dev) + `neo-brain-support` | Bugs techniques + problèmes connus pour trancher Bug/Support/SR |
| Phase C | `neo-brain-support` | Enrichir vault si pattern non documenté |
| /analyse Bug | `neo-brain` (dev) | Contexte technique, module, FRONT/BACK |
| /analyse Support/SR | `neo-brain-support` | FAQ, procédures, langage non-technique |

Vault d'abord → Jira ensuite. Batch = lecture seule. Phase C et /analyse = lecture + écriture (écriture après validation support).
Si skills brain indisponibles → noter "Vault non consulté" et continuer.

---

## Gotchas

Ajouter une ligne à chaque fois que Claude rate quelque chose.

- **Lire `learnings.md` avant de classifier** — appliquer les corrections passées directement. Utiliser la colonne COMMENT TROUVER SEUL (mots-clés vault, vérifications LOJII, raisonnement).
- **Note interne — MCP JIRA `add_internal_note`** — Utiliser le tool MCP `add_internal_note` pour poster les notes internes sur les tickets SC/SD. Ne jamais utiliser `addCommentToJiraIssue` (MCP Atlassian) — il crée un commentaire public, pas une note interne. Ne jamais utiliser "Répondre au client".
- **Français correct avec accents — OBLIGATOIRE** — Toutes les notes internes, réponses client suggérées, et commentaires Jira doivent être rédigés en français correct avec tous les accents (é, è, ê, à, ù, ç, etc.). Ne jamais écrire en ASCII sans accents. Jira gère parfaitement l'UTF-8. Cela s'applique aussi aux résumés de batch, rapports de rétrospective, et toute communication visible par l'équipe.
- **Calcul J-2 ouvré** — Lundi→Jeudi (sem. précédente), Mardi→Vendredi (sem. précédente), Mercredi→Lundi, Jeudi→Mardi, Vendredi→Mercredi. Ne jamais compter samedi ni dimanche.
- **Complétion du batch** — Si J-2 donne moins de `tickets_par_jour`, compléter avec J-1, puis J. Ne jamais dépasser la limite configurée.
- **Filtre assigné** — Traiter uniquement les tickets assignés à Valéry MARTIROSYAN (accountId 5f74464dac3a2d006fd1ffd2). Ne jamais traiter un ticket assigné à quelqu'un d'autre.
- **Pas de N2 pendant le batch** — les N2 sont créés uniquement pendant `/analyse`, après confirmation explicite de l'utilisateur. Le batch classe et note, il n'agit pas.
- **Étiquette "À_valider" dans le champ Étiquettes** — conserver les étiquettes existantes du ticket lors de l'ajout. Ne pas écraser. Utiliser `editJiraIssue` en lisant d'abord les labels actuels.
- **Retirer l'étiquette "À_valider" après traitement** — dans `/analyse`, retirer "À_valider" du champ Étiquettes via `editJiraIssue` une fois le ticket traité, qu'il soit validé ou corrigé.
- **Service Request ambigu** — si la faisabilité de l'intervention directe est incertaine, classer SR avec la mention "Faisabilité à confirmer". L'utilisateur tranchera dans `/analyse`.
- **Google Drive MCP** — doit être connecté dans Cowork pour accéder à "02_clients partagés". Si non connecté, noter "Drive non consulté" dans le résumé du batch et continuer. Ne jamais bloquer le workflow pour ça.
- **Mémoriser les corrections** — après chaque reclassification dans `/analyse`, mettre à jour `learnings.md` ET `memory_user_edits`. Le fichier persiste entre skill upgrades, la mémoire Claude est disponible immédiatement.
- **JQL labels EMPTY** — utiliser `(labels is EMPTY OR labels != "À_valider")` et NON `labels != "À_valider"`. En JQL, `labels != "X"` exclut silencieusement les tickets dont le champ labels est vide, ce qui fait rater tous les nouveaux tickets jamais étiquetés.
- **JQL assignee IN interdit** — `assignee in (liste)` retourne 0 résultat silencieusement sur accountIds hétérogènes (bug Jira). Toujours lancer des requêtes séparées par agent, en parallèle.
- **JQL casse status** — si 0 résultat avec `"NOUVELLE CREATION"`, retenter avec `"Nouvelle création"` (casse alternative).
- **URL nues dans les notes internes** — pas de `[TEXTE|URL]` ni `[TEXTE](URL)` dans Jira SD. Utiliser uniquement des URL nues sur leur propre ligne (Jira auto-linkifie).
- **Pas de formatage dans les notes internes** — Jira SD ignore gras/souligné/italique (wiki et markdown). Texte brut + emojis + tirets + sauts de ligne uniquement.
- **issuetype + requestType + composant** — après classification, mettre à jour ces 3 champs via `editJiraIssue`. Voir `references/jira-field-mappings.md` pour les IDs.
- **createIssueLink INTERDIT en batch** — ne jamais créer de liens Jira automatiquement. L'agent N1 contrôle le N2 et lie manuellement après vérification. Mentionner le N2 dans la note interne avec l'URL nue.
- **Ne pas réaffecter** — conserver l'assigné actuel du ticket. Le batch ne touche pas à l'assignation.
- **Étapes de vérification OBLIGATOIRES dans chaque note** — chaque note interne DOIT contenir une section "📋 Étapes de vérification / actions dans LOJII" avec des étapes concrètes, numérotées, spécifiques au ticket. Bug : étapes de reproduction. Support : vérifications config/état. SR : étapes d'intervention. Jamais générique.
- **Message d'erreur descriptif ≠ Bug** — "Ce numéro existe déjà", "doublon", "format invalide" sont des gardes métier applicatives, pas des bugs. Vérifier dans LOJII si le message dit vrai avant de classifier Bug. Voir section Classification ci-dessous pour les règles complètes.
- **Charger le lexique AVANT de classifier** — à l'étape 3a-bis, charger uniquement `lexique-expressions-clients.md` + `glossaire-support.md` via read_note (PAS de recherche vault). La recherche vault générale c'est en 3c, pas ici. Le lexique traduit les expressions client en termes techniques pour guider les recherches vault de 3c.
- **`retro_done.txt` anti-doublon** — les tickets déjà rétro-analysés sont listés dans `retro_done.txt` (un par ligne). Ne jamais les re-traiter. Si le fichier n'existe pas, le créer vide.
- **Rétrospective obligatoire après correction** — après chaque reclassification dans `/analyse`, créer un fichier `UPDATE/retro-*.md` en plus de la ligne `learnings.md`. Ne jamais sauter cette étape.

---

## Sources de recherche — obligatoires pour tout type de ticket

Pour chaque ticket analysé (batch ET `/analyse`), consulter ces sources dans cet ordre. Ne pas se limiter à une seule source. Les combiner pour construire la réponse la plus complète possible.

| Priorité | Source | Quand |
|----------|--------|-------|
| 0 | **Vault neoteem-brain** | TOUJOURS — via `neo-brain-support` (FAQ, procédures, problèmes connus) + `neo-brain` dev (bugs techniques, modules). Si trouvé → utiliser pour la note. |
| 0.5 | **Lexique + glossaire** | TOUJOURS en 3a-bis — `lexique-expressions-clients.md` + `glossaire-support.md` via read_note directe. PAS de recherche vault. |
| 1 | **`learnings.md`** | TOUJOURS — patterns appris sur les vrais tickets. Complémentaire au vault. |
| 2 | **JQL — N2 en cours** | TOUJOURS — vérifier s'il existe un N2 non clôturé sur le même symptôme. Données temps réel que le vault n'a pas. |
| 3 | **JQL — SC/SD et N2 résolus** | FALLBACK — seulement si le vault n'a pas la réponse. Chercher dans SC ET SD. |
| 4 | **Google Drive — "02_clients partagés"** | OPTIONNEL — si MCP Google Drive connecté. Ne jamais bloquer si indisponible. |
| 5 | **Mémoire projet Cowork** | AUTOMATIQUE — contexte des sessions précédentes. |


---

## Classification

Ordre de priorité : vault neoteem-brain (problèmes connus, FAQ) → `learnings.md` (corrections passées) → définitions ci-dessous.

Note `07-Support/problemes-connus/pb-*` → Bug. Note `07-Support/faq/faq-*` → Support. Note `07-Support/procedures/proc-*` → SR. Sinon :

**Bug** — LOJII se comporte anormalement : erreur technique (crash, HTTP 500, données corrompues, écran blanc) → Bug probable. Erreur applicative descriptive ("existe déjà", "doublon") → vérifier d'abord dans LOJII si le message dit vrai. Si oui = garde métier = **Support**. Si non = Bug potentiel.

**Support** — Le client ne sait pas comment utiliser LOJII. Le logiciel fonctionne correctement. Question d'usage, demande d'explication, méconnaissance d'une fonctionnalité. Inclut les cas où un message d'erreur applicatif est correct et le client a fait une erreur de saisie.

**Service Request** — Action à réaliser sur les données ou la configuration. Correction ponctuelle, extraction, paramétrage. Ni un bug, ni une question d'usage. Consulter `references/service-request-rules.md` pour déterminer si le support peut intervenir directement.

---

## PHASE A — Batch automatique

Se déclenche sur la tâche planifiée ou si l'utilisateur dit "lance le triage" / "traite les tickets du jour".

### Étape 1 — Charger la configuration et les apprentissages

Lire `config.json`. Lire `learnings.md` — retenir aussi la colonne COMMENT TROUVER SEUL (mots-clés vault, vérifications LOJII, raisonnement correct). Les patterns s'appliquent à toutes les classifications du batch.

### Étape 2 — Calculer la date J-2 ouvré et récupérer les tickets

Calculer la date J-2 selon le tableau des gotchas. Lancer la requête JQL :

```
project in (SC, SD)
AND status in ("Nouvelle création", "En attente de neoteem", "Retour dev")
AND assignee = "5f74464dac3a2d006fd1ffd2"
AND created >= "J-2 00:00" AND created <= "J-2 23:59"
ORDER BY created ASC
```

Si résultats < `tickets_par_jour` → relancer avec la plage J-1, puis J jusqu'à atteindre la limite. Stopper à `tickets_par_jour` tickets au total.

### Étape 3 — Traiter chaque ticket

Pour chaque ticket :

**3a. Lire le ticket**
`getJiraIssue` avec champs : `summary, description, status, issuetype, priority, created, comment, attachment, labels`

**3a-bis. Comprendre — traduire le vocabulaire client**

Charger ces **2 fichiers uniquement** via `neo-brain-support` (read_note, PAS de recherche vault générale) :
1. `07-Support/lexique-expressions-clients.md` — mapping expressions client → diagnostics
2. `07-Support/glossaire-support.md` — termes métier LOJII, définitions, chemins navigation

Pour chaque expression du client dans le ticket :
1. Chercher une correspondance dans le lexique (expression exacte ou variante)
2. Si trouvée → extraire le diagnostic probable, les vérifications à faire, les notes vault liées
3. Si pas trouvée → noter l'expression comme candidat enrichissement lexique

Produire une **compréhension structurée** avant de classifier :
- **Expressions client identifiées** : [termes client] → [diagnostic technique via lexique]
- **Module probable** : [déduit du lexique ou du contexte]
- **Confiance** : haute (lexique matche) / moyenne (lexique partiel) / faible (ticket vague, aucun match)
- **Mots-clés techniques pour recherche vault** : [termes techniques à utiliser en 3c]

Si confiance = faible → mentionner dans la note interne (Recommandation : "ticket vague, classification incertaine").
Cette étape ne modifie pas le ticket Jira — c'est une traduction interne pour guider la classification et les recherches.

**3b. Classifier** (Bug / Support / Service Request)
Appliquer `learnings.md` en premier. Identifier le type selon les définitions ci-dessus.

**3c. Consulter toutes les sources** (section "Sources de recherche" ci-dessus)
**Utiliser les mots-clés techniques identifiés en 3a-bis** pour les recherches vault au lieu des termes bruts du client. Si 3a-bis a produit "facture existe déjà → garde métier applicative, module Comptabilité", chercher "garde métier" et "comptabilité facturation" dans le vault, pas "erreur facture".
Recherches vault + Jira (N2 en cours) en parallèle, quel que soit le type de ticket. JQL SC/SD résolus en fallback si vault insuffisant.
**Vault** : utiliser le flux **ticket-triage** de neo-brain-support (2 recherches minimum avec termes alternatifs avant de conclure "Aucune note vault"). Le vault a 850+ notes — si 07-Support/ ne matche pas, 02-BDD/, 03-Apps/, Knowledge/ contiennent souvent l'info sous forme technique. Reformuler les notes techniques pour la note interne.

**3d. Mettre à jour les champs Jira** via `editJiraIssue` (voir `references/jira-field-mappings.md`) :
- `issuetype` selon la classification
- `customfield_10010` (requestType) selon projet SC ou SD
- `components` si incorrect par rapport au contenu du ticket
- `priority` → Highest si N2 BLOQUANT identifié

**3e. Rédiger et poster la note interne** via `add_internal_note` (MCP JIRA).
Ne jamais utiliser `addCommentToJiraIssue` (commentaire public).

Format de la note interne — titres en gras Unicode, séparateurs entre sections, URLs nues uniquement :
```
🔍 𝗧𝗶𝗰𝗸𝗲𝘁𝘀 𝘀𝗶𝗺𝗶𝗹𝗮𝗶𝗿𝗲𝘀

SC-XXXXX — [résumé court]
https://neoteem.atlassian.net/browse/SC-XXXXX
Ou : Aucun ticket N2 similaire trouvé en cours sur ce sujet.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚫ 𝗖𝗹𝗮𝘀𝘀𝗶𝗳𝗶𝗰𝗮𝘁𝗶𝗼𝗻 : [Bug / Support / SR] ([précision courte])

Symptôme : [description du problème rapporté par le client, contexte, bases concernées, PJ disponibles]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟠 𝗩𝗲́𝗿𝗶𝗳𝗶𝗰𝗮𝘁𝗶𝗼𝗻𝘀 𝗮̀ 𝗳𝗮𝗶𝗿𝗲 𝗽𝗼𝘂𝗿 𝗰𝗼𝗻𝗳𝗶𝗿𝗺𝗲𝗿 𝘀𝗶 𝗰'𝗲𝘀𝘁 𝘂𝗻 [𝗕𝗨𝗚/𝗦𝘂𝗽𝗽𝗼𝗿𝘁/𝗦𝗥] ?

1. [étape concrète spécifique au ticket]
2. [étape concrète spécifique au ticket]
3. [etc.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ 𝗥𝗲𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝗮𝘁𝗶𝗼𝗻 :

[Diagnostic et recommandation : N2 bloquant/non bloquant, escalade, vérification config, etc.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 𝗥𝗲́𝗽𝗼𝗻𝘀𝗲 𝗰𝗹𝗶𝗲𝗻𝘁 𝘀𝗲𝗹𝗼𝗻 𝗺𝗮 𝗿𝗲𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝗮𝘁𝗶𝗼𝗻 :

Bonjour,

[Texte concis — accusé de réception du problème, diagnostic simplifié, prochaines étapes. Vouvoiement.]

Bien à vous,

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙ 𝗔𝗰𝘁𝗶𝗼𝗻𝘀 𝗲𝗳𝗳𝗲𝗰𝘁𝘂𝗲́𝗲𝘀 :

Type → [Bug / Support / SR] ([conservé/modifié]) – Type de demande → [nom] ([ID]) – Composant → [nom] ([conservé/modifié]) – Priorité → [niveau]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 𝗩𝗮𝘂𝗹𝘁 𝗻𝗲𝗼𝘁𝗲𝗲𝗺-𝗯𝗿𝗮𝗶𝗻 :

[Notes vault utilisées pour le diagnostic — reformulées si techniques. Ou : Aucune note vault sur ce sujet (après 2+ recherches avec termes alternatifs).]
```

**Règles de mise en page des notes internes :**
- Titres en **gras Unicode mathématique** (𝗔𝗕𝗖) — Jira affiche ces caractères en gras sans formatage wiki. Utiliser la table de conversion : A→𝗔, B→𝗕, C→𝗖, etc. Les accents fonctionnent dans le texte normal mais PAS dans les caractères gras Unicode.
- **Séparateurs** ━━━ (U+2501 BOX DRAWINGS HEAVY HORIZONTAL) entre chaque section — 30 caractères par ligne.
- **Emojis** en début de chaque titre de section.
- **Sauts de ligne** : une ligne vide après chaque titre, une ligne vide avant chaque séparateur.
- **Pas de formatage wiki/markdown** — pas de `*gras*`, `_italique_`, `+souligné+`. Jira Service Desk les ignore dans les notes internes.
- La section "Réponse client selon ma recommandation" doit toujours commencer par "Bonjour," et finir par "Bien à vous," — texte concis entre les deux.

**3f. Ajouter l'étiquette "À_valider" dans le champ Étiquettes**
Lire les étiquettes existantes du ticket. Ajouter "À_valider" dans le champ Étiquettes sans supprimer les autres.
`editJiraIssue` avec le champ `labels` mis à jour (Étiquettes).

### Étape 4 — Résumé du batch

```
✅ Triage terminé — [N] tickets traités

📊 Répartition :
- Bugs : [N]
- Support : [N]
- Service Requests : [N]

🧠 Vault neoteem-brain :
- Tickets informés par le vault : [N]/[total] ([%])
- Notes vault utilisées : [liste courte]
- Sujets non couverts par le vault : [liste — candidats enrichissement]

📝 Notes internes : [Jira OK / Fallback .docx — raison]

Tickets traités :
- SC-XXX — [titre court] — [type] — [vault: oui/non]
- ...

→ Tape /analyse pour démarrer la session de revue.
```

---

## PHASE C — Rétrospective auto-correctrice

Se déclenche **avant le batch** (Étape 0 dans les tâches planifiées). Compare les notes IA avec les actions réelles des agents humains.

**→ Lire `references/phase-c-retro.md` pour le détail complet des étapes C1 à C6.**

Résumé : JQL tickets traités → filtrer via `retro_done.txt` → comparer note IA vs actions humaines → si divergence : créer `UPDATE/retro-*.md` + enrichir learnings.md (avec COMMENT TROUVER SEUL) + enrichir vault/lexique si pattern réutilisable → rapport avec causes (vault, interprétation IA, ticket vague) + alias à ajouter + vocabulaire piège + lexique enrichi.

---

## PHASE B — Session interactive `/analyse`

Se déclenche quand l'utilisateur tape `/analyse`.

### Étape 1 — Récupérer les tickets avec l'étiquette "À_valider"

```
project in (SC, SD) AND labels = "À_valider" AND assignee = "5f74464dac3a2d006fd1ffd2" ORDER BY created ASC
```

Annoncer : "X tickets avec l'étiquette À_valider. On commence ?"

### Étape 2 — Présenter chaque ticket

Pour chaque ticket, afficher :

```
📋 [SC/SD-XXXXX] — [Titre]
Client : [nom] | Statut : [statut] | Créé le : [date]

🤖 Mon analyse :
J'ai vu : [éléments qui ont guidé la classification]
→ Type identifié : [Bug / Support / Service Request]
[Résumé de la note posée]

✅ C'est correct ?
```

Attendre la réponse avant d'agir.

### Étape 3a — Validation (oui)

**Bug**
Proposer la création d'un N2. Utiliser le skill `analyse-qualification-tickets` pour la qualification complète (type BLOQUANT/BUG, priorité, sprint, responsable FRONT/BACK, Module parent). Avant de créer, ajouter une note interne sur le ticket SC/SD avec la réponse client type (problème identifié, transmission à l'équipe technique, formule de politesse, vouvoiement).

**Support**
1. Chercher dans les tickets résolus (depuis `date_recherche_support` de config.json) :
   `project in (SC, SD) AND status in ("Résolu", "Fermé", "CLOTURE") AND created >= "[date]" AND text ~ "[mots-clés]"`
2. Si réponse trouvée → proposer la réponse client prête à envoyer (adapter au contexte, ne pas copier-coller brut)
3. Sinon → rechercher dans les tickets SC/SD résolus via JQL (fallback)
4. Si réponse trouvée → proposer réponse + source
5. Sinon → proposer des questions de clarification à poser au client

**Service Request**
Consulter `references/service-request-rules.md`.
- Intervention directe possible → proposer les étapes précises dans LOJII
- N2 Intervention BDD nécessaire → proposer création N2 (PO Responsable du Module, sprint en cours, statut D.O.R.)
- Faisabilité incertaine → demander à l'utilisateur de trancher

Dans tous les cas : retirer "À_valider" du champ Étiquettes du ticket après action.

**Auto-enrichissement vault (uniquement en /analyse, JAMAIS en batch)** — après chaque ticket validé par le support :
- Si le vault n'avait PAS de note sur ce problème et qu'on a trouvé la réponse → créer la note via `neo-brain-support` (Bug → `pb-*`, Support → `faq-*`, SR → `proc-*`)
- Si le vault avait une note incomplète → enrichir via `append_note`
- Fonctionne en **CLI et MCP** (écriture disponible dans les deux modes depuis MCP v1.1.0)
- Cet enrichissement est la boucle vertueuse : chaque ticket traité rend le vault plus complet pour les suivants.

### Étape 3b — Correction (non / je corrige)

1. Demander : "Quelle est la bonne classification ?"
2. Demander : "Qu'est-ce qui t'a guidé ?" (pour capturer le pattern correct)
3. Agir selon le bon type (étape 3a)
4. **Mettre à jour la mémoire** :
   - Append dans `learnings.md` : `[YYYY-MM-DD] | [SC-XXXXX] | [Classe Claude] → [Classe correcte] | [Pattern] | COMMENT TROUVER SEUL : [mots-clés vault à utiliser, vérifications à faire dans LOJII, raisonnement à suivre]`
   - Appeler `memory_user_edits` avec le pattern condensé : "Pour les tickets LOJII décrivant [pattern], classer [type] et non [type erroné]"
5. **Rétrospective** — créer `UPDATE/retro-YYYY-MM-DD-TICKET.md` :
   - Pourquoi je me suis trompé
   - Comment j'aurais pu trouver seul
   - Cause racine (vault insuffisant / mauvaise interprétation IA / ticket trop vague)
   - Action corrective (créer note vault, ajouter alias vault, enrichir learnings.md avec vocabulaire piège)

### Étape 4 — Récapitulatif de session

```
📊 Session /analyse terminée
- Traités : [N] tickets
- Validés sans correction : [N]
- Reclassifiés : [N] (learnings mis à jour)
- N2 créés : [N]
- Réponses rédigées : [N]
- Interventions directes : [N]

🧠 Vault neoteem-brain :
- Notes vault créées/enrichies : [N] (boucle vertueuse)
- Sujets manquants signalés : [liste]
```

---

## Références

| Fichier | Quand le consulter |
|---------|-------------------|
| `config.json` | Au démarrage de chaque batch et /analyse |
| `learnings.md` | Avant toute classification |
| `references/service-request-rules.md` | Pour tout ticket Service Request |
| `references/jira-field-mappings.md` | IDs issuetype, requestType, composants par projet SC/SD |
| Skill `analyse-qualification-tickets` | Pour la qualification complète d'un N2 |
| Skill `neo-brain-support` | Vault neoteem-brain perspective support (FAQ, procédures, problèmes connus) |
| Skill `neo-brain` (dev) | Vault neoteem-brain perspective dev (contexte technique, modules, FRONT/BACK) |
| `retro_done.txt` | Liste des tickets déjà rétro-analysés (anti-doublon Phase C) |
| `references/phase-c-retro.md` | Phase C complète — rétrospective auto-correctrice (6 étapes) |
| `lexique-expressions-clients.md` | Mapping expressions client → diagnostics techniques (via vault neo-brain-support) |
| `UPDATE/` | Rétrospectives post-correction — analyse des erreurs de classification |

---

## Apprentissage — 5 couches de mémoire

Chaque ticket traité alimente **5 niveaux de mémoire** complémentaires :

| Quoi sauvegarder | Où | Comment |
|-----------------|-----|---------|
| Correction de classification (ticket X mal classé) | **`learnings.md`** | Append : `[date] | [ticket] | [erreur] → [correction] | [pattern] | COMMENT TROUVER SEUL : [mots-clés vault, vérifications LOJII, raisonnement]` |
| Auto-correction rétrospective (Phase C) | **`learnings.md`** + **mémoire Claude** | La Phase C compare notes auto vs réponses agents et capitalise les écarts |
| Nouveau problème connu, FAQ, procédure | **Vault neoteem-brain** | `create_note` ou `append_note` via neo-brain-support (en /analyse et Phase C) |
| Préférences équipe, contexte implicite, habitudes | **Mémoire projet Cowork** | Se capitalise naturellement entre sessions |
| Rétrospective structurée (pourquoi l'erreur, comment l'éviter) | **`UPDATE/retro-*.md`** | Créer fichier après correction en /analyse OU divergence détectée en Phase C |

**Règles :** correction ponctuelle → `learnings.md`. Savoir réutilisable → vault. 3+ tickets mêmes symptômes sans note vault → créer `07-Support/problemes-connus/`.
