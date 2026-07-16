---
titre: "Critique — Plan vault forge-brain global user-scope (dispo tous repos machine)"
type: knowledge
domaine: claude-code
derniere-maj: 2026-07-16
auteur: claude
sources:
  - "[[limite-mcp-lock-inter-ecritures]]"
  - "[[critique-2026-06-27-pivot-vault-agent-first]]"
  - "session 2026-07-16 (audit stagnation vault + advisor + DA)"
aliases:
  - "critique vault global user-scope"
  - "DA vault point cloud global 16 juillet"
  - "critique 2026-07-16 forge-brain user-scope"
  - "verdict devils-advocate vault machine-wide"
  - "critique MCP forge-brain user-level"
tags:
  - "#type/critique"
  - "#domaine/claude-code"
  - "#domaine/vault"
---

## Devils Advocate — Plan vault forge-brain global user-scope

**Intention déclarée :** rendre le vault forge-brain consultable depuis toutes les sessions Claude Code de la machine (A config MCP user-scope, B serveur toujours vivant, C discipline user-CLAUDE.md, D extension DA), pour enrayer la chute de 80 % de consultation causée par la migration du travail réel hors forge.

---

### Verdict

**Bloquants : 1 | Avertissements : 4 | Nitpicks : 2**

**Décision recommandée : LIVRER AVEC CORRECTIONS** — plus précisément **STAGER**. La Part A seule satisfait la contrainte dure de Raphael à coût quasi nul via un mécanisme prouvé. B+C+D sont des élaborations coûteuses et risquées bâties sur une **prémisse non testée**. Le BLOCKING porte sur le bundling all-at-once, pas sur l'idée.

---

### Si je devais le faire marcher malgré mes objections

**Stager, ne pas tout livrer d'un coup.**

1. **Phase 1 (maintenant) — Part A seule** : `claude mcp add -s user` (mécanisme déjà en place, docs-langchain/context7 y sont). Satisfait littéralement « le vault dispo sur tous les repos de la machine », zéro fichier de repo, coût quasi nul. GARDER le hook SessionStart forge existant comme relance serveur.
2. **Phase 1bis — mesurer 2 semaines** : `usage_stats` donne déjà search_brain par fenêtre. Suivre spécifiquement les appels vault DEPUIS des sessions non-forge. C'est le test de la prémisse (cf BLOCKING).
3. **Phase 2 (SI usage monte)** : ajouter B (mais en **hook user-scope SessionStart**, pas tâche planifiée — cf AVERT-2) + C. Si l'usage reste proche de zéro → on a évité pollution de contexte permanente + surface d'injection élargie pour rien.
4. **Ajouter une convention d'écriture** avant toute écriture concurrente réelle (cf BLOCKING/AVERT-1) : writes vault UNIQUEMENT depuis forge, ou append-only depuis non-forge, ou coder le lock par chemin.
5. **Débundler D** : passe subagent-creator dédiée, hors de ce plan (cf AVERT-4).

---

### Angle Technique — Qu'est-ce qui se casse ?

**Le plan EST le déclencheur documenté du bug de concurrence.** La note [[limite-mcp-lock-inter-ecritures]] explique verbatim pourquoi le lock n'a jamais été codé : *« usage solo, écritures séquentielles »*. Et son déclencheur-qui-justifierait-de-coder, verbatim : *« passage à un usage multi-agent parallèle réel où plusieurs agents/sessions écrivent le vault simultanément »*. Ce plan convertit précisément cette prémisse (solo/séquentiel) de vraie à FAUSSE : forge + neo_ia ouverts en parallèle, aucun ne voyant l'autre. Conséquence concrète : `update_property`/`append_note` quasi simultanés sur la même note → last-write-wins silencieux → **perte d'une édition de note sur la base de connaissance**. La mitigation nommée par la note est « discipline » — mais la discipline CROSS-session (deux fenêtres aveugles l'une à l'autre) est bien plus faible que la discipline intra-session. Le risque (v) est listé dans le plan **sans aucune mitigation**.

Serveur down entre logons (risque ii) : la tâche planifiée au logon ne s'auto-répare pas en cours de journée (limite déjà admise par le plan). MCP HTTP down → il faut vérifier que la session ne bloque pas au démarrage (dégradation gracieuse, warning, pas d'échec bloquant).

Couplage (iv) réel mais mineur : rename/déplacement du repo forge casse le chemin `start.py` silencieusement pour TOUTES les sessions machine. Acceptable pour une machine mono-utilisateur.

**Objections :**
- BLOQUANT (score 82) : livrer A+B+C+D en bloc active le déclencheur de course inter-écritures ([[limite-mcp-lock-inter-ecritures]]) SANS mitigation, sur une prémisse non testée. Restructuré en A-first + mesure + convention d'écriture → retombe en AVERTISSEMENT.
- AVERTISSEMENT (score 78, AVERT-1) : risque (v) écritures concurrentes listé sans mitigation. Exiger une convention explicite (single-writer forge, ou append-only non-forge, ou lock par chemin codé) AVANT d'ouvrir l'écriture multi-session.
- AVERTISSEMENT (score 72, AVERT-2) : Part B sur-construite. Une tâche planifiée `schtasks` (fragile sur droits, fallback dossier Startup) ne s'auto-répare pas mid-day. Un **hook user-scope SessionStart** dans `~/.claude/settings.json` (user-global ≠ fichier de repo, respecte « rien dans les repos ») fire à CHAQUE session, check port 8091, relance si down — même logique que le hook forge existant, déplacée en user scope. Strictement meilleur : self-healing, pas de fragilité schtasks. Tue le risque ii.
- NITPICK : `pyw`/`py` (PEP 514 launcher) et non `pythonw C:\...` en dur (doctrine windows-hooks cross-machine).
- NITPICK : vérifier dégradation gracieuse MCP HTTP down (warning, pas blocage SessionStart).

