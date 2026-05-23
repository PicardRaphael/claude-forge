---
titre: "Critique -- Snapshot repo system (forge pilote)"
resume: "DA sur systeme de memoire repo par snapshot vault, 3 bloquants identifies"
aliases:
  - "critique-snapshot-repo"
  - "DA-snapshot-system-22mai"
  - "critique-memoire-repo-incremental"
  - "snapshot-vault-DA"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-22
auteur: claude
sources:
  - "[[methode-analyser-repo]]"
  - "[[raisonnement-22mai-doctrine-vs-enforcement]]"
  - "[[erreur-hooks-workflow-enforcement]]"
tags:
  - "#type/critique"
  - "#domaine/claude-code"
  - "#workflow/devils-advocate"
---

## Devils Advocate -- Snapshot repo system (forge pilote)

**Intention declaree :** stocker un snapshot vault par repo analyse (SHA + manifest hash + propositions DEPLOYEES/REJETEES) pour faire des analyses incrementales delta-only et capitaliser le contexte d\'analyse.

---

### Verdict

**Bloquants :** 3 | **Avertissements :** 5 | **Nitpicks :** 2

**Decision recommandee :** LIVRER AVEC CORRECTIONS -- le concept est valide, l\'execution actuelle a 3 trous qui le feront echouer silencieusement dans les 2 mois.

---

### Si je devais le faire marcher malgre mes objections

Garder, mais reduire le scope a l\'os :

1. **Tuer le `claude-hash` du frontmatter** -- il est sans valeur (un edit de typo dans une rule = nouveau hash = "tout est nouveau"). Remplacer par un `claude-summary` textuel mis a jour a la main : "12 agents, 28 skills, 14 hooks, doctrine 22 mai active".

2. **Remplacer SHA seul par `{sha, branch, remote-url}`** + validation au chargement : `git cat-file -e <sha>` avant `git log <sha>..HEAD`. Si SHA disparu (rebase/squash/force-push) -> fallback "snapshot orphelin -> re-analyse complete".

3. **PAS de dossier `snapshots/` separe.** Une seule note `<repo>-snapshot.md` ecrasee a chaque analyse. Historique dans `log.md` vault.

4. **PAS de modification de [[methode-analyser-repo]]** comme "etape 0/7 obligatoire". Doctrine 22 mai = pas de workflow force. Advisory conditionnel uniquement.

5. **MEMORY.md : UN seul pointer** vers `vault/00-Hub/snapshots-index.md`. Pas 6 lignes dans MEMORY.md.

6. **TTL implicite** : si `derniere-maj` > 60j -> l\'agent annonce "snapshot vieux, fiabilite degradee".

7. **Pilote forge + 1 repo applicatif** (ia_back). Forge seule = META, ne valide pas le pattern.

---

### Angle Technique -- Qu\'est-ce qui se casse ?

**Le `claude-hash` est mort-ne.** Le tree .claude/ change constamment sur forge. claude-hash != stored -> "nouveau" a chaque fois. Valeur informationnelle = zero.

**Le SHA orphelin = piege silencieux.** `git log <sha>..HEAD` sur un SHA disparu ne crashe pas -- il renvoie un range tordu. L\'agent croit "0 commits = rien a faire" alors que le SHA n\'existe plus.

**`files-count-apps: 156`** et **`manifest-hash`** : metriques fragiles. Un fixture ajoute, une dep patch bump -> "tout est nouveau".

**Hash de manifest != hash de structure.** Le bon signal architectural = `git diff --stat <sha>..HEAD -- apps/*/*.py | head` au moment de l\'analyse, pas un hash stocke.

**Objections :**

- BLOQUANT : `claude-hash` invalide a chaque edit. Le retirer.
- BLOQUANT : SHA orphelin -> git log silencieusement faux. Valider `git cat-file -e`.
- AVERTISSEMENT : `files-count-apps` et `manifest-hash` trop sensibles.
- AVERTISSEMENT : pas de validation de la branche/remote stockee.
- NITPICK : `dirs-toplevel` redondant avec `ls`.

---

### Angle Strategique -- Est-ce le bon probleme ?

**Le snapshot cree une 4e couche de verite.** Deja existant : (1) code, (2) `<repo>.md`, (3) `<app>-architecture.md`, (4) `analyse-*.md`. Snapshot = 5e. Sans regle de fusion -> contradictions dans 3 mois.

**La liste "Propositions REJETEES" est un piege.** Sans date d\'expiration -> gardien d\'idees mortes. Jarvis perd sa capacite de re-proposer quand le contexte change.

**Break-even tokens douteux.** Lire snapshot 200-500L = 3-5k tokens. Analyse fraiche repo bien structure avec CLAUDE.md a jour = 5-10k tokens. Gain incertain.

**Doctrine 22 mai.** Modifier `methode-analyser-repo` pour imposer etape 0/7 = workflow force, exactement ce qui vient d\'etre retire des hooks (cf [[erreur-hooks-workflow-enforcement]]).

**Objections :**

- BLOQUANT : doctrine 22 mai violee si enforcement. Advisory conditionnel.
- AVERTISSEMENT : 4e couche de verite sans regle de fusion.
- AVERTISSEMENT : REJETEES sans TTL = gardien d\'idees mortes.
- AVERTISSEMENT : break-even tokens douteux pour repos avec CLAUDE.md.

---

### Angle Pratique -- Combien de temps avant l\'abandon ?

**Qui maintient ?** Raphael via agents. Oubliseront de MAJ REJETEES en 3 sessions.

**Snapshot stale = menteur.** Sans signal de fraicheur, un snapshot de 90j est traite comme verite.

**Cout cache de la doctrine.** Nouveau dossier `snapshots/`, nouveau template, nouveau gotcha. Pourquoi pas reutiliser `Knowledge/syntheses/` avec tag `#type/snapshot-repo` ?

**Pilote forge** = pire candidat. Forge evolue tous les jours, snapshot perime en 48h. Un repo applicatif stable (lojii, bdd) serait mieux.

**Objections :**

- AVERTISSEMENT : pas de signal de fraicheur -> menteur silencieux.
- AVERTISSEMENT : forge comme pilote unique = mauvais candidat.
- AVERTISSEMENT : pourquoi pas reutiliser Knowledge/syntheses/ ?
- NITPICK : MEMORY.md surcharge. Index dans une note vault, pas sur MEMORY.md.

---

### Vault -- Historique pertinent

- [[erreur-hooks-workflow-enforcement]] -- Confirme la doctrine 22 mai contre workflow force. Renforce le bloquant sur "etape 0/7 imposee".
- [[erreur-pipeline-trop-long-frustration]] -- Risque de trop construire avant de tester. L\'advisor #2 l\'a flague.
- [[critique-2026-05-22-vault-doctrine-renversement]] -- Pertinent pour coherence doctrine vault.
- [[erreur-da-heredoc-bash-silencieux]] -- Rappel methode : critique sauvegardee via Python base64, pas heredoc (heredoc a echoue, cf bug 22 mai).

