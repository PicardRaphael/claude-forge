---
titre: "Audit gap vault forge-brain vs pattern Karpathy strict"
resume: "Audit READ-ONLY gap analysis du vault forge-brain (320 notes) contre spec Karpathy Gist 4 avril 2026 — 3 layers raw/wiki/schema, 3 ops Ingest/Query/Lint, 2 fichiers obligatoires index.md+log.md."
aliases:
  - "audit gap vault karpathy"
  - "gap analysis forge-brain"
  - "audit karpathy strict"
  - "audit vault 22 mai"
derniere-maj: 2026-05-22
auteur: claude
type: audit
tags:
  - "#type/audit"
  - "#domaine/vault"
  - "#sujet/karpathy"
---

# Audit gap vault forge-brain vs pattern Karpathy strict

> Audit READ-ONLY. Source spec : `04-Techniques/claude-code/pattern-vault-llm-karpathy.md` (Gist Karpathy 4 avril 2026).
> Stats vault : 320 notes, 137 tags, 1733 wikilinks, 1874 aliases.

---

## Section 1 — Layers Karpathy (raw / wiki / schema)

**Spec** : 3 layers stricts. `raw/` = immuable, jamais touché par LLM. `wiki/` = LLM-owned. `CLAUDE.md` ou `AGENTS.md` = schema.

**État actuel forge-brain** :

| Layer | Existe ? | Constat |
|-------|----------|---------|
| `raw/` séparé | **NON** | Aucun dossier dédié aux sources immuables |
| `wiki/` (LLM-owned) | Implicite | Tout le vault est traité comme LLM-owned (00-Hub à 07-Prompts, Knowledge, 0-Inbox, 1-Projets, 2-Casquettes) |
| Schema (CLAUDE.md/AGENTS.md) | Partiel | `CLAUDE.md` racine repo + rules `.claude/rules/forge-brain-proactive.md`. **Pas de schema versionné dans le vault lui-même** |

**Gaps concrets** :
- Les **rapports de recherche** `0-Inbox/_chantier-22mai/recherche-*.md` (sources externes Karpathy, YouTube, X) sont mélangés avec les notes LLM-owned (synthèses, audits) dans le même dossier `0-Inbox/_chantier-22mai/`. Aucune séparation source brute vs production LLM.
- Aucun transcript Whisper / web clip Defuddle archivé séparément. Les recherches sont déjà digérées en notes.
- Le dossier `0-Inbox/` est ontologiquement une "capture rapide à trier", pas un `raw/` immuable Karpathy.
- Aucun dossier `references/` ou `sources/` détaché.

**Verdict** : pas de layer 1 (`raw/`). Violation potentielle d'immutabilité quand le LLM édite un rapport de recherche déjà capitalisé.

---

## Section 2 — Fichiers obligatoires (index.md + log.md)

**Spec Karpathy** :
- `index.md` content-oriented (orientation LLM, lu en premier, PAS sommaire généré)
- `log.md` append-only, format strict `## [YYYY-MM-DD] action | titre`

**État actuel** :

| Fichier | Existe ? | Conformité |
|---------|----------|------------|
| `index.md` racine vault | **NON** | Aucun fichier `index.md` |
| `00-Hub/Home.md` (proxy) | OUI | **Partiellement content-oriented** : 7 lignes navigation par MOCs (table dossier→contenu), pas d'orientation par concepts/erreurs. C'est un **sommaire de dossiers**, pas un index Karpathy |
| `00-Hub/MOC-*.md` | OUI (7 MOCs) | Sommaire généré par catégorie (Claude-Code, Concurrents, Modeles, Techniques, Leaders, Industrie, Prompts). Karpathy demande UN index unique content-oriented, pas 7 sommaires fragmentés |
| `log.md` append-only | **NON** | Aucun fichier `log.md` au format Karpathy |
| `CHANGELOG.md` racine vault | OUI | **Format NON conforme** : narratif markdown sections `## YYYY-MM-DD — résumé`, pas `## [YYYY-MM-DD] action \| titre`. Pas d'action atomique par entrée. Mélange ajouts/modifs/leaders/source en blocs |

