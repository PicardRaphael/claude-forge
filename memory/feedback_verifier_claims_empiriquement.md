---
name: verifier-claims-empiriquement
aliases:
  - audit-claims-after-brief
  - audit-claims-after-brief-or-subagent
  - sub-agent-claim-sans-empirie
description: "Tout claim \"X créé/modifié/fixé/fait\" — le mien en fin de tâche OU celui d'un sub-agent éditeur (skill-creator, claudemd-optimizer, hook-creator, architect) — DOIT être vérifié empiriquement (ls/cat/grep/diff/test) AVANT d'être relayé à l'utilisateur. Le claim vient de l'intention, pas de l'état réel post-edit."
metadata:
  type: feedback
---

Tout claim "X créé / modifié / fixé / fait" doit être vérifié empiriquement AVANT d'être relayé comme acquis à l'utilisateur. Vaut pour MES briefs de fin de tâche ET pour les retours de sub-agents éditeurs. Un sub-agent génère son résumé depuis son intention/plan, pas depuis l'état réel post-edit — l'écriture peut échouer silencieusement (surtout en contournant `delegate-guard` via Bash) sans que le sub-agent le sache.

**Why:**
- Session 2026-05-20 : annoncé `certs/README.md` créé → DA vérifie `ls certs/` → inexistant. Claim faux relayé = perte de confiance. Même session : sub-agent x-read écrit `claude-forge/secrets/` au lieu de `claude-forge/.claude/secrets/` (calcul de path faux).
- Session 2026-05-24 : claudemd-optimizer annonce "7 patches appliqués" alors que 3 patterns sur 7 étaient encore présents (L55, L87, L99). Détecté uniquement parce que le hook-creator suivant a grep et remonté l'écart.
- Récidive 2026-05-27 (ce chantier) : skill-creator annonce 296L puis 309L pour un SKILL.md qui en fait 211 puis 219. Vérif PowerShell systématique a corrigé.

**How to apply:**
- Brief contient "X créé" → `ls X` ou `cat X | head` AVANT de relayer.
- Brief contient "Y modifié" → `grep <pattern attendu> Y` pour confirmer.
- Brief contient "fix appliqué" → re-grep le motif fixé pour vérifier qu'il a disparu.
- Sub-agent retourne un calcul (path résolu, nombre de lignes, version, regex matched) → recalculer indépendamment avant d'agir dessus. Pour les paths Python `Path(__file__).parent.parent.parent` : compter les parents manuellement vs le fichier réel.
- "Skill chargée dans la liste" ≠ "skill fonctionnelle" — tester avec un appel concret.
- S'applique particulièrement aux sub-agents touchant des fichiers protégés par `delegate-guard` (CLAUDE.md, agents/*, SKILL.md) : ils contournent via Bash, l'écriture peut foirer silencieusement.
- Si discordance claim vs réel → relancer le sub-agent en lui montrant le delta. NE PAS relayer le claim brut.
- Coût d'un check empirique : 1 tool call. Coût d'un claim faux : confiance + correction publique.

Consolide depuis : [[feedback_audit_claims_after_brief]] (claims de brief, général) et [[feedback_sub_agent_claim_sans_empirie]] (extension aux sub-agents éditeurs). Précédent vault : [[erreur-subagent-bypass-delegate-guard]]. Lié : [[verify-exhaustive-claims]], [[gotchas-line-numbers-verifies-empiriquement]], [[verify-empirique-avant-affirmation-session]].
