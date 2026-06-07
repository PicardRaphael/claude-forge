---
titre: "Bilan vault forge-brain — 2026-05-24"
resume: "Audit complet vault forge-brain le 2026-05-24 — 364 notes auditées via 6 sub-agents parallèles, 76% conformes, 59 MODIFY + 14 ARCHIVE + 5 MERGE + 1 DELETE."
aliases:
  - "bilan vault 2026-05-24"
  - "audit vault 24 mai 2026"
  - "vault audit complet 24 mai"
  - "forge-brain audit 2026-05-24"
  - "audit 364 notes vault"
  - "bilan karpathy forge-brain mai 2026"
derniere-maj: 2026-05-24
auteur: claude
type: synthese
tags:
  - "#type/synthese"
  - "#domaine/vault"
  - "#domaine/audit"
sources:
  - "Audit dispatch 6 clusters parallèles read-only via MCP forge-brain"
  - "Méthode A→B→C→D→E .claude/rules/sequence-canonique-modification.md"
  - "Pattern [[pattern-vault-llm-karpathy]] (3-layers validation)"
---

# Bilan vault forge-brain — 2026-05-24

> Audit complet livré par 6 sub-agents parallèles (clusters C1-C6) en mode read-only via MCP forge-brain. Méthode A→B→C→D→E appliquée.

---

## Stats globales

- **Notes vault** : 368 (selon `vault_stats`) — 364 auditées + 4 Karpathy racine (SCHEMA, index, log, CHANGELOG)
- **Conformes standard** : 278 (76%)
- **Écarts détectés** : 79 (24%) répartis :
  - **Type 1 doctrinal drift** : 8 cas (couleurs Agent—X, MOC-Modèles obsolète, sweet spot CLAUDE.md 100L vs 200L)
  - **Type 2 structurel** : 28 cas (orphelins graphe, mauvais dossier, frontmatter cassé)
  - **Type 3 qualité** : 43 cas (aliases <4, resume générique, wikilinks <2, stubs)
- **Tags vault** : 190 (4 `None`, doublons `#projet/ia-back` vs `#projet/ia_back`)
- **Wikilinks** : 2276 (densité saine)
- **Aliases** : 2148 (moyenne 5.8/note — au-dessus du seuil 4-6)

## Karpathy 3-layers — validation

| Élément | Status | Détail |
|---|---|---|
| `raw/` | ✅ OK | 8 sources immuables `raw/2026-05-22-chantier/` |
| `wiki/` (couche LLM-owned) | ✅ OK | 13 dossiers wiki respectés selon ontologie SCHEMA |
| `SCHEMA.md` | ✅ OK | À jour 2026-05-22, conventions claires |
| `index.md` | ⚠️ Mineur | Content-oriented mais Home.md = sommaire de dossiers (drift léger) |
| `log.md` | ✅ OK | Append-only respecté, format `## [YYYY-MM-DD] action \| titre` |
| `CHANGELOG.md` | ✅ OK | Narration prosaïque à jour 23 mai |

**Verdict Karpathy** : conforme. Home.md à reconverger vers content-oriented (P1).

---

## Plan priorisé

### P0 — Critiques (à fixer immédiatement)

| Action | Cluster | Impact |
|---|---|---|
| **Couleurs 5 fiches `Agent — X`** : 4 meta-créateurs → `pink` (agent-creator=blue, claudemd-optimizer=yellow, hook-creator=orange, skill-creator=green) + project-auditor red → purple | C2 | Drift Type 1 auto-référentiel (canonique [[agents-color-convention]] contredite) |
| **MOC-Modèles drift** : Gemini 4.0 "attendu I/O 19 mai" passé, GPT-5.4 vs GPT-5.5 incohérent entre MOCs | C1 | Type 1 doctrinal, haute visibilité |
| **Effort Levels Guide YAML cassé** : aliases inline + bloc liste dupliqué → parser cassé, `get_property` retourne `introuvable` | C4 | Bug parsing Obsidian, note critique |
| **MERGE `mcp-vs-cli-vs-skills` → `mcp-vs-skills-doctrine`** : doublon sémantique, doctrine 23 mai canonique | C2 | Préserver benchmarks tokens uniques |
| **MOC-Leaders section `## Industrie` dupliquée** : erreur d'édition à fusionner | C1 | Type 3 structurel |
| **Leak scope MCP forge-brain** : `.claude/agent-memory/` indexé alors que hors `vault/claude-forge/` | C1 | Pollution résultats search |
| **Sonnet 4.6 + Haiku 4.5 stubs** : pricing/benchmarks/ID manquants, disproportion vs Opus 4.7 | C3 | Modèles de production quotidienne |

### P1 — Qualité (vague suivante)

