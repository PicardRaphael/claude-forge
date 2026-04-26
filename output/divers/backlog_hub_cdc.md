# Product Backlog Intelligence Hub — Cahier des charges v2

---

## 1. Contexte

En tant qu'éditeur de logiciel chez Neoteem, tu reçois en permanence des demandes d'évolution provenant de sources multiples : tickets Jira (projets N2 et AML), mails, textes libres. Ces signaux sont épars, souvent redondants et difficiles à exploiter. Tu as besoin d'un outil qui structure ce flux, t'aide à prendre des décisions éclairées, génère des tickets N2 dans Jira de façon propre, et offre de la visibilité différenciée à ton équipe interne et à tes clients.

---

## 2. Flux complet

```
        SOURCES                  MOTEUR IA                    ACTIONS
┌─────────────────┐      ┌──────────────────────┐      ┌─────────────────────┐
│ Jira N2 (auto)  │      │ 1. Reformulation      │      │ Validation spec     │
│ Jira AML (auto) │ ───▶ │ 2. Dédoublonnage      │ ───▶ │ par Nils            │
│ Mail (collé)    │      │ 3. Classement         │      └──────────┬──────────┘
│ Texte libre     │      │ 4. Scoring pertinence │                 │
└─────────────────┘      │ 5. Proposition spec   │                 ▼
                         └──────────────────────┘      ┌─────────────────────┐
                                                        │ Création ticket N2  │
                                                        │ dans Jira           │
                                                        └──────────┬──────────┘
                                                                   │
                                                                   ▼
                                                        ┌─────────────────────┐
                                                        │ Interface statuts   │
                                                        │ Interne / Client    │
                                                        └─────────────────────┘
```

---

## 3. Ingestion des demandes

| Source | Mode | Traitement |
|---|---|---|
| Jira N2 | Synchronisation automatique | Lecture, dédoublonnage, normalisation |
| Jira AML | Synchronisation automatique | Lecture, dédoublonnage, normalisation |
| Mail | Copier-coller dans l'interface | Reformulation + classement par l'IA |
| Texte libre | Copier-coller dans l'interface | Reformulation + classement par l'IA |

---

## 4. Traitement par l'IA

Pour chaque demande ingérée, l'IA effectue les opérations suivantes dans l'ordre :

### 4.1 Reformulation
La demande brute est réécrite dans un langage clair, fonctionnel et homogène, indépendamment de la qualité du texte d'origine.

### 4.2 Dédoublonnage
L'IA vérifie si une demande similaire ou identique existe déjà dans la base. Si c'est le cas, elle y rattache la nouvelle occurrence plutôt que de créer une entrée supplémentaire. La fréquence de remontée est incrémentée.

### 4.3 Classement dans un regroupement fonctionnel
La demande est rattachée au regroupement de fonctionnalités le plus pertinent, issu de Jira comme base de départ. Si aucun regroupement existant ne convient, l'IA en suggère un nouveau, soumis à validation.

### 4.4 Scoring de pertinence
L'IA calcule un score basé sur :
- La fréquence à laquelle cette demande a été formulée (toutes sources confondues)
- Une proposition de classement soumise à validation
- Un ajustement manuel possible à tout moment

### 4.5 Proposition de spécification fonctionnelle
Lorsqu'une demande atteint un seuil de pertinence suffisant — ou à la demande de Nils — l'IA génère une proposition de spécification structurée :
- Description du besoin
- Comportement attendu
- Cas limites identifiés
- Critères d'acceptance suggérés
- Description publique (version client, anonymisée et simplifiée)

La spécification ne devient officielle qu'après validation explicite.

---

## 5. Génération du ticket Jira N2

Une fois la spécification validée, l'outil crée automatiquement un **ticket dans le projet N2 de Jira** avec les informations structurées issues de la spec. Les tickets AML restent en lecture seule : ils alimentent le hub mais ne sont pas créés depuis celui-ci.

Jira reste l'outil de suivi du développement pour les équipes dev. Le hub l'alimente proprement, sans remplacer son rôle opérationnel.

---

## 6. Regroupements fonctionnels

Les demandes sont organisées en regroupements de fonctionnalités (et non en epics Jira) :
- La **base de départ** est issue des epics existantes dans Jira
- L'IA peut **suggérer de nouveaux regroupements** si une demande ne correspond à aucun existant
- Nils **valide ou rejette** chaque suggestion de regroupement

---

## 7. Statuts des demandes

| Statut | Signification |
|---|---|
| 🟡 Remonté | Demande reçue, en cours d'analyse |
| 🔵 En cours de spécification | Demande pertinente, spec en cours |
| 🟣 Spécifié | Spec validée, ticket N2 Jira créé |
| 🟢 Planifié | Pris en charge dans une version |
| ✅ Livré | Fonctionnalité disponible |
| ⚫ Rejeté | Demande non retenue (motif facultatif) |

---

## 8. Visibilité client — Garde-fou éditorial

Chaque demande dispose d'un **interrupteur de visibilité indépendant du statut**, contrôlé manuellement.

### Règle par défaut
Toute demande est **masquée pour le client** jusqu'à activation explicite.

### Comportement

| Visibilité | Ce que le client voit |
|---|---|
| 🔴 Masqué (défaut) | La demande n'apparaît pas dans l'interface client |
| 🟢 Visible | Description publique + statut affichés |

### Règle automatique optionnelle
Il est possible de définir une règle automatique de passage en "Visible" à partir d'un certain statut (ex. : toute demande passant en "Planifié" devient automatiquement visible), avec possibilité de masquage manuel au cas par cas.

---

## 9. Profils d'accès

### 👤 Utilisateur client — Vue "Transparence"
Accès via un **extranet avec authentification login/mot de passe** (à construire).

Il voit :
- Toutes les demandes marquées "Visible", **anonymisées**
- Le statut de chaque demande
- Le regroupement fonctionnel associé
- La description publique (reformulée, sans jargon interne)

Il ne voit pas :
- L'identité des autres clients demandeurs
- Le score de priorité interne
- Les notes et commentaires internes
- Le détail de la spécification fonctionnelle
- Le lien vers le ticket Jira N2

### 🏢 Salarié interne — Vue "Pilotage"
Accès via authentification interne.

Il voit tout ce que voit le client, plus :
- L'identité des clients à l'origine des demandes
- Le score de priorité et son détail
- Les commentaires et notes internes
- Le détail complet de la spécification fonctionnelle
- Le lien vers le ticket Jira N2 associé
- Le contrôle de la visibilité client (interrupteur)

---

## 10. Ce que l'outil n'est pas (périmètre exclu)

- Il ne remplace pas Jira pour le suivi du développement : il l'**alimente proprement en créant des N2**
- Il ne gère pas les sprints ni les affectations développeurs
- Il ne crée pas de tickets AML : le projet AML est en lecture seule
- La communication client directe (email, notifications) n'est pas dans le périmètre initial

---

## 11. Valeur attendue

| Problème actuel | Solution apportée |
|---|---|
| Demandes éparpillées sur 3 canaux | Base unique et consolidée |
| Doublons dans N2 et AML | Dédoublonnage automatique |
| Spécifications rédigées manuellement | Proposition IA soumise à validation |
| Tickets N2 créés manuellement et de façon hétérogène | Génération automatique depuis la spec validée |
| Pas de visibilité sur l'état des demandes | Interface de statuts accessible selon le profil |
| Priorisation intuitive | Score basé sur la fréquence + ajustement manuel |
| Risque d'exposer des infos sensibles aux clients | Garde-fou éditorial avec visibilité par défaut masquée |
