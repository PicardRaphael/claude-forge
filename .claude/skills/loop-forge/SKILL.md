---
name: loop-forge
description: ALWAYS invoke when the user wants to DESIGN or spec a recurring work loop / autonomous routine (code or non-code). Writes a SPEC then stops. NOT for running a loop — use builtin /loop or /goal to execute. DO NOT design without invoking first.
argument-hint: "[décris le job répétitif à automatiser]"
allowed-tools: Read, Write, Glob, Grep, Bash, Task, AskUserQuestion, mcp__forge-brain__*
user-invocable: true
model: opus
effort: high
memory: project
---

# loop-forge — Conception de boucles de travail

Transforme un job répétitif (code ou non-code) en spec structurée : `SPEC-loop-<nom>.md`.

> **STOP CRITIQUE — règles non-négociables :**
> - Cette skill **CONÇOIT** des boucles. Elle n'exécute, ne génère, ne crée aucun composant.
> - Elle s'arrête à la génération de `SPEC-loop-<nom>.md`. Point final.
> - La création de skills, agents, hooks ou règles est une étape SÉPARÉE, orchestrée par la session principale.
> - Ne jamais auto-générer de composants `.claude/`. Ne jamais lancer `/go`, `/spec`, ou un agent créateur.
> - **Attention `/loop` builtin** : `/loop` est une commande native Claude Code (répète une tâche N fois). Cette skill `/loop-forge` CONÇOIT des boucles — elle ne les exécute pas. Si l'utilisateur veut exécuter une boucle existante, rediriger vers `/loop`.

---

## Workflow — 9 blocs séquentiels

**Mécanique Tasks natif** : créer une tâche via `TaskCreate` par bloc avec statut `pending`. Passer à `in_progress` en débutant le bloc, `completed` avant d'avancer au suivant. Ne jamais passer au bloc N+1 tant que le bloc N n'est pas `completed`. Raison : Opus 4.8 interprète littéralement et ne généralise pas seul — la checklist explicite évite d'oublier un bloc.

---

### Bloc 0 — CONTEXTE

`AskUserQuestion` (max 4 items) :
1. Orga et domaine : qui est derrière ce loop, dans quel contexte métier ?
2. Objectif business : quel problème ça résout, quelle valeur ça crée ? (le POURQUOI)
3. **Bifurcation** : est-ce un loop **code** (shell, Python, script, outil CLI, API, fichiers) ou **hors-code** (process humain, checklist, réflexion, veille, validation qualité) ?
4. Environnement : quel(s) repo(s) ou contexte(s) techniques cadrent le loop ?

> **La bifurcation (Q3) répond à UNE seule question : quelles questions techniques poseront les blocs suivants** (branche code → `references/questions-code.md`, branche hors-code → `references/questions-hors-code.md`). Elle ne décrit PAS sur quoi le loop opère.
>
> **Ne PAS demander ici le périmètre fonctionnel** (les objets/fichiers/sources que le loop traite, ni le repo d'écriture). C'est le rôle du **Bloc 3**, qui distingue périmètre d'écriture et périmètre de traitement. Confondre bifurcation, périmètre d'écriture et périmètre de traitement = 3 questions différentes mélangées → l'utilisateur ne sait pas répondre (observé dogfood 5 juin). Q4 ici reste un cadrage léger (« dans quel(s) repo(s) ce loop s'inscrit-il »), pas un inventaire des objets traités.

