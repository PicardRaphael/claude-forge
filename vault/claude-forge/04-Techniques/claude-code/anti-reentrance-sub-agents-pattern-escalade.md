---
titre: "Anti-ré-entrance sub-agents Claude Code — pattern d'escalade vers session principale"
resume: "Escalade vers session principale = DÉFAUT recommandé pour le hors-scope (contexte propre, coût maîtrisé, debugging lisible) via signal STOP + ESCALADE REQUISE markdown. Le nesting sous-agents est POSSIBLE depuis CC v2.1.172 (amende 16 juin) mais reste déconseillé par défaut ; enforçable par disallowedTools: Agent. Format standardisé neo_ia."
aliases:
  - "anti reentrance sub agents"
  - "sub-agent ne peut pas invoquer sub-agent"
  - "escalade session principale"
  - "ESCALADE REQUISE format"
  - "sub-agent cannot call sub-agent"
  - "re-entrance prevention claude code"
  - "pattern escalade neo_ia"
  - "session principale orchestre"
derniere-maj: 2026-06-16
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
  - "#domaine/agents"
  - "#doctrine/2026"
---

# Anti-ré-entrance sub-agents Claude Code — pattern d'escalade

> Note canonique forge — solution au probleme de re-entrance des sub-agents, decouvert sur neo_ia 23 mai 2026.

> ⚠️ **PRÉMISSE AMENDÉE (16 juin 2026)** — Le nesting de sous-agents est **POSSIBLE depuis CC v2.1.172** (foreground toute profondeur, background plafond 5). Les passages ci-dessous qui parlent d'« interdit » / « ne peut PAS invoquer Agent » sont conservés pour l'historique mais décrivent une **recommandation de design** (escalade = défaut), PAS une impossibilité technique. Lire la section « AJOUT 16 juin 2026 — AMENDE » en bas avant de citer cette note comme « impossible ».

---

## QUOI — Definition

**Sub-agent ré-entrance** = un sub-agent (lance via le tool `Agent` depuis la session principale) qui tente d'invoquer un autre sub-agent via le tool `Agent` lui aussi.

**Pourquoi c'est DÉCONSEILLÉ par défaut (recommandation forge, PAS une impossibilité depuis v2.1.172 — cf AMENDE en bas)** :
- **Boucle infinie potentielle** — agent A appelle B qui appelle A qui... *(neutralisée par v2.1.172 : foreground self-limiting, background plafonné 5)*
- **tool_use partages conflictuels** — les tool_use_id ne sont pas isoles entre les niveaux d'imbrication *(la plateforme gère désormais l'isolation)*
- **Contexte explose** — chaque sub-agent a son propre window de contexte, l'imbrication multiplie la consommation *(CONFIRMÉ par la doc — reste la vraie raison de préférer l'escalade)*
- **Debugging impossible** — transcripts JSONL fragmentes, traces croisees *(neutralisé : panel arborescent + transcripts isolés)*

**Règle Anthropic implicite** ([[comment-creer-agent]] canonique forge, section Architecture anti-pattern) :
> Un sub-agent ne devrait pas avoir le tool `Agent` sauf cas explicite documente. La session principale orchestre.

---

## POURQUOI — Le probleme observe sur neo_ia

Session 23 mai 2026, refactor `dev-neochat.md` :
- J'avais ecrit dans le scope : "Hors scope → **deleguer** a `dev-shared-utils` ou `dev-shared-tools`"
- Raphael a detecte : "un sub-agent peut pas appeler de sub-agent je crois comment résoudre le souci ?"

Le mot "deleguer" suggerait implicitement que dev-neochat (sub-agent) pouvait invoquer dev-shared-utils (autre sub-agent). À l'époque c'était impossible techniquement ; depuis v2.1.172 c'est possible, mais reste **déconseillé par défaut** (escalade > nesting pour ce cas cross-scope).

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

Le défaut forge est l'escalade : quand tu detectes une tache hors scope, tu **arretes** et **retournes un signal d'escalade** a la session principale (contexte propre, coût maîtrisé). Le nesting de sous-agents est techniquement possible (CC v2.1.172) mais NON le défaut ici — ne tente pas d'invoquer un autre agent toi-même sauf consigne explicite.

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

