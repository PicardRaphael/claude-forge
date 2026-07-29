# CHANTIER — mémoire parfaite sur 3 repos

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
| 4 | Prouver le gate `paths:` puis étendre le scoping | ⛔ **BLOQUÉ — preuve absente** (voir ci-dessous) |
| 5 | Mesurer avant/après en tokens réels | 🔶 **délégué** — chiffre borné ci-dessous ; `/context` = 10 s de Raphael |
| 6 | Décision vault avec clause de sortie mesurable | ⬜ à faire |
| 7 | Compléter les `trigger:` manquants, **sélectivement** | ⬜ à faire (voir critère) |

## Le mécanisme livré — `memory-recall.py`

`UserPromptSubmit` : lit le prompt, score les fichiers mémoire sur leur champ `trigger:` (lexical, ~60 ms de travail réel), injecte **au plus 3** souvenirs — le plus souvent **rien**. Plafonds bas assumés : le texte injecté est sauvé dans le transcript et **renvoyé à chaque tour suivant**, donc un rappel inutile coûte en permanence alors qu'un rappel manqué ne coûte qu'une fois.

**Comportement mesuré** (8 prompts réalistes, 29 juil.) : silencieux sur 3/8 (« salut ca va », « ajoute un test », méta-question) ; 3 rappels sur « commit et push » et « fix le bug dans le hook python windows » ; 1 sur « audite neo_ia », « crée une skill », « merge la branche ». Pas de sur-déclenchement observé — la sélectivité tient à 19 triggers.

## ⛔ Le point bloqué — le gate `paths:` n'est PAS prouvé

Les deux logs de la sonde ne contiennent **qu'une ligne chacun**, un `session_start` sur un fichier de test :

```
forge   : 2026-07-29T12:55:03  reason=session_start  path=.claude/rules/test.md
neo_ia  : 2026-07-29T13:06:48  reason=session_start  path=.claude/rules/x.md
```

**Aucun `path_glob_match` n'a jamais été observé.** neo_ia a pourtant 2 rules scopées (`database-rules`, `testing-mandatory`) : il faut une vraie session neo_ia qui touche un `.sql` ou un fichier de `tests/`, puis relire le log.

Tant que cette ligne n'apparaît pas, **ne pas étendre le scoping `paths:`** — précédent `once: true` : champ documenté, silencieusement ignoré. Un champ documenté n'est pas un champ honoré.

## Le gain, borné honnêtement (point 5) — ⚠️ « ~6 200 tokens » était surévalué

**Mesuré en caractères** sur neo_ia, 29 juil. (`wc -c`, artefacts chargés à chaque session) :

| Artefact | Chars | Statut |
|---|---|---|
| `memory/MEMORY.md` | 5 977 | condensé depuis 17 948 → **−11 971 chars acquis** |
| `CLAUDE.md` | 8 235 | chargé inconditionnellement |
| rules NON scopées | 57 438 | chargées inconditionnellement |
| rules scopées `paths:` | 11 020 | **conditionnel — gain NON réclamable** (gate non prouvé) |

**Ce qui est réellement acquis** : la condensation de l'index, soit **≈ 3 000–3 600 tokens/session** (11 971 chars ÷ 3,3 à ÷ 4). Zéro savoir perdu, 27 fichiers intacts et tous indexés.

**Ce qui ne l'est pas** : les 11 020 chars de rules scopées. Un gate non prouvé économise **zéro** — tant qu'aucun `path_glob_match` n'apparaît dans le log de la sonde, ces rules peuvent très bien être chargées à chaque session comme les autres. L'ancien chiffre « ~6 200 tokens/session » additionnait les deux : il est donc **faux tant que le point 4 est bloqué**.

**Ces chiffres sont des comptes de caractères, pas des tokens.** La conversion ÷3,3–÷4 est une estimation. La mesure autoritative est `/context`, qui n'est accessible que depuis un terminal interactif : **une session `claude` sur neo_ia + `/context`** donne le nombre réel. Pas exécutable depuis une session agent (ni `tiktoken`, ni SDK, ni clé API ici — vérifié).

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
