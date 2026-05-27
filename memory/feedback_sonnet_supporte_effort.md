---
name: sonnet-46-supporte-effort-parameter
description: "Sonnet 4.6 SUPPORTE effort (low/medium/high/max). Default high. xhigh = Opus 4.7 only. Fallback auto vers high. JAMAIS dire \"effort sur Sonnet = code mort\"."
metadata: 
  node_type: memory
  type: reference
  originSessionId: a4e196c9-ffac-4668-a189-2e0902c13357
---

Erreur commise 26 mai 2026 : j'ai affirmé que `effort:` sur Sonnet = code mort. **FAUX**.

**Why** : Sonnet 4.6 est le **premier Sonnet à supporter effort**. Niveaux : low / medium / high / max. Default = `high`. Seul `xhigh` est exclusif à Opus 4.7. Si on met `xhigh` sur Sonnet → fallback automatique vers `high`.

**Verbatim Anthropic** :
> "Effort is supported on Opus 4.7, Opus 4.6, and Sonnet 4.6. Sonnet 4.6 is the first Sonnet model to support the effort parameter."

**Precedence** : env var > --effort flag > frontmatter > parent default.

**How to apply** :
- Garder `effort:` dans frontmatter Sonnet (PAS retirer)
- Pour économiser tokens sur agents Sonnet mécaniques (scan, maintenance, inspection) : passer high → `medium` ou `low`
- Pour agents Sonnet code complexe (devs) : garder `high`
- Pour critères de calibrage : voir [[effort-opus-47-doctrine-anthropic-2026]] note vault

**Lien feedback** : [[opus47-workflow-decisions]] (à mettre à jour aussi)
