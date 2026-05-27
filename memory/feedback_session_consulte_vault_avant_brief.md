---
name: session-consulte-vault-avant-brief-sub-agent
description: "La SESSION PRINCIPALE doit consulter le vault EN PREMIER, extraire le contexte, le mettre DANS le brief du sub-agent. Jamais déléguer la lecture vault aveuglément."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: df277af9-47f3-4793-8326-bf2e183d5f4a
---

La session principale (Jarvis) DOIT consulter le vault forge-brain AVANT de briefer un sub-agent créateur/analyseur, extraire le contexte pertinent, et le METTRE DANS le brief. Le sub-agent ne fait que re-consulter en filet de sécurité (pattern brief-then-direct).

**Why :** 2026-05-27, erreur grave. J'ai modifié les templates BRIEF de la skill /spec (ia_back + neo_ia) en INVENTANT 4 sections (Gherkin, recherche préalable, refs, vérif) avec seulement l'advisor, SANS consulter le vault. J'ai même briefé skill-creator en lui demandant de lire `comment-creer-skill` (MAUVAISE canonique pour un template de spec/output) sans vérifier qu'il l'a fait. Raphael m'a repris : "ni toi ni skill-creator n'avez call le vault". En cherchant APRÈS coup, j'ai trouvé des notes canoniques directement pertinentes JAMAIS lues : `pattern-spec-driven-development`, `pattern-sdd-triangle`, `pattern-spec-skill-deployment` (template BRIEF déjà documenté !), `critique-2026-05-21-brief-distant-template-spec` (un DA avait DÉJÀ critiqué ce template !), `running-implementation-notes`, `methode-analyser-repo`.

**How to apply :**
1. AVANT toute modif de composant `.claude/` ou tout brief de sub-agent créateur → `mcp__forge-brain__search_brain` sur le SUJET RÉEL de la tâche (pas le type de composant)
2. Lire les canoniques pertinentes EN ENTIER (`read_note` sans max_lines)
3. Choisir la BONNE canonique : modifier un template de spec ≠ créer une skill. Le sujet (SDD, BRIEF, handoff agent) dicte la canonique, pas le type de fichier.
4. EXTRAIRE le contexte vault et le METTRE dans le brief du sub-agent (pattern [[pattern-mcp-brief-then-direct]])
5. Le sub-agent re-consulte seulement en filet, pas en exploration aveugle
6. VÉRIFIER empiriquement que le sub-agent a lu le vault (cf [[sub-agent-claim-sans-empirie-verifier-post-dispatch]])

Anti-pattern combiné : biais d'action en session longue + délégation de la lecture vault au sub-agent + pas de vérification empirique. Les 3 ensemble = travail non sourcé.

Audit de réparation : `claude-forge/PROMPT-audit-vault-jamais-consulte.md` (à lancer en session fraîche).

Lien : [[feedback_lire_canoniques_avant_audit]], [[feedback_workflow_spec_forge_jira]], [[feedback_spec_trous_structurels_a_checker]]
