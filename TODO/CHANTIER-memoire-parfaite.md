# CHANTIER — mémoire parfaite sur 3 repos

> **Instantané historique du 29 juillet 2026.** Ne pas exécuter ce chantier comme plan courant. Le remplacement actif est `TODO/SPEC-loop-second-brain-refresh.md` et les contrats `docs/second-brain/`. Les mesures ci-dessous restent utiles comme preuves historiques.

**Ouvert : 2026-07-29 | Mis à jour : 2026-07-29 | Mandat Raphael : carte blanche | À reprendre tel quel après un `/clear`**

> Vit dans `TODO/` — **versionné**. Déplacé depuis `output/` (gitignoré) le 29 juil. sur demande de Raphael : un fichier de reprise non versionné ne peut pas être daté contre `git log`, donc rien ne signale sa péremption, et il meurt au changement de machine. Le dater contre `git log --oneline -10` avant de s'y fier reste le réflexe (cf `memory/feedback_brief_premisse_fausse_verifier_avant_executer.md`).

## L'objectif, dans ses mots

> « Quand je développe sur claude-forge, neo_ia, neoteem-back-ts, la mémoire soit utilisée à la perfection **pour éviter de refaire les mêmes erreurs** qu'à une époque. Quand je lance une feature, s'il y a besoin de mémoriser quelque chose, mais **vraiment** quelque chose, pas quelque chose de lambda. Des fois il veut tout mémoriser — il faut vraiment mémoriser les **choses vraiment importantes**. »

Deux problèmes distincts, à ne pas confondre :
1. **RAPPEL au bon moment** — je lance `/feature X` → les 2-3 erreurs passées pertinentes remontent, pas les 151 fichiers
2. **ÉCRITURE sélective** — ne capturer que ce qui a une valeur réelle

Contrainte : **mémoire 100 % locale au repo**, aucun branchement vault sur neo_ia et back-ts.

---

## Déjà fait (tours précédents, tout poussé)

| Action | Résultat mesuré |
|---|---|
| Index `MEMORY.md` condensés | neo_ia 17 948 → 5 977 (−66 %) · back-ts 11 063 → 9 042 (−18 %) |
| Dépendance vault retirée | 0 réf `forge-brain` dans `.claude/` de neo_ia et back-ts |
| 3 rules scopées `paths:` | 12 620 chars conditionnels (neo_ia ×2, back-ts ×1) |
| `learning-reminder` → détecteur | lit le transcript, ne parle que s'il trouve de la matière |
| Sonde `InstructionsLoaded` | branchée sur neo_ia, log gitignoré |
| Gain net | ⚠️ **« ~6 200 tokens » CORRIGÉ** → acquis ≈ **3 000–3 600 tokens/session** (index seul). Le reste dépendait du gate `paths:` non prouvé. Détail : § « Le gain, borné honnêtement » |

## État des hooks mémoire (mesuré)

| Repo | Hooks mémoire |
|---|---|
| claude-forge | `learning-reminder` (Stop) · `session-health` (UserPromptSubmit) · `session-reminder` + `memory-size-watcher` + `memory-saturation-watcher` (SessionStart) |
| neo_ia | `memory-watcher` (SessionStart) · `learning-reminder` (Stop) |
| neoteem-back-ts | `memory-watcher.ts` (SessionStart) · `learning-reminder.ts` (Stop) |

**Le trou identifié** : 9 hooks, tous en surveillance (SessionStart) ou rappel (Stop). **Aucun n'injecte le bon souvenir au moment où le travail commence.** C'est exactement ce que demande le mandat.

---

## Faits techniques établis (source primaire, ne pas re-chercher)

