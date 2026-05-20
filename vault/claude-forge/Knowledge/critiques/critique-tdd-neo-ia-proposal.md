---
titre: "Critique - Architecture TDD/Eval-Driven neo_ia (Test-First a 3 vitesses)"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-19
auteur: claude
aliases:
  - critique tdd neo_ia
  - test-first 3 vitesses critique
  - test-spec-interviewer critique
  - tdd-guard hook critique
  - eval-driven neo_ia
tags:
  - "#type/critique"
  - "#domaine/claude-code"
  - "#projet/neo_ia"
---

# Critique - Architecture TDD/Eval-Driven neo_ia

**Intention declaree :** Passer neo_ia en TDD strict avec 3 vitesses (unit local / integration pre-PR / functional DeepEval nightly), un nouvel agent test-spec-interviewer, un hook tdd-guard.py bloquant, et un flip du pipeline pour produire les tests AVANT le code.

---

## Verdict global

**Bloquants : 4 | Majeurs : 4 | Mineurs : 2**

**Decision recommandee : REWORK**

Trois bloquants independants (doublon /spec, casse /go autonome, hook trop large) plus un trou strategique non specifie (variance LLM sur seuils). Pas patchable en une passe - la proposition melange une bonne idee (eval-driven, valide par le vault agents-evaluation) avec trois implementations cassees a reecrire separement.

---

## Verdict point par point (questions Raphael)

### Q1 - Friction interviewer (5-8 questions/feature)

**Verdict : MAJEUR**

5-8 questions via AskUserQuestion sur CHAQUE feature = 5-15 min ajoutees en mode interactif, mais pire : **rupture du flow**. Raphael travaille en sprint de focus, pas en Q&A administrative.

- Feature taille S (~30 min coder) -> interview ajoute 30-50% de temps. Le ratio s inverse pour les petites features.
- Feature taille M (~2h) -> interview ajoute ~10%. Acceptable.

Le probleme n est pas la duree moyenne, c est la **distribution**. Sur 80% des features (S/petites), l interview est plus longue que le dev. Sur les 20% restantes (M/L), elle est utile.

**Fix possible :** Interview conditionnelle - if feature_size in {M, L} or has_llm_agent: interview. Sinon skip et test-writer infere depuis le BRIEF.

### Q2 - TDD strict sur agents LLM non-deterministes

**Verdict : MAJEUR (la proposition est silencieuse sur le sujet le plus dur)**

Le red-green-refactor strict suppose qu un test failed->passed est un signal causal sur le code. Sur du LLM avec seuil 0.80 :
- Run 1 (red) : score 0.45 -> fail attendu
- Implementation prompt -> Run 2 (green) : score 0.85 -> pass
- Run 3 (CI nightly, sans changement de code) : score 0.78 -> fail
- Run 4 : 0.86 -> pass

Ce n est pas du TDD, c est du **stochastic gating**. La proposition ne dit RIEN sur :
- Combien de runs par eval ? (1 = flake garanti, 10 = cout x10)
- Quel critere statistique ? (moyenne >= seuil ? p95 >= seuil ? worst-of-n ?)
- Que faire d un flake en CI : retry auto ? marquer flaky ? bloquer ?

Le vault agents-evaluation valide eval-driven comme concept (90% pass-rate DeepEval + golden datasets) mais le concept implique une **strategie de variance**. Sans elle, soit on tolere la flake (et on perd l enforcement), soit on bloque sur du bruit (et l equipe desactive le gate en 2 semaines - pattern documente dans erreur-advisory-rules-insuffisantes).

**Manque dans la proposition :** spec explicite k runs, agregation, retry policy, seuil = bande de confiance pas valeur ponctuelle. Sans ca, le niveau functional est de la decoration.

### Q3 - Hook tdd-guard.py bloquant

**Verdict : BLOQUANT**

Le vault contient erreur-marker-ttl-blocage-agents (TTL 60min bloquait sessions longues) et erreur-advisory-rules-insuffisantes (3 incidents prouvant que les advisory echouent, donc les hooks sont OK - mais doivent etre chirurgicaux). Ce hook coche les mauvaises cases :

