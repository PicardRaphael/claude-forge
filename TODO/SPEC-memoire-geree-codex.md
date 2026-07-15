# SPEC — Mémoire gérée pour Codex (couche externe possédée)

_Conçue le 15 juil. 2026. **Statut : SPEC à dégainer quand Raphael passe réellement sur Codex.** Rien à construire avant. Fondée sur la recherche mémoire Codex du 15 juil. (2 agents, sources primaires) — cf notes vault `memoire-optimale-codex-chatgpt` + `loop-apprentissage-codex`._

## 0. Le problème (rappel)

La mémoire native de Codex (`[memories]`) est **délibérément non pilotable à la main** — doc verbatim : *« Treat these files as generated state... don't rely on editing them by hand as your primary control surface »*. Pas de commande write/pin/force. `/memories` = toggles on/off.

**Conséquence** : une mémoire qu'on GÈRE (versionnée, éditable, auditable, dont on décide le contenu) ne peut PAS être les `[memories]` bidouillés (Codex les régénère/écrase). Ce doit être une **couche EXTERNE possédée** que Codex *consomme* mais ne *contrôle* pas. C'est le pattern forge (vault + `/done`) transposé à Codex.

## 1. Architecture cible — 2 couches distinctes

| Couche | Contenu | Mécanisme Codex | Possédée/versionnée ? |
|--------|---------|-----------------|----------------------|
| **A — Règles durables** (instruction-memory) | conventions, décisions, procédures | `AGENTS.md` + Skills `.agents/skills` | OUI (fichiers git) |
| **B — Épisodique contrôlé** (learned-memory) | ce qui s'est passé aux sessions passées | serveur MCP mémoire OU hook `Stop`/`PreCompact`→`SessionStart` | OUI si couche externe |

> Ne JAMAIS mélanger : « Instructions belong in version-controlled files. Learned knowledge belongs in a searchable memory store. Mixing them creates maintenance headaches » (codex.danielvaughan.com). La contrainte liante = le **jugement** (quoi retenir, quand MAJ), pas l'infra.

## 2. Options pour la couche B (épisodique) — décision à trancher au moment du build

| Option | Ce que c'est | Pour | Contre |
|--------|--------------|------|--------|
| **B1 — mem0 (plugin Codex)** | `codex plugin add mem0@mem0-plugins` → MCP + Skills + 6 hooks lifecycle pré-câblés (SessionStart load, UserPromptSubmit search, Stop store summary, PreCompact store) | clé en main, extraction sémantique auto, scopé `user_id` (partagé Codex+Cursor+CC), le plus rapide à monter | dépendance externe (clé API MEM0_API_KEY), mémoire chez un tiers, moins « possédée » |
| **B2 — Basic Memory (MCP)** | vault **markdown local = source de vérité**, éditable/versionnable, cross-tool via MCP (`codex mcp add basic-memory ...`) | le plus « possédé » (fichiers markdown à toi, git), cross-tool, pas de tiers | produit externe quand même, moins d'extraction auto que mem0 |
| **B3 — vault forge-brain branché sur Codex** | exposer le MCP forge-brain (déjà existant !) à Codex via `[mcp_servers.forge-brain]` dans son config.toml → Codex lit/écrit TON vault | **zéro nouveau composant** (le MCP existe), mémoire 100% possédée et déjà versionnée, cohérent avec l'écosystème forge | forge-brain n'a pas de mémoire épisodique auto (il faudrait un hook Codex Stop→create_note) ; risque de polluer le vault de bruit de session |
| **B4 — DIY zéro-dépendance** | AGENTS.md + hook Codex `SessionStart` (Python stdlib) lisant un fichier markdown local | contrôle total, aucune dépendance | tout à écrire/maintenir soi-même |

**Recommandation à ce stade (à re-challenger au build)** : **B3 (vault forge-brain branché sur Codex)** — c'est le plus cohérent avec ton écosystème (ton cerveau est déjà là, déjà versionné, déjà accessible en MCP) et ça évite un 2e système de mémoire. Le seul travail = un hook Codex `Stop`/`PreCompact` qui écrit un résumé de session via `create_note`/`append_note` (avec redaction secrets), réinjecté au `SessionStart`. À arbitrer vs B1 (mem0) si tu veux l'extraction sémantique auto sans écrire de hook.

## 3. Couche A (règles durables) — le montage

- **AGENTS.md** à la racine du/des repo(s) Codex : conventions, commandes, standards, `## Review guidelines`. Cap 32 KiB (troncature silencieuse au-delà → ne pas en faire une grosse mémoire). Nesting racine→sous-dossiers si besoin.
- **Skills `.agents/skills`** : les procédures réutilisables (l'équivalent de tes skills forge). Le standard Agent Skills est partagé → certaines skills forge peuvent inspirer les skills Codex (mais **pas portables byte-identique** — répertoires + champs diffèrent).

## 4. Le loop d'apprentissage (couche B en mouvement)

Une fois la couche B en place, le compounding = le pattern déjà documenté (`loop-apprentissage-codex`) : une **scheduled task Codex** (automation) qui scanne `~/.codex/sessions`, repère les frictions, et met à jour skills/AGENTS.md. C'est le pendant Codex de `/skill-evolve friction` qu'on a construit pour forge. **Garde-fou** : compounding jugement-piloté (validation humaine avant écriture), append incrémental jamais réécriture (façon ACE).

## 5. Arbitrages honnêtes (« la mémoire parfaite n'existe pas encore »)

- **Portabilité** : mémoire MCP (B1/B2/B3) portable cross-provider ; `[memories]` natif non.
- **Staleness** : mauvais backend = contexte périmé qui dégrade la sortie. Si on empile `[memories]` natif + couche externe → mettre `disable_on_external_context = true` pour éviter l'injection redondante.
- **Versioned reads (non résolu)** : deux agents qui écrivent en concurrence → le plan de l'un périme celui de l'autre. Aucun produit ne le résout proprement au 15/07. À garder en tête si usage multi-agent.
- **Régions** : `[memories]` natif indisponible EEA/UK/Suisse au lancement (→ AGENTS.md + couche externe seuls là-bas).

## 6. Séquence de construction (le jour J)

1. Choisir l'option couche B (B3 recommandé, ou B1 si extraction auto voulue).
2. Poser AGENTS.md racine (couche A) sur le repo Codex.
3. Brancher la couche B :
   - si B3 : `[mcp_servers.forge-brain]` dans `~/.codex/config.toml` + hook Codex `Stop`→`create_note` (avec redaction secrets).
   - si B1 : `codex plugin add mem0@mem0-plugins` + clé API.
4. Vérifier en RUN réel : Codex retrouve-t-il un fait d'une session passée ? (le tip #1 Boris — donner un moyen de vérifier).
5. Activer le loop d'apprentissage (automation scheduled) une fois la couche B stable.
6. **DA avant** si ça touche la machinerie (hook Codex, exposition du vault forge-brain à un outil externe = surface d'injection à checker — cf lethal trifecta).

## 7. Prérequis avant de dégainer cette SPEC

- Raphael utilise réellement Codex (CLI/IDE) sur au moins un repo.
- Décider quel repo est le « terrain » Codex.
- Re-vérifier la fraîcheur des options (Codex bouge chaque semaine — mem0/Basic Memory/config.toml peuvent avoir évolué). Relancer une vérif source primaire au moment du build.
