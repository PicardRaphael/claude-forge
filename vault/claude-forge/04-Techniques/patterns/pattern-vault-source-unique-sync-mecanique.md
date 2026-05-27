---
titre: "Pattern — Vault dossier source unique + sync mécanique des consommateurs"
resume: "Quand une liste (leaders, configs) vit à la fois dans le vault et dans un consommateur (skill), le dossier vault est la SOURCE UNIQUE et un script de sync régénère le bloc consommateur à la MAINTENANCE (pas au runtime), entre marqueurs, sans toucher le reste."
aliases:
  - "pattern vault source unique"
  - "sync mecanique vault"
  - "single source of truth vault"
  - "sync-leaders pattern"
  - "vault folder source of truth"
  - "regeneration entre marqueurs"
derniere-maj: 2026-05-27
auteur: claude
type: technique
sources:
  - "Chantier C cc-news sync-leaders 27 mai 2026"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/patterns"
---
# Pattern — Vault dossier source unique + sync mécanique

> Pattern forge dérivé du Chantier C (27 mai 2026) : résoudre une double-source entre vault et skill consommatrice.

## Le problème

Une liste (leaders à surveiller, configs de domaine, etc.) est dupliquée entre :
- **le vault** (`05-Leaders/<domaine>/` — fiches structurées, durables)
- **un consommateur** (`cc-news/references/domain-*.md` — listes hardcodées)

Les deux **divergent** silencieusement : le consommateur rate ce que le vault sait. Cf cas cc-news : ~36 fiches vault absentes des plans de chasse, ~14 cibles chassées sans fiche (divergence **bidirectionnelle**).

## La décision discriminante

Pas « runtime fetch dynamique » (coût répété, le vault ne donne que des noms pas des queries). La vraie question : **qui est source unique de QUOI**.

| Artefact | Source unique |
|----------|---------------|
| Liste des entités (noms) | **dossier vault** = vérité, mécaniquement (`list_notes(folder)`) |
| Métadonnées d'usage (handles, queries) | consommateur, OU frontmatter vault si normalisé |
| Logique opérationnelle (splits, sources directes) | **consommateur** (pas d'équivalent vault) |

## Le mécanisme

1. **Marqueurs** dans le consommateur : `<!-- SYNC:x:start -->` / `<!-- SYNC:x:end -->`. Le script ne réécrit QUE l'entre-deux.
2. **Script de sync** lancé à la **maintenance** (après ajout/retrait d'une fiche), **pas au runtime** — le consommateur lit un fichier déjà à jour, zéro surcoût par exécution.
3. **Idempotent** : re-lancer sans changement vault ⇒ « inchangé ». À vérifier par round-trip (run 1 = modifié, run 2 = inchangé).
4. **Section éditée à la main préservée** : tout ce qui est hors marqueurs (watchlist, queries, sources directes) n'est jamais touché.
5. **Report des écarts non couverts** : le script signale ce que le vault contient mais que la logique opérationnelle ne vise pas encore (ex : leader synced sans query) — dette mesurée, pas masquée.

## Pourquoi maintenance et pas runtime

`feedback_da_probe_empirique_avant_verdict` + mesure : runtime = coût MCP × N agents × scan, et le vault donne des noms, pas des artefacts opérationnels prêts. Régénérer à la modif = 1 acte conscient quand on touche la source, ~100× moins coûteux.

## Lecture vault par un script

Un script de transformation déterministe lit le vault en `open()`/`glob()` direct (I/O fichier), **équivalent d'un hook** — distinct de l'accès agent au vault que `vault-cat-guard.py` interdit. Légitime, mais à documenter explicitement pour ne pas être imité comme une normalisation par une session future.

## Mode dégradé assumé

Si une métadonnée n'est pas un champ structuré (handles X dans `aliases`, pas `handle_x`), le script n'émet que les valeurs **haute confiance** (lien `x.com/` explicite). Un faux positif (handle d'orga) est **pire** qu'un vide (génère une mauvaise query). Denylist manuelle pour les faux connus. Le reste = dette tracée vers une passe de normalisation frontmatter.

## Liens

- [[mcp-vs-skills-doctrine]]
- [[pattern-vault-llm-karpathy]]
- [[comment-creer-skill]]
- [[methode-analyser-repo]]
