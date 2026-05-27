---
name: verifier-audit-deja-fait-avant-relancer
description: "Avant de lancer un audit thématique, vérifier que les notes du scope n'ont pas déjà été auditées récemment (frontmatter derniere-maj + backlinks vers Knowledge/erreurs/audit-*)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 326cfe7f-04a8-4854-8083-be00b4f78b4d
---

Avant de lancer un audit thématique sur un dossier vault, vérifier MÉCANIQUEMENT si les notes ont déjà été auditées récemment.

**Why** : Le 2026-05-23, j'ai lancé l'audit thématique 04 agents-ia alors que toutes les notes du dossier dataient déjà du 23 mai et référençaient `Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23`. Audit redondant = perte de tokens + risque de re-corriger ce qui était déjà correct. Pareil pour le thème 06 patterns/context déjà fait par une autre session.

**How to apply** :

Avant phase A d'un audit thématique :

1. `mcp__forge-brain__list_notes(folder="04-Techniques/<theme>")` → noter les `derniere-maj` du frontmatter
2. Si `derniere-maj` de la majorité = date du jour ou veille → fort indicateur d'audit déjà fait
3. `mcp__forge-brain__search_brain(query="<theme>-claims-fausses", limit=5)` → chercher une note `Knowledge/erreurs/<theme>-claims-fausses-YYYY-MM-DD` existante
4. Lire `vault/claude-forge/0-Inbox/context-actuel.md` → la section "Dernière session" liste les audits récents
5. Lire `vault/claude-forge/CHANGELOG.md` (10 premières lignes) → audits sont logués chronologiquement

Si audit déjà fait → STOP, ne pas relancer. Si user insiste → demander si correction des erreurs résiduelles ou audit fresh sur claims nouveaux apparus depuis.

Lié : [[feedback_audit_thematique_methode]] [[feedback_consolidate_searches]]
