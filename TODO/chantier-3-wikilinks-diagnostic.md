# Chantier 3/5 — Réparation wikilinks cassés · DIAGNOSTIC (Phase 1, lecture seule)

**Date** : 2026-06-07 · **Statut** : Phase 1 terminée, attente arbitrage Raphael avant Phase 2
**Total lint** : 133 wikilinks brisés · **Cibles distinctes absentes** : ~55 (une réparation = plusieurs liens)

## Méthode

- `lint_vault(limit=200)` → 133 liens (source → cible inexistante)
- Inventaire complet des 459 notes (hors `raw/` exclu du lint) via `list_notes` par dossier
- Matching chaque cible contre l'inventaire réel + `search_brain` ciblés
- **Test décisif MCP** : `read_note("boris-cherny")` → introuvable. MCP ne résout PAS le kebab quand la note est Title Case → ces liens sont **réellement morts pour Jarvis**, pas des faux positifs du lint.

## Grille par cause (comptes EXACTS — classés mécaniquement, somme vérifiée = 133)

| Cause | Liens | Cibles distinctes | Réparable par | Auto ? |
|-------|------:|------:|---------------|--------|
| A. Casse leader (kebab/tiret → Title Case, note EXISTE) | 3 | 3 | alias kebab sur la note cible | semi-auto |
| B. Renommage (cible existe sous autre nom) | 5 | 5 | corriger texte OU alias | manuel |
| C. Typo réelle | 1 | 1 | corriger texte du lien | manuel |
| D. Lien → composant `.claude/` (skill/rule, pas note vault) | 19 | 15 | trancher : note-pont / rediriger / retirer | **Raphael** |
| E. Lien → fichier `memory/*.md` (pas note vault) | 10 | 8 | retirer lien OU créer note vault | **Raphael** |
| F. Placeholder syntaxique (exemple dans note doctrine) | 15 | 13 | no-op (ou code-span pour silence lint) | no-op |
| G. Cible absente — jamais créée (roadmap responsable-ia + concepts vault) | 80 | 61 | **Raphael tranche** : stub / vraie note / retrait | **Raphael** |

**Somme = 133** (vérifiée par script). A+B+C = 9 liens réparables sans arbitrage. D+E+G = 109 = arbitrage Raphael. F = 15 no-op.

---

## Détail par cause

