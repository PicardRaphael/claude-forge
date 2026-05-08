---
titre: "LLM Wiki — Pattern Karpathy"
resume: "100 articles, 400K mots plain text, 70x plus efficient que RAG pour organiser la connaissance"
aliases:
  - "llm wiki"
  - "karpathy wiki"
domaine: technique
type: technique
derniere-maj: 2026-04-21
auteur: claude
sources: []
tags:
  - "#type/technique"
  - "#domaine/technique"
---

## Description

Pattern d'[[Andrej Karpathy]] (avril 2026). Utiliser les LLMs pour organiser la connaissance plutôt que générer du code.

## Quand utiliser

Quand on a besoin d'organiser un corpus de connaissances large. Alternative à RAG pour les bases de connaissances personnelles.

## Specs

- ~100 articles, 400K mots
- Plain text (pas de base vectorielle)
- 70x plus efficient que RAG
- Maintenance : LLM organise, humain valide

## Exemple

Un wiki personnel de ~100 articles couvrant un domaine (ex: droit immobilier, compliance, stack technique). Chaque article = ~4000 mots. Le LLM organise les articles (structure, cross-references, sommaire), l'humain valide le contenu.

## Lien avec forge-brain

Ce vault est inspiré du même principe : knowledge base structurée, notes atomiques, cross-linkée, plain text Obsidian.

## Liens

- [[MOC-Techniques]]
- [[Andrej Karpathy]]
