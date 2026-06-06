---
feature: loop-alignement-vault-skills
date_spec: 2026-06-05
type: loop-hors-code
statut: draft
---

# SPEC loop — Alignement vault ↔ skills-ref & agents

> Généré par /loop-forge. Conception uniquement — la création des composants est une étape séparée.

## 0. Contexte

**Orga / domaine :** claude-forge (Raphael) — maintenance de la cohérence doctrinale du setup Claude Code.
**Objectif business :** garantir que les skills de référence (`cc-*-ref`) et les agents reflètent la doctrine du vault forge-brain. Un écart silencieux = un composant qui enseigne une doctrine périmée ou incomplète. Cas déclencheur : `/goal` et Agent View documentés au vault mais absents de `cc-features-ref` (trouvé à la main le 5 juin 2026).
**Branche :** hors-code (veille / comparaison sémantique de docs, pas de fonction métier).
**Environnement :** repo claude-forge uniquement (vault + `.claude/`).

---

## 1. Job

**Description reformulée :** "Depuis le vault forge-brain et les composants `.claude/` (skills-ref + agents), comparer la doctrine de chaque côté, jusqu'à produire un rapport des NOUVEAUX écarts d'alignement."

- **Fréquence actuelle (manuelle) :** quasi jamais — détecté par hasard au fil des sessions (d'où le trou /goal resté longtemps).
- **Coût/temps actuel :** ~0 (non fait systématiquement) ; quand fait à la main, ~20-30 min de grep + lecture croisée.
- **ROI attendu de l'automatisation :** évite le drift doctrinal silencieux ; rattrape automatiquement ce qu'un cc-news ou un ajout vault oublie de propager.

---

## 2. Type de loop

**Type retenu :** time-loop (`/loop`)

- **Justification :** le désalignement naît lentement (à chaque ajout vault ou modif skill). Un scan hebdomadaire suffit à rattraper les écarts sans surveiller en continu. Ni inner-loop (dépend de la discipline, c'est ce qui a créé le trou), ni goal-loop (l'alignement n'est pas un état final atteignable une fois — de nouveaux écarts apparaissent en permanence).
- **Critère de terminaison nominal (succès) :** un cycle = rapport d'écarts produit (même vide) + état mis à jour.
- **Critère de terminaison exceptionnel :** cap N cycles atteint, OU fichier stop présent, OU erreur fatale (vault MCP injoignable).

---

## 3. Périmètre

- **Repo d'écriture (unique) :** claude-forge (le rapport + le fichier d'état y sont écrits).
- **Repos en lecture croisée :** aucun (mono-repo).
- **Pattern multi-repo si applicable :** N/A.

### Acteurs / Canaux _(hors-code)_

| Rôle | Qui | Canal de travail | Canal de notif |
|------|-----|-----------------|----------------|
| Scanner | loop (session Claude) | vault MCP forge-brain + Read `.claude/` | rapport fichier |
| Décideur | Raphael | relecture du rapport hebdo | — |

- **Sync ou async :** async (le loop tourne, Raphael lit quand il veut).
- **Contrainte fuseau :** aucune.

### Artefacts / Livrables _(hors-code)_

- **Input de chaque itération :** le vault forge-brain (notes canoniques, changelog, features) + les 6 skills-ref (`cc-features-ref`, `cc-skills-ref`, `cc-hooks-ref`, `cc-agents-ref`, `cc-prompt-ref`, `cc-cowork-ref`) + les agents `.claude/agents/`.
- **Livrable attendu :** rapport d'écarts `TODO/alignment-report-<date>.md` listant, dans les DEUX sens : (a) doctrine/feature au vault absente d'un composant qui devrait la refléter ; (b) affirmation d'un composant absente ou contredite par le vault. Chaque écart inclut une commande de dispatch suggérée (ex: "déléguer à skill-creator : ajouter X à cc-features-ref").
- **Template du livrable :** liste structurée { composant cible · type d'écart (descendant/montant) · note vault concernée · action suggérée }.
- **Stockage :** `TODO/` + état dans `.claude/_alignment-state.json`.
- **Durée de conservation :** rapports 30j ; état persistant indéfini.

### Validation qualité _(hors-code)_

- **Critère de qualité :** voir Bloc 5 (couverture + reproductibilité + 0 faux positif échantillon).
- **Reviewer :** Raphael (relit le rapport, déclenche ou non les dispatches).
- **Seuil d'acceptation :** rapport actionnable, écarts réels.
- **Feedback loop si insuffisant :** faux positifs récurrents → affiner le critère de comparaison (évolution V2 : 2e agent validateur).

---

## 4. Les 4 briques

| Brique | Description |
|--------|-------------|
| **Déclencheur** | cron hebdomadaire via `/loop` natif Claude Code sur la machine locale (ex: 1×/semaine). |
| **Source(s)** | vault forge-brain (MCP `search_brain`/`read_note`) + `.claude/skills/cc-*-ref/SKILL.md` + `.claude/agents/*.md` (Read/Grep). |
| **Critère de jugement** | un écart est réel si une doctrine/feature présente d'un côté est absente ou contredite de l'autre, ET n'est pas déjà dans le journal des écarts traités/ignorés. |
| **Action** | écrire le rapport des NOUVEAUX écarts + la commande de dispatch suggérée pour chacun. JAMAIS modifier skill/agent directement (passe par skill-creator/agent-creator après validation Raphael). |

### Idempotence & état _(code ET hors-code)_

- **Si même item traité 2× :** journal `.claude/_alignment-state.json` listant les écarts déjà corrigés OU marqués "ignoré volontairement" (clé = hash composant+note+type). Le rapport hebdo ne montre que les écarts absents du journal → pas de re-signalement, pas de fatigue de lecture.
- **Si interruption mid-batch :** le scan est relançable de zéro (lecture seule, pas d'effet de bord) ; l'état n'est mis à jour qu'en fin de cycle complet, après écriture du rapport. Une interruption = simple re-scan au cycle suivant.

---

## 5. Vérification

**Méthode retenue :** combinaison couverture + reproductibilité + échantillon (signal PASS/FAIL composite).

- **PASS si les 3 vrais ensemble :**
  1. **Couverture** : le scan a traité 100% des composants listés (count attendu vs count scanné — vérifiable mécaniquement).
  2. **Reproductibilité** : 2 passes du scan sur le même état renvoient le MÊME set d'écarts (détecte les hallucinations instables du jugement sémantique LLM).
  3. **0 faux positif sur échantillon** : sur les N écarts signalés, un échantillon relu confirme qu'ils sont réels (pas inventés).
- **Justification du combo** : la comparaison vault↔composant est un jugement sémantique flou ; (2) attrape l'instabilité LLM, (1)+(3) attrapent l'incomplétude et l'invention. Aucune des trois seule ne suffit.
- **Évolution V2 (si faux positifs persistent)** : 2e agent validateur vote réel/faux sur chaque écart.

---

## 6. Infra

**Option retenue :** machine locale — `/loop` natif Claude Code lancé directement par Raphael sur sa machine.

- **Détails :** Windows, `/loop` hebdo (intervalle ex: `7d` ou self-paced). Org bloque le cloud → local obligatoire de toute façon.
- **Incompatibilités signalées :** un time-loop sur machine locale ne tourne pas quand la machine dort. **Acceptable ici** : le scan est non-urgent et idempotent — s'il rate une semaine, il rattrape au prochain réveil sans rien perdre (état persistant). Pas de risque de double-traitement.

---

## 7. Garde-fous (obligatoires)

| Garde-fou | Décision |
|-----------|----------|
| Validation humaine | par exception — Raphael relit le rapport hebdo et déclenche les dispatches. Aucune modif de composant sans sa validation (delegate-guard l'impose déjà structurellement). |
| Cap coût / itération | cap N cycles (le `/loop` s'arrête après N semaines sauf relance explicite) + scan borné aux composants listés (pas d'exploration ouverte). |
| Log / trace | chaque cycle écrit `TODO/alignment-report-<date>.md` (trace du run) + met à jour `.claude/_alignment-state.json`. Notification : le rapport lui-même (pas de canal externe, local). |
| Kill-switch | fichier flag `.claude/.alignment-loop.stop` — si présent, le loop s'arrête immédiatement au cycle suivant. + arrêt manuel `/loop` natif. |

---

## 8. Composants à créer (HORS SCOPE de /loop-forge)

> Créer ces composants depuis la session principale après validation de cette spec.

| Composant | Type | Description |
|-----------|------|-------------|
| `align-vault-skills` | skill | Le job lui-même : scan vault ↔ skills-ref+agents, compare dans les 2 sens, écrit le rapport + commandes de dispatch suggérées, met à jour l'état. Lancée en `/loop` hebdo. |
| `.claude/_alignment-state.json` | fichier d'état | Journal des écarts traités/ignorés (idempotence). Créé/maintenu par la skill, pas un composant à coder séparément. |
| (pas de hook kill-switch dédié) | — | Le kill-switch = simple fichier flag testé en tête de skill ; pas besoin d'un hook. |

---

## 9. Critères de done

- [ ] Le `/loop` hebdo se déclenche et produit un rapport (même vide).
- [ ] La vérification PASS/FAIL est opérationnelle (couverture + 2 passes identiques + échantillon).
- [ ] Chaque cycle produit `alignment-report-<date>.md` + met à jour `_alignment-state.json`.
- [ ] Les 4 garde-fous opérationnels (validation par exception, cap cycles, rapport-trace, fichier stop).
- [ ] Un premier run complet validé par Raphael (les écarts signalés sont réels, le /goal+AgentView corrigé n'est PAS re-signalé).

---

## Notes / À confirmer

- **Intervalle exact du `/loop`** : hebdomadaire proposé ; à ajuster (bi-mensuel possible si peu de churn).
- **Portée "agents"** : confirmer si on scanne le frontmatter agents (modèle/effort vs doctrine) ou seulement les références doctrinales dans le body. Proposé : body + wikilinks cités.
- **Sens "montant" (composant→vault)** : un écart montant peut être légitime (skill plus récente que le vault) → le rapport doit le marquer "à arbitrer" plutôt que "à corriger".
- **Comparaison sémantique** : le cœur du job est un jugement LLM (note vault ≈ section skill ?). Le critère de reproductibilité (Bloc 5.2) est la garde principale contre l'instabilité.
