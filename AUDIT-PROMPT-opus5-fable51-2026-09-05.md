# Audit prompt — cruft daté vs Opus 5 / Fable 5.1 — 2026-09-05

> Méthode : `/claude-api prompt-audit` (`shared/prompt-audit.md`), croisée avec la canonique vault
> [[doctrine-par-modele-opus5-fable5]] (mise à jour le 5 sept. 2026) et `shared/model-migration.md`
> §§ *Migrating to Claude Opus 5* / *Migrating to Claude Fable 5.1*.
> **C'est un audit : rien n'est modifié.** Les hunks du § Diff proposé s'appliquent via les skills
> créatrices (`skill-creator`, `subagent-creator`, `claudemd-creator`) — jamais à la main.

## Hypothèses de cadrage (Step 0)

| | |
|---|---|
| **Scope** | Surface prompt de `claude-forge` : `CLAUDE.md`, `AGENTS.md`, `memory/MEMORY.md` (tous trois `@`-importés à chaque session), 12 rules, 5 agents, 51 skills (+ leurs `references/`), texte injecté par les 20 hooks, et `claude-prompting-best-practices.md` à la racine. ≈ 9 550 lignes. |
| **Cible** | **Opus 5** = cible vive (défaut forge, cf `feedback_preference_modele_opus`). **Fable 5.1** = compatibilité anticipée : aucun composant ne l'épingle, tous les `model:` sont des alias. |
| **Hors scope** | `.agents/` (adaptateurs Codex), contenu du vault, code des serveurs MCP, `.claude/worktrees/`. |
| **Non-Anthropic** | Aucun marqueur d'un autre fournisseur détecté dans la surface prompt. |

## Résumé

**7 findings actionnables, 2 flags, et une surface globalement saine.** Les trois pièges classiques
d'une migration Fable 5.1 — règles anti-formatage, instructions « montre ton raisonnement »
(refus `reasoning_extraction`), suppresseurs de narration — sont **absents**, ce que la canonique
vault avait déjà vérifié le 5 septembre et que les greps de cet audit confirment indépendamment.

Ce qui reste se concentre en trois foyers :

1. **`craft-prompt/references/techniques-claude.md` est le foyer le plus coûteux** (5 findings). C'est
   la référence qui alimente la skill de *création de prompts* : chaque prompt que tu génères hérite
   d'une doctrine arrêtée au 8 avril 2026. Elle enseigne le Chain-of-Thought explicite et
   l'auto-correction — deux instructions que Opus 5 rend contre-productives — et une ligne y est
   carrément **inversée** pour Opus 5 (« Opus 4.7 spawn moins de subagents → le spécifier »).

2. **La doctrine de délégation de forge pousse dans le mauvais sens pour Opus 5.**
   `comportement-proactif.md` encourage le fan-out parallèle par défaut. C'était juste quand les
   modèles sous-déléguaient ; Opus 5 sur-délègue. Anthropic est explicite : *« any "delegate more"
   guidance you added for Opus 4.8 should come out, and you likely want an explicit cap. »*
   Point délicat : **Fable 5.1 va dans l'autre sens** (délègue bien, en asynchrone) — la règle doit
   donc devenir conditionnelle au modèle, pas être simplement inversée.

3. **Les deux skills de veille n'ont pas de garde `effort`.** La canonique du 5 septembre avertit
   qu'à effort `low` Fable 5.1 répond de mémoire au lieu de chercher, *« a fast-moving area like AI
   models and developer tools »* — exactement le domaine de `cc-news`. Aucune des deux skills ne
   déclare d'effort : elles héritent du défaut de session.

| Groupe (guide) | Findings |
|---|---|
| 1b — scaffolds remplacés par une feature API | 3 |
| 1d — fossiles (texte ayant survécu à son modèle) | 3 |
| 4 — config & architecture | 1 |
| Keep-list #11 — re-baselining (ajout de texte) | 1 |
| Flags (rapport seulement) | 2 |

---

## Findings

