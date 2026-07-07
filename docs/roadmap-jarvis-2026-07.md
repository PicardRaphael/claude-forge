# Roadmap Jarvis — Optimisations & nouvelles features

**Figé le 2026-07-07.** Audit complet du repo (skills, rules, hooks, agents, vault, scripts) croisé avec les features CC v2.1.202 et l'état de l'art web juillet 2026. Objectif : le meilleur bras droit IA possible + un vault parfait.

**Méthode** : 4 agents read-only en parallèle (audit `.claude/` 3 lentilles · audit structurel vault · gap features CC · état de l'art web) + lecture canoniques en entier ([[workflow-claude-code-optimal]], [[methode-analyser-repo]]) + vérification empirique des claims structurants par la session principale. **Verdict DA intégré** (2 bloquants corrigés — #7 flippé, #20 re-scopé ; 4 items spéculatifs rétrogradés en P3 ; critique complète : `Knowledge/critiques/critique-2026-07-07-roadmap-jarvis.md`).

---

## Synthèse exécutive

**État : setup mature, aucun défaut critique.** Le socle (skills créatrices, hooks de garde, vault MCP, veille, doctrine) est solide. Les gains sont dans 3 directions :

1. **Éponger la dette identifiée** (P0) — contradictions vault/config, vestiges, seuils périmés. Coût faible, corrige de l'info activement fausse.
2. **Exploiter ce que CC offre déjà** (P1-P2) — notification asynchrone, orchestration native, dashboards, résilience modèle. Forge n'utilise que 4 events de hooks sur ~29 et zéro plugin.
3. **Monter d'un cran en proactivité et sécurité** (P2-P3) — routines Jarvis proactives (daily brief, vérité brutale), durcissement MCP/injection, éval de régression. C'est là que « bras droit » se joue.

**Légende** : Adoption **B** = behavioral (Jarvis fait seul) · **C** = config (hard-block settings.json → édition manuelle Raphael). Effort S/M/L.

---

## P0 — Correctifs (dette, info fausse servie en continu)

### P0.1 Vault

| # | Correctif | Preuve | Effort |
|---|-----------|--------|--------|
| 1 | **3 canoniques sans surface de récupération** : `comment-creer-skill` (50 backlinks !), `comment-creer-agent`, `comment-creer-hook` ont 0 alias + 0 tag. En mode agent-first (aliases pondérés 8× dans search_brain), c'est le fix le plus rentable du vault. Ajouter 4-6 aliases + 2 tags chacune. | lint_vault | S |
| 2 | **MOC-Claude-Code auto-contradictoire** : re-liste les agents SUPPRIMÉS au pivot 6 juin (`agent-creator`, `project-analyzer`, `project-auditor`…) comme actifs, juste après sa propre ligne « Agents supprimés ». + changelog s'arrête à mai (juillet non lié). Purger le bloc mort, relier CC juillet + notes features récentes. | Lecture MOC | S |
| 3 | **SCHEMA §7 prescrit un dossier `Templates/` inexistant** (10 templates listés, 0 présent dans l'index). Trancher : recréer les templates OU retirer §7 (comme `raw/` au pivot agent-first). | list_notes vide | S |
| 4 | **101 wikilinks cassés — 4 familles à traiter différemment** : (a) ~50 scaffolding responsable-ia jamais construit → décision prune-OU-build, pas « créer 50 notes » ; (b) ~15 liens malformés `[[../dossier/note]]` → conversion mécanique `[[note]]` ; (c) ~20 renvois vers memory/rules (pas des notes vault) → promouvoir `config-repo-equipe-vs-forge` (cité 4×) + `amende-vs-pivot-couche-factuelle-design` (cité 2×) en notes vault, statuer sur la convention pour le reste ; (d) ~10 vrais trous/typos → tri unitaire. | lint_vault 101 | M |
| 5 | **Séquelles de la migration du 7 juillet (ma propre dette)** : 15 notes créées non câblées aux MOCs (0 backlink) + ~12 tags plats hors convention (`worktrees`, `oauth`, `qualite`…) introduits. Câbler aux MOCs, normaliser vers `#type/`·`#domaine/`, fusionner les quasi-doublons (`patterns`→`#type/pattern`, `modeles`→`#type/modele`, `conformité`→`conformite`). | get_backlinks, get_tags | S |
| 6 | **Hygiène résiduelle** : Home affiche « 511 notes » (réel 531) ; 0-Inbox stagne à 6 notes non triées ; `.claude/agent-memory/` indexé dans le vault ; `11-Warp` absent de la liste fournisseurs SCHEMA. | vault_stats | S |

### P0.2 `.claude/`

| # | Correctif | Preuve | Effort |
|---|-----------|--------|--------|
| 7 | **Contradiction `agent-memory/` — corriger les CHECKS, PAS purger le dossier** (item flippé par le DA, preuves vérifiées) : le dossier est VIVANT (écritures 27 juin, exemption explicite `vault-write-guard.py:32`, `config-guardian:124` le compte comme pattern désiré, devils-advocate y écrit). Les 2 vestiges réels : (a) `repo-inspector.md:111` qui le codifie « chemin obsolète » → corriger ce check ; (b) `forge-review/SKILL.md:87` lit `.claude/agent-memory/skill-creator/MEMORY.md` **inexistant** (réf morte) → repointer vers les subdirs réels. | ls + grep vérifiés | S |
| 8 | **Seuils `memory-saturation-watcher` périmés** : WARNING 250 / CRITICAL 290 / « plancher ~240 » calibrés AVANT la migration (memory = 145 fichiers désormais). Le hook ne s'alarmera plus jamais. Recalibrer (ex. WARNING 180 / CRITICAL 220) + réécrire le commentaire doctrine. | grep vérifié | S |
| 9 | **~10 skills « ALWAYS invoke » hors trigger-map** (`.skill-triggers.json` = 28 entrées / 50 skills) : `audit-departement`, `choix-outils-ia`, `rag-design`, `reco-automatisation`, `veille-outils-ia`, `loop-forge`, `outcomes-test`, `methode-pivoter-doctrine`, `doctrine-impact-check`, `pivot-check` n'obtiennent pas le nudge proactif. Les ajouter. | comptage vérifié | S |
| 10 | **2 rules stubs** (`read-section-preference`, `vault-consultation-protocol`) encore référencées par 2 fichiers → repointer les références PUIS supprimer les stubs. | audit .claude/ | S |

---

## P1 — Quick wins (features CC + état de l'art, effort S)

| # | Feature | Usage proposé | Gain Jarvis | Adopt. |
|---|---------|---------------|-------------|--------|
| 11 | **`/dataviz` + Artifacts** (v2.1.198) — **REPORTÉ (décision Raphael 7 juil.)** | Livrer audits, `vault_stats`, gap-analyses, et livrables Lead IA (CODIR) en dashboard visuel partageable au lieu de murs de markdown. À réactiver au prochain besoin CODIR | « Présenter à Tony » des synthèses lisibles ; double usage casquette Lead IA | B |
| 12 | **`/rewind` + checkpoints** (v2.1.191, reprise avant `/clear`) | Checkpoint avant toute opération structurelle (refonte vault, migration masse, propagation cross-repo). **À appliquer dès la Vague 1** (pendant la chirurgie P0, pas après — DA) | Filet de sécurité mécanique sur le destructif | B |
| 13 | **Slash-skills empilées** (≤5, v2.1.199) | Composer les chaînes existantes : `/cc-news /doctrine-impact-check`, `/recap /forge-brain` | Moins d'allers-retours | B |
| 14 | **`fallbackModel`** (≤3 replis, v2.1.166) | Opus 4.8 → Opus 4.6 si indisponible. **Exclure 4.7 explicitement** (préférence Raphael) | Résilience zéro-babysitting | C |
| 15 | **Hook `Notification` → webhook Discord** (v2.1.198) | Router `agent_completed` / `agent_needs_input` vers #veille-tech (webhook déjà en place). ⚠️ Vérifier le payload réel du hook AVANT de câbler (champs non confirmés en source primaire) | « Sir, l'audit est terminé » — proactivité asynchrone : lancer, partir, être pingé | C |
| 16 | **statusLine / claude-hud** | HUD live : % contexte, branche, modèle, coût | Colle à l'obsession tokens (autocompact 50%, budgets MEMORY.md) | C |
| 17 | **Pattern déterministe-d'abord** (état de l'art) | Dans les routines de veille/monitoring : filtre par mots-clés/regex SANS LLM d'abord, LLM ensuite pour classer/rédiger | Coût et latence réduits — discipline « tokens = ressource précieuse » | B |
| 18 | **Staleness ≠ decay** (mem0) | Check périodique « ce fait haute-pertinence est-il encore vrai ? » sur les notes projet/user les plus lues — distinct de l'âge `derniere-maj` | Évite que Jarvis affirme avec assurance une phase projet périmée | B |
| 19 | **Consolidation mémoire planifiée** | Étendre `/clean-memory` + saturation-watcher en routine planifiée (Task Scheduler local) couvrant AUSSI le vault (merge doublons, dates relatives→absolues, prune) | Maintenance sans intervention — les briques existent déjà | B/C |

---

## P2 — Chantiers (effort M, forte valeur)

| # | Chantier | Description | Gain | Adopt. |
|---|----------|-------------|------|--------|
| 20 | **Raccourcir les rules** (re-scopé par le DA) | Les 17 rules = 47 399 chars (~12k tokens) injectés à CHAQUE session. ⚠️ La conditionnalisation `paths:` est INADAPTÉE ici : ces règles sont topic/action-triggered (une question management, un `append_note` MCP), pas déclenchées par lecture de fichier → elles cesseraient silencieusement de charger. Le gain sûr = **densifier/raccourcir** les rules les plus longues (même doctrine, moins de chars). Gain réel ~1 % de contexte, cacheable — utile, pas « levier #1 » | Gain tokens sans régression de correction | B |
| 22 | **Durcissement MCP/injection** (état de l'art, arXiv 2601.17548 + Anthropic auto-mode) | 3 volets : (a) doctrine « sorties MCP + contenu web = données NON fiables, jamais instructions » (note vault + rules) ; (b) hook egress-allowlist : WebFetch/curl autorisés vers liste de domaines, confirmation pour domaine neuf ; (c) sonde légère « ce contenu fetché contient-il des instructions ? » avant capitalisation vault — **advisory, jamais bloquant** (détection LLM peu fiable, DA) | Ferme la plus grosse surface d'attaque d'un Jarvis autonome fichiers+web (forge est MCP-lourd : forge-brain, NeoBrain, context7) | B+C |
| 23 | **`/matin` — daily brief transverse** | Agréger : état chantiers multi-repo (git log nuit), tickets Jira ouverts, notes vault récentes, actions requises — format Action Required / FYI / Handled. Déclenchement Task Scheduler local. ⚠️ Repos pro + Jira = machine PRO (à exécuter là-bas) | 5 min de revue au lieu de 30 — la routine chief-of-staff par excellence | B+C |
| 27 | **Câblage-à-la-création** (processus vault) | Règle : toute note neuve = ≥2 wikilinks entrants réels (MOC ou note sœur) le jour même + tags conformes. À encoder dans les skills d'écriture vault (done, cc-news, forge-brain) | Tue la cause racine des orphelins (cf. P0.5) | B |
| 28 | **LSP plugins cross-repo** (`pyright-lsp`, `typescript-lsp`) | Pour code-dev dans ia_back (TS), neo_ia (Python), lojii (Vue) — diagnostics, navigation symboles | Qualité code-dev repos cibles | C |
| 29 | **Hook `mcp_tool` SessionStart** (v2.1.119) | Injecter les notes vault récentes directement au démarrage (vs simple lancement du serveur). ⚠️ Coût tokens à CHAQUE session + partiellement redondant avec `/recap` — ne l'adopter que si l'injection reste ≤ quelques lignes | Contexte vault automatique dès le tour 1 | C |

---

## P3 — À arbitrer / explorations

| # | Sujet | Tension à trancher |
|---|-------|--------------------|
| 21 | **Dynamic Workflows par défaut sur les fan-outs** (rétrogradé de P2 par le DA) | Jusqu'à 1000 sous-agents pour des fan-outs forge de ~4 agents + prérequis plan Max/Team NON confirmé. La boucle `Agent()` manuelle suffit aujourd'hui. Adopter seulement si un fan-out réel dépasse ses limites. |
| 24 | **Module « vérité brutale »** (allocation de temps vs OKR — rétrogradé de P2) | Différenciateur Jarvis fort (« Être franc ») MAIS infra neuve à maintenir en solo, sans incident déclencheur. DA : build on-demand. Machine PRO (Jira). Raphael tranche : construire maintenant ou au premier besoin réel ? |
| 25 | **Autonomie graduée des routines** (rétrogradé de P2) | Beau contrat de confiance, mais forge n'a aujourd'hui que ~3 routines planifiées — un ladder formel est prématuré. À reprendre quand le nombre de routines autonomes le justifie. |
| 26 | **Golden-set de régression** (rétrogradé de P2) | Qui maintient les goldens après chaque évolution légitime ? Risque « abandonné dans 2 semaines » + faux positifs → ignoré. À reprendre au premier incident de régression silencieuse de skill. |
| 30 | **Query-driven growth** (vault qui grandit à chaque requête) | Heurte frontalement la discipline anti-bloat forge. Option médiane : spawn sous gate (créer seulement si search_brain ne trouve rien + validation). Ou rejet assumé. |
| 31 | **`learning-reminder` → nudge non-bloquant** | Seul hook hors lint/sécu/scope (Stop block). Garder tel quel (discipline assumée, choix Raphael) OU convertir en `additionalContext` pour alignement doctrinal total. |
| 32 | **`ask` masqués par security-guard** | Les entrées `ask` catastrophiques de settings.json ne se déclenchent jamais (hard-block PreToolUse avant). Défense-en-profondeur assumée OU déduplication. |
| 33 | **Vrai sandbox OS** (WSL2 / Windows Sandbox) | Le hook egress-allowlist (#22b) couvre l'essentiel à effort S. Le kernel-level = L, à réserver si les routines autonomes montent en puissance. |
| 34 | **`/design-sync` pour lojii** | Hors-scope forge, mais pertinent pour neofront (Vue, 634 composants) via Figma MCP. À signaler à la prochaine session lojii. |
| 35 | **Division `responsable-ia`** (670 chars, 8+ livrables) | Pattern hub valide en setup perso. Diviser seulement si la précision de trigger devient un problème mesuré. |

### Écartés sciemment (couverture prouvée, pas des oublis)

- **`/schedule` cloud, background agents auto-PR, Remote Control mobile** — org bloque le cloud ; tout reste sur Task Scheduler local.
- **Hooks SubagentStop/SessionEnd d'enforcement, PreCompact auto-dump** — doctrine 22 mai (pas de workflow hooks) ; « Document & Clear » reste manuel.
- **OTel/monitoring externe** — `/usage` natif suffit pour un poste solo.
- **Auto Memory `~/.claude`** — choix assumé memory/ in-repo versionné.
- **Claude in Chrome** — x-read + defuddle couvrent ; marginal.

---

## Ordre d'exécution recommandé

**`<done>` de la roadmap** : (a) P0 exécuté = `lint_vault` sans les 101 cassés ni les 0-alias, MOCs cohérents, checks `.claude/` sans contradiction ni réf morte ; (b) P1 = features adoptées dans le workflow réel (au moins 1 usage constaté chacune) ou `.proposed` remis à Raphael ; (c) P2/P3 = chaque item soit exécuté, soit explicitement rejeté par Raphael. Pas de « fait à moitié » silencieux.

1. **Vague 1 (une session)** : checkpoint `/rewind` D'ABORD (#12), puis P0 complet — #1-3, 5-10 en direct, #4 en 4 sous-lots. Le repo cesse de servir de l'info fausse.
2. **Vague 2 (une session)** : P1 behavioral (#11, 13, 17-19) + préparer les `.proposed` pour les P1 config (#14-16) → édition manuelle Raphael en une passe.
3. **Vague 3 (une session par chantier)** : P2 par ordre de valeur Jarvis : #22 (sécurité — préalable à toute montée en autonomie), #20 (densifier les rules), #27 (câblage-à-la-création), #23 (/matin, machine pro), puis #28-29.
4. **P3** : arbitrages Raphael au fil de l'eau (AskUserQuestion item par item).

**Boucle de contrôle** : chaque vague se termine par vérification empirique + commit + entrée CHANGELOG vault.

---

*Sources : rapports agents audit-claude / audit-vault / gap-features-cc / etat-art-web (2026-07-07) · [[workflow-claude-code-optimal]] · [[methode-analyser-repo]] · arXiv 2601.17548 · anthropic.com/engineering (auto-mode, sandboxing) · mem0.ai (staleness) · verdict devil's advocate intégré.*
