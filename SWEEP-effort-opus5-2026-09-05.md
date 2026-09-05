# Sweep d'effort — Opus 5 (5 septembre 2026)

> Déclencheur : Anthropic, page *Effort* — « If you carried effort settings over from an earlier
> model, run a fresh effort sweep on your evals rather than reusing them. » Généralisé sur Fable 5.1 :
> « effort level names don't correspond to the same amount of thinking across models ».
> Le sweep se refait **à chaque changement de modèle**, y compris entre deux versions d'une famille.

## Portée

| Axe | Statut |
|---|---|
| Opus 5 | **mesuré** — 10 composants `model: opus` + toutes les skills sans `model:` héritent d'Opus 5 |
| Sonnet 5 | hors sweep — 12 composants `model: sonnet`, calibrage `sonnet, high` déjà arbitré par type |
| Fable 5.1 | **sans objet** — aucun composant du parc ne déclare ce modèle |

Parc au moment du sweep : 29 déclarations `effort:` — 27 × `high`, 2 × `medium`
(`python-ref`, `vault-health`), 1 × `xhigh` (`repo-inspector`).

## Protocole

Une seule variable change. Même agent, même cible, même prompt, trois niveaux d'effort.

- **Véhicule** : `repo-inspector` (`model: opus` → Opus 5, `disallowedTools: Write, Edit`,
  `permissionMode: plan` — read-only, donc rejouable sans risque).
- **Cible fixe** : les 9 fichiers de `.claude/rules/`, périmètre borné explicitement dans le prompt.
- **Sortie imposée** : tableau d'écarts `fichier:ligne | écart | canonique | sévérité`, total par
  sévérité, et **liste des fichiers lus en entier vs partiellement** — c'est cette dernière colonne
  qui discrimine l'effort.
- **Critère de lecture** (Lydia Hallie, repris dans `feedback_allocation_modele_effort`) :
  *did it not try hard enough, or did it not know enough ?* Fichiers sautés / vérification
  manquante → l'effort est trop bas. Erreur malgré un contexte complet → c'est le modèle, pas l'effort.
- **Ce qui compte comme gain** (`subagent-creator` § Gotchas) : « un fichier lu en plus qui change
  la conclusion, **pas une réponse plus longue** ». Un rapport plus verbeux au même niveau de
  couverture ne justifie pas le surcoût ; seul un écart réel manqué au niveau inférieur le justifie.

Le niveau retenu est le plus bas qui ne perd ni écart ni couverture de lecture.

## Mesures

| Run | Effort | Écarts (C/I/S) | Rules lues en entier | Tokens | Outils | Durée |
|---|---|---|---|---|---|---|
| 1 | `xhigh` | 19 (1/10/8) | 12/12 | 154 773 | 26 | 9 min |
| 2 | `high` | 13 (1/7/5) | 12/12 | 136 135 | 32 | 6,7 min |
| 3 | `medium` | 11 (1/5/5) | 12/12 | 123 917 | 29 | 12,1 min |

Le prompt est resté **identique aux trois runs**, y compris son erreur de départ (il annonce
« 9 fichiers » alors que `.claude/rules/` en contient 12). Corriger le prompt entre deux runs aurait
fait varier deux choses à la fois ; l'erreur conservée devient au contraire un discriminant —
repérer et corriger le périmètre annoncé est un comportement d'effort élevé.

## Lecture des résultats

**Le nombre d'écarts n'est pas la métrique.** `xhigh` en produit 19 et `high` 13, mais ce ne sont
pas les mêmes : les deux runs se recouvrent sur environ la moitié des items et divergent surtout
sur le classement de sévérité. Compter les lignes reviendrait à récompenser la verbosité.

**Ce qui départage vraiment :**

| Signal | `xhigh` | `high` | `medium` |
|---|---|---|---|
| Rules lues en entier | 12/12 | 12/12 | 12/12 |
| Écart de périmètre du brief (9 annoncés vs 12 réels) repéré et corrigé | oui | oui | oui |
| Classes de défauts fermées par mesure, pas par intuition | 3 | 2 | 3 |
| A refusé d'affirmer une staleness non mesurée | non | non | **oui** |

**Les trois niveaux tiennent la couverture, et chacun trouve un CRITIQUE différent :**

| Effort | Son CRITIQUE propre |
|---|---|
| `xhigh` | 11 rules eager qui devraient être scopées ou converties en skills |
| `high` | contradiction frontale `mcp-brief-then-direct.md:66` (« Workaround = édition manuelle ») ↔ `delegate-to-specialists.md:45-47` (« INTERDIT — ne jamais contourner le hook ») |
| `medium` | doctrine ≠ code : la rule documente 4 types protégés, `delegate-guard.py:53-61` en protège 7 (`settings.json`, `AGENTS.md`, `.mcp.json`, `hooks.json`, `config.toml`, `settings.local.json`) |

Appliqué au critère (« un fichier lu en plus qui change la conclusion ») : **aucun fichier en plus à
aucun niveau, aucune conclusion changée par le surcoût**. `xhigh` coûte +25 % de tokens sur `medium`
et ne trouve rien que les niveaux inférieurs manquent.

Le nombre d'écarts décroît avec l'effort (19 → 13 → 11) mais **la gravité, non** : c'est `medium`
qui remonte l'écart doctrine↔code le plus actionnable. L'effort supplémentaire achète du volume de
SUGGESTIONS de style, pas de la profondeur de jugement.

## Verdict

**`repo-inspector` : `xhigh` → `high`.** La mesure tue `xhigh` — c'était l'objet du finding.

**`high`, pas `medium`, malgré des résultats équivalents.** Trois raisons, dites franchement :
n = 1 par niveau et la variance inter-runs est manifestement élevée (les trois trouvent des
ensembles différents, ce qui est en soi le résultat le plus solide du sweep) ; `repo-inspector` est
un agent de **jugement**, et l'Option C réserve `medium`/`low` au mécanique ; `high` est le point de
départ officiel Opus 5. Descendre de deux crans sur une seule observation serait exactement le
raisonnement — bouger un réglage sur une mesure unique — que ce sweep existe pour discipliner.

**Les 27 autres composants à `high` restent à `high`** : ils sont déjà au point de départ recommandé
sur Opus 5, il n'y a donc aucun écart à corriger. `python-ref` et `vault-health` restent à `medium`
(inspection mécanique, conforme).

**Ce que le sweep ne dit pas** : que `medium` serait insuffisant. Il dit que rien ne prouve qu'il
soit meilleur, et qu'un seul run par niveau ne suffit pas à trancher entre deux niveaux voisins.
Une descente vers `medium` sur cet agent reste ouverte, contre 3 runs par niveau.

## Non mesuré, retenu par type

Les 4 skills porteuses d'evals (`cc-news`, `done`, `forge-brain`, `project-memory`) ne sont pas
passées au banc : leurs cas d'eval **écrivent dans le vault réel** (instance MCP unique, port 8091 —
le worktree ne l'isole pas), et ce sont des décisions de routage et d'écriture canonique, donc du
jugement. Retenues à `high` par type, conformément à l'Option C. `cc-news` porte en plus une
interdiction doctrinale de `low` (le modèle répond de mémoire sur un domaine à chiffres volatils).

C'est une limite de périmètre assumée, pas un trou dans le sweep.