**Gaps concrets** :
- `Home.md` (7 MOCs nav) ≠ index.md content-oriented. Un LLM cherchant "comment écrire un CLAUDE.md" doit traverser Home → MOC-Claude-Code → note canonique = 3 sauts au lieu de 1.
- `CHANGELOG.md` existe mais format hybride. Verbatim Karpathy strict = `## [YYYY-MM-DD] action | titre` + liens, append-only. Actuel = paragraphes narratifs avec sections "Ajoutées / Modifiées / Source".
- Aucune trace append-only des opérations Lint / Ingest / Query.

**Verdict** : 0/2 fichiers obligatoires au format strict. `Home.md` et `CHANGELOG.md` sont des proxies partiels mais non-conformes.

---

## Section 3 — Schema (CLAUDE.md / AGENTS.md)

**Spec** : schema partagé humain↔LLM. Conventions, règles d'écriture, boundaries.

**État actuel** :
- `CLAUDE.md` racine repo (claude-forge) : oui, mais c'est le schema du **REPO**, pas du **vault**. Couvre projet entier (Jarvis, MCP, agents).
- `.claude/rules/forge-brain-proactive.md` : couvre conventions vault (frontmatter, dossiers, qualité). C'est le **schema vault de facto**, mais externalisé hors vault.
- `.claude/rules/vault-consultation-protocol.md` : protocole consultation.
- Pas de `AGENTS.md` (alternative cross-LLM évoquée par Hashimoto).
- Pas de `vault/claude-forge/CLAUDE.md` ou `vault/claude-forge/SCHEMA.md` dans le vault lui-même.

**Gap** : le schema vault vit dans `.claude/rules/`, pas dans le vault. Un agent qui n'a pas accès aux rules forge (ex. exécuté ailleurs) ne trouve pas les conventions. Karpathy place le schema **au même niveau** que le wiki.

---

## Section 4 — Opérations Karpathy (Ingest / Query / Lint)

| Op | État | Tooling |
|----|------|---------|
| **Ingest** | OUI | cc-news + skill `defuddle` + skill `watch` (Whisper) + skill `x-read` + `forge-brain-proactive.md` rule "capitaliser après recherche web" |
| **Query** | OUI excellent | MCP forge-brain (11 outils, FTS5, alias expansion, content-hash, port 8091) — dépasse Karpathy minimal |
| **Lint** | Partiel | Agent `vault-maintainer.md` + skill `vault-audit/` existent, mais **pas d'invocation périodique** (pas de `/loop` ou `/schedule` documenté pour Lint vault). `/forge-review` existe pour audit mensuel forge global mais pas dédié vault |

**Gap** : Lint existe en outillage mais pas en cadence. Pas de garantie d'exécution périodique. Aucun fichier `log.md` ne traceraient les passes de lint si elles existaient.

---

## Section 5 — Conventions notes (échantillon)

**Standard forge** (`forge-brain-proactive.md`) : 4-6 aliases, resume spécifique, derniere-maj ISO, 2+ tags, 2+ wikilinks.

**Échantillon 4 notes lues** :

| Note | Aliases | Resume | derniere-maj | Tags | Wikilinks | Verdict |
|------|---------|--------|--------------|------|-----------|---------|
| `pattern-vault-llm-karpathy.md` | 10 | spécifique | 2026-05-22 | 4 | 15+ | **OK** |
| `00-Hub/Home.md` | 6 | générique | 2026-05-08 | 1 | 7 MOCs | **Partiel** (resume générique "Point d'entrée") |
| `MOC-Claude-Code.md` | 5 | spécifique | 2026-05-22 | 2 | 20+ | **OK** |
| `angela-jiang.md` (leader) | 6 | spécifique | 2026-05-22 | 2 | (non lu détail) | **OK** |
| `erreur-advisory-rules-insuffisantes.md` | 6 | spécifique | 2026-05-10 | 4 | (non lu détail) | **OK** |
| `recherche-karpathy-vault-canonique.md` | 4 | spécifique | 2026-05-22 | 2 | (rapport recherche) | **OK** seuil bas (4 = minimum) |

