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

**Pourquoi c'est non négociable** : un audit produit 20 à 50 findings d'un coup avec une autorité apparente haute (`file:line`, ton assuré). Relayer sans mesurer propage des faux à l'échelle — et si l'audit débouche sur un nettoyage, chaque faux devient une suppression.

📎 **3 cas réels mesurés + le raisonnement long** : `docs/doctrine/post-dispatch-cas-reels.md` (chemin « mort » qui existait sur l'autre PC · « repo » qui était un conteneur de 10 repos · deny global inventé, jamais lu). À lire quand un audit produit des findings à relayer.

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

Un frontmatter présent peut être **cassé** : le motif deux-points-espace dans un scalaire YAML non quoté (`Modes: mode=audit`) lève une `ScannerError` et rend le composant **invisible silencieusement**. Après toute création/modification de composant, **parser** le YAML plutôt que le regarder — `check-frontmatter.py` ci-dessous.

## Les trois findings mécanisables — script, pas jugement

Ces trois-là ne demandent aucune interprétation : un script les tranche en exit 0/1, donc ils ne dépendent plus de ma discipline. Chaînables avant un commit (`py … && git commit`) — un script qui *imprime* l'erreur mais sort en 0 laisse passer le commit, constaté le 29 juil.

```bash
py .claude/scripts/check-frontmatter.py && py .claude/scripts/check-refs.py && py .claude/scripts/check-portability.py
```

| Script | Ce qu'il tranche | Mode d'échec évité |
|---|---|---|
| `check-frontmatter.py` | frontmatter YAML invalide (motif `: ` dans un scalaire non quoté) | composant **invisible silencieusement** |
| `check-refs.py` | un texte route vers un agent/skill inexistant | routage qui échoue à l'invocation, sans erreur |
| `check-portability.py` | chemin absolu utilisateur · hook en `python` au lieu de `py` · hook sans `timeout` | casse sur l'autre machine, souvent en silence |

Chacun accepte un chemin de repo en argument (`py .claude/scripts/check-refs.py ../neot-v2/neo_ia`) — utile pour les repos voisins qui n'embarquent pas les scripts.

⚠️ `check-refs.py` ne couvre que les citations en **contexte de routage** — son silence ne prouve pas l'absence de toute référence morte (détail + le pourquoi des 108 faux positifs : `docs/doctrine/post-dispatch-cas-reels.md`).

Le reste (« ce finding est-il pertinent ? », « cette inférence tient-elle ? ») n'est pas mécanisable : un script peut vérifier qu'une colonne « Mesure » existe, jamais que la mesure a réellement été faite.

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
