---
name: vault-edit-gotchas-outillage
description: Quatre gotchas outillage à l'écriture vault — delegate-guard faux positif sur note nommée agents-*.md, insert_section qui misparente après un header nu, Edit disque direct qui désynchronise l'index SQLite (réindex au poll 30s), et delete_note par stem (pas chemin) qui laisse les liens brisés
metadata:
  type: reference
---

Gotchas découverts en éditant des notes vault, tous liés à l'outillage d'écriture, pas au contenu.

**Why:** chacun a coûté un détour ; ils sont invisibles tant qu'on ne les a pas rencontrés et re-mordront sur toute édition vault future.

**How to apply:**

1. **delegate-guard faux positif sur notes vault `agents-*.md`** — le hook `delegate-guard.py` matche `agents/*.md` PAR NOM. Une note vault `04-Techniques/agents/agents-architecture.md` se fait bloquer en Edit direct comme si c'était un sous-agent `.claude/agents/`. → Pour modifier le CONTENU d'une note vault, utiliser les outils MCP forge-brain (`insert_section`, `update_note`, `append_note`) qui ne passent pas par le hook PreToolUse Edit. Réserver Edit/Write aux notes dont le nom ne déclenche pas le pattern (ex. `index.md`, `stack-*.md`, `economie-*.md` passent). Ne JAMAIS contourner le hook par env var/script (cf [[delegate-guard-env-var-blocked]]).

2. **`insert_section` misparente après un header de section nu** — `mcp__forge-brain__insert_section(marker="## Section", position="after")` insère juste APRÈS la ligne du header, pas après la section entière. Si la section commence par un header `##` suivi directement de sous-sections `###` ou d'une table, le contenu inséré se loge AVANT le corps existant → la table/le bloc d'origine se retrouve reparenté sous la dernière sous-section insérée. → Pour insérer en FIN de section, viser un marker précis (dernière phrase de la section, en gras si possible) plutôt que le header nu. Vérifier le placement avec `read_section(file, heading="## Section")` (le param s'appelle `heading` et DOIT commencer par `#`). Correction = `update_note` (réécriture complète) si le bloc est déjà mal parenté.

3. **Edit DISQUE direct sur une note vault → index SQLite désynchronisé** (7 juin 2026, chantier 5). Corriger une note vault via `Edit`/`Write` (au lieu des outils MCP) écrit bien le disque, mais ne réindexe PAS : la table `links`/`tags` du MCP reste sur l'ancien état. La réindexation n'arrive qu'au prochain tick du watcher (poll `poll_interval_seconds=30` dans config.yaml) — d'où un `lint_vault` qui montre encore un lien qu'on vient de corriger. NE PAS confondre avec le lag d'agrégat (limite #4, fluctuation non liée aux edits) : ici c'est l'écriture hors-MCP qui n'a pas déclenché `index_note`. → Éditer le CONTENU d'une note vault TOUJOURS via MCP (`update_note`/`update_property`/`insert_section`) qui réindexe atomiquement en fin d'appel. Si un Edit disque a déjà eu lieu : forcer la réindexation par un appel MCP sur la note (`update_property` sur `derniere-maj` suffit — il appelle `index_note`), ou attendre le poll 30s. C'est la raison d'être de la doctrine « vault via MCP, jamais Edit direct » — pas du dogme, l'index en dépend.

4. **`delete_note` prend le STEM (pas le chemin) — et laisse les wikilinks brisés** (27 juin 2026). `mcp__forge-brain__delete_note(file=...)` résout par nom/alias : passer un chemin complet (`raw/.../note.md`) → « introuvable » silencieux (constat : 8 suppressions ratées avant correction). Passer le STEM (`note`). Refuse si backlinks>0 sauf `force=True` ; avec `force`, les liens entrants deviennent BRISÉS (pas de cleanup auto) → lancer `lint_vault(category=broken_wikilinks)` après et nettoyer la source. Cf [[decision-vault-agent-first]] (un brut distillé = jetable).

Contexte : (1)(2) capitalisation rapport « Stack IA en production 2026 » → vault, cf [[stack-ia-production-2026]], [[delegate-guard-pattern]] ; (3) correction de 2 wikilinks cassés détectés par `lint_vault(category=broken_wikilinks)`, chantier 5 limite #1.