### F1 — `techniques-claude.md:142` — conseil de délégation **inversé** pour Opus 5

- **Preuve** : `- Opus 4.7 spawn moins de subagents et fait moins de tool calls → le specifier quand necessaire`
- **Pattern** : 1d — fossile de version modèle.
- **Pourquoi obsolète** : le comportement s'est inversé d'une génération à l'autre. `model-migration.md`
  § Opus 5 : *« Delegates to subagents more readily — the opposite of Opus 4.8. […] Claude Opus 5
  reaches for them freely, which multiplies cost and latency. »* Suivre cette ligne aujourd'hui
  amplifie exactement le défaut du modèle.
- **Confiance** : **Haute** · **Action** : `rewrite`

### F2 — `techniques-claude.md:56` — « Self-Correction » enseignée comme technique courante

- **Preuve** : `| **Self-Correction** | Verifier sa propre reponse avant de livrer | Code, maths, analyses critiques |`
- **Pattern** : 1b — scaffold remplacé par un comportement natif.
- **Pourquoi obsolète** : *« Claude Opus 5 verifies its own work without being asked. Instructions
  that tell it to verify now cause over-verification. Removing them reduces over-verification with
  no capability regression — this is a delete, not a rewrite. »* La canonique vault ajoute la
  frontière à préserver : vérifier **un tiers** (rapport de sous-agent, source volatile) reste
  légitime ; c'est la relecture de son propre output frais qui est redondante.
- **Confiance** : **Haute** · **Action** : `rewrite` (restreindre au périmètre tiers, ne pas supprimer la ligne)

### F3 — `techniques-claude.md:11,28-30` — Chain-of-Thought explicite enseigné comme technique courante

- **Preuve** : `| **Chain-of-Thought** | "Think step by step" ou <thinking> tags | Raisonnement complexe, maths, code |`
  puis `1. **Basic** : "Think step by step"` / `3. **Structured** : <thinking> et <answer> tags separes`
- **Pattern** : 1b — scaffold remplacé par l'adaptive thinking + `effort`.
- **Pourquoi obsolète** : sur les modèles à thinking natif l'incantation est au mieux redondante, et
  la profondeur se règle par configuration (`effort`), pas en prose. Le variant « structuré »
  (`<thinking>` + `<answer>` séparés) est le plus risqué : il demande au modèle de **restituer son
  raisonnement dans la réponse**, ce qui est le déclencheur nommé du refus `reasoning_extraction`
  sur Fable 5.1 — refus silencieux avec fallback vers Opus 4.8.
- **Confiance** : **Haute** · **Action** : `rewrite`

### F4 — `techniques-claude.md:3, 88, 137-143` — table des modèles arrêtée à Opus 4.8

- **Preuve** : en-tête l.3 `_Source : […] recherche 8 avril 2026_` ; l.88 `model="claude-opus-4-7"`
  dans l'exemple d'adaptive thinking ; § *Breaking changes* qui s'arrête à Opus 4.8 (l.137-143).
- **Pattern** : 1d — fossile ; Group 2 — spécificités volatiles sans date de vérification.
- **Pourquoi obsolète** : ni Opus 5 ni Fable 5.1 n'apparaissent, alors que ce sont le défaut de forge
  et le modèle Fable courant. L'exemple de code épingle un ID de modèle de génération précédente,
  que la skill reproduira tel quel dans les prompts qu'elle génère.
- **Confiance** : **Haute** · **Action** : `rewrite`

### F5 — `comportement-proactif.md:69,71,72` — garde-fous qui *encouragent* la délégation

- **Preuve** : l.69 `- **JAMAIS 'general-purpose' pour > 8 operations** — decouper en agents paralleles`
  · l.72 `scan archi (étape 1) + scan code […] sont OBLIGATOIRES en parallèle de l'audit '.claude/'`
  · l.71 `JAMAIS un seul agent pour multi-repo — 1 agent par repo, en parallele`