Si branche **code** ET repo identifié → analyser le repo avec `Glob` + `Read package.json` ou `pyproject.toml` + `git log -20` pour pré-remplir la section Stack du Bloc 5 (ne pas re-demander ce qu'on peut déduire).

---

### Bloc 1 — JOB

Demander une description libre du job répétitif.

La skill **reformule** ensuite en 1 phrase canonique sous la forme : "Depuis [source], [action], jusqu'à [fin]."

`AskUserQuestion` :
- "Est-ce que cette reformulation est exacte ?" (valider ou corriger)
- Fréquence actuelle (si déjà fait manuellement) : combien de fois par semaine/mois ?
- Coût/temps actuel par exécution manuelle : combien de temps ça prend, quel effort ?

Ces métriques (fréquence × temps) serviront à justifier l'investissement de conception dans la spec.

---

### Bloc 2 — TYPE DE LOOP

La skill EXPLIQUE les 3 types, puis RECOMMANDE selon le job décrit. L'utilisateur valide.

**Les 3 types :**
- **inner-loop** = slash command lancée à la main, plusieurs fois par jour (ex : `/commit-push-pr`). Usage : tâches fréquentes à faible latence déclenchées humainement.
- **time-loop** (`/loop`) = récurrent sur intervalle, autonome jusqu'à 3 jours. Usage : batches périodiques, surveillance, jobs planifiés.
- **goal-loop** (`/goal`) = tourne jusqu'à ce qu'une condition soit vraie. Usage : convergence vers un état cible, retry jusqu'à succès, exploration bornée.

Recommander le type le plus adapté en expliquant brièvement pourquoi (1-2 lignes). L'utilisateur valide ou choisit un autre type.

Une fois le type validé, préciser :
- Critère de terminaison nominal (succès)
- Critère de terminaison exceptionnel (timeout / N itérations max / erreur fatale / kill-switch manuel)

---

### Bloc 3 — PÉRIMÈTRE

Le périmètre couvre **DEUX dimensions distinctes**, à poser séparément. Ne pas les fusionner : le repo où le loop ÉCRIT n'est pas forcément ce que le loop TRAITE.

#### 3.1 — Périmètre d'ÉCRITURE (où le loop écrit)

**Règle d'écriture (non-négociable)** : un loop doit avoir un périmètre d'ÉCRITURE fermé : 1 repo, 1 monorepo, ou 1 PR. La lecture cross-repo est autorisée. Un loop qui ÉCRIT sur plusieurs repos en devinant lequel est refusé.

`AskUserQuestion` :
- Quel est le repo cible d'écriture ? (1 seul)
- Y a-t-il besoin de lire dans d'autres repos ? (lecture croisée OK)
- **Si multi-repo en écriture** → proposer le pattern fleet : soit 1 loop par repo (parallèle), soit 1 manager qui lit + des workers qui écrivent chacun dans leur repo. L'utilisateur choisit.

#### 3.2 — Périmètre de TRAITEMENT (sur quoi le loop opère)

**Distinct du périmètre d'écriture.** Sur QUELS objets le loop travaille à chaque itération : quels fichiers, dossiers, sources, entités. Un loop peut écrire dans le repo X (écriture) mais traiter les skills + agents de `.claude/` (traitement), ou traiter des feedbacks d'une DB, des notes d'un vault, des PR ouvertes, etc.

`AskUserQuestion` :
- Sur quels objets le loop opère-t-il concrètement ? (fichiers/dossiers précis, sources de données, entités métier)
- Ce périmètre de traitement est-il le même que le repo d'écriture, ou différent ? (ex : « traite `.claude/skills/` + `.claude/agents/` mais écrit la spec/le rapport dans `TODO/` »)
- Y a-t-il un filtre (extension, label, statut, date) qui borne les objets traités ?

> Pourquoi séparer (dogfood 5 juin) : un loop hybride ou un loop hors-code qui opère sur des fichiers d'un repo se cadre mal quand « code/hors-code », « repo d'écriture » et « objets traités » sont mélangés. Bifurcation (Bloc 0) = quelles questions poser ; périmètre d'écriture (3.1) = où ça écrit ; périmètre de traitement (3.2) = sur quoi ça travaille. Trois choses.

#### 3.3 — Questions complémentaires

Inputs/outputs, stack, gestion d'erreur → voir `references/questions-code.md` (branche code) ou `references/questions-hors-code.md` (branche hors-code), conduites en 1-2 `AskUserQuestion` (batches de 4 max).

---

### Bloc 4 — LES 4 BRIQUES

`AskUserQuestion` pour clarifier chacune des 4 briques fondamentales du loop :

1. **Déclencheur** : qu'est-ce qui lance une itération ? (cron, webhook, événement fichier, commande manuelle, commit, fin d'une autre tâche)
2. **Source(s)** : d'où viennent les données ou artefacts traités à chaque itération ?
3. **Critère de jugement** : comment le loop sait-il si une itération est réussie ou non ?
4. **Action** : que fait concrètement le loop sur chaque item ? (transformer, envoyer, sauvegarder, notifier)

**5e question — OBLIGATOIRE, non-skippable (code ET hors-code) :**

