---
titre: "Pattern MCP brief-then-direct — orchestration token-efficient sub-agents"
resume: "Session principale consulte MCP/CLI + valide advisor + brief enrichi au sub-agent. Sub-agent reçoit synthèse directe, exécute. Si doute non couvert → filet : sub-agent re-consulte directement le MCP. Pattern transposable forge-brain, obsidian-brain, postgres, langfuse, context7, tout CLI/MCP."
aliases:
  - "pattern mcp brief direct"
  - "brief enrichi filet mcp"
  - "mcp orchestration token efficient"
  - "session principale brief sub-agent vault"
  - "mcp re-consultation pattern"
  - "filet de sécurité mcp sub-agent"
  - "doctrine consultation mcp jarvis"
derniere-maj: 2026-05-24
auteur: claude
type: technique
sources:
  - "Session 24 mai 2026 — Raphael identifie le pattern (Jarvis-level)"
  - "[[anti-reentrance-sub-agents-pattern-escalade]] — pattern jumeau (escalade non-réentrance)"
  - "[[mcp-vs-skills-doctrine]] — distinction MCP/skills/CLI"
  - "Thariq Shihipar (Eng Lead Claude Code Anthropic) — '50-100 tools MCP → modèle se perd'"
  - "[[workflow-claude-code-optimal]] — pipeline /spec → architect → dev → /go"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/orchestration"
  - "#sujet/mcp"
  - "#doctrine/2026"
---

# Pattern MCP brief-then-direct — orchestration token-efficient sub-agents

## QUOI

Pattern d'orchestration où la **session principale** :
1. Consulte le MCP/CLI/vault pertinent (search, read)
2. Valide l'approche avec advisor si livrable majeur
3. Briefe le sub-agent dispatché **avec la synthèse pertinente déjà extraite** dans le prompt
4. Le sub-agent reçoit le contexte directement utilisable, exécute sans re-chercher
5. **Filet de sécurité** : si pendant l'exécution le sub-agent rencontre un doute non couvert par le brief, il peut re-consulter le MCP directement (a accès via `mcp__server__*` dans ses `tools:`)

**Transposable à tout MCP** : forge-brain (vault perso), obsidian-brain (vault métier neoteem-brain), postgres (schéma DB), langfuse (traces), context7 (docs libs), docs-langchain, etc. Pattern identique aux CLI maison (bash wrappers).

---

## POURQUOI — Le problème résolu

### Anti-pattern 1 : Sub-agent consulte vault systématiquement

```
Session principale → dispatch sub-agent
  ↓
Sub-agent : "OK je vais d'abord chercher dans le vault"
  ↓ search_brain (5 résultats × 200 tokens)
  ↓ read_note (note 1 × 2000 tokens)
  ↓ read_note (note 2 × 1500 tokens)
  ↓ ... 4000+ tokens consommés AVANT le travail réel
  ↓ commence enfin sa tâche
```

Coût : multiplié par N sub-agents dispatchés dans la session. Si 5 sub-agents dispatchés → 5 × 4000 = 20 000 tokens gaspillés en consultations redondantes (la session principale a probablement déjà fait les mêmes recherches).

### Anti-pattern 2 : Sub-agent ne consulte jamais

```
Session principale → dispatch sub-agent
  ↓
Sub-agent : exécute aveugle sur ses connaissances pré-entraînement
  ↓ Ne sait pas que [erreur X] a déjà été commise (vault Knowledge/erreurs/)
  ↓ Refait l'erreur
  ↓ 4h de debug, on capitalise après-coup (cf [[erreur-capitalisation-ex-post-23-24mai]])
```

Coût : régression silencieuse, friction utilisateur.

### Anti-pattern 3 : Session principale recopie tout le vault dans le prompt

```
Session principale → "Voici le vault entier sur ce sujet : [10 000 tokens]"
  → dispatch sub-agent avec tout le contexte
```

Coût : contexte du sub-agent pollué, attention dégradée, prone overthinking. Le sub-agent perd le signal dans le bruit.

### Solution Jarvis-pattern : brief enrichi + filet direct

