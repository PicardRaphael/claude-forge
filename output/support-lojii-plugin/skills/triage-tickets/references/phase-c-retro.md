# Phase C — Rétrospective auto-correctrice

Référence complète de la Phase C. Appelée depuis le SKILL.md principal.

---

## PHASE C — Rétrospective auto-correctrice

Se déclenche **avant le batch** (Étape 0 dans les tâches planifiées). Compare les notes internes automatiques avec les réponses réelles des agents humains pour en déduire les erreurs et mettre à jour `learnings.md`.

La Phase C utilise `retro_done.txt` pour ne rétro-analyser chaque ticket qu'une seule fois. Un ticket est ajouté à la liste après analyse, qu'il y ait eu divergence ou non.

### Objectif

Boucle d'amélioration continue : chaque exécution corrige les erreurs passées AVANT de traiter de nouveaux tickets. La Phase C remplace la tâche autonome "feedback-sur-ses-propres-notes-internes" en l'intégrant directement au cycle de triage.

### Étape 1 — Récupérer les tickets à rétro-analyser

Lancer cette requête JQL :
```
project in (SC, SD)
AND status != "NOUVELLE CREATION" AND status != "Nouvelle création"
AND comment ~ "Classification" AND comment ~ "Vault neoteem-brain"
AND created >= -21d
ORDER BY created ASC
```

Lire `retro_done.txt` (même dossier que `learnings.md`). Ce fichier contient une clé de ticket par ligne (ex: `SC-98234`). Filtrer les tickets déjà listés. Si aucun ticket ne reste après filtrage → passer directement à la Phase A.

Si `retro_done.txt` n'existe pas → le créer vide et continuer (tous les tickets sont nouveaux).

Si 0 ticket retourné par JQL → passer directement à la Phase A. Pas de rétro à faire.

### Étape 2 — Pour chaque ticket, extraire

- **Ma classification** (Bug / Support / SR) depuis ma note interne (commentaire de "Service Clients Neoteem" contenant "Classification")
- **Ma recommandation** (escalade N2, réponse client suggérée, vérifications)
- **Le issuetype actuel** du ticket (ce que l'agent a mis)
- **Le statut actuel**
- **Les commentaires de l'agent humain** (tout commentaire qui n'est PAS de "Service Clients Neoteem") — distinguer :
  - Notes internes de l'agent (jsdPublic: false) = son analyse interne
  - Réponses au client (jsdPublic: true) = ce qu'il a réellement répondu
- **Les PJ ajoutées par l'agent** (captures d'écran de la résolution)

### Étape 3 — Analyser la réponse au client

Pour chaque ticket où l'agent a répondu :
- Quel diagnostic l'agent a-t-il communiqué ? (cause identifiée)
- Quelle solution concrète a-t-il proposée ? (chemin LOJII, manipulation, contournement)
- A-t-il demandé des informations complémentaires ? Lesquelles ?
- Le client a-t-il répondu après ? La réponse a-t-elle résolu le problème ou a-t-il fallu itérer ?

