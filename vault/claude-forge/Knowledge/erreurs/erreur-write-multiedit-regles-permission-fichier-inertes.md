---
titre: "Erreur — règles Write(path)/MultiEdit(path) inertes, seul Edit(path) est évalué"
type: knowledge
domaine: claude-code
derniere-maj: 2026-07-16
auteur: claude
statut: actif
aliases:
  - Write path MultiEdit path règle inerte permission
  - seul Edit path évalué permission fichier
  - Edit couvre Write et MultiEdit permissions
  - MultiEdit not matched by file permission checks
  - règle permission fichier scopée par chemin
  - permission allow Edit tous outils édition
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#domaine/securite"
---

# Erreur — `Write(path)` / `MultiEdit(path)` sont inertes dans les permissions fichier

## La règle Claude Code

Dans `settings.json` / `settings.local.json`, le **contrôle de permission sur fichiers** ne reconnaît qu'une seule forme scopée par chemin : **`Edit(path)`**. Et cette règle **couvre tous les outils d'édition** — `Edit`, `Write`, **et** `MultiEdit`.

Conséquence directe :
- `Write(path)` et `MultiEdit(path)` **ne sont jamais évalués** par le contrôle fichier → règles mortes, bruit inerte.
- Un `Edit(path)` **seul** suffit à autoriser Write/Edit/MultiEdit sur ce chemin.

Message diagnostique caractéristique (émis par Claude Code) :
> Permission allow rule (.claude/settings.json): `MultiEdit(.claude/agents/**)` is not matched by file permission checks — only `Edit(path)` rules are. Use `Edit(.claude/agents/**)` instead (Edit rules cover all file-editing tools).

## Ne pas confondre avec le matcher de HOOK

Piège de symétrie : côté **hooks PreToolUse**, un matcher DOIT lister les trois outils explicitement — `Write|Edit|MultiEdit` — sinon trou architectural (cf [[comment-creer-hook]] triplet-checker, oublier `MultiEdit` = blind spot). La couverture implicite `Edit ⊃ {Write, MultiEdit}` vaut **uniquement pour les règles de permission fichier**, PAS pour les matchers de hook. Deux mécanismes distincts, deux conventions opposées.

## Portée observée (16 juillet 2026)

Le pattern inerte était présent dans **les 4 repos** — forge, ia_back, neo_ia, neoteem-brain — sous deux formes :
- `MultiEdit(.claude/agents/**)` / `MultiEdit(.claude/skills/**)` / `MultiEdit(./**)` (doublons des `Edit(...)` juste au-dessus)
- `Write(<repo>/**)` + `MultiEdit(<repo>/**)` (doublons du `Edit(<repo>/**)`)

Plus un `"Write"` global (sans chemin) redondant avec le `"Edit"` global.

## Le fix

Supprimer toute règle `Write(path)` et `MultiEdit(path)` dès qu'un `Edit(path)` couvre le même chemin. **Aucune couverture perdue** — `Edit(path)` autorise déjà Write/Edit/MultiEdit sur ce chemin.

⚠️ `settings.json` (permissions) est protégé par l'auto-mode classifier (self-modification, cf [[auto-mode-classifier]]) : l'édition peut nécessiter un feu vert manuel de Raphael selon le mode. Ces fichiers ne sont PAS des skills/agents/hooks/CLAUDE.md → hors périmètre de `delegate-guard`, édition directe légitime.

## Liens

- [[erreur-deny-global-ecrase-allow-projet]] — autre piège permissions (précédence deny global vs allow projet ; ici c'est la FORME de la règle, pas la précédence)
- [[erreur-settings-paths-hardcodes-multi-poste]] — settings, chemins durs cross-poste
- [[enableallprojectmcp-permissions-allow]] — couverture permissions au niveau MCP tool (sujet frère, niveau tool)
- [[comment-creer-hook]] — matcher hook `Write|Edit|MultiEdit` (convention OPPOSÉE : triplet explicite obligatoire)
- [[auto-mode-classifier]] — édition de settings.json permissions protégée
