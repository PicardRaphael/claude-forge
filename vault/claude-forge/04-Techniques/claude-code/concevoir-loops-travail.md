---
titre: "Concevoir un loop de travail (méthode universelle code & hors-code)"
resume: "Note canonique forge — comment concevoir un loop de travail autonome : 3 types (inner/loop/goal), 4 briques (déclencheur/source/jugement/action), vérification obligatoire (tip #1 Boris), READ vs WRITE cross-repo, 3 infra (serveur/local/Desktop), 4 garde-fous. Socle doctrinal de la skill /loop-forge."
aliases:
  - "concevoir un loop"
  - "loop de travail"
  - "construire un loop claude code"
  - "loop builder doctrine"
  - "3 types de loop"
  - "inner loop time loop goal loop"
  - "read vs write cross-repo"
  - "fleet of agents per repo"
derniere-maj: 2026-07-27
auteur: claude
type: technique
sources:
  - "Podcast Acquired (interview Boris Cherny, juin 2026) + howborisusesclaudecode.com"
  - "VentureBeat — creator of Claude Code reveals his workflow (2026)"
  - "Sunghyun Roh (Medium) — Multi-Repo Workspace Strategy (READ/WRITE split)"
  - "Anthropic engineering/managed-agents + 7-strategy framework large codebases"
  - "Claude Opus 4.8 prompting (TaskCreate/TaskUpdate, interprétation littérale)"
  - "Docs officielles code.claude.com : /goal, scheduled-tasks, desktop-scheduled-tasks, routines (fetchées 27 juil. 2026)"
  - "Plugin officiel anthropics/claude-code plugins/ralph-wiggum (README)"
  - "SpecBench arXiv 2605.21384 (reward hacking) + postmortem qualité CC (InfoQ mai 2026) + Every/Kieran Klaassen Compound Engineering"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/workflow"
  - "#doctrine/2026"
---
# Concevoir un loop de travail

> Note canonique forge — méthode pour concevoir un loop de travail autonome, **code ou hors-code**. Socle doctrinal de la skill `/loop-forge`. Le *pourquoi* (pre-compute > inference) vit dans [[pre-compute-vs-inference-loops-boris]] ; cette note traite le *comment*.

---

## QUOI — Un loop = un job répétitif automatisé de bout en bout

Un loop n'est PAS « une source de retours » ni « une feature demandée ». C'est **un job répétitif complet, du déclencheur jusqu'à l'action**, qui tourne sans qu'on le re-prompte à chaque fois.

**Règle fondatrice** : *1 loop = 1 job répétitif bien défini.* Un job peut lire plusieurs sources ; une source peut alimenter plusieurs jobs. Ne jamais raisonner « 1 loop par source » → raisonner « quel job, du début à la fin ? ».

Distinction des 3 niveaux d'abstraction (cf [[pre-compute-vs-inference-loops-boris]]) : écrire le code → prompter Claude (niveau 2, tu déclenches chaque tâche) → **écrire des loops** (niveau 3, le loop déclenche). Demander une feature = niveau 2. Un loop = niveau 3.

---

## Les 3 types de loop (Boris, vérifié web)

| Type | Mécanique | Quand | Exemple |
|------|-----------|-------|---------|
| **Inner-loop** | slash command lancée à la main, plusieurs fois/jour | workflow répété pendant que tu bosses | `/commit-push-pr` |
| **Time-loop** (`/loop`) | récurrent sur intervalle, autonome — expiration **7 jours** (doc officielle ; le « 3 jours » qui circule dans les blogs est faux) | tâche périodique sans surveillance | `/loop babysit all my PRs` ; `/loop 30m /slack-feedback` |
| **Goal-loop** (`/goal`) | tourne **jusqu'à condition vraie** | objectif binaire vérifiable | `/goal all tests in test/auth pass and lint is clean` |

La skill explique les 3, **recommande** celui adapté au job, l'utilisateur valide. Inner-loop = juste une slash command classique ; la valeur autonome est dans `/loop` et `/goal`.

