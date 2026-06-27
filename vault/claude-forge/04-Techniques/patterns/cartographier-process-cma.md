---
titre: "Cartographier ses process — méthode CMA (Clarifier · Mapper · Amplifier)"
resume: "Méthode amont : inventorier ses process récurrents par fréquence, les formaliser en fiche process, trancher agent-vs-automatisation, puis router vers la bonne brique (loop-forge si boucle Claude Code, n8n si automatisation externe). Distincte de besoin→capability (une brique) — ici on cartographie un portfolio de process."
aliases:
  - "cartographier process CMA"
  - "fiche process"
  - "clarifier mapper amplifier"
  - "arbre agent vs automatisation"
  - "mapping process par fréquence"
  - "contexte statique dynamique méthode"
type: technique
domaine: patterns
status: active
derniere-maj: 2026-06-27
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/patterns"
  - "#domaine/claude-code"
  - "#domaine/agents"
sources:
  - "https://www.youtube.com/watch?v=IubQUC9TL2w (Eliott Meunier — L'IA devient simple avec un Second Cerveau IA, cours complet)"
  - "memory/reference_eliott_meunier_prisme.md"
---

## Quand utiliser cette note

Déclencheur : **« j'aimerais déléguer / automatiser mon quotidien à l'IA mais je ne sais pas par où commencer »**. Cette note est l'étape **amont** : on inventorie *tous* ses process récurrents, on les priorise, et pour chacun on tranche **agent ou automatisation**, AVANT de construire la brique.

Frontière nette avec les notes voisines (vérifiée 27 juin) :
- [[methode-monter-systeme-workflow]] = « pour CE besoin précis, quelle brique (skill/agent/hook/MCP) ? ». Une brique à la fois.
- **Cette note** = « quels sont TOUS mes process, lesquels valent l'investissement, agent ou automatisation ? ». Un **portfolio** de process.
- Une fois le verdict rendu, on **route** (voir § Routage) vers la skill `loop-forge` (cible = boucle Claude Code) ou vers [[n8n-self-host-mcp-claude]] (cible = automatisation externe).

## La méthode CMA

| Étape | Question | Sortie |
|---|---|---|
| **C — Clarifier** | Qui suis-je, quel contexte, quels process ? | Le contexte (cf structure IPCRA, [[architecture-cerveau-obsidian-mcp]]) |
| **M — Mapper** | Quels process je refais ≥ 1×, à quelle fréquence ? | L'inventaire + 1 fiche process par item retenu |
| **A — Amplifier** | Agent ou automatisation pour chacun ? | La brique créée (route vers loop-forge / n8n / créateur) |

> Verbatim utile : *« 80 % des implémentations IA en entreprise échouent (étude MIT citée) parce qu'on saute la phase process-driven. »* Le mapping explicite est ce qui manque, pas l'outil.

## Mapper par fréquence (les 5 catégories de trigger)

On classe par fréquence parce que **la fréquence révèle le ROI** et conditionne le type d'implémentation :

- **Daily** — traiter mails, checker métriques, traiter l'inbox
- **Weekly** — newsletter, revue de projets, contenu
- **Monthly** — facturation, analytics, planification
- **On-trigger** — événement déclenche une suite (nouveau client → onboarding ; bug signalé → fix)
- **Manuel / ponctuel** — lancement produit, revue annuelle, refonte site

## La fiche process

Pour chaque process retenu, une fiche :

| Champ | Contenu |
|---|---|
| Nom | Le process |
| Fréquence + déclencheur | daily/weekly/… + ce qui le lance |
| Temps actuel | minutes/heures par exécution manuelle (→ justifie l'investissement) |
| **Input statique** | ce qui ne change pas (style, gabarit, qui je suis) |
| **Input dynamique** | données du jour propres à cette exécution (notes de la semaine, dernier call, base clients) |
| Étapes | la suite d'actions |
| **Méthode** | *l'élément le plus important* — comment je fais ça bien (mes critères qualité, ce que je fais toujours/jamais). À expliciter via coach / livre / formation si on ne l'a pas en tête |
| Output + exemples | format attendu + 1 bon exemple, 1 mauvais exemple |

> La **méthode** est le cœur de valeur : l'IA suit des étapes facilement, mais elle a une méthode *basique* par défaut. Expliciter la meilleure méthode du marché = ce qui transforme un exécutant médiocre en livrable de qualité reproductible.

## Anatomie de la brique : statique / dynamique / méthode

Toute brique (slash command, agent, workflow) se compose des 3 mêmes éléments — c'est la grille de relecture quand on en conçoit une :

1. **Contexte statique** — étapes, style, comportement attendu, qui est l'utilisateur (vit dans le SKILL.md / l'agent .md).
2. **Contexte dynamique** — données de l'exécution courante, récupérées à la volée (fichiers vault, base de données, API, MCP, web). Jamais de copier-coller : la brique va chercher.
3. **Méthode** — la recette qualité explicite.

## Arbre de décision — agent vs automatisation

Distinct de l'arbre besoin→capability de [[methode-monter-systeme-workflow]] : ici on décide le **mode d'exécution** d'un process déjà mappé.

```
Le déclencheur est-il automatique ?
   └─ NON (manuel) ────────────────→ AGENT supervisé (slash command lancée à la main)
   └─ OUI ↓
Y a-t-il une intervention humaine ?
   └─ OUI, c'est du JUGEMENT complexe → AGENT supervisé (ou automatisation partielle)
   └─ OUI, simple VALIDATION ────────→ AUTOMATISATION avec validation (draft généré, humain approuve)
   └─ NON, aucune intervention ──────→ AUTOMATISATION pure (tourne seule)
```

## Routage forge — où créer la brique une fois le verdict rendu

| Verdict | Cible | Où aller |
|---|---|---|
| Agent supervisé / boucle récurrente exécutée par Claude Code | inner-loop, `/loop`, `/goal`, slash command | skill `loop-forge` → spec, puis créateur (cf [[concevoir-loops-travail]]) |
| Automatisation externe (webhook/schedule, tourne sans Claude dans la boucle) | workflow n8n self-host | [[n8n-self-host-mcp-claude]] |
| Brique unitaire isolée (1 transformation, 1 garde, 1 connecteur) | skill / agent / hook / MCP | [[methode-monter-systeme-workflow]] + skill `cc-advisor` |

## Priorisation (ne pas tout faire d'un coup)

1. Lister les ~10 process les plus chronophages.
2. Classer chacun avec l'arbre (agent / automatisation / déjà couvert).
3. Matrice impact × effort → commencer par le quadrant **fort impact / facile**.
4. Implémenter process par process, quick wins d'abord.

## Liens

- [[methode-monter-systeme-workflow]] — méthode sœur : besoin → quelle brique (une à la fois)
- [[concevoir-loops-travail]] — canonique derrière la skill `loop-forge` (cible boucle Claude Code)
- [[n8n-self-host-mcp-claude]] — cible automatisation externe
- [[architecture-cerveau-obsidian-mcp]] — la couche contexte (IPCRA) sur laquelle CMA s'appuie
- [[pattern-vault-llm-karpathy]] — anti-dérive de la couche d'interconnexion
