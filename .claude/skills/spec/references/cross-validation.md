# Validation croisée — 3 checks pré-génération (Phase 5)

Obligatoires avant de générer le plan de vagues. Chaque check doit produire une **preuve citée** dans le plan. "Vérifié mentalement" ne compte pas.

---

## Check 1 — Compatibilité tool↔agent

Pour chaque CU qui enchaîne plusieurs tools :

1. Lire le config de l'agent recommandé (ex: `agents/universal/config.yaml`, `agents/X/config.yaml`)
2. Extraire la liste des tools déclarés
3. Comparer avec les tools requis par le CU

**Format de preuve dans le plan :**
```
Check compat — CU-2 (consulter_devis → envoyer_mail) :
- Agent recommandé : devis
- Tools de devis (config.yaml) : [consulter_devis, recherche_copro]
- envoyer_mail absent → devis NON compatible pour ce CU
- Alternative : agent X qui possède [consulter_devis + envoyer_mail]
```

---

## Check 2 — Existence et type des champs référencés

Pour chaque colonne citée dans un prompt CC :

1. Identifier la table source (via neo-brain-dev-ia ou Grep fichiers SQL)
2. Lire le DDL ou la fonction pour confirmer nom et type exacts
3. Vérifier le schéma côté backend (Drizzle, SQLAlchemy, Pydantic, etc.)
4. Noter si `UUID`, `TEXT`, `BOOLEAN`, tableau (`UUID[]`), etc.

**Méthode prioritaire** : `mcp__postgres__query` (source vivante) → Grep fichiers SQL en fallback.

**Cas courants à piéger :**
- Champ "auteur" → souvent `TEXT email`, pas `UUID acteur_id`
- Jointures documents/fichiers → souvent tableau UUID avec opérateur `&&`, pas FK simple
- Champ "assigné" → FK vers acteur ou email libre ?

**Format de preuve dans le plan :**
```
Check champs — filtre "créé par moi" :
- Colonne supposée : acteur_id
- Réel (devis.sql:L34) : devisdemande_user_ajout TEXT (email)
- Résolution dans le prompt CC : filtrer sur email, pas acteur_id
```

---

## Check 3 — Champs capturés par les clients API (côté LLM)

Applicable uniquement quand le service LLM consomme des champs du backend via un client.

1. Identifier le client API côté LLM (Glob pour trouver le fichier)
2. Vérifier que le champ est dans le mapping de réponse du client
3. Si absent → ajouter sous-tâche "étendre le client pour capturer X"

**Format de preuve dans le plan :**
```
Check client — champ acteur_key :
- Backend expose acteur_key (route.ts:L67)
- Client côté LLM : acteur_key absent du mapping (client.py:L112-L130)
- Sous-tâche ajoutée : Tâche 1.3 — Étendre le client pour capturer acteur_key
```

---

## Cas courants par domaine (Neoteem)

| Domaine | Piège connu |
|---------|------------|
| Devis/travaux | `devisdemande_user_ajout` = email TEXT, pas acteur_id |
| GED | Jointure devis↔documents via tableau UUID (`&&`) |
| Contacts | `f_get_contacts` filtre par copro_id — ne pas confondre avec acteur_id |
| Tâches | Table = `t_dossier_action`, pas `t_tache` |
| Schémas Drizzle | Vérifier `infra/db/schema/` — noms colonnes peuvent différer du PG |

---

## Cas réel — Ticket "Agent Devis" (2026-05-05)

- **Étape 2 sautée** → champ `tache_aid_assignee` inexistant, table `t_tache` au lieu de `t_dossier_action`.
- **Agent incompatible CU-2** (consulter_devis → envoyer_mail) → l'agent n'avait pas envoyer_mail.
- **`devisdemande_user_ajout` supposé = acteur_id** → c'est `email TEXT`. Fix : toujours vérifier via mcp__postgres__query.
- **GED↔devis via tableau UUID `&&`** → jointure non triviale sous-estimée. Documenter le pattern exact.
- **`acteur_key` dans backend mais non capturé par le client LLM** → tâche incomplète.