| Action | Cluster | Notes concernées |
|---|---|---|
| **7 fiches `Agent — X` stubs ~30L** à étoffer (workflow, paramètres, exemples) | C2 | Toutes les `Agent — agent-creator`, etc. |
| **4 features stubs** : Agent Teams, Claude Desktop, Session Sharing, Project Glasswing | C2 | Étoffer ou MERGE |
| **14 orphelines Knowledge** à reconnecter (0 backlink) | C6 | erreur-subagent-bypass, erreur-seuils-canoniques, agents-ia-22-claims-fausses, erreur-4-fabrications, critique-2026-05-21-brief-distant, critique-2026-05-22-audit-neo_ia, critique-2026-05-22-guard-ddl-ban, neo-ia-tests-lenteur-diagnostic, question-idor-coproprietes, architecture-full-web-charte, techniques-inedites, outils-portabilite-forge, rag-obsidian-claude-video-analyse, neoteem-agentic-engineering-mapping |
| **5 fiches leaders `sources: []` vides** : Sam Altman, Amanda Askell, Rafael Rafailov, Patrick Lewis, Teknium | C5 | Combler sources frontmatter |
| **Home.md** : resume générique + non content-oriented Karpathy strict | C1 | Refonte vers index concepts |
| **`_META-GENERATOR` orpheline (0 backlink)** : créée 24 mai, lier depuis MOC-Prompts + CLAUDE.md | C3 | Sinon jamais trouvée |
| **2 incohérences canonique/doublon** : Harrison Chase + Ethan Mollick — la "doublon" est plus complète que la "canonique" | C5 | Décision : inverser ou enrichir canonique |

### P2 — Cosmétique / Maintenance

| Action | Cluster | Détail |
|---|---|---|
| **Notes >500L** : extraction vers `references/` | C4 | methode-analyser-repo (605L), workflow-claude-code-optimal (553L), stack-python-ia (492L) |
| **Surveiller proche seuil** : pattern-vault-llm-karpathy (498L), comment-creer-agent (477L), comment-creer-hook (468L) | C4 | Croissance future |
| **Tags incohérents** : `#type/knowledge` → `#type/feature` pour Cowork GA + Managed Agents | C2 | Cohérence taxonomie |
| **Aliases dupliqués (inline + YAML list)** : context-management, Code with Claude 2026 | C2 | Parsing potentiellement cassé |
| **Allie K Miller orpheline** : 0 backlink, à lier depuis MOC-Leaders-Industrie | C5 | Reconnexion graphe |
| **GitHub Copilot + Gemini CLI + Agent Skills Spec** : `derniere-maj` 28-33 jours sur fast-evolving | C3 | Refresh à prévoir |
| **OpenAI Revenue 25B + Anthropic Revenue 30B** : MERGE potentiel dans `revenues-IA-2026` | C3 | OpenAI Revenue 25B presque vide |
| **Méta-index `audit-23mai-fabrications`** : créer index regroupant les 6 erreurs audit thématique 23 mai | C6 | Sous-indexation actuelle |

### Archive (chantier livré)

| Action | Cluster | Notes |
|---|---|---|
| **Archiver 12 notes `_chantier-22mai/`** vers `raw/chantier-22mai/` ou `Knowledge/audits-archives/` | C1 | Polluent 0-Inbox (ontologie "capture rapide à trier") |
| **MIGRATE `audit-mcp-forge-brain`** vers `04-Techniques/claude-code/` | C1 | Note référence durable (2 backlinks réels), pas inbox |
| **Archiver 2 snapshots datés** : analyse-2026-05-22 (ia_back), analyse-claude-code-2026-05-13 (lojii) | C6 | 0 backlink |

---

## Actions ADD (notes manquantes détectées)

Peu de wikilinks brisés majeurs (aucun crash). Quelques candidats :
- Backlink retour `Allie K Miller` ← MOC-Leaders-Industrie
- Backlink retour 14 orphelines Knowledge ← notes canoniques liées

## Actions MODIFY (par cluster — synthèse 59 notes)

- **Aliases insuffisants (< 4)** : ~3 notes (Claude Mythos Preview, delegate-guard-pattern, etc.)
- **Resume générique** : ~5 notes (Home, Claude Desktop, Project Glasswing, Session Sharing, Piebald-AI)
- **Wikilinks manquants (< 2)** : ~8 notes (`Agent — X` stubs, features stubs)
- **Tags non conformes** : 2 (Cowork GA + Managed Agents)
- **Frontmatter YAML cassé** : 3 (Effort Levels Guide, context-management, Code with Claude 2026)
- **Stubs <30L** : 11 (7 `Agent — X` + 4 features)
- **Sources vides** : 5 (Sam Altman, Amanda Askell, Rafael Rafailov, Patrick Lewis, Teknium)
- **Drift Type 1 doctrinal** : 6 (couleurs Agent — X + project-auditor, MOC-Modeles, claudemd-optimizer 100L)