```
1. Session principale consulte vault (5-10 requêtes ciblées, ~2000 tokens)
2. Session principale synthétise : "Voici les 3 points pertinents pour ta tâche"
3. Brief enrichi au sub-agent : tâche + synthèse (300-500 tokens)
4. Sub-agent exécute avec contexte ciblé
5. Si doute non couvert → sub-agent fait UNE requête MCP ciblée (filet)
```

Coût total : ~2500 tokens vs 20 000 anti-pattern 1. Qualité supérieure car contexte ciblé.

---

## COMMENT — Pattern d'implémentation

### Côté session principale

Workflow standard avant dispatch :

1. **Consulter MCP/CLI** pertinent au sujet
   - Vault : `mcp__forge-brain__search_brain` + `read_note` ciblés
   - DB : `mcp__postgres__describe_table` ou wrapper CLI
   - Docs lib : `mcp__context7__resolve-library-id` + `query-docs`
   - Traces : `mcp__langfuse__get_session` ou wrapper

2. **Advisor validation** sur livrable majeur (skill réutilisée, agent orchestrant, refonte)

3. **Synthèse dans le prompt sub-agent** :

```markdown
[Tâche à exécuter]

Voici les éléments pertinents extraits du [vault/DB/docs] :
- Point 1 : [synthèse 1-2 lignes]
- Point 2 : [synthèse 1-2 lignes]
- Note canonique de référence : [[note-name]] (déjà lue, voici la conclusion : ...)

[Si applicable] Validation advisor : approche X retenue.

Exécute. Si tu rencontres un doute non couvert par ce brief, tu peux re-consulter le MCP via mcp__server__* (filet, pas exploration parallèle).
```

### Côté sub-agent — body section standardisée

À ajouter dans le body de chaque sub-agent ayant accès à un MCP :

```markdown
## MCP — accès direct (filet de sécurité)

Tu reçois normalement un brief enrichi de la session principale avec les éléments MCP pertinents déjà extraits (vault, DB, docs, traces).

**Si pendant l'exécution tu rencontres un doute non couvert par ton brief** (terme inconnu, décision technique conflictuelle, pattern incertain, valeur DB précise non fournie), tu peux re-consulter directement :

- `mcp__forge-brain__search_brain` query ciblée (vault perso)
- `mcp__obsidian-brain__search_brain` (vault métier neoteem-brain)
- `mcp__postgres__*` (schéma DB)
- `mcp__context7__*` (docs libs)
- [autres MCP selon agent]

**Pas systématique** — la session principale t'a déjà briefé. C'est un filet de sécurité, pas une exploration parallèle. Anti-pattern : scanner par réflexe sans en avoir besoin (coût tokens élevé sur N agents).

**Quand l'utiliser** :
- ✅ Terme/acronyme non défini dans le brief
- ✅ Conflit entre 2 approches mentionnées
- ✅ Valeur précise nécessaire (ex : type exact colonne DB)
- ❌ Re-vérifier ce que le brief dit clairement
- ❌ "Au cas où" sans déclencheur précis
```

---

## QUAND — Critère d'application

### Le pattern s'applique quand :

- ✅ Sub-agent dispatché a accès à un MCP/CLI (`mcp__server__*` dans tools)
- ✅ La tâche nécessite du contexte que le sub-agent n'a pas (vault, DB schéma, docs lib, traces)
- ✅ Session principale a le temps/contexte pour consulter en amont
- ✅ Plusieurs sub-agents dispatchés dans la session sur des tâches connexes (gain × N)

### NE PAS appliquer quand :

- ❌ Sub-agent purement procédural (pas besoin de MCP — ex : test-writer écrit tests, code-reviewer review syntaxe)
- ❌ Tâche one-shot ultra-courte (overhead briefing pas justifié)
- ❌ Session principale n'a pas accès au MCP pertinent (laisser sub-agent chercher)

---

## TRANSPOSITION cross-MCP

