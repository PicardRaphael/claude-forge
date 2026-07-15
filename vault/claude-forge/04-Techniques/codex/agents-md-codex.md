---
titre: "AGENTS.md — le fichier d'instructions projet de Codex"
resume: "Note canonique forge — AGENTS.md, l'équivalent CLAUDE.md côté OpenAI Codex : cap 32 KiB (project_doc_max_bytes), nesting racine→CWD, AGENTS.override.md, global ~/.codex/AGENTS.md, concaténation root-first, § Review guidelines pour la review PR. Vérifié doc officielle au 15 juil. 2026."
aliases:
  - "AGENTS.md"
  - "agents md codex"
  - "agents.md nesting"
  - "project_doc_max_bytes"
  - "AGENTS.override.md"
  - "instructions projet codex"
  - "equivalent claude.md codex"
derniere-maj: 2026-07-15
auteur: claude
type: technique
sources:
  - "https://learn.chatgpt.com/docs/agent-configuration/agents-md"
  - "https://github.com/openai/codex"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#doctrine/2026"
---
# AGENTS.md — le fichier d'instructions projet de Codex

> Note canonique forge — `AGENTS.md` est à Codex ce que `CLAUDE.md` est à Claude Code : les conventions durables du repo, lues avant tout travail. Vérifié sur `learn.chatgpt.com/docs/agent-configuration/agents-md` au **15 juil. 2026** (pages non datées → datation par les versions citées). Mécanismes propres à Codex — ne pas présumer l'identité avec CLAUDE.md.

---

## QUOI

`AGENTS.md` = fichier markdown de conventions repo (commandes, étapes de vérification, attentes de review). Codex le lit « before doing any work ». Standard de nom `AGENTS.md` : spec collective cross-LLM (OpenAI/Google/Cursor, août 2025), pas un format propriétaire.

---

## COMMENT

### Cap de taille — 32 KiB via `project_doc_max_bytes` (CERTAIN)

> Verbatim : « Codex skips empty files and stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default). »

- La limite porte sur la **taille COMBINÉE de tous les AGENTS.md agrégés**, pas un fichier isolé.
- Configurable :
```toml
project_doc_max_bytes = 65536
```
- *Nuance* : le chiffre 32 KiB n'est sourcé que par la page AGENTS.md de `learn.chatgpt.com` (absent du `config.md` du repo, devenu stub). Une seule source primaire officielle → CERTAIN sur le principe, chiffre à re-tester (`codex doctor`) pour blindage.

### Nesting + override (CERTAIN)

- Codex agrège les `AGENTS.md` **de la racine Git jusqu'au répertoire courant**, un fichier par dossier.
- Concaténation **root-first** : « Codex concatenates files from the root down, joining them with blank lines. »
- **Override** : « Files closer to your current directory override earlier guidance because they appear later in the combined prompt. » Le plus proche du CWD gagne (par position dans le prompt combiné).
- **`AGENTS.override.md`** : dans un dossier, un `.override.md` **remplace** le `AGENTS.md` frère (il ne s'y ajoute pas).

Exemple d'arborescence :
```
AGENTS.md                                  # racine, actif
services/payments/AGENTS.md                # ignoré (override présent)
services/payments/AGENTS.override.md       # actif pour ce sous-arbre
services/search/AGENTS.md                  # actif pour ce sous-arbre
```

### Chargement global + projet (CERTAIN)

- **Global** : `~/.codex/AGENTS.md` (et `~/.codex/AGENTS.override.md` prioritaire) — existe et s'applique à tous les projets.
- **Projet** : walk du Git root vers le CWD.
- Ordre de merge : global → projet (racine → bas). *Probable* sur l'ordre exact global-avant-projet.

### Section Review guidelines (CERTAIN)

Pour la review de PR (`@codex review`), Codex lit une section `## Review guidelines` dans **l'`AGENTS.md` le plus proche de chaque fichier modifié** et ne flag que P0/P1. C'est le point d'ancrage pour customiser la review par sous-dossier.

### Structure recommandée

Pas de schéma imposé. En-têtes libres (exemples doc : `## Working agreements`, `## Repository expectations`, `## Payments service rules`, `## Review guidelines`).

---

## QUAND

- **AGENTS.md** = conventions durables, commandes, standards, review. Ce qui doit persister entre sessions.
- **PAS** le how-to procédural → skill ([[comment-creer-skill-codex]]).
- **PAS** l'enforcement 100 % → hook ([[comment-creer-hook-codex]]).
- **PAS** les réglages machine (modèle, sandbox, MCP) → config.toml ([[config-toml-profils-codex]]).

Position dans la Surface Map (cf [[workflow-codex-optimal]]) : `prompt → AGENTS.md → config.toml → skills → ...`. AGENTS.md est le premier levier de configuration au-dessus du prompt.

---

## ANTI-PATTERNS

- ❌ **Kitchen sink AGENTS.md** — cap 32 KiB combiné ; au-delà, les fichiers suivants sont ignorés silencieusement.
- ❌ **Mettre du how-to dans AGENTS.md** — le procédural va en skill (progressive disclosure), AGENTS.md est toujours chargé.
- ❌ **Croire qu'un `AGENTS.override.md` s'ajoute au `.md` frère** — il le remplace.
- ❌ **Mécanisme de MAJ auto pour capitaliser des learnings** — n'existe PAS : AGENTS.md se met à jour manuellement (ou via une scheduled task qui l'édite). Le compounding auto passe par `[memories]` (cf [[loop-apprentissage-codex]]).
- ❌ **Présumer l'identité avec CLAUDE.md** — la doc OpenAI ne fait aucune comparaison ; nesting/override/cap sont des mécanismes Codex spécifiques.

---

## SOURCES

- `learn.chatgpt.com/docs/agent-configuration/agents-md` (doc officielle, non datée — 15/07/2026).
- Comparaison AGENTS.md ↔ CLAUDE.md : **absente des docs OpenAI** — ne pas affirmer d'équivalence de mécanisme.

---

## WIKILINKS

- [[workflow-codex-optimal]] — note maître (Surface Map)
- [[config-toml-profils-codex]] — les réglages machine (frère de AGENTS.md)
- [[comment-creer-skill-codex]] — le how-to
- [[comment-creer-hook-codex]] — l'enforcement
- [[loop-apprentissage-codex]] — pourquoi AGENTS.md ne se met pas à jour seul ([memories])
- [[comment-ecrire-claudemd]] — l'équivalent Claude Code (miroir, pas identité)
