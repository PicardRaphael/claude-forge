# SPEC-loop — skill-friction-scan

_Conçue le 15 juil. 2026 via `loop-forge`. Statut : SPEC à valider — AUCUN composant créé. Décision #3 du rapport doctrine Codex, instanciée pour forge._

## 0. Contexte

- **Orga / domaine** : claude-forge (machinerie personnelle Jarvis de Raphael).
- **Objectif business** : fermer la boucle de compounding sur les **skills forge** — détecter celles qui ont **frotté en usage réel** et les améliorer. Comble l'axe manquant : `align-vault-skills` regarde la dérive doctrine↔vault, `skill-evolve` score la maturité statique d'une skill ; **aucun ne regarde le comportement observé en session**. Ce loop lit les transcripts.
- **Type** : hors-code piloté par jugement (analyse de transcripts + proposition d'amendements ; l'écriture reste déléguée à `skill-evolve`→`skill-creator`).
- **Environnement** : repo forge uniquement.

## 1. Job

**Phrase canonique** : « Depuis les transcripts de session forge récents, détecter les skills qui ont frotté et proposer un rapport d'amendements à valider, jusqu'à ce que Raphael tranche. »

- Fréquence : **à la demande** (pas de planification).
- Coût manuel actuel : aujourd'hui non fait systématiquement — les frictions skills se perdent entre sessions (le détail est oublié 3 sessions plus tard, cf memory-discipline). Valeur = capturer ce qui échappe.

## 2. Type de loop

**inner-loop** — slash command `/skill-friction-scan` lancée à la main.

- Raison : Raphael a choisi « à la demande » → pas de time-loop autonome, pas de planification. Évite le doublon avec l'`align-vault-skills` hebdo et supprime les incompatibilités infra (machine qui dort, etc.).
- **Terminaison nominale** : rapport de friction produit + présenté.
- **Terminaison exceptionnelle** : aucune session récente à scanner → rapport vide honnête (« aucune friction détectée »), pas d'invention.

## 3. Périmètre