- `@imports` sont **EAGER** : « imported files load at launch » → l'index est payé à chaque session. Découper ne gagne rien, seule la **condensation** paie.
- `paths:` sur une rule **gate le chargement réel** : « Path-scoped rules trigger when Claude reads files matching the pattern, not on every tool use ». Gate honoré (correctifs v2.1.198/207/211/217, installé 2.1.220).
- ⚠️ Une rule scopée **reste chargée toute la session** après déclenchement → glob étroit obligatoire.
- `description:` sur une **rule** = inerte. `globs`/`alwaysApply` = Cursor uniquement.
- Types de hooks réels : `command`, `http`, `mcp_tool`, **`prompt`** (éval single-turn par un modèle, retourne oui/non), **`agent`** (spawne un sous-agent, expérimental).
- `UserPromptSubmit` → `hookSpecificOutput.additionalContext` (max 10 000 chars, 30 s). ⚠️ **Le texte injecté est sauvé dans le transcript** et renvoyé à chaque requête → les injections **s'accumulent**. Pas gratuit.
- L'API Claude memory tool **auto-injecte** « ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE » → un index ne se lit pas tout seul.
- État de l'art : meilleur `recall@10` = **0,862** (LongMemEval) → 1 item pertinent sur 7 manqué même par un retriever réglé.
- Les scores de rappel des vendeurs **excluent** la catégorie « sans réponse » (LoCoMo) — celle qui teste « savoir qu'on ne sait pas ». Non citables comme garantie.
- `mem0` : −90 % tokens mais **−6 points de précision** (72,9 % → 66,9 %).

---

## Travaux terminés (les 2 agents ont rendu, résultats absorbés)

`mem-trigger` (recherche) et `mem-audit` (audit des fichiers mémoire) sont **terminés**. Leurs sorties sont déjà intégrées : les champs `trigger:` posés sur 19 fichiers et le critère d'écriture durci de `learning-reminder`. Ne pas les relancer.

## Plan d'exécution — état réel

| # | Étape | État |
|---|---|---|
| 1 | Croiser recherche × audit → critère d'écriture + carte des déclencheurs | ✅ fait |
| 2 | **Injection contextuelle** `UserPromptSubmit` | ✅ **livré** — `memory-recall.py`, branché sur les 3 repos |
| 3 | Durcir l'écriture (`learning-reminder` exige que le souvenir nomme l'erreur) | ✅ fait (`af60bf3`) |
| 4 | Prouver le gate `paths:` puis étendre le scoping | ✅ **PROUVÉ par `/context all`** (29 juil.) — extension débloquée |
| 5 | Mesurer avant/après en tokens réels | 🔶 **délégué** — chiffre borné ci-dessous ; `/context` = 10 s de Raphael |
| 6 | Décision vault avec clause de sortie mesurable | ⬜ à faire |
| 7 | Compléter les `trigger:` manquants, **sélectivement** | ⬜ à faire (voir critère) |

## Le mécanisme livré — `memory-recall.py`

`UserPromptSubmit` : lit le prompt, score les fichiers mémoire sur leur champ `trigger:` (lexical, ~60 ms de travail réel), injecte **au plus 3** souvenirs — le plus souvent **rien**. Plafonds bas assumés : le texte injecté est sauvé dans le transcript et **renvoyé à chaque tour suivant**, donc un rappel inutile coûte en permanence alors qu'un rappel manqué ne coûte qu'une fois.

**Comportement mesuré** (8 prompts réalistes, 29 juil.) : silencieux sur 3/8 (« salut ca va », « ajoute un test », méta-question) ; 3 rappels sur « commit et push » et « fix le bug dans le hook python windows » ; 1 sur « audite neo_ia », « crée une skill », « merge la branche ». Pas de sur-déclenchement observé — la sélectivité tient à 19 triggers.

## ✅ Le gate `paths:` est PROUVÉ — `/context all` sur neo_ia, 29 juil. 2026

La sonde `InstructionsLoaded` n'a servi à rien (ses 2 logs ne contiennent qu'un `session_start` sur un fichier de test). **C'est `/context all` qui a tranché**, par une preuve plus directe : la ventilation fichier par fichier des Memory files.

neo_ia a **25 rules sur disque**. `/context all` en liste **23**. Les 2 absentes sont *exactement* les 2 rules scopées :

