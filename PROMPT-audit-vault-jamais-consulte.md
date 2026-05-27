# Prompt pour une nouvelle session forge — Audit "vault jamais consulté en premier"

> Copier-coller ce prompt dans une nouvelle session Claude Code ouverte dans `claude-forge`.
> Contexte : session du 2026-05-27 où une erreur systémique a été commise.

---

## CONTEXTE DE L'ERREUR (ce qui s'est passé)

Pendant une session de travail sur le workflow Spec-Driven Development de Neoteem (skill `/spec` dans ia_back + neo_ia), j'ai (session principale Jarvis forge) commis une erreur de discipline grave et RÉCURRENTE :

**J'ai modifié des composants `.claude/` (templates BRIEF de la skill /spec) SANS JAMAIS consulter le vault forge-brain en premier.**

Détails factuels :
1. J'ai conçu 4 nouvelles sections de template BRIEF (Gherkin, Recherche préalable, Implémentations de référence, Comment vérifier) en les **inventant** (aidé seulement de l'advisor), sans lire AUCUNE note canonique du vault.
2. J'ai briefé l'agent `skill-creator` en lui demandant de lire `comment-creer-skill` — mais (a) c'était la MAUVAISE canonique (on touchait des templates de spec/output, pas la structure d'une skill), et (b) je n'ai jamais vérifié empiriquement qu'il l'a réellement lue.
3. Quand Raphael m'a repris ("ni toi ni skill-creator n'avez call le vault"), j'ai ENFIN cherché dans le vault et découvert qu'il existait des notes canoniques directement pertinentes que personne n'avait lues :
   - `pattern-spec-driven-development` (SDD, Thariq/Boris/Anthropic)
   - `pattern-sdd-triangle` (SPEC/TESTS/CODE, Drew Breunig)
   - `pattern-spec-skill-deployment` (template BRIEF — DÉJÀ documenté dans le vault !)
   - `critique-2026-05-21-brief-distant-template-spec` (un devil's advocate avait DÉJÀ critiqué ce template BRIEF)
   - `running-implementation-notes` (pattern Thariq)
   - `methode-analyser-repo` (exploration AVANT assumptions)
   - `comment-creer-agent` (pattern initializer agent → coding agent, harnais long-running Anthropic)

C'est exactement l'anti-pattern que CLAUDE.md et les rules forge interdisent. Les commits concernés (déjà pushés) :
- ia_back `develop` : `1e20c38` (enrichissement /spec) + `7f1d955` (BRIEF auto-suffisant)
- neo_ia `develop` : `2257ec3` + `2525840`

---

## TA MISSION (4 phases, dans l'ordre)

### PHASE A — Diagnostiquer la cause racine de l'erreur systémique

Tu es l'enquêteur. Réponds factuellement à :

1. **Pourquoi la session principale a-t-elle sauté la consultation vault ?** Hypothèses à vérifier dans les rules :
   - Est-ce que les rules forge (`forge-brain-proactive.md`, `sequence-canonique-modification.md`, `check-before-create.md`, `vault-consultation-protocol.md`) exigent que la SESSION PRINCIPALE consulte le vault, ou seulement les SUB-AGENTS ?
   - Lis ces 4 rules EN ENTIER. Identifie le trou : la séquence A→B→C→D→E parle de "LIRE canoniques EN ENTIER", mais est-ce assez explicite que c'est la SESSION qui doit le faire AVANT de briefer un sub-agent, et pas déléguer cette lecture au sub-agent ?
   - Y a-t-il un hook qui aurait dû bloquer ? (`delegate-guard.py` ou autre). Pourquoi n'a-t-il pas tiré ?

2. **Pourquoi le brief au sub-agent était-il insuffisant ?** Le pattern correct est documenté dans `pattern-mcp-brief-then-direct` (vault) : la session principale consulte le vault, EXTRAIT le contexte pertinent, et le MET DANS LE BRIEF du sub-agent. Le sub-agent re-consulte seulement en filet de sécurité. Vérifie : est-ce que ce pattern est appliqué dans les rules de dispatch forge ? Est-il enforced ou juste advisory ?

3. **Vérifier empiriquement** : lis les transcripts/commits. Le brief que j'ai donné à skill-creator demandait de lire `comment-creer-skill`. Est-ce la bonne canonique pour modifier un TEMPLATE DE BRIEF (output de spec) ? Ou aurait-il fallu `pattern-spec-skill-deployment` + `pattern-spec-driven-development` + la critique DA existante ?

### PHASE B — Auditer la qualité du travail produit sans vault

Maintenant qu'on SAIT que le vault n'a pas été consulté, vérifie si le résultat est quand même bon ou s'il y a des écarts avec les canoniques.

1. **Lis EN ENTIER via MCP forge-brain (`read_note` SANS max_lines)** :
   - `pattern-spec-driven-development`
   - `pattern-sdd-triangle`
   - `pattern-spec-skill-deployment`
   - `critique-2026-05-21-brief-distant-template-spec` (CRITIQUE EXISTANTE — quels reproches avaient été faits ? Ont-ils été respectés dans les nouvelles modifs ?)
   - `running-implementation-notes`
   - `methode-analyser-repo`

2. **Lis les modifs réellement commitées** :
   - `ia_back/.claude/skills/spec/SKILL.md`
   - `ia_back/.claude/skills/spec/references/output-templates.md`
   - `neo_ia/.claude/skills/spec/SKILL.md`
   - `neo_ia/.claude/skills/spec/references/output-templates.md`

3. **Croiser** : les 4 sections ajoutées (Gherkin, Recherche préalable, Implémentations de référence, Comment vérifier) + les 3 modifs précédentes (check sécu IA, Observabilité Langfuse, décisions assignées) sont-elles :
   - Cohérentes avec les patterns canoniques du vault ?
   - En contradiction avec la critique DA de mai 2026 sur le template BRIEF ?
   - Redondantes avec quelque chose déjà documenté ?
   - Manquantes de quelque chose que le vault recommande (ex : le pattern initializer→coding agent d'Anthropic, le SDD triangle) ?

4. **Verdict** : liste des écarts mesurables. Pour chacun : KEEP (bon) / FIX (corriger) / ADD (manque). Avec preuve citée (note vault + ligne du template).

### PHASE C — Renforcer l'enforcement pour que ça ne se reproduise JAMAIS

Le vrai problème : la règle "consulter le vault en premier" est advisory et la session principale l'a zappée sous pression (session longue, fatigue, biais d'action).

Propose (NE PAS appliquer sans validation Raphael) :

1. **Faut-il un mécanisme d'enforcement** ? Options à évaluer (avec leurs tradeoffs, cf doctrine 22 mai "hooks = lint/sécu/scope, JAMAIS workflow") :
   - Une rule plus explicite "SESSION PRINCIPALE consulte vault AVANT brief sub-agent créateur" ?
   - Un renforcement de `sequence-canonique-modification.md` avec une étape "0. SESSION lit le vault et MET le contexte dans le brief" ?
   - Le pattern `pattern-mcp-brief-then-direct` doit-il devenir OBLIGATOIRE dans tous les briefs de sub-agents créateurs ?
   - Attention : un hook qui force la consultation vault = workflow hook = potentiellement anti-pattern doctrine 22 mai. Évalue si c'est lint/sécu/scope ou workflow.

2. **Capitaliser l'erreur** : créer une note `Knowledge/erreurs/erreur-vault-jamais-consulte-session-principale.md` (template erreur) + un feedback mémoire `feedback_session_consulte_vault_avant_brief.md`.

3. **Mettre à jour CLAUDE.md** si besoin (gotcha "la session principale DOIT consulter le vault AVANT de briefer un sub-agent, ne jamais déléguer cette lecture").

### PHASE D — Synthèse + plan d'action

1. Résumé en 10 lignes max : cause racine, écarts trouvés, fix proposé.
2. Liste priorisée des actions (P0 = corriger un écart canonique réel, P1 = enforcement, P2 = capitalisation).
3. Présenter à Raphael AVANT toute application. Il tranche.

---

## CONTRAINTES

- **Tu commences par le vault. Pas d'exception.** C'est précisément l'objet de l'audit — montre l'exemple.
- Lis les canoniques EN ENTIER (`read_note` sans max_lines), pas `search_brain` extraits.
- Vérifie empiriquement chaque claim (grep, read fichiers réels, git log) avant de l'affirmer.
- Ne corrige rien sans validation Raphael — c'est un audit, pas une exécution.
- Applique la séquence A→B→C→D→E à toi-même.
- Si tu dispatches un sub-agent : mets le contexte vault DANS le brief (pattern brief-then-direct), ne lui délègue pas la lecture canonique aveugle.

## SORTIE ATTENDUE

1. Cause racine de l'erreur (Phase A) — factuelle, avec citation des rules
2. Tableau des écarts (Phase B) — KEEP/FIX/ADD avec preuve note vault + ligne
3. Proposition d'enforcement (Phase C) — avec tradeoff doctrine 22 mai
4. Plan d'action priorisé P0/P1/P2 (Phase D)
