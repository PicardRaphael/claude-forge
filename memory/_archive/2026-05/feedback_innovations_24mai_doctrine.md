---
name: innovations-24mai-doctrine-meta-canonique
description: 2 innovations validées 24 mai après DA + advisor + recherche web — hook meta-commentary-detector (enforcement 100%) + auto-injection canonique read_note dans body des créateurs. Patterns originaux forge.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72a20014-5e49-4c73-a59e-6512f642233a
---

24 mai 2026 — 2 innovations forge originales déployées dans claude-forge après DA + advisor + recherche web :

**Innovation #1 — Hook `meta-commentary-detector.py`**

PreToolUse Write|Edit|MultiEdit sur composants `.claude/` + CLAUDE.md. Détecte 9 patterns interdits (Source:, D'après, `(validé X)`, `(UCL ...)`, ligne italique tradeoff, attribution auteur, justification historique). Exclusions : vault/Knowledge/references/RECAP/CHANGELOG, frontmatter YAML, désambiguïsation ≤3 mots.

Convertit doctrine "pas de meta" de advisory → enforcement 100% (cf [[raisonnement-22mai-doctrine-vs-enforcement]]).

Pattern original : appliquer un hook PreToolUse aux meta-commentaires spécifiquement. La communauté reconnaît "hook bloque > documentation advisory" mais personne ne l'applique aux patterns de justification.

**Innovation #2 — Auto-injection canonique dans body créateurs**

Section "Lecture obligatoire au démarrage" ajoutée en tête de body de :
- skill-creator → read_note(comment-creer-skill) + read_note(mcp-vs-skills-doctrine)
- agent-creator → read_note(comment-creer-agent) + read_note(workflow-claude-code-optimal)
- hook-creator → read_note(comment-creer-hook) + read_note(raisonnement-22mai-doctrine-vs-enforcement)
- claudemd-optimizer → read_note(comment-ecrire-claudemd) + read_note(erreur-meta-commentaires-composants)
- project-auditor → read_note(methode-analyser-repo) + read_note(comment-creer-hook)
- project-analyzer → idem project-auditor

Résout le finding audit "0 agent ne fait read_note dans son body" — wikilinks décoratifs devenus appels MCP obligatoires.

Pattern original : forcer la lecture EN ENTIER (SANS max_lines) de la canonique correspondante. Inédit dans la communauté.

**Why :** doctrine advisory laissait drift garanti (cf [[feedback_doctrine_drift_pattern]]). 2 angles d'attaque parallèles : (a) bloquer mécaniquement (hook), (b) charger systématiquement la source de vérité (auto-injection). Couverture défense en profondeur.

**How to apply :**
- Quand on crée un nouveau créateur/analyseur forge → AJOUTER section "Lecture obligatoire au démarrage" avec read_note des canoniques pertinentes
- Quand on audite un repo externe → PROPOSER `meta-commentary-detector.py` si CLAUDE.md > 50L OU vault canonique séparé (catalogue [[comment-creer-hook]] section "HOOKS TRANSVERSAUX")
- Posture : ces 2 innovations sont des patterns forge **réutilisables cross-repos**. Ne pas redécouvrir, propager.

**Sources de la décision :**
- DA verdict : [[critique-2026-05-24-meta-commentaires-doctrine]]
- Advisor a validé les 6 amendements DA + suggéré ces 2 innovations
- Recherche web : "hook PreToolUse > advisory documentation" = pattern reconnu communauté, mais application meta-commentaires + auto-injection canonique = inédits forge
- Anthropic claude-for-legal CLAUDE.md vérifié empiriquement : 0 meta-commentaire → doctrine forge alignée
