---
titre: "Critique — Plan modernisation .claude/ repo bdd (PostgreSQL Loji)"
type: knowledge
domaine: claude-code
derniere-maj: 2026-07-13
auteur: claude
tags:
  - "#type/critique"
  - "#domaine/claude-code"
  - "#domaine/skills"
---
# Devils Advocate — Plan de modernisation `.claude/` repo bdd

**Intention déclarée :** moderniser la config `.claude/` d'un repo d'équipe PostgreSQL (compresser descriptions skills, migrer @rôles vers natif, convertir 12 commands en skills, fusionner méthode dev dans CLAUDE.md) sans casser les workflows quotidiens de l'équipe.

---

## Verdict

**Bloquants :** 0 | **Avertissements :** 4 | **Nitpicks :** 2

**Décision recommandée :** SHIP WITH FIXES

Le plan est doctrinalement propre (repo équipe = portabilité, pas de hooks bloquants, valeur convertie avant suppression, gouvernance chez Bastien). Aucun bloquant : les gates de validation incrémentale (L49) désamorcent le risque le plus grave en le transformant en dette mesurable plutôt qu'en casse. Mais quatre tensions non résolues doivent être adressées AVANT d'attaquer les phases 2-4.

---

## Si je devais le faire marcher malgré mes objections

1. **Mesurer le budget AVANT Phase 4, pas après.** La checklist skill-creator dit « 10+ skills → vérifier budget avec `/doctor` ». Le repo est à 20 skills, cible ~30-34 post-conversion. Lancer `/doctor` sur la branche AVANT de convertir la moindre command, noter le headroom réel, et ajouter au plan une projection de compte de skills post-Phase-4. Si le budget est déjà tendu à 20, Phase 4 devient conditionnelle.
2. **Trancher la question « pourquoi convertir » avant Phase 4.** Pour les 8 commands sans side-effect (/verif /optim /refacto /clean /investigate + /ticket /testunit), décider explicitement : model-invocable (bénéfice auto-trigger, coût budget) OU slash-only `disable-model-invocation: true` (préserve le budget, mais alors la skill est fonctionnellement quasi-identique à la command d'origine → la conversion perd sa justification). Ne pas laisser ce choix implicite.
3. **Recompter la cible CLAUDE.md** après avoir lu dev.md : ~150L est probablement faux. Poser une fourchette honnête (~180-200L) ou justifier les coupes supplémentaires.
4. **Définir un critère de validation exécutable pour /ticket** (les 6 phases + 2 checkpoints humains déclenchent-ils de façon fiable en skill ?), pas « on testera en session réelle ».
5. **Cadrer Phase 3 comme fix du bug (collision namespace), pas comme démolition de l'architecture-rôles de Bastien** — proposer d'abord le fix minimal, laisser Bastien arbitrer la conversion en skills.

---

## Angle Technique — Qu'est-ce qui se casse ?

**AVERTISSEMENT (score 72) — Contradiction budget interne Phase 2 ↔ Phase 3+4.** Le plan désigne le drop silencieux des descriptions à ~20 skills comme « risque principal » (L17) et y répond par Phase 2 (compression pour sortir de la zone). Puis Phase 3 (docu + brainstorm) et Phase 4 (12 commands) **ajoutent ~10-14 skills model-invocables** — seules 4 des 12 commands sont flaggées `disable-model-invocation` (L45), et ce flag y est mis pour la bonne raison (side-effects), pas pour le budget. Le listing droppe par ranking **récence + fréquence** = piloté par le NOMBRE de skills, pas seulement la longueur des descriptions. Les command-skills fraîchement ajoutées et très utilisées rankeraient haut et pousseraient les skills métier rares (taxe-fonciere hors saison) HORS du listing — exactement le silent-fail que Phase 2 devait empêcher. Le plan ne fournit **aucune projection de budget post-Phase-4**. Pas bloquant car les gates incrémentaux (L49) permettent de mesurer et reculer, mais le trou d'analyse est réel.

**AVERTISSEMENT (score 68) — /ticket : régression de sémantique d'exécution.** Une slash command = prompt injecté (début de tour, déterministe). Une skill = chargée quand triggée, le modèle DOIT choisir de la suivre et peut sauter des étapes. /ticket est l'orchestrateur 6 phases avec 2 checkpoints humains — l'outil le plus riche de l'équipe. Le convertir en skill (surtout si model-invocable) risque des phases sautées ou des checkpoints contournés. Le plan dit seulement « tester en session réelle avant de supprimer » (L48) : trop mince pour ce joyau. Il faut un critère de validation explicite et reproductible.

**NITPICK (score 30) — Cible CLAUDE.md ~150L arithmétiquement douteuse.** 248L − 17 (Custom Agents) − ~40 (compression index) = ~191L, PUIS on intègre la méthode dev (conventions + 5 étapes + validation, non triviale). La liste des « à garder » (L52) est longue. Atteindre 150L exigerait ~40L de coupes non identifiées EN PLUS de l'ajout dev. Cible probablement fausse de 40-50L. Non fonctionnel, mais un chiffre faux dans un plan érode la confiance dans les autres chiffres.

**Objections :**
- BLOQUANT : aucun
- AVERTISSEMENT : contradiction budget Phase 2 ↔ 3+4 sans projection ; /ticket perte de déterminisme d'exécution
- NITPICK : cible CLAUDE.md 150L sous-estimée

---

## Angle Stratégique — Est-ce le bon problème ?

**AVERTISSEMENT (score 66) — La conversion commands→skills perd des deux côtés.** Le vrai coût-bénéfice n'est pas posé. Deux cas :
- Command → skill **model-invocable** : gagne l'auto-trigger, mais consomme le budget listing (cf tension Phase 2) et fait perdre le déterminisme d'exécution (cf /ticket).
- Command → skill **slash-only** (`disable-model-invocation`) : préserve le budget et le déterminisme, MAIS une skill slash-only est fonctionnellement quasi-identique à la command d'origine (déclenchée par l'utilisateur, hors listing model-facing). Dans ce cas **la conversion n'apporte quasi rien** — on refait 12 outils qui marchent pour un gain marginal.
Le plan justifie la conversion par « valeur préservée » (L44) mais ne montre jamais quel PROBLÈME RÉEL de l'équipe elle résout. Convertir 12 outils utilisés et fonctionnels = surface de régression pour un bénéfice non démontré. Phase 4 mérite un « pourquoi » explicite ou un report sine die.

