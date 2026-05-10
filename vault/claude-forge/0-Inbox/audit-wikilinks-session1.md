---
titre: "Audit Wikilinks — Session 1 Migration Vault"
resume: "86 liens orphelins identifiés dans le vault, classés par catégorie avec source et action recommandée"
aliases:
  - "audit wikilinks"
  - "liens orphelins vault"
  - "wikilinks audit"
  - "orphan links audit"
type: context
status: active
derniere-maj: 2026-05-10
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Résumé

- **248 wikilinks** uniques scannés dans 198 notes
- **98 liens** sans note correspondante
- **12 faux positifs** (paths résolus + liens formatifs) → **86 vrais orphelins**

## Faux positifs (pas d'action)

| Lien | Raison |
|------|--------|
| `1-Projets/*/...` (10 liens) | Wikilinks avec path complet — fichiers existent |
| `créez un lien` | Placeholder dans Bienvenue.md |
| `Grok")\`` | Lien malformé (regex artifact) |

---

## Cat. 1 — Modèles inexistants (7 liens)

Impact : **MOC-Modeles cassé**. Action : supprimer les liens ou créer les notes en Session 2 (cc-news).

| Lien orphelin | Référencé dans | Action |
|---------------|---------------|--------|
| `[[GPT-5.4]]` | MOC-Modeles, OpenAI Codex, plan | Supprimer (GPT-5.5 sera créé) |
| `[[Opus 4.6]]` | MOC-Modeles, plan | Supprimer (Opus 4.7 existe déjà) |
| `[[Gemini 3.0 Flash]]` | MOC-Modeles, plan | Supprimer ou créer en Session 2 |
| `[[Gemini 3.1 Pro]]` | MOC-Modeles, plan | Supprimer ou créer en Session 2 |
| `[[GPT-5.3 Codex Spark]]` | MOC-Modeles, plan | Supprimer (obsolète) |
| `[[Grok 4.3 Beta]]` | MOC-Modeles, plan | Supprimer ou créer en Session 2 |
| `[[Grok 5]]` | MOC-Modeles, plan | Supprimer ou créer en Session 2 |

## Cat. 2 — Leaders sans fiche (12 liens)

Impact : MOC-Leaders + notes techniques ont des liens morts. Action : créer les fiches leaders prioritaires.

| Lien orphelin | Référencé dans | Action |
|---------------|---------------|--------|
| `[[Amanda Askell]]` | MOC-Leaders, Karpathy Dev, amanda-askell-PE, System Prompt AA | **Créer** (4 refs) |
| `[[Cat Wu]]` | MOC-Leaders | Créer en Session 2 |
| `[[Noah Zweben]]` | MOC-Leaders | Créer en Session 2 |
| `[[Jarred Sumner]]` | MOC-Leaders | Créer en Session 2 |
| `[[Alex Albert]]` | MOC-Leaders, claude-desktop-preferences | **Créer** (2 refs) |
| `[[Yann LeCun]]` | MOC-Leaders | Créer en Session 4 |
| `[[Elon Musk]]` | MOC-Leaders | Évaluer (pertinence ?) |
| `[[Joao Moura]]` | Agents IA, agents-frameworks | **Créer** (2 refs tech) |
| `[[Yohei Nakajima]]` | Agents IA | Créer en Session 4 |
| `[[Patrick Lewis]]` | RAG, Douwe Kiela | **Créer** (2 refs tech) |
| `[[Rafael Rafailov]]` | fine-tuning-alignment | Créer |
| `[[Amanda Askell — Prompt Engineering & Custom Instructions]]` | Karpathy Dev Discipline | Rediriger vers `[[amanda-askell-prompt-engineering]]` |

## Cat. 3 — Features CC sans note dédiée (15 liens)

Impact : MOC-Claude-Code a 15 liens morts. Action : créer les notes features ou supprimer les liens.

