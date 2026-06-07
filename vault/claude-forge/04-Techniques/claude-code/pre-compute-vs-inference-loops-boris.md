---
titre: "Pre-compute vs inference — pourquoi écrire des loops (Boris Acquired juin 2026)"
resume: "Principe doctrinal Boris Cherny : 3 niveaux d'abstraction (écrire le code → prompter Claude → écrire des loops qui promptent Claude). Fondement = pre-compute > inference : faire écrire au modèle un programme rejouable gratuitement plutôt que re-sampler à chaque tâche. Source primaire podcast Acquired transcrit 5 juin 2026."
aliases:
  - "pre-compute vs inference"
  - "my job is to write loops"
  - "boris loops"
  - "trois niveaux abstraction coding"
  - "pre-compiling tokens"
  - "under-fund everything boris"
  - "couple hundred claudes running"
derniere-maj: 2026-06-05
auteur: claude
type: technique
sources:
  - "Podcast Acquired (Ben Gilbert + David Rosenthal) — interview Boris Cherny, partagé via x.com/0xCodez/status/2062464183409545224 le 4 juin 2026"
  - "Transcription Whisper de la vidéo native X (30 min), forge 5 juin 2026"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/workflow"
  - "#doctrine/2026"
---

# Pre-compute vs inference — pourquoi écrire des loops

