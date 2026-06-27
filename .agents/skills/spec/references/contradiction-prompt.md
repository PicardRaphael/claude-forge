# Contradiction Check — Prompt et Exemples

Prompt à exécuter quand plusieurs BRIEFs ont été générés (taille L ou XL).

---

## Prompt inline

```
Tu as généré plusieurs BRIEFs pour une même feature. Lis-les tous et identifie les contradictions.

Une contradiction = deux BRIEFs qui décrivent le même comportement de façon incompatible,
ou qui font des hypothèses contradictoires sur le contrat d'interface.

Pour chaque contradiction trouvée :
1. Cite la section du BRIEF A (ligne exacte ou reformulation)
2. Cite la section du BRIEF B (ligne exacte ou reformulation)
3. Explique pourquoi c'est contradictoire
4. Propose une résolution (quel BRIEF a raison, ou comment réconcilier)

Si aucune contradiction : écrire "Aucune contradiction détectée."
```

---

## Exemples de contradictions typiques (ia_back / neo_ia)

### Exemple 1 — Format de réponse API

**BRIEF-IA-BACK :** L'endpoint POST /messages retourne `{ id, content, createdAt }`.

**BRIEF-NEOIA :** Après appel ia_back, parser `message_id` depuis la réponse.

**Contradiction :** ia_back retourne `id`, neo_ia attend `message_id`. Tool cassé au premier appel.

**Résolution :** Aligner sur une convention (snake_case `message_id` ou camelCase `id`). Corriger les deux BRIEFs.

---

### Exemple 2 — Qui crée la ressource

**BRIEF-IA-BACK :** POST /conversations crée la conversation et retourne un `conversationId`.

**BRIEF-NEOIA :** Avant d'appeler ia_back, neo_ia crée une conversation via son ORM et passe son ID.

**Contradiction :** Doublon ou erreur FK. Source de vérité pour les IDs : toujours ia_back (ou le service de persistance).

**Résolution :** Le service LLM appelle le backend et utilise l'ID retourné.

---

### Exemple 3 — Pagination vs liste complète

**BRIEF-IA-BACK :** GET /documents retourne liste paginée `{ data, total, page, pageSize }`.

**BRIEF-NEOIA :** Au démarrage de session, récupérer TOUS les documents via GET /documents.

**Contradiction :** neo_ia suppose une liste complète, ia_back pagine. Données partielles silencieuses.

**Résolution :** Soit ia_back expose /documents/all, soit neo_ia implémente une boucle de pagination.

---

### Exemple 4 — Authentification

**BRIEF-IA-BACK :** Endpoint extrait userId depuis JWT middleware (déjà en place).

**BRIEF-NEOIA :** Passer userId dans le body payload.

**Contradiction :** ia_back ignore le userId du body. Erreur d'auth ou attribution incorrecte.

**Résolution :** Le service LLM passe le Bearer token dans le header Authorization, pas userId dans le body.

---

## Usage

Après génération de tous les BRIEFs (taille L ou XL) :

1. Soumettre le prompt avec le contenu de tous les BRIEFs en contexte
2. Si contradictions détectées → créer `TODO/feature-<nom>/CONTRADICTIONS.md`
3. Corriger les BRIEFs
4. Signaler : "X contradictions détectées et corrigées — voir CONTRADICTIONS.md"
