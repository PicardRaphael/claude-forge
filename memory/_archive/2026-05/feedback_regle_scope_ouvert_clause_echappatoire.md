---
name: regle-scope-ouvert-clause-echappatoire
description: "Regle LLM advisory : scope ouvert + clause echappatoire, sinon alibi de categorie"
metadata:
  type: feedback
---

Quand on redige une regle advisory pour un LLM (CLAUDE.md, rule, skill, doctrine), eviter 2 pieges :

1. **Scope ferme par liste de categories** ("AVANT toute X / Y / Z, faire ABC") — le LLM peut classer une demande hors X/Y/Z et s'auto-dispenser de la regle.
2. **Pas de clause d'echappatoire** ("consulter le vault AVANT") — si la condition est vide, le LLM peut se bloquer ou inventer un pretexte.

Les deux combines produisent un **alibi de categorie**.

**Fix teste sur CLAUDE.md L14** (v3, 28 mai 2026 — pas encore valide empiriquement, a confirmer en sessions suivantes) :
- Scope ouvert : "AVANT toute reponse substantielle a une question (proposition, redaction d'un ticket/commentaire/spec/explication, refonte, audit, jugement, recommandation, recherche web)"
- Clause echappatoire : "Si aucune note pertinente -> repondre quand meme, mais avoir cherche d'abord"

**Why:** Hypothese formulee 28 mai apres 2 incidents sur CLAUDE.md L14 (24 mai 40 tours skip vault + 28 mai 14 iterations redaction commentaire ticket). N=1 sur le meta-pattern (meme regle, 2 versions). Les 2 incidents auraient pu etre resolus par un simple ajout d'exemple "redaction de ticket" dans la liste fermee — l'attribution "scope ouvert = fix" reste non isolee. Cf [[erreur-vault-jamais-consulte-session-principale]].

**How to apply:** Quand tu rediges une regle advisory comportementale ("AVANT de repondre, fais X"), preferer formulation large + clause d'echappatoire a liste fermee de categories. **Promouvoir vault uniquement apres 2-3 occurrences sur des regles distinctes** (pas 2 versions de la meme regle). Pour l'instant : regle empirique, a valider en sessions suivantes.
