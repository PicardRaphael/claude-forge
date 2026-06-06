---
name: jira-adf-rendu-mcp
description: Rendu visuel description Jira (titres colorés+emoji) = ADF via MCP contentFormat:adf uniquement. Wiki markup h2. cassé, markdown sans couleur. read-path ≠ write-path.
metadata:
  type: reference
---

Le rendu d'une description Jira Cloud avec titres colorés + emoji + séparateurs s'obtient **uniquement via l'ADF du MCP Atlassian** (`contentFormat:"adf"`). Le wiki markup `h2.`/`h3.` est cassé sur Jira Cloud (texte brut). Le markdown via MCP rend les titres mais **sans couleur** (la couleur = mark ADF `textColor`, ex `#00b8d9`, impossible en markdown).

**Pièges vérifiés empiriquement (5 juin 2026, skill `spec` PO) :**
- `responseContentFormat` (lecture) ≠ `contentFormat` (écriture) : le MCP renvoie toujours du markdown à la lecture même si on demande `adf`. **NE PAS inférer le comportement d'écriture depuis le read-path** (erreur commise puis corrigée — l'advisor a tranché).
- `getJiraIssue` + `expand:"renderedFields"` = HTML réellement affiché → lire la couleur exacte (`<font color>`).
- Pas de `deleteJiraIssue` dans le MCP (suppression web only).
- Build zip plugin Neoteem : Python zipfile (séparateurs `/`), JAMAIS `Compress-Archive` (sépare `\`, Claude rejette).

**Why :** raisonner sur une donnée de lecture pour conclure sur l'écriture m'a fait sous-estimer le bon fix ; seule la mesure empirique (ticket test + renderedFields) a tranché. Toujours mesurer le rendu, ne pas supposer.

**How to apply :** pour toute mise en forme Jira via MCP → ADF + `contentFormat:adf` ; valider en lisant `renderedFields` d'un ticket test vs un ticket de référence. Doctrine complète : note vault [[jira-rendu-adf-mcp-atlassian]]. Cf [[measure-before-optimize-tests]] (mesurer avant d'agir).
