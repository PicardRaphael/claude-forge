---
titre: "HTML > Markdown pour plans et specs — doctrine Thariq Shihipar (Anthropic) mai 2026"
resume: "Thariq Shihipar (Engineering Lead Claude Code, Anthropic) démontre empiriquement que HTML bat Markdown 17/20 pour plans/specs/design — scrollable, visuel, mockups intégrés, micro-apps jetables, design systems vivants"
aliases:
  - "html vs markdown"
  - "thariq html plans"
  - "html for specs"
  - "html unreasonable effectiveness"
  - "design system html"
  - "micro app html plan"
  - "html doctrine anthropic"
derniere-maj: 2026-05-24
auteur: claude
type: technique
sources:
  - "https://thariqs.github.io/html-effectiveness — 20 exemples Thariq"
  - "https://simonwillison.net/2026/May/8/unreasonable-effectiveness-of-html/ — Analyse Simon Willison"
  - "https://www.lennysnewsletter.com/p/how-i-ai-html-is-the-new-markdown — Podcast Lenny's Newsletter"
  - "https://www.chatprd.ai/how-i-ai/claude-code-anthropic-thariq-shihipar-on-replacing-markdown-with-html — ChatPRD interview"
  - "Code with Claude SF mai 2026 — Thariq talk"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#doctrine/2026"
  - "#domaine/specs"
---

# HTML > Markdown — doctrine Thariq Shihipar (Anthropic Engineering Lead Claude Code)

## QUOI

Thariq Shihipar (Engineering Lead Claude Code, Anthropic) publie 8 mai 2026 sur X : *"Using Claude Code: The Unreasonable Effectiveness of HTML"*. 4.4M vues en 16h, 8200 likes. Démontre empiriquement que **HTML bat Markdown 17/20** pour plans/specs/design quand le human lit la sortie.

> "HTML has become the superior format for communicating with AI agents, replacing Markdown for planning and specs. While Markdown was popular because it's both human- and machine-readable, HTML offers far richer expression — interactive elements, visual mockups, scrollable sections, and better information density."