| MCP | Session principale consulte AVANT brief | Sub-agent filet AVEC |
|-----|---------------------------------------|---------------------|
| **forge-brain** (vault perso) | `search_brain` + `read_note` canoniques + feedbacks pertinents | `mcp__forge-brain__*` si terme/note non couvert dans brief |
| **obsidian-brain** (vault neoteem-brain métier) | Search business rules, schemas BDD, fiches produits | `mcp__obsidian-brain__*` si règle métier précise non fournie |
| **postgres** (DB) | `describe_table`, `list_indexes` pour structure pertinente | `mcp__postgres__*` si valeur DB précise nécessaire |
| **context7** (docs libs) | `resolve-library-id` + `query-docs` pour API à jour | `mcp__context7__*` si signature précise non fournie |
| **docs-langchain** | `search_docs_by_lang_chain` sur API utilisée | `mcp__docs-langchain__*` si pattern précis nécessaire |
| **langfuse** (traces) | `get_session` traces pertinentes pour debug | `mcp__langfuse__*` si trace précise nécessaire |
| **CLI maison** (bash wrappers, scripts/) | Exécuter le wrapper pertinent, extraire output | Sub-agent invoque le CLI via Bash si applicable |

**Pattern identique** : session principale = orchestrateur token-efficient, sub-agent = exécutant avec filet.

---

## OPTIMISATION — 3 niveaux

### Niveau basique
- Section "MCP re-consultation" dans body des sub-agents ayant `mcp__server__*` dans tools
- Brief enrichi systématique côté session principale pour livrables M/L

### Niveau avancé
- Synthèses vault structurées dans prompt sub-agent (puces, wikilinks aux notes lues)
- Filet conditionnel précisé par cas (terme inconnu / conflit / valeur précise — pas "au cas où")
- Validation advisor avant brief pour livrables majeurs

### Niveau expert
- Hook `SubagentStop` qui mesure les re-consultations MCP par sub-agent → identifie briefs sous-spécifiés (pattern empirique : si sub-agent X re-consulte > 3 fois en moyenne, son brief est insuffisant)
- Cache de briefs réutilisables (ex : architect-deep neo_ia génère un "kit contexte NeoChat" réutilisable pour 5 dispatchs dev-neochat suivants)

---

## ANTI-PATTERNS

### Côté session principale
- ❌ **Dispatch sans consultation préalable** → sub-agent réinvente ou hallucine
- ❌ **Recopier vault entier dans prompt** → contexte sub-agent pollué
- ❌ **Brief vague "regarde le vault"** → le sub-agent doit deviner quoi chercher
- ❌ **Pas de brief si MCP accessible** → friction utilisateur (sub-agent re-fait recherche)

### Côté sub-agent
- ❌ **Scanner MCP par réflexe** au démarrage → coût tokens × N dispatchs
- ❌ **Re-vérifier ce que le brief dit clairement** → boucle inutile
- ❌ **Ignorer le brief et chercher tout seul** → invalide l'orchestration
- ❌ **Filet utilisé pour exploration parallèle** au lieu de doute ciblé

### Cross-agent
- ❌ **Sub-agent N+1 ne reçoit pas le contexte du sub-agent N** → session principale doit propager
- ❌ **Brief identique pour 5 dispatchs** → pas de personnalisation tâche-spécifique

---

## EXEMPLES CONCRETS

### Exemple 1 — Création d'agent forge (chantier 24 mai 2026)

**Session principale (moi)** :
1. `search_brain "comment-creer-agent"` → résolution canonique
2. `read_note "comment-creer-agent"` EN ENTIER
3. `search_brain "AskUserQuestion sub-agent"` → trouve issue #18721
4. Brief enrichi à `agent-creator` :

```
Crée agent X avec ces specs : [...]
Contexte vault extrait :
- [[comment-creer-agent]] section AskUserQuestion : sub-agent NE PEUT PAS appeler AskUserQuestion (issue #18721) → utiliser pattern ESCALADE
- [[comment-creer-agent]] section wildcard MCP : préférer mcp__server__* à liste explicite
- Doctrine 22 mai : pas de workflow hooks, advisory uniquement
Exécute. Filet : mcp__forge-brain__* si doute sur convention couleur ou modèle.
```

`agent-creator` exécute avec contexte ciblé, n'a pas eu à re-chercher.

### Exemple 2 — Ajout endpoint ia_back

**Session principale** :
1. `mcp__obsidian-brain__search_brain "endpoint pattern Neoteem"` → conventions
2. `mcp__postgres__describe_table users` → schéma précis
3. `mcp__context7__query-docs "hono zod-openapi"` → signature à jour
4. Brief enrichi à `api-designer` puis `dev` :

