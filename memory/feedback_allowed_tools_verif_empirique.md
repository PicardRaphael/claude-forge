---
name: allowed-tools-verif-empirique
description: Vérifier allowed-tools par grep du body avant de déclarer la liste complète
metadata:
  type: feedback
---

Avant de déclarer ou corriger les `allowed-tools` d'une skill, faire un grep sur le body pour
identifier TOUS les outils réellement appelés (WebFetch, WebSearch, Read, Bash, mcp__*).
Ne pas supposer depuis le nom de la skill ou son titre.

**Why:** Session 2026-06-06 : arxiv-verification avait WebFetch non déclaré. Raphael a demandé
de vérifier empiriquement avant d'affirmer "WebFetch uniquement".

**How to apply:** `grep -E "WebFetch|WebSearch|Read|Bash|mcp__" SKILL.md` avant tout audit
allowed-tools. Ne déclarer que les outils qui apparaissent dans le body.
