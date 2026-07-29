---
description: "Vérification empirique obligatoire après tout dispatch d'un sub-agent qui clame avoir créé/modifié/supprimé des fichiers — ne jamais relayer le résumé sans grep/ls/diff"
---

# Vérification empirique post-dispatch — OBLIGATOIRE

Les sub-agents retournent « done » même en cas d'échec silencieux (Write denied retourne exit 0 côté Bash mais le fichier n'existe pas). La session principale DOIT vérifier empiriquement avant de relayer un résultat à Raphael.

## Checklist post-dispatch (4 points)

1. **Fichiers existent ?** — `ls -la <chemin attendu>` ou `Glob .claude/skills/<nom>/**`
2. **Contenu conforme ?** — `head -20 <fichier>` (frontmatter complet ?)
3. **Git diff confirme ?** — `git -C <repo> diff --stat` + `git -C <repo> status --short` (résoudre `<repo>` via `git rev-parse --show-toplevel`, jamais de path en dur OS-spécifique)
4. **Taille réaliste ?** — `wc -l <fichier>` (SKILL.md < 5 lignes = échec silencieux)

## Deux natures de sortie, deux vérifications

| L'agent a produit… | Ce qui peut être faux | Comment vérifier |
|---|---|---|
| des **FICHIERS** (créé/modifié/supprimé) | le fichier n'existe pas, est vide, ou le frontmatter est cassé | checklist 4 points ci-dessus |
| un **CONSTAT** (audit, analyse, finding, chiffre) | le fait affirmé est faux, ou vrai mais mal interprété | § Vérifier un CONSTAT ci-dessous |

Le second cas est le plus dangereux : rien n'échoue, rien n'est vide, le rapport est bien écrit — et le fait est faux. C'est ce qui rend la vérification **plus** nécessaire sur un audit que sur une création.

## Vérifier un CONSTAT d'audit — quoi, quand, pourquoi

**Le principe** : un agent d'audit rapporte ce qu'il a **déduit** de ce qu'il a lu. Entre le fichier et son verdict il y a une inférence, et c'est l'inférence qui casse. Reproduire soi-même la mesure la plus courte qui tranche le verdict.

**Vérifier AVANT de relayer ou d'agir** (bloquant) :

| Type de finding | Mesure qui tranche |
|---|---|
| « le fichier X n'existe pas » / « chemin mort » | `ls -d <chemin>` — et se demander *sur quelle machine* (cf `git-multi-repo.md` : 2 PC, arborescences différentes) |
| « X est un repo / un composant » | `ls -d <X>/.git` — un dossier n'est pas un repo |
| « le champ est vide / absent » | `Read` direct du frontmatter — une liste YAML multi-lignes se lit comme « vide » |
| chiffre, seuil, compteur | recompter soi-même (`wc -l`, `grep -c`, parse du fichier de config) |
| « la garde/le deny existe » | lire la définition (`settings.json`, code du hook) — cf `feedback_diagnostic_empirique_avant_affirmer_garde` |
| « aucune occurrence » / « tout est conforme » | grep de validation — cf `feedback_verify_exhaustive_claims` |
| citation d'une source externe | relire la source **dans sa section** (un exemple n'est pas une assertion ; vérifier le périmètre) |

**Ne pas re-vérifier** (coût sans gain) : une opinion de conception (« cette skill gagnerait à être découpée »), une recommandation, un jugement de priorité. Il n'y a pas de fait à mesurer — c'est un avis, à discuter, pas à confirmer.

**Le déclencheur pratique** : si le finding va provoquer une **action irréversible** (suppression, réécriture, `git rm`) ou une **affirmation à Raphael**, il se vérifie. S'il alimente une discussion, non.

**Pourquoi c'est non négociable sur un audit de repo** : un audit produit 20 à 50 findings d'un coup, et son autorité apparente est haute (rapport structuré, `file:line`, ton assuré). Relayer sans mesurer, c'est propager des faux à l'échelle — et si l'audit débouche sur un plan de nettoyage, chaque faux devient une suppression.

