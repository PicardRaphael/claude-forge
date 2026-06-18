---
titre: "Critique — ia-workbench / spec discovery cross-repo"
resume: "Devil's advocate sur le repo de management ia-workbench et son skill /spec cross-repo : trou d'oracle (TROU 1, BLOCKING), risque de 4e copie du référentiel Jira (TROU 2, BLOCKING — prior art pattern-vault-source-unique existe déjà), discovery sur brain périmé, coût tokens abonnement, dérive orchestrateur."
aliases:
  - "critique ia-workbench"
  - "critique spec discovery cross-repo"
  - "trou oracle tickets parfaits"
  - "quatrieme copie epics-jira"
domaine: claude-code
type: knowledge
derniere-maj: 2026-06-18
auteur: claude
sources:
  - "[[pattern-vault-source-unique-sync-mecanique]]"
  - "[[pre-compute-vs-inference-loops-boris]]"
  - "[[multi-agent-handoff-loss-pattern]]"
tags:
  - "#type/knowledge"
  - "#domaine/claude-code"
---

## Devils Advocate — ia-workbench / skill /spec cross-repo

**Intention déclarée :** Un repo frère sans code (`ia-workbench`) dont le skill `/spec` fait une discovery cross-repo (brain + lecture code neo_ia/back-ts/bdd) puis crée des tickets Jira parfaits à 80-90 %, pour fiabiliser l'ENTRÉE avant d'automatiser l'exécution par un loop.

---

### Verdict

**Bloquants :** 2 | **Avertissements :** 4 | **Nitpicks :** 2

