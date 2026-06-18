# Conception — Discovery + /spec cross-repo + Loop d'implémentation

**Figé le 2026-06-18** (session longue, Document & Clear). Plan de référence pour reprendre propre après /clear.

---

## 0. L'objectif final (le « pourquoi »)

Passer du **niveau 2** (Raphael + Jérôme lancent `/feature` story par story, à la main) au **niveau 3** (un loop enchaîne l'exécution des user stories qu'ils ont choisies). Fondement : pre-compute > inference ([[pre-compute-vs-inference-loops-boris]]). Le loop **amplifie l'entrée** : un bon ticket → exécution géniale ; un ticket flou → déchet en série. **Donc on fiabilise l'entrée AVANT d'automatiser.**

Roadmap en phases (on fait petit à petit) :
- **Phase 1 — Qualité d'entrée/sortie** (prérequis du loop)
  - ✅ Template de PR dual-audience + hook `pr-template-guard` (back-ts + neo_ia) — **LIVRÉ 18 juin**
  - ⬜ `/spec` repensé : discovery cross-repo → bon template par repo → tests explicites
  - ⬜ Fiabiliser `/feature` (bug du ticket sans parent, etc.)
- **Phase 2 — Orchestration** : le loop (itère sur les US d'une story) + état/reprise (pattern Ralph)
- **Phase 3 — neo_ia** : plus tard, quand on aura les datasets d'éval comme oracle (la sortie d'un agent IA n'est pas vérifiable mécaniquement comme un endpoint)

---

## 1. Architecture réelle des produits (validée avec Raphael)

```
NeoIA (Python/LangGraph, agents IA)
  └─ TOOLS qui appellent → endpoints de neoteem-back-ts

neoteem-back-ts (TS/Hono/Drizzle, en construction)
  └─ expose endpoints qui tapent dans la base
  └─ soit RÉUTILISE des fonctions SQL existantes de bdd (trop lourdes à réécrire)
  └─ soit les RÉÉCRIT en Drizzle (gain perf)

bdd (repo Postgres) — fonctions SQL existantes : on LIT/réutilise, JAMAIS on n'exécute le SQL
ia_back — EN TRAIN DE MOURIR (story N2-111278 le décommissionne) → à oublier
```

Couplage entre repos = **le contrat d'API** (l'endpoint back-ts que le tool neo_ia consomme), pas le système de fichiers. → **PAS de monorepo, PAS de dossier `IA/` parent** (créerait une 3e couche de config en collision avec les `.claude/` mûrs, les chemins absolus, `repo-scope-guard`).

Règle cross-repo : une story qui touche 2 repos se **découpe en US mono-repo liées** (US endpoint back-ts → puis US tool neo_ia). Chaque loop reste mono-repo. Le champ `🗂️ Repo cible` existe déjà dans les templates.

Suggestion d'index/optim SQL révélée par le dev → décrite dans `doc/db-suggestions/N2-xxxxx.md` + mentionnée dans la PR, **jamais exécutée**.

---

## 2. Le `/spec` repensé — discovery AVANT étiquetage

Principe clé (validé empiriquement + web « repo as knowledge graph ») : **chercher d'abord, étiqueter ensuite.** L'étiquette « ça touche tel repo » est le RÉSULTAT des recherches, jamais une hypothèse de départ.

Déroulé cible :
```
1. Raphael décrit la feature (langage naturel).
2. DISCOVERY (dans l'ordre) :
   a. neoteem-brain (via skill neo-brain-dev-ia, NOMMÉE par Raphael) = LA CARTE
      → "cette capacité existe déjà ? dans quel repo ?" (évite de réinventer ; cas mails)
      ⚠️ Le brain est PARTIELLEMENT PÉRIMÉ (pointe encore vers ia_back mourant)
      → mapper système-mourant → remplaçant (ia_back → neoia-api/back-ts), idéalement
         dérivé d'un signal vivant (présence neoia-api) ou daté, pas codé en dur.
   b. vérifier dans le CODE RÉEL des repos pointés (back-ts / neo_ia / bdd)
      → c'est l'étape qui RATTRAPE le brain périmé. Capacité CLI-depuis-forge requise.
   c. conclure : quels repos touchés + étiquettes.
3. PRÉSENTER le verdict à Raphael (jamais décider seul) → il confirme/corrige.
4. Pour CHAQUE US : template du bon repo + tests explicites (voir §3).
5. Validation → création tickets Jira (story d'abord, GO, puis sous-tâches).
```

