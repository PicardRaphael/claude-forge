---
name: user-invocable-orthographe
description: La forme officielle Anthropic du champ frontmatter skill est `user-invocable` (avec un c), PAS `user-invokable`. Vérifié sur code.claude.com/docs/en/skills. Défaut = true (visible dans menu /).
metadata:
  type: reference
---

Le champ frontmatter SKILL.md qui contrôle la visibilité dans le menu `/` s'écrit **`user-invocable`** (avec un `c`), pas `user-invokable` (avec un `k`). Source primaire : `code.claude.com/docs/en/skills` (table frontmatter) :
> `user-invocable` — Set to `false` to hide from the `/` menu. Default: `true`.

L'autre champ d'invocation est `disable-model-invocation: true` (empêche Claude de charger la skill automatiquement).

**Why:** Le 3 juin 2026, j'ai "corrigé" à tort le `user-invocable` (correct) d'une skill de Marie-Laure en `user-invokable`, en me fiant à "ce que forge utilise majoritairement" — or 37 fichiers forge ET la skill `cc-skills-ref` portaient la faute `user-invokable`. La majorité interne reproduisait l'erreur ; seule la doc Anthropic tranchait. Vérité ≠ consensus interne.

**How to apply:** Toujours `user-invocable` (avec c) dans tout frontmatter skill. Ne jamais valider une orthographe de champ frontmatter sur "ce que le repo utilise" — vérifier la doc Anthropic source primaire (cf [[feedback_llm_deep_research_version_numbers]] : source primaire avant d'agir, et [[feedback_verify_exhaustive_claims]]). Impact fonctionnel nul (champ inconnu ignoré, défaut true = visible) mais l'orthographe juste évite la repropagation via `cc-skills-ref`. Fix de masse appliqué le 3 juin (37 fichiers, 47 occ) via pattern [[feedback_python_script_refactor_masse]].