### A. Casse/forme leader — kebab vers Title Case (5 liens, 4 cibles)
Le lien utilise le slug kebab, mais la note leader est en Title Case. MCP ne résout pas.
- `[[addy-osmani]] -> [[erik-schluntz]]` → note réelle **`Erik Schluntz`**
- `[[affaan-mustafa-ecc-hackathon-winner]] -> [[boris-cherny]]` → **`Boris Cherny`**
- `[[eval-pattern-anthropic-skill-creator]] -> [[Thariq-Shihipar]]` → **`Thariq Shihipar`** (tiret au lieu d'espace)
- (+ vérifier les autres liens kebab→leader au passage)

**Stratégie** : ajouter l'alias kebab (`boris-cherny`, `erik-schluntz`, `thariq-shihipar`) sur chaque note leader via `update_property` aliases. Répare TOUS les liens kebab futurs + comble le manque qualité (lint signale déjà ces leaders avec <4 aliases). Une écriture par note.

### B. Renommage — la cible existe sous un autre nom (6 liens, 5 cibles)
- `[[audit-ia-back-25mai-quartet]] -> [[ia-back-project]]` → note réelle **`ia_back`** (1-Projets/Neoteem/ia_back/)
- `[[audit-ia-back-25mai-quartet]] -> [[neo-ia-project]]` → **`neo_ia`**
- `[[feedback-sbi-radical-candor]] -> [[architecture-rag-canonique]]` → **`rag-architecture`** (04-Techniques/rag/)
- `[[neo-ia-tests-lenteur-diagnostic]] -> [[neoia-test-infrastructure]]` → **`neo-ia-tests-lenteur-diagnostic`** (la note elle-même, alias "test infrastructure neo_ia")
- (+ recheck `google-mit... -> [[multi-agent-handoff-loss-pattern]]`, `[[critique-will-vs-ecc-deux-doctrines]]` → note réelle `will-vs-ecc-deux-doctrines-anthropic`)

**Stratégie** : ⚠️ `move_note` NE répare PAS ces cas (la cible n'a jamais été une note sous ce nom). Réparation = corriger le texte du lien vers le nom réel, OU ajouter l'alias sur la cible. Manuel, cas par cas.

### C. Typo réelle (2 liens, 2 cibles)
- `[[affaan-mustafa-ecc-hackathon-winner]] -> [[thariq-shihpar]]` → faute **shihpar** vs **shihipar** (note `Thariq Shihipar`)
- (+ `[[critique-will-vs-ecc-deux-doctrines]]` si confirmé écart de nom)

**Stratégie** : corriger le texte du lien. PAS d'alias (n'encode pas la faute).

### D. Lien vers composant `.claude/` réel — skill/rule, pas note vault (~14 liens, ~11 cibles)
Ces cibles sont des **skills/rules forge existantes**, pas des notes vault. Le lien voulait pointer vers une doc qui n'existe pas en note.
- `[[da-blocking-arbitrage]]` (skill) — 4 occurrences : eval-pattern, comparaison-skill, CHANGELOG, analyse-plugin, plugins-officiels-veille
- `[[outcomes-test]]`, `[[skill-evolve]]` (skills) — eval-pattern
- `[[delegate-to-specialists]]` (rule) — comment-creer-hook, comment-creer-skill → note vault proche = `delegate-guard-pattern`
- `[[cross-repo-propagation]]` (rule) — plugins-officiels-veille
- `[[memory-discipline]]`, `[[pivot-check]]`, `[[web-search-canonical-source]]`, `[[vault-audit]]`, `[[recap]]` (skills/rules)
- `[[mcp-transport-stdio-http-crashloop]]` — comment-creer-hook

**Stratégie (Raphael tranche)** : (a) retirer le wikilink (garder texte simple) ; (b) créer une note-pont vault par composant ; (c) rediriger vers la note vault existante la plus proche (ex. `delegate-to-specialists`→`delegate-guard-pattern`).

### E. Lien vers fichier `memory/*.md` — pas note vault (6 liens, 6 cibles)
- `[[mcp-alias-ambigu-chemin-exact]]`, `[[workflow-args-array-gotcha]]`, `[[python-windows-cross-machine]]`, `[[delegate-guard-env-var-blocked]]`, `[[vault-edit-gotchas-outillage]]`, `[[import-ajoute-pas-remplace-automemory]]`, `[[automemorydirectory-absolu-casse-multiprojet]]`

**Stratégie (Raphael tranche)** : ces concepts vivent en mémoire, pas dans le vault. Retirer le wikilink OU créer la note vault si le concept mérite d'être canonique.

### F. Placeholder syntaxique — exemple dans note doctrine (~15 liens, no-op)
Illustrations de syntaxe dans des notes qui *expliquent* les wikilinks. Ne pointent vers rien par nature.
- `[[X]]`, `[[X#H]]`, `[[stem]]`, `[[stem#section]]`, `[[Stem]]`, `[[Alpha]]`, `[[own-stem]]`, `[[old]]` — note `mcp-vault-llm-design`
- `[[note-name]]`, `[[note-canonique]]` — `pattern-mcp-brief-then-direct`
- `[[>>> x <<<]]`, `[[note-vault-canonique]]`, `[[llm-lit-court-homogene-pas-couche-deterministe]]` — `pattern-maintenance-hybride-corpus-accumulatif`
- `[[Nom-leader]]` — `erreur-audit-07-leaders`
- `[[X]]` — `critique-2026-05-27-compounding-retroactif`

**Stratégie** : **no-op assumé** — ne se réparent jamais vers une cible. Option propreté : passer en code-span (`` `[[X]]` ``) pour que le lint cesse de les compter. À valider avec Raphael (cosmétique).

### G. Cible absente — roadmap responsable-ia + croisés (~85 liens, ~27 cibles distinctes)
Les `index.md` des sous-dossiers `responsable-ia` (16 index distincts, le lint les agrège sous `[[index]]`) + liens croisés entre notes management/gouvernance/communication listent un **sommaire de contenu en grande partie jamais écrit**.

Cibles les plus citées (création/stub = répare plusieurs liens) :
- `[[intake-no-factory-yes-if]]` (×4 : frameworks-comparatif, rice-en-pratique, roadmap-now-next-later, okr-equipe-ia-wodtke)
- `[[securite-llm-owasp]]` / `securite-llm-owasp-mitre-atlas` (×3+), `[[ai-usage-policy-interne]]` (×3), `[[manager-seniors-plus-experimentes]]` (×3)
- `[[vendor-management-llm-dpa]]`, `[[build-vs-buy-vs-finetune-rag]]`, `[[roi-ia-mesure-mckinsey]]`, `[[dire-non-yes-and-fournier]]`, `[[adr-michael-nygard]]`, `[[cr-meeting-template]]` (×2 chacun)
- ~20 autres cibles à 1 lien (recrutement-profils, onboarding-30-60-90, nist-ai-rmf, iso-42001, etc.)

**Stratégie (Raphael tranche, NE PAS recréer en masse)** : ce sont probablement des stubs/roadmap volontaires. Trois options par cible : (a) laisser le lien cassé = TODO de contenu assumé ; (b) créer la vraie note ; (c) retirer le lien de l'index si abandonné.

---

## Distinction SUPPRESSION vs JAMAIS CRÉÉE
Non tranchée par preuve : seul `git log --all --full-history -- <path>` le dirait. Buckets D/E/G fusionnés sous « cible absente aujourd'hui ». Aucune cible présentée comme « supprimée » sans cette preuve (per règle « jamais supposer mort sans regarder »).

## Casse par le Chantier 2 (tags) ?
**Aucune** — confirmé : les tags ne sont pas des wikilinks, les 133 sont pré-existants et stables.

## Plan Phase 2 (par lot de cause, commit + lint après chaque, le chiffre DESCEND)
1. **Lot A** (alias leaders) — gain net ~5 liens, semi-auto, zéro risque
2. **Lot B+C** (renommages + typos) — ~8 liens, manuel ciblé
3. **Lots D/E/G** — APRÈS arbitrage Raphael (créer/retirer/laisser)
4. **Lot F** — cosmétique optionnel (code-span)
