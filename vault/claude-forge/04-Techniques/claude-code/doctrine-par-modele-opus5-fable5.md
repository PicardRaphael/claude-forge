---
titre: "Doctrine par modèle — Opus 5 vs Fable 5 : ce qui change dans les prompts, skills et agents"
resume: "Les règles de prompting Anthropic diffèrent PAR MODÈLE et non par génération : Opus 5 s'auto-vérifie (retirer le scaffolding de vérification) tandis que Fable 5 exige une vérification explicite sur les runs longs, délègue massivement, refuse les instructions show-your-reasoning (reasoning_extraction) et dégrade sur les skills trop prescriptives. Grille de décision + checklist de migration."
aliases:
  - doctrine par modele
  - Opus 5 vs Fable 5
  - prompting par modele Claude 5
  - reasoning_extraction refusal
  - skills too prescriptive Fable
  - agent en Fable que faire
  - verification par modele
derniere-maj: 2026-07-29
auteur: claude
type: technique
sources:
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5"
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5"
  - "https://platform.claude.com/docs/en/build-with-claude/effort"
  - "https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices"
  - "https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/agents"
  - "#statut/canonique"
  - "#doctrine/2026"
---
# Doctrine par modèle — Opus 5 vs Fable 5

> **Le principe à retenir** : Anthropic ne publie plus une doctrine unique de prompting. Les règles dépendent du **comportement par défaut mesuré de chaque modèle**. Une instruction utile sur un modèle est du gaspillage — ou un refus — sur un autre.
>
> Vérifié en source primaire le 29 juil. 2026. Chaque page modèle se compare à **Opus 4.8** comme baseline, donc Opus 5 et Fable 5 sont **concurrents**, pas successifs : la divergence est un réglage voulu, pas un décalage de version.

## Pourquoi cette note existe

Deux erreurs de lecture ont failli être promulguées dans forge le 29 juil. 2026 :

1. **Généraliser un claim modèle-spécifique.** « Skills developed for prior models are often too prescriptive » a été lu comme valant pour tous les Claude 5 → **faux**, la page est cadrée « specific to Claude Fable 5 and Claude Mythos 5 ».
2. **Lire un exemple de prompt comme une assertion.** « do not use subagents to verify or double-check your own work » se trouve **dans un bloc d'exemple** que l'on est invité à donner au modèle, en section contrôle des coûts — pas une position doctrinale d'Anthropic. La même page endosse d'ailleurs les patterns writer-verifier.

D'où la règle de méthode : **un verbatim se lit dans sa section, et avec son périmètre de modèle.**

## Tableau de décision — que faire selon le modèle de l'agent

