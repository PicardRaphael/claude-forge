---
titre: "Lojii — Frontend gestion immobilière"
resume: "Application Vue 3 / Vuetify 3 de gestion locative et copropriété, client lourd Neoteem, 634 composants, migration Composition API en cours"
aliases:
  - lojii
  - lojii-front
  - lojii frontend
  - frontend immobilier
  - gestion locative frontend
  - neofront lojii
type: context
derniere-maj: 2026-05-24
auteur: claude
tags:
  - "#type/context"
  - "#projet/neoteem"
  - "#projet/lojii"
  - "#tech/vue3"
  - "#tech/vuetify"
  - "#tech/pinia"
---
## Vue d'ensemble

Application frontend de gestion immobilière (locatif + copropriété) développée par [[Neoteem]]. Client lourd embarqué dans un Chromium WinDev + mode web.

- **Repo** : Bitbucket, branches `develop` / `test` / `prepilote` / `master`
- **Chemin local** : `C:\Users\raphael.picard_neote\Documents\neofront\lojii`
- **Taille** : ~87K lignes, 634 fichiers `.vue`, 26 MB de sources

## Stack technique

| Tech | Version | Rôle |
|------|---------|------|
| Vue | 3.5.13 | Framework frontend |
| Vuetify | 3.7.17 | UI Material Design |
| Vite | 6.2.1 | Build + dev HTTPS |
| Pinia | 3.0.1 | State management (29 stores) |
| Vue Router | 4.5.0 | Hash history routing |
| Tiptap | 3.20.1 | Rich text editor (6 packages) |
| TinyMCE | 6 (CDN) | Rich text editor legacy |
| Chart.js + vue-chartjs | 4.4.8 / 5.3.2 | Graphiques |
| @vueuse/core | 14.1.0 | Composables utils |
| SASS | 1.86 | CSS preprocessing |
| ESLint | 9.34 | Linting (flat config) |
| Prettier | 3.5.3 | Formatage |
| Vitest | jsdom | Tests unitaires (26 tests) |
| Playwright | chromium | Tests E2E (1 test) |
| Husky | 9.1.7 | Git hooks (branch protection) |

**Langage** : JavaScript pur (pas de TypeScript).

## Architecture

```
src/
  main.js              → Auth → config → mount
  App.vue              → Layout 13K lignes (menu + onglets + contenu)
  router/              → 20 fichiers, 27 modules de routes
  store/               → 29 stores Pinia + 1 legacy reactive store
  plugins/             → neoteem.js (API wrapper), filtres, utils, eventBus, menus (5055L)
  composables/         → useEcranConfig, useNeodocChat, useTiersList, FicheActeur
  services/            → requeteConfigApi, requeteSaveApi
  components/
    _bibliotheque/     → ~126 composants partagés (Fields, Filtres, Dialogs, Blocs, Boutons, Table)
    _common/           → 11 composants génériques
    [Module]/          → ~300+ composants métier
    IA/                → 10 composants (NeoChat, NeoDoc)
  views/               → ~150 vues
  assets/scss/         → 14 fichiers SCSS
```

## Modules métier

Commercialisation · Banque · Suivi Proprietaire · Suivi Locataire · Fiche Proprietaire · Fiche Locataire · Fiche Copropriété · Fiche Coproprietaire · Fiche Acteur · Administration · [[NeoChat]] · [[NeoDoc]] · Fournisseurs · Relances · Migration · Mutation · Assurance · Requête · Bibliothèque

## Conventions

| Type | Convention | Exemple |
|------|-----------|---------|
| Composant fichier | PascalCase | `UserCard.vue` |
| Store fichier | kebab-case | `visite-immeuble.js` |
| Store export | `use` + PascalCase | `useVisiteImmeuble` |
| Router fichier | kebab-case | `suivi-proprietaire.js` |
| CSS class | kebab-case | `.user-card` |
| Variables globales | `$` prefix | `$main`, `$eventBus` |
| Composants globaux | `nt-` prefix | auto-enregistrés via import.meta.glob |
| Imports | `@/` alias | `import X from '@/store/main'` |
| Unités CSS | rem (jamais px) | — |
| Style | `<style scoped>` + SCSS | — |

## Patterns clés

