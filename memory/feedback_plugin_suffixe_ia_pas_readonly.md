---
name: plugin-suffixe-ia-pas-readonly
description: "Suffixe `-ia` plugin n'est PAS read-only — verifier description verbatim allowed-tools avant d'absorber dans un -admin"
metadata:
  type: feedback
---

`neoteem-brain-dev-ia` est admin write a lui seul (description verbatim "Full vault access read+write via MCP obsidian-brain"), contrairement a `neoteem-brain-dev` qui est read-only. Le suffixe est specialisation domaine (IA stack), pas niveau d'acces.

**Why** : Step 6 audit plugins 28 mai 2026 — recommandation initiale "absorber dev-ia dans dev-admin" erronee. Raphael corrige : "dev-ia est admin a lui seul, pas besoin d'un dev-ia-admin". Confirme empiriquement par lecture SKILL.md.

**How to apply** : pour tout plugin avec `<X>-<suffix>`, lire la `description:` ET `allowed-tools:` du SKILL.md AVANT de raisonner sur l'absorption read-only/admin. Le suffixe (-ia, -support, -dev) indique le domaine ; le niveau d'acces (read-only vs admin) se lit dans la description verbatim et les tools. Lien : [[feedback_plugin_admin_absorbe_readonly]].
