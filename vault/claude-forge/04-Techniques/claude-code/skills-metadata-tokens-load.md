---
titre: "Skills metadata tokens — coût de chargement au démarrage CC"
resume: "Claude Code charge name+description de toutes les skills au démarrage. Mesure forge au 5 sept. 2026 : 51 skills, 11 323 chars, ~3 400 tokens. Le mécanisme n'est PAS une troncature à 250 chars mais un budget global avec drop entier des descriptions quand le listing dépasse ~1 % du contexte."
aliases:
  - "skills-metadata-tokens-load"
  - "skills tokens demarrage"
  - "cap description skill 250 chars"
  - "coût tokens skills session"
  - "optimisation tokens skills"
  - "skills metadata charge"
  - "budget listing skills"
type: technique
domaine: claude-code
derniere-maj: 2026-09-05
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/skills"
  - "#domaine/context-management"
---
# Skills metadata tokens — coût de chargement au démarrage CC

> Mesure empirique initiale du 28 mai 2026 ; mécanisme corrigé et mesure refaite le **5 septembre 2026**.

## Mécanisme (non documenté Anthropic)

À chaque démarrage de session, Claude Code charge le frontmatter `name:` + `description:` de **toutes** les skills disponibles (forge `.claude/skills/` + plugins user-scope). Visible dans le system-reminder SessionStart sous la section `available skills`.

Le body de la skill n'est **pas** chargé au démarrage — seulement à l'invocation (progressive disclosure). Seule la description compte pour le coût initial.

## ⚠️ Correction du 5 septembre 2026 — ce n'est pas une troncature à 250

Cette note affirmait : *« Au-delà [de 250 chars], la description est aussi tronquée dans le system-reminder /skills »*. **C'est faux, et ça l'était déjà quand la note a été écrite** : la correction avait été actée le 18 juin dans [[comment-creer-skill]], trois semaines avant la rédaction de cette note-ci. Une régression, pas un simple retard — d'où l'intérêt de vérifier le corpus avant d'écrire une note qui recoupe un sujet déjà traité.

Le mécanisme réel : **il n'y a pas de troncature uniforme à 250 caractères**. Sous pression de budget, Claude Code **drope des descriptions entières** — celles des skills peu utilisées — quand le listing dépasse environ 1 % de la fenêtre de contexte. La conséquence pratique est différente et plus brutale : une description trop longue ne se fait pas raboter, elle fait courir le risque que **d'autres skills disparaissent entièrement** du listing, donc cessent de pouvoir s'auto-déclencher.

Le cap de 250 caractères reste une **bonne pratique de budget** — moins de chars, plus de skills visibles — mais ce n'est pas un seuil de troncature. Ne pas re-propager l'ancienne justification.

## Mesure forge au 5 septembre 2026

| Source | Skills | Chars descriptions | Tokens (~÷3,3) |
|---|---|---|---|
| Forge `.claude/skills/` | **51** | **11 323** | **~3 431** |
| Plugins projet | 0 | 0 | 0 |

`enabledPlugins` est vide dans `.claude/settings.json` : le coût plugins mesuré en mai (35 skills, ~3 000 tokens) ne s'applique plus au scope projet. Les plugins user-scope (`~/.claude/`) n'ont pas été recomptés dans cette passe.

**Seulement 3 descriptions dépassent 250 caractères** : `cc-news` (290), `obsidian-markdown` (262), `obsidian-bases` (256).

### Comparaison avec la mesure du 28 mai 2026

| | 28 mai | 5 sept. | Écart |
|---|---|---|---|
| Skills forge | 49 | 51 | +2 |
| Chars cumulés | 15 300 | 11 323 | **−26 %** |
| Tokens | ~3 825 | ~3 431 | −10 % |
| Plus longue description | `cc-news` 530 | `cc-news` 290 | −45 % |

Le travail d'optimisation a porté : le corpus a grossi de deux skills tout en réduisant d'un quart le coût de chargement. Les trois pires cas de mai (`cc-news` 530, `x-read` 517, `spec` 511) sont tous rentrés dans les clous. C'est le rare cas où une note de dette peut être relue comme une mesure de progrès — raison de plus pour la garder à jour plutôt que de la laisser affirmer un état révolu.

## Leviers d'optimisation (priorité décroissante)

1. **Garder les descriptions denses et courtes** (~250 chars comme repère de budget, pas comme seuil de troncature) → maximise le nombre de skills réellement listées.
2. **Désinstaller les plugins non utilisés** → en mai, les plugins pesaient 44 % du coût total.
3. **Body riche, description courte** : pour une skill complexe, les détails vont dans le body (chargé à l'invocation), la description ne porte que le déclencheur.

## Script de mesure

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

Même principe que [[pattern-vault-llm-karpathy]] (références légères au chargement, détail à la demande) et [[comment-creer-skill]] (description courte pour un auto-trigger fiable — **source canonique du mécanisme de budget**, cette note n'en porte que la mesure).

## WIKILINKS

- [[comment-creer-skill]] — mécanisme de budget canonique + catégories Thariq
- [[plugin-vs-skill-anatomie]] — progressive disclosure : métadonnées au départ, body à l'activation
- [[mcp-vs-skills-doctrine]] — quand skill, quand MCP, quand Bash
- [[context-management]] — gestion globale du context window CC
- [[pattern-vault-llm-karpathy]] — principe légèreté init / détail à la demande
