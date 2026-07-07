---
titre: "Skills metadata tokens — coût de chargement au démarrage CC"
resume: "Claude Code charge name+description de TOUTES les skills au démarrage : 49 forge + 35 plugins ≈ 6 800 tokens. Cap description 250 chars = principal levier d'optimisation."
aliases:
  - "skills-metadata-tokens-load"
  - "skills tokens demarrage"
  - "cap description skill 250 chars"
  - "coût tokens skills session"
  - "optimisation tokens skills"
  - "skills metadata charge"
type: technique
domaine: claude-code
derniere-maj: 2026-07-07
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/skills"
  - "#domaine/context-management"
---
# Skills metadata tokens — coût de chargement au démarrage CC

> Mesure empirique du 28 mai 2026, session audit context tokens.

## Mécanisme (non documenté Anthropic)

À chaque démarrage de session, Claude Code charge le frontmatter `name:` + `description:` de **toutes** les skills disponibles (forge `.claude/skills/` + plugins user-scope). Visible dans le system-reminder SessionStart sous la section `available skills`.

Le body de la skill n'est **pas** chargé au démarrage — seulement à l'invocation (progressive disclosure). Seule la description compte pour le coût initial.

## Mesure (49 forge + 35 plugins)

| Source | Skills | Chars descriptions | Tokens (~÷4) |
|---|---|---|---|
| Forge `.claude/skills/` | 49 | 15 300 | ~3 825 |
| Plugins user-scope | 35 | 11 982 | ~2 996 |
| **Total** | **84** | **27 282** | **~6 800** |

Avec tokenizer réel Claude (~÷3.3) : **~8 200 tokens** par session, avant le moindre message utilisateur.

## Top 3 descriptions forge à réduire en priorité (28 mai 2026)

| Skill | Chars |
|---|---|
| cc-news | 530 |
| x-read | 517 |
| spec | 511 |

Cap recommandé : **250 chars max** par description. Au-delà, la description est aussi tronquée dans le system-reminder `/skills` (limite system prompt).

## Leviers d'optimisation (priorité décroissante)

1. **Cap descriptions forge à 250 chars** → économie ~1 500 tokens cumulés (skills trop longues réduites)
2. **Désinstaller plugins skills non utilisés** → économie ~3 000 tokens (plugins = 44 % du coût total)
3. **Body riche, description courte** : pour une skill complexe, mettre les détails dans le body (chargé à l'invocation) et garder la description dense mais courte

## Script de mesure (PowerShell)

```powershell
Get-ChildItem .claude\skills -Directory | ForEach-Object {
  $sk = Join-Path $_.FullName 'SKILL.md'
  if (Test-Path $sk) {
    $c = Get-Content $sk -Raw
    $m = [regex]::Match($c, '(?ms)^description:\s*(.+?)(?=^\w+:|^---)')
    if ($m.Success) { [PSCustomObject]@{Name=$_.Name; Chars=$m.Groups[1].Value.Trim().Length} }
  }
} | Sort-Object Chars -Descending
```

## Connexion doctrine

Même principe que [[pattern-vault-llm-karpathy]] (références legères au chargement, détail à la demande) et [[comment-creer-skill]] (cap description 250 chars pour auto-trigger fiable).

## WIKILINKS

- [[comment-creer-skill]] — règle des 250 chars + catégories Thariq
- [[plugin-vs-skill-anatomie]] — progressive disclosure : ~30-50 tokens au départ, body à l'activation
- [[mcp-vs-skills-doctrine]] — quand skill, quand MCP, quand Bash
- [[context-management]] — gestion globale du context window CC
- [[pattern-vault-llm-karpathy]] — principe légèreté init / détail à la demande
