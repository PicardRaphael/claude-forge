---
name: advisor-da-web-search
description: "Advisor et devil's advocate devraient pouvoir chercher sur internet quand ils ne sont pas sûrs d'un point technique"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 405aaef3-b4d6-4ba2-9292-03dc7f0bab67
---

Quand advisor ou devil's advocate doutent d'un fait technique (ex: quel champ le runtime CC injecte dans le JSON stdin des hooks), ils devraient pouvoir chercher sur internet pour vérifier au lieu de se baser uniquement sur la mémoire et le vault.

**Why:** Session 2026-05-21 : le DA a identifié correctement que le champ `agent_type` vs `subagent_type` n'était pas vérifié empiriquement, mais n'a pas pu chercher en ligne pour trancher. Le claude-code-guide agent a dû être lancé séparément pour trouver la doc.

**How to apply:** Quand un point technique est incertain pendant advisor/DA, lancer une recherche web (cc-news, WebSearch, ou claude-code-guide) AVANT l'advisor/DA pour fournir les faits vérifiés dans le prompt. Ou envisager d'ajouter WebSearch aux tools du DA.

**Extension (2026-06-09) — vaut aussi pour toute affirmation technique quantitative à Raphael, pas seulement advisor/DA.** Affirmer une **cadence / fréquence / seuil / version** de mémoire (ex : « mutation testing = hebdomadaire seulement ») = risque de demi-vérité, surtout si ça part dans un livrable gravé (CDC, ticket). Réflexe : WebSearch AVANT d'affirmer. Et si la recherche corrige une affirmation déjà faite à Raphael → **surfacer l'écart explicitement** (« tu pensais X, l'état de l'art c'est Y, voici pourquoi »), jamais basculer en silence (advisor verbatim 2026-06-09). Cas réel : « hebdo seulement » → réalité = deux étages (incrémental scopé par PR + full planifié). Cf [[feedback_verify_avant_affirmation_session]] (changements repo) — ici c'est un fait technique externe. Distinct mais même famille : mémoire session ≠ source de vérité.