**Stats macro** (vault_stats) : 1874 aliases / 320 notes = **5.85 aliases/note moyen** → au-dessus du minimum 4-6 forge. **Conforme**.

Pas de gap majeur sur conventions notes. Quelques resumes génériques (Home.md) à durcir mais c'est marginal.

---

## Section 6 — Verdict global

| # | Gap | Priorité | Effort | Action proposée |
|---|-----|----------|--------|-----------------|
| 1 | **Pas de `raw/` immuable** — sources externes mélangées au LLM-owned | **P0** | M | Créer `raw/` au racine vault, déplacer transcripts/clips/captures Whisper/Defuddle. Règle "LLM ne touche jamais raw/" |
| 2 | **Pas de `index.md` content-oriented** racine vault — Home.md est sommaire MOCs | **P0** | S | Créer `vault/claude-forge/index.md` orienté concepts/erreurs/canoniques (pas dossiers). Home.md conservé comme nav Obsidian |
| 3 | **Pas de `log.md` append-only** au format Karpathy strict | **P0** | S | Créer `log.md` racine vault. Format `## [YYYY-MM-DD] action \| titre`. Migrer trace CHANGELOG progressivement, ou garder les deux (CHANGELOG narratif humain + log.md atomique LLM) |
| 4 | **Schema vault hors vault** (vit dans `.claude/rules/`) | **P1** | S | Créer `vault/claude-forge/SCHEMA.md` ou `AGENTS.md` dans le vault, miroir de `forge-brain-proactive.md`. Le vault devient self-describing |
| 5 | **Rapports recherche** `_chantier-22mai/` non séparés sources/synthèses | **P1** | M | Restructurer : `_chantier-22mai/raw/` (sources externes) vs `_chantier-22mai/synthese/` (production LLM). Ou déplacer définitivement raw → `raw/chantier-22mai/` |
| 6 | **Lint pas périodique** — vault-maintainer existe mais pas cadencé | **P1** | S | `/schedule` mensuel ou `/loop` weekly de `vault-maintainer`. Output dans `log.md` |
| 7 | **CHANGELOG.md format non strict Karpathy** | **P2** | S | Optionnel : garder format actuel + ajouter `log.md` strict en parallèle (humain vs LLM). Ou migrer 1x complet |
| 8 | **7 MOCs fragmentés** vs 1 index Karpathy | **P2** | M | Conserver MOCs (vue Obsidian), mais `index.md` Karpathy doit avoir liste plate des canoniques + erreurs + concepts top |
| 9 | **`Home.md` resume générique** | **P2** | XS | Resume spécifique mentionnant 320 notes / canoniques / Karpathy |

**Synthèse priorisation** :
- **P0 (critique, à faire avant prochain cycle)** : 3 gaps (raw/, index.md, log.md). Effort total : ~M.
- **P1 (équilibré)** : 3 gaps (schema in-vault, restruct chantier, lint cadencé). Effort total : ~M-L.
- **P2 (nice-to-have)** : 3 gaps cosmétiques.

**Conformité actuelle vs Karpathy strict** : **~40%**. Forces : layer 2 wiki excellent (320 notes, 5.85 aliases moyen, MCP custom 4 forces uniques), opérations Ingest+Query au top, schema documenté (mais externalisé). Faiblesses : pas de `raw/`, pas de `index.md` strict, pas de `log.md` append-only, schema hors vault.

**Réserve** : forge dépasse Karpathy minimal sur certains axes (aliases, MCP custom, agents dédiés). Les 3 gaps P0 sont ceux qui empêcheraient un agent externe de comprendre le vault selon le contrat Karpathy public.
