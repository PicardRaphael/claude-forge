---
titre: "Skills externes (marketplace) — upstream sync, jamais fabriquer"
resume: "Asset manquant dans une skill installée depuis un marketplace (kepano/obsidian-skills) = WebFetch/sync verbatim depuis upstream, jamais inventer le contenu localement."
aliases:
  - "obsidian-skills-sacred"
  - "skills externes intouchables"
  - "upstream sync skill marketplace"
  - "asset manquant skill kepano"
  - "fabrication asset interdite"
  - "sync verbatim upstream"
domaine: claude-code
type: doctrine
derniere-maj: 2026-07-07
auteur: claude
sources:
  - "Incident 27 mai 2026 — json-canvas/references/EXAMPLES.md (kepano/obsidian-skills)"
  - "memory/feedback_sync_skill_upstream_pas_fabriquer.md"
  - "memory/feedback_skills_externes_intouchables.md"
tags:
  - "#type/doctrine"
  - "#domaine/claude-code"
  - "#domaine/skills"
---

# Skills externes (marketplace) — upstream sync, jamais fabriquer

## Règle canonique

Quand une skill installée depuis un marketplace (ex : `kepano/obsidian-skills`) référence un asset (`references/EXAMPLES.md`) absent de notre copie locale, l'asset a été perdu lors de la copie/installation — il existe upstream. **Ne jamais fabriquer le contenu localement.**

## Pourquoi c'est critique

Fabriquer localement crée un fork silencieux :
- Si upstream publie l'asset plus tard → conflit garanti
- Si on a inventé du contenu pour combler un dangling ref → on le maintient à vie sans contrôle
- Diff minimal > authoring : le contenu upstream est la source de vérité, pas notre imagination

**Cas réel (27 mai 2026)** : allais fabriquer `json-canvas/references/EXAMPLES.md` — l'advisor a stoppé. Vérification : `kepano/obsidian-skills` avait bien le fichier (6 476 octets). Récupéré verbatim.

## Procédure — asset manquant dans skill marketplace

1. **Vérifier l'arbre upstream** : `GET api.github.com/repos/<owner>/<repo>/git/trees/main?recursive=1`
2. **Asset existe upstream** → télécharger verbatim (`Invoke-WebRequest raw.githubusercontent.com/<owner>/<repo>/main/<path>`, vérifier taille bytes serveur == bytes fichier)
3. **Asset absent upstream aussi** (dangling chez eux) → retirer la référence locale, pas fabriquer

> ⚠️ **WebFetch paraphrase** (petit modèle) — pour du contenu verbatim (code, exemples, templates), utiliser `Invoke-WebRequest` ou `curl`, jamais WebFetch.

## Skills externes = copies read-only

Les skills kepano (`json-canvas`, `defuddle`, `obsidian-markdown`, `obsidian-bases`, `obsidian-cli`) sont des **copies read-only** de l'upstream. Doctrine complémentaire :
- **JAMAIS modifier le SKILL.md** de ces skills externes
- Déclenchement custom → `.skill-triggers.json` uniquement (cf `memory/feedback_skills_externes_intouchables.md`)
- Mises à jour → re-sync depuis upstream, jamais édition locale

## Wikilinks

- [[plugin-vs-skill-anatomie]] — anatomie plugin vs skill, distribution marketplace
- [[comment-creer-skill]] — création skills forge (distinctes des skills externes)
- [[mcp-vs-skills-doctrine]] — MCP data / skills how-to
