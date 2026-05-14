---
titre: "Cowork — Pourquoi les skills ne suivent pas les instructions"
resume: "Diagnostic complet quand une skill Cowork ne suit pas les instructions — 2 problemes distincts, checklist debugging 9 etapes, bugs connus et pattern Skill Activation Hook"
aliases:
  - "cowork skills reliability"
  - "skills ne suivent pas instructions"
  - "skill activation failure"
  - "skill drift"
  - "debugging skills cowork"
  - "pourquoi skill marche pas"
domaine: claude-code
type: technique
derniere-maj: 2026-05-14
auteur: claude
sources:
  - "https://dev.to/thestack_ai/i-audited-214-claude-code-skills-73-were-silently-broken-2m9a"
  - "https://medium.com/@marc.bara.iniesta/claude-skills-have-two-reliability-problems-not-one-299401842ca8"
  - "https://claudefa.st/blog/tools/hooks/skill-activation-hook"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/cowork"
---

## Les 2 problemes distincts

### Probleme A — Activation failure : la skill ne se declenche jamais

Audit de 214 skills communautaires : **73% silencieusement cassees** — jamais declenchees.

| Cause | Frequence |
|-------|-----------|
| Descriptions vagues sans phrases de declenchement | 68% |
| Descriptions < 20 mots | 41% |
| Collision entre skills (descriptions qui se chevauchent) | ~15% |
| Budget contexte sature (skills silencieusement droppees) | invisible |

Meme avec YAML valide, le declenchement autonome atteint **~50% de succes**. Claude priorise la tache telle qu'il la comprend, pas la verification de l'existence d'une skill.

### Probleme B — Drift/skip : la skill se declenche mais ignore des instructions

- **Context drift** — les instructions originales sont poussees loin du point de generation actif
- **Fluency bias** — quand la tache semble evidente, Claude saute les etapes de verification
- **Compaction detruit le contexte** — les rules path-scoped et CLAUDE.md imbriques sont resumes et perdus
- Un texte marque "OBLIGATOIRE" a **zero force mecanique** — c'est advisory (~80% compliance max)

## Formule directive (100% activation sans hook)

```markdown
# MAUVAIS (passif)
Helps with Docker configuration and containers.

# BON (directif)
ALWAYS invoke this skill when reviewing code changes before committing.
Use for pull request reviews, diff reviews, and any time the user says
'check', 'review', or 'audit' code.
DO NOT write security feedback without invoking this skill first.
```

Formule : `ALWAYS invoke when [trigger]. DO NOT [action concurrente] without invoking first.`

## Checklist diagnostic (9 etapes)

1. **Description specifique ?** Directive (ALWAYS invoke when...) ou passive (Helps with...) ? Contient des phrases de declenchement concretes ? Si vague → recrire. Fixe 68% des echecs.

2. **Limites respectees ?** Description < 1 024 chars (champ seul), description + when_to_use < 1 536 chars (combiné dans le listing). Nom < 64 chars, lowercase + tirets.

3. **Skill montee et activee ?** Dans Cowork : verifier Customize > Skills UI. Verifier `enabledPlugins` dans settings.json (bug #17832). Pour les plugins : verifier que le composant skill est monte, pas juste le MCP (bug #31542).

4. **Collision entre skills ?** Chercher les descriptions qui se chevauchent. Si 2 skills matchent le meme prompt → ajouter "Use this for X, NOT for Y."

5. **Budget contexte sature ?** Si 10+ skills, le budget (~1% du context window) peut etre depasse. Desactiver les skills peu utilisees. Reduire les descriptions non-critiques. `/doctor` pour diagnostiquer.

6. **Tester avec des prompts realistes.** Pas "trigger my skill" mais exactement ce qu'un utilisateur taperait.

7. **SKILL.md trop long ?** Si > 500 lignes / ~5 000 tokens, l'attention decay. Deplacer dans `references/`. Garder le body sur contraintes et gotchas.

8. **Ajouter un hook si toujours instable.** Pour activation : hook `UserPromptSubmit` qui injecte "Use Skill(nom)" dans les prompts matchants. Pour compliance : hook PreToolUse guard (exit 2).

9. **Verification visible.** Si la skill s'active mais saute des etapes, ajouter une checklist obligatoire dans l'output. "Do NOT output the final result without first showing the completed checklist."

## Bugs connus Cowork

| Bug | Description |
|-----|-------------|
| **#50669** | Cowork ne charge que 3/27 skills personnelles. Ne scanne PAS `~/.claude/skills/` au demarrage — les skills doivent etre explicitement enregistrees via UI ou manifest |
| **#31542** | Le composant skill d'un plugin installe peut ne pas etre monte dans le container VM Cowork, meme si le plugin apparait comme installe. Le MCP du meme plugin fonctionne |
| **#17832** | Race condition : plugins ajoutes a `installed_plugins.json` mais PAS a `enabledPlugins` dans settings.json. Edit manuel necessaire |

### Budget contexte Cowork

Plus serre que CC pur. Plugins et MCP tools en competition pour le contexte. Si Claude agit comme s'il oublie une skill → saturation de budget, pas un bug du modele.

## Pattern Skill Activation Hook (forge ne l'a pas encore)

Un hook `UserPromptSubmit` qui intercepte les prompts et ajoute des recommandations de skills avant que Claude ne les voie. Claude ne peut pas oublier car il n'a jamais eu a se souvenir.

Le hook track ce qu'il a deja recommande et ne repete pas. Complement aux guard hooks (qui gerent la compliance, pas l'activation).

## Liens

- [[skills-guide]] — Format et best practices
- [[hooks-guide]] — Patterns d'enforcement
- [[harness-engineering]] — 65% des echecs = harness, pas modele
- [[erreur-advisory-rules-insuffisantes]] — Preuve empirique que l'advisory ne suffit pas
- [[prompting-chat-cowork-code]] — Differences de prompting par plateforme
