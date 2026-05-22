---
titre: "Mitchell Hashimoto — Origine du terme Harness Engineering"
resume: "Créateur Ghostty + ex-fondateur HashiCorp. A nommé harness engineering le 5 février 2026 dans my-ai-adoption-journey — terme repris par Fowler, OpenAI, Mollick en 2 semaines. AGENTS.md compounding où chaque ligne = un bad behavior observé"
aliases:
  - "Mitchell Hashimoto"
  - "Hashimoto"
  - "mitchellh"
  - "Ghostty"
  - "harness engineering origin"
  - "AGENTS.md compounding"
  - "HashiCorp founder"
derniere-maj: 2026-05-22
auteur: claude
type: leader
sources:
  - "https://mitchellh.com/writing/my-ai-adoption-journey"
  - "https://github.com/ghostty-org/ghostty/blob/main/AGENTS.md"
tags:
  - "#type/leader"
  - "#domaine/agents"
  - "#domaine/harness-engineering"
  - "#leader/agents"
---

# Mitchell Hashimoto — Origine du terme Harness Engineering

## QUI

**Mitchell Hashimoto** — Créateur de **Ghostty** (terminal moderne en Zig + Swift/GTK, ~30k stars en 2026). Ex co-fondateur **HashiCorp** (Terraform, Vagrant, Consul, Vault, Nomad) — l'une des success stories majeures du DevOps des années 2010. Pseudo Twitter / GitHub : `mitchellh`. Blog `mitchellh.com`.

Profil : ingénieur systèmes legendary tier. N'est pas chez Anthropic. Sa contribution est **lexicale + comportementale** — il a nommé un pattern que tout le monde pratiquait sans mot pour le désigner.

## POURQUOI EST PERTINENT

Hashimoto a **inventé le terme "harness engineering"** dans un blog post du **5 février 2026**. En 2 semaines, le terme a été repris par :
- Martin Fowler (cf [[martin-fowler]] — taxonomy Guides+Sensors)
- Addy Osmani (cf [[addy-osmani]] — Ratchet Principle, "+21.8 pts")
- OpenAI (mentions internes)
- Ethan Mollick (Wharton)

C'est le **moment de naissance** d'un vocabulaire partagé pour parler de configuration d'agent.

Sa deuxième contribution majeure : le pattern **AGENTS.md compounding** (alternative à CLAUDE.md, adopté notamment par OpenAI Codex), où chaque ligne du fichier est née d'un bad behavior observé.

## CONTRIBUTIONS CLÉS

### 1. Définition canonique du concept

> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."

C'est **textuellement** le compounding learning. Boris Cherny dira plus tard la même chose chez Anthropic (cf Pragmatic Engineer : *"Anytime we see Claude do something incorrectly, we add it to CLAUDE.md"*) — Hashimoto l'a formulé en premier.

### 2. Composants harness identifiés

Dans son post fondateur, Hashimoto liste son harness perso :
- **AGENTS.md** — plain-text implicit prompting, **chaque ligne = un bad behavior observé**
- Scripts pour screenshots (visual feedback loop)
- Filtered test runners (`-Dtest-filter` plutôt que suite full)
- Outils pairés avec updates AGENTS.md pour que l'agent les connaisse

### 3. AGENTS.md de Ghostty — référence vivante

Repo public : https://github.com/ghostty-org/ghostty/blob/main/AGENTS.md

Contenu observé :
- Build commands ciblées : `zig build`, flag macOS speedup `-Demit-macos-app=false`
- Tests : `zig build test`, **préférence `-Dtest-filter`** (suite full lente)
- Structure : `src/` core Zig, `macos/` Swift, `src/apprt/gtk` GTK
- Convention `libghostty-vt` : *"C enums must include `a _MAX_VALUE = GHOSTTY_ENUM_MAX_VALUE sentinel`"*
- Formatters : `zig fmt .`, SwiftLint `--strict --fix`, Prettier
- **Interdictions explicites** : *"Never create an issue"* et *"Never create a PR"*

C'est un AGENTS.md vrai-monde, qui sert d'exemple **concret** à toute la communauté.

### 4. Pattern AGENTS.md vs CLAUDE.md

AGENTS.md = format adopté par OpenAI Codex, Cursor, Aider — concurrent direct de CLAUDE.md d'Anthropic. Même esprit (memory file lu au démarrage de session), mais nom différent.

Hashimoto utilise **AGENTS.md** côté Ghostty. La compatibilité forge : Claude Code lit `CLAUDE.md` ; pour cross-tool, certains repos symlinkent ou maintiennent les deux.

## VERBATIM NOTABLES

> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."

> "Agents are much more efficient when they produce the right result the first time"

> "I'm making an earnest effort whenever I see an agent do a Bad Thing to prevent it from ever doing that bad thing again."

> "Each line in that file is based on a bad agent behavior, and it almost completely resolved them all."

## ALIGNEMENT FORGE

Le pattern Hashimoto = **règle Jarvis "workaround ≥ 2 fois = bug"** (mémoire `recurring-meta-anti-pattern`). MÊME PHILOSOPHIE : compounding errors → harness tightening.

Différence : Hashimoto reste sur enforcement **par prompt** (AGENTS.md, interdictions textuelles). Forge a dépassé ce stade — quand une règle doit tenir, c'est un **hook exit 2**, pas une interdiction texte (cf [[comment-creer-hook]], doctrine "If a rule must hold every time, make it a hook").

## WIKILINKS

- [[addy-osmani]] — a popularisé "harness engineering" en s'appuyant sur Hashimoto
- [[martin-fowler]] — taxonomy Guides+Sensors qui structure le concept
- [[comment-ecrire-claudemd]] — équivalent Anthropic d'AGENTS.md
- [[comment-creer-hook]] — étape suivante au-delà du prompt
- [[workflow-claude-code-optimal]] — compounding learning intégré

## SOURCES

- **Blog post fondateur** (5 février 2026) : https://mitchellh.com/writing/my-ai-adoption-journey
- **Ghostty AGENTS.md** (référence vivante) : https://github.com/ghostty-org/ghostty/blob/main/AGENTS.md
- **Ghostty repo** : https://github.com/ghostty-org/ghostty

---

## NOTE D'HIÉRARCHIE DES SOURCES

Source **secondaire** (couche 3). Hashimoto a **nommé** un pattern que Anthropic pratique aussi (Boris : "we add it to CLAUDE.md"). En cas de conflit terminologique CLAUDE.md vs AGENTS.md, **Anthropic > Hashimoto** côté Claude Code (donc CLAUDE.md). Mais le **principe** compounding learning est légitimement attribué à Hashimoto.