```
Ajouter endpoint POST /api/users/notifications
Schéma DB : users.notifications_enabled (bool, default false, nullable)
Convention Neoteem : path kebab-case, retour 200 sur succès avec { ok: true }
Hono pattern : OpenAPIHono + zod schema avec .openapi()
Filet : mcp__postgres__* si autres colonnes notification à consulter
```

Pas de re-recherche schéma DB par `dev` — déjà fourni.

### Exemple 3 — Audit vault (pattern anti)

**Anti-pattern observé chantier 23 mai** :
- 6 sub-agents dispatchés en parallèle pour auditer 6 thèmes vault
- Chaque sub-agent re-faisait `search_brain` sur les mêmes canoniques
- Coût × 6 = ~12 000 tokens en consultations redondantes

**Pattern correct** :
- Session principale fait UNE passe canoniques + extrait synthèse
- Brief enrichi à chaque sub-agent avec sa partie + synthèse commune
- Coût × 1 = ~2000 tokens partagés

---

## SOURCES

- **Session 24 mai 2026** — Raphael identifie le pattern : *"toi tu call pour proposer + advisor + tu donnes au sub-agent ce qu'il faut, s'il est pas sûr il peut recall le vault"*
- **[[anti-reentrance-sub-agents-pattern-escalade]]** — pattern jumeau (escalade non-réentrance)
- **[[mcp-vs-skills-doctrine]]** — distinction MCP/skills/CLI
- **[[workflow-claude-code-optimal]]** — pipeline /spec → architect → dev → /go (pattern complémentaire)
- **Thariq Shihipar** (Eng Lead Claude Code Anthropic) — *"50-100 tools MCP → modèle se perd"*, doctrine token-efficient
- **Boris Cherny** (Pragmatic Engineer) — *"thinnest wrapper"* (le harness fait le travail, pas le sub-agent)

---

## WIKILINKS

- [[comment-creer-agent]] — section MCP re-consultation à ajouter
- [[comment-creer-skill]] — section MCP re-consultation à ajouter
- [[mcp-vs-skills-doctrine]] — distinction enrichie avec ce pattern
- [[anti-reentrance-sub-agents-pattern-escalade]] — pattern jumeau (escalade)
- [[workflow-claude-code-optimal]] — pipeline complet
- [[Thariq Shihipar]] — doctrine token-efficient

---

**Fin note canonique `pattern-mcp-brief-then-direct.md`** — créée 24 mai 2026, chantier marathon tour 3.

## AJOUT 27 mai 2026 — Cause-racine empirique : MCP sub-agent NON connecté (`No such tool available`)

Ce pattern n'est pas qu'une optimisation tokens — c'est une **nécessité structurelle**. Vérifié empiriquement (Chantier A, 27 mai 2026) : le `mcp__server__*` listé dans le `tools:` d'un sub-agent est **décoratif**. Le serveur MCP n'est PAS connecté dans le contexte d'exécution du sub-agent : l'appel `mcp__forge-brain__read_note(...)` retourne `No such tool available`. Confirmé sur 2 agents (skill-creator, hook-creator).

Conséquence : un sub-agent à qui on ordonne « lire les canoniques via MCP » sans fournir le contenu fallback sur `cat`/`find` du vault → viole la doctrine MCP-only ([[forge-brain-proactive]]).

**Règle architecturale** : la session principale est le SEUL contexte avec accès MCP effectif. Tout brief sub-agent impliquant le vault contient les extraits inline + « JAMAIS cat/find/grep/Read le vault ; si manque, ESCALADE ». Ne JAMAIS écrire « lis via MCP » dans un brief sub-agent.

Enforcement structurel proposé (défense en profondeur) : hook `vault-cat-guard` (PreToolUse Bash, bloque cat/find/grep sur `vault/`). Cf [[comment-creer-hook]] catalogue transversal.

Lié : [[anti-reentrance-sub-agents-pattern-escalade]] (le sub-agent ne peut pas non plus invoquer Agent — même classe de limitation contextuelle).

## AJOUT 27 mai 2026 (suite) — Exception : quand le doublon révèle un agent mort-né (KILL > faire marcher)

