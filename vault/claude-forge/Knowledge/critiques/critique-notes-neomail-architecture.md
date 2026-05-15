---
titre: "Critique — Notes architecture NeoMail (2 notes vault)"
type: knowledge
domaine: neo_ia
derniere-maj: 2026-05-11
auteur: claude
aliases:
  - "critique neomail architecture"
  - "critique notes neomail"
  - "devil advocate neomail archi"
tags:
  - "#type/knowledge"
  - "#domaine/neoteem"
resume: "Critique DA des 2 notes architecture NeoMail — webhook pipeline et architecture. Objections et recommandations sur la documentation vault."
---

## Verdict : LIVRER TEL QUEL

Le devil's advocate a vérifié les 2 notes NeoMail contre le code source. Résultat :

- **Blueprint** : correspond exactement au code (`blueprint.py` L18-36)
- **Pipeline webhook** : les 10 étapes correspondent au flow dans `webhook_handler.py`
- **21 tools** : confirmé via `ToolPromptLoader.get_tools_for_agent("neomail")` dans `builder.py`
- **Différences NeoChat vs NeoMail** : tableau exact (pas d'historique, pas de suggestions confirmé dans `streaming.py`)
- **BROUILLON ONLY** : les 5 niveaux d'enforcement sont présents dans le code

## Points mineurs notés

- Les handlers NeoMail sont instanciés sans arguments (contrairement à Universal qui passe des sets de tools) — correct car NeoMail utilise les defaults
- La note mentionne que MailPreviewHandler n'a pas de `confirm_messages` passé — c'est exact dans le code, les defaults suffisent

## Liens

- [[neomail-architecture]]
- [[neomail-webhook-pipeline]]
- [[critique-notes-neochat-architecture]]
