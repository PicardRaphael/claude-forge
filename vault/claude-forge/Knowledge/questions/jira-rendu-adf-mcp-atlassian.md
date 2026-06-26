---
aliases:
  - rendu Jira ADF MCP
  - titres colorés Jira description
  - wiki markup Jira cassé
  - contentFormat adf Jira
  - emoji couleur ticket Jira
resume: "Le rendu visuel d'une description Jira Cloud (titres colorés + emoji + séparateurs) ne s'obtient QUE via l'ADF du MCP Atlassian (contentFormat:adf) ; le wiki markup h2./h3. est cassé et le markdown ne porte pas la couleur."
derniere-maj: 2026-06-26
tags:
  - "#type/question"
  - "#stack/atlassian"
  - "#domaine/jira"
  - "#projet/neoteem-po"
---
# Rendu d'une description Jira Cloud (titres colorés + emoji) via le MCP Atlassian

## Problème

Les descriptions de tickets affichaient `h2. Objectif` / `h3.` en **texte brut littéral** dans Jira Cloud. La skill `spec` PO produisait du **wiki markup Jira** (`h2.`, `h3.`, `{color}`), syntaxe legacy que **Jira Cloud n'interprète plus** → rendu cassé. acli n'arrange rien (il envoie tel quel).

## Les 3 formats — ce qui marche et ce qui ne marche pas

| Format | Titres | Couleur | Verdict |
|---|---|---|---|
| **Wiki markup** (`h2.`, `h3.`, `{color}`) | texte brut littéral | non | ❌ cassé sur Jira Cloud |
| **Markdown** (`###`, `*`, `---`) via MCP `contentFormat:"markdown"` | vrais titres + emoji + séparateurs | **NON** (titres noirs) | ⚠️ propre mais pas de couleur |
| **ADF** via MCP `contentFormat:"adf"` | vrais titres h3 + emoji | **OUI** `#00b8d9` | ✅ pixel-perfect |

## La couleur de titre = mark ADF `textColor` (impossible en markdown)

Mesuré sur le HTML rendu (`getJiraIssue` + `expand:"renderedFields"`) du ticket de référence N2-98153 :
```html
<h3>🎯 <font color="#00b8d9">Objectif / problématique :</font></h3>
```
La couleur est une **marque ADF `textColor`** sur le texte du heading. Le markdown standard (`###`) ne peut pas la porter. Donc pour reproduire un rendu coloré → ADF obligatoire.

Pattern ADF validé en prod (heading coloré + paragraphe + séparateur + liste) :
```json
{ "type": "heading", "attrs": {"level": 3}, "content": [
    {"type": "text", "text": "🎯 "},
    {"type": "text", "text": "Objectif :", "marks": [{"type": "textColor", "attrs": {"color": "#00b8d9"}}]}
]}
```
Séparateur `---` = nœud `{"type":"rule"}`. Listes = `bulletList`. Emojis unicode (💡🎯⚙️) fonctionnent directement en ADF.

## Gotchas découverts (vérifiés empiriquement 5 juin 2026)

