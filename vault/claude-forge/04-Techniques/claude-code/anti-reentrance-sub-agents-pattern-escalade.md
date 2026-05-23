---
titre: "Anti-ré-entrance sub-agents Claude Code — pattern d'escalade vers session principale"
resume: "Doctrine Anthropic : un sub-agent ne peut PAS invoquer un autre sub-agent via le tool Agent (risque boucle infinie + tool_use conflits). Solution = pattern STOP + signal d'escalade markdown structure vers la session principale qui orchestre. Format ESCALADE REQUISE standardise pour neo_ia."
aliases:
  - "anti reentrance sub agents"
  - "sub-agent ne peut pas invoquer sub-agent"
  - "escalade session principale"
  - "ESCALADE REQUISE format"
  - "sub-agent cannot call sub-agent"
  - "re-entrance prevention claude code"
  - "pattern escalade neo_ia"
  - "session principale orchestre"
derniere-maj: 2026-05-23
auteur: claude
type: technique
sources:
  - "[[comment-creer-agent]] canonique forge — section Architecture anti-pattern"
  - "Doctrine Anthropic Agent SDK : 'Claude decides when to invoke subagents'"
  - "Session 23 mai 2026 neo_ia — detection in-situ par Raphael"
  - "Boris Cherny Pragmatic Engineer — thinnest wrapper, secret sauce dans le modele"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/agents"
  - "#doctrine/2026"
---

# Anti-ré-entrance sub-agents Claude Code — pattern d'escalade

> Note canonique forge — solution au probleme de re-entrance des sub-agents, decouvert sur neo_ia 23 mai 2026.

---

## QUOI — Definition

**Sub-agent ré-entrance** = un sub-agent (lance via le tool `Agent` depuis la session principale) qui tente d'invoquer un autre sub-agent via le tool `Agent` lui aussi.

**Pourquoi c'est interdit (doctrine Anthropic)** :
- **Boucle infinie potentielle** — agent A appelle B qui appelle A qui...
- **tool_use partages conflictuels** — les tool_use_id ne sont pas isoles entre les niveaux d'imbrication
- **Contexte explose** — chaque sub-agent a son propre window de contexte, l'imbrication multiplie la consommation
- **Debugging impossible** — transcripts JSONL fragmentes, traces croisees

**Règle Anthropic implicite** ([[comment-creer-agent]] canonique forge, section Architecture anti-pattern) :
> Un sub-agent ne devrait pas avoir le tool `Agent` sauf cas explicite documente. La session principale orchestre.

---

## POURQUOI — Le probleme observe sur neo_ia

Session 23 mai 2026, refactor `dev-neochat.md` :
- J'avais ecrit dans le scope : "Hors scope → **deleguer** a `dev-shared-utils` ou `dev-shared-tools`"
- Raphael a detecte : "un sub-agent peut pas appeler de sub-agent je crois comment résoudre le souci ?"

Le mot "deleguer" suggerait implicitement que dev-neochat (sub-agent) pouvait invoquer dev-shared-utils (autre sub-agent). **Faux selon doctrine**.

Audit complet 3 dev-app sur neo_ia :
- `dev-neochat.md` : "Hors scope (deleguer)" → 4 occurrences nominatives d'autres agents
- `dev-shared-utils.md` (cree session 3) : "HORS scope (rediriger)" → 4 occurrences nominatives
- `dev-neodoc.md`, `dev-neomail.md`, `dev-shared-tools.md` : pas de formulation problematique (chance)

---

## COMMENT — Pattern d'escalade canonique

### Principe

Le sub-agent **detecte** qu'une tache est hors scope, **arrete** son travail, et **retourne un signal structure** a la session principale. La session principale lit le signal et invoque le bon sub-agent (ou continue elle-meme).

```
Session principale
    │
    │ Agent(subagent_type="dev-neochat")
    ▼
dev-neochat
    │
    │ Detection : tache touche API publique shared_utils
    │ Action : STOP + emet ESCALADE REQUISE markdown
    │
    ▼
Session principale (lit l'escalade)
    │
    │ Agent(subagent_type="dev-shared-utils")
    ▼
dev-shared-utils
```

