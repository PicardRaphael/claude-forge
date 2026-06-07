---
titre: "Erreur — 22 claims fausses vault Claude Code détectées audit 23 mai 2026"
resume: "Audit thématique 95 claims a révélé 22 erreurs structurelles ou citations fausses propagées dans le vault — fondations doctrinales mal sourcées (Justin Young split, Brad Abrams vs Angela Jiang, lethal trifecta Thariq vs Willison). Causes: extrapolation forge non sourcée + propagation coquilles tierces (Simon Willison Angela Kiang) + paraphrases présentées comme verbatim Anthropic."
aliases:
  - "erreur 22 claims fausses 23 mai"
  - "audit thematique erreurs propagees"
  - "doctrine drift verbatim"
  - "extrapolation forge non sourcee"
  - "coquille Angela Kiang Angela Jiang"
derniere-maj: 2026-05-23
auteur: claude
type: erreur
sources:
  - "Audit thématique vault Claude Code 23 mai 2026"
  - "output/audit-vault-thematique/01-claude-code/"
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#domaine/doctrine"
---

# Erreur — 22 claims fausses vault Claude Code détectées audit 23 mai

## QUOI s'est passé

Audit thématique de 12 notes canoniques vault Claude Code (chantier 22 mai déjà commité, vérifié par DA) a révélé **22 erreurs propagées** :

### 3 erreurs structurelles (Type 3 — réécriture)
1. **Justin Young 2-agent = "Opus init + Sonnet coding"** — extrapolation forge. Article dit textuellement "harness was otherwise identical".
2. **Advisor strategy = Angela Jiang 5× cost reduction** — coquille Simon Willison "Angela Kiang" propagée. Vraie attribution = **Brad Abrams** (CwC SF avec Mario Rodriguez GitHub). Verbatim : "close to Opus-level intelligence at much lower prices", **pas de chiffre 5×**.
3. **Lethal trifecta = Thariq** — terme créé par **Simon Willison juin 2025**.

### 9 attributions/sources fausses
- "Agent = Model + Harness" attribué à Fowler/Böckeler → en fait Hashimoto popularise (5 fév 2026)
- LangChain 52.8→66.5 attribué à Fowler 2 avril → en fait Vivek Trivedy LangChain 17 fév 2026, modèle **GPT-5.2-Codex** pas Claude
- Hashimoto "coined harness engineering" → il hedge lui-même "I didn't coin", popularise
- "AGENTS.md compounding pattern Hashimoto" → spec collective OpenAI/Google/Cursor août 2025
- Boris "MCP cross-surface" → terme "cross-surface" non verbatim
- Karpathy "Vibe coding is over → Agentic engineering" → titre exact "From Vibe Coding to Agentic Engineering", complémentaires pas remplacement
- 9 catégories Thariq "LinkedIn 17 mars" → post Anthropic mars 2026 "Lessons from Building Claude Code"
- "Claude decides when to parallelize — you're defining the capability, not the scheduling" → formule paraphrasée, verbatim docs = "Claude decides when to call a tool"
- Böckeler "isn't the model itself" → "except the model itself"

### 6 chiffres inventés
- claude-for-legal CLAUDE.md = 174L (pas 130)
- multica-ai = 67L (pas 70)
- Hook timeouts = 600s/30s/60s selon type (pas 60s partout)
- 29 events hooks (pas 25+) — vault rate TaskCreated + StopFailure
- effort: max TOUJOURS DISPONIBLE mai 2026 (pas déprécié v2.1.91)
- Boris Plan Mode "~80% des sessions" → "most sessions" attesté, 80% non sourcé
- Osmani "Forge 79.8% vs CC 58%, +21.8 pts" → 58% et +21.8 non sourcés chez Osmani

### 3 conseils techniques invalides
- Stop hook `once: true` dans settings.json → ignoré silencieusement, honoré uniquement skill frontmatter
- Description SKILL.md limite 1024 chars → vraie limite pratique ~250 chars (system reminder `/skills` tronque)
- "Hooks are deterministic and recommended for lint, test, and security" présentée comme verbatim Anthropic → paraphrase, pas dans docs/hooks

## POURQUOI c'est arrivé

### Cause 1 — Extrapolation forge non sourcée
- "Sonnet exécution / Opus jugement" doctrine forge basée sur pattern observé en sessions
- Cherchait un appui Anthropic → choisi Justin Young 2-agent → extrapolé "Init=Opus, Coding=Sonnet" qui n'est PAS dans l'article
- Pattern : doctrine forge plausible cherche source canonique → extrapole un détail non écrit

