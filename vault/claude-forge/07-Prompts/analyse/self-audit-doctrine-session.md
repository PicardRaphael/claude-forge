---
titre: "Prompt — Self-audit doctrine session (post-mortem)"
resume: "Prompt à coller en session fraîche pour auditer si Claude a respecté la doctrine forge dans une session passée. 7 checks evidence-based, format PASS/FAIL/PARTIAL avec citation transcript/commits"
aliases:
  - "self-audit doctrine"
  - "self-audit session"
  - "audit jarvis post-mortem"
  - "verifier doctrine claude session"
  - "audit comportement claude"
  - "post-mortem doctrine forge"
derniere-maj: 2026-05-25
type: prompt
domaine: claude-code
sources:
  - "[[methode-analyser-repo]]"
  - "[[methode-pivoter-doctrine]]"
  - "[[amanda-askell-prompt-engineering]] (TDD prompts)"
  - ".claude/rules/sequence-canonique-modification.md"
  - ".claude/rules/comportement-proactif.md"
  - ".claude/rules/devils-advocate-pipeline.md"
tags:
  - "#type/prompt"
  - "#domaine/audit"
  - "#methode/verification"
---

# Prompt — Self-audit doctrine session (post-mortem)

## Quand l'utiliser

Après une session significative (10+ échanges substantifs, modifs vault/MCP/code), pour vérifier que Claude a respecté la doctrine forge. **Exécution OBLIGATOIRE en session fraîche `/clear`** sur le transcript/commits de la session auditée — sinon biais auto-justification.

## Variables à remplir

- `{SESSION_REF}` — référence de la session à auditer : `git log --since "YYYY-MM-DD HH:MM"` OU chemin transcript exporté OU "session actuelle (post-mortem mid-session)"
- `{SCOPE}` — `full` (7 checks) ou `quick` (3 checks bloquants : mémoire / canoniques / advisor)

## Prompt à coller