PAS d'invocation directe dev-neochat → dev-shared-utils.

### Format standard "ESCALADE REQUISE"

A inclure dans la reponse finale du sub-agent quand il detecte hors scope :

```markdown
## ESCALADE REQUISE

**Detection** : <description precise de la tache hors scope>
**Raison** : <pourquoi c'est hors scope dev-X>
**Agent recommande** : `<sub-agent cible>` (OU `architect-deep` si breaking change)
**Etat actuel** : <fichiers touches jusqu'ici, etat du repo, branche, dirty/clean>
**Suite recommandee** : <prompt pret-a-l'emploi pour la session principale qui invoquera l'agent suggere>
```

### Champs obligatoires

| Champ | Pourquoi |
|-------|----------|
| **Detection** | La session principale doit comprendre immediatement ce qui est hors scope. Pas d'ambiguite. |
| **Raison** | Justification doctrinale. Permet de challenger ("non c'etait dans scope") sans ping-pong. |
| **Agent recommande** | Decision deja prise par le sub-agent → session principale n'a qu'a executer. |
| **Etat actuel** | Sans ca, le sub-agent suivant repart de zero → contexte perdu. |
| **Suite recommandee** | Prompt copy-paste-ready → 0 friction pour la session principale. |

---

## QUAND — Critère d'application

### Le sub-agent doit emettre ESCALADE REQUISE quand :

