---
name: regression-diagnostic-diff-avant-redesign
description: Régression à point d'introduction connu (réécriture) = diffuser AVANT de redesigner. Ne pas anchrer sur l'hypothèse user "trop gros".
trigger: regression, ne marche plus, casse, avant ca marchait, diff
metadata:
  type: feedback
---

Quand une régression a un **point d'introduction connu** (une réécriture, un commit, une migration daté), faire le **diff original→nouveau AVANT de proposer un redesign**. Bisecter le changement est plus rapide et plus sûr que refondre.

**Why:** Session 1er juin 2026, automatisation triage support LOJII (Cowork 7h). Hypothèse user = "le skill fait trop de choses, il faut diviser". L'advisor a flagué que mes propres données la contredisaient : tailles quasi identiques (402→418 L) et logique de classification byte-identique. Le diff a révélé la vraie cause : la réécriture avait migré la mémoire (learnings/retro) de **fichiers locaux bundlés** vers des **notes vault MCP jamais créées** — et Cowork ne peut pas écrire le vault en run planifié. Vérifié empiriquement : `read_note("learnings-triage")` → introuvable.

**How to apply:**
1. Si régression + point d'introduction connu → `diff` ciblé AVANT tout redesign. Cf [[feedback_brief_premisse_fausse_verifier_avant_executer]].
2. Ne jamais anchrer le plan sur l'hypothèse causale du user (souvent hedgée "potentiellement parce que…") — la tester matériellement.
3. Asymétrie runtime à checker : **lecture** vault peut marcher là où **écriture** échoue (headless vs interactif). Garder ce qui marche, ne migrer que ce qui casse.
4. Pour une boucle d'apprentissage (write→read), vérifier que le **write-path résout dans TOUS les points d'entrée** (un placeholder lié dans le prompt planifié reste non résolu en session interactive `/analyse`). Source unique = config.json lu partout.
5. Best practice triage IA 2026 (DevRev/Fini) : séparer raisonnement probabiliste (classification cohérente, 1 prompt) de l'exécution déterministe (mémoire/mappings/format en references). NE PAS fragmenter la classification en micro-skills.
