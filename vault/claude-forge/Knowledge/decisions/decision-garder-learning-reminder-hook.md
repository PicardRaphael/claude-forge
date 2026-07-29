---
titre: "Décision — learning-reminder : de rappel systématique à détecteur (V2, 29 juil. 2026)"
resume: "Le hook Stop learning-reminder est passé de rappel systématique (decision:block à chaque fin de session, payoff mesuré nul) à DÉTECTEUR qui lit le transcript et n'alerte que s'il trouve un apprentissage non capitalisé. Remplace la décision du 29 mai 2026, dont les 2 piliers techniques étaient périmés. Appliqué à forge d'abord ; les copies des autres repos divergent (3 textes, 2 mécanismes, 2 langages)."
aliases:
  - "decision learning-reminder"
  - "learning-reminder detecteur"
  - "learning-reminder V2"
  - "garder learning-reminder"
  - "exception doctrine 22 mai learning-reminder"
  - "Stop hook learning-reminder décision"
  - "proactivity-reminder supprimé"
domaine: claude-code
type: decision
derniere-maj: 2026-07-29
auteur: claude
tags:
  - "#type/decision"
  - "#domaine/claude-code"
  - "#sujet/hooks"
  - "#doctrine/2026"
---

# Décision — learning-reminder : rappel systématique → détecteur (V2)

> Cette note **remplace** la décision du 29 mai 2026 (« GARDÉ, exception assumée »), dont les deux piliers techniques sont devenus faux. Historique conservé en bas.

## Décision (29 juillet 2026)

`learning-reminder` **reste**, mais change de nature : il ne demande plus, il **détecte**.

| Avant (mai → juil.) | Après (V2) |
|---|---|
| `decision: block` à **chaque** fin de session | `decision: block` **seulement** si un apprentissage non capitalisé est détecté |
| Question générique en 6 points | Cite **quels** signaux ont été trouvés |
| Happy path = « rien à sauvegarder » | Happy path = **silence** (exit 0) |

Mécanisme : le hook lit le transcript de la session (champ `transcript_path` du JSON stdin — le même pattern que `delegate-guard.py`), cherche des signaux d'apprentissage (correction explicite de Raphael, nouvelle norme énoncée, doctrine mesurée périmée, gotcha découvert) **et** vérifie si une capitalisation a déjà eu lieu (`memory/*.md`, appels MCP d'écriture vault, `Knowledge/*`). Signaux **sans** capitalisation → alerte. Sinon, silence.

## Pourquoi ce pivot — les deux mesures qui l'ont déclenché

**1. Payoff mesuré nul.** `search_sessions` sur les transcripts : **8 occurrences** de « rien à sauvegarder » et **zéro capture attribuable au hook**. Le 27 juil., la réponse au hook était *« tout ce que la session a appris a déjà été capitalisé avant ce tour »*. La session du 29 juil. a produit ~10 apprentissages capitalisés — **aucun déclenché par le hook**.

