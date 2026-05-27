---
name: spec-driven-development-pattern
description: "Pattern SDD complet — Thariq interview→SPEC.md→new session, feature-dev plugin 7 phases, GSD/SpecKit/BMAD frameworks, calibration gate, cross-BRIEF contradiction detection"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 42f0ff3e-7431-4682-bf0b-f2823840a715
---

## Pattern Spec-Driven Development (recherche 2026-05-12)

### Consensus pionniers
- **Thariq Shihipar** (Eng Manager CC) : "interview me using AskUserQuestion → SPEC.md → new session to execute"
- **Boris Cherny** (créateur CC) : Plan Mode → iterate → one-shot. "Give Claude a way to verify its work"
- **Anthropic docs officiels** : interview → SPEC.md → clean session
- **Upfront investment** : plus le workflow IA est long, PLUS le travail humain amont est important

### feature-dev plugin (Sid Bidasaria, Anthropic)
7 phases : Discovery → Exploration (2-3 agents //) → Questions → Architecture (2-3 architectes //) → Implementation → Review (3 reviewers //) → Summary.
Installable via `/plugin install feature-dev@claude-plugins-official`.
Différence avec /spec : feature-dev fait tout en session, /spec produit des artefacts collaboratifs.

### Frameworks communautaires
- **GitHub Spec Kit** (93K stars) : Constitution → Specify → Clarify → Plan → Tasks → Implement
- **GSD** (59K stars) : Discuss → Plan → Execute → Verify → Ship, contexte frais par agent
- **BMAD** (46K stars) : 12+ agents SDLC, document sharding en story files

### Innovations identifiées
1. **Cross-BRIEF contradiction detection** — personne ne fait ça, multi-audience checking
2. **BRIEF-as-RAG-view** — BRIEFs = projections d'une source unique
3. **Pre-code test skeleton** (Red Gate) — tests qui échouent AVANT le code
4. **Calibration gate** — adapter la taille du dossier spec à la complexité (S/M/L/XL)
5. **Spec diff** — planning vs reality post-implémentation

### Pipeline Neoteem validé
```
/spec (idée → dossier spec) → /decompose-ticket (spec → tâches CC) → /go (exécution)
```

### Anti-patterns
- Over-specification paradox (UCL 2601.00880) : > S*=0.509 = dégradation quadratique
- Monolithic spec > 150 instructions = compliance drop
- Kitchen sink session = pollution contexte

**Why:** Recherche exhaustive web + vault pour construire la skill /spec dans ia_back et neo_ia.
**How to apply:** Utiliser comme référence lors de la création de la skill /spec et pour tout workflow de planification.