1. **`responseContentFormat` (lecture) ≠ `contentFormat` (écriture)** : deux paramètres indépendants du MCP. Le MCP Atlassian renvoie TOUJOURS la description en markdown à la lecture, même quand on demande `adf` — c'est une limite de sérialisation de la *réponse*, qui ne dit RIEN sur le format d'écriture. Ne pas inférer le comportement d'écriture depuis le read-path (erreur commise puis corrigée).
2. **`expand:"renderedFields"`** sur `getJiraIssue` renvoie le **HTML réellement affiché** → seul moyen fiable de lire la couleur exacte (`<font color="#...">`) et la structure rendue.
3. **Pas de `deleteJiraIssue`** dans le MCP Atlassian — suppression uniquement via l'interface web. Transitions disponibles via `getTransitionsForJiraIssue`.
4. **acli ne garantit pas le rendu** : pour la mise en forme, le MCP en ADF est le moteur. acli → pièces jointes (upload natif que le MCP ne fait pas) + repli.
5. **Méthode de validation** : créer 1 ticket test via MCP, lire son `renderedFields`, comparer au ticket de référence, supprimer (ou laisser l'user supprimer). Mesurer, ne pas supposer.

## Panel ADF multi-contenu (encadrés Neoteem)

Le nœud `panel` ADF (fond jaune = `panelType:"warning"`) peut contenir plusieurs paragraphes et des marques `strong`. Pattern validé pour les encadrés PO Neoteem (6 juin 2026) :

```json
{
  "type": "panel",
  "attrs": { "panelType": "warning" },
  "content": [
    { "type": "paragraph", "content": [
      { "type": "text", "text": "⚠️ Titre en gras", "marks": [{ "type": "strong" }] }
    ]},
    { "type": "paragraph", "content": [
      { "type": "text", "text": "Premier paragraphe de contenu." }
    ]},
    { "type": "paragraph", "content": [
      { "type": "text", "text": "Deuxième paragraphe." }
    ]}
  ]
}
```

Rendu Jira : `<div class="panel" style="background-color: #fffae6;">` contenant les paragraphes. Vérifiable sur N2-111159.

**Deux encadrés distincts par type de ticket (règle Neoteem PO)** :
- Parent STORY → encadré **court** (1 paragraphe, texte simple)
- Sous-tâche [WEB] → encadré **« Règles Claude »** (titre gras + 4 paragraphes, composants Neoteem)
- Toute sous-tâche technique → encadré **choix techniques** (« Les choix techniques sont indicatifs... »)

## Application Neoteem

Skill `spec` (plugin PO `neoteem-po`) : création via MCP `createJiraIssue` + `contentFormat:"adf"`, gabarit ADF dans `references/templates-tickets.md`, ticket **N2-98153** = référence vivante de style (relisible via MCP). Doctrine moteur : MCP par défaut, acli pour PJ.

## Liens

- Build plugin via Python zipfile (séparateurs `/`), JAMAIS `Compress-Archive` (sépare en `\`, Claude rejette « invalid characters ») — cf `build-skills-zip.ps1` du repo `neoteem-plugin-claude-admin`.
- [[plugin-vs-skill-anatomie]] — distribution skills/plugins Neoteem

---

## AJOUT 26 juin 2026 — CORRECTION du gotcha #1 : `responseContentFormat:"adf"` renvoie BIEN l'ADF (read-path)

Le gotcha #1 ci-dessus (« le MCP Atlassian renvoie TOUJOURS la description en markdown à la lecture, même quand on demande `adf` ») est **faux à partir d'au moins juin 2026** — vérifié empiriquement le 26 juin sur le projet IA (`getJiraIssue` avec `responseContentFormat: "adf"`).

**Constat mesuré** : `getJiraIssue(..., responseContentFormat: "adf")` renvoie le **document ADF structuré complet** dans `fields.description` (arbre `{type:"doc", content:[...]}` avec headings, marks `textColor`, `taskList`, `table`, `panel`, `codeBlock`…), PAS du markdown. Ça a permis un **retrait chirurgical** (lire l'ADF réel → supprimer un seul nœud → réécrire via `editJiraIssue` `contentFormat:"adf"`) au lieu d'une reconstruction ADF à l'aveugle depuis le markdown. Sur les mêmes tickets, `responseContentFormat: "markdown"` (ou l'omission) renvoie bien du markdown — donc le paramètre **est respecté** au read, contrairement à ce que disait le gotcha #1.

**Lecture à jour** :
- Pour MODIFIER chirurgicalement une description Jira existante (retirer/ajouter un nœud sans casser le rendu coloré) → `getJiraIssue` `responseContentFormat:"adf"` puis `editJiraIssue` `contentFormat:"adf"` avec l'arbre modifié. Pas besoin de reconstruire l'ADF de mémoire.
- `expand:"renderedFields"` (gotcha #2) reste utile pour lire le **HTML rendu** (vérifier la couleur exacte affichée, un glyphe corrompu au source, etc.) — complémentaire de l'ADF, pas redondant.
- Le gotcha #1 était peut-être vrai sur une version antérieure du MCP (note datée 5 juin) ; le comportement a changé. **Mesurer à la source avant de s'appuyer sur le read-path** plutôt que relayer le gotcha #1 tel quel.

Contexte : chantier `/spec` 3 repos — retrait de lignes parasites + ajout d'un footer `/spec · rôle:` sur IA-27/28/33/34, rendu `#00b8d9` préservé. Cf `memory/project_spec_unification_3repos.md`.
