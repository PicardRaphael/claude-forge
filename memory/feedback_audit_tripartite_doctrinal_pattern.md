---
name: audit-tripartite-doctrinal-pattern
description: "Pour décision majeure config CC, lancer 3 teammates Agent Teams avec lentilles doctrinales distinctes (Will/ECC/Boris). Débat via mailbox → consensus 3/3, 2/3, désaccords priorisés."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a4e196c9-ffac-4668-a189-2e0902c13357
---

Pattern validé empiriquement 26 mai 2026 : audit forge/ia_back/neo_ia via Agent Team `forge-audit-doctrines` avec 3 teammates :
- will-auditor (doctrine Anthropic Applied AI : minimum agents, frontier models can manage)
- ecc-auditor (doctrine ECC hackathon winner : spécialisation, capitalisation skills)
- boris-auditor (doctrine Boris Cherny : compounding, verify output, /clear, Karpathy)

**Why** : 1 seul auditeur = vision partielle. 3 lentilles croisées via débat mailbox = signal beaucoup plus fort, hiérarchie naturelle Critical(3/3) / Important(2/3) / Minor(1/3 désaccords).

**Résultats empiriques de cette session** :
- Convergence 3/3 sur 6 fusions agents + 6 migrations Haiku
- Convergence 2/3 sur 17 skills à capitaliser + pipeline AgentShield
- Désaccords explicites Will/ECC sur 3 fusions secondaires → arbitrage utilisateur clair

**How to apply** :
1. `TeamCreate(team_name="<audit-name>")` + TaskCreate 4 tasks (3 audits + 1 consensus)
2. `Agent(subagent_type="project-auditor", team_name="<audit-name>", name="will-auditor", prompt="...")` x3
3. Briefs incluent : lentille doctrinale + `read_note` canoniques vault + workflow (claim task → analyse → SendMessage challenge → respond → mark completed)
4. ECC ou Boris (le plus exigeant) prend Task #4 consensus
5. `TeamDelete` après shutdown gracefully

**Gotcha critique** : skills frontmatter NOT applied en teammate (limitation Anthropic). Inclure instructions MCP en clair dans body du prompt. Workaround = déclarer skills dans project settings.

**Candidat capitalisation `~/.claude/agents/`** : will-auditor.md / ecc-auditor.md / boris-auditor.md scope user cross-repo réutilisables sur tout audit futur.

Liens : [[anti-reentrance-sub-agents]], [[anthropic-doctrine-biais-full-thune]]