| Lien orphelin | Référencé dans | Priorité |
|---------------|---------------|----------|
| `[[Cowork]]` | MOC-Industrie, 7 autres notes | **Haute** — Cowork GA existe, créer alias ou redirect |
| `[[Effort Levels]]` | MOC-CC, MOC-Tech, Opus 4.7, 2 autres | **Haute** — 5 refs |
| `[[Plugin Marketplace]]` | MOC-CC, setup-complet, analyse-plugin | **Moyenne** — 3 refs |
| `[[Agent Teams]]` | MOC-CC, changelog, Lydia Hallie | Moyenne |
| `[[Dispatch]]` | MOC-Industrie, Computer Use, Cowork GA | Moyenne |
| `[[Auto Mode]]` | MOC-CC, 2 changelogs | Basse |
| `[[Context Management]]` | MOC-CC, Workflow Boris | Basse |
| `[[Dynamic Loop]]` | MOC-CC | Basse |
| `[[Fleet Commander]]` | MOC-Techniques | Basse |
| `[[Hooks System]]` | MOC-CC | Basse |
| `[[Remote Control]]` | MOC-CC | Basse |
| `[[Routines]]` | MOC-CC | Basse |
| `[[Session Sharing]]` | MOC-CC, Lydia Hallie | Basse |
| `[[Skills System]]` | MOC-CC | Basse |
| `[[Worktrees]]` | MOC-CC | Basse |

## Cat. 4 — Techniques sans note (16 liens)

Impact : MOCs techniques et notes de référence. Action : créer les notes atomiques ou supprimer les liens.

| Lien orphelin | Référencé dans | Priorité |
|---------------|---------------|----------|
| `[[rag-evaluation]]` | agents-evaluation, rag-architecture, rag-metadata, RAG | **Haute** — 4 refs |
| `[[rag-production]]` | rag-architecture, rag-metadata, RAG, Chip Huyen | **Haute** — 4 refs |
| `[[Best practices Boris Thariq]]` | setup-complet, pattern-vault-query-guard, 2 autres | **Haute** — alias vers `best-practices-claude-code-leaders` ? |
| `[[System Prompt Design]]` | MOC-Techniques, forge-prompt-machine | Moyenne |
| `[[Skills Best Practices]]` | MOC-CC, Thariq Shihipar | Moyenne |
| `[[CLAUDE.md Best Practices]]` | MOC-CC | Basse — alias vers `claudemd-maintenance` ? |
| `[[Context Management]]` | MOC-CC, Workflow Boris | Basse |
| `[[Description Trigger Pattern]]` | MOC-Prompts | Basse |
| `[[Document and Clear]]` | MOC-Techniques | Basse |
| `[[Drive-By Refactoring]]` | MOC-Techniques | Basse |
| `[[Knowledge-First Routing]]` | MOC-Techniques | Basse |
| `[[Over-Engineering]]` | MOC-Techniques | Basse |
| `[[Prompt vs Skill vs Rule]]` | MOC-Prompts | Basse |
| `[[Silent Assumptions]]` | MOC-Techniques, Karpathy | Basse |
| `[[Skills as Composability]]` | MOC-Techniques | Basse |
| `[[System Prompt Gemini CLI]]` | MOC-Prompts | Basse |

## Cat. 5 — Industrie sans note (19 liens)

Impact : MOC-Industrie principalement. Action : supprimer les liens (événements périmés) ou créer si encore pertinent.

