---
aliases:
  - vault jamais consulté session principale
  - session skip vault avant brief
  - délégation lecture vault sub-agent
  - brief sub-agent sans contexte vault
  - vault pas call en premier
  - erreur consultation vault session
auteur: claude
cree: 2026-05-27
derniere-maj: 2026-06-01
repo: claude-forge
resume: La session principale a modifié des templates BRIEF /spec sans consulter le vault d'abord, et a délégué la lecture canonique au sub-agent sans vérifier — travail non sourcé.
tags:
  - "#type/erreur"
  - "#erreur/comportement"
  - "#erreur/vault"
  - "#domaine/claude-code"
titre: Vault jamais consulté par la session principale avant brief sub-agent
type: erreur
---
# Vault jamais consulté par la session principale avant brief sub-agent

## Ce qui s'est passé

Le 2026-05-27, lors du travail sur le workflow Spec-Driven Development de Neoteem (skill `/spec` sur ia_back + neo_ia), la session principale (Jarvis) a :

1. Conçu 4 nouvelles sections de template BRIEF (Gherkin, Recherche préalable, Implémentations de référence, Comment vérifier) en les **inventant**, aidée seulement de l'advisor, **sans lire aucune note canonique du vault**.
2. Briefé l'agent `skill-creator` en lui demandant de lire `comment-creer-skill` — **mauvaise canonique** (on touchait un template de spec/output, pas la structure d'une skill) — **sans vérifier empiriquement** qu'il l'a lue.
3. Découvert APRÈS le reproche de Raphael qu'il existait des notes canoniques directement pertinentes, jamais lues : [[pattern-spec-driven-development]], [[pattern-sdd-triangle]], [[pattern-spec-skill-deployment]] (template BRIEF déjà documenté), [[critique-2026-05-21-brief-distant-template-spec]] (un DA avait DÉJÀ critiqué ce template), [[running-implementation-notes]], [[methode-analyser-repo]].

## Pourquoi c'est une erreur

- CLAUDE.md forge ligne critique : "AVANT toute proposition / recherche web / refonte : consulter le vault via MCP forge-brain. Le vault contient probablement déjà la réponse."
- Les rules `forge-brain-proactive.md`, `sequence-canonique-modification.md`, `vault-consultation-protocol.md` l'exigent.
- Le travail produit est **non sourcé** : peut diverger des patterns canoniques, ignorer une critique DA existante, réinventer du déjà-documenté.
- Combinaison de 3 anti-patterns : biais d'action en session longue + délégation de la lecture vault au sub-agent + absence de vérification empirique.

## Quoi faire à la place

1. La SESSION PRINCIPALE consulte le vault EN PREMIER (`search_brain` sur le sujet réel, puis `read_note` EN ENTIER des canoniques).
2. Choisir la canonique par le SUJET de la tâche (SDD, BRIEF, handoff), pas par le type de fichier.
3. EXTRAIRE le contexte vault et le METTRE dans le brief du sub-agent (pattern [[pattern-mcp-brief-then-direct]]).
4. Le sub-agent re-consulte seulement en filet de sécurité.
5. VÉRIFIER empiriquement que le sub-agent a consulté le vault (cf erreur sub-agent claim sans empirie).

## Pattern général