La raison structurelle : la capitalisation arrive **pendant** la session, poussée par les rules en **pré-action** (`memory-discipline`, `check-before-create`, `forge-brain-proactive`). Le hook, en post-hoc, ne créait pas le comportement — il le constatait trop tard. Le motif de mai (« Raphael n'exécute pas `/done` de façon fiable ») restait vrai, mais le filet ne servait pas : d'autres mécanismes avaient pris le relais.

**2. Un bug, présent sur forge uniquement.** Le hook faisait `sys.stdin.read()` sans parser → il ne testait **jamais** `stop_hook_active`, et son marqueur était **global** (`claude-forge-learning-reminded`) au lieu d'être par `session_id`. Si l'écriture du marqueur échouait (exception avalée), il bloquait à **chaque** Stop — précédent de boucle infinie dans [[erreur-hooks-bash-quoting-windows]]. Deux sessions forge concurrentes se volaient aussi le marqueur. Les trois autres repos avaient déjà la garde correcte ; le repo le plus critique était le seul fragile.

## Les 2 piliers de mai, périmés

La décision du 29 mai reposait sur deux faits techniques qui ne tiennent plus :

1. ❌ « **Stop ne supporte PAS `additionalContext`**, donc convertir en advisory est *infaisable* ». **Faux depuis CC v2.1.163 (4 juin 2026)** — six jours après la décision. Docs officielles : « Stop and SubagentStop also accept `hookSpecificOutput.additionalContext` for non-error feedback that continues the conversation ».
2. ❌ « `once: true` = mécanisme légitime ». **Silencieusement ignoré** dans `settings.json` (honoré en frontmatter de skill uniquement) — mesuré dans `AUDIT-CLAUDE-2026-06-17.md:26`. L'unicité reposait en réalité sur le marqueur fichier.

⚠️ Pourquoi la V2 garde quand même `decision: block` : `additionalContext` s'injecte « for the next model request ». Au Stop **terminal**, il n'y a pas de requête suivante — un advisory pur y serait invisible, donc du code mort. `block` est conservé, mais il ne se déclenche que quand il y a matière.

## Périmètre — les copies ne sont pas le même composant

Mesuré le 29 juil. : **3 textes différents, 2 mécanismes, 2 langages**.

| Repo | Garde anti-boucle | Marqueur | Texte |
|---|---|---|---|
| **forge** | ❌ absente (corrigée en V2) | global → par session | 6 items, sans garde anti-hallucination |
| neo_ia | ✅ | par `session_id` | 5 items + filtre anti-bruit |
| neoteem-brain | ✅ | par `session_id` | 3 items + filtre |
| neoteem-back-ts | ✅ | par `session_id` | 5 items, **TypeScript** |
| `.codex/hooks/` | — | — | ⛔ **jamais toucher** |

⛔ La copie `.codex/` est hors périmètre pour deux raisons cumulatives : sous Codex, `block` sur `Stop` a la sémantique **inversée** (= forcer la continuation, cf [[comment-creer-hook-codex]]), et `.codex/`/`.agents/` est le miroir géré par Raphael (décision du 27 juil., cf `reference_agents_dir_chatgpt_mirror`).

## Clause de sortie (à re-tester, pas à supposer)

Le détecteur se supprime si l'une de ces conditions est mesurée :
- il alerte alors que la capitalisation avait bien eu lieu (faux positifs) sur ≥ 2 sessions ;
- il reste silencieux sur une session où un apprentissage a manifestement été perdu (faux négatifs) ;
- un mécanisme en pré-action couvre déjà le cas de façon fiable.

**Mesure, pas impression** : `search_sessions` sur les alertes émises vs les captures réelles. C'est l'instrument qui a tranché ce pivot ; `git log` sur `memory/` ne peut pas le faire (un commit est indiscernable selon sa cause).

## Historique — décision du 29 mai 2026 (remplacée)

Audit `.claude/` multi-repo du 29 mai flaguait 2 Stop hooks forge comme drift doctrinal. Discriminateur appliqué alors : `decision:block` = enforcement workflow = drift 22 mai ; `additionalContext`/exit 0 = acceptable.

| Hook | Décision de mai | Statut aujourd'hui |
|---|---|---|
| `proactivity-reminder.py` | **SUPPRIMÉ** (behavior-shaping, zéro payoff) | reste supprimé — décision confirmée |
| `learning-reminder.py` | **GARDÉ**, exception assumée (« Raphael n'exécute pas `/done` de façon fiable ») | **remplacé par la V2 détecteur** |

Le sujet a été rouvert **trois fois** (29 mai : GARDÉ · 17 juin : « proche de la ligne mais KEEP » · roadmap juil. item 31 : « garder OU convertir en `additionalContext` », jamais exécuté). C'est le pattern [[feedback_recurring_meta_anti_pattern]] : revisiter ≥ 2 fois signale l'absence d'une décision écrite qui **clôt** le sujet. Cette note est cette décision — elle porte la clause de sortie mesurable ci-dessus pour éviter un quatrième passage.

## Liens

- [[raisonnement-22mai-doctrine-vs-enforcement]] — doctrine hooks = lint/security/scope
- [[comment-creer-hook]] — `stop_hook_active` obligatoire, exit 0 + JSON sur Stop
- [[comment-creer-hook-codex]] — sémantique `block` inversée sous Codex
- [[erreur-hooks-bash-quoting-windows]] — précédent de boucle infinie sur ce hook
- [[feedback_recurring_meta_anti_pattern]] — revisiter ≥ 2 fois = décision manquante
- [[devils-advocate-pipeline]] — le sibling `devil-advocate-stop`, supprimé au pivot 22 mai