Le pattern brief-inline rend le MCP en sous-agent inutile pour la **lecture** (on fournit les extraits). Mais il ne résout PAS le cas d'un agent dont le métier est l'**écriture MCP dense**. Diagnostic posé sur 2 cas spéciaux (session 27 mai, cas spéciaux Chantier A) :

### Critère discriminant : densité d'écriture MCP

| Métier de l'agent | Survit au contexte sous-agent ? | Verdict |
|---|---|---|
| **Analyse + 0-1 écriture** (devils-advocate : critique + 1 `create_note`) | OUI — mode dégradé viable (renvoyer le livrable en texte, la session principale persiste si utile) | Garder en agent, brief clarifié |
| **N× écriture MCP en boucle** (vault-maintainer : `update_property` × notes + MOC + backlinks) | NON — le métier EST impossible (MCP décoratif = `No such tool available` sur chaque write) | Candidat KILL |

### Règle : avant de "faire marcher", chercher le doublon

Un agent au métier MCP-write-dense ne se "fait pas marcher" en sous-agent (β orchestré = la session principale devrait rejouer toute la logique de correction à partir d'un rapport markdown — absurde). La bonne question est : **existe-t-il déjà une skill qui couvre ce métier en session principale (MCP effectif) ?**

- **Cas vault-maintainer (KILL, 27 mai)** : son métier (aliases, MOC, frontmatter, backlinks, dédoublonnage) était **déjà couvert** par `/vault-audit` — une skill qui tourne en session principale (MCP effectif) + script Python déterministe. Aucune invocation historique via le tool `Agent`. Verdict : **doublon mort-né → KILL**, pas architecture spéciale. Le seul apport unique (trigger proactif "after cc-news / note creation") a été porté dans la description de `/vault-audit`. L'exemption hook `vault-cat-guard` a été retirée (surface réduite, MCP-only plus strict).

### Principe de design qui en découle

> **Agents = analyse + écritures MCP rares** (survivent au mode dégradé sous-agent).
> **Skills = écritures MCP denses** (tournent en session principale, MCP effectif).

Un composant dont la valeur est `N× MCP-write` est structurellement une **skill**, pas un agent. Si on hésite à le créer en agent "parce qu'il doit écrire beaucoup dans le vault/la DB", c'est le signal qu'il doit être une skill.

Lié : [[anti-reentrance-sub-agents-pattern-escalade]] (même classe — limitation contextuelle du sous-agent), [[mcp-vs-skills-doctrine]] (distinction MCP/skills renforcée par ce critère).

## AJOUT 27 mai 2026 (suite 2) — Précision audit transverse : write MCP vault ≠ write filesystem

Audit transverse densité MCP write des 10 agents restants (post-KILL vault-maintainer, 27 mai) : **0 candidat KILL/PIVOT**. Flotte saine, vault-maintainer était le cas isolé.

Le critère de densité capté par l'audit a révélé une nuance à expliciter : **seule l'écriture MCP vault compte**, pas l'écriture filesystem.

| Écriture | Marche en sous-agent ? | Compte pour le critère "dense" ? |
|---|---|---|
| `mcp__forge-brain__create_note/append_note/update_property/...` (vault) | NON (`No such tool available`) | OUI — c'est le critère |
| `Write`/`Edit` filesystem (`.claude/`, code, skills) | OUI | NON — hors critère |

Les 4 créateurs (agent-creator, skill-creator, claudemd-optimizer, hook-creator) écrivent BEAUCOUP — mais sur le **filesystem** (`.claude/`), et leur `mcp__forge-brain__*` sert à la **lecture** des canoniques (`read_note`). Donc classés **rare**, pas dense. Confondre les deux aurait produit 4 faux candidats KILL.

**Règle de mesure** : grep le préfixe exact `mcp__forge-brain__(create_note|append_note|update_note|update_property|insert_section|bulk_update_property|move_note|delete_note)` dans le corps de l'agent — pas juste `Write|Edit`. Seul ce pattern, en boucle (× N notes), déclenche KILL/PIVOT.

Corollaire (prévention > audit récurrent) : le critère étant rare (1 cas sur 11 agents historiques), mieux vaut l'ancrer comme question-réflexe de création dans `agent-creator` (« métier = N× write MCP vault ? → skill, pas agent ») qu'en audit périodique. Conforme à « gardes en écriture > scanners périodiques ».
