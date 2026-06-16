---
titre: "Relais inter-agents fiable — mémoire de travail partagée"
resume: "Hub : les 3 fuites du multi-agent (perte verticale / redondance horizontale / coût de relecture) et leurs parades canoniques. Pointe vers les foyers existants, ne les re-rédige pas. Le registre léger est déployé sur neo_ia + neoteem-back-ts, à observer avant promotion canonique. Inclut la méthode de déploiement sur un nouveau repo."
aliases:
  - "relais inter-agents"
  - "relais inter-agents fiable"
  - "mémoire de travail partagée agents"
  - "transmettre contexte entre agents"
  - "anti-doublon recherche multi-agent"
  - "coordination agents tokens"
  - "déployer relais feature nouveau repo"
type: technique
derniere-maj: 2026-06-16
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/agents"
  - "#domaine/orchestration"
---

# Relais inter-agents fiable

Quand plusieurs agents collaborent sur une tâche (orchestrateur → architecte →
dev → testeur, ou tout fan-out), trois fuites surviennent parce que les
sous-agents sont isolés et sans état partagé : **(1) perte verticale** (le
« pourquoi » d'une décision ne remonte pas, seul un résumé passe), **(2)
redondance horizontale** (un agent refait une recherche déjà faite), **(3)
coût de relecture** (un agent relit du code faute de savoir lequel compte).
Ce hub renvoie aux parades — il ne les recopie pas (single-source).

## Les parades, par fuite

- **Perte verticale** → [[multi-agent-handoff-loss-pattern]] : compte les
  *handoffs* sur le chemin critique, pas les agents ; orchestrateur central
  (valide avant de relayer) plutôt que swarm.
- **Redondance horizontale + coût de relecture** → [[pattern-mcp-brief-then-direct]] :
  la session principale extrait le contexte et le **transmet** dans le brief ;
  l'agent ne re-cherche qu'en filet ; elle **propage** le contexte de l'agent N
  vers N+1.
- **Artefacts-relais + contrats de format + gates** → [[software-factory-pattern-2026]]
  (story/spec/brief = artefacts ; validator read-only + checkpoints humains =
  gates) + [[workflow-claude-code-optimal]]. Dans forge, l'artefact-relais réel
  est le dossier `TODO/feature-X/` produit par la skill `/spec` (SPEC.md + BRIEFs).
- **Registre léger** (savoir ce qui a déjà été fait, avant une op coûteuse) →
  **déployé sur neo_ia + neoteem-back-ts** (section « Déjà fait » du format
  `notes`, fichier-relais `.tmpclaude/feature-notes/`, 2026-06-16) — **à observer
  en usage réel avant promotion canonique** (déployé ≠ validé) :
  `feedback_registre-relais-agents`.

## Relais intra-/feature (déploiement 2026-06-16)

Sur neo_ia + neoteem-back-ts, le relais d'une `/feature` est un **fichier unique
sectionné** (`.tmpclaude/feature-notes/<slug>.md`, gitignoré, éphémère, skill
`/notes`) à 6 sections : Objectif / Déjà fait / Décisions / Déviations / État / Next.
**La SESSION le persiste** par défaut (les agents read-only ne l'écrivent jamais) ;
un agent déjà-writer (dev, test-writer) peut écrire sa propre section au fil de
l'eau (ceinture anti-coupure). Lecture **ciblée par section**, jamais le fichier
entier. **Frontière cross-repo** : le relais ne traverse jamais un repo (gitignoré) —
le véhicule cross-repo reste le ticket Jira autosuffisant. Au `/ship`, migration
**sélective** du durable (décisions archi + déviations → `doc(s)/adr/` ; gotchas →
`memory/`) puis suppression.

### Le maillon read-only : contrat de sortie de l'architect

Un agent **read-only** (architect, reviewer) ne compte QUE sur ce qu'il RETOURNE —
pas de ceinture anti-coupure (contrairement au dev déjà-writer qui s'auto-sauvegarde,
cf le cas N2-111283 de [[anti-reentrance-sub-agents-pattern-escalade]]). La fuite
observée (3 récurrences back-ts) : l'architect rend son plan dans un message
**intermédiaire** puis termine par « plan ci-dessus » → seul le dernier message
revient à la session, le plan complet est perdu, et **le dev re-décide**.

Parade en 2 volets, **sans jamais ouvrir Write** (ce serait perdre la frontière
d'outils = le modèle de sécurité, pour zéro gain : la richesse vient du contrat de
sortie, pas des permissions) :
1. **Côté agent** — exiger « TON DERNIER MESSAGE EST LE LIVRABLE » : ré-émettre le
   plan COMPLET dans le message final, jamais « voir ci-dessus ».
2. **Côté dispatch** — le prompt `/feature` injecte les sections relais ciblées
   (Objectif + Déjà fait, par section) ET exige le retour complet ; **la session
   persiste** le plan dans § Décisions (l'agent reste read-only).

Déployé sur architect-deep (neo_ia) + architect (back-ts), 2026-06-16. Les sections
« alternatives écartées » et « pièges » du contrat de sortie sont **en réserve** —
à n'ajouter que si l'observation prouve un re-travail réel (muscler sur fuite
observée, pas peur théorique).

## Déployer le relais /feature sur un NOUVEAU repo — méthode

Recette éprouvée sur le couple neo_ia / neoteem-back-ts (2026-06-16). **Adapter,
jamais copier** — chaque repo a sa structure.

1. **Lire le ou les formats RÉELS d'implementation-notes du repo cible AVANT de
   trancher l'unique** : un repo peut avoir 2 formats divergents (skill `notes` +
   rule), ou un seul. Lire chacun EN ENTIER, choisir la base, absorber les apports
   de l'autre, réduire le perdant en stub-pointeur. Le format cible = 6 sections
   (Objectif / Déjà fait / Décisions / Déviations / État / Next).
2. **Vérifier l'état git réel** : `git ls-files "*implementation-notes*"` (ces
   fichiers sont-ils committés comme **livrables durables** ? → ne PAS les détracker)
   et le `.gitignore` (`.tmpclaude/` est-il déjà couvert ? sinon l'ajouter). Le
   relais éphémère va dans `.tmpclaude/feature-notes/` pour ne PAS entrer en
   collision avec un dossier `docs/implementation-notes/` de livrables durables.
3. **Grep REPO-WIDE (pas seulement `.claude/`)** tous les pointeurs vers l'ancien
   chemin, les migrer, puis re-grep pour prouver 0 résiduel. Trier chaque hit :
   pointeur-relais (à migrer) vs livrable durable réel qui cite un fichier existant
   (à laisser). Cf [[feedback_verify_exhaustive_claims]] (le scope du grep est une
   déclaration exhaustive).
4. **Adapter à la stack du repo, pas copier l'autre** : `docs/` vs `doc/`,
   `dev-*` multiples (neo_ia) vs `dev` singulier (back-ts), `## Next` vs
   `## Prochaine étape`, `doc/adr/` singulier. Lire les libellés réels avant de
   matcher.
5. **Read-only préservé** : 0 frontmatter d'agent touché. La session persiste, les
   agents lisent. Si une fuite read-only existe (architect) → contrat de sortie
   (ci-dessus), jamais Write.
6. **Cleanup éphémère vs trace** : le relais est gitignoré et jeté au `/ship` ;
   seules les décisions d'archi durables migrent (sélectivement) vers `doc(s)/adr/`
   + `memory/`. Ne pas déverser chaque note dans l'ADR.

## Quand appliquer — vs sur-engineering

- Appliquer le relais explicite quand : tâche **séquentielle** à ≥ 3 relais, ou
  plusieurs agents sur des sous-tâches **connexes** (gain × N).
- Sur-engineering quand : fan-out **parallèle** (aucun handoff sur le chemin
  critique — c'est déjà optimal), ou tâche one-shot courte. **La coordination
  ne doit jamais coûter plus que ce qu'elle économise.**

## Liens

- [[technique-shared-agent-memory]] — mémoire persistante (CLAUDE.md / `memory:` agent / Cowork)
- [[anti-reentrance-sub-agents-pattern-escalade]] — escalade vers la session principale + contrat de sortie sub-agent
- [[pattern-spec-skill-deployment]] — méthode sœur : déployer la skill `/spec` sur un nouveau repo
- [[3-axes-strategiques-forge]] — discipline tokens
