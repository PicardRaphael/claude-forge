---
titre: "Critique — 4 skills RAG + outils IA (cc-rag-ref, rag-design, choix-outils-ia, veille-outils-ia)"
resume: "DA conditionnel : un seul FIX-FIRST réel — collision de routage avec responsable-ia (pas amendé en réciproque). Reste = avertissements style description + tags source chiffres."
aliases:
  - critique 4 skills RAG juin 2026
  - DA cc-rag-ref rag-design choix-outils-ia veille-outils-ia
  - collision responsable-ia routage
  - critique skills RAG outils IA
  - devils advocate RAG 17 juin
type: knowledge
domaine: claude-code
derniere-maj: 2026-06-17
auteur: claude
tags:
  - "#type/critique"
  - "#domaine/claude-code"
sources:
  - "[[e-descriptions-keyword-stuffing]]"
  - "[[comment-creer-skill]]"
---

## Devils Advocate — 4 skills RAG + outils IA

**Intention déclarée :** doter forge d'un corpus RAG en contexte (cc-rag-ref), d'un dialogue de conception RAG (rag-design), d'un cadrage build-vs-buy opérationnel (choix-outils-ia) et d'une maintenance des notes-paysage marché sous gate humain (veille-outils-ia), avec des frontières anti-doublon explicites.

### Verdict

**Bloquants :** 0 | **Avertissements :** 3 | **Nitpicks :** 3
**Décision recommandée :** LIVRER AVEC CORRECTIONS (1 fix-first : disambiguation réciproque de responsable-ia)

### Le seul écueil à corriger avant SHIP — collision de routage avec responsable-ia

Les 4 nouvelles skills disambiguent vers le bas (chacune dit « NOT for ... responsable-ia »). Mais `responsable-ia` est antérieure et n'a PAS été amendée en réciproque : sa description déclenche sur « build vs buy », « RAG/agent architecture for Loji (NeoChat, NeoDocs) », « agent Loji », « feature IA ». Donc :
- « build ou buy pour de l'OCR » → peut faire feu sur `choix-outils-ia` ET `responsable-ia`.
- « architecture RAG NeoDocs » → `rag-design` ET `responsable-ia`.
Deux skills en `ALWAYS invoke` sur la même intention = non-déterminisme de routage. **Fix = une ligne** dans la description de `responsable-ia` : ajouter « NOT for the operational tool choice (choix-outils-ia), NOT for technical RAG conception (rag-design) — responsable-ia = strategic CODIR decision only. » Sans ça, la frontière documentée ne tient pas au runtime.

### Ce qui NE casse PAS (faux positifs écartés)

- **cc-rag-ref (false) vs rag-design (true) sur « RAG »** : pas une collision. cc-rag-ref est `user-invocable:false` (se charge en contexte), rag-design l'invoque explicitement `Skill(cc-rag-ref)` au démarrage. Co-firing intentionnel.
- **Longueur des descriptions** (333/382/429/447 chars) : NON bloquant. La règle « ~250 chars sinon /skills tronque → auto-trigger cassé » (note `e-descriptions-keyword-stuffing`, 2026-04-23) est PÉRIMÉE : les 4 descriptions s'affichent en entier dans la liste skills de la session courante (CC 2.1.167). Le brief autorise ≤1024 chars. Seul coût réel = ~150 tokens de démarrage cumulés (de minimis vs 6.8k baseline). Avertissement, pas bloquant.
- **Chiffres Contextual Retrieval -35/-49/-67** : valeurs Anthropic FIXES, pas volatiles comme pricing/⭐. L'architecture est cohérente (faits stables embarqués, faits volatils en vault via veille). Pas un drift single-source.

### Avertissements

- **AVERTISSEMENT — quoted FR phrases dans 2 descriptions** : `choix-outils-ia` et `veille-outils-ia` portent 5-6 formulations entre guillemets (« je veux de la voix/TTS/OCR », « rafraîchis la veille »...). C'est l'anti-pattern documenté `e-descriptions-keyword-stuffing` (matching sémantique ≠ keyword) ET en tension avec la doctrine du brief « 3e personne directive ». Dilué (les verbes d'intention sont présents) mais à trimmer : garder les verbes, couper les citations.
- **AVERTISSEMENT — responsable-ia non amendé** (cf fix-first ci-dessus, classé ici comme la cause).
- **AVERTISSEMENT — chiffres embarqués sans tag de provenance inline** : ajouter un marqueur source (« source Anthropic ») COLLÉ aux -35/-49/-67 dans cc-rag-ref pour qu'un futur lecteur ne tente pas de les « rafraîchir » via veille-outils-ia (qui ne touche QUE les notes-paysage, pas cette skill).

### Nitpicks

- NITPICK — veille-outils-ia : gate humain par item présent (diff `[v]/[m]/[i]`, « jamais en bloc » étape 4 + Gotchas). C'est de la prose advisory non enforced, mais post-pivot 22 mai interdit les hooks de workflow → advisory est le plafond accepté. OK.
- NITPICK — chaîne references = 1 niveau (SKILL → references/*.md → vault via MCP read_note = appel data, pas chaîne de fichiers). Conforme.
- NITPICK — vérifier que les 11 stems de rag-corpus.md résolvent (RAG + leaders confirmés ; spot-check les autres au prochain run).

### Si je devais le faire marcher malgré mes objections

1. **Amender `responsable-ia`** (via skill-creator, delegate-guard bloque l'edit direct) : ajouter la phrase de disambiguation réciproque. C'est le seul changement bloquant le SHIP.
2. Trimmer les citations FR dans `choix-outils-ia` + `veille-outils-ia`, garder les verbes d'intention.
3. Taguer « (source Anthropic) » inline sur les -35/-49/-67 de cc-rag-ref.
Les 3 corrections sont chirurgicales — aucune refonte.

### Vault — historique pertinent

`e-descriptions-keyword-stuffing` (2026-04-23) — anti-pattern citations dans descriptions, toujours valide sur le VOLET style (citations FR) ; PÉRIMÉ sur le volet longueur (truncation /skills non reproductible en CC 2.1.167). Aucune critique antérieure sur ces 4 skills (net-neuf).
