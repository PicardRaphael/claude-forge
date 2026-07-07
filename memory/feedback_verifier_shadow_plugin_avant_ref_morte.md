---
name: verifier-shadow-plugin-avant-ref-morte
description: "Skill supprimée ≠ référence morte : vérifier le shadow plugin avant de purger"
metadata:
  type: feedback
---

Une skill supprimée du `.claude/skills/` d'un repo ne rend PAS forcément mortes les références qui la nomment : une skill de même nom peut survivre via un **plugin** (`~/.claude/plugins/marketplaces/<m>/.../skills/<nom>`) ou un autre scope. Une référence n'est « morte » que si elle ne résout plus vers RIEN. Avant de purger : `find ~/.claude/plugins -type d -name "<skill>"`. Shadow présent → la réf résout, GARDER. Shadow absent → vraiment morte, purger/repointer. Vérifier CHAQUE nom séparément (l'asymétrie est le piège : `spec` avait un shadow PO vivant, `neoteem-back-ts` non).

**Why:** Session 24 juin — 2 skills forge supprimées (`spec`, `neoteem-back-ts`). J'ai failli purger toutes les réfs `/spec`/`Skill(spec)` ; le shadow plugin `neoteem-admin/po` les gardait vivantes. Ne pas confondre non plus le NOM DE REPO (`neoteem-back-ts`, vivant) avec la skill du même nom.
**How to apply:** Avant tout nettoyage de références après suppression d'un composant nommé — `find` le shadow plugin par nom, un par un, avant de trancher mort/vivant. Cf [[plugin-vs-skill-anatomie]].
