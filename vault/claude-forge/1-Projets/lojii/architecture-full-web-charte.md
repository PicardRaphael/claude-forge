---
titre: "Architecture Full Web — Charte Front-End Lojii"
resume: "Document officiel Denis THEVENOT : conventions Vue 3/Vuetify 3, IHM 4 blocs, routing 3 niveaux, stores Pinia $prefix, eventBus, nomenclature, roadmap WinDev→Vue3"
aliases:
  - architecture full web
  - charte frontend lojii
  - conventions denis thevenot
  - charte front-end neoteem
  - process charte front
  - nomenclature lojii
  - IHM lojii blocs
type: knowledge
derniere-maj: 2026-05-13
auteur: claude
sources:
  - "Architecture Full Web.pdf (Denis THEVENOT, 22/03/2024, maj 30/10/2025)"
tags:
  - "#type/knowledge"
  - "#projet/lojii"
  - "#domaine/tech"
---

## Document source

PDF de 23 pages par Denis THEVENOT, document de reference OFFICIEL pour toutes les conventions du projet [[lojii]]. Copie integrale dans `.claude/skills/lojii-conventions/references/architecture-full-web.md`.

## Points cles

### IHM — 4 blocs (1920x1080)

- **MainMenu** : 60px ferme, ~300px ouvert, toute hauteur
- **BarOnglets** : 40px haut, visible si mode WebApp + onglet ouvert (ctrl+clic)
- **BarTitre** : 50px haut, bouton retour + icone + titre + recherche + notifications + panneau user
- **ModuleMain** : largeur dynamique (1570 avec menu, 1870 sans), hauteur proportionnelle

### Routing 3 niveaux

1. `App.vue` → `<router-view />` = module/fiche
2. `Module.vue` → `<ModuleMenu /> + <router-view />` = interface
3. `_App.vue` → `<router-view />` = vue de l'interface

Routes 1er niveau commencent par `/`, enfants sans `/`. Lazy import obligatoire.

### Nomenclature `$` prefix

Tous les globaux prefixes `$` : `$main`, `$menu`, `$router`, `$route`, `$eventBus`, `$props`, `$emit`, `$rechercheGlobale`.

### Navigation

`$eventBus.$emit('change-route', '/path')` — JAMAIS `$router.push` (sauf dans template @click).

### hideMenu / hideIhm

Meta route pour ecrans Chromium WinDev : `meta: { hideMenu: true, hideIhm: true }`.

### Arborescence

- `views/` et `components/` : PascalCase, modules au 1er niveau (pas d'activite Syndic/Gerance/Commun)
- `composables/` : kebab-case, meme structure que components
- `_common/` : transverse, `_bibliotheque/` : composants migres Vue3
- `plugins/` : centralise (utils, filters, eventBus, neoteem, menus, store)

### Roadmap (7/11 etapes faites)

- [x] POC → Vue2 → Vue3/Vite → migration composants → bibliotheque
- [ ] Migration derniers ecrans WinDev
- [ ] Implementation iframes projets isoles Vue2
- [ ] Desactiver Lojii WD, lancer Lojii FW
- [ ] Migration derniers projets Vue2

## Liens

- [[lojii]] — projet frontend
- [[windev-front]] — application desktop a migrer