**Décision recommandée :** LIVRER AVEC CORRECTIONS — le principe (fiabiliser l'entrée avant le loop) est sain et conforme à la doctrine Boris. Mais deux trous structurels doivent être bouchés AVANT de construire, sinon on construit une amplification aveugle (TROU 1) sur un référentiel qui re-dérive (TROU 2).

---

### Si je devais le faire marcher malgré mes objections

**TROU 1 — donner un oracle bon marché AVANT d'écrire la première ligne du loop.**
- Définir une rubrique de ticket "parfait" en 5-8 critères BINAIRES vérifiables sans jugement (epic correct ? étiquettes présentes ? ADF valide ? US cross-repo découpées dans le bon ordre back-ts→neo_ia ? AC présents ? lien parent correct ? pas de SQL inventé ?). C'est la rubrique de la skill `outcomes-test` déjà existante en forge.
- Capturer le verdict humain À CHAQUE relecture : Raphael relit déjà à l'œil — il suffit qu'il tape `accepté` / `corrigé: <quoi>` et qu'un append vault (`Knowledge/spec-outcomes/`) garde 1 ligne. Coût ~0, c'est le SEUL moyen d'avoir un dénominateur. Sans ça, "80 %" est une croyance, pas une mesure.
- Le loop ne s'allume QUE quand la mesure dépasse un seuil (ex : 15 tickets consécutifs ≥ rubrique). Gate empirique, pas un pari.

**TROU 2 — appliquer le pattern forge DÉJÀ canonique au lieu d'inventer.**
- `[[pattern-vault-source-unique-sync-mecanique]]` règle exactement ça : le référentiel Jira (6 epics figés, étiquettes, protocole ADF, hiérarchie) devient SOURCE UNIQUE dans le **vault** (note canonique unique, ex `Knowledge/jira/referentiel-epics-figes.md`), et un script de sync régénère le bloc entre marqueurs `<!-- SYNC:jira:start/end -->` dans CHAQUE `references/epics-jira.md` consommateur (neo_ia, back-ts, skill forge, et workbench).
- Sync à la MAINTENANCE (quand le référentiel change), pas au runtime — zéro surcoût par ticket, idempotent, round-trip vérifié.
- Workbench ne devient PAS une 4e copie manuelle : il devient un 4e CONSOMMATEUR régénéré mécaniquement. Les 3 copies actuelles qui ont déjà dérivé sont reconvergées par le même script. C'est le fix de la dette existante ET la prévention de la 4e.

---

### Angle Technique — Qu'est-ce qui se casse ?

**Objections :**
- **BLOCKING (TROU 1) — pas d'oracle = amplification aveugle.** Le plan repose sur "80-90 % parfaits" jugé à l'œil, sans dénominateur, sans capture de l'échec, sans boucle d'amélioration. C'est exactement ce que `[[pre-compute-vs-inference-loops-boris]]` interdit implicitement : Boris assume "most ideas are bad, maybe 20 % good" MAIS son loop a (a) un checkpoint vérifiable — le code compile/teste — et (b) un gate humain — il relit les PR le matin. Le loop /spec n'a ni checkpoint vérifiable (un ticket ne "compile" pas) ni métrique. Sans oracle on ne saura JAMAIS si on est à 80 ou 40 %, et un loop qui amplifie une entrée non mesurée produit du déchet en série — `[[multi-agent-handoff-loss-pattern]]` mesure 17× l'erreur en swarm sans point de validation au handoff. Fix : rubrique binaire + capture verdict (voir ci-dessus).
- **BLOCKING (TROU 2) — 4e copie qui dérive.** Le référentiel Jira embarqué en `references/epics-jira.md` existe en 3 exemplaires "synchronisés" QUI ONT DÉJÀ DÉRIVÉ (cf project_neoteem_back_ts : "3 exemplaires synchronisés"). Embarquer une 4e copie statique dans workbench reproduit mécaniquement la dette. Le pattern forge `[[pattern-vault-source-unique-sync-mecanique]]` est la réponse canonique DÉJÀ validée — l'ignorer serait une régression doctrinale. Fix : vault source unique + sync entre marqueurs (voir ci-dessus).
- **IMPORTANT — discovery sur brain périmé.** Le brain NeoTeem (carte des architectures) pointe encore ia_back mourant. Une discovery qui fait confiance au brain pour dire "quels repos sont touchés" va router vers un repo décommissionné. Fix : la discovery DOIT croiser brain (rapide, possiblement périmé) AVEC lecture du code réel (lent, vrai) et SIGNALER les divergences au lieu de trancher — l'humain arbitre. Marquer ia_back comme `deprecated` dans le brain en priorité 0.
- **IMPORTANT — découpage cross-repo automatique = piège de contrat.** "US endpoint back-ts → puis US tool neo_ia" suppose que l'IA connaît le contrat d'API (shape de l'endpoint, params du tool) AVANT qu'il existe. Le découpage est trivial à énoncer mais le CONTENU de l'US back-ts (forme de la réponse que le tool neo_ia consommera) est précisément ce que l'IA ne peut pas inventer (contrainte forte Raphael). Fix : /spec produit le SQUELETTE des US liées + un placeholder explicite "contrat d'API à définir par l'humain/discovery" — jamais un contrat inventé.

---

### Angle Stratégique — Est-ce le bon problème ?

**Objections :**
- **IMPORTANT — l'ordre est juste, mais le séquencement du build doit suivre.** Fiabiliser l'entrée avant le loop = exactement la bonne intuition (pre-compute Boris). MAIS le plan veut construire la discovery cross-repo multi-sous-agents AVANT d'avoir prouvé que le /spec mono-repo + capture d'oracle marche. Risque : on construit la pièce la plus chère (discovery cross-repo) sur une fondation (oracle) absente. Séquence recommandée : (1) oracle + rubrique sur les /spec mono-repo MATURES existants, (2) mesurer 2-3 semaines, (3) SEULEMENT alors bâtir le /spec workbench cross-repo. Le cross-repo n'apporte rien tant que le mono-repo n'est pas mesuré bon.
- **NITPICK — "loupe à tickets" vs skills /spec mono-repo matures : frontière floue à l'usage.** Raphael veut garder les /spec mono-repo pour "je sais déjà que ça ne touche qu'un repo". Mais qui décide "je sais déjà" ? Si l'humain se trompe et lance le /spec mono-repo sur un besoin en réalité cross-repo, le ticket est faux par construction. Trancher : règle explicite de routage (par défaut workbench/discovery ; mono-repo uniquement sur affirmation explicite "mono-repo X").

---

### Angle Pratique — Combien de temps avant l'abandon ?

**Objections :**
- **IMPORTANT — coût tokens discovery multi-sous-agents À CHAQUE ticket, sur abonnement.** Raphael est sur abonnement (peur explicite des tokens) ; multi-agents = +200-500 %. Une discovery qui lit le code réel de 3 repos via sous-agents À CHAQUE création de ticket est insoutenable si la majorité des besoins sont en réalité mono-repo ou répétitifs. Fix pre-compute : (a) cache de discovery par zone de code (un map repos↔domaines régénéré à la maintenance, pas re-scanné par ticket), (b) discovery cross-repo DÉCLENCHÉE seulement quand le besoin est ambigu, pas systématique, (c) brain d'abord (cheap), code réel seulement sur divergence.
- **AVERTISSEMENT — dérive insidieuse vers l'agent orchestrateur interdit.** Le plan dit "workbench prépare, repos exécutent" — sain. Mais un /spec qui (1) délègue à N sous-agents d'exploration, (2) agrège, (3) découpe en US liées multi-repos, (4) crée dans Jira, RESSEMBLE déjà à de l'orchestration. La frontière tient tant que workbench ne LANCE jamais l'exécution (/feature, /go) des repos. Garde-fou dur : workbench n'a PAS accès en write au code des repos produit, et ne peut PAS invoquer leurs skills d'exécution. Quand le loop multi-stories arrivera → outil Workflow (pre-compute orchestration), PAS un agent orchestrateur dans workbench. À surveiller à chaque ajout de skill workbench.
- **NITPICK — permissions.allow cross-repo lecture neot-v2/** : techniquement OK mais élargit la surface. Scoper en read-only strict (`Read`/`Grep`/`Glob` sur `neot-v2/**`, jamais `Write`/`Edit`/`Bash` destructif) et le documenter, sinon un futur sous-agent workbench pourrait écrire cross-repo par accident.

---

### Vault — Historique pertinent

- `[[pattern-vault-source-unique-sync-mecanique]]` (27 mai 2026) — prior art DIRECT pour TROU 2 : pattern canonique forge déjà validé pour résoudre une double/triple-source vault↔consommateurs. Workbench doit l'appliquer, pas le contourner.
- `[[pre-compute-vs-inference-loops-boris]]` — fondement doctrinal : le loop de Boris a un checkpoint vérifiable + gate humain ; le loop /spec n'en a aucun. C'est l'argument de fond du TROU 1.
- `[[multi-agent-handoff-loss-pattern]]` — error amplification 17× sans validation au handoff : quantifie le risque du TROU 1.
- `project_neoteem_back_ts` (mémoire) — confirme "skill spec en 3 exemplaires synchronisés", la dette que la 4e copie aggraverait.
