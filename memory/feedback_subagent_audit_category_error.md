---
name: subagent-audit-category-error
description: "Sub-agent audit vault flagge \"drift\" sur note de doc citant des valeurs d'un objet externe — vérifier que la note décrit elle-même l'objet vs documente un objet vivant ailleurs"
trigger: drift, audit vault, note de doc, faux positif
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3751b01a-33d9-4962-b652-428c951e42d4
---

## Pattern d'erreur

Sub-agent audit (read-only) lit une note `01-Claude/Code/agents/Agent — X.md` qui mentionne `color: blue` dans son body. Conclut : "drift Type 1 doctrinal vs canonique agents-color-convention qui dit pink pour meta-creators".

**Le piège** : la note est une **fiche de documentation** qui décrit l'agent éponyme. La valeur `color:` réelle de l'agent vit dans `.claude/agents/X.md` (autre fichier). Vérification empirique : tous les agents `.claude/agents/` étaient déjà conformes (pink/purple), seules les notes vault étaient obsolètes.

Si j'avais appliqué le "fix" recommandé par C2 (changer la doc en pink), j'aurais :
1. Confirmé une fausse divergence
2. Masqué le vrai problème (doc obsolète à supprimer ou synchroniser)

## Why

Advisor a flaggé : "ces notes sont des fiches Knowledge, pas les agents eux-mêmes. La rule parle du frontmatter `.claude/agents/`, pas du `color:` qu'une note de doc cite dans son body. Avant fix : ouvre `.claude/agents/agent-creator.md` et confirme."

5 minutes de vérif empirique vs propagation drift sur 5 notes + corruption auto-référentielle.

## How to apply

Quand un sub-agent audit signale un drift Type 1 doctrinal sur une valeur citée (color, model, effort, version) :

1. **Identifier la source de vérité** : la valeur vit-elle dans cette note (objet propre) ou ailleurs (note de doc) ?
2. Si note de doc → ouvrir la source de vérité réelle et vérifier
3. Si source de vérité conforme → la note de doc est OBSOLÈTE, pas en drift
4. Décision : supprimer la doc (si redondante) OU synchroniser (si valeur historique)

**Règle générale** : avant tout mass-fix recommandé par sub-agent audit, vérifier 2-3 cas en lecture directe. Le coût de la vérif (5 min) est dérisoire vs le coût d'une propagation inverse.

## Liens

- Méthode A→B→C→D→E : étape C "croisement" doit inclure vérif source de vérité
- [[feedback_audit_claims_after_brief]] — vérifier empiriquement les claims de sub-agents
- Audit vault 24 mai 2026 : 5 fiches `Agent — X` auraient été corrompues sans cette vérif
