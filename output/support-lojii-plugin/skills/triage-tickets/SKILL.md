---
name: triage-tickets
description: 'Automatic triage of Neoteem SC/SD tickets in two modes. Batch mode classifies tickets (Bug/Support/Service Request) using neoteem-brain vault + Jira, posts internal notes, adds label. Review mode (/analyse) for interactive validation. Use PROACTIVELY when user says "lance le triage", "traite les tickets", or "/analyse". Composes with analyse-qualification-tickets for N2 qualification. Not for single ticket analysis or general questions.'
---

# Triage Automatique des Tickets Support

Deux modes : **batch** (traitement automatique J-2) et **`/analyse`** (revue interactive).

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

| Phase | Skill(s) à utiliser | Ce qu'on cherche |
|-------|---------------------|-----------------|
| Batch (classification) | **neo-brain** (dev) principal, **neo-brain-support** complément | Dev : bugs techniques connus dans le code/BDD. Support : problèmes connus documentés. Les deux aident à trancher Bug vs Support vs SR. |
| /analyse (Bug confirmé) | **neo-brain** (dev) | Contexte technique pour qualification N2, module, FRONT vs BACK |
| /analyse (Support) | **neo-brain-support** | Réponse prête dans 07-Support/, langage non-technique pour le client |
| /analyse (Service Request) | **neo-brain-support** | Procédure existante, faisabilité intervention |

**Le vault ne remplace PAS Jira.** Le vault donne le contexte et le diagnostic rapide. Jira donne les tickets réels et les actions (création N2, transitions, PJ). Workflow : vault d'abord → Jira ensuite.

**Règle lecture/écriture :**
- **Batch** = **lecture seule** du vault. Le batch pré-analyse, il ne valide pas. Pas d'écriture vault pendant le batch.
- **/analyse** = **lecture + écriture**. L'écriture vault (auto-enrichissement) se fait uniquement après validation par le support.

Si les skills brain ne sont pas disponibles → noter "Vault non consulté" dans le résumé du batch et continuer.

---

## Gotchas

Ajouter une ligne à chaque fois que Claude rate quelque chose.

- **Lire `learnings.md` avant de classifier** — les corrections passées sont là pour éviter de répéter les mêmes erreurs. Si un pattern similaire au ticket en cours est présent, l'appliquer directement.
- **Note interne — MCP JIRA `add_internal_note`** — Utiliser le tool MCP `add_internal_note` pour poster les notes internes sur les tickets SC/SD. Ne jamais utiliser `addCommentToJiraIssue` (MCP Atlassian) — il crée un commentaire public, pas une note interne. Ne jamais utiliser "Répondre au client".
- **Calcul J-2 ouvré** — Lundi→Jeudi (sem. précédente), Mardi→Vendredi (sem. précédente), Mercredi→Lundi, Jeudi→Mardi, Vendredi→Mercredi. Ne jamais compter samedi ni dimanche.
- **Complétion du batch** — Si J-2 donne moins de `tickets_par_jour`, compléter avec J-1, puis J. Ne jamais dépasser la limite configurée.
- **Filtre assigné** — Traiter uniquement les tickets assignés à Valéry MARTIROSYAN (accountId 5f74464dac3a2d006fd1ffd2). Ne jamais traiter un ticket assigné à quelqu'un d'autre.
- **Pas de N2 pendant le batch** — les N2 sont créés uniquement pendant `/analyse`, après confirmation explicite de l'utilisateur. Le batch classe et note, il n'agit pas.
- **Étiquette "À_valider" dans le champ Étiquettes** — conserver les étiquettes existantes du ticket lors de l'ajout. Ne pas écraser. Utiliser `editJiraIssue` en lisant d'abord les labels actuels.
- **Retirer l'étiquette "À_valider" après traitement** — dans `/analyse`, retirer "À_valider" du champ Étiquettes via `editJiraIssue` une fois le ticket traité, qu'il soit validé ou corrigé.
- **Service Request ambigu** — si la faisabilité de l'intervention directe est incertaine, classer SR avec la mention "Faisabilité à confirmer". L'utilisateur tranchera dans `/analyse`.
- **Google Drive MCP** — doit être connecté dans Cowork pour accéder à "02_clients partagés". Si non connecté, noter "Drive non consulté" dans le résumé du batch et continuer. Ne jamais bloquer le workflow pour ça.
- **Mémoriser les corrections** — après chaque reclassification dans `/analyse`, toujours mettre à jour `learnings.md` ET la mémoire Claude (`memory_user_edits`). Les deux canaux se complètent : le fichier persiste entre skill upgrades, la mémoire Claude est disponible immédiatement en contexte.
- **JQL labels EMPTY** — utiliser `(labels is EMPTY OR labels != "À_valider")` et NON `labels != "À_valider"`. En JQL, `labels != "X"` exclut silencieusement les tickets dont le champ labels est vide, ce qui fait rater tous les nouveaux tickets jamais étiquetés.
- **JQL assignee IN interdit** — `assignee in (liste)` retourne 0 résultat silencieusement sur accountIds hétérogènes (bug Jira). Toujours lancer des requêtes séparées par agent, en parallèle.
- **JQL casse status** — si 0 résultat avec `"NOUVELLE CREATION"`, retenter avec `"Nouvelle création"` (casse alternative).
- **URL nues dans les notes internes** — la syntaxe wiki `[TEXTE|URL]` et markdown `[TEXTE](URL)` s'affichent en texte brut non cliquable dans Jira Service Desk. Utiliser uniquement des URL complètes nues sur leur propre ligne — Jira auto-linkifie les URL nues.
- **issuetype + requestType + composant** — après classification, mettre à jour ces 3 champs via `editJiraIssue`. Voir `references/jira-field-mappings.md` pour les IDs.
- **createIssueLink INTERDIT en batch** — ne jamais créer de liens Jira automatiquement. L'agent N1 contrôle le N2 et lie manuellement après vérification. Mentionner le N2 dans la note interne avec l'URL nue.
- **Ne pas réaffecter** — conserver l'assigné actuel du ticket. Le batch ne touche pas à l'assignation.