---

### Angle Stratégique — Est-ce le bon problème ?

**La prémisse centrale n'est pas testée.** Le diagnostic (consultation −80 %, 65 % des sessions hors forge) est solide et mesuré. Mais le plan repose sur une hypothèse implicite : *les sessions non-forge consulteraient le vault si elles le pouvaient, et le feront une fois disponible.* Lecture concurrente tout aussi plausible : quand Raphael bosse dans neo_ia, il fait du **travail de code neo_ia** — et le vault forge (doctrine Claude Code, concurrents, leaders, techniques) a peu à offrir à ce domaine. **Disponibilité ≠ usage.** Le consensus état-de-l'art que le plan cite lui-même (« ce qui vit est ce qui est utilisé en boucle ») coupe CONTRE le plan : rendre disponible ne crée pas la boucle d'usage.

Piège de routing non traité : neo_ia a déjà NeoBrain MCP (stack Neoteem/Loji). Ajouter forge-brain partout = **deux cerveaux partout**, risque de confusion sur lequel interroger pour quoi.

C'est de la **sur-ingénierie en amont de la preuve**. A seul teste l'hypothèse à coût quasi nul. B/C/D engagent la machinerie (pollution de contexte permanente, surface d'injection, complexité serveur) avant de savoir si quiconque consulte depuis une session non-forge. Le staging défuse i/ii/iii pendant la fenêtre de test.

**Objections :**
- BLOQUANT (voir Technique — même finding, angle stratégique) : la prémisse « disponibilité → usage » n'est pas validée. Mesurer d'abord (A + usage_stats, 2 semaines), élaborer ensuite.
- AVERTISSEMENT (score 60) : deux MCP-cerveaux dans neo_ia (NeoBrain + forge-brain) sans règle de routing → confusion probable. Prévoir une ligne « pour la stack Neoteem/Loji : NeoBrain ; pour doctrine CC/techniques/veille : forge-brain ».

---

### Angle Pratique — Combien de temps avant l'abandon ?

Part C : `~/.claude/CLAUDE.md` chargé dans **toutes** les sessions machine (~quelques centaines de tokens partout, y compris sessions équipe locales où le vault est inutile — risque iii). Coût permanent, bénéfice conditionné à la prémisse non testée. Si l'usage ne monte pas, ce fichier devient de la doctrine morte chargée à chaque tour — exactement le type de dette « périmée qui dégrade chaque tâche » que CLAUDE.md forge combat. D'où le staging : ne créer C qu'après validation.

Part D (extension DA) : **scope-creep**. Confronter le plan critiqué aux `Knowledge/decisions/` n'a AUCUN rapport avec la disponibilité du vault. Bundlé, D ship sans son propre examen. À vérifier aussi : `Knowledge/decisions/` est-il réellement peuplé ? Si clairsemé, D ajoute une étape search qui retourne le plus souvent rien = overhead par run. À débundler en passe subagent-creator dédiée.

Injection (risque i) : réel mais AVERTISSEMENT, pas bloquant — le lethal trifecta existe DÉJÀ dans forge aujourd'hui ; le plan élargit l'ouverture, et la ligne C.4 amène les sessions non-forge à PARITÉ avec la posture (advisory) actuelle de forge. Mais la surface dangereuse précise = `delete_note`/`update_note` depuis une session qui ingère du contenu non fiable SANS les rules forge. C.5 (« prudence ») est trop faible.

**Objections :**
- AVERTISSEMENT (score 68, AVERT-3, injection i) : C.5 « prudence » insuffisant pour les ops destructives (`delete_note`/`update_note`) depuis session non-forge ingérant du contenu non fiable. Exiger une ligne DURE (interdiction ops destructives vault hors forge) ou un deny tool-level dans les settings user-scope.
- AVERTISSEMENT (score 65, AVERT-4, D scope-creep) : Part D sans rapport avec la disponibilité du vault, ship sans scrutiny propre. Débundler ; vérifier `Knowledge/decisions/` peuplé avant d'ajouter une étape search systématique.
- NITPICK : C = tokens permanents partout ; ne créer qu'après validation Phase 1bis.

---

### Vault — Historique pertinent

- [[limite-mcp-lock-inter-ecritures]] : le plan est le déclencheur exact que cette note nomme comme condition de codage du lock. Kill shot du BLOCKING/AVERT-1.
- [[critique-2026-06-27-pivot-vault-agent-first]] : précédent de méthode (pivot vault soumis à DA, verdict LIVRER AVEC CORRECTIONS sur énumération incomplète de foyers). Pertinence de posture, pas de contenu — l'analyse ci-dessus tient sans ce lien.
