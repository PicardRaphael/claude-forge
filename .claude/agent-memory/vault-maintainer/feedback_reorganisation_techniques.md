---
name: Feedback reorganisation 04-Techniques
description: Patterns appris lors de la reorganisation structurelle de 04-Techniques (2026-05-10)
type: feedback
---

## Regles apprises lors de la reorganisation 04-Techniques (2026-05-10)

**Regle 1 : Ne pas merger des notes qui se cross-referencent**

Quand deux notes s'explicitement cross-referencent dans leur section ## Liens ET couvrent des angles distincts (framework conceptuel vs checklist d'application), les garder separees. Le merge efface la distinction intentionnelle.

**Why:** agentic-engineering-karpathy (framework conceptuel) et pattern-agentic-engineering (checklist projet) etaient candidates au merge mais sont complementaires, pas redondantes.

**How to apply:** Verifier la section ## Liens des deux notes. Si elles se linkent mutuellement ET ont des resumes differents, c'est signe de complementarite, pas de duplication.

---

**Regle 2 : Wikilinks — toujours normaliser vers nom seul, pas chemin**

Lors d'un deplacemennt, supprimer les prefixes de chemin dans les wikilinks internes. `[[04-Techniques/vibe-coding-setup-complet]]` → `[[vibe-coding-setup-complet]]`. Obsidian resout par nom, pas par chemin.

**Why:** Les chemins relatifs cassent quand les notes bougent. Les noms resolvent toujours.

**How to apply:** A chaque note deplacee, scanner la section ## Liens pour des wikilinks avec prefixe dossier et les normaliser.

---

**Regle 3 : Notes qui quittent un domaine → MOC source ET MOC cible**

Quand une note change de domaine (ex: technique → feature), mettre a jour les deux MOCs : retirer du MOC source (ou signaler le deplacement), ajouter au MOC cible.

**Why:** Le MOC-Techniques listait des notes Neoteem-infra et Claude Desktop qui n'etaient pas des techniques generiques. Le MOC refletait une taxonomie incorrecte.

**How to apply:** Pour chaque deplacement hors du dossier d'origine, identifier le MOC source et le MOC cible. Modifier les deux.

---

**Regle 4 : mkdir avant Write sur nouveau dossier**

Les dossiers Knowledge/evolutions/ et Knowledge/reviews/ n'existaient pas. Write direct echoue silencieusement ou cree des fichiers au mauvais endroit. Toujours `mkdir -p` avant Write dans un dossier potentiellement absent.

**Why:** Bash ls pour verifier l'existence d'abord, puis mkdir si absent.

**How to apply:** Avant tout Write dans un sous-dossier Knowledge/ ou nouveau sous-dossier, verifier son existence avec ls et creer si necessaire.

---

**Regle 5 : type du frontmatter doit correspondre au dossier cible**

claude-desktop-preferences.md avait `type: technique` mais allait dans `01-Claude-Code/features/`. Le type a ete corrige en `feature` lors du deplacement.

**Why:** Le type frontmatter doit correspondre au template du dossier cible (feature.md, technique.md, etc.).

**How to apply:** Lors d'un deplacement de dossier, verifier que `type:` dans le frontmatter correspond bien au type attendu par le dossier cible.
