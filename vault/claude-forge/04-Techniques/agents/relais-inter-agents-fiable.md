---
titre: "Relais inter-agents fiable — mémoire de travail partagée"
resume: "Hub : les 3 fuites du multi-agent (perte verticale / redondance horizontale / coût de relecture) et leurs parades canoniques. Pointe vers les foyers existants, ne les re-rédige pas. Net-neuf = le registre léger, en hypothèse."
aliases:
  - "relais inter-agents"
  - "relais inter-agents fiable"
  - "mémoire de travail partagée agents"
  - "transmettre contexte entre agents"
  - "anti-doublon recherche multi-agent"
  - "coordination agents tokens"
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
  **pas encore canonique**, hypothèse en cours : `feedback_registre-relais-agents`.

## Quand appliquer — vs sur-engineering

- Appliquer le relais explicite quand : tâche **séquentielle** à ≥ 3 relais, ou
  plusieurs agents sur des sous-tâches **connexes** (gain × N).
- Sur-engineering quand : fan-out **parallèle** (aucun handoff sur le chemin
  critique — c'est déjà optimal), ou tâche one-shot courte. **La coordination
  ne doit jamais coûter plus que ce qu'elle économise.**

## Liens

- [[technique-shared-agent-memory]] — mémoire persistante (CLAUDE.md / `memory:` agent / Cowork)
- [[anti-reentrance-sub-agents-pattern-escalade]] — escalade vers la session principale
- [[3-axes-strategiques-forge]] — discipline tokens
