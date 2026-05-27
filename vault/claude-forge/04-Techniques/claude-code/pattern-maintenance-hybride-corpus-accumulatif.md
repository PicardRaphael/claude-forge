---
titre: "Maintenance hybride d'un corpus accumulatif — déterministe + LLM + gate humaine"
resume: "Pattern canonique pour empêcher un corpus accumulatif (index mémoire, doctrine, FAQ, changelog) de se diluer : 3 couches déterministe (détection mécanique cheap) / LLM (clustering sémantique) / humain (gate [v]/[m]/[i] typée par section). Canonique vivante modifiable + archive append-only sacré. Anti enforcement-théâtre : pas de couche déterministe lourde sur corpus court/homogène."
aliases: ["maintenance hybride corpus", "pattern compaction mémoire", "déterministe llm gate humaine", "archive append-only canonique vivante", "clean-memory pattern", "maintenance données accumulatives"]
type: technique
derniere-maj: 2026-05-27
auteur: claude
tags: ["#type/technique", "#domaine/claude-code", "#sujet/maintenance", "#doctrine/2026"]
---

# Maintenance hybride d'un corpus accumulatif

Tout corpus qui s'accumule par ajout (index mémoire `MEMORY.md`, notes de doctrine, FAQ, changelog, base de feedbacks) se dilue avec le temps : doublons conceptuels, amendements successifs non consolidés, items dormants. Sans maintenance, le signal se noie dans le volume et le coût de lecture croît. Ce pattern structure la maintenance sans automatisme aveugle.

## Principe — trois couches

| Couche | Rôle | Quand |
|--------|------|-------|
| **Déterministe** (script, grep) | Détection mécanique *cheap* : orphelins (fichier sans entrée index), citations entrantes, liens morts | Métriques objectives uniquement |
| **LLM** | Clustering **sémantique** : doublons conceptuels, amendements, ambigus à NE PAS fusionner, dormants | Le jugement, pas la mécanique |
| **Humain** | Gate `[v]/[m]/[i]` typée par section, `[m]` anti tout-ou-rien | Toute opération destructive |

Le LLM lit le corpus entier et regroupe mieux que toute heuristique lexicale sur corpus court/homogène — la couche déterministe se limite aux métriques objectives. Construire une couche déterministe lourde (Jaccard, ML) par-dessus une lecture LLM possible = **enforcement-théâtre** (cf [[llm-lit-court-homogene-pas-couche-deterministe]]). Mesurer que le LLM rate AVANT de construire l'aide.

## Architecture stockage

- **Canonique vivante** (`MEMORY.md`, note doctrine) : modifiable.
- **Archive append-only sacré** (`_archive/YYYY-MM/`) : jamais modifiée après écriture. Réversibilité totale.
- **Journal** (`MEMORY-archive-log.md`) : append-only, trace par opération (fichiers, raison, méta-feedback, rollback).

## Gate typée par section (critères LLM)

- **A — doublons conceptuels** → fusion (méta consolidé + archive originaux + aliases pour préserver backlinks)
- **B — amendements successifs** → fusion (le récent absorbe l'ancien)
- **C — ambigus** → **rejeter la fusion par défaut**, présenter la distinction, arbitrage. Fusionner deux concepts distincts pour gagner des lignes efface une nuance utile.
- **D — dormants** → archive solo ; non-cité = nécessaire mais NON suffisant, critère décisif = obsolescence/absorption prouvée.

## Méta-principe partagé avec doctrine-vivante

Même ADN que [[doctrine-vivante]] : **gate humaine non négociable + anti-scan-aveugle**. Différence de cible : doctrine-vivante fait évoluer *la doctrine* sur signal externe ; ce pattern empêche *un corpus accumulatif* de se diluer. Deux applications d'un même principe (l'humain tranche, le mécanisme propose).

## Cas empirique — clean-memory (27 mai 2026)

`MEMORY.md` 196 feedbacks. Couche déterministe a révélé 10 orphelins + 57% sans citation entrante (→ citation = mauvais critère d'archivage seul). LLM a proposé 3 fusions (claims, tests-adverses, jarvis) + 2 ambigus correctement rejetés. Gate humaine : 3 fusions validées, A4 ignoré (parent/spécialisation), C1/C2 séparés. Couche Python Jaccard initialement prévue puis **coupée** (enforcement-théâtre). Skill : `/clean-memory`.

## Wikilinks

- [[llm-lit-court-homogene-pas-couche-deterministe]] — anti enforcement-théâtre (fondement de la limite déterministe)
- [[doctrine-vivante]] — méta-principe partagé (gate humaine + anti-scan-aveugle)
- [[methode-pivoter-doctrine]] — autre application de gate humaine sur changement structurant
- [[pattern-mcp-brief-then-direct]] — skill = écritures MCP denses en session principale
- [[comment-creer-skill]] — skill de jugement LLM = validation par exécution, pas test unitaire
