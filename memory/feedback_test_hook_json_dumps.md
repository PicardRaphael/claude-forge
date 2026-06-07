---
name: test-hook-json-dumps
description: Tester un hook = JSON via json.dumps (jamais à la main, \U/\D Windows casse). Logique≠armement.
metadata:
  type: feedback
---

Pour tester un hook PreToolUse qui lit `tool_input.file_path` (ou `command`), construire le payload stdin avec **`json.dumps` en Python**, JAMAIS écrire le JSON à la main dans le shell.

**Why:** 7 juin 2026, test du hook `vault-write-guard`. Le CAS 1 (Edit note vault → doit bloquer) sortait `exit 0` au lieu de `exit 2` — faux négatif alarmant. Cause : le JSON tapé à la main contenait un chemin Windows `C:\Users\...\Documents\...` ; `\U`, `\D` ne sont PAS des échappements JSON valides → `json.load` lève → le hook **fail-open (exit 0)** par design → le fail-open a MASQUÉ le test (on croyait tester le hook, on testait un JSON cassé). Même classe de bug que « Bash mange `\\U` dans settings.json » (cf [[reference_auto_mode_classifier]] section backslash Windows), mais ici côté harnais de test.

**How to apply:**
- Harnais de test d'un hook : `payload = {...}; js = json.dumps(payload); subprocess.run([...], input=js)`. Les backslashes Windows sont échappés correctement par `json.dumps`. Jamais de JSON littéral écrit à la main avec un chemin Windows dedans.
- Distinguer DEUX preuves complémentaires, les deux nécessaires :
  - **LOGIQUE du script** = invocation directe / isolation (`py hook.py < json`). Déterministe, observable, zéro effet de bord. Prouve que le code décide juste.
  - **ARMEMENT / câblage** = vrai Edit (ou vrai appel d'outil) via le harness. Prouve que `settings.json` câble bien le hook (matcher, enregistrement) — un hook au code parfait mais mal matché ne s'arme pas.
- Un hook qui `fail-open` (exit 0 sur exception) NE révélera JAMAIS un bug de harnais de test : il avale silencieusement le JSON cassé. Toujours vérifier que le JSON parse côté Python AVANT de conclure « le hook ne bloque pas ».

Cf [[feedback_hook_vs_harness_permission_distinction]] (bypass hook ≠ bypass harness).
