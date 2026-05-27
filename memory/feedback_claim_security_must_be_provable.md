---
name: claim-security-must-be-provable-by-code
description: "Toute description skill/agent qui claim un contrat sécurité (\"read-only\", \"sandboxed\", \"no write\", \"enforced by construction\") DOIT être prouvable par le code, pas juste par convention"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8957d13-cb6a-43d0-ae69-71bb7fa375a2
---

Toute description skill/agent qui claim un contrat sécurité — "read-only enforced", "sandboxed", "no write methods exposed", "by construction" — DOIT être prouvable structurellement par le code. Sinon utiliser "by discipline" pour être honnête.

**Why:** Session 2026-05-20, skill x-read description disait "Read-only enforced by construction — no write methods exposed". Or reader.py importe `Account` class qui a `tweet()`, `like()`, `follow()` accessibles en RAM via l'objet. C'est read-only **par discipline** (le CLI main() ne route pas vers ces methods), pas **par construction**. Le DA a tagué cette régression comme bloquante — claim faux = perte de confiance, et vecteur d'attaque réel via prompt injection sur tweet capté.

**How to apply:**
- Avant d'écrire "read-only", "no write", "sandboxed", "enforced" dans une description : grep le code pour vérifier que c'est structural
- Si le code importe une classe full-access (ex: `Account` au lieu de `Scraper`) → écrire "by discipline" pas "by construction"
- Pour un vrai read-only structural : créer une subclass qui override les write methods en `raise NotImplementedError` + test unitaire
- Ne pas confondre "n'appelle pas X" (discipline) avec "ne peut pas appeler X" (construction)
- Check-list DA à étendre : tout claim sécu doit avoir une ligne de code qui le prouve, sinon EVOLVE BLOQUANT
- Vecteur d'attaque concret : skill multimodale qui lit du contenu user-generated (tweet, web page) → prompt injection peut demander Claude d'éditer le fichier pour appeler une write method existante en RAM

Voir [[critique-session-2026-05-20-running-notes-decompose-xread-mcp]] dans le vault.
