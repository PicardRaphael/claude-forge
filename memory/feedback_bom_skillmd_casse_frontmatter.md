---
name: bom-skillmd-casse-frontmatter
description: BOM UTF-8 en tête d'un SKILL.md casse le frontmatter → "plugin validation failed" Cowork ou skill non chargée. Écrire SKILL.md en UTF-8 SANS BOM.
metadata:
  type: reference
---

Un BOM UTF-8 (octets `239 187 191`) en tête d'un `SKILL.md` casse le parsing du frontmatter YAML. Symptôme : **« plugin validation failed »** à l'upload Cowork, OU la skill est silencieusement **non chargée** (l'utilisateur tape `/spec`, rien ne s'active, Claude rédige « à la main » sans suivre les templates ni l'ADF — ce qui ressemble à un bug de la skill alors que c'est qu'elle n'a jamais tourné).

**Cause du BOM (Windows) :** PowerShell `Out-File` / `Set-Content` ajoutent un BOM par défaut. Réflexe : écrire en UTF-8 sans BOM →
`[System.IO.File]::WriteAllText($f, $c, (New-Object System.Text.UTF8Encoding($false)))`. Vérifier : `[System.IO.File]::ReadAllBytes($f)[0..2]` ≠ `239 187 191`.

**Why :** sur le cas PO Neoteem (6 juin 2026), j'ai d'abord soupçonné le packaging du zip puis le `allowed-tools`, alors que le SKILL.md avait un BOM (édité plus tôt via PowerShell). Diagnostic mécanique non vérifié = perte de temps.

**How to apply :** après toute écriture/édition de SKILL.md (ou .md de plugin) via PowerShell sur Windows, vérifier l'absence de BOM avant de zipper/livrer. Doctrine complète : note vault [[plugin-vs-skill-anatomie]] (section Anti-patterns). Cf [[python-path-windows-hooks]] (autres pièges Windows d'encodage).