---

## Sources de recherche — obligatoires pour tout type de ticket

Pour chaque ticket analysé (batch ET `/analyse`), consulter ces sources dans cet ordre. Ne pas se limiter à une seule source. Les combiner pour construire la réponse la plus complète possible.

| Priorité | Source | Quand |
|----------|--------|-------|
| 0 | **Vault neoteem-brain** | TOUJOURS — via `neo-brain-support` (FAQ, procédures, problèmes connus) + `neo-brain` dev (bugs techniques, modules). Si trouvé → utiliser pour la note. |
| 1 | **`learnings.md`** | TOUJOURS — patterns appris sur les vrais tickets. Complémentaire au vault. |
| 2 | **JQL — N2 en cours** | TOUJOURS — vérifier s'il existe un N2 non clôturé sur le même symptôme. Données temps réel que le vault n'a pas. |
| 3 | **JQL — SC/SD et N2 résolus** | FALLBACK — seulement si le vault n'a pas la réponse. Chercher dans SC ET SD. |
| 4 | **Google Drive — "02_clients partagés"** | OPTIONNEL — si MCP Google Drive connecté. Ne jamais bloquer si indisponible. |
| 5 | **Mémoire projet Cowork** | AUTOMATIQUE — contexte des sessions précédentes. |

Confluence supprimé — le vault neoteem-brain contient déjà ces connaissances.

---

## Classification

Ordre de priorité : vault neoteem-brain (problèmes connus, FAQ) → `learnings.md` (corrections passées) → définitions ci-dessous.

Si le vault contient une note `07-Support/problemes-connus/pb-*` qui correspond au symptôme → **Bug** quasi certain.
Si le vault contient une note `07-Support/faq/faq-*` qui répond à la question → **Support**.
Si le vault contient une note `07-Support/procedures/proc-*` décrivant l'action demandée → **Service Request**.

En l'absence de match vault et de pattern `learnings.md`, utiliser ces définitions :

**Bug** — LOJII se comporte anormalement. Erreur affichée, données incorrectes, fonctionnalité absente ou cassée, crash. Le logiciel ne fait pas ce qu'il est censé faire.

**Support** — Le client ne sait pas comment utiliser LOJII. Le logiciel fonctionne correctement. Question d'usage, demande d'explication, méconnaissance d'une fonctionnalité.

**Service Request** — Action à réaliser sur les données ou la configuration. Correction ponctuelle, extraction, paramétrage. Ni un bug, ni une question d'usage. Consulter `references/service-request-rules.md` pour déterminer si le support peut intervenir directement.

---

## PHASE A — Batch automatique

Se déclenche sur la tâche planifiée ou si l'utilisateur dit "lance le triage" / "traite les tickets du jour".