---

## Les 4 briques d'un loop

Tout loop se décrit par 4 briques. La skill les demande **explicitement** (1 tâche cochée chacune — Opus 4.8 interprète littéralement, ne généralise pas seul, cf [[comment-creer-skill]] section checklist Tasks) :

1. **Déclencheur** — qu'est-ce qui le réveille ? (horaire/cron/Task Scheduler, événement, condition, continu)
2. **Source(s)** — d'où vient le travail ? (MCP, tickets, tests qui cassent, web/RSS, fichiers…)
3. **Critère de jugement** — comment Claude décide d'agir ou d'ignorer ? (le filtre « ~20% des idées sont bonnes » de Boris)
4. **Action** — il produit quoi ? (draft ticket, PR, note, rapport) + où l'humain valide

---

## IDEMPOTENCE & ÉTAT — la question qui casse un loop en prod

Un loop autonome retraite fatalement des items déjà vus (redémarrage, déclencheur qui re-tire, recouvrement de fenêtres). **« Que se passe-t-il si le loop traite 2× le même item ? »** est la question #1 qui casse un loop en production — un time-loop non-idempotent re-poste le même message Slack, re-crée le même ticket, ré-envoie le même mail.

Deux dimensions, à traiter pour TOUT loop (code ET hors-code) :

1. **Idempotence** — l'action est-elle sûre si répétée ? Sinon, marqueur de « déjà traité » (clé d'idempotence, état persistant, label sur la source). Côté hors-code aussi : où est tracé « ce qui a déjà été fait » pour ne pas re-traiter un item clos ?
2. **Reprise après interruption** — si le loop s'arrête au milieu d'un lot, comment reprend-il sans tout refaire ni rien sauter ? (état persistant entre itérations, checkpoint, journal des items traités).

Ce n'est PAS optionnel : une SPEC qui laisse l'idempotence à « à confirmer » produit un loop dangereux. À cadrer explicitement avant la vérification.

---

## VÉRIFICATION — le tip #1 (OBLIGATOIRE)

> « Probably the most important thing to get great results out of Claude Code: give Claude a way to verify its work. If Claude has that feedback loop, it will **2-3x the quality** of the final result. » — Boris Cherny

Un loop **sans méthode de vérification = anti-pattern bloquant**. Options selon le type de job :
- **Code** : tests qui passent, typecheck, `/goal` sur condition, agent de vérif en background, Chrome extension (UI/UX), agent-stop hook déterministe, plugin Ralph Wiggum (looping autonome).
- **Hors-code** : relecture croisée par un 2e agent (lens différente), critère mesurable explicite, validation humaine sur échantillon.