### 3.1 — Écriture (fermé)
- **Repo d'écriture** : forge uniquement.
- Le loop lui-même **n'écrit AUCUNE skill**. Il écrit **un rapport** dans `output/skill-friction-<date>.md`. L'écriture des skills est une étape SÉPARÉE (`skill-evolve`→`skill-creator`) déclenchée après validation Raphael.
- Lecture cross-repo : autorisée si besoin (transcripts d'autres repos sous `~/.claude/projects/`), mais l'écriture reste forge.

### 3.2 — Traitement (sur quoi il opère)
- **Source de traitement** : transcripts de session `~/.claude/projects/<projet>/*.jsonl` (+ sous-agents `subagents/*.jsonl`). Vérifié empiriquement : ~159 fichiers/14j pour forge, lisibles.
- **Objets évalués** : les skills de `.claude/skills/` de forge (croiser leur usage observé dans les transcripts).
- **Filtre** : fenêtre temporelle (défaut : depuis le dernier run, sinon N derniers jours passés en argument).

## 4. Les 4 briques + idempotence

1. **Déclencheur** : commande manuelle `/skill-friction-scan [fenêtre]`.
2. **Source** : transcripts `.jsonl` récents + liste des skills forge.
3. **Critère de jugement** : une skill « a frotté » si l'un des **4 signaux** est détecté —
   - **Auto-invocation ratée** : le sujet d'un tour correspondait à une skill mais elle n'a pas été invoquée (Raphael l'a lancée à la main, ou le travail a été refait sans elle). → *fix description.*
   - **Résultat corrigé** : la skill s'est déclenchée puis son résultat a été repris/corrigé par Raphael dans les tours suivants. → *fix body/procédure.*
   - **Erreur/blocage récurrent** : même gotcha/blocage dans ≥2 sessions. → *ajouter un gotcha / fixer.*
   - **Collision** : deux skills en concurrence de déclenchement, ou mauvaise skill déclenchée. → *désambiguïser descriptions.*
4. **Action** : produire un **rapport** listant, par skill ayant frotté : le signal, la preuve (extrait de transcript + session:ligne), l'amendement proposé.
5. **Idempotence & état** :
   - **Ne pas re-proposer 2× le même amendement** : un fichier d'état (`output/.skill-friction-state.json`) journalise les amendements déjà proposés (hash signal+skill) ; un item déjà proposé et non traité est marqué « en attente », pas re-listé comme neuf.
   - **Reprise** : le state stocke la date du dernier scan → la fenêtre par défaut repart de là (pas de re-scan de sessions déjà analysées).
   - I/O d'état routée via **script Python** (déterministe, pas de prompt Write en unattended — même si inner-loop, bonne hygiène).

## 5. Vérification (signal PASS/FAIL)

- **Validation d'un amendement proposé** (garde-fou d'étape 4 de la recette, façon AWM/chatprd) : chaque amendement candidat doit être **étayé par une preuve extraite du transcript** (citation + localisation). Signal automatique : *un amendement sans preuve citée = FAIL, rejeté du rapport.* Pas de proposition « à l'intuition ».
- **Vérification du rapport lui-même** : chaque item cite session + extrait → relisable/falsifiable par Raphael. Un rapport dont un item n'a pas de preuve = rapport invalide (à régénérer).

## 6. Infra

- **Machine locale, à la demande** (option A) — cohérent avec inner-loop. Pas de Task Scheduler, pas de serveur H24. Zéro incompatibilité infra (le loop ne tourne que quand Raphael le lance).

## 7. Garde-fous

1. **Validation humaine** : le loop **PROPOSE un rapport, n'écrit jamais une skill**. Raphael valide item par item ; seuls les amendements validés partent vers `skill-evolve`→`skill-creator`. (Compounding **jugement-piloté** : ni Willison ni OpenAI ne décrivent un loop auto-édition — l'humain reste sur la validation.)
2. **Cap coût** : borne sur le nombre de transcripts lus par run (déléguer le scan à des sous-agents en parallèle si volume élevé — max 6-8 ops/agent, découpe par fenêtre). Rapport plafonné aux N frictions les plus étayées.
3. **Log/trace** : le rapport horodaté dans `output/` EST la trace ; le state JSON journalise les runs. Notification : sortie console (pas de webhook — usage solo).
4. **Kill-switch** : trivial (inner-loop manuel — Ctrl+C). Pas de fichier flag nécessaire.

## 8. Composants à créer (déduits — inner-loop hors-code)

> À créer par la session principale APRÈS validation de cette SPEC. **DA avant implémentation** (touche la machinerie skills).

1. **1 skill `skill-friction-scan`** (`.claude/skills/`, `user-invocable: true`, slash command) — orchestre : lit les transcripts, applique les 4 signaux, valide (preuve obligatoire), génère le rapport. Réutilise `skill-evolve` pour le versant scoring/écriture.
2. **1 script Python** (`scripts/`) — parsing déterministe des `.jsonl` + gestion de l'état (`.skill-friction-state.json`) + I/O rapport. (Le LLM juge les frictions ; le script lit/écrit/dédoublonne.)
3. **Pas de hook, pas d'entrée planifiée** (inner-loop manuel).
4. **Écriture des amendements** : déléguée à `skill-evolve`→`skill-creator` (append incrémental, façon ACE — jamais réécriture complète d'une skill), une fois les items validés par Raphael.

### Recette de référence (recherche 15 juil.)
- Squelette 5 étapes : Trigger (manuel) → Source (transcripts) → Extraction (skill + amendement) → **Validation** (preuve obligatoire) → Écriture append incrémental (après gate humain).
- Fondements : ECC (hook+state+evolve), AWM/chatprd (validation gate), ACE (append incrémental, anti context-collapse). Cf [[loop-apprentissage-codex]].

## 9. Ce que ce loop N'EST PAS (anti-doublon)

- ≠ `align-vault-skills` (dérive doctrine↔vault, source = vault).
- ≠ `skill-evolve` seul (maturité statique d'une skill, sur demande, source = la skill).
- **Complément** : ce loop apporte l'axe « comportement observé en session » (source = transcripts) qu'aucun des deux n'a. Il **réutilise** `skill-evolve` comme moteur d'écriture.
