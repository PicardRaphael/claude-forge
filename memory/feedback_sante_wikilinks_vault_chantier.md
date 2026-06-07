---
name: sante-wikilinks-vault-chantier
description: "131 wikilinks brisés dans le vault forge-brain au 2026-06-07 (baseline lint_vault). Chantier dédié hygiène à mener Obsidian fermé, séparément de toute écriture vault en cours."
metadata:
  node_type: memory
  type: feedback
---

Au 7 juin 2026, `mcp__forge-brain__lint_vault` rapporte **131 wikilinks brisés** dans le vault forge-brain (baseline mesurée en début de session capitalisation « Référence technique stack IA »). 0 YAML cassé, 0 orpheline.

**Why:** Raphael veut réparer ces 131 liens, mais PAS en parallèle d'une autre écriture vault (deux opérations d'écriture vault concurrentes = race-condition, Obsidian doit être fermé). À traiter comme chantier dédié distinct, dans la même famille hygiène que `/clean-memory`.

**How to apply:** Quand le chantier démarre (Obsidian fermé, aucune autre écriture vault en cours) :
1. `lint_vault` pour la liste fraîche (le compte aura pu bouger).
2. **Diagnostiquer la CAUSE par catégorie** avant de réparer : (a) `[[index]] -> [[fiche-non-créée]]` = MOC casquettes pointant vers des fiches jamais écrites (le gros du volume — décider créer-les-fiches vs retirer-les-liens) ; (b) `[[note]] -> [[../dossier/cible]]` = wikilinks à chemin relatif `../` non résolus par le linker (corriger en wikilink nu `[[cible]]`) ; (c) renommages/suppressions ayant laissé des liens morts ; (d) typos/placeholders (`[[X]]`, `[[stem]]`, `[[Nom-leader]]` dans mcp-vault-llm-design / erreur-audit-07-leaders = exemples illustratifs intentionnels, à exclure).
3. Réparer par catégorie, pas lien par lien. Les placeholders illustratifs (catégorie d) = laisser tels quels ou escaper.
4. Re-`lint_vault` pour vérifier la baisse.

**Garde-fou écriture vault confirmé cette session** : `lint_vault` avant/après une écriture vault = contrôle wikilink fiable (le script `detect-wikilink-corruption.py` parfois cité N'EXISTE PAS dans le repo — l'équivalent matériel est `lint_vault` + skill `/vault-audit`). Vérifié : delta 0 sur 131 après création de 4 notes correctement liées. Cf [[feedback_mcp_alias_ambigu_chemin_exact]] (écriture vault sûre) et `.claude/skills/vault-audit`.