La session principale lit ce bloc et orchestre la suite. Toi tu **NE TENTES PAS** d'invoquer l'autre agent via le tool Agent — défaut forge (cf AMENDE : c'est un choix de design, plus une impossibilité technique).
```

### Section "Tools" du sub-agent

Pour garder un agent en leaf-node (recommandé par défaut) : déclarer une ligne `tools:` explicite SANS `Agent`, ou `disallowedTools: Agent`. ⚠️ Piège v2.1.172 : un agent qui **omet** la ligne `tools:` **hérite de `Agent`** et peut donc nester par défaut — l'omission n'est PAS neutre.

Exception : si vraiment un sub-agent doit pouvoir spawn d'autres sub-agents (cas type "reviewer qui dispatche un verifier par finding", endossé par la doc), documenter explicitement la raison. Cf AMENDE 16 juin — section « CE QU'ON PEUT FAIRE ».

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
| Escalade plutôt que nesting par défaut | contexte propre, coût maîtrisé, debugging clair |
| Format ESCALADE structure | Session principale lit + decide sans avoir besoin de re-analyser |
| Etat actuel inclus | Le prochain sub-agent n'a pas a refaire le travail deja fait |
| Suite recommandee prompt-ready | Friction quasi-zero pour la session principale |

---

## ANTI-PATTERNS

### Doctrinaux
- ❌ **Mot "deleguer" dans agent.md** sans expliciter le pattern d'escalade → ambiguite → le LLM peut tenter d'invoquer un autre agent (désormais POSSIBLE, donc l'ambiguïté coûte vraiment un nesting non voulu)
- ❌ **Omettre la ligne `tools:` sur un agent censé être leaf-node** → il hérite de `Agent` et peut nester par défaut (piège v2.1.172)
- ❌ **Pattern "redirige vers X"** → suggere implicitement une invocation. Preferer "STOP + escalade vers session principale qui invoquera X"

### Techniques
- ❌ **Pas d'etat actuel dans ESCALADE** → travail double, le suivant repart de zero
- ❌ **Suite recommandee vague** ("voir avec dev-shared-utils") → la session principale doit re-construire le prompt
- ❌ **Detection tardive** (apres 50 ops sur hors-scope) → coût massif, detecter au plus tot

### Comportementaux
- ❌ **Sub-agent qui force le scope** ("je vais le faire quand meme") → risque casser API publique
- ❌ **Sub-agent qui ignore et continue** sans signaler → la session principale ne sait pas
- ❌ **Sub-agent qui nest par réflexe** au lieu d'escalader sur un cas cross-scope → contexte explosé, orchestration illisible

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


---

## AJOUT 10 juin 2026 — La RELANCE après escalade : resume ou re-brief, jamais un prompt nu

Observé en production sur neoteem-back-ts (US1, premier `/feature`) : à chaque aller-retour escalade → réponse humaine → relance, le dev **refaisait toutes ses recherches**. Ce n'est pas un bug — chaque invocation `Agent()` démarre un contexte VIERGE, et l'escalade détruit le contexte de l'agent. Le format ESCALADE REQUISE (sections ci-dessus) protège le côté AGENT (« État actuel » + « Suite recommandée ») ; cet ajout couvre le côté SESSION PRINCIPALE (la relance).

### Doctrine de relance (2 crans)

1. **Resume d'abord** : les sub-agents sont officiellement resumables depuis **CC v2.0.28** — chaque agent a un `agent_id`, son historique vit dans `agent-<agentId>.jsonl`, et le paramètre `resume` reprend le MÊME agent avec contexte préservé. Caveat bugs connus (vérifiés juin 2026) : [#11712](https://github.com/anthropics/claude-code/issues/11712) — le transcript ne stocke PAS les prompts utilisateur qui ont initié l'agent (l'agent repris garde ses tool results mais perd le cadrage) ; [#33651](https://github.com/anthropics/claude-code/issues/33651) — perte silencieuse de messages quand la chaîne de progrès sub-agent dépasse la chaîne principale au resume. **Conséquence : même en resume, re-donner le cadrage (ticket + objectif) dans le message.**
2. **Re-brief riche en filet** (si resume indisponible ou douteux) : la relance embarque (a) le plan architect, (b) le rapport / « État actuel » du run précédent, (c) la réponse humaine, (d) les fichiers déjà identifiés — avec la consigne explicite « ne refais pas l'exploration, repars de cet état ».

### Principe directeur (convergence PubNub / registry-handoff pattern)

**La session principale injecte le contexte, l'agent ne le re-cherche pas.** C'est l'orchestrateur qui lit les rapports précédents / implementation-notes et n'injecte QUE le pertinent — un sub-agent qui « se renseigne » dans les rapports des autres se disperse (le Frontend Agent qui lit un rapport DB tente de « réparer » le schéma). Anti-pattern symétrique : coller 10 rapports dans la relance — le re-brief est dense, pas exhaustif (le re-reading est l'ennemi du long-context).

### Déploiement 10 juin 2026

- neoteem-back-ts : rule `.claude/rules/agent-relaunch-context.md` + pointeurs `/feature` étapes 3 et 5.
- neo_ia : section « Relance après escalade » dans `.claude/rules/sub-agent-patterns.md` (enrichissement du foyer existant) + pointeurs `/feature`.

### Sources

- [Subagents in the SDK — platform.claude.com](https://platform.claude.com/docs/en/agent-sdk/subagents) — `resume` param, agent_id, stateless par défaut
- [Issue #11712](https://github.com/anthropics/claude-code/issues/11712) + [Issue #33651](https://github.com/anthropics/claude-code/issues/33651) — limites du resume
- [PubNub Best practices for Claude Code sub-agents](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/) — invocation failures = context density
- [Tembo — Claude Code Subagents 2026 Guide](https://www.tembo.io/blog/claude-code-subagents) — fresh instance par défaut, memory opt-in

---

## AJOUT 16 juin 2026 — AMENDE : le nesting est désormais POSSIBLE (v2.1.172), mais l'escalade reste le DÉFAUT

> **Statut de cette note : prémisse factuelle amendée, recommandation de design conservée.** Ce n'est PAS un abandon du pattern — c'est une correction de réalité + un nouveau levier d'enforcement. Source primaire vérifiée : [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) § « Spawn nested subagents » + changelog v2.1.172 / v2.1.178.

### Ce qui était FAUX (couche factuelle)

La note (et ses foyers : [[comment-creer-agent]] table de capacités, `subagent-creator` SKILL, [[limites-subagents-claude-code]], feedback memory) affirmait : **« un sub-agent ne peut PAS invoquer le tool Agent / pas de subagents imbriqués »**. **Périmé depuis CC v2.1.172 (10 juin 2026)**, verbatim changelog :
> « Sub-agents can now spawn their own sub-agents (up to 5 levels deep) »

Et doc subagents, verbatim :
> « As of Claude Code v2.1.172, a subagent can spawn its own subagents. »

### Ce qui SURVIT (couche design) — et pourquoi

Distinguer **possibilité technique** (levée) de **recommandation** (intacte). Sur les 4 raisons historiques de cette note :

| Raison | Statut après v2.1.172 |
|---|---|
| Boucle infinie | **Neutralisée** : foreground *« self-limiting: the main conversation waits on the entire chain »* ; background plafonné à 5 niveaux *« fixed and not configurable… to prevent runaway concurrent trees »* |
| Debugging impossible | **Neutralisée** : panel arborescent (`(+N)` descendants, path back to `main`) + transcripts isolés `agent-{id}.jsonl` |
| tool_use conflicts | Non documenté comme bloquant — la plateforme gère l'isolation |
| **Explosion de contexte** | **CONFIRMÉE** (verbatim : *« Running many subagents that each return detailed results can consume significant context »*) |

**Conclusion** : l'escalade-vers-session-principale reste le **défaut recommandé** (contexte propre, coût maîtrisé, orchestration lisible). Le nesting s'active **sélectivement**, pour un cas précis (ci-dessous), jamais par réflexe.

### Règles exactes du nesting (verbatim doc)

- **Profondeur** : comptée en niveaux sous le main. **Foreground = n'importe quelle profondeur** (auto-limité, chaque niveau bloque son parent). **Background = plafond 5** ; un background au niveau 5 *« does not receive the Agent tool and cannot spawn further »*.
- **Défaut tool — PIÈGE** : un sous-agent *« inherits all tools if omitted »* → s'il **omet la ligne `tools:`**, il hérite de `Agent` et **peut nester par défaut**. Pour l'EN EMPÊCHER : *« omit `Agent` from its tools list or add it to `disallowedTools` »* — donc ligne `tools:` explicite SANS `Agent`, ou `disallowedTools: Agent`.
- **`Agent(type)` allowlist** : ne s'applique qu'à un agent **main-thread** (`claude --agent`). Dans une définition de sous-agent, *« any type list inside the parentheses is ignored »* (seul l'effet « peut nester » subsiste). Pour bloquer des types en sous-agent → `permissions.deny: ["Agent(X)"]`.
- **Fork** : *« A fork cannot spawn further forks »* mais peut spawner un sous-agent nommé (qui compte dans la profondeur).

### Enforcement v2.1.178 (15 juin) — gouverner les spawns

- **`Tool(param:value)`** (wildcard `*`) : règle de permission matchant un paramètre d'input. Ex `Agent(model:opus)` *« to block Opus subagents »* — gouverne le modèle/coût de tout spawn. Couche DIFFÉRENTE de `Agent(type)` en `tools`.
- **Auto mode** : les spawns de sous-agents sont désormais *« evaluated by the classifier before launch »* — un sous-agent imbriqué ne peut pas s'auto-élever ses permissions (il hérite l'auto mode du parent).

### CE QU'ON PEUT FAIRE — patterns activables (pour améliorer skills/agents forge)

**Le cas d'usage que la doc endosse explicitement** (verbatim) :
> « Use this when a delegated task itself splits into parallel subtasks, such as **a reviewer subagent that dispatches a verifier per finding**, so the intermediate output never reaches your main conversation. Only the top-level subagent's summary returns to you. »

→ **Fan-out hiérarchique où l'intermédiaire est du bruit**. La valeur = isolation de contexte multi-niveaux (seul le résumé du top-level remonte).

**Candidats forge à évaluer (gate Raphael avant de muter un agent)** :
- `repo-inspector` (mode audit) : dispatche déjà des sous-agents par lentille/repo → pourrait, par lentille, dispatcher un verifier par finding sans polluer son propre contexte. Il a déjà `Agent` (volontaire).
- `devils-advocate` : un verifier adverse par objection (refuter chaque claim indépendamment) — pattern reviewer→verifier canonique.

**Arbitrage — quand préférer quoi** :
- **Nesting** : sous-travail parallélisable dont l'output intermédiaire ne doit jamais polluer le main. Endossé doc.
- **Escalade session principale** (CETTE note, défaut) : sous-travail touchant un autre scope/expertise/API publique — session orchestre, contexte propre.
- **Agent Teams** : *« sustained parallelism or exceed your context window »* / inter-communication entre sessions.
- **Forks** : side-task nécessitant trop de contexte pour un agent nommé, ou plusieurs approches en parallèle depuis le même point (cache partagé, moins cher ; ne peut pas re-forker).
- Le tool **Workflow** : NON couvert par la doc subagents — arbitrage nesting-vs-Workflow hors source primaire, à traiter séparément (ne pas inférer).

### Coûts (à citer prudemment)

- Doc subagents : **aucun chiffre par niveau** (seulement l'avertissement contexte ci-dessus).
- Chiffre PRIMAIRE Anthropic ([engineering/multi-agent-research-system](https://www.anthropic.com/engineering/multi-agent-research-system)) : agents ≈ **4× tokens** vs chat, multi-agent ≈ **15× tokens** vs chat — mais c'est du multi-agent/Agent Teams, **PAS** une métrique de profondeur de nesting.
- Chiffres « coût géométrique / 50×+ par profondeur » = **agrégateurs (aicosts.ai, ofox.ai), à confirmer** — jamais cités comme autorité (cf [[llm-deep-research-version-numbers-hallucinated]]).

### Foyers amendés en cohérence (16 juin 2026)

[[comment-creer-agent]] (source amont, table capacités) · [[limites-subagents-claude-code]] (+ méthode audit corrigée) · `subagent-creator` SKILL.md (L278) · feedback memory `anti_reentrance_sub_agents` · corps amont de CETTE note (sections QUOI + WORKFLOW + résumé) · gloses index [[MOC-Techniques]] et [[pattern-mcp-brief-then-direct]]. Anti-drift via [[methode-pivoter-doctrine]] — chercher TOUS les foyers avant d'éditer.

### Sources (primaire)

- [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) § Spawn nested subagents (lue en entier 16 juin)
- [code.claude.com/docs/en/changelog](https://code.claude.com/docs/en/changelog) — v2.1.172 (10 juin), v2.1.178 (15 juin)
- [anthropic.com/engineering/multi-agent-research-system](https://www.anthropic.com/engineering/multi-agent-research-system) — 4×/15× tokens