**Trois cas réels, session du 29 juil. 2026** — mêmes agents, aucun fichier écrit, trois faits faux :

1. « chemin mort `Documents/ia_back` » → le chemin existe **sur l'autre PC** de Raphael. Le fait mesuré (« absent ici ») était juste ; l'interprétation (« erroné ») était fausse.
2. « repo fantôme `lojii/neofront` » → le dossier existe. `ls -d neofront/.git` a tranché : ce n'est pas un repo, c'est un **conteneur de ~10 repos**. Deux erreurs opposées corrigées par une seule mesure.
3. « `git merge *` est en deny global intentionnel » (écrit dans un feedback depuis mai) → parse de `settings.json` : **0 entrée deny**. Une intention rassurante avait été fabriquée pour une garde jamais lue.

Aucun des trois n'aurait été attrapé par la checklist « fichiers » : aucun fichier n'était en jeu.

## Par type d'agent

| Agent | Vérifier |
|---|---|
| skill-creator | `ls .claude/skills/<nom>/SKILL.md` + `wc -l > 20` |
| subagent-creator | `ls .claude/agents/<nom>.md` + frontmatter complet |
| hook-creator | `ls .claude/hooks/<nom>.py` + `grep exit 2` |
| claudemd-creator | `wc -l CLAUDE.md` + diff avant/après |
| **repo-inspector / Explore / agent d'audit** | **§ Vérifier un CONSTAT** — les findings bloquants et tout fait chiffré, avant de relayer |
| tout agent | `git diff --stat` pour confirmer les fichiers touchés |

## Valider un frontmatter, pas seulement sa présence

Un frontmatter présent peut être **cassé** : le motif deux-points-espace dans un scalaire YAML non quoté (`Modes: mode=audit`, `date : 25 juillet`) lève une `ScannerError` et rend le composant **invisible silencieusement**. 9 composants étaient dans cet état le 29 juil. 2026, dont 7 antérieurs à la session.

Après toute création/modification de composant, parser le YAML plutôt que le regarder :

```bash
py .claude/scripts/check-frontmatter.py
```

Le script sort en **1** si un frontmatter est cassé, ce qui permet `py .claude/scripts/check-frontmatter.py && git commit …` : le commit ne part pas si un composant est invisible. Un script qui *imprime* l'erreur mais sort en 0 laisse passer le commit — constaté le 29 juil. (le commit est parti malgré l'échec affiché).

## Anti-patterns

- « Le sub-agent a dit done » → non. exit 0 ≠ succès. Vérifier empiriquement.
- Relayer le résumé sub-agent sans grep/ls → régression silencieuse.
- « Je vois le résultat dans la conversation » → le sub-agent peut avoir affiché le PRÉVU sans avoir écrit.
- Skipper la vérif sur agents « fiables » → tous échouent silencieusement sur Write denied.
- Relayer un finding d'AUDIT sans Read direct du fichier incriminé → un agent peut lire une liste YAML multi-lignes (`tools:` suivi de `- Read`) comme « champ vide » et rapporter un CRITIQUE faux (audit neo_ia 27 juil. : 2 faux positifs frontmatter). Contre-vérifier chaque finding bloquant par Read avant de le relayer ou d'agir.

## Gotchas

- Exit 0 ≠ succès : Write denied retourne exit 0 côté Bash mais le fichier n'existe pas.
- Contenu affiché ≠ contenu écrit : le sub-agent peut générer le contenu dans son output sans avoir pu le Write.
- Glob sans résultat = fichier absent (ne pas interpréter comme un bug Glob).
- `git diff` vide après agent : soit rien fait, soit changements non stagés — vérifier les deux.
- Nouvel anti-pattern de sub-agent découvert → l'ajouter dans la section Anti-patterns.