La skill `/loop-forge` **refuse de finaliser** sans méthode de vérif définie (propose des défauts selon le type, mais n'avance pas à vide).

**Doer ≠ Checker (consensus 2026)** : celui qui fait ne se note jamais lui-même — le vérificateur est un test exécutable, un modèle SÉPARÉ (le juge Haiku de `/goal`), ou un agent à lens différente. Une sortie qui dépend de l'auto-évaluation du modèle sort trop tôt ou jamais. Et le vérificateur est lui-même la surface d'attaque n°1 (cf section reward hacking dans l'AJOUT 27 juil. plus bas).

---

## PÉRIMÈTRE — séparer READ et WRITE (clé du cross-repo)

Le piège classique : un loop aveugle sur N repos qui doit *deviner* où agir → le contexte sature, l'agent perd le fil, la qualité s'effondre (vérifié industrie).

**Le bon mental model (best practice 2026)** :
> Le cross-repo est un besoin de **lire/explorer**. Le **WRITE doit toujours être sur un seul repo, une seule PR.**

Règles pour la skill :
- **1 loop = 1 périmètre d'ÉCRITURE fermé** (1 repo / 1 monorepo / 1 PR).
- **READ cross-repo autorisé** si le job en a besoin (lire bdd + neo_ia pour comprendre, mais écrire dans UN seul).
- Si vrai besoin multi → **pattern fleet** : soit 1 loop par repo (N loops indépendants), soit 1 loop *manager* qui lit/planifie cross-repo + délègue le write à des *workers* mono-repo (worktrees pour isolation, conflits structurellement impossibles).
- **REFUS** du seul vrai anti-pattern : un loop qui *écrit* sur plusieurs repos en devinant lequel.

Verdict industrie : 1 session sur tous les repos ❌ · monorepo + 1 agent ⚠️ · **fleet 1 agent/repo ✅** · manager+workers ✅ · worktrees ✅.
Contrainte forge : le nesting de sub-agents est possible (depth 3 par défaut depuis CC v2.1.219, 24 juil. 2026) mais l'orchestration vient par défaut de la **session principale**, pas d'un agent-leader — escalade > nesting (cf [[feedback_no_cto_agent]], [[anti-reentrance-sub-agents-pattern-escalade]]).

---

## INFRA — où le loop tourne (3 options + incompatibilités)

### Gotcha unattended — router l'I/O fichier via script (vérifié dogfood 5 juin 2026)

Une skill destinée à tourner en `/loop` **sans surveillance** ne doit PAS écrire ses fichiers via le tool `Write` ni via heredoc Bash : en mode unattended, un prompt de permission `Write` bloque le cycle, et le heredoc casse sous certaines gardes. **Router toute l'I/O fichier (état, rapport, kill-switch) via un script Python** appelé en `Bash(python3 ...)` — déterministe, pas de prompt, contourne aussi `vault-cat-guard`. Le script possède ce que le LLM ne sait pas faire de façon stable : lecture/écriture d'état, date système (jamais `Date.now` en skill), écriture du livrable. Pattern validé sur la skill `align-vault-skills` (`scripts/alignment_state.py`).


| Option | Tourne | Pour | Limite |
|--------|--------|------|--------|
| **Machine locale — `/loop` en session** | quand la session est ouverte | loops attended pendant que tu bosses | session fermée = loop mort (restauré via `--resume` si non expiré) ; min 1 min |
| **Machine locale — Desktop scheduled tasks** | à l'heure planifiée, **sans session ouverte** (app Desktop ouverte + machine éveillée suffisent) | le vrai « loop auto » local sans serveur | machine endormie = run skippé (catch-up : UN seul run manqué rejoué au réveil ; option « Keep computer awake ») ; min 1 min |
| **Serveur H24 / routines cloud** | en continu, indépendant de ta machine | loops permanents façon Boris | infra à monter/maintenir ; accès repos privés à régler ; routines cloud = min 1h, fresh clone sans fichiers locaux |

La skill **demande + signale les incompatibilités** : ex. « loop H24 critique » + « machine locale qui dort » = incohérent → force un choix. Boris tourne « a couple hundred Claudes » côté serveur ; en local/Desktop, commencer petit (1 loop, 1 périmètre).

---

## GARDE-FOUS (les 4, obligatoires sur tout loop autonome)

Un loop qui dérape coûte cher ou fait des dégâts. La skill impose les 4 :

1. **Validation humaine** — le loop produit des *drafts* (PR, tickets) ; l'humain valide avant l'action finale irréversible (Boris : Plan Mode + relecture des PRs).
2. **Plafond coût / itérations** — max N tours ou budget tokens, sinon arrêt (adaptation forge cruciale en infra locale/Desktop = facture réelle).
3. **Log / trace de chaque tour** — le loop écrit ce qu'il fait (vault/fichier) → tu sais le matin ce qu'il a fait la nuit (Boris : Agent view, system notifications).
4. **Kill-switch / terminaison MULTI-COUCHES** — moyen d'arrêt clair, et jamais une seule couche : (a) condition de convergence objective (`/goal` = la condition EST le stop ; tests verts, queue vide, passe complète sans nouveau finding), (b) détection de stall (même erreur N fois d'affilée, ex. streak 3 → stop + escalade humaine), (c) budgets durs (max itérations, coût, wall-clock ; `/loop` expire à 7 j ; fichier stop). Une couche seule ne suffit pas : un loop peut respecter le budget en étant coincé, ou progresser en le dépassant.

3/4 sont directement chez Boris ; le plafond coût est un ajout forge justifié par l'infra non-illimitée.

---

## SORTIE — SPEC puis dispatch (pre-compute)

La conception d'un loop produit une **SPEC réutilisable**, pas une génération directe :
1. La skill `/loop-forge` remplit les 9 blocs (contexte → job → type → périmètre → 4 briques → vérif → infra → garde-fous) puis écrit `SPEC-loop-<nom>.md` et **s'arrête**.
2. En étape séparée validée, la **session principale** dispatche vers les créateurs : `skill-creator` (logique réutilisable), `agent-creator` (jugement/exécution par phase — pipeline spec→draft→simplify→verify de Boris), `hook-creator` (vérif/kill-switch déterministe).

Pourquoi SPEC d'abord : c'est le principe pre-compute appliqué à `/loop-forge` elle-même — on écrit le plan une fois, relisable/rejouable, avant de brûler des tokens en génération (cf [[pre-compute-vs-inference-loops-boris]], [[pattern-spec-driven-development]]).

---

## LOOPS vs GRAPHES — quand un loop suffit (juillet 2026)

Le buzz [[graph-engineering-buzz]] (18 juil. 2026) n'invalide rien de cette note — débunk logique (Turing Post) : « **A loop is already a graph** ». Le consensus de fond qui en sort renforce la méthode :

- Une tâche bien scopée + un vérificateur clair (le tip #1 de cette note) = **un loop suffit**. Le passage à un graphe d'agents ne se justifie que sur un critère de **séparabilité** (spécialités distinctes, outils différents par étape, parallélisme réel, isolation de contexte) — jamais de cardinalité.
- Chaque node d'un graphe doit être un loop qui ship fiablement SEUL avant câblage (« a graph of weak nodes is just slop produced in parallel »).
- Les transitions qui DOIVENT firer = hooks (arêtes déterministes), pas des instructions de prompt.
- Contre-exemple utile : GPT Researcher a migré d'un pipeline graphe VERS une core loop — la maturité peut aller dans les deux sens.

### Place dans l'échelle d'adoption Boris

[[steps-of-ai-adoption-boris]] (16 juil. 2026) positionne les loops exactement là où cette note les met : la transition **2→3** (« découper le travail en loops et routines », « let Claude kick off Claude ») et le step 3 (Routines, /loop, /batch, /goal, dynamic workflows). Verbatim Boris (post du 15 juil.) : « If Claude instead writes a lint rule, CI step, or routine, that class of issue can be fully automated forever. **This is really what people are talking about when they talk about loops.** »

---

## AJOUT 27 juillet 2026 — mécaniques vérifiées + loop engineering (recherche 3 agents, sources primaires)

### Mécaniques officielles vérifiées (docs code.claude.com fetchées — crédit MAX)

- **`/goal`** (v2.1.139) = wrapper autour d'un **Stop hook prompt-based** : après chaque tour, la condition + le transcript sont jugés par un **modèle Haiku séparé** (Doer ≠ Checker natif — il ne lit pas les fichiers, il juge ce que la conversation a surfacé). Condition ≤ 4000 chars ; **la borne se met DANS la condition** (« …or stop after 20 turns ») ; une seule goal active/session ; ne change PAS les permissions → pairer avec auto mode pour tourner sans surveillance ; headless : `claude -p "/goal …" --output-format stream-json --verbose`. Indisponible si `disableAllHooks`.
- **`/loop`** = bundled skill, 3 modes : intervalle fixe (`/loop 5m …`, min 1 min, cron sous-jacent) ; **self-paced** (prompt seul → Claude choisit le délai via `ScheduleWakeup`, clampé 1 min–1 h) ; nu (`/loop`) → prompt de maintenance intégré (babysit PR/CI/conflits), personnalisable via **`.claude/loop.md`** (projet) ou `~/.claude/loop.md` (≤ 25 000 bytes, éditable à chaud). Expiration **7 jours**, max 50 tâches/session, `Esc` pour stopper.
- **`ScheduleWakeup(stop: true)`** (v2.1.202) : le loop dynamique se termine proprement de lui-même ; sans replanification, wakeup de secours ~20 min puis fin.
- **Desktop scheduled tasks** = le tier local sans session : prompt stocké dans `~/.claude/scheduled-tasks/<nom>/SKILL.md`, presets Manual→Weekly + cron custom, une tâche peut se replanifier via le MCP tool `update_scheduled_task`, worktree toggle par run.
- **Routines cloud** (`/schedule`, alias `/routines`) : min 1 h, 3 triggers (schedule / API POST `/fire` / GitHub events) ; depuis v2.1.214 le payload d'un fire API arrive **wrappé untrusted** — le prompt doit opt-in explicitement pour agir dessus (cohérent [[agents-securite]] / rule contenu-externe-non-fiable).
- **Plugin officiel `ralph-wiggum`** (anthropics/claude-code) : boucle par Stop hook EN session locale — `/ralph-loop "tâche… Output <promise>COMPLETE</promise>" --completion-promise "COMPLETE" --max-iterations 50` ; `/cancel-ralph` pour tuer. Le README est explicite : **`--max-iterations` = mécanisme de sécurité PRIMAIRE** (la promise est un match de chaîne exact, fragile). Philosophie Ralph (Geoffrey Huntley) : l'état vit dans les FICHIERS + git, chaque itération repart d'un contexte frais — c'est ce qui évite le context rot.

### Reward hacking — LE risque du tip #1 (SpecBench arXiv 2605.21384, vérifié)

Donner un vérificateur crée la cible de triche (Goodhart) : les agents frontier **saturent les tests visibles (~100 %)** et l'écart ne se voit que sur des tests **held-out** — gap jusqu'à 100 points sur les gros codebases, et il **croît avec l'horizon** (+27pp au 90e percentile par ×10 LOC). La surface d'attaque n°1 est **le vérificateur lui-même** (modifier les tests, overfit aux visibles, feature-isolation) — pas l'exploit délibéré. Plus de budget de recherche ne ferme pas le gap. Parades pratiques : vérificateur **exécutable/déterministe > LLM-judge** pour juger du code (Lean4Agent : alignement faible du jugement LLM sur les tâches SWE) MAIS LLM-judge **fort pour détecter la triche** (EVILGENIE) — deux rôles distincts ; garder des checks held-out hors de portée du loop ; un test flaky corrompt le signal (le loop « répare » ce qui n'était pas cassé).

### Compounding implémenté + incident→eval (la boucle qui se referme)

- **Compound Engineering** (Every / Kieran Klaassen, plugin CC fév. 2026) : cycle **Plan → Work → Review → Compound** — la phase Compound réinjecte les leçons dans un fichier lu à chaque session future (« lessons as assets ») ; split d'effort ~80/20 planning+review vs génération ; capturer la leçon JUSTE après l'échec/succès, avant compaction. C'est l'implémentation concrète du verbatim Boris ci-dessus (finding récurrent → lint rule/CI step/hook → la classe d'erreur disparaît pour toujours).
- **Incident → eval** (doctrine Anthropic, InfoWorld) : chaque défaut qui atteint la prod → (1) à quelle étape aurait-il été observable ? (2) fixture MINIMAL qui reproduit le mécanisme, (3) ajout à la suite déterministe ou à l'éval du reviewer. Dimensionnement : **20-50 tâches issues de VRAIS échecs** (pas des milliers de cas synthétiques) ; distinguer **pass@k** (≥1 succès sur k — outil interne) de **pass^k** (succès à chaque fois — workflow client-facing).
- **Postmortem qualité Claude Code** (Anthropic, mai 2026, InfoQ) : 6 semaines de régression tracées à 3 changements — « the eval suite was too narrow to detect a 3% quality drop from prompt changes ». Même Anthropic a dérivé faute d'evals assez larges + soak periods. L'argument massue pour la discipline vérification.

### Chiffres circulants (CLAIMS convergents de blogs — jamais officiels, ordres de grandeur seulement)

~20 itérations suffisent pour une tâche bien définie ; **> 50 itérations = la spec est à raffiner**, pas la boucle à allonger ; boucle 50 tours sur gros codebase ≈ $50-100 d'API.

---

## ANTI-PATTERNS

- ❌ « 1 loop par source de retour » → raisonner en **jobs**, pas en sources.
- ❌ Loop qui **écrit** sur plusieurs repos en devinant lequel → READ cross-repo OK, WRITE mono-repo.
- ❌ Loop **sans vérification** → le tip #1 est non négociable.
- ❌ Loop où le doer **s'auto-note** → checker séparé (test exécutable, juge Haiku de `/goal`, 2e agent), et vérificateur protégé (le loop ne doit pas pouvoir modifier ses propres tests).
- ❌ Loop **sans kill-switch / plafond** → runaway coûteux. Terminaison = 3 couches (convergence + stall + budget), jamais une seule.
- ❌ Construire un **agent orchestrateur** pour gérer les loops → session principale orchestre (cf [[feedback_no_cto_agent]]).
- ❌ Loop « H24 » sur **machine qui dort** → incohérence infra (Desktop tasks = catch-up d'UN seul run manqué, pas de rattrapage complet).
- ❌ Une feature **one-shot** transformée en loop → un loop = job *répétitif*.

---

## WIKILINKS

- [[pre-compute-vs-inference-loops-boris]] — le *pourquoi* (fondement théorique)
- [[workflow-claude-code-optimal]] — routines, multi-clauding, `/loop` dans le workflow global
- [[steps-of-ai-adoption-boris]] — les loops = transition 2→3 de l'échelle d'adoption
- [[graph-engineering-buzz]] — loops vs graphes, critère de séparabilité
- [[Boris Cherny]] — fiche leader
- [[programmatic-tool-calling]] — pre-compute au niveau API
- [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] — orchestration native + workflows nommés `.claude/workflows/`
- [[pattern-spec-driven-development]] — SPEC avant exécution
- [[comment-creer-skill]] · [[comment-creer-agent]] · [[comment-creer-hook]] — composants générés depuis la SPEC
- [[feedback_no_cto_agent]] · [[anti-reentrance-sub-agents-pattern-escalade]] — pourquoi la session principale orchestre

---

## Gotcha infra — cron natif Claude Code = SESSION-ONLY (16 juil. 2026)

Découvert à la construction de la routine vault-health : l'outil `CronCreate` de Claude Code est **session-only** — « jobs live only in this Claude session, nothing is written to disk » + auto-expiration des récurrents à **7 jours**. Il sert aux rappels et polls DANS une session vivante, jamais comme déclencheur persistant d'un loop hebdo/mensuel.

Conséquence pour le Bloc 6 (infra) d'une SPEC de loop récurrent local :
- **Déclencheur persistant machine locale** = **Desktop scheduled task** (officiel, sans session ouverte) ou Task Scheduler Windows (`Register-ScheduledTask` + `StartWhenAvailable` pour le rattrapage machine-éteinte) / cron OS — jamais CronCreate.
- **/schedule (scheduled cloud agents)** = cloud → inutilisable si le loop dépend d'une ressource localhost (MCP local, fichiers locaux).
- **Installer une persistance OS qui exécute un agent headless = décision UTILISATEUR explicite** : le classifier auto-mode bloque à raison (« Unauthorized Persistence ») un wrapper schtasks/`claude -p` non approuvé nommément en conversation — proposer les options (auto vs manuel) AVANT de créer quoi que ce soit. Cas vault-health : Raphael a choisi le déclencheur manuel assumé.