### Cause 2 — Propagation de coquilles tierces
- Simon Willison live blog CwC London écrit "Angela Kiang" (lapsus)
- Vault forge corrige automatiquement en "Angela Jiang" (la vraie Angela existe à Anthropic)
- Mais attribue à Angela Jiang ce qui revient à Brad Abrams (autre talk même conférence)
- Pattern : correction de typo source tierce sans vérifier l'attribution réelle

### Cause 3 — Paraphrases présentées comme verbatim
- Concept canonique Anthropic ("Claude decides when to invoke") attesté multi-sources
- Forge a écrit une formule pédagogique élégante : "Claude decides when to parallelize — you're defining the capability, not the scheduling"
- Cette formule n'existe pas dans Agent SDK overview
- Pattern : verbatim "approximatif" inventé pour densité pédagogique

### Cause 4 — search_brain seul ≠ audit
- Phase B audit doctrine 22 mai utilisait `search_brain` (extraits ~10 lignes)
- Insuffisant pour détecter qu'un chiffre 174L est écrit 130L dans une autre section
- Insuffisant pour repérer attribution croisée Hashimoto→Fowler
- Pattern : audit basé sur search ≠ audit basé sur read_note entier

## QUOI faire à la place — méthode validée 23 mai

### Avant écrire un verbatim Anthropic
1. **Fetch direct docs** : `WebFetch` la page exacte
2. **Grep le verbatim** : ne JAMAIS inventer une formule "approximative" présentée comme citation
3. **Si paraphrase** : marquer explicitement "paraphrase pédagogique" ou "concept attesté multi-sources"

### Avant attribuer une stratégie à quelqu'un
1. **Vérifier sur LinkedIn / X officiel** : qui est-ce ? Quel rôle ?
2. **Trouver le talk source primaire** (slug CwC, transcript, blog Anthropic)
3. **Vérifier croisé** : 1 source tierce peut avoir une coquille (Willison "Angela Kiang")

### Avant citer un chiffre numérique
1. **gh api ou WebFetch** pour mesurer empiriquement (lignes, stars, etc.)
2. **Marquer date de vérification** : "174 lignes (vérifié 23 mai 2026)"
3. **Si chiffre non sourcé** : retirer ou remplacer par qualitatif ("la plupart" pas "80%")

### Méthode audit valide
- **read_note SANS max_lines** (pas search_brain)
- **Sub-agents par cluster thématique** (pas par note)
- **Self-verify FAUX à fort impact** AVANT phase D
- **Distinguer Type 1/2/3** dans plan correction

## Comment éviter

- Si une claim semble parfaite et trop précise (verbatim, chiffre, attribution) → la **vérifier directement** avant de la propager
- Si plusieurs notes citent la même formule mot pour mot → suspect que c'est une paraphrase forge, pas un verbatim
- Si une coquille tierce existe (live blog typo) → trianguler avec 2+ sources avant correction

## Liens

- [[critique-2026-05-22-8-canoniques-chantier]] — DA initial qui avait détecté 1 bloquant mais raté ces 22
- [[methode-pivoter-doctrine]] — pattern régression silencieuse
- [[methode-analyser-repo]] — séquence A→B→C→D→E
- [[Brad-Abrams]] — fiche leader créée pour corriger l'attribution
- [[Mitchell-Hashimoto]] — fiche leader créée pour corriger l'attribution
- [[comparaison-skill-anthropic-claude-code-setup]] — comparaison post-audit
- `output/audit-vault-thematique/01-claude-code/` — artefacts complets (95 claims, 6 clusters, croisement, plan)

## Stats audit

- **95 claims auditées** (12 notes canoniques)
- **6 sub-agents parallèles** par cluster thématique
- **4 commits** poussés sur main
- **22 erreurs corrigées** (3 structurelles + 9 attributions + 6 chiffres + 3 conseils invalides + 1 verbatim Anthropic non vérifié)
- **2 fiches leaders créées** (Brad Abrams, Mitchell Hashimoto)
- **1 rule transverse** : `.claude/rules/sequence-canonique-modification.md`
- **Temps wall-time** : ~30 min phase B (sub-agents) + ~2h phase D-E (réécriture vault)
