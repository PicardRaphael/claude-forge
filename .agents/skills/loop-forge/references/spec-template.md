# Template — SPEC-loop-`<nom>`.md

Remplacer tous les `<...>` par les réponses collectées. Champ non renseigné = `"à confirmer"`.

---

```markdown
---
feature: loop-<nom>
date_spec: <YYYY-MM-DD>
type: loop-<code|hors-code>
statut: draft
---

# SPEC loop — <nom lisible>

> Généré par /loop-forge. Conception uniquement — la création des composants est une étape séparée.

## 0. Contexte

**Orga / domaine :** <qui, quel contexte métier>
**Objectif business :** <le POURQUOI — problème résolu, valeur créée>
**Branche :** code | hors-code
**Environnement :** <repo(s) ou contexte(s)>

---

## 1. Job

**Description reformulée :** "Depuis [source], [action], jusqu'à [fin]."

- **Fréquence actuelle (manuelle) :** <N fois/semaine ou N fois/mois>
- **Coût/temps actuel :** <durée par exécution, effort humain>
- **ROI attendu de l'automatisation :** <estimation gain>

---

## 2. Type de loop

**Type retenu :** inner-loop | time-loop | goal-loop

- **Justification :** <pourquoi ce type>
- **Critère de terminaison nominal (succès) :** <condition>
- **Critère de terminaison exceptionnel :** <timeout | N itérations max | erreur fatale | kill-switch>

---

## 3. Périmètre

### Périmètre d'écriture (où le loop écrit)

- **Repo d'écriture (unique) :** <nom du repo>
- **Repos en lecture croisée :** <liste ou "aucun">
- **Pattern multi-repo si applicable :** fleet-parallèle | manager+workers | N/A

### Périmètre de traitement (sur quoi le loop opère)

- **Objets traités :** <fichiers/dossiers, sources de données, entités — ex: `.claude/skills/` + `.claude/agents/`>
- **Même que le repo d'écriture ?** oui | non — <si non, préciser la différence>
- **Filtre / bornage :** <extension, label, statut, date, ou "aucun">

> Le repo d'écriture (où le loop écrit) peut différer des objets traités (sur quoi il travaille).

<!-- === BRANCHE CODE === -->
### Stack / Implémentation _(code)_

- **Langage / runtime :** <Python | Bun | Bash | autre> _(pré-rempli depuis analyse repo Bloc 0)_
- **Outils CLI requis :** <liste>
- **APIs / services externes :** <liste avec auth method>
- **Path dans le repo :** <ex: scripts/loops/mon-loop.py>

### Inputs / Outputs _(code)_

| Direction | Source/Dest | Format | Volume estimé |
|-----------|-------------|--------|---------------|
| Input     | <source>    | <fmt>  | <N/unit>      |
| Output    | <dest>      | <fmt>  | <N/unit>      |

### Gestion d'erreur _(code)_

- **Retry policy :** <N tentatives, délai exponentiel/fixe>
- **Erreurs fatales (arrêt loop) :** <liste>
- **Erreurs non-fatales (log + continue) :** <liste>
- **Dead letter / items échoués :** <où / comment>
- **Verrou concurrence :** OUI — <mécanisme> | NON

<!-- === BRANCHE HORS-CODE === -->
### Acteurs / Canaux _(hors-code)_

| Rôle | Qui | Canal de travail | Canal de notif |
|------|-----|-----------------|----------------|
| <rôle> | <qui> | <outil> | <canal> |

- **Sync ou async :** <sync | async>
- **Contrainte fuseau :** <si applicable>

### Artefacts / Livrables _(hors-code)_

- **Input de chaque itération :** <document, état, information>
- **Livrable attendu :** <note, rapport, ticket, décision>
- **Template du livrable :** <path ou description>
- **Stockage :** <vault, dossier partagé, wiki>
- **Durée de conservation :** <7j, 30j, indéfini>

### Validation qualité _(hors-code)_

- **Critère de qualité :** <checklist, score, validation pair>
- **Reviewer :** <qui valide>
- **Seuil d'acceptation :** <description>
- **Feedback loop si insuffisant :** <recommencer, corriger, escalader>

---

## 4. Les 4 briques

| Brique | Description |
|--------|-------------|
| **Déclencheur** | <cron / webhook / événement fichier / commande manuelle / commit / fin d'une tâche> |
| **Source(s)** | <d'où viennent les données ou artefacts à traiter> |
| **Critère de jugement** | <comment le loop sait qu'une itération est réussie ou non> |
| **Action** | <ce que le loop fait concrètement sur chaque item> |

### Idempotence & état _(code ET hors-code)_

- **Si même item traité 2× :** <marqueur "déjà traité" / clé d'idempotence / label sur source / dédoublonnage>
- **Si interruption mid-batch :** <état persistant / checkpoint / journal des items traités>

---

## 5. Vérification

**Méthode retenue :** <description de la méthode choisie>

Exemples selon type :
- inner-loop : tests unitaires / typecheck / dry-run avec diff visible
- time-loop : agent de vérification séparé / rapport diff itération N vs N-1
- goal-loop : condition de succès mesurable et auto-vérifiable
- hors-code : relecture croisée / critère mesurable (score, checklist, approbation)

---

## 6. Infra

**Option retenue :** machine locale | serveur H24 | Claude Desktop scheduled

- **Détails :** <OS, scheduler, fréquence cron si applicable>
- **Incompatibilités signalées :** <ex: loop autonome + machine locale = risque extinction>

---

## 7. Garde-fous (obligatoires)

| Garde-fou | Décision |
|-----------|----------|
| Validation humaine | <fréquence : chaque itération / par batch N / par exception> |
| Cap coût / itération | <N itérations max | N tokens/appels API max par cycle> |
| Log / trace | <mécanisme + stockage logs + notification échec (canal + destinataires)> |
| Kill-switch | <comment interrompre immédiatement : fichier flag / env var / commande / autre> |

---

## 8. Composants à créer (HORS SCOPE de /loop-forge)

> Créer ces composants depuis la session principale après validation de cette spec.

| Composant | Type | Description |
|-----------|------|-------------|
| <nom> | skill / agent / hook / rule / script | <rôle dans le loop> |

---

## 9. Critères de done

- [ ] Le déclencheur est testé et fonctionnel
- [ ] La méthode de vérification est opérationnelle (Bloc 5)
- [ ] Chaque itération produit le livrable attendu
- [ ] Les 4 garde-fous sont opérationnels (validation, cap, log, kill-switch)
- [ ] Un premier run complet a été validé par un humain

---

## Notes / À confirmer

- <point à clarifier 1>
- <point à clarifier 2>
```