- **API** : `neoteem.query(url, method, data)` — wrapper fetch + auth token
- **Auth** : Google OAuth via `window.Auth`, `window.currentUser`
- **Navigation** : `$eventBus.$emit('change-route', '/path')` (legacy, pas router.push)
- **Messages** : `$main.setMsgSuccess/Error/Warning/Info()`
- **Stores Pinia** : `defineStore` + `ref` + HMR (`acceptHMRUpdate`)
- **Composants globaux** : `nt-*` auto-enregistrés dans `nt-components.js`

## État de migration

- **57% Composition API** (`<script setup>`) — 338 fichiers
- **43% Options API** (`export default {}`) — 258 fichiers à migrer
- **TinyMCE → Tiptap** : migration en cours (double éditeur)
- **Legacy store.js → Pinia** : migration en cours
- **51 micro-apps Vue 2** (neofront/) à migrer comme composants natifs dans lojii
- **914 écrans WinDev** vivants (sur 1601) à migrer vers Vue 3 dans lojii
- Pas de Vue 2 dans lojii lui-même (confirmé 2026-05-13)

### Micro-apps Vue 2 dans neofront/ (51 SPAs satellites)

Embarquées dans lojii via iframe/popup. Vue 2.6 + Vuetify 2.7 + Vue CLI 5.
Exemples : commercialisation, banque, suivi-locataire, suivi-proprietaire, compta-copropriete, lettrage, relances, mutation, fournisseur, extranet, depot_dossier_front, mail, widgets...
Documentation complète dans le vault neoteem-brain : `03-Apps/neofront/<app>/`

### Écrans WinDev (914 vivants)

Application desktop WinDev 30, 1601 fenêtres (914 vivantes, 687 mortes). Chromium embarqué affiche lojii web.
Documentation complète dans le vault neoteem-brain : `03-Apps/neofront/windev-front/` (29 notes)

## Dette technique identifiée

1. 2 fichiers ESLint (non-déterministe)
2. NeoChat.vue = 3140 lignes (à décomposer)
3. Tests quasi inexistants (26 unit / 1 E2E pour 634 composants)
4. menus.js = 5055 lignes / 191 KB
5. App.vue = 13K lignes
6. Husky pre-commit = protection branches uniquement (pas lint/format)
7. CLAUDE.md 330L avec composants fantômes

## Particularités

- **Mode Chromium embarqué** : détection client lourd WinDev, `hideIhm`/`hideMenu`
- **Multi-tenant** : détection `@neotimm.fr` / `@neoteem.fr` pour admins
- **PWA** : Service Worker via vite-plugin-pwa (workbox autoUpdate)
- **Module IA** : [[NeoChat]] (chatbot, 3140L) + [[NeoDoc]] intégrés
- **Variable globale `WL`** : WinDev Language, déclarée dans ESLint globals

## Config Claude Code (état 2026-05-13)

- CLAUDE.md : 87L (optimisé, composants fantômes supprimés)
- `.claude/` partagé avec l'équipe (retiré du .gitignore, seul settings.local.json ignoré)
- 4 agents : architect, vue-dev, code-reviewer, test-writer
- 6 skills : lojii-conventions, lojii-design-system, lojii-windev-mapping, lojii-vue2-mapping, go, spec
- 6 rules : vue-conventions, quality-gates, api-patterns, agent-limits, check-before-create, learn-from-mistakes
- 5 hooks : architect-guard, commit-guard, format-and-lint, on-env-protect, session-health

## Liens

- [[ia_back]] — Backend IA (API NeoChat/NeoDoc)
- [[neo_ia]] — Monorepo Python agents IA
- [[Neoteem]] — Entreprise
- [[Raphael-Picard]] — Lead IA


## Questions ouvertes

- [[question-idor-coproprietes-conseil-syndical]] — Security-auditor ia_back a détecté un IDOR : auth présente mais aucun contrôle de scope par copropriété. Un utilisateur authentifié peut accéder aux données d'une autre copro.

## Architecture

- [[architecture-full-web-charte]] — Document officiel Denis THEVENOT : conventions Vue 3/Vuetify 3, IHM 4 blocs, routing 3 niveaux, stores Pinia $prefix, eventBus, nomenclature, roadmap WinDev→Vue3.
