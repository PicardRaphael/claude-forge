---
titre: "Raisonnement — comment détecter un subagent dans un hook PreToolUse"
resume: "Instinct initial = CLAUDE_AGENT env var (utilisé partout). Pivot après vérification = agent_type/subagent_type dans le JSON stdin. Le runtime CC n'a jamais auto-set d'env var pour l'identité agent."
aliases:
  - "raisonnement agent detection hook"
  - "raisonnement CLAUDE_AGENT vs agent_type"
  - "hook subagent detection reasoning"
  - "comment detecter subagent dans hook"
type: raisonnement
domaine: claude-code
derniere-maj: 2026-05-21
auteur: claude
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
  - "#domaine/hooks"
sources:
  - "Session 2026-05-21 — dispatch-guard implementation"
---

## Problème

Comment un hook PreToolUse peut-il distinguer de manière fiable si le Write/Edit vient de la session principale ou d'un subagent nommé ?

## Chaîne de raisonnement

1. **Instinct initial : CLAUDE_AGENT env var** — Le hook tdd-guard existant (neo_ia) utilise `os.environ.get("CLAUDE_AGENT")`. Le delegate-guard de forge aussi. Pattern répandu dans la codebase. Première approche : dispatch-guard utilise la même mécanique.

2. **Vérification existence** — Grep sur tous les agents des 2 repos : AUCUN agent n'a `CLAUDE_AGENT` dans son env frontmatter. La variable n'est déclarée nulle part.

3. **Question clé** — Est-ce que le runtime CC set `CLAUDE_AGENT` automatiquement ? Lancement claude-code-guide pour vérifier.

4. **Pivot** — Documentation CC : il n'y a PAS de `$CLAUDE_AGENT` env var automatique. Le hook reçoit un JSON stdin avec `agent_id` et `agent_type` quand il s'exécute dans un subagent. C'est le mécanisme officiel.

5. **Conflit vault** — La critique vault `critique-2026-05-21-color-tdd-cto-mindset` recommandait un dispatch-guard basé sur `CLAUDE_AGENT`. La mémoire hook-creator mentionne `subagent_type` comme "champ canonique". Deux sources internes en conflit.

6. **Résolution** — Multi-field fallback : `agent_type || subagent_type`. Couvre les deux hypothèses et les variations inter-versions CC. Le DA a validé cette approche et identifié le risque single-field comme bloquant.

7. **Validation** — Les hooks existants (tdd-guard) qui utilisaient `CLAUDE_AGENT` env var étaient du dead code. Le bypass test-writer fonctionnait uniquement grâce à une autre exemption (fichiers dans tests/). Le dead code était masqué par une protection redondante.

## Insight clé

**Le code qui "marche" n'est pas forcément le code qui fait ce qu'on pense.** Le tdd-guard bypass test-writer "marchait" mais pas pour la raison attendue. Ce pattern (protection redondante masquant du dead code) est dangereux car il crée une fausse confiance — quand on retire la protection redondante ou qu'on construit un nouveau hook sur la même base, le dead code expose son vrai comportement.

**Corollaire :** quand un pattern est répandu dans la codebase (CLAUDE_AGENT env var), vérifier qu'il fonctionne réellement avant de le reproduire. La popularité interne d'un pattern ne garantit pas sa validité.

## Réutilisation

- Quand on construit un hook qui doit distinguer main session vs subagent → JSON stdin, multi-field
- Quand on audite des hooks existants → vérifier que les conditions env var sont réellement fonctionnelles
- Quand on copie un pattern d'un hook existant → vérifier empiriquement, pas juste reproduire

## Liens

- [[erreur-claude-agent-env-var-dead-code]] — l'erreur elle-même
- [[critique-2026-05-21-dispatch-guard-livraison]] — critique DA qui a validé le multi-field
- [[architecture-decision-hook-maison-vs-plugin-tiers]] — décision hook maison pour tdd-guard


## Confirmation empirique — 2026-05-21

Tests E2E exécutés sur neo_ia + ia_back. Payloads runtime capturés dans `.claude/dispatch-debug.json` :
- Main session : `agent_type` et `subagent_type` tous deux **ABSENTS**
- Subagents : `agent_type` = nom de l'agent (e.g. `"test-writer"`, `"dev-neochat"`, `"dev"`)
- `subagent_type` non observé dans aucun payload

**Verdict** : `agent_type` est le champ runtime réel. Le multi-field fallback (`agent_type || subagent_type`) reste la bonne pratique.