La règle "consulter le vault d'abord" est advisory et a été zappée sous pression (session longue, fatigue, biais d'action). Question ouverte : faut-il un enforcement plus fort sans tomber dans le workflow-hook (anti-pattern doctrine 22 mai) ? Audit de réparation dédié : `claude-forge/PROMPT-audit-vault-jamais-consulte.md`.

## Liens

- [[methode-analyser-repo]]
- [[pattern-mcp-brief-then-direct]]
- [[pattern-spec-skill-deployment]]
- [[critique-2026-05-21-brief-distant-template-spec]]


## 2e occurrence — 28 mai 2026 (rédaction commentaire ticket Neoteem)

**Contexte** : Raphael demande "aide-moi à écrire ce commentaire" sur un ticket Jira "Comparatif devis" (étapes 1-5 + actions post-comparaison). La session principale a traité la demande comme **assistance rédactionnelle simple** et a rédigé 14 itérations V1→V14 du commentaire **sans une seule consultation du vault**.

**Cause-racine** : la ligne 14 de CLAUDE.md listait 6 catégories ("proposition / recherche web / refonte / audit / jugement / recommandation"). "Aide-moi à rédiger ce commentaire/ticket/spec" n'était dans **aucune** des 6. Trou doctrinal de scope, pas violation.

**Conséquences** :
- 14 itérations correctives de l'archi (V7→V10) car la session a supposé l'archi neo_ia/ia_back/front au lieu de la vérifier vault
- Notes vault pertinentes ratées : [[ia_back]], [[neo_ia]], [[critique-2026-05-21-brief-distant-template-spec]], skills `spec` et `craft-prompt`
- Raphael surface explicitement : "dès que je te pose une question, il faudrait que tu vérifies si on a des notes. S'il y en a tant mieux, sinon tu réponds quand même"

**Fix appliqué** :

- **AMEND CLAUDE.md L14** (28 mai 2026) — élargissement scope de "6 catégories" à "toute réponse substantielle à une question Raphael", ajout exemple explicite "rédaction d'un ticket/commentaire/spec/explication", clause "si aucune note pertinente → répondre quand même mais avoir cherché d'abord", anti-pattern daté ajouté.
- **Capitalisation feedback memory** : `feedback_archi_clarifier_avant_livrable_cross_stack` (tier-2) déjà créé en /done — règle "AskUserQuestion archi en V1" pour livrables cross-stack.

**Pattern transverse renforcé** : la règle de consultation vault doit avoir un scope **ouvert** (toute réponse substantielle) avec clause d'**échappatoire explicite** (si rien → répondre quand même). Sinon le LLM cherche un alibi pour ne pas chercher en classant la demande hors des catégories listées.

**Déclencheur de réactivation** : 3e occurrence de skip vault sur question d'assistance rédactionnelle → envisager Option B (hook session-health amendé) ou Option C (skill vault-reflex auto-trigger). Pour l'instant, AMEND L14 suffit.


## 3e occurrence — 1er juin 2026 (audit skills, doctrine consultée tardivement) + FIX Option C appliqué

**Contexte** : un agent menait un audit de 5 skills. Il a chargé les canoniques vault (`comment-creer-skill`, `mcp-vs-skills-doctrine`) **tardivement** — étape B après avoir déjà produit l'audit, au lieu d'AVANT. Raphael : « je ne comprends pas pourquoi il n'a pas fait le workflow entier ». Variante qualitative des occurrences 1-2 (« consulté en retard », pas « jamais »), mais même cause-racine : la règle de consultation est déclarative/passive et zappée sous pression.

**Diagnostic du réel** (vérifié sur fichiers `.claude/`) :
- `mcp-autostart.py` démarre le serveur MCP mais ne déclenche aucune consultation.
- `vault-cat-guard.py` interdit l'accès brut au vault (force le MCP) mais n'oblige pas à consulter.
- `skill-activation.py` (UserPromptSubmit) injecte un rappel `additionalContext` advisory — MAIS l'entrée `forge-brain` avait des triggers trop étroits (« cherche dans le vault », « note vault ») qui ne matchent pas une question de fond.
- **Aucun mécanisme ne RAPPELLE de consulter le MCP quand la question le mérite.**

**Fix appliqué — Option C (le déclencheur prévu par cette note à la 3e occurrence)** :

1. **`.skill-triggers.json`** — entrée `forge-brain` enrichie : passage de `triggers: [liste plate]` à `triggers_by_subject: {skill, agent, hook, claudemd, general}`. Le sujet `general` couvre les mots d'intention substantielle (propose, audit, analyse profonde, ton avis, recommande, rédige, compare, optimise, refonte, pourquoi). Mots EXCLUS volontairement : fix, corrige, petit, salut, merci.

2. **`skill-activation.py`** (via hook-creator) — le session-tracker mémorise désormais des clés composites `skill_name::sujet` au lieu de noms de skill nus. Conséquence : **re-fire quand le SUJET change** dans une même session (skill→agent = 2 rappels, car canoniques vault différentes), mais **anti-spam même sujet** (propose une skill ×3 = 1 rappel). Rétro-compatible : les 23 autres entrées en liste plate gardent le comportement once-per-session par nom de skill.

**Pourquoi re-fire par sujet** : cas surfacé par Raphael — dans une session il demande une skill PUIS un agent, ce sont des notes canoniques DIFFÉRENTES. Le once-per-session global ratait le 2e sujet.

**Validation empirique** (8/8 tests + stdin réel UTF-8 vérifié par la session principale, pas seulement le rapport sous-agent) :
- propose une skill → rappel sujet skill ✅
- crée un agent (même session) → rappel sujet agent ✅ (le cas Raphael)
- propose une skill ×3 → 1 seul rappel ✅
- merci / corrige typo → aucun rappel ✅
- entrée legacy (cc-news) → comportement inchangé ✅
- tracker corrompu → fail-open exit 0 ✅

**Gotcha encodage** : un test via `echo | py` en Git Bash Windows corrompt les accents (`crée` → octet cassé) et produit un faux négatif. Claude Code envoie du JSON UTF-8 propre → le hook matche correctement en prod. Toujours tester un hook à triggers accentués avec un payload UTF-8 explicite (`subprocess input=payload.encode('utf-8')`), jamais via echo bash.

**Doctrine respectée** : le hook reste advisory (exit 0, injecte un rappel, ne force rien) — conforme [[raisonnement-22mai-doctrine-vs-enforcement]] (pas de workflow-hook bloquant). C'est un sensor/guide léger, pas un gate.

**Hors-scope assumé** (Raphael : « reprend juste pour le mcp ») : le trou de routing du tripartite (« analyse profonde » ne déclenche pas boris/ecc/will-auditor) reste en option documentée non appliquée. Advisor disait « pas de trigger », DA disait « trigger-rappel léger ». Arbitrage : gardé prêt-à-coller si récidive (cf feedback reviole_3x = garde-fou structurel avant 3e occurrence).