- **Pattern** : 1d — mitigation écrite pour un modèle qui sous-déléguait.
- **Pourquoi obsolète** : Opus 5 atteint les sous-agents spontanément ; chacun re-établit son
  contexte, re-explore, rapporte, et le coordinateur relit le rapport. Anthropic recommande un
  **plafond explicite** plutôt qu'un encouragement. Attention à la divergence : Fable 5.1 délègue
  *bien* et gagne à le faire en asynchrone — d'où une règle conditionnelle plutôt qu'inversée.
- **Confiance** : **Haute** · **Action** : `rewrite`
- ⚠️ Touche une règle de routage structurante → **Devil's Advocate avant application**.

### F6 — `cc-news` et `veille-outils-ia` — aucune garde `effort`

- **Preuve** : frontmatter de `.claude/skills/cc-news/SKILL.md` et `.claude/skills/veille-outils-ia/SKILL.md` — pas de clé `effort:`.
- **Pattern** : Group 4 — config de requête.
- **Pourquoi obsolète** : la canonique du 5 septembre est explicite — *« ne jamais faire tourner une
  veille à effort `low`, le modèle répondrait de mémoire sur exactement le domaine où sa mémoire est
  périmée »*. Sans déclaration, ces deux skills héritent du défaut de session : une session basculée
  en `low` transforme silencieusement la veille en récitation de mémoire. `arxiv-verification`, elle,
  déclare déjà `effort: high`.
- **Confiance** : **Haute** · **Action** : `add`

### F7 — Absence de calibrage de longueur des livrables écrits (Opus 5)

- **Preuve** : ni `CLAUDE.md` (19 l.) ni `AGENTS.md` (118 l.) ne contraignent la longueur des fichiers produits.
- **Pattern** : keep-list #11 — re-baselining (le fix est d'**ajouter** du texte, pas d'en retirer).
- **Pourquoi** : *« Longer written deliverables […] files Claude Opus 5 writes to disk — reports,
  Markdown documents, summaries — are often longer than on prior models. »* Forge produit
  massivement des livrables Markdown (audits, notes vault, specs, roadmaps) ; c'est le sur-coût le
  plus directement exposé, et il n'est aujourd'hui borné nulle part.
- **Confiance** : **Moyenne** · **Action** : `add`

### F8 (flag) — Le sweep d'effort n'a pas été refait pour Opus 5 / Fable 5.1

29 composants déclarent un `effort:` (28 `high`/`xhigh`, 2 `medium`). La canonique est explicite :
*« refaire le sweep : effort level names don't correspond to the same amount of thinking across
models »*, et `memory/feedback_allocation_modele_effort.md` porte la même consigne. Aucune trace
d'un sweep post-Opus 5. Deux pistes concrètes de gain : `repo-inspector` est le seul `xhigh` du repo
(à re-mesurer contre `high`), et sur Fable 5.1 `medium` égale Fable 5 pour moins cher. Aucun edit
proposé — c'est une mesure à faire, pas une réécriture.

### F9 (flag) — `claude-prompting-best-practices.md` (racine, 787 l.) s'arrête avant les deux cibles

Son en-tête annonce couvrir « Claude's latest models » et liste Fable 5, Mythos 5, Opus 4.8, 4.7,
4.6, Sonnet 4.6, Haiku 4.5 — ni Opus 5 ni Fable 5.1. Le fichier n'est pas `@`-importé (donc pas de
coût par tour), mais il se présente comme la référence de prompting du repo. Hors scope d'un edit
ici : sa mise à jour relève de `cc-news` + `self-updater`, pas d'un audit de cruft.

---

## Non-findings — ce qui est sain, et pourquoi je n'y touche pas

Un audit qui ne trouve rien ne doit rien changer. Vérifié explicitement :