| Rule | `paths:` | Dans `/context` ? |
|---|---|---|
| `database-rules.md` (2 677 chars) | `**/*.sql`, `**/repositories/**` | ❌ **absente** |
| `testing-mandatory.md` (8 343 chars) | `**/tests/**`, `**/test_*.py` | ❌ **absente** |
| les 23 autres | aucun | ✅ toutes présentes |

**Confirmation arithmétique** : la somme des tokens listés fait 32 796 contre 32 700 affichés (écart 0,3 %, un arrondi). Il n'y a **aucune place** pour les 11 020 chars des 2 rules gatées. Elles ne sont pas chargées, point.

**Leçon de méthode** : la preuve n'est pas venue de l'instrument construit pour ça (la sonde), mais d'une commande native qui expose l'état réel. Chercher d'abord ce que l'outil expose déjà avant d'instrumenter.

→ **L'extension du scoping est débloquée** (voir § suivant).

## Le gain, MESURÉ (point 5) — `/context` sur les 2 repos, 29 juil. 2026

| | claude-forge | neo_ia |
|---|---|---|
| Memory files | **35,5k tok** · 20 fichiers | **32,7k tok** · 27 fichiers |
| Fenêtre utilisée | 67,6k / 1M (7 %) | 74,4k / 1M (7 %) |
| Rules | 16, **0 scopée** | 25, **2 scopées (gatées, prouvé)** |
| Chars eager | 82 758 | 73 948 |

**Ratio réel : 2,26–2,33 chars/token** — pas 3,3–4 comme estimé. Corpus français + markdown dense (tableaux, backticks, wikilinks, noms techniques) = tokenisation beaucoup plus fine que la prose anglaise. **Toute estimation antérieure à ÷3,3 sous-évaluait de ~40 %.**

**Acquis, chiffré au bon ratio** :
- Condensation de l'index neo_ia : −11 971 chars ⇒ **≈ 5 100 tokens/session** (et non 3 000–3 600).
- Gate `paths:` sur 2 rules : 11 020 chars ⇒ **≈ 4 700 tokens/session** — désormais **réclamable**, le gate est prouvé.
- Total neo_ia : **≈ 9 800 tokens/session**. L'ancien « ~6 200 » était *sous*-estimé, pas surestimé — mais pour la mauvaise raison (mauvais ratio ⨯ gate non prouvé).

**Deux faits que l'estimation n'aurait pas donnés** :
- **`MCP tools · 0 tokens (loaded on-demand)`** — 79 à 87 outils MCP ne coûtent **rien** au démarrage. Contre-intuitif : on pourrait croire à un coût fixe par serveur.
- **Skills : 8,4k pour 73 skills** — seules les descriptions sont chargées, pas les corps. La doctrine « description ≤ 250 chars » se paie donc directement ici.

**Mise en perspective** : 7 % de fenêtre utilisée sur 1M. Ce n'est pas un problème de saturation — c'est un coût *par requête*. L'optimisation vaut le coup, mais casser un garde-fou pour 1 % de contexte serait un mauvais échange.

⚠️ `/context` n'est **pas** exécutable depuis une session agent (commande de terminal interactif ; ni `tiktoken`, ni SDK, ni clé API disponibles — vérifié). C'est une mesure à demander à Raphael, 10 secondes.

## Où est le gisement restant — mesuré par fichier

**Les rules = ~75 % des Memory files sur les deux repos.** C'est le seul levier qui compte.

**forge — 0 / 16 scopée**, alors que plusieurs sont déclenchées par fichier. Top 6 = ~15 000 tokens :

| Rule | Tokens | Scopable ? |
|---|---|---|
| `post-dispatch-verify` | ~3 660 | non (transverse) — mais découpable principe/référence |
| `comportement-proactif` | ~2 760 | non (routage) |
| `delegate-to-specialists` | ~2 170 | partiellement |
| `memory-discipline` | ~2 160 | non |
| `sequence-canonique-modification` | ~2 130 | non |
| `forge-brain-proactive` | ~2 100 | non |
| `changelog-vault` | ~334 | **oui** → `vault/**` |
| `windows-hooks` | ~887 | **oui** → `.claude/hooks/*.py` |
| `coaching-lead-ia` | ~780 | **→ SKILL** (task-specific, cf doctrine Anthropic) |

