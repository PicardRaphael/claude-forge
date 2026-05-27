---
name: da-failure-decision-protocol
description: "Si devil's advocate retourne erreur (529, timeout, output vide), ne PAS livrer sans verdict — soit relancer, soit invoquer advisor comme remplacement, soit STOP la livraison"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8957d13-cb6a-43d0-ae69-71bb7fa375a2
---

Si le devil's advocate échoue (API 529 Overloaded, timeout, transcript vide, output JSON cassé) : NE PAS livrer le chantier sans verdict alternatif. 3 options dans l'ordre :

1. **Relancer le DA** une seule fois (5 min plus tard)
2. **Invoquer advisor** comme remplacement (il voit la conversation complète, peut donner un verdict structuré)
3. **STOP la livraison** : commit en WIP, capitaliser le draft, finir en session dédiée

NE JAMAIS : livrer en se disant "le DA d'avant a déjà validé l'idée générale" — c'est exactement la régression que le DA est censé attraper.

**Why:** Session 2026-05-20 — fusion `/spec` + `/decompose-ticket` shippée sur 3 repos sans verdict DA final (529 API error après lancement). J'ai utilisé le DA du matin comme proxy ("a déjà validé l'idée") mais le DA du matin n'avait pas vu : le SKILL.md final 147L (sub-agent), le déploiement cross-stack, la suppression decompose-ticket, ni le drift potentiel master/clones. Le hook devil-advocate-stop a été ignoré bypassé par "tu m'as ordonné de finir". Le DA aurait probablement signalé l'absence de test sur vrai ticket avant push.

**How to apply:**
- Hook devil-advocate-stop bloque pour une raison → respecter le blocage
- DA 529 → relancer 1 fois, si échec → advisor comme fallback obligatoire
- Si l'utilisateur dit "fais tout commit push" alors qu'aucun verdict DA n'est valide → signaler explicitement avant d'agir : "DA n'a pas validé, advisor recommandait STOP, tu confirmes override ?"
- Override doit être conscient et tracé (pas implicite)
- L'absence de verdict ≠ verdict positif. Default = ne pas livrer.
- Lien : [[erreur-devils-advocate-tronque]] (vault) — pattern similaire de DA non-finalisé livré quand même

**Cas Windows PowerShell heredoc (ajouté 22 mai)** :
- Symptôme : DA tourne 15-20 min, retourne un fragment de bricolage shell (write-critique.ps1, heredoc cassé) au lieu d'une critique
- Cause : DA tente d'écrire la critique vault via Bash heredoc → quoting PowerShell échoue → DA finit par ne sauver que le frontmatter de la note
- Signal d'alerte : la note vault contient SEULEMENT le frontmatter (résumé OK, body vide)
- Action : lire la note quand même, le `resume:` du frontmatter contient souvent un verdict utile (ex 22 mai : "REVISE + 3 bloquants manqués dont 1 sécu critique" trouvé dans le résumé alors que le body était vide)
- Fix systémique : prompt explicitement DA à utiliser `mcp__forge-brain__create_note` (MCP) au lieu de Bash heredoc
