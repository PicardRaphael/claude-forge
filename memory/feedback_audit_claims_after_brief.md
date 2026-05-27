---
name: audit-claims-after-brief-or-subagent
description: "Après un brief ou un retour de sub-agent, TOUJOURS vérifier empiriquement (ls/cat/grep/test) les claims \"X créé/modifié/fixé\" avant de les relayer comme acquis"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8957d13-cb6a-43d0-ae69-71bb7fa375a2
---

Après chaque brief de fin de tâche (le mien ou d'un sub-agent) qui claim "X créé/modifié/fait" : vérifier empiriquement avant de relayer comme acquis à l'utilisateur.

**Why:** Session 2026-05-20 : j'ai annoncé que `certs/README.md` était créé. DA a vérifié `ls certs/` → fichier inexistant. Probablement effacé quand Jérôme a donné les vrais certs et tu as remplacé le contenu du dossier. Claim faux relayé à l'utilisateur = perte de confiance.

Pattern fréquent aussi avec sub-agents skill-creator/architect : ils annoncent "fix appliqué" mais le calcul de path peut être faux (cf x-read SKILL.md où le sub-agent a écrit `claude-forge/secrets/` au lieu de `claude-forge/.claude/secrets/`).

**How to apply:**
- Brief contient "X créé" → `ls X` ou `cat X | head` AVANT de relayer
- Brief contient "Y modifié" → `grep <pattern attendu> Y` pour confirmer
- Brief contient "fix appliqué" → re-grep le motif fixé pour vérifier qu'il n'existe plus
- Sub-agent retourne un calcul (path résolu, version installée, regex matched) → recalculer indépendamment avant d'agir dessus
- Pour les paths Python `Path(__file__).parent.parent.parent` : compter manuellement les parents et vérifier vs le fichier réel
- "Skill chargée dans la liste" ≠ "skill fonctionnelle" — toujours tester avec un appel concret
- Coût d'un check empirique : 1 tool call. Coût d'un claim faux : confiance + correction publique
