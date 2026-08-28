# SPEC — Mémoire gérée pour Codex

**Statut : remplacée le 27 août 2026.**

Cette SPEC du 15 juillet proposait plusieurs architectures avant l’usage réel de Codex. Elle ne doit plus guider une implémentation : elle mélangeait recall natif, mémoire contrôlée et écriture agentique depuis des hooks.

La source active est désormais :

- `TODO/SPEC-loop-second-brain-refresh.md` pour les invariants et critères d’acceptation ;
- `docs/second-brain/news-refresh.md` pour la veille et la correction du vault ;
- `docs/second-brain/session-capture.md` pour les apprentissages de session et le profil de Raphaël ;
- la note vault `Raphael-Picard` et ses casquettes pour les faits et préférences explicites ;
- `memory/user_raphael_profile.md` comme adaptateur de compatibilité sans biographie dupliquée ;
- la note vault `memoire-optimale-codex-chatgpt` pour la doctrine.

## Décisions qui remplacent l’ancienne SPEC

- La mémoire locale Codex reste un recall généré et non autoritaire.
- Le vault est canonique pour le profil, les projets, les décisions et la doctrine ; `memory/` garde adaptateurs, incidents précis et phases temporaires.
- Un hook peut détecter ou injecter, mais ne décide pas seul d’une mutation sémantique.
- Claude et Codex partagent les contrats, pas des copies intégrales de skills.
- Les hypothèses personnelles et les données sensibles nouvelles nécessitent une validation humaine.
- Une demande explicite de création de projet ou `/done` peut créer le foyer non sensible clairement requis ; aucune note n'est supprimée automatiquement.

L’historique antérieur reste disponible dans Git si une justification d’architecture doit être retrouvée.