**AVERTISSEMENT (score 58) — Phase 3 démolit l'architecture qui EST la raison d'être de la branche de Bastien.** Le chantier « claude commun » (branche N2-111820) construit la convention @dev/@docu/@brainstorm. Le plan propose de la supprimer (agents/dev.md, section Custom Agents, README). Le vrai problème à résoudre est la **collision namespace** (typeahead @, auto-délégation, AskUserQuestion qui casse en subagent) — un bug technique précis. Or le fix du bug n'exige pas forcément de convertir les rôles en skills. Et attention : le typeahead @dev que l'équipe a « dans les doigts » DÉPEND de l'enregistrement subagent — sortir de agents/ casse cette muscle memory. Le plan asserte le bénéfice (« plus de collision ») sans mapper le coût sur l'usage quotidien (@dev devient quoi ? @docu ?) ni signaler la perte silencieuse du `model: opus` quand dev→CLAUDE.md et docu→skill. Proposer d'abord le fix minimal du bug, laisser Bastien arbitrer la refonte.

**Objections :**
- BLOQUANT : aucun
- AVERTISSEMENT : conversion commands→skills perd des deux côtés (bénéfice non démontré) ; Phase 3 démolit l'archi-rôles sans mapper le coût muscle-memory + perte model:opus
- NITPICK : aucun

---

## Angle Pratique — Combien de temps avant l'abandon ?

**NITPICK (score 40) — Risque budget asserté, jamais mesuré sur CE repo.** Le « risque principal » (L17) dit que les skills rares « PEUVENT devenir invisibles » — conditionnel. Personne n'a observé le drop à 20 skills sur bdd. Phase 2 (compresser 20 descriptions) pourrait être une optimisation prématurée si le budget n'est pas réellement tendu. Fix trivial : `/doctor` d'abord, décision ensuite. Sans mesure, on risque un chantier de compression qui ne sert à rien, abandonné à mi-course.

**Ordre des phases (réponse au brief Q6) :** moderniser creation-skill AVANT de compresser les descriptions (Phase 1 avant Phase 2) est le BON ordre — dogfooding, la fabrique produit le format cible. Ne pas inverser. En revanche, insérer une mesure `/doctor` en Phase 0 (avant tout) pour ancrer Phase 2 et Phase 4 sur du réel.

**Gouvernance (réponse au brief Q5) :** le plan respecte correctement le fait que c'est le chantier de Bastien (tout passe par sa branche, protection trigramme, proposition pas application). Bon point. Risque résiduel : si l'équipe travaille en parallèle sur la branche, une refonte Phase 3 des rôles peut entrer en conflit avec le travail en vol de Bastien — coordonner explicitement avant Phase 3.

**Objections :**
- BLOQUANT : aucun
- AVERTISSEMENT : aucun
- NITPICK : risque budget non mesuré empiriquement (fix : /doctor en Phase 0)

---

## Vault — Historique pertinent

- [[skills-metadata-tokens-load]] + [[comment-creer-skill]] (AJOUT 18 juin 2026) confirment le mécanisme du budget listing CC 2.1.129+ : `skillListingBudgetFraction` (1 % défaut), drop de descriptions ENTIÈRES ranké par récence+fréquence à ~15-25 skills à 200K. Aucune source vault n'établit que `disable-model-invocation` sort une skill du budget listing — le flag empêche l'auto-invocation, pas le chargement metadata. C'est ce qui rend la tension Phase 2↔4 réelle.
- [[config-repo-equipe-vs-forge]] : la doctrine « repo équipe = portabilité, hooks non-bloquants, pas de machinerie forge » est correctement appliquée dans la section « Ce qu'on NE fait PAS ».
- Pas d'antécédent direct trouvé sur une conversion commands→skills ratée dans le vault — la critique tient sur l'analyse.