### Étape 1 — Charger la configuration et les apprentissages

Lire `config.json`. Lire `learnings.md`. Les patterns appris s'appliquent à toutes les classifications du batch.

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

**3b. Classifier** (Bug / Support / Service Request)
Appliquer `learnings.md` en premier. Identifier le type selon les définitions ci-dessus.

**3c. Consulter toutes les sources** (section "Sources de recherche" ci-dessus)
Recherches vault + Jira (N2 en cours) en parallèle, quel que soit le type de ticket. JQL SC/SD résolus en fallback si vault insuffisant.
**Vault** : utiliser le flux **ticket-triage** de neo-brain-support (2 recherches minimum avec termes alternatifs avant de conclure "Aucune note vault"). Le vault a 850+ notes — si 07-Support/ ne matche pas, 02-BDD/, 03-Apps/, Knowledge/ contiennent souvent l'info sous forme technique. Reformuler les notes techniques pour la note interne.

**3d. Mettre à jour les champs Jira** via `editJiraIssue` (voir `references/jira-field-mappings.md`) :
- `issuetype` selon la classification
- `customfield_10010` (requestType) selon projet SC ou SD
- `components` si incorrect par rapport au contenu du ticket
- `priority` → Highest si N2 BLOQUANT identifié

**3e. Rédiger et poster la note interne** via `add_internal_note` (MCP JIRA).
Ne jamais utiliser `addCommentToJiraIssue` (commentaire public).

Format de la note (URLs nues uniquement) :
```
[emoji] Classification : [Bug / Support / SR]
[Symptôme / Question / Nature] : [description courte]
Contexte pièces jointes : [1 ligne max]

🔍 Tickets similaires :
SC-XXXXX — [résumé court]
https://neoteem.atlassian.net/browse/SC-XXXXX
Ou : "Aucun ticket similaire trouvé."

🧠 Vault neoteem-brain :
[Notes utilisées pour le diagnostic — inclure notes techniques reformulées si pas de note 07-Support/]
Ou : "Aucune note vault sur ce sujet." (uniquement après 2+ recherches avec termes alternatifs)

⚡ Recommandation :
→ [N2 bloquant] 🔴 Priorité Highest appliquée. N2-XXXXX — à lier manuellement.
  https://neoteem.atlassian.net/browse/N2-XXXXX
→ [N2 non bloquant] N2-XXXXX identifié — à lier manuellement.
→ [Nouveau bug] Créer un N2 de type [BUG/BLOQUANT] sur module [nom].
→ [Pas nécessaire] Pas de N2 nécessaire à ce stade.

💬 Réponse client suggérée (Support uniquement) :
Bonjour,
[contenu vouvoiement]
Cordialement,
[Nom agent assigné au ticket]

🔧 Actions effectuées :
Type → [Bug / Support / SR]
Type de demande → [nom] [+ "⚠️ à corriger manuellement" si erreur read-only]
Composant → [nom]
Priorité → [Highest si N2 bloquant, sinon inchangée]
Lien N2 → à créer manuellement après contrôle
```

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
   - Append dans `learnings.md` : `[YYYY-MM-DD] | [SC-XXXXX] | [Classe Claude] → [Classe correcte] | [Pattern]`
   - Appeler `memory_user_edits` avec le pattern condensé : "Pour les tickets LOJII décrivant [pattern], classer [type] et non [type erroné]"

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

---

## Apprentissage — 3 couches de mémoire

Chaque ticket traité alimente **3 niveaux de mémoire** complémentaires :

| Quoi sauvegarder | Où | Comment |
|-----------------|-----|---------|
| Correction de classification (ticket X mal classé) | **`learnings.md`** | Append : `[date] | [ticket] | [erreur] → [correction] | [pattern]` |
| Nouveau problème connu, FAQ, procédure | **Vault neoteem-brain** | `create_note` ou `append_note` via neo-brain-support (uniquement en /analyse) |
| Préférences équipe, contexte implicite, habitudes | **Mémoire projet Cowork** | Se capitalise naturellement entre sessions |

**Règles :**
- Correction ponctuelle → `learnings.md` (immédiat, opérationnel)
- Savoir réutilisable par toute l'équipe → vault (permanent, structuré)
- Si un même symptôme revient 3+ fois sans note vault → créer la note `07-Support/problemes-connus/`
- Si le vault n'avait pas l'info → créer la note pendant /analyse
- Si une reclassification contredit le vault → corriger la note vault via `append_note`
