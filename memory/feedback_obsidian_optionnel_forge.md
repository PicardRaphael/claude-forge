---
name: obsidian-optionnel-forge
description: forge-brain — Obsidian optionnel (GUI humaine seule). Le MCP couvre toutes les ops agent. Débranché de fait depuis ~30/05/2026, sans casse. obsidian-cli supplanté par le MCP.
metadata:
  node_type: memory
  type: feedback
---

**forge-brain : Obsidian est OPTIONNEL.** Le MCP forge-brain (local, port 8091) couvre **toutes les opérations agent** sur le vault : lire, chercher (FTS5 BM25), créer, écrire, déplacer (avec réécriture wikilinks auto), supprimer, lint. Obsidian n'apporte plus que la **GUI humaine** : graphe visuel, reading mode, plugins, édition Canvas/Excalidraw à la souris.

**Why:** Vérifié le 07/06/2026 — Obsidian est **débranché de fait depuis ~30/05** (0 process, cache `.obsidian/` figé au 30/05), et rien ne casse : le MCP répond normalement (0 erreur sur 500+ appels/7j). Obsidian = **lecture humaine seule**, jamais d'écriture ni d'usage Claude dessus → exclu du vecteur race-condition (cf [[feedback_sante_wikilinks_vault_chantier]]). Le chemin `obsidian-cli` (« Obsidian DOIT être ouvert ») est **supplanté par le MCP** — cf [[reference_obsidian_query_brain]] (obsolète pour forge-brain).

**How to apply:**
- Ne PAS re-douter chaque session « ai-je besoin d'Obsidian ? » → non, pour les ops agent. Le MCP suffit.
- Rouvrir Obsidian uniquement pour un besoin **humain visuel** (voir le graphe, éditer à la main).
- Distinct d'obsidian-brain (autre MCP, autre vault — cf [[project_mcp_v2]]).
