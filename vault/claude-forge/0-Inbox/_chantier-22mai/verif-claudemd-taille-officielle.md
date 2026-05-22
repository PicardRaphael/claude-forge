---
titre: "Vérification — Taille officielle CLAUDE.md selon Anthropic"
resume: "Anthropic recommande officiellement 'target under 200 lines per CLAUDE.md file' dans la doc memory — claim VRAIE, sémantique = recommandation (pas hard limit)"
aliases: ["verif claudemd taille", "claudemd 200 lignes", "claudemd size officiel", "claude-md sweet spot"]
derniere-maj: 2026-05-22
auteur: claude
tags: ["#type/verification", "#domaine/claude-code"]
---

# Verdict

**Claim VRAIE** — confirmée à la source primaire Anthropic, formulation exacte = "target under 200 lines per CLAUDE.md file".

Nuance importante : c'est une **recommandation** ("target"), pas une **hard limit**. Au-delà = "consume more context and reduce adherence", pas un blocage technique.

# Citations verbatim

## Source 1 — docs.claude.com/en/docs/claude-code/memory (redirigé vers code.claude.com/docs/en/memory)

Section "Write effective instructions" :

> **Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence. If your instructions are growing large, use path-scoped rules so instructions load only when Claude works with matching files. You can also split content into imports for organization, though imported files still load and enter the context window at launch.

URL canonique : https://code.claude.com/docs/en/memory (ancienne docs.claude.com/en/docs/claude-code/memory → 301 permanent)

Section "My CLAUDE.md is too large" (troubleshooting) confirme :

> Files over 200 lines consume more context and may reduce adherence. Use path-scoped rules to load instructions only when Claude works with matching files, or trim content that isn't needed in every session. Splitting into @path imports helps organization but does not reduce context, since imported files load at launch.

Note auto-memory (table CLAUDE.md vs Auto Memory) :

> Loaded into: Every session (first 200 lines or 25KB)  ← s'applique à MEMORY.md, PAS à CLAUDE.md
> This limit applies only to MEMORY.md. CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence.

→ Distinction critique : CLAUDE.md = pas de troncature ("loaded in full"), juste recommandation 200L. MEMORY.md (auto-memory) = vraie limite hard 200L/25KB.

## Source 2 — code.claude.com/docs/en/best-practices

Pas de chiffre explicite mais doctrine cohérente :

> Keep it concise. For each line, ask: "Would removing this cause Claude to make mistakes?" If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!

Anti-pattern nommé "The over-specified CLAUDE.md" :

> If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise.
> **Fix**: Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook.

# Tableau croisé sources

| Source | Chiffre | Sémantique | Niveau d'autorité |
|---|---|---|---|
| docs.claude.com/memory (officiel) | **< 200 lignes** | "target" (recommandation) | PRIMAIRE Anthropic |
| code.claude.com/best-practices | Pas de chiffre, "concise" | "ruthlessly prune" | PRIMAIRE Anthropic |
| HumanLayer blog | ~60 lignes (leur root) | Pratique terrain | Tiers (cité par recherche) |
| Builder.io / TurboDocx (tiers) | < 300 lignes max, 200 sweet spot | Consensus communauté | Tiers |
| forge CLAUDE.md actuel | "~100L max" | Règle interne | Notre doctrine |
| Note vault `pattern-claude-md` (si existe) | À vérifier | — | Forge |

**Pas de divergence Anthropic ↔ Anthropic** : un seul chiffre officiel = 200. Les "300 max" viennent uniquement de tiers (Builder.io, TurboDocx).

# Réponses aux questions précises

1. **Anthropic recommande EXPLICITEMENT une taille ?** OUI — "target under 200 lines per CLAUDE.md file"
2. **URL exacte** : https://code.claude.com/docs/en/memory — section "Write effective instructions" → "Size". Page récente (refonte navigation docs.claude.com → code.claude.com en cours, redirect 301 actif). Pas de "last updated" visible mais contenu inclut features 2026 (auto memory v2.1.59+, `claudeMd` key in managed settings).
3. **Divergences Anthropic** : aucune. Le 200 est répété 2× dans la même page (recommandation + troubleshooting "too large").
4. **Sémantique "sweet spot"** : Anthropic dit "target under" (= recommandation). PAS de "hard limit". Conséquences nommées : "consume more context", "reduce adherence", "Claude ignores half of it". Soft warning, pas blocage.
5. **Anti-patterns officiels** :
   - "The over-specified CLAUDE.md" (best-practices page) — fix = ruthlessly prune ou convertir en hook
   - "Bloated CLAUDE.md files cause Claude to ignore your actual instructions" (memory page)
   - Test verbatim : "Would removing this cause Claude to make mistakes? If not, cut it."

# Conclusion exploitable

Pour rédiger une note canonique CLAUDE.md dans le vault forge :

- **Cible officielle Anthropic : < 200 lignes** (verbatim "target under 200 lines per CLAUDE.md file")
- **Pas une hard limit** — c'est une recommandation pour préserver adherence
- **Notre forge CLAUDE.md dit "~100L max"** : plus strict que l'officiel, OK (Boris HumanLayer = 60L, même direction)
- **Anti-pattern officiel** : "The over-specified CLAUDE.md" — convertir règles répétitives en hooks (cohérent avec notre doctrine "Hooks > Rules")
- **Test verbatim Anthropic** : "Would removing this cause Claude to make mistakes? If not, cut it." → identique au test déjà présent dans notre CLAUDE.md forge ("Would removing this cause mistakes? No → Remove")
- **Distinction critique à documenter** : 200 lignes = recommandation CLAUDE.md ; 200 lignes / 25KB = HARD limit auto-memory (MEMORY.md). Ne pas confondre.

Lien à créer dans la note canonique : [[pattern-claude-md]], [[Hooks-vs-Rules]], [[auto-memory]].