Empiriquement validé (18 juin) : le brain SAIT répondre — il a sorti les routes acteurs `/api/v1/acteurs/{id}/contexte` + le mapping endpoint↔tool LangChain (`search_acteurs` → `recherche_acteur`). C'est la carte endpoint↔tool dont la discovery a besoin.

---

## 3. Tests explicites par type de US (point Raphael)

Le ticket doit dire QUELS tests, pas juste « écris des tests ».
- **US back-ts** (endpoint, déterministe) → unitaires (use-case) + parité/intégration (compareRows vs base).
- **US neo_ia** (agent/tool, NON déterministe) → unitaire (fonction du tool) + intégration (le tool appelle vraiment l'endpoint) + fonctionnel/e2e (l'agent utilise le tool en conversation réelle) + **éval** (dataset figé si comportement LLM change).

---

## 4. Architecture composant — VÉRIFIÉE (état Claude Code juin 2026)

Décision « plein d'agents vs un agent avec skills » tranchée par recherche web + doctrine :

> **Connaissance = SKILLS · Workers lourds isolés = SOUS-AGENTS · Coordination = SESSION PRINCIPALE.**
> Pattern mûr 2026 : « many top skills are thin orchestration layers over subagents ».

- **Skills de connaissance** : comment écrire une story back-ts, une story neo_ia, les étiquettes/templates. (= ce que Raphael décrivait : « skill back-ts, skill neo_ia, skill étiquette ». Instinct juste.) Injectées dans un agent via `skills:` frontmatter (contenu chargé au démarrage).
- **Sous-agents d'exploration** : lire en profondeur un repo (neo_ia, bdd) = travail bruyant à ISOLER. 1 agent par repo, en parallèle (sweet spot 3-5).
- **Session principale orchestre** : interroge le brain (MCP dispo en session principale), décide, présente. PAS un agent-chef.

Pourquoi pas un agent orchestrateur, malgré que ce soit DÉSORMAIS techniquement possible (v2.1.172) :
- **Raison COÛT (vérifiée, pas dogme)** : multi-agents = +200-500% tokens ; incidents réels 8-47k$. Nesting fait pour « gérer le contexte » (pousser le bruit loin), PAS pour orchestrer. Profondeur utile = 2-3, jamais 5. Sur abonnement (pas API), chaque agent // consomme le quota Nx plus vite.
- Cible à terme pour le LOOP (traiter PLUSIEURS stories) = l'outil **Workflow** (orchestration hors-contexte), pas un arbre d'agents imbriqués.

---

## 5. Déploiement

- **v1 = skill/flow CLI lancé depuis claude-forge** (seul endroit avec vue + droits cross-repo lecture).
- **Cowork/Desktop = ABANDONNÉ pour v1** : la discovery exige de lire le code réel des 3 repos (étape 2b) ; Cowork ne peut pas (pas de stdio MCP, accès fichier différent) → discovery réduite au brain seul = réponse périmée avec fausse confiance. Pire qu'inutile. (Idée « au pire Cowork » de Raphael = musing, pas exigence.)

---

## 6. Dette à nettoyer (découverte par le DA, 18 juin)

⚠️ Il n'y a PAS « 3 copies synchronisées d'un /spec ». Réalité vérifiée :
- **Lignée Jira** (le vrai `/spec`) en 3 copies : `neoteem-back-ts/.claude/skills/spec/` + `neo_ia/.claude/skills/spec/` + forge skill `neoteem-back-ts`. **DÉJÀ désynchronisées** : back-ts a 2 references, neo_ia en a 8 dont 3 ORPHELINES (`decompose-waves`, `output-templates`, `cross-validation` non câblées).
- **Skill `spec` SÉPARÉE chez forge** (lignée TODO/vagues, sortie différente) → **collision de nom** avec la lignée Jira.

