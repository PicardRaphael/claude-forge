---
titre: "Gotchas outillage écriture vault — delegate-guard faux positif + insert_section misparente"
resume: "Deux gotchas à l'écriture vault : (1) delegate-guard.py matche agents/*.md par nom → bloque les notes vault 04-Techniques/agents/*.md (utiliser MCP, pas Edit) ; (2) insert_section position=after insère après la LIGNE du header, pas la section → misparente (viser un marker précis en fin de section)."
aliases:
  - "vault edit gotchas"
  - "delegate-guard faux positif note vault"
  - "insert_section misparente header"
  - "écrire note vault agents"
  - "gotcha insert_section position after"
derniere-maj: 2026-06-07
auteur: claude
type: pattern
tags:
  - "#type/pattern"
  - "#domaine/mcp"
  - "#domaine/vault"
---

# Gotchas outillage écriture vault

> Deux gotchas liés à l'outillage d'écriture (pas au contenu), invisibles tant qu'on ne les a pas rencontrés, et qui re-mordent sur toute édition vault.

## 1. delegate-guard faux positif sur notes vault `agents-*.md`

Le hook `delegate-guard.py` matche `agents/*.md` **par nom de chemin**. Une note vault comme `04-Techniques/agents/agents-architecture.md` ou `04-Techniques/agents/google-mit-scaling-agent-systems-2025.md` se fait bloquer en Edit direct comme si c'était un sous-agent `.claude/agents/` — le segment `agents/` suffit à déclencher le pattern.

**Contournement légitime** : pour modifier le CONTENU d'une note vault bloquée par ce faux positif, utiliser les outils MCP forge-brain (`update_note`, `insert_section`, `append_note`) qui ne passent pas par le hook PreToolUse Edit. Les notes dont le chemin ne contient pas `agents/` (ex. `index.md`, `stack-*.md`) passent en Edit direct. Ne JAMAIS contourner par env var/script (cf [[delegate-guard-pattern]]).

## 2. `insert_section` misparente après un header de section nu

`insert_section(marker="## Section", position="after")` insère juste **après la LIGNE du header**, pas après la section entière. Si la section commence par `## Section` suivi directement d'une sous-section `###` ou d'une table, le contenu inséré se loge AVANT le corps existant → la table / le bloc d'origine se retrouve reparenté sous la dernière sous-section insérée.

**Réparation** : pour insérer en FIN de section, viser un marker **précis** (dernière phrase de la section, en gras si possible) plutôt que le header nu. Vérifier le placement avec `read_section(file, heading="## Section")` (le param s'appelle `heading` et DOIT commencer par `#`). Si déjà mal parenté : `update_note` (réécriture complète).

## 3. Edit DISQUE direct → index SQLite désynchronisé

Corriger une note vault via `Edit`/`Write` (au lieu des outils MCP) écrit bien le disque, mais ne réindexe PAS : la table `links`/`tags` du MCP reste sur l'ancien état. La réindexation n'arrive qu'au prochain tick du watcher (`poll_interval_seconds=30` dans config.yaml) — d'où un `lint_vault` qui montre encore un lien qu'on vient de corriger.

**Ne pas confondre** avec le lag d'agrégat (fluctuation non liée aux edits) : ici c'est l'écriture hors-MCP qui n'a pas déclenché `index_note`.

**Réparation** : si un Edit disque a déjà eu lieu, forcer la réindexation par un appel MCP sur la note (`update_property` sur `derniere-maj` suffit — il appelle `index_note`), ou attendre le poll 30s. → Toujours éditer le contenu d'une note vault via MCP (`update_note`/`update_property`/`insert_section`) qui réindexe atomiquement en fin d'appel. C'est la raison d'être de la doctrine « vault via MCP, jamais Edit direct » — pas du dogme, l'index en dépend.

## 4. `delete_note` prend le STEM (pas le chemin) — et laisse les wikilinks brisés

`mcp__forge-brain__delete_note(file=...)` résout par nom/alias : passer un chemin complet (`raw/.../note.md`) → « introuvable » silencieux (constat : 8 suppressions ratées avant correction). Passer le **STEM** (`note`).

Refuse si backlinks>0 sauf `force=True` ; avec `force`, les liens entrants deviennent **BRISÉS** (pas de cleanup auto) → lancer `lint_vault(category=broken_wikilinks)` après et nettoyer chaque source. Cf [[decision-vault-agent-first]] (un brut distillé = jetable — cas où `force=True` est acceptable).

## Wikilinks

- [[mcp-vault-llm-design]] — design MCP vault, gotchas résolution
- [[delegate-guard-pattern]] — le hook de protection (et son périmètre légitime)
