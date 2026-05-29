---
name: settings-local-env-secret-pattern
description: "settings.json référence ${GCHAT_WEBHOOK_URL} mais doit être résolu depuis settings.local.json (gitignored) section env. Si settings.local.json sans section env → hook exit silently sans erreur"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e91e446c-e32c-4517-ab41-e1e4c5555314
---

# settings.local.json section `env` pour secrets de hooks

## La règle

Pattern Claude Code pour secrets utilisés par hooks (webhooks, API keys) :

1. **`.claude/settings.json`** (versionné) : référence `${VAR_NAME}` dans la section `env`
2. **`.claude/settings.local.json`** (gitignored) : définit la valeur réelle dans `env.VAR_NAME`
3. **Hook Python/TS** : lit `os.environ.get("VAR_NAME", "")` et exit silently si vide

Si étape 2 oubliée → hook exit 0 silencieux, aucune erreur, aucune notif. Diagnostic difficile car le hook "fonctionne" du point de vue Claude Code.

## Why

Validé empiriquement 26 mai 2026 :
- Push neo_ia + ia_back parallèle → notif Google Chat ia_back OK, neo_ia silent
- Hooks `on-push-notify.py` (neo_ia) et `.ts` (ia_back) configurés identiquement dans settings.json
- Différence : `settings.local.json` ia_back contenait `env.GCHAT_WEBHOOK_URL` réel, neo_ia non
- Hook neo_ia ligne 9-11 : `if not WEBHOOK_URL: sys.exit(0)` = silent skip
- Fix : ajouter section `env` dans `neo_ia/.claude/settings.local.json` avec URL identique → notif fonctionne immédiatement

## How to apply

Quand on déploie un hook utilisant une variable d'env sur un nouveau repo :

1. Copier le hook + sa registration `settings.json`
2. **CRITIQUE** : copier la section `env.<VAR>` dans `settings.local.json` cible
3. Vérifier `.gitignore` exclut `settings.local.json` (sinon secret leak)
4. Tester empiriquement : `echo '{...}' | uv run python .claude/hooks/<hook>.py` avec `VAR=...` injecté
5. Si silent silent : grep `os.environ.get` dans le hook pour identifier la variable manquante

## Diagnostic pattern silent-skip

Quand un hook ne déclenche aucune notif visible :

```bash
# 1. Hook bien registered ?
grep "<hook-name>" .claude/settings.json

# 2. Section env présente dans settings.json ?
python -c "import json; print(json.load(open('.claude/settings.json')).get('env',{}))"

# 3. Section env présente dans settings.local.json ?
cat .claude/settings.local.json | grep -A1 "env"

# 4. Test direct hook avec env injecté
VAR=value bash -c 'echo "{...}" | uv run python .claude/hooks/<hook>.py'
```

## Anti-patterns à éviter

- ❌ Commit `settings.local.json` contenant secret (vérifier .gitignore AVANT)
- ❌ Hardcoder URL/token dans `.py` ou `.ts` (perd portabilité + leak si commit)
- ❌ Exit silent sans log au moins en mode debug (impossible à diagnostiquer)
- ❌ Supposer que le hook marche parce que pas d'erreur (silent skip = pas erreur)

## Wikilinks

- [[critique-2026-05-24-regex-source-faux-positifs]] — scope per-repo
- [[erreur-password-postgres-clair-mcp-json]] — pas de secret dans configs versionnés
- [[feedback_claim_security_must_be_provable]] — sécu prouvable