| Sujet | Opus 5 | Fable 5 / Mythos 5 |
|---|---|---|
| **Effort de départ** | `high` (défaut). `xhigh` = step-up mesuré. `low`/`medium` = « primary control » du coût | `high` par défaut ; `low`/`medium` « often exceed `xhigh` performance on prior models » |
| **Vérification** | **Retirer** le scaffolding : « verifies its own work without being told to » | **Rendre explicite** sur les runs longs : « Separate, fresh-context verifier subagents tend to outperform self-critique » |
| **Auto-correction** | Ne pas instruire de re-checks : « Avoid instructing re-checks it already performs » | — |
| **Délégation** | Cadrer, plafonner : « delegates to subagents more readily… it multiplies cost » | **Encourager** : « Use subagents frequently », async > blocking, sous-agents longue durée (gain de cache) |
| **Skills prescriptives** | Aucun claim — les skills forge restent valides | **« too prescriptive … can degrade output quality »** → re-tester contre le défaut |
| **Montrer son raisonnement** | Toléré | ⛔ **Risque de REFUS** (`reasoning_extraction`) → fallback vers Opus 4.8 |
| **Verbosité** | Réponses plus longues par défaut → prompter la concision explicitement (l'effort ne raccourcit pas le texte visible) | Idem, brièveté pilotable par instruction courte |
| **Scope** | Peut élargir la tâche → contraindre explicitement | Peut agir sans qu'on demande (branches de backup, brouillons) → poser les limites |
| **Thinking** | Non désactivable à `xhigh`/`max` (erreur **400**) | Adaptive uniquement, thinking résumé |

## Le piège majeur sur Fable 5 — `reasoning_extraction`

Verbatim ([prompting-claude-fable-5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5), § *Recommended scaffolding changes*) :

> « **Don't instruct Claude to reproduce its reasoning in the response.** Prompts, skills, or harness instructions that tell the model to echo, transcribe, or explain its internal reasoning as response text can trigger the `reasoning_extraction` refusal category on Claude Fable 5, causing elevated fallbacks to Claude Opus 4.8. Audit existing skills and system prompts for reflection or show-your-thinking instructions when migrating. »

**Ce n'est pas une dégradation de qualité, c'est un refus** (`stop_reason: "refusal"`) et un fallback silencieux. Tout composant qui demande « explique ton raisonnement », « montre ta chaîne de décision », « transcris ta réflexion » est concerné.

Alternative officielle : lire les blocs `thinking` structurés de l'adaptive thinking, et utiliser un outil *send-to-user* pour la progression.

Fable 5 fait aussi tourner des **classifieurs de sécurité** (cybersécu offensive, biologie/sciences du vivant) qui peuvent refuser même du travail bénin — prévoir un fallback vers Opus 4.8.

## Checklist — « je veux passer un agent en Fable 5 »

À dérouler **avant** de changer `model:` dans un frontmatter :

1. **Grep le body de l'agent** pour toute instruction de type show-your-reasoning (« explique ton raisonnement », « détaille ta réflexion », « montre comment tu as conclu »). Présent → réécrire ou ne pas migrer. C'est le point bloquant n°1.
2. **Vérifier les skills chargées** par cet agent : trop prescriptives (longues checklists comportementales, énumération de cas) → tester le défaut d'abord, retirer ce qui n'améliore rien.
3. **Retirer** les instructions de délégation restrictive : Fable 5 veut déléguer beaucoup, en asynchrone.
4. **Ajouter** une vérification explicite si le run est long : « Establish a method for checking your own work at an interval of [X]… verifying your work with subagents against the specification. »
5. **Ajouter** l'ancrage anti-fabrication sur les runs longs : « Before reporting progress, audit each claim against a tool result from this session. »
6. **Prévoir le fallback** Opus 4.8 (refus classifieurs) — côté serveur ou client.
7. **Timeouts** : les tours Fable 5 durent des minutes, les runs autonomes des heures. Adapter les attentes, préférer le check asynchrone au blocage.

## Ce qui NE dépend pas du modèle (confirmé inchangé)

La page canonique [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) **n'a pas été révisée** dans le sens de Fable 5 :

- **Plafond 500 lignes** pour un `SKILL.md`, découper au-delà.
- **Progressive disclosure** + `references/`.
- ⚠️ **Les exemples restent recommandés** : « Examples convey the desired style and level of detail to Claude more clearly than descriptions alone. » — ceci **contredit** la lecture « les exemples contraignent l'exploration » qu'on peut tirer du billet context-engineering du 24 juil. Ne pas supprimer les exemples des skills par principe.
- Les contraintes ne sont pas à supprimer mais à **calibrer** : « Match the level of specificity to the task's fragility and variability » (pont étroit = garde-fous exacts ; champ ouvert = direction générale).
- **Références à 1 niveau de profondeur max** — au-delà, « Claude might use commands like `head -100` to preview content… resulting in incomplete information ».
- **Table des matières obligatoire** dans un fichier de référence > 100 lignes.
- Coût récurrent souvent ignoré : « Once a skill loads, its content stays in context across turns, so **every line is a recurring token cost**. » Budget de listing = **1 %** de la fenêtre de contexte ; en débordement, Claude Code **drop les descriptions** des skills les moins invoquées.

## Frontière à ne pas confondre — vérifier son travail ≠ vérifier un tiers

Le claim Opus 5 (« retirer les instructions de vérification ») vise la **relecture redondante de son propre travail fraîchement produit**. Il ne vise **pas** le contrôle de l'affirmation d'un tiers qui peut échouer silencieusement.

| Objet vérifié | Statut |
|---|---|
| Mon output, relu sans information neuve | **Redondant sur Opus 5** → retirer |
| Le rapport d'un sous-agent (`exit 0` sur Write refusé, faux positifs d'audit) | **À garder** — mode d'échec différent |
| Une source web volatile avant capitalisation | **À garder** |
| L'input que je vais juger (lire la note en entier avant de trancher) | **À garder** — c'est de la complétude d'entrée, pas de la re-vérification |

Motif officiel du claim : **redondance et coût**, pas biais — « removing them reduces wasted tokens **with no loss in quality** ».

Le `self-preferential bias` (post [harness](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code), 2 juin) est un phénomène distinct, lié à la **longueur d'un même contexte** : « Claude's tendency to prefer its own results or findings, especially when asked to verify or judge them against a rubric. » Remède officiel = contextes séparés. Il justifie les vérificateurs indépendants ; il ne contredit pas le claim Opus 5.

## Convergence forge — antérieure à Anthropic

`memory/feedback_stop_over_verifying.md` (13 mai 2026) énonçait déjà la règle de périmètre exacte : travail de **cette** session → verdict direct ; travail d'une session **antérieure** → relecture justifiée. Anthropic publie la même position deux mois plus tard. Neuf composants forge portent déjà l'interdit « ❌ Re-vérifier ce que le brief dit clairement ».

## Liens

- [[effort-opus-47-doctrine-anthropic-2026]] — grille effort par modèle (source de vérité sur `effort:`)
- [[comment-creer-agent]] · [[comment-creer-skill]] · [[comment-ecrire-claudemd]]
- [[Opus 5]] · [[workflow-claude-code-optimal]]
- [[verification-sources-canoniques]] — lire un verbatim dans sa section
