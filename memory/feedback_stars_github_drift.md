---
name: stars-github-drift-x3-x6-six-mois
description: "Stars GitHub repos populaires AI/LLM peuvent drifter x3-x6 en 6 mois (DeepEval 5K→15.6K, MLX 4K→26K). Re-vérifier systématiquement lors d'audit thématique."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9d187182-be69-4f77-822a-84b8ce7a1e5c
---

**Règle** : Les stars GitHub d'un repo populaire dans l'écosystème IA/LLM peuvent doubler/tripler/sextupler en 6 mois. Re-vérifier systématiquement via WebFetch lors d'audits thématiques vault, ne JAMAIS se fier au chiffre noté.

**Why** : Audit fine-tuning 23 mai 2026 a révélé :
- DeepEval : 5K → 15.6K (×3, écart depuis nov 2025)
- MLX (Apple) : 4K → 26.4K (×6, écart depuis dec 2024)
- Unsloth : 54K → 65K
- LLaMA-Factory : 68K → 71.5K
- Label Studio : 20K → 27K

Le drift est asymétrique : repos en hype récente (DeepEval RAG/agentic eval, MLX Apple Silicon) explosent, repos établis stagnent ou montent linéairement.

**How to apply** :
- Audit thématique vault : si la note date >3 mois et cite stars GitHub, lancer WebFetch systématique
- Brief sub-agents auditeurs : "tolérance ±5K pour stars, mais WebFetch obligatoire pas se fier au noté"
- À l'écriture d'une note tech, dater explicitement les stars : "~15K stars (mai 2026)"
- Ne pas réutiliser un chiffre stars sans timestamp

**Sister rules** : [[verify-exhaustive-claims]], [[tweet-hype-paraphrase-non-verifiee-pattern]]