**neo_ia — 2 / 25 scopées**, les plus grosses restantes : `agent-routing` (3,4k), `ia-back-contract` (2,9k), `sub-agent-patterns` (2,2k), `repo-scope` (2k), `billing-labels` (1,8k — **volontairement eager**, un glob y ferait faux-négatif sur le cas « nouvelle app »).

⚠️ Rappel : une rule scopée **reste chargée toute la session** après déclenchement → glob étroit obligatoire. Et ne jamais gater un garde-fou qui doit mordre *avant* que le fichier ne soit touché.

## Optimisation appliquée sur forge — 29 juil. 2026 (~1 490 tokens eager)

| Action | Avant → après | Gain eager |
|---|---|---|
| `windows-hooks` **scopée** `paths:` | eager → conditionnel | **~1 160 tok** |
| `post-dispatch-verify` dégraissée (récit → `docs/doctrine/`) | 8 537 → 7 718 chars | ~356 tok |
| `MEMORY.md` restructuré 7 sous-sections | 11 151 → 10 609 chars | ~236 tok |

**Trois décisions NÉGATIVES, aussi importantes que les gains** — un futur passage d'optimisation ne doit pas les défaire :

1. **`changelog-vault` NON scopée** malgré l'évidence apparente (`vault/**`). Le gate fire sur **lecture**, or les notes du vault s'écrivent via MCP (`create_note`/`append_note`) — aucun Read sur `vault/**`. La scoper la rendrait muette exactement dans le cas qu'elle attrape (CHANGELOG oublié). Commentaire explicatif laissé dans le fichier. ~298 tokens assumés.
2. **Référence sortie vers `docs/doctrine/`, pas `.claude/rules/references/`.** Premier essai dans un sous-dossier de `rules/` annulé : aucun précédent sur les 3 repos, et `/context all` ne liste que des `.md` à plat → impossible d'affirmer qu'un sous-dossier n'est pas ramassé comme rule. Si l'hypothèse était fausse, les 3 989 chars devenaient un coût **net**.
3. **`coaching-lead-ia` (768 tok) laissée en rule.** Candidate évidente au passage en skill (task-specific, cf doctrine Anthropic), MAIS la skill `responsable-ia` existe déjà et couvre les *livrables* — la rule couvre le *coaching + la capture terrain*, frontière explicite et voulue. Ce n'est pas un doublon : convertir est une décision de conception, à arbitrer par Raphael, pas une optimisation.

**Ce qui reste volontairement eager** : `comportement-proactif` (2,8k), `forge-brain-proactive` (2,1k), `sequence-canonique-modification` (2,2k), `memory-discipline`, `delegate-to-specialists`. Ce sont les tables de routage et les méthodes canoniques : elles doivent être en contexte **avant** de savoir quel fichier sera touché. Les gater ferait rater le déclenchement — c'est le cœur de la réserve « garde-fou tardif ».

**Le vrai enseignement du gain modeste sur `MEMORY.md`** : la condensation n'a rendu que 236 tokens parce qu'elle a été **réinvestie en couverture** — 19 fichiers mémoire existants n'étaient pas indexés du tout (index passé de 50 à 69 pointeurs). Un index qui mentait par omission valait moins que 5 % de tokens.

## Bilan des 3 repos — 29 juil. 2026

| Repo | Gain eager | Rules scopées | Index mémoire |
|---|---|---|---|
| claude-forge | ~1 490 tok | 1 / 16 | 69/69 (19 trous comblés) |
| neo_ia | ~1 200 tok | 4 / 25 | 27/27 ✅ |
| neoteem-back-ts | **~2 150 tok** | 4 / 11 | 35/35 ✅ |
| **Total** | **~4 840 tok/session** | | |

