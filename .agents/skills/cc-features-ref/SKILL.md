---
name: cc-features-ref
description: Load when Codex must answer about current Claude Code features. Reads the Claude-native reference and requires cc-news for any possibly stale claim.
---

# Claude Code features — adaptateur Codex

Lire **en entier** `.claude/skills/cc-features-ref/SKILL.md`.

Cette copie ne porte volontairement aucun catalogue : elle évite le mojibake et
la dérive des dates entre `.claude` et `.agents`.

Pour toute feature, version, modèle, événement hook ou commande susceptible
d'avoir changé, invoquer `cc-news` et privilégier les sources Anthropic
officielles avant de répondre ou de corriger le vault.