- Modification touche **API publique** d'un module consomme par d'autres apps (signature, contract retour, exception types)
- **Cross-app refactor** detecte (libs + 2+ apps en meme PR)
- **Breaking change** structurel (renames, suppression module, schema DB)
- **Domaine d'expertise specifique** d'un autre sub-agent (ex: dev-neochat touche shared_tools pour ajout structurel d'un tool → dev-shared-tools mieux equipe)
- **Architecture nouvelle** (nouveau module, nouveau pattern) → architect-deep d'abord

### Le sub-agent peut continuer (touche locale OK) quand :

- Ajout d'un exemple `config.yaml` pour un tool deja existant
- Fix d'un bug interne d'un handler (pas l'API publique)
- Ajout de tests unitaires
- Documentation locale

**Regle d'or** : si la modif change ce que les **autres apps** voient quand elles importent le module → ESCALADE. Si ca reste invisible aux autres apps → continue.

---

## WORKFLOW — Integration dans agent.md

### Section "Hors scope" du sub-agent

```markdown
**Hors scope (STOP + escalade session principale)** :

Un sub-agent ne peut PAS invoquer un autre sub-agent (doctrine Anthropic anti-re-entrance — risque boucle infinie + tool_use conflits). Quand tu detectes une tache hors scope, tu **arretes** et **retournes un signal d'escalade** a la session principale.

Cas d'escalade :
- <Cas 1> → suggerer `<agent-cible>`
- <Cas 2> → suggerer `<agent-cible>`
- <Cas N> → suggerer `<agent-cible>`

**Format du signal d'escalade** :

\`\`\`markdown
## ESCALADE REQUISE

**Detection** : ...
**Raison** : ...
**Agent recommande** : `...`
**Etat actuel** : ...
**Suite recommandee** : ...
\`\`\`

La session principale lit ce bloc et orchestre la suite. Toi tu **NE TENTES PAS** d'invoquer l'autre agent via le tool Agent — c'est interdit par doctrine.
```

### Section "Tools" du sub-agent

NE PAS inclure `Agent` dans le frontmatter `tools:`. Les sub-agents standard n'ont PAS ce tool.

Exception : si vraiment un sub-agent doit pouvoir spawn d'autres sub-agents (cas tres rare type "orchestrateur de tests parallèles"), documenter explicitement la raison et accepter le risque.

---

## OPTIMISATION — 3 niveaux

### Niveau basique

- Formulation "STOP + escalade" dans la section Hors scope
- Format ESCALADE REQUISE en markdown structure

### Niveau avance

- + Detecter en early-stop (avant 5+ ops gaspillees sur du hors-scope)
- + Inclure les fichiers deja touches dans "Etat actuel" pour eviter le travail double
- + Prompt "Suite recommandee" pret-a-l'emploi avec tous les params necessaires

### Niveau expert

- + Hook `SubagentStop` qui detecte automatiquement "## ESCALADE REQUISE" dans la sortie et logge dans CSV pour mesurer les patterns d'escalade frequents → revele que certaines limites de scope sont mal definies si trop d'escalades sur le meme axe.
- + Session principale qui automatise la suite : lire ESCALADE REQUISE → spawn directement l'agent recommande avec le prompt fourni (orchestration semi-automatique)

---

## POURQUOI CETTE OPTIM — Gain mesurable

| Optim | Gain |
|-------|------|
| Anti-re-entrance respecte | 0 boucle infinie, 0 tool_use conflict, debugging clair |
| Format ESCALADE structure | Session principale lit + decide sans avoir besoin de re-analyser |
| Etat actuel inclus | Le prochain sub-agent n'a pas a refaire le travail deja fait |
| Suite recommandee prompt-ready | Friction quasi-zero pour la session principale |

---

## ANTI-PATTERNS

### Doctrinaux
- ❌ **Mot "deleguer" dans agent.md** sans expliciter le pattern d'escalade → ambiguite → le LLM peut tenter d'invoquer un autre agent
- ❌ **Tool `Agent` dans frontmatter sub-agent** sans documentation explicite du cas d'usage
- ❌ **Pattern "redirige vers X"** → suggere implicitement une invocation, donc faux. Preferer "STOP + escalade vers session principale qui invoquera X"

### Techniques
- ❌ **Pas d'etat actuel dans ESCALADE** → travail double, le suivant repart de zero
- ❌ **Suite recommandee vague** ("voir avec dev-shared-utils") → la session principale doit re-construire le prompt
- ❌ **Detection tardive** (apres 50 ops sur hors-scope) → coût massif, detecter au plus tot

### Comportementaux
- ❌ **Sub-agent qui force le scope** ("je vais le faire quand meme") → risque casser API publique
- ❌ **Sub-agent qui ignore et continue** sans signaler → la session principale ne sait pas
- ❌ **Sub-agent qui invoque quand meme `Agent`** malgre l'interdiction → boucle ou crash silencieux

---

## EXEMPLES CONCRETS

### Exemple 1 — dev-neochat detecte breaking change shared_utils

Tache utilisateur : "ajoute un nouveau champ a `BaseAgentState` pour le tracking de latence"

dev-neochat detection :
- `BaseAgentState` est dans `packages/shared_utils/shared_utils/engine/state.py`
- Modifier sa signature = breaking change pour `apps/neodoc` et `apps/neomail` qui consomment
- Hors scope dev-neochat

Sortie dev-neochat :

```markdown
## ESCALADE REQUISE

**Detection** : Ajout champ `latency_ms` a `BaseAgentState` TypedDict dans `packages/shared_utils/shared_utils/engine/state.py`

**Raison** : `BaseAgentState` est l'API publique du Declarative ReAct Engine, consomme par les 3 apps (neochat, neodoc, neomail). Modifier sa signature = breaking change cross-app. Doctrine `dev-neochat` : limite a `apps/neochat/` + touches locales `packages/shared_*/`. API publique = hors scope.

**Agent recommande** : `architect-deep` d'abord (pour valider l'impact des 3 apps), puis `dev-shared-utils` pour l'implementation.

**Etat actuel** : 0 fichier touche. Branche `develop` clean.

**Suite recommandee** : Invoquer `architect-deep` avec ce prompt :
"Analyser l'impact d'ajouter un champ `latency_ms: float` a `BaseAgentState` (`packages/shared_utils/shared_utils/engine/state.py`). Verifier les 3 apps consommatrices (neochat, neodoc, neomail) : faut-il rendre le champ optionnel ? Faut-il une migration ? Output : plan d'implementation step-by-step pour `dev-shared-utils`."
```

Session principale lit, spawn `architect-deep`, recoit plan, spawn `dev-shared-utils` avec le plan.

### Exemple 2 — dev-shared-utils detecte cross-app refacto

Tache : "rename `BaseAgentState.messages` en `BaseAgentState.history`"

dev-shared-utils :
- Modification dans `packages/shared_utils/shared_utils/engine/state.py` ✅ scope OK
- MAIS impact direct sur les 3 apps qui referencent `state["messages"]` ⚠️ cross-app
- Doctrine : modif `shared_utils/` OK, mais "Si breaking API publique → architect-deep d'abord"

Sortie :

```markdown
## ESCALADE REQUISE

**Detection** : Rename `BaseAgentState.messages` → `BaseAgentState.history`

**Raison** : Cle TypedDict referencee dans les 3 apps (`state["messages"]` apparait dans ~40 fichiers neochat + neodoc + neomail). Cross-app refactor requiert dev-lead pour orchestrer en 1 PR.

**Agent recommande** : `dev-lead`

**Etat actuel** : 0 fichier touche. Branche `develop` clean.

**Suite recommandee** : Invoquer `dev-lead` avec ce prompt :
"Refactor cross-app : rename `BaseAgentState.messages` -> `BaseAgentState.history` (TypedDict dans `packages/shared_utils/shared_utils/engine/state.py`). Etapes : (1) modifier le TypedDict, (2) grep + rename dans 3 apps neochat/neodoc/neomail, (3) tests unit par app, (4) test integration end-to-end. 1 PR atomique."
```

---

## SOURCES — Verbatim avec URLs

- **Anthropic Agent SDK** ([code.claude.com/docs/en/agent-sdk/overview](https://code.claude.com/docs/en/agent-sdk/overview)) — "Claude decides when to invoke"
- **Anthropic Building agents** ([anthropic.com/engineering/building-agents-with-the-claude-agent-sdk](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk))
- **Boris Cherny Pragmatic Engineer** — thinnest wrapper, secret sauce dans le modele
- **[[comment-creer-agent]] canonique forge** — section Architecture anti-pattern
- **[[raisonnement-22mai-doctrine-vs-enforcement]]** — doctrine 22 mai : Claude decides, pas hook

---

## GOTCHAS — Pieges observes

### Pieges formulation
- **Mot "deleguer"** ambigu → preferer "STOP + escalade"
- **Mot "rediriger"** ambigu → meme probleme
- **"Voir avec X"** vague → preciser le format ESCALADE REQUISE

### Pieges detection
- **Detection tardive** (apres travail commence) → coût ops gaspillees. Detecter au PLAN, pas au CODE.
- **Detection trop large** (escalade pour tout) → bloque le sub-agent, friction
- **Pas de critere clair "touche locale" vs "API publique"** → ambiguite continue

### Pieges format
- **Etat actuel manque** → le suivant repart de zero
- **Suite recommandee vague** → la session principale re-construit
- **Pas d'agent recommande precis** → choix difficile pour la session principale

### Pieges session principale
- **Ignore le bloc ESCALADE REQUISE** → le sub-agent suivant ne sait pas
- **Re-spawn le meme sub-agent** sans changer le prompt → boucle
- **Override la recommandation** sans raison → casse le pattern, sub-agent stoppera la prochaine fois sur la meme detection

---

## ALIASES — Findability

Aliases declares en frontmatter (8) :
- anti reentrance sub agents
- sub-agent ne peut pas invoquer sub-agent
- escalade session principale
- ESCALADE REQUISE format
- sub-agent cannot call sub-agent
- re-entrance prevention claude code
- pattern escalade neo_ia
- session principale orchestre

---

## WIKILINKS

### Notes canoniques sœurs
- [[comment-creer-agent]]
- [[comment-creer-skill]]
- [[comment-creer-hook]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]

### Knowledge / refs
- [[raisonnement-22mai-doctrine-vs-enforcement]]
- [[architecture-decision-niveaux-mesure-agents]]
- [[feedback_methode_abcde_carte_pas_verdict]]
- [[niveau-1-static-mesure-agents-neo-ia-2026-05-22]]

### Forge custom
- [[agent-creator]]
- [[devils-advocate-pipeline]]

---

**Fin note canonique `anti-reentrance-sub-agents-pattern-escalade.md`** — chantier 23 mai 2026.