## Actions DELETE (1)

- Aucune suppression franche identifiée. Les 14 archives ne sont pas des DELETE mais des MIGRATE vers `raw/` ou `Knowledge/audits-archives/`.
- Candidate single : si décision business → `_chantier-22mai/PLAN-EXECUTION-FINAL` (status: archive après chantier livré)

## Actions MERGE (5)

1. **`mcp-vs-cli-vs-skills`** → `mcp-vs-skills-doctrine` (C2) — doublon sémantique, doctrine 23 mai canonique
2. **OpenAI Revenue 25B + Anthropic Revenue 30B** → `revenues-IA-2026` (C3) — OpenAI Revenue 25B presque vide
3. **Project Glasswing** → potentiellement absorbé dans `Claude Security` (C2) — vérifier infos uniques
4. **Claude Desktop (stub)** → enrichir ou MERGE dans `claude-desktop-preferences` (C2)
5. **Harrison Chase / Ethan Mollick** : décision inversion canonique/doublon ou enrichissement canonique (C5)

---

## Patterns transverses détectés

1. **Chantier 22 mai livré mais notes de travail en `_chantier-22mai/` non archivées** — 12 notes 0 backlink polluent 0-Inbox
2. **Stubs systématiques** sur fiches `Agent — X` (~30L) et features secondaires (~20L)
3. **Audit 23 mai thématique très efficace** : 91/95 notes 04-Techniques OK, 71/79 leaders OK — la fraîcheur post-audit tient
4. **Doctrine 22 mai bien propagée** : raisonnement-22mai-doctrine-vs-enforcement = 35 backlinks (cœur doctrinal solide)
5. **Drift couleurs Agent — X** = drift Type 1 auto-référentiel : le vault contredit sa propre canonique [[agents-color-convention]]
6. **Leak scope MCP forge-brain** sur `.claude/agent-memory/` — indexer hors `vault/claude-forge/`
7. **0 doublon réel détecté** sur 04-Techniques malgré apparences (Agents IA / agents-architecture, 4 notes SDD, etc.) — séparation conceptuelle valide
8. **Aliases dupliqués (inline + YAML list)** = pattern récurrent (3 notes touchées) → bug de templater ou éditeur Obsidian ?

---

## Décision Raphael (GO/NO-GO par vague)

**Vague E1 — P0 critiques** (~30 min, peu risqué, gains forts) :
- Fix couleurs 5 fiches `Agent — X`
- Fix MOC-Modèles (Gemini 4.0 + GPT-5.4/5.5)
- Fix Effort Levels Guide YAML cassé
- MERGE mcp-vs-cli-vs-skills
- Fix MOC-Leaders dédupliquer `## Industrie`
- Configurer scope MCP forge-brain (exclure `.claude/agent-memory/`)
- Étoffer Sonnet 4.6 + Haiku 4.5 (specs + benchmarks)

**Vague E2 — P1 qualité** (~1h-2h, productif) :
- Étoffer 7 stubs `Agent — X` + 4 features stubs
- Reconnecter 14 orphelines Knowledge
- Combler 5 fiches leaders `sources: []`
- Refondre Home.md content-oriented Karpathy
- Lier `_META-GENERATOR`
- Décision Harrison Chase / Ethan Mollick (inversion ou enrichissement)

**Vague E3 — P2 cosmétique + archives** (~1h, ménage) :
- Archiver 12 notes `_chantier-22mai/` + 2 snapshots datés
- MIGRATE audit-mcp-forge-brain vers 04-Techniques/claude-code/
- Tags Cowork GA + Managed Agents
- Aliases dupliqués (3 notes)
- Notes >500L extraction `references/`
- Méta-index audit-23mai-fabrications

**Total estimé** : E1 ~30 min, E2 ~1-2h, E3 ~1h. Soit ~3h pour assainissement complet.

---

## Question à Raphael

**GO pour appliquer E1 (P0) ?** GO global E1+E2+E3 ? Préférence d'ordre ? Veux-tu valider note par note pour les MERGE / archive sensibles ?

---

## Wikilinks

- [[pattern-vault-llm-karpathy]] — pattern canonique 3-layers validé
- [[methode-analyser-repo]] — séquence A→B→C→D→E appliquée
- `.claude/rules/sequence-canonique-modification.md` — méthode source canonique (rule, hors vault)
- [[methode-pivoter-doctrine]] — checklist post-pivot
- [[SCHEMA]] — conventions vault
- [[index]] — index content-oriented
- [[CHANGELOG]] — narration prosaïque
- [[agents-color-convention]] — canonique couleurs (contredite par 5 fiches)
- [[mcp-vs-skills-doctrine]] — canonique doctrine MCP/Skills
