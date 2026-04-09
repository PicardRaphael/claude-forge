# Guide technique : Connecter GitHub a l'organisation Claude IA

**Pour :** Administrateur de l'organisation + DevOps
**Temps estime :** 15 minutes

---

## Pourquoi

L'auto-sync des plugins Cowork (pour l'equipe support) necessite GitHub. Voir `Projets/pourquoi-github.md` pour le contexte business.

Claude Code (devs) n'a PAS besoin de GitHub — Bitbucket suffit.

---

## Etape 1 — Admin connecte GitHub (5 min)

L'administrateur de l'organisation "Claude IA" doit :

1. Se connecter a **https://claude.ai** avec le compte admin
2. Aller dans **Parametres** → **Organisation** → **Integrations**
3. Cliquer **Connecter GitHub**
4. Autoriser l'acces au compte GitHub de l'organisation

### Si l'organisation n'a pas de compte GitHub

1. Creer un compte GitHub gratuit : https://github.com/signup
2. Creer une organisation GitHub (gratuit) : https://github.com/organizations/plan
3. Nom suggere : `neoteem` ou `neoteem-ia`
4. Inviter Raphael comme membre

---

## Etape 2 — DevOps cree le repo plugin (10 min)

```bash
# Creer le repo sur GitHub (public ou prive)
# Nom : claude-support-plugin
# Organisation : neoteem (ou le nom choisi)

git clone https://github.com/neoteem/claude-support-plugin.git
cd claude-support-plugin

# Structure minimale
mkdir -p skills agents
touch plugin.json
```

### plugin.json minimal

```json
{
  "name": "support-neoteem",
  "version": "1.0.0",
  "description": "Plugin support Neoteem — triage, recherche base connaissances, escalade"
}
```

Raphael remplira les skills/agents ensuite.

---

## Etape 3 — Configurer le marketplace Cowork (5 min)

L'admin dans claude.ai :

1. Aller dans **Parametres** → **Organisation** → **Plugins** (ou Cowork)
2. **Add marketplace source** → GitHub
3. Selectionner le repo `neoteem/claude-support-plugin`
4. Mode : **Auto-install** (tous les membres recoivent automatiquement)
5. Activer **GitHub sync** (auto-resync a chaque push)

---

## Etape 4 — Activer Dispatch (optionnel, 1 min)

Si l'equipe veut utiliser Dispatch (controle mobile → desktop) :

1. **Parametres** → **Organisation** → **Features**
2. Activer **Dispatch**
3. C'est org-wide (tous les membres ou personne)

---

## Verification

Demander a un membre (non-admin) d'ouvrir Claude Desktop :
- Le plugin "Support Neoteem" doit apparaitre dans la liste des plugins
- Si absent → verifier que le marketplace est en mode auto-install

---

## Notes

- Le repo GitHub est utilise UNIQUEMENT pour les plugins Cowork (pas pour le code)
- Bitbucket reste l'outil principal pour les 128 repos de code
- Le repo peut etre prive (recommande)
- Pour ajouter un 2e plugin plus tard, meme process