En déduire :
- La **vraie problématique** du ticket (pas ce que le client a décrit, mais ce que l'agent a identifié comme cause réelle)
- Le **type de résolution** adapté à cette famille de tickets (réponse directe, vérification config, escalade dev, intervention BDD)

### Étape 4 — Comparer ma note vs la réalité

- Ma classification correspond-elle au issuetype actuel ?
- Ma recommandation correspond-elle à ce que l'agent a réellement fait ?
- L'agent a-t-il trouvé une cause que je n'avais pas identifiée ?
- Ma "réponse client suggérée" était-elle pertinente par rapport à ce que l'agent a réellement envoyé ?
- Si l'agent a joint des captures d'écran, les lire (`get_attachment_content`) pour comprendre la résolution concrète

### Étape 5 — Capitaliser les apprentissages

Pour chaque erreur identifiée :
1. **`learnings.md`** — Append : `[date] | [ticket] | [Ma classe] → [Classe correcte] | [Pattern à retenir sous forme de RÈGLE] | COMMENT TROUVER SEUL : [mots-clés vault à utiliser, vérifications à faire dans LOJII, raisonnement à suivre]`
   - La RÈGLE doit être actionnable : "quand le client dit X, vérifier Y dans LOJII AVANT de conclure Z"
   - La colonne COMMENT TROUVER SEUL doit décrire le chemin de résolution : quels mots-clés chercher dans le vault, quelles vérifications faire dans LOJII, quel raisonnement suivre. C'est cette colonne qui permet à l'IA de reproduire le bon raisonnement, pas juste de connaître la réponse.
   - Si la réponse de l'agent contient un diagnostic ou une solution réutilisable → l'inclure comme modèle
2. **Mémoire Claude** — `memory_user_edits` avec le pattern condensé
3. **Vault neoteem-brain** (si pattern réutilisable non documenté) :
   - Résolution agent révèle un pattern LOJII non documenté → créer note FAQ `07-Support/faq/` via `neo-brain-support`
   - Captures d'écran montrent des chemins LOJII utiles → décrire les étapes dans la note vault
   - Réponse client type réutilisable → sauvegarder comme modèle dans la note vault
   - Si une note vault existait mais n'a pas été trouvée à cause de mots-clés manquants → ajouter les alias via `update_property` (propriété `aliases`) sur la note existante. Les alias doivent inclure les termes que le client utilise dans ses tickets (vocabulaire client ≠ vocabulaire technique).
   - Si la rétro révèle un vocabulaire client non couvert par le lexique → enrichir `lexique-expressions-clients.md` via `neo-brain-support` (`append_note`) avec la nouvelle expression client, ses variantes, le diagnostic réel, les vérifications à faire, et les tickets de référence. Format identique aux entrées existantes du lexique (tableau diagnostic + questions à poser + cas récurrents).
4. **`retro_done.txt`** — append la clé du ticket (ex: `SC-98234`) pour ne pas le rétro-analyser à nouveau lors des prochains runs.
5. **`UPDATE/retro-*.md`** — pour chaque divergence détectée, créer `UPDATE/retro-YYYY-MM-DD-TICKET.md` :
   - **Classification corrigée** : Claude [type initial] → Agent humain [type actuel]
   - **1. Pourquoi je me suis trompé** : mauvais mots-clés vault, symptôme mal interprété, contexte manquant...
   - **2. Ce qui m'aurait permis de trouver seul** : mots-clés alternatifs, note vault manquante, règle manquante...
   - **3. Cause racine de l'erreur** — identifier laquelle s'applique :
     - **Vault insuffisant** : note manquante, alias manquants, ou mauvais référencement → "si la note `[X]` avait eu les alias `[Y, Z]`, ma recherche aurait matché" / "si le vault avait une note sur `[sujet]`..."
     - **Mauvaise interprétation IA** : j'ai mal compris ce que le client décrivait (vocabulaire client ≠ vocabulaire technique, symptôme ambigu, contexte mal déduit) → "le client a dit `[termes]`, j'ai interprété `[X]` alors que ça signifiait `[Y]`". Noter le vocabulaire piège et la bonne interprétation pour learnings.md.
     - **Ticket trop vague** : le ticket ne contenait pas assez d'éléments pour classifier correctement (description d'une ligne, pas de capture, pas de contexte) → "le ticket disait seulement `[description]`, pas assez d'info pour trancher entre `[type A]` et `[type B]`". Signaler pour amélioration process (hors scope IA).
   - **4. Action corrective** : créer note vault, enrichir learnings.md, ajouter des alias vault sur les notes existantes (`update_property` aliases), proposer un modèle de rédaction de ticket...

### Étape 6 — Rapport de rétrospective

```
📊 Rétrospective — [date]
- Tickets analysés : [N]
- Classifications correctes : [N] ([X]%)
- Erreurs de classification : [N] ([X]%)
- Réponses client pertinentes vs hors sujet : [N]/[N]
- Tendance principale : [ex: sur-classification Bug → Support]

📝 Nouveaux apprentissages :
- [Pattern 1] (depuis [ticket])
- [Pattern 2] (depuis [ticket])

🧠 Vault enrichi : [N] notes créées/mises à jour
- Rétrospectives créées : [N] (dossier UPDATE/)

📋 Causes des erreurs :

🏷️ Vault — notes/alias à ajouter :
- `[note.md]` → aliases : [mot1], [mot2]
- Créer : `[nouvelle-note.md]` sur [sujet]

🤖 Mauvaise interprétation IA — vocabulaire piège :
- Client dit "[terme]" → signifie [diagnostic réel], pas [interprétation erronée]

📝 Tickets trop vagues (amélioration process) :
- [TICKET] : "[description]" — pas assez d'info pour trancher [type A] vs [type B]

📖 Lexique enrichi :
- Nouvelle expression : "[expression client]" → [diagnostic réel] (ajoutée au lexique)
- ...
Ou : Aucune nouvelle expression à ajouter.
```

Si aucune erreur détectée → rapport court "Rétrospective : [N] tickets analysés, 100% correct. Rien à corriger."