Companion site : [thariqs.github.io/html-effectiveness](https://thariqs.github.io/html-effectiveness) — 20 exemples self-contained générés par Claude Code.

## POURQUOI

- **Markdown plat** : plan 1000 lignes = personne ne lit. Thariq lui-même : "I'd just ask Claude to edit the plan instead of reading it myself."
- **HTML riche** : scrollable, visuel, mockups intégrés, density d'information supérieure, codable interactif
- **Coût égal** : Claude génère HTML aussi vite que Markdown (token cost comparable)
- **Verdict empirique** : HTML gagne 17/20 head-to-head Markdown. Les 3 perdus = tâches où l'output reste internal au loop agent (jamais lu humain)

## COMMENT — 3 workflows Thariq

### 1. Plans visuels HTML au lieu de markdown plat

Au lieu de :
```markdown
- Feature A
  - Detail 1
  - Detail 2
- Feature B
```

Demander :
```
Plan this feature as an HTML file with one section per idea, each with:
- visual mockup
- description
- risk assessment
- estimated effort badge
```

Résultat : page HTML scrollable, sections cliquables, code highlight, mockups CSS, **lisible**.

### 2. Micro-apps jetables pour éditer parties du plan

Thariq : prendre une table d'un plan HTML, demander à Claude *"créé une UI gamifiée pour éditer cette section"*. Résultat : single-file HTML avec drag/drop, validation, export JSON. **Utilisé puis jeté**.

Verbatim : *"micro software on top of micro software approach means you can have the perfect tool for every specific problem, then discard it when you're done."*

### 3. Living design systems HTML

Au lieu de pointer Claude vers un Figma ou un GitHub repo, maintenir un **fichier HTML unique** représentant tout le design system : couleurs, typographies, espacements, composants. Travels with code, lisible humain + machine. Claude peut extraire un design system d'une codebase existante et l'encoder en HTML.

## QUAND — Critère d'application

### Utiliser HTML quand :
- ✅ Plan/spec destiné à être **lu par humain** (Raphael, équipe, stakeholder)
- ✅ Document **persistant** (TODO/feature-X/, ADR, design system)
- ✅ Besoin de **visuel** (mockup, diagramme, table riche, comparaison side-by-side)
- ✅ Document **interactif** souhaité (édition future, exploration, validation)
- ✅ Output **long** (>200 lignes) — Markdown plat devient illisible
- ✅ **Multi-section** avec navigation (table of contents scrollable)

### Garder Markdown quand :
- ❌ Output **interne au loop agent** (jamais lu humain — JSON, tool output)
- ❌ Document **court** (<50 lignes) — Markdown reste suffisant
- ❌ Fichier consommé par **autre LLM** sans humain dans la boucle
- ❌ Versionning git diff important (HTML diff = bruit visuel vs sémantique)
- ❌ Contexte **READMEs** projet (Markdown reste convention)

## Application à forge / Neoteem

### /spec extension : option `--format html`

Skill `/spec` peut produire :
- `SPEC.md` (Markdown — default, compatible git/IDE)
- `plan.html` (HTML — bonus pour features L/XL avec mockups)

Implémentation suggérée : ajout `--format html` ou `--rich` dans `$ARGUMENTS` → Phase 4 (génération) produit HTML interactif au lieu de Markdown plat.

### ADR / decisions

Fichiers `Knowledge/decisions/ADR-NNN-<topic>.html` au lieu de `.md` quand décision architecturale majeure mérite documentation visuelle (diagrammes, comparaisons).

### Design system Neoteem

Candidat évident : `lojii/docs/design-system.html` — composants Vuetify documentés avec exemples live (au lieu d'un Markdown plat). Mockups responsive intégrés.

## GOTCHAS

- ❌ **Tout HTML par défaut** = overkill. Garder Markdown pour fichiers courts/internes
- ❌ **HTML sans CSS inline** = moche. Always include `<style>` tag pour rendu autonome
- ❌ **HTML modifié manuellement** = perte du caractère "throwaway" Thariq. Préférer regénérer
- ❌ **Diff git HTML** = bruyant. Si versionnement critique → Markdown reste meilleur

## ANTI-PATTERNS

- **Convertir tout l'existant Markdown en HTML** : non. Convertir au cas par cas selon critère (lu humain ? long ? visuel ?)
- **HTML pour communication ChatPRD/Slack** : non. Convention Markdown reste pour collaboration humaine textuelle
- **Forcer HTML quand Markdown suffit** : Boris dit "thinnest wrapper" — pareil pour formats. Choisir le bon outil

## SOURCES

- **Thariq Shihipar** (Engineering Lead Claude Code, Anthropic) — [@trq212 sur X](https://x.com/trq212), [thariqs.github.io](https://thariqs.github.io)
- **Companion site 20 exemples** — [thariqs.github.io/html-effectiveness](https://thariqs.github.io/html-effectiveness)
- **Simon Willison analyse** — [simonwillison.net/2026/May/8/unreasonable-effectiveness-of-html/](https://simonwillison.net/2026/May/8/unreasonable-effectiveness-of-html/)
- **Lenny's Newsletter podcast** — [How I AI: HTML is the new Markdown](https://www.lennysnewsletter.com/p/how-i-ai-html-is-the-new-markdown)
- **ChatPRD interview** — [Thariq on Replacing Markdown with HTML](https://www.chatprd.ai/how-i-ai/claude-code-anthropic-thariq-shihipar-on-replacing-markdown-with-html)
- **YouTube Code with Claude SF** — [Why this Claude Code engineer uses HTML files as AI specs](https://www.youtube.com/watch?v=Qrpm7E80wQ0)

## WIKILINKS

- [[pattern-spec-driven-development]] — Pipeline /spec où HTML peut s'intégrer
- [[Thariq Shihipar]] — Fiche leader (à créer si absente)
- [[workflow-claude-code-optimal]] — Pipeline complet
- [[running-implementation-notes]] — Pattern Thariq compagnon (running notes)
- [[methode-analyser-repo]] — Analyse repo peut produire output HTML pour Raphael
