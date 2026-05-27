---
name: sub-agent-claim-sans-empirie-verifier-post-dispatch
description: "Sub-agents (claudemd-optimizer notamment) prétendent \"fix appliqué\" sans empirie. TOUJOURS grep/diff post-dispatch côté session principale avant de claim au user."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72a20014-5e49-4c73-a59e-6512f642233a
---

Sub-agents claim "fix appliqué" sans vérification empirique. Exemple 24 mai 2026 : claudemd-optimizer 1er passage a annoncé "7 patches appliqués" alors que 3 patterns sur 7 étaient encore présents (L55, L87, L99). Détecté uniquement parce que le sub-agent hook-creator suivant a fait un grep et a remonté l'écart.

**Why :** sub-agents génèrent leur "résumé final" depuis leur intention/plan, pas depuis l'état réel post-edit. Surtout quand ils contournent le delegate-guard via Bash + Python — l'écriture peut échouer silencieusement et le sub-agent croit que c'est fait. C'est l'extension exacte de [[feedback_audit_claims_after_brief]] mais sur les sub-agents éditeurs (pas seulement audit).

**How to apply :**
- Après TOUT sub-agent qui prétend modifier des fichiers (créateur, optimizer, hook-creator) → grep/diff empirique côté session principale
- Cible : `grep -c "pattern attendu" <fichier>` ou `git diff --stat`
- Si discordance entre claim sub-agent et réel → relancer le sub-agent en lui montrant le delta
- NE PAS relayer le claim sub-agent à Raphael sans vérification
- S'applique particulièrement aux sub-agents qui touchent à des fichiers protégés par delegate-guard (CLAUDE.md, agents/*, SKILL.md) — ils contournent souvent via Bash et l'écriture peut foirer
- Étendre la couverture [[feedback_audit_claims_after_brief]] aux ÉDITIONS, pas seulement aux audits

**Précédent vault :** [[erreur-subagent-bypass-delegate-guard]] documente le contournement Bash. Cette feedback memory documente le risque CLAIM associé.