```
<role>
Tu es un évaluateur externe en session fraîche. Mindset DA strict : chercher où Claude a violé sa propre doctrine forge, pas justifier ce qui a marché. Tu n'as PAS de contexte conversationnel avec la session auditée — tu lis le transcript/commits comme un auditeur tiers.
</role>

<contexte>
Doctrine de référence (sources de vérité) :
- `.claude/rules/sequence-canonique-modification.md` — séquence A→B→C→D→E obligatoire
- `.claude/rules/comportement-proactif.md` — dispatch composants
- `.claude/rules/devils-advocate-pipeline.md` — DA conditionnel ciblé
- `.claude/rules/check-before-create.md` — mémoire + vault + refs AVANT modification
- `.claude/rules/memory-discipline.md` — relire feedbacks pertinents début tâche
- `vault/claude-forge/04-Techniques/claude-code/methode-analyser-repo.md` — étape 1b code RÉEL
- MEMORY.md racine memoire perso forge

Session auditée : {SESSION_REF}

Outils MCP forge-brain disponibles (v1.3) pour cross-check : search_brain, read_note, find_by_property, lint_vault.
</contexte>

<tache>
Pour chaque check ci-dessous : PASS / FAIL / PARTIAL / N/A + 1-2 lignes evidence (citation transcript ou commit hash ou outil non-appelé).

## Check 1 — Mémoire consultée AVANT action

**Question** : avant chaque modification substantielle (créer/modifier skill/agent/hook/CLAUDE.md/note vault), Claude a-t-il consulté les feedbacks mémoire pertinents ?

**Comment vérifier** :
- Grep transcript pour `Read.*memory/feedback_` ou MEMORY.md lu
- Si tâche `créer un X` → feedback `feedback_X*` ou `feedback_skill_structure` consulté ?
- Si erreur récurrente → feedback correspondant consulté avant de répéter ?

**FAIL si** : modification faite sans aucun read de mémoire pertinente identifiable.

## Check 2 — Canoniques vault lues EN ENTIER

**Question** : avant audit/modif d'un composant existant, Claude a-t-il fait `read_note` SANS max_lines sur les canoniques pertinentes, OU seulement `search_brain` (extraits ~10 lignes) ?

**Comment vérifier** :
- Grep transcript pour `mcp__forge-brain__read_note` (full read)
- Versus `mcp__forge-brain__search_brain` (extraits seulement)
- Notes attendues selon tâche : créer skill → `comment-creer-skill` ; créer agent → `comment-creer-agent` ; etc.

**FAIL si** : audit/création sans lecture intégrale d'au moins 1 canonique pertinente.

## Check 3 — Séquence A→B→C→D→E respectée (ordre)

**Question** : Claude a-t-il analysé le RÉEL (faits bruts) AVANT de lire les canoniques (biais perception), ou inversé ?

**Comment vérifier** :
- 1ers outils appelés dans la session = analyse code/repo (Glob, Read, git log) ?
- OU 1ers outils = lecture canoniques vault (biais doctrine d'abord) ?

**FAIL si** : canoniques lues avant analyse du réel.

## Check 4 — Advisor timing

**Question** : `advisor()` appelé AVANT travail substantiel (écrire, éditer, déclarer), ou APRÈS (justification a posteriori) ?

**Comment vérifier** :
- Position des appels `advisor` dans le transcript
- Si décision majeure prise SANS advisor → FAIL
- Si advisor APRÈS implémentation pour valider → PARTIAL

**N/A si** : tâche courte/triviale (< 10 échanges).

## Check 5 — DA conditionnel sur livrables majeurs

**Question** : DA appelé sur livrables majeurs (skill réutilisée, agent orchestrant, archi, refonte structurelle vault) ? Skippé sur trivial (bug fix, edit doc) ?

**Comment vérifier** :
- Lister les livrables de la session
- Pour chaque livrable : majeur ou trivial ? DA appelé ?
- Réf : `.claude/rules/devils-advocate-pipeline.md` tableau

**FAIL si** : livrable majeur shipped sans DA. **FAIL aussi si** : DA appelé sur tâche triviale (overhead).

## Check 6 — Single source of truth (pas de doublons)

**Question** : Claude a-t-il créé un nouveau feedback/note vault couvrant un sujet déjà existant ?

**Comment vérifier** :
- Lister les notes/feedbacks créés dans la session
- Pour chaque : `search_brain` ou grep mémoire pour vérifier qu'aucun fichier existant ne couvrait déjà
- Si doublon créé → FAIL

**FAIL si** : ≥ 1 doublon détecté.

## Check 7 — Tests adverses sur code rewriting/destructif

**Question** : tout code de la session qui réécrit/supprime/modifie en masse (move_note, mass-fix, refactor) a-t-il des tests cas adverses ?

**Comment vérifier** :
- Lister les changements code (commits)
- Pour chaque code rewriting : test happy path ET ≥ 1 test adverse (self-link, edge case, regex partial match) ?
- Référence : `feedback_da_dicte_tests_adverses`

**N/A si** : aucun code rewriting dans la session.

</tache>

<format_sortie>
Format obligatoire :

| Check | Status | Evidence (citation transcript/commit/outil non-appelé) |
|-------|--------|-------------------------------------------------------|
| 1. Mémoire AVANT action | PASS/FAIL/PARTIAL/N/A | ... |
| 2. Canoniques EN ENTIER | ... | ... |
| 3. Séquence A→B→C→D→E | ... | ... |
| 4. Advisor timing | ... | ... |
| 5. DA conditionnel | ... | ... |
| 6. Single source of truth | ... | ... |
| 7. Tests adverses destructif | ... | ... |

**Score** : N PASS / M FAIL / P PARTIAL sur 7 checks applicables.

**Si FAIL ≥ 2** :
- Identifier LE pattern dominant des fails (mémoire pas consultée OU canoniques pas lues OU ...)
- Proposer UN seul nouveau feedback memory à créer, format `feedback_<sujet>.md` avec : pattern observé, why (session ref), how to apply
- PAS 5 propositions. UN seul. Le plus récurrent.

**Si FAIL = 0** : "Session conforme. Pas de capitalisation nécessaire."

**Si N/A ≥ 4** : "Session trop courte/simple pour audit utile. Ignorer ce rapport."
</format_sortie>

<contraintes>
- Evidence-based UNIQUEMENT : pas de vibes, citation transcript/commit hash/outil non-appelé obligatoire
- Mindset DA strict : tu cherches ce qui CLOCHE, pas ce qui marche
- Pas de filler ("Great audit!", "Overall good session!") — verdict direct
- Pas de "You are a..." — déjà fait dans <role>
- 1 seule proposition de capitalisation max — le pattern dominant
- Si tu hésites entre 2 statuts → choisir le plus sévère (PARTIAL > PASS quand doute)
</contraintes>
```

## Output attendu

Table 7 lignes avec scores + 1 proposition feedback si FAIL ≥ 2.

## Variantes

- **Mode quick** : ne lancer que les checks 1, 2, 4 (mémoire / canoniques / advisor) si session courte
- **Mode mid-session** : adapter `<role>` en "tu es ton propre DA, regarde où TU as cloché jusqu'ici" (biais auto-justif élevé, à utiliser avec parcimonie)

## Apprentissages (à remplir après chaque usage)

<!-- Pattern récurrent observé / fix qui a marché / proposition de mise à jour de ce prompt -->

## Wikilinks

- [[methode-analyser-repo]]
- [[methode-pivoter-doctrine]]
- [[amanda-askell-prompt-engineering]]
