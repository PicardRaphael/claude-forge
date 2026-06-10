# Relance d'un sub-agent après escalade — resume ou re-brief riche, JAMAIS un prompt nu

Chaque invocation `Agent()` démarre un contexte VIERGE : relancer un agent après une escalade avec seulement « voici la réponse, continue » force une ré-exploration complète (fichiers relus, recherches refaites — coût × chaque aller-retour).

1. **Resume d'abord** : reprendre le MÊME agent (`SendMessage` vers son nom/id, ou `resume` `agent_id` — CC ≥ 2.0.28, transcript `agent-<id>.jsonl`). Même en resume, re-donner le cadrage (tâche + objectif) — le transcript ne conserve pas toujours les prompts initiaux.
2. **Sinon re-brief riche** : la relance embarque le rapport / « État actuel » du run précédent + la réponse + les fichiers déjà identifiés, avec la consigne « ne refais pas l'exploration, repars de cet état ».
3. **La session principale injecte le contexte, l'agent ne le re-cherche pas** — elle lit les rapports précédents et n'injecte QUE le pertinent (dense, pas exhaustif).
4. Symétriquement : tout brief d'agent susceptible d'escalader exige un bloc d'escalade avec « État actuel » + « Suite recommandée » complets.

Canonique (pourquoi, bugs connus du resume, sources) : vault [[anti-reentrance-sub-agents-pattern-escalade]] section AJOUT 10 juin 2026. Déployé aussi : neoteem-back-ts (`rules/agent-relaunch-context.md`) + neo_ia (`rules/sub-agent-patterns.md` § Relance).
