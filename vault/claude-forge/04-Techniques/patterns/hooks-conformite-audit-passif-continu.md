---
titre: "Hooks de conformité par construction = audit passif continu"
resume: "Les hooks de conformité (delegate-guard, meta-commentary-detector, etc.) ne sont pas que des gardes : ils font office d'audit passif permanent. Quand un hook bloque une action prévue et légitime, il révèle souvent une dette préexistante. Doctrine : ne jamais contourner — profiter du blocage pour nettoyer dans la même passe."
aliases:
  - "hooks audit passif"
  - "blocage hook revele dette"
  - "conformite par construction audit"
  - "hook compliance passive audit"
  - "ne jamais contourner un hook"
  - "hook block reveals tech debt"
type: pattern
domaine: claude-code
derniere-maj: 2026-05-27
auteur: claude
tags:
  - "#type/pattern"
  - "#domaine/claude-code"
  - "#domaine/hooks"
---

# Hooks de conformité par construction = audit passif continu

## Le pattern

Un hook de conformité (`delegate-guard`, `meta-commentary-detector`, `security-guard`...) qui bloque par construction (exit 2) ne protège pas seulement l'action courante : il **scanne et juge l'état existant à chaque déclenchement**. C'est un audit passif permanent, gratuit, qui tourne à chaque Edit/Write.

Conséquence non-évidente : **quand un hook bloque une action prévue et légitime, le blocage révèle souvent une dette préexistante** — une violation qui dormait dans le fichier avant ton action, et que le hook vient d'exposer en scannant l'ensemble.

## Doctrine

1. **Ne jamais contourner** un blocage de hook de conformité (pas de bypass env-var, pas de `.proposed` de complaisance, pas de désactivation temporaire).
2. **Traiter le blocage comme un audit qui vient de trouver quelque chose** : lire ce qu'il signale, distinguer ma modification de la dette préexistante.
3. **Nettoyer la dette révélée dans la MÊME passe** — pas en rappel dans 2 semaines (cf le feedback `zero-dette-technique-nettoyer-completement`).
4. Si le blocage est un faux positif → durcir le hook (le critère est trop large), pas le contourner.

## Occurrences empiriques

1. **Phase 2 — `delegate-guard`** : audit a révélé que le hook lui-même avait un substring match sur `agent_id` (L143-145) = bypass indu. Le hook protégeait, mais son propre code contenait une faille de conformité. Caractérisé + fixé (exact-match), test inversé en regression guard. Cf [[bug-caracterise-fix-trivial-vs-couteux]].
2. **Session Mémoire Portable (27 mai 2026) — `meta-commentary-detector`** : en tentant d'ajouter la section `## Mémoire` à CLAUDE.md, le hook a bloqué sur une violation PRÉEXISTANTE L77 (`= tip #1 Boris`, attribution-source) qui dormait depuis des semaines. Nettoyée dans la même passe + autre attribution `Doctrine Anthropic "xhigh partout" = ...` L57 retirée par cohérence. La distinction attribution-source vs label-structurel a été capitalisée pour éviter les faux positifs sur les titres (cf [[erreur-meta-commentaires-composants]]).

## Réutilisation

Quand un hook bloque une action que tu pensais légitime : ne pas pester ni contourner. Lire le verbatim du blocage, identifier si c'est TA modif ou une dette préexistante. Si dette préexistante → l'audit passif vient de trouver, nettoie-la maintenant. C'est un avantage de la conformité par construction, pas un obstacle.

## Liens

- feedback `zero-dette-technique-nettoyer-completement` — doctrine connexe : nettoyer la dette révélée immédiatement
- [[erreur-meta-commentaires-composants]] — la dette révélée cette session (attribution-source)
- [[bug-caracterise-fix-trivial-vs-couteux]] — la dette révélée Phase 2 (delegate-guard substring)
- [[avantages-acquis-claude-forge-vs-hermes]] — "conformité par construction" comme avantage forge