| Vérification | Résultat |
|---|---|
| Règles anti-formatage (« jamais de puces/titres/gras ») | **0 occurrence** — Fable 5.1 sous-formate déjà ; en trouver une aurait été un fix prioritaire |
| Instructions « montre ton raisonnement » | **0 occurrence** — pas d'exposition au refus `reasoning_extraction` (hors F3, qui est de la doctrine enseignée, pas une instruction active) |
| Suppresseurs de narration (« hold all findings », « ne narre pas ») | **0 occurrence** — les 11 hits de « silencieux » désignent des *échecs* silencieux, pas des consignes de silence |
| Scaffolding de vérification | **Déjà à la posture Opus 5** — 6 composants portent `❌ Re-vérifier ce que le brief dit clairement`, et les seules re-vérifications prescrites visent des tiers (sources volatiles, rapports de sous-agents), ce que la canonique classe explicitement comme à garder |
| `model: opus` / `sonnet` en frontmatter (27 occurrences) | **Forme correcte** — alias non épinglés, ils suivent la génération courante. Épingler un ID daté serait le défaut ; ce n'en est pas un |
| `effort: high` (26 occurrences) | **Doctrine forge assumée**, alignée sur le défaut Anthropic. Voir F8 pour la mesure, pas pour un edit |
| Descriptions en `ALWAYS invoke when…` | **Texte de routage** — le guide autorise explicitement une urgence calibrée dans le trigger (Group 3), à l'inverse du corps. Non flaggé |
| Injections de hooks (`session-health`, `skill-activation`, `memory-recall`) | **Pas des rappels périodiques** — gated une fois par session ou par seuil, elles injectent des pointeurs contextuels, pas des instructions ré-insérées. Le motif « reminder toutes les N tours » (qui casse l'append-only de Fable 5.1) est absent |
| 210 marqueurs `JAMAIS`/`MUST`/`OBLIGATOIRE` | **Provenance vérifiée** — adossés à `memory/feedback_*.md` ou porteurs de leur « parce que ». Le guide garde l'emphase quand elle est un correctif tracé (keep-list #5), et `feedback_feedback_reviole_3x` documente que ces règles ont été re-violées. **Aucun edit de volume proposé.** |
| `obsidian-markdown` / `obsidian-bases` (descriptions > 250 c.) | Copies kepano read-only, non protégées et non maintenues ici. Exclues |

---

## Diff proposé

Un hunk par finding. À appliquer via les skills créatrices — `delegate-guard` bloque de toute façon
l'écriture directe d'un `SKILL.md`, d'un agent ou d'un `CLAUDE.md`.

### Hunk F1+F2+F3+F4 — `.claude/skills/craft-prompt/references/techniques-claude.md`

```diff
@@ -1,3 +1,3 @@
 # Techniques Prompt — Claude (Anthropic)

-_Source : docs.anthropic.com, Anthropic Engineering Blog, recherche 8 avril 2026_
+_Source : docs.anthropic.com, Anthropic Engineering Blog — vérifié le 5 septembre 2026._
+_Doctrine par modèle : [[doctrine-par-modele-opus5-fable5]] (le prompting Claude diffère PAR MODÈLE, pas par génération)._

@@ -11 +11 @@
-| **Chain-of-Thought** | "Think step by step" ou `<thinking>` tags | Raisonnement complexe, maths, code |
+| **Thinking adaptatif** | `thinking: {type: "adaptive"}` + `output_config.effort` | Raisonnement complexe — se règle en configuration, pas en prose |

@@ -26,31 +26,29 @@
-### Chain-of-Thought — 3 niveaux
-
-1. **Basic** : "Think step by step"
-2. **Guided** : decrire les etapes de raisonnement
-3. **Structured** : `<thinking>` et `<answer>` tags separes
+### Thinking — régler la profondeur, ne pas la prescrire
+
+Le thinking est natif et toujours actif sur Opus 5 et Fable 5.1. Régler `effort`
+(`low` → `max`), pas écrire « think step by step » : l'incantation est redondante.
+
+⛔ Ne jamais demander au modèle de **restituer son raisonnement dans sa réponse**
+(« montre ton raisonnement », `<thinking>` + `<answer>` séparés) : sur Fable 5.1 c'est
+le déclencheur du refus `reasoning_extraction`, avec fallback silencieux vers Opus 4.8.
+Pour lire le raisonnement, utiliser les blocs `thinking` de l'API
+(`display: "summarized"`, ou `"updates"` pour la progression inter-outils).

@@ -56 +56 @@
-| **Self-Correction** | Verifier sa propre reponse avant de livrer | Code, maths, analyses critiques |
+| **Vérification d'un tiers** | Contrôler un rapport de sous-agent ou une source volatile | Sortie d'agent, chiffre daté — **pas** son propre output frais : Opus 5 s'auto-vérifie, l'instruire cause de la sur-vérification |

@@ -88 +88 @@
-    model="claude-opus-4-7",
+    model="claude-opus-5",

@@ -90 +90 @@
-    output_config={"effort": "xhigh"},  # low | medium | high | xhigh | max
+    output_config={"effort": "high"},  # low | medium | high | xhigh | max — défaut recommandé : high

@@ -137,143 +137,145 @@
-- `budget_tokens` **NON SUPPORTE** sur Opus 4.7 → `thinking: {type: "adaptive"}` + `output_config: {effort: "xhigh"}`
-- `effort: xhigh` = defaut a l'ere Opus 4.7 (avril-mai 2026) ; depuis Opus 4.8 (28 mai) le defaut recommande est `high`. `high` reste defaut Sonnet 4.6
+- `budget_tokens` renvoie **400** sur Fable 5/5.1, Opus 5/4.8/4.7 et Sonnet 5 → `thinking: {type: "adaptive"}` + `output_config: {effort: …}`
+- Défaut recommandé : `high`. `xhigh` = step-up mesuré. Sur Fable 5.1, `low`/`medium` dépassent souvent le `xhigh` des modèles antérieurs — mais **jamais `low` sur une tâche de veille** (le modèle répond de mémoire)
 - Prefill deprecated sur claude-4.6+ → Structured Outputs
 - Skills = standard ouvert (agentskills.io) adopte par OpenAI, Gemini, GitHub Copilot
-- Opus 4.7 est plus litterral que 4.6 → instructions de scope explicites, parallelisme explicite
-- Opus 4.7 spawn moins de subagents et fait moins de tool calls → le specifier quand necessaire
-- Nouveau tokenizer Opus 4.7 : meme input = ~1.0-1.35x plus de tokens que 4.6
+- Opus 5 suit les instructions littéralement → cadrer le scope explicitement
+- **Opus 5 sur-délègue** (inverse d'Opus 4.8) → plafonner le nombre de sous-agents, ne pas encourager le fan-out
+- **Fable 5.1 délègue bien**, en asynchrone → l'encourager plutôt que le brider. La consigne de délégation est conditionnelle au modèle
+- Opus 5 rédige des réponses et des livrables Markdown plus longs → calibrer la longueur explicitement
+- Tokenizer inchangé depuis Opus 4.7 (Fable 5.1 inclus)
```

### Hunk F5 — `.claude/rules/comportement-proactif.md`

```diff
@@ -66,72 +66,74 @@
 ## Anti-patterns de dispatch

 - **JAMAIS `Explore` pour auditer un projet** — Explore = recherche rapide read-only, PAS un audit
-- **JAMAIS `general-purpose` pour > 8 operations** — decouper en agents paralleles
 - **JAMAIS Grep/Read brut sur le vault** → voir `.claude/rules/forge-brain-proactive.md` (source canonique de la règle)
-- **JAMAIS un seul agent pour multi-repo** — 1 agent par repo, en parallele
-- **JAMAIS s'arrêter à l'audit `.claude/` quand l'user demande "analyse mon repo / propose-moi config CC"** — c'est la méthode 6 étapes [[methode-analyser-repo]] : scan archi (étape 1) + scan code pour patterns récurrents (étape 5) sont OBLIGATOIRES en parallèle de l'audit `.claude/`. Sinon propositions théoriques déconnectées du repo réel.
+- **JAMAIS s'arrêter à l'audit `.claude/` quand l'user demande "analyse mon repo / propose-moi config CC"** — c'est la méthode 6 étapes [[methode-analyser-repo]] : le scan archi (étape 1) et le scan code (étape 5) font partie du livrable, en parallèle de l'audit `.claude/`. Sinon propositions théoriques déconnectées du repo réel.
+
+## Plafond de délégation — dépend du modèle
+
+Un sous-agent re-établit son contexte, re-explore, rapporte, et la session relit son rapport : le
+surcoût est réel et se paie même quand le fan-out paraît élégant.
+
+**Sur Opus 5** (défaut forge) : déléguer **rarement**, et seulement quand le gain dépasse clairement
+ce surcoût. Multi-repo et investigations larges multi-fichiers le justifient — un agent par repo
+reste le bon découpage. Ne pas déléguer ce qui se fait en quelques appels d'outils, ni une
+vérification (elle appartient à la boucle principale). Un seul sous-agent suffit-il ? Alors un seul.
+
+**Sur Fable 5.1** : l'inverse — la délégation parallèle est fiable et gagne à être asynchrone
+(les agents longue durée gardent leur contexte, la session ne bloque pas sur le plus lent).
+
+Source : [[doctrine-par-modele-opus5-fable5]] — le comportement de délégation diverge PAR MODÈLE.
```

### Hunk F6 — `cc-news` et `veille-outils-ia` : garde `effort`

```diff
--- a/.claude/skills/cc-news/SKILL.md
+++ b/.claude/skills/cc-news/SKILL.md
@@ -4,5 +4,6 @@
 user-invocable: true
+effort: high    # jamais `low` sur une veille : le modèle répondrait de mémoire (cf doctrine-par-modele-opus5-fable5)
 allowed-tools: WebSearch, WebFetch, Read, Agent, mcp__forge-brain__search_brain, …

--- a/.claude/skills/veille-outils-ia/SKILL.md
+++ b/.claude/skills/veille-outils-ia/SKILL.md
@@ -4,5 +4,6 @@
 user-invocable: true
+effort: high    # jamais `low` sur une veille : le modèle répondrait de mémoire (cf doctrine-par-modele-opus5-fable5)
 allowed-tools: WebSearch, WebFetch, Read, Skill, mcp__forge-brain__search_brain, …
```

### Hunk F7 — `AGENTS.md` : calibrage de longueur des livrables

À insérer dans le bloc d'ouverture, après `- Diff minimal, aucune feature spéculative.` :

```diff
@@ -8,0 +9 @@
+- Calibrer la longueur d'un livrable écrit (rapport, note, spec) sur ce que la tâche demande : couvrir le fond, sans sections de remplissage, résumés redondants ni boilerplate.
```

---

## Vérification recommandée avant d'appliquer

Le guide traite toute suppression comme une hypothèse, pas une conclusion.

1. **F1-F4** : demander à `craft-prompt` de produire un prompt sur une tâche de raisonnement, avant
   et après. Le « après » ne doit plus contenir ni `<thinking>` ni consigne d'auto-vérification.
2. **F5** : lancer un audit multi-repo avant/après et compter les sous-agents spawnés. La règle
   réécrite doit réduire le fan-out sans casser le découpage un-agent-par-repo.
3. **F6** : purement additif, aucun risque de régression.
4. **F7** : comparer la longueur d'un même livrable avant/après — Anthropic mesure ~20 % de
   réduction avec une consigne de concision équivalente.
5. **F5 uniquement** : passer par `devils-advocate` avant application (règle de routage structurante).

## Ce que cet audit n'a pas fait

- Aucun fichier modifié : le rapport et le diff sont les livrables.
- Pas de sweep d'effort mesuré (F8) — c'est une campagne de mesure, pas une réécriture.
- ~40 skills hors multiplicateurs de doctrine n'ont été lues qu'aux points touchés par un grep de
  signal, pas intégralement. Les greps couvraient l'ensemble des signaux du guide ; une lecture
  intégrale des 8 000 lignes de `SKILL.md` remonterait surtout du bruit de style, pas du cruft daté.
