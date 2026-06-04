---
name: mcp-transport-stdio-http-crashloop
description: Serveur FastMCP en crash loop systemd + nginx 502 = transport stdio au lieu de http. Le log dit "with transport 'stdio'". Diagnostiquer par les logs AVANT de soupçonner l'OAuth.
metadata:
  type: feedback
---

Un serveur MCP (FastMCP) déployé sur VM derrière nginx qui **crash-loop** (systemd `restart counter` qui grimpe) + **nginx 502 Bad Gateway** = très probablement lancé en transport **`stdio`** au lieu de **`http`**. En stdio sans client stdin attaché, le process démarre, indexe, puis s'arrête aussitôt → systemd le relance en boucle → nginx ne joint jamais de backend stable → 502.

**Signature dans les logs** : `Starting MCP server 'X' with transport 'stdio'` puis `Background loops stopped` → `Deactivated successfully` → `Scheduled restart job, restart counter is at N`.

**Why:** Le 3 juin 2026, le MCP obsidian-brain (VM) était en crash loop. J'ai d'abord parié à 80% sur l'OAuth (« il a mis l'authentification, ça boucle ») — FAUX. Les logs ont tranché : c'était le transport stdio (un commit du 1er juin avait mis stdio en défaut). Leçon : sur une crash loop, **lire les logs du service AVANT de former une hypothèse** ; le dernier changement mentionné par l'user (ici OAuth) est un biais, pas une preuve. Cf [[feedback_regression_diagnostic_diff_avant_redesign]] (diagnostic empirique avant hypothèse).

**How to apply:**
1. Crash loop + 502 → demander/lire les logs systemd (`journalctl -u <svc>`) ou applicatifs. Chercher la ligne `transport '...'`.
2. Fix : lancer FastMCP en `--transport http --host 0.0.0.0 --port N` (ou `app.run(transport="streamable-http", ...)`). Le défaut d'un serveur destiné à une VM/HTTP doit être `http`, pas `stdio` (stdio = Claude Desktop local via command+args).
3. Un `git pull` sur la VM suffit à propager un fix de code si la VM pull le repo — mais il faut un restart du service (le crash loop le fait tout seul : le prochain restart relit le code corrigé).
4. Test de validation : `curl <url>` ne doit plus renvoyer 502. Handshake : POST initialize avec `Accept: application/json, text/event-stream` → JSON-RPC result. Un GET simple renvoie 406 (normal en Streamable HTTP, pas une erreur).