**Idempotence & état** : deux sous-questions à poser ensemble :
- Si le loop traite 2× le même item, que se passe-t-il ? (marqueur "déjà traité" / clé d'idempotence / label sur la source / dédoublonnage)
- Si le loop s'interrompt au milieu d'un lot, comment reprend-il sans tout refaire ni rien sauter ? (état persistant / checkpoint / journal des items traités)

Si l'utilisateur répond "ça n'arrivera pas" ou "c'est simple" → expliquer que tout loop peut être interrompu (crash, kill-switch, machine redémarrée) et re-poser. Cette question ne peut pas rester sans réponse dans la spec. Réf : [[concevoir-loops-travail]] section "IDEMPOTENCE & ÉTAT".

---

### Bloc 5 — VÉRIFICATION (OBLIGATOIRE BLOQUANT)

> Boris tip #1 : "Give Claude a way to verify its work → 2-3x quality improvement."

La skill **propose des mécanismes de vérification par défaut** selon le type choisi au Bloc 2, puis demande validation :

- **inner-loop** → tests unitaires sur le script / typecheck / dry-run mode avec diff visible
- **time-loop** → agent de vérification séparé qui relit les outputs / goal-check explicite / rapport de diff itération N vs N-1
- **goal-loop** → condition de succès mesurable et automatiquement vérifiable / garde-fou "max N itérations avant vérification humaine"
- **hors-code** → relecture croisée par un second acteur / critère mesurable (score, checklist cochée, approbation explicite)

`AskUserQuestion` bloquant :
- "Quelle méthode de vérification retiens-tu ?" (choix parmi les propositions ou alternative)

**La skill REFUSE de passer au Bloc 6 sans une méthode de vérification produisant un signal binaire/mesurable (PASS/FAIL).**

Distinction obligatoire à rappeler si l'utilisateur répond "un humain regarde" :
> "La vérification (Bloc 5) doit produire un signal automatique PASS/FAIL : test, check, condition, critère chiffré. 'Un humain regarde' n'est PAS une vérification au sens tip #1 Boris — c'est la validation humaine du Bloc 7 (garde-fou), distincte. Quel signal automatique dit PASS ou FAIL après chaque itération ?"

Re-poser jusqu'à obtenir un signal mesurable. Si la branche est réellement non-automatisable (hors-code pur), la méthode acceptable est un critère mesurable explicite (score ≥ seuil, checklist cochée à 100%, approbation formelle enregistrée) — pas un jugement informel.

---

### Bloc 6 — INFRA

`AskUserQuestion` :
- Sur quelle infrastructure le loop tourne-t-il ?
  - A : Machine locale (Task Scheduler Windows / cron macOS/Linux) — ne tourne pas si la machine est éteinte
  - B : Serveur H24 (VPS, container, cloud function)
  - C : Claude Desktop scheduled (déclenché depuis Claude Desktop)

**Signaler les incompatibilités :**
- Si type = time-loop ou goal-loop (autonomie multi-heures) ET option A (machine locale) → avertir : "Un loop autonome sur machine locale s'arrête si la machine dort ou est éteinte. Confirmes-tu ce choix ou préfères-tu l'option B ?"
- Si option C → préciser que Claude Desktop scheduled est limité aux tâches compatibles avec le contexte Claude (pas d'accès système natif).

---

### Bloc 7 — GARDE-FOUS (obligatoires)

Ces 4 garde-fous sont **non-négociables** dans toute spec :

1. **Validation humaine** : à quelle fréquence un humain valide-t-il le résultat ? (chaque itération / par batch / par exception)
2. **Cap coût/itération** : limite max d'itérations ou de tokens/appels API par cycle
3. **Log/trace** : traçabilité de chaque itération (qui a fait quoi, quand, résultat) + stockage des logs (path ou service) + notification en cas d'échec (canal + destinataires)
4. **Kill-switch** : comment interrompre le loop immédiatement si nécessaire ? (fichier flag, variable env, commande manuelle)

Si l'utilisateur n'a pas répondu à ces 4 points, `AskUserQuestion` pour les compléter.

---

### Bloc 8 — SORTIE

#### 8.1 — Résoudre le path de sortie

Exécuter via Bash :
```bash
git rev-parse --show-toplevel
```

Le fichier de sortie = `<racine-repo>/TODO/SPEC-loop-<nom-kebab>.md`.

Si le dossier `TODO/` n'existe pas :
```bash
mkdir -p "<racine>/TODO"
```

#### 8.2 — Écrire la spec

Template complet dans `references/spec-template.md`.

Remplir le template avec toutes les réponses collectées (blocs 0-7). Aucun champ ne doit rester vide — si info manquante : `"à confirmer"`.

**Avant d'écrire**, déduire la section "Composants à créer" selon le type et l'infra (ne pas laisser en `<nom>` vide) :

| Type | Infra | Composants déduits |
|------|-------|-------------------|
| inner-loop, code | toute | 1 skill `<job>` + 1 script de vérification (Bloc 5) |
| time-loop, code | machine locale | 1 skill `<job>` + 1 hook kill-switch + 1 entrée Task Scheduler (Windows) / crontab (macOS/Linux) |
| time-loop, code | serveur H24 | 1 skill `<job>` + 1 hook kill-switch + 1 service systemd / cron / job planifié |
| goal-loop, code | toute | 1 skill `<job>` + 1 agent de vérification + 1 hook kill-switch |
| hors-code (tout type) | toute | 1 skill `<job>` (checklist interactive) + 1 template de livrable + critère de validation Bloc 5 |

Adapter selon les réponses réelles (ex : si hook kill-switch déjà existant → ne pas le lister).

#### 8.3 — Gate de validation

Après écriture :

1. Afficher le path absolu du fichier généré
2. `AskUserQuestion` bloquant :
   - A : "STOP — j'inspecte la spec avant de décider" ← **recommandé, par défaut**
   - B : "Ajuster un point avant validation"
   - C : "Prêt à passer à la création des composants"
3. Si A ou B → la skill se termine. Aucune action supplémentaire.
4. Si C → afficher exactement : *"Crée les composants décrits dans `TODO/SPEC-loop-<nom>.md`"* (phrase à copier-coller dans la session principale). La skill NE crée JAMAIS les composants.

---

## Gotchas

- **`/loop` collision** : `/loop` natif Claude Code exécute une tâche N fois. `/loop-forge` conçoit une spec. Si l'utilisateur tape `/loop` en voulant cette skill, corriger et rediriger.
- **JAMAIS créer de composants** : même si l'utilisateur dit "et crée aussi la skill", répondre : "Hors scope de loop-forge. La session principale crée les composants après validation de la spec."
- **`$(git rev-parse --show-toplevel)` pas `${CLAUDE_PROJECT_DIR}`** : `CLAUDE_PROJECT_DIR` est vide dans le contexte skills. Toujours résoudre le repo via git.
- **`$ARGUMENTS` jamais dans les backticks** : parser l'argument dans le raisonnement, passer la valeur résolue (variable locale) aux commandes Bash.
- **Orchestration de créateurs = session principale, pas le sub-agent** : un sous-agent peut techniquement spawner (CC v2.1.172) mais le défaut forge reste l'escalade — si un sub-agent de cette skill doit orchestrer un créateur, STOP + ESCALADE vers la session principale (contexte propre, coût maîtrisé ; pattern [[anti-reentrance-sub-agents-pattern-escalade]]).
- **Branche hors-code ne nécessite pas de script** : ne pas proposer d'implémentation technique pour un loop humain/process. La spec suffit.
- **Garde-fous non-négociables** : ne pas skipper le Bloc 7 même si l'utilisateur dit "c'est simple". Un loop sans kill-switch est dangereux.
- **Gate AskUserQuestion obligatoire** en fin de Bloc 8 : ne jamais passer directement à la création de composants.
- **Taille SPEC** : une spec complète fait 80-150 lignes. Moins = info manquante. Plus = trop de prose.

---

## Apprentissage

Après chaque utilisation significative :
- Si une question de l'interview bank s'avère inutile ou manquante → noter ici avec la date
- Si un type de loop nouveau émerge (hors code/hors-code binaire) → documenter
- Si le template spec ne couvre pas un cas → noter la section manquante

**2026-06-05** (dogfood) — Bloc 0 mélangeait bifurcation et périmètre fonctionnel : un loop hors-code traitant des fichiers d'un repo se cadrait mal. Correction : bifurcation reste au Bloc 0 (= quelles questions poser), le périmètre vit au Bloc 3 scindé en écriture (3.1) et traitement (3.2). Trois concepts distincts à ne jamais reconfondre.

---

## Références

- `references/questions-code.md` — bank de questions blocs 3-4-5 pour loops code
- `references/questions-hors-code.md` — bank de questions blocs 3-4-5 pour loops hors-code
- `references/spec-template.md` — template complet SPEC-loop-`<nom>`.md