**Cas legitimes que le hook va casser :**
- Rename de symbole (refactor pur, comportement identique) -> Edit sur 10 fichiers, aucun test a ecrire, hook bloque les 10
- Extract method / extract class -> idem
- __init__.py mis a jour pour exposer un nouveau module -> pas de test_init.py qui ait du sens
- Migrations Alembic (apps/*/migrations/) -> generees, pas testables unit
- Fichiers de config (config.py, settings.py) -> pas de test unit pertinent
- Hotfix de prod 3h du matin -> la derniere chose qu on veut c est un hook bloquant
- Generation de code (protobuf, openapi clients) -> idem
- Update de dependance qui change une signature -> cascade d Edits dans toute la codebase

La proposition mentionne CLAUDE_AGENT=test-writer et --no-tdd comme bypass. **Insuffisant** :
- --no-tdd env var = soit on l oublie (hook bloque), soit on l active par defaut dans sa session (et le hook n enforce plus rien)
- Pas de bypass pour rename/extract/migrations/init/config

**Pattern correct (depuis le vault pattern-vault-query-guard) :**
- Bypass paths explicites (regex sur migrations/, __init__.py, config files, tests/)
- Bypass via detection semantique du changement (impossible en hook simple) OU via marker .refactor-marker pose par un agent refactor-only qui jure comportement preserve
- Le hook ne doit JAMAIS bloquer un Edit dont le diff ne change pas la signature publique.

**Faisabilite reelle :** un hook qui detecte 'ce diff change le comportement observable et donc necessite un test' est de la magie statique. La proposition pretend le faire avec existe-t-il un test_*.py correspondant - c est un mauvais proxy. On peut avoir test_foo.py qui existe sans qu il teste la nouvelle fonctionnalite.

### Q4 - Pipeline 4 vers 6 etapes

**Verdict : MAJEUR**

Pipeline actuel : architect -> dev-* -> test-writer -> code-reviewer = 4 etapes.
Propose : architect -> test-spec-interviewer -> test-writer (RED) -> dev-* (GREEN) -> test-writer (REFACTOR) -> code-reviewer = 6 etapes.

**+50% d etapes** pour 0 amelioration de qualite validee par evidence. Le vault pattern-architect-first-pipeline documente que les agents sequentiels saturent a 200K contexte ; chaque etape ajoutee = un point de defaillance (timeout, contexte sature, marker manquant).

Sur feature M (typique neo_ia) :
- Pipeline actuel : ~25-40 min (architect 5 + dev 15 + test-writer 8 + reviewer 7)
- Pipeline propose : ~50-70 min (architect 7 + interviewer 10 + test-writer RED 8 + dev 15 + test-writer REFACTOR 8 + reviewer 7)

**Quasi-doublement du wall-clock**. Et test-writer est appele 2 fois, ce qui double les risques de drift entre les deux passes (le test-writer REFACTOR peut desaligner les tests avec ce que dev a reellement implemente si dev a diverge du contrat - alors les tests RED initiaux etaient sur des specifications mortes).

### Q5 - Conflit avec dev-discipline.md (simplicity first, 3+ usages)

**Verdict : MAJEUR**

dev-discipline.md dit explicitement pas d abstraction tant qu il n y a pas 3+ usages. test-spec-interviewer = nouvel agent dedie a un use case (interview pre-test) sans aucune preuve de 3+ usages reels par mois.

Calcul honnete : neo_ia fait combien de features taille M+ par mois ? Probablement 5-15. Sur celles-ci, combien justifient une interview de 5-8 questions ? Optimiste : 30-50%. Donc 2-7 usages/mois. A la limite du seuil.

Surtout, **/spec etend deja le BRIEF avec acceptance tests** (point 5 de la proposition). Donc soit /spec est l interviewer (et test-spec-interviewer est redondant - voir Q7), soit /spec ne fait pas le job et c est /spec qu il faut corriger.

**Conclusion :** sur-ingenierie probable. Le pattern Boris cite dans le vault (Workflow Boris) est explicite : minimal harness, maximize signal. Ajouter un agent pour un use case ambigu = anti-pattern.

### Q6 - Interviewer = goulot d etranglement, casse /go autonome

**Verdict : BLOQUANT**

/go est concu pour tourner en mode autonome (Raphael peut le lancer et partir). AskUserQuestion est par definition synchrone et bloquant : pas de reponse -> pas de progression. L escalade a Raphael proposee dans le point 2 EST le deadlock, pas la solution.

Scenarios casses :
- Raphael lance /go feature-X a 18h avant de partir -> interviewer pose 8 questions a 18h05 -> pipeline gele jusqu au lendemain
- Mode CI / scheduled task -> pas d utilisateur connecte -> pipeline gele indefiniment, hooks de timeout vont kill le run

**Fix obligatoire :** Mode dual.
- Mode /go --interview (explicite, interactif) : test-spec-interviewer pose ses questions
- Mode /go (defaut, autonome) : test-spec-interviewer skip et utilise le BRIEF + plan architect tel quel, genere tests-spec.md sans interaction (mode best effort), produit un warning si infos manquantes

Sans ce dual mode, la proposition CASSE l autonomie qui est un acquis structurel de neo_ia.

### Q7 - Doublon avec /spec

**Verdict : BLOQUANT**

Le point 5 dit : /spec etendu : section Acceptance Tests obligatoire dans le BRIEF (cas nominaux + edge + erreurs + metriques DeepEval pour agents).

Le point 2 dit : test-spec-interviewer pose 5-8 questions : criteres d acceptation mesurables, edge cases, entrees invalides, contrats d erreur, seuils DeepEval.

**C est la meme chose**. Les utilisateurs vont :
- Soit remplir /spec a fond, puis l interviewer leur repose les questions -> frustration -> skip de l interview
- Soit remplir /spec a minima en sachant que l interviewer compensera -> /spec devient une coquille vide
- Soit l equipe se demande c est lequel le canonique et utilise les deux a moitie

Le vault pattern-spec-driven-development et la memoire spec-driven-development-pattern documentent que le BRIEF EST deja l artefact qui porte les acceptance criteria. Ajouter un second agent qui demande la meme chose = violation directe du Single Source of Truth (memoire single-source-of-truth).

**Fix :** UN seul artefact. Soit /spec fait l interview (et test-spec-interviewer disparait), soit on enleve la section Acceptance Tests de /spec et c est l interviewer qui produit tests-spec.md comme artefact unique. Pas les deux.

### Q8 - Cout Gemini DeepEval nightly

**Verdict : MAJEUR**

La proposition dit functional DeepEval (Gemini) -> nightly + pre-release seulement. Bien, c est conscient du cout. Mais :
- Nightly = 1 run/nuit. Si k=5 pour gerer la variance (Q2), c est 5 runs.
- DeepEval typique pour neo_ia (3 agents NeoChat/NeoDoc/NeoMail) avec golden dataset de ~30 scenarios par agent = 90 scenarios. Chaque scenario fait des tool calls (RAG vault, BDD, etc.) = 5-20 LLM calls. A k=5 -> 90 x 10 x 5 = **4500 LLM calls Gemini par nuit**.
- Gemini 2.5 Pro input ~1.25 USD/M tokens, output ~5 USD/M tokens. Si scenario moyen 5K tokens in + 1K out = 6K tokens x 4500 = 27M tokens/nuit ~ **~50-80 USD/nuit** = ~1500-2400 USD/mois rien que pour eval nightly.

C est probablement absorbable mais ce n est pas trivial. Et :
- Pre-release = combien de fois ? Si Raphael lance /go 5 fois/jour et que pre-release tourne a chaque PR -> explosion
- Le manque de spec sur la frequence pre-release et sur k = trou budgetaire

**Fix :** spec de cout explicite. Nightly = 1 run/scenario sauf flake detectee -> retry. Pre-release = trigger manuel uniquement, pas auto sur push. Mettre un budget cap (ex: 100 USD/jour) avec circuit breaker.

### Q9 - Variance LLM + CI flake -> desactivation

**Verdict : BLOQUANT**

Lie a Q2 mais bloquant a part car c est la dynamique sociale qui tue le systeme. Pattern documente dans erreur-advisory-rules-insuffisantes : tout enforcement percu comme arbitraire (flake) est progressivement desactive. Avec un seuil ponctuel sur LLM stochastic :
- Semaine 1 : 2 flakes, on rale mais on retry
- Semaine 3 : 10 flakes, on ajoute une whitelist
- Semaine 6 : on commente pytest --deselect functional_* dans le CI temporairement
- Mois 3 : functional DeepEval desactive en CI, ne tourne plus que manuellement, plus personne ne regarde

**Fix obligatoire :** Pas de gate blocking sur functional tant que :
1. Strategie de variance definie (k runs, agregation)
2. Systeme de flake quarantine automatique (3 fails consecutifs = quarantine, ping a Raphael, pas merge bloquante)
3. Dashboard de stabilite des evals (% pass rate par scenario sur 30 jours)

Sans ces 3 garde-fous, functional doit etre **advisory-only en CI** (report dans le PR comment, pas merge gate). Promouvoir en gate apres 30 jours de stabilite prouvee.

### Q10 - Feature simple = over-engineering, critere de bypass

**Verdict : MAJEUR**

Exemple Raphael : ajouter un champ a un endpoint REST. Pipeline complet :
- architect : Contrats testables : field_x: str optional, validation X, error 422 si Y
- test-spec-interviewer : 5-8 questions sur edge cases d un champ string
- test-writer RED : test_endpoint_accepts_field_x, test_endpoint_rejects_invalid_field_x
- dev : ajoute le champ (5 lignes Pydantic)
- test-writer REFACTOR : edge cases
- code-reviewer

Pour 5 lignes de code. **Ratio overhead 50:1**.

La proposition ne definit aucun critere de bypass. La rule dev-discipline mentionne simplicity first mais pas comment l operationnaliser.

**Fix :** Taille de feature explicite dans le BRIEF (S/M/L). Mode :
- S (<= 30 LoC, pas de logique metier, pas d agent LLM) -> pipeline simple (architect light + dev + test-writer + reviewer, pas d interview, pas de RED-GREEN strict, juste test apres)
- M/L -> pipeline complet TDD
- Agents LLM -> toujours pipeline complet + eval-driven

Sans critere taille, le pipeline lourd est applique partout -> equipe contourne -> enforcement meurt (Q9 again).

---

## Si je devais le faire marcher malgre mes objections

Chemin concret vers l avant, en 3 vagues, sans toucher au coeur autonome de /go :

**Vague 1 - Eval-Driven Agents (valeur elevee, risque faible)**
1. Etendre /spec avec section Acceptance Tests + Eval Spec (golden scenarios + metriques DeepEval + seuils + variance policy k=3, agregation = mean). **PAS de nouvel agent interviewer**.
2. Mettre a jour architect.md pour produire Contrats testables - signatures + error cases + behavioral specs. Une rule, pas un agent.
3. Ajouter un agent unique eval-spec-writer (sonnet, effort:high) qui consomme /spec et produit tests/eval/feature.eval.yaml (scenarios + metriques). Tourne en pre-commit pour features avec agent LLM, sinon skip.
4. DeepEval en CI : **advisory pendant 30 jours**, report dans PR comment. Promotion en gate seulement apres stabilite prouvee (% flake < 5%).

**Vague 2 - TDD Unit (valeur moyenne, risque moyen)**
5. Slash command /tdd feature (skill, pas hook) : workflow opt-in pour le dev quotidien. Red-green-refactor manuel, pas d enforcement.
6. Modifier test-writer.md : ajouter mode --first (genere tests AVANT impl) declenche par /tdd, sinon comportement actuel.
7. **PAS de hook tdd-guard pour l instant**. Mesurer sur 30 jours combien de features sont effectivement faites en TDD via /tdd. Si > 50% organique -> considerer un hook. Sinon, le hook serait punitif.

**Vague 3 - Enforcement (si Vague 1+2 marchent)**
8. Si Vague 1 montre que les acceptance tests sont systematiquement ecrites -> hook acceptance-tests-guard qui verifie que la section existe dans le BRIEF avant pipeline. Pattern marker existence-seule (vault pattern-architect-first-pipeline).
9. Si Vague 2 montre adoption TDD > 50% -> hook tdd-guard avec bypass paths explicites (migrations, __init__.py, config, rename refactors via marker refactor-only).

**Ce qu on ne fait pas :**
- Pas d agent test-spec-interviewer separe (doublon /spec)
- Pas de flip 4 vers 6 etapes du pipeline (test-writer reste 1 appel, pas 2)
- Pas de hook tdd-guard d emblee (apprendre avant d enforcer)

---

## 5 modifications concretes a apporter a la proposition

1. **SUPPRIMER l agent test-spec-interviewer**. Fusionner ses responsabilites dans /spec etendu (point 5 de la proposition originale). Une seule source de verite pour les acceptance tests. Resout Q5, Q7, Q6 partiellement.
2. **DOWNGRADE le hook tdd-guard d emblee en simple skill /tdd opt-in**. Mesurer adoption pendant 30 jours avant de considerer un hook. Si hook ajoute plus tard, exige bypass paths explicites (migrations, __init__.py, config*, tests/, marker refactor-only). Resout Q3.
3. **DEFINIR variance policy explicite pour functional DeepEval** : k=3 runs minimum, agregation = mean (pas valeur ponctuelle), retry auto sur 1 flake, quarantine sur 3 fails consecutifs avec ping Raphael (pas merge bloquante). Sans ca, functional reste advisory-only en CI. Resout Q2, Q9.
4. **AJOUTER mode dual /go avec --interview optionnel** (defaut = autonome, sans interview). L interview ne doit JAMAIS bloquer le pipeline en mode autonome ou CI. Resout Q6.
5. **AJOUTER critere de bypass par taille de feature** dans la rule testing-mandatory : S (<= 30 LoC, no LLM) -> pipeline simple (4 etapes actuelles, pas de RED-GREEN strict). M/L et tout ce qui touche un agent LLM -> pipeline complet TDD. Resout Q10, Q4 partiellement.

Apres ces 5 modifications : pipeline reste a 4-5 etapes (au lieu de 6), un seul artefact de specification (/spec), enforcement progressif (skill -> mesure -> hook), variance LLM geree, autonomie /go preservee, bypass clair pour les petites features.

---

## Vault - Historique pertinent

Evidence directe utilisee dans cette critique :

- [[erreur-marker-ttl-blocage-agents]] - pattern marker doit etre existence-seule + bypass paths explicites
- [[erreur-advisory-rules-insuffisantes]] - 3 incidents prouvent que rules trop strictes ou trop floues finissent desactivees ; alimente directement Q9 (dynamique sociale de desactivation)
- [[erreur-hooks-bash-quoting-windows]] - toute hook ajoutee doit utiliser pattern python avec chemin absolu git rev-parse ; contrainte plateforme pour tout hook tdd-guard futur
- [[agents-evaluation]] - valide eval-driven comme CONCEPT (DeepEval, 90% pass-rate, golden datasets), mais documente aussi LLM-as-Judge ajoute latence/cout significatif et trajectory vs outcome (20-40% delta)
- [[pattern-architect-first-pipeline]] - pattern reference pour les hooks markers ; documente agents sequentiels, max 6-8 ops, contexte 200K, pas de TTL sur markers
- [[pattern-spec-driven-development]] - le BRIEF EST l artefact qui porte les acceptance criteria (alimente Q7)
- Memoire single-source-of-truth - UN fichier canonique par concept (viole par doublon /spec vs test-spec-interviewer)
- Memoire dev-discipline (rule neo_ia) - pas d abstraction sans 3+ usages reels (alimente Q5)
- Memoire bash-permission-format et python-path-windows-hooks - implementation hook tdd-guard a des contraintes plateforme a respecter