| Lien orphelin | Référencé dans | Action |
|---------------|---------------|--------|
| `[[Piebald-AI System Prompts]]` | MOC-Industrie, Context Engineering, System Prompt CC | **Créer** (3 refs dont technique) |
| `[[Project Glasswing]]` | MOC-Industrie, Claude Security | **Créer** (2 refs) |
| `[[Stanford AI Index 2026]]` | MOC-Industrie, Anthropic Revenue | Créer ou supprimer |
| `[[Convergence AI Coding]]` | MOC-Industrie, Agent Skills Spec | Créer ou supprimer |
| `[[Bun Acquisition]]` | MOC-Industrie | Supprimer lien (événement) |
| `[[Cache TTL Controversy]]` | MOC-Industrie | Supprimer lien |
| `[[CC Pro Plan Test]]` | MOC-Industrie | Supprimer lien |
| `[[CC Quality Postmortem]]` | MOC-Industrie | Supprimer lien |
| `[[Codex For Everything]]` | MOC-Industrie | Supprimer lien |
| `[[Codex GPT-5.3]]` | MOC-Industrie | Supprimer lien (obsolète) |
| `[[Copilot Cloud Agent]]` | MOC-Industrie | Supprimer lien |
| `[[Copilot Usage-Based Billing]]` | MOC-Industrie | Supprimer lien |
| `[[Gemini CLI Updates]]` | MOC-Industrie | Supprimer lien |
| `[[Gemini CLI v0.37]]` | MOC-Industrie | Supprimer lien |
| `[[Google Invest 40B Anthropic]]` | MOC-Industrie | Supprimer lien |
| `[[LangChain LangGraph 1.0]]` | MOC-Industrie | Supprimer lien |
| `[[Leak Code Source CC]]` | MOC-Industrie | Supprimer lien |
| `[[OpenAI Revenue 25B]]` | MOC-Industrie, Sam Altman | Supprimer lien |
| `[[Panne 15 avril 2026]]` | MOC-Industrie | Supprimer lien |

## Cat. 6 — Erreurs supprimées (3 liens)

Impact : notes Knowledge qui pointent vers des erreurs supprimées. Action : supprimer les liens.

| Lien orphelin | Référencé dans | Action |
|---------------|---------------|--------|
| `[[erreur-creation-sans-vault-query]]` | erreur-marker-ttl-blocage-agents | Supprimer le lien |
| `[[erreur-pipeline-advisory-sans-hooks]]` | MOC-Techniques, erreur-marker-ttl | Supprimer les liens |
| `[[erreur-skip-checklist-skill-modification]]` | pattern-vault-query-guard | Supprimer le lien |

## Cat. 7 — Autres (5 liens)

| Lien orphelin | Référencé dans | Action |
|---------------|---------------|--------|
| `[[cc-news]]` | erreur-skill-monolithique | Ajouter alias à une note existante |
| `[[Claude Desktop]]` | claude-desktop-preferences | Créer ou alias |
| `[[ColPali]]` | jina-embeddings-v4 | Créer (technique RAG) |
| `[[Cursor 3]]` | MOC-Industrie | Supprimer (n'existe pas encore) |
| `[[Cursor v3.2]]` | MOC-Industrie | Supprimer |
| `[[Web Search GA]]` | MOC-Industrie | Supprimer lien |

## Synthèse par MOC

| MOC | Liens orphelins | Action principale |
|-----|----------------|-------------------|
| **MOC-Modeles** | 7 | Nettoyer tout (modèles fictifs) |
| **MOC-Industrie** | ~22 | Purge massive liens événements non documentés |
| **MOC-Claude-Code** | ~12 | Créer notes features ou supprimer |
| **MOC-Techniques** | ~10 | Créer notes atomiques ou supprimer |
| **MOC-Leaders** | ~8 | Créer fiches leaders manquants |
| **MOC-Prompts** | 3 | Créer ou supprimer |

## Résolutions rapides (aliases à ajouter)

Ces orphelins peuvent être résolus en ajoutant un alias à une note existante :
- `[[Best practices Boris Thariq]]` → alias dans `best-practices-claude-code-leaders.md`
- `[[CLAUDE.md Best Practices]]` → alias dans `claudemd-maintenance.md`
- `[[Cowork]]` → alias dans `Cowork GA.md`
- `[[Codex GPT-5.3]]` → alias dans `OpenAI Codex.md`
- `[[Amanda Askell — Prompt Engineering & Custom Instructions]]` → alias dans `amanda-askell-prompt-engineering.md`

## Liens

- [[plan-restructuration-vault]]
- [[MOC-Modeles]]
- [[MOC-Industrie]]
- [[MOC-Claude-Code]]
- [[MOC-Techniques]]