**back-ts a le meilleur ratio** (~2 150 tok pour 11 rules) parce que ses rules sont adossées à un enforcement mécanique : `depcruise` en CI, `file-size-guard`, Biome. Quand une garantie est tenue par un hook ou la CI, la rule ne porte plus que le *raisonnement* — donc elle peut être conditionnelle sans rien risquer.

### Le critère qui a émergé — quand scoper est sûr

**Scoper est sûr quand la garantie est ailleurs.** Trois cas rencontrés :

| Situation | Scoper ? | Exemples |
|---|---|---|
| Un **hook / la CI** enforce mécaniquement | ✅ oui — la rule ne porte que le raisonnement | `file-size-limit` (×2 repos), `frontieres-hexagonales`, `conventions-code`, `windows-hooks` |
| La rule ne sert qu'en **lisant/écrivant un type de fichier** | ✅ oui | `agents-color-convention`, `tdd-doctrine` |
| La rule doit mordre **à la création**, ou après une action sans lecture | ❌ **non** — le gate fire sur LECTURE, elle serait muette dans son propre cas | `changelog` (×3), `source-tree-update`, `changelog-vault` |
| Table de **routage** / méthode canonique, nécessaire avant de savoir quel fichier sera touché | ❌ non | `agent-routing`, `comportement-proactif`, `sequence-canonique-modification` |

Chaque décision négative porte un **commentaire inline dans le fichier** expliquant pourquoi, pour qu'une passe d'optimisation future ne la défasse pas en croyant bien faire.

### Reste possible (non fait)

- **forge** : `post-dispatch-verify` (~3,3k tok restants), `comportement-proactif` (2,8k), `forge-brain-proactive` (2,1k) — tous des transverses, dégraissables mais pas scopables.
- **neo_ia** : `agent-routing` (3,3k), `sub-agent-patterns` (2,4k), `repo-scope` (2k) — même nature.
- `coaching-lead-ia` → skill : décision de conception en attente d'arbitrage Raphael (cf § décisions négatives).
- Mesure `/context` post-optimisation à refaire sur les 3 repos pour confirmer les chiffres estimés ici.

## Couverture `trigger:` — mesurée

| Repo | Fichiers mémoire | Avec `trigger:` (29 juil., après pose) |
|---|---|---|
| claude-forge | 85 | **72** (était 19) |
| neo_ia | 27 | **23** (était 22) |
| neoteem-back-ts | 35 | **33** (était 12) |

Les `reference_*` de back-ts se sont révélés les garde-fous les plus rentables du corpus : chacun documente un piège qui coûte une heure de debug (un flag qui ne matche rien, un type invisible sous Bun, un vert local / rouge CI). 10 d'entre eux étaient en markdown nu, sans frontmatter — donc non indexables du tout.

**Critère de sélection — ne PAS couvrir à 100 %.** Un `trigger:` se pose si le fichier **nomme une erreur qui se reproduirait sans lui**. Manquent à ce titre sur forge : `feedback_major_mistakes`, `feedback_never_pure_executor`, `feedback_recurring_meta_anti_pattern`, `feedback_carte_blanche_commit_push`. En revanche `user_raphael_profile`, les `project_*` et `reference_discord_webhook` **ne doivent pas en recevoir** : ce ne sont pas des garde-fous, et les déclencher serait exactement le « il veut tout mémoriser » que le mandat rejette.

## Réserves à ne pas perdre

- **Ne pas construire un rappel qui se déclenche trop tard** : `changelog` (« à jour après chaque changement ») et `billing-labels` (« tout nouvel appel Gemini ») ont été volontairement laissés eager pour cette raison. Un garde-fou tardif est pire qu'un garde-fou coûteux.
- **Prouver avant d'étendre** : précédent `once: true`, champ documenté mais silencieusement ignoré.
- **Le vault forge-brain reste disponible en user-scope** (`~/.claude.json`) — donc accessible depuis toute session sans être déclaré dans les repos. Ne pas le déclarer dans neo_ia/back-ts (risque de course inter-écritures + confusion de routage à 2 cerveaux, cf DA du 16 juil.).