> Note canonique forge — fondement théorique de la pratique des routines / `/loop` / Dynamic Workflows, énoncé par Boris Cherny au podcast Acquired (juin 2026). Source primaire transcrite, pas la paraphrase du tweet @0xCodez qui survend une « démo daily setup » (c'est en réalité une interview origin-story).

---

## QUOI — Les 3 niveaux d'abstraction du coding

Boris décrit sa propre montée en abstraction sur ~1 an (verbatim 10:58-11:53) :

| Niveau | Description | Qui déclenche ? |
|--------|-------------|-----------------|
| **1. Écrire le code** | Toi + autocomplétion IDE | Toi, ligne par ligne |
| **2. Prompter Claude** | Tu demandes une feature, Claude écrit. 5-10 Claudes en parallèle | Toi, à chaque tâche |
| **3. Écrire des loops** | Des programmes tournent en continu et promptent Claude à ta place | Le loop, en autonomie |

**Verbatim clé** :
> "In November, I uninstalled my IDE because I wasn't using it. At that point I was running maybe five, ten Claudes in parallel and my coding was prompting Claude to write code. Now it's leveled up again to the next level of abstraction where **I don't prompt Claude anymore. I have loops that are running. They're the ones that are prompting Claude and figuring out what to do. My job is to write loops.**"

**Distinction critique** : demander une feature = niveau 2 (acte ponctuel, tu reviens pour la suivante). Un **loop** = niveau 3 : un programme qui décide tout seul *quoi* demander à Claude, en boucle, sans intervention.

### Le setup réel de Boris (verbatim 28:11)
> "Right now I have **a couple hundred Claudes running** doing stuff. A bunch are looking at **Twitter feedback, GitHub issues, Slack** and they're figuring out what to build next. Most ideas are bad, but **maybe 20% are good**. If you project out 3-6 months, most ideas will probably be good."

Loop type (reconstruction) :
```
TANT QUE (toujours) :
   1. lire nouveaux GitHub issues + tweets + Slack
   2. pour chacun → Claude juge : bonne idée de feature ?
   3. si oui (≈20%) → Claude écrit le code
   4. ouvrir une PR
   5. recommencer
```
Boris ne demande rien : il relit le matin les PRs produites par ses loops. Son seul travail = écrire/régler les loops.

---

## POURQUOI — Pre-compute > inference

C'est le fondement théorique de tout ce qui précède (verbatim 20:01-20:23) :

> "When do you want to do the computation? Do you want to do it in **real time** when you sample from the model and do inference? Or do you want to **pre-compute** so you can have the model write a program and then **run that program repeatedly — and that's free for you**. Essentially we want to do the latter as much as possible."

Analogie **pre-compiling** (Ben Gilbert, 25:09, validée par Boris) :
> "Raise your upfront costs but decrease your ongoing costs. You've done a big pile of work upfront so that the over-and-over-again tasks are easy and streamlined."

**Traduction forge** : ne re-paie pas le modèle pour re-réfléchir à chaque tâche identique. Fais-lui écrire **une fois** un artefact rejouable (programme, skill, loop), puis rejoue-le quasi gratuitement. C'est exactement le *pourquoi* derrière :
- **routines / skills** ([[workflow-claude-code-optimal]]) — écris la règle une fois, le modèle la réutilise à l'infini
- **`/loop`** — la boucle s'exécute sans re-prompt humain
- **PTC** ([[programmatic-tool-calling]]) — « 20 tool calls = 1 inference »
- **Dynamic Workflows** ([[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]]) — le script JS pré-calcule l'orchestration

Boris explicite aussi le lien principes → skills (verbatim 24:25) :
> "It's really good to have a set of principles so you don't have to make ad hoc decisions every time. The model can use these principles also, and **it comes in the form of skills**."

---

## QUAND — Monter d'un niveau

- Niveau 2 (prompter Claude) = parfaitement productif, défaut sain pour la majorité des tâches.
- Passer au niveau 3 (loop) seulement pour des **tâches répétitives bien définies** où le déclencheur et le critère de succès sont clairs (surveiller des tickets, trier des feedbacks, régénérer un artefact). Une feature one-shot N'EST PAS un candidat loop.

---

## Conseil org/budget associé (verbatim 23:33-24:18)

- "Give everyone **as many tokens as possible**, let them experiment."
- "To quote Jensen: **the more you buy, the more you save**."
- "**Under-fund everything a little bit.** Projet qui demande 4 ingénieurs → mets-en 2 + plein de tokens, ils trouveront quoi automatiser. Compounding : moins de ressources humaines force l'automatisation, et c'est moins cher la fois d'après."
- Shift budget **humains → tokens** : raise upfront cost, decrease ongoing cost.

---

## Autres points de l'interview (contexte, peu actionnable forge)

- **Origin story** : équipe Labs fin 2024, « product overhang », coding = Petri dish pour étudier la sûreté (« we exist to research AI safety »).
- **Métriques** : code/ingénieur ×3 « very outdated, beaucoup plus maintenant » ; ramp-up new hire 2 jours vs semaines.
- **Org** : « golden age of the generalist », fusion eng/PM/designer/researcher « gone by end of year », titre unique « member of technical staff ».
- **Taste** : son dogme « no classes, only functions » → le modèle écrivait des classes → « maybe the model's right ». Le product taste = l'alpha aujourd'hui, « but this is also going to go away ». Dernier rempart humain = **enseigner les valeurs au modèle** (« the way we teach our kids to be good people »).
- **Co-work** : construit en ~8-9 jours, 100% en Claude Code, déclenché parce qu'un non-eng (David d'Acquired) a dû ouvrir un terminal.

---

## Anti-pattern source

⚠️ Le tweet @0xCodez (« in 30 minutes Boris reveals his actual daily Claude Code setup… worth more than a $500 vibe-coding course ») **survend** : c'est une interview podcast origin-story, pas une démo de config. Pattern tweet-hype connu — transcrire la source primaire plutôt que capitaliser la paraphrase. Cf [[feedback_tweet_hype_paraphrase_pattern]].

---

## WIKILINKS

- [[Boris Cherny]] — fiche leader
- [[workflow-claude-code-optimal]] — routines, `/loop`, multi-clauding (ce principe en est le fondement)
- [[programmatic-tool-calling]] — pre-compute au niveau API
- [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] — pre-compute de l'orchestration
- [[mcp-vs-skills-doctrine]] — skills = principes rejouables