Le DA cite l'historique forge : la fusion `/spec`+`/decompose-ticket` a été faite parce que « la duplication cross-repo générait du drift ». Ajouter une 4e pièce sans régler les 3 copies répéterait l'erreur ([[feedback_single_source_of_truth]]).

→ **Décision Raphael** : « je m'en fous qu'on refasse tout ». Donc option ouverte = repenser proprement, supprimer/améliorer l'existant, source unique. À cadrer au reprise.

---

## 7. Décisions FIGÉES vs À TRANCHER au reprise

**Figé :**
- Discovery = chercher d'abord (brain carte → code réel vérif → conclure). Jamais étiqueter par hypothèse.
- Jamais décider seul / inventer → toujours proposer, demander (Raphael insistant).
- Connaissance = skills, exploration lourde = agents, coordination = session.
- v1 CLI depuis forge ; pas Cowork v1 ; pas de monorepo/dossier IA parent.
- Tests explicites par type de US.

**À trancher au reprise :**
- Forme exacte du `/spec` repensé (une skill forge qui charge des sous-skills + délègue à des agents d'explo ? découpage précis).
- « route vers le bon /spec » = consultatif (la discovery DIT quoi lancer, l'humain lance) vs autre — l'ambiguïté DA reste ouverte.
- Ordre : nettoyer la dette des 3 copies AVANT, ou en faire l'occasion d'unifier.
- Quand bascule-t-on vers l'outil Workflow (pour le loop multi-stories).

---

## MAJ 18 juin 2026 (après-midi) — Le BRIEF voyage avec le ticket (pièce jointe Jira)

Décision Raphael : le BRIEF technique complet d'une story / US ne vit plus seulement en lien Bitbucket — il devient une **pièce jointe du ticket Jira**, pour que le détail (dont les tests) voyage physiquement avec le ticket. Le ticket Jira reste le résumé scannable (dual-audience) ; la PJ porte le BRIEF auto-suffisant complet. Le `.md` reste AUSSI versionné dans le repo (vie git normale) ; la PJ est un instantané attaché à la création.

### Découpage MCP tranché (vérifié web 18 juin)

Le **MCP Atlassian officiel** (Rovo) liste les PJ (nom, taille, type, URL) via `getJiraIssue` mais **n'expose AUCUN download du contenu** d'une PJ — limitation connue ouverte (JRACLOUD-97830, atlassian-mcp-server#15). Donc le MCP NEOTEEM maison n'est PAS un doublon, il comble ce trou.

Règle d'outillage Jira (à appliquer partout) : **MCP Atlassian officiel d'abord ; MCP NEOTEEM pour ce que l'officiel ne couvre pas.**

| Action | Outil | MCP |
|---|---|---|
| Détecter les PJ d'un ticket (nom, URL) | `getJiraIssue` (champ `attachment`) | Atlassian officiel |
| **Lire le contenu** d'une PJ | `get_attachment_content(attachment_id)` | NEOTEEM (existe déjà) |
| **Créer/attacher** une PJ | `add_attachment` | NEOTEEM — **À AJOUTER (Jérôme)** |

### Côté LECTURE — LIVRÉ (18 juin), non committé

Étape 1 (Brief) des deux `/feature` (neoteem-back-ts + neo_ia) modifiée : `getJiraIssue` inclut `attachment` ; si PJ présente(s) → les lire TOUTES dès le début, AVANT l'architect, via `get_attachment_content` du MCP NEOTEEM. **Toute** PJ (pas que `.md`). **La PJ prime sur la description** (source technique complète et à jour). Règle officiel→NEOTEEM écrite dans la skill. Prise en compte à la prochaine session CLI (skills snapshotées au démarrage).

### Côté ÉCRITURE + INFRA — en attente Jérôme

Prompt remis à Jérôme : (1) ajouter `add_attachment(issue_key, filename, content)` au MCP NEOTEEM — réutilise la logique d'upload déjà dans `copy_attachments`, UTF-8 sans BOM, appelable plusieurs fois (un BRIEF story + un par US), n'écrase pas ; (2) **exposer le MCP NEOTEEM en HTTP** (comme `neobrain` via `https://mcp-brain.neoteem.fr/mcp`) pour le brancher en CLI — car aujourd'hui il N'EST PAS dans les `.mcp.json` des repos (neo_ia n'a aucun MCP Jira CLI ; back-ts n'a que l'Atlassian officiel). Une fois l'URL fournie → l'ajouter aux `.mcp.json` de neo_ia + back-ts.

⚠️ **Tant que le MCP NEOTEEM n'est pas branché en CLI, la lecture de PJ par `/feature` est inopérante** — la modif des skills est correcte mais dort jusqu'au branchement.

### Diagnostic « tests pas assez mentionnés » — CAUSE RÉELLE PROUVÉE (lecture des tickets + `.md` source)

Hypothèse initiale « le /spec appauvrit les tickets en les poussant dans Jira » = **FAUSSE** (vérifié). Réalité (S1-migration-ia-back.md ligne 3 + 29) : les **BRIEFs `.md` par US n'existent pas encore** au moment de la création du ticket — ils sont rédigés « avant chaque /feature ». Donc le ticket Jira mince reflète une source qui, à ce stade, EST mince. Deux vrais problèmes distincts :
1. **Moment de rédaction (Cas B)** : le test détaillé d'une US est écrit trop tard (juste avant /feature), donc invisible à la relecture et fragile pour un loop autonome. Pour un loop, le test doit être figé AVANT, pas pendant.
2. **Type de test non forcé** : la ligne `**test** :` des templates est générique — elle ne force pas à distinguer unitaire / intégration / fonctionnel-e2e / éval selon la nature de l'US (vrai sur les 2 templates). Levier solide pour le nouveau /spec. Nuance vérifiée : une US de **migration à parité** hérite légitimement du test défini au niveau story (US5 maigre ≠ défaut) ; le vrai manque est sur les US tool/feature LLM (ex. US11 : aucun test propre).

→ Ces 2 points deviennent des exigences de conception du `/spec` de ia-workbench : produire des US où le « quoi tester + de quel type » est complet et figé dès la création.

### Reste à concevoir (cœur, non entamé)

Le `/spec` de ia-workbench lui-même : discovery cross-repo (brain carte ⨯ code réel) + découpage en US liées + tests par type d'US figés dès création. Les `/spec` mono-repo de neo_ia/back-ts restent FINIS et en place (on les fiabilise une fois, on les utilisera moins — pas une dette à tuer). DA et advisor consultés ; oracle/séquence A→B→C ABANDONNÉS (prémisse « on part de rien » fausse — il y a déjà des stories réelles à améliorer).

## Sources vérifiées (18 juin 2026)
- MCP Atlassian officiel sans download attachment : support.atlassian.com/atlassian-rovo-mcp-server (supported-tools), JRACLOUD-97830, github atlassian-mcp-server#15
- Nesting v2.1.172 + coûts : ofox.ai/claude-code-nested-subagents-2026, claudefa.st, cloudzero
- Agents vs skills : code.claude.com/docs/en/skills, developersdigest, theaiarchitects
- Subagent MCP access : github issues #13898 #34935, code.claude.com/docs/en/agent-sdk/subagents
- Repo-as-knowledge-graph / spec discovery : harness.io, augmentcode (Graphify), Notion spec-to-implementation
- Ticket/PR parfaits : INVEST, EARS, Gherkin ; dual-audience PR (github.blog agent PRs)
- DA critique : à persister dans Knowledge/critiques/critique-2026-06-18-fork-discovery-spec.md
