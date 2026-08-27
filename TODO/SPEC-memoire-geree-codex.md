# SPEC — Mémoire gérée pour Codex

**Statut : remplacée le 27 août 2026.**

Cette SPEC du 15 juillet proposait plusieurs architectures avant l’usage réel de Codex. Elle ne doit plus guider une implémentation : elle mélangeait recall natif, mémoire contrôlée et écriture agentique depuis des hooks.

La source active est désormais :

- `TODO/SPEC-loop-second-brain-refresh.md` pour les invariants et critères d’acceptation ;
- `docs/second-brain/news-refresh.md` pour la veille et la correction du vault ;
- `docs/second-brain/session-capture.md` pour les apprentissages de session et le profil de Raphaël ;
- `memory/user_raphael_profile.md` pour les faits et préférences explicites ;
- la note vault `memoire-optimale-codex-chatgpt` pour la doctrine.

## Décisions qui remplacent l’ancienne SPEC

- La mémoire locale Codex reste un recall généré et non autoritaire.
- Le vault et `memory/` sont les couches contrôlées.
- Un hook peut détecter ou injecter, mais ne décide pas seul d’une mutation sémantique.
- Claude et Codex partagent les contrats, pas des copies intégrales de skills.
- Les hypothèses personnelles et les données sensibles nouvelles nécessitent une validation humaine.
- Une note nouvelle est proposée avant création ; aucune note n’est supprimée automatiquement.

L’historique antérieur reste disponible dans Git si une justification d’architecture doit être retrouvée.
