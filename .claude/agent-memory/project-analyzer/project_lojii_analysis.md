---
name: project-lojii-analysis
description: Lojii frontend analysis - Vue 3.5/Vuetify 3/Vite 6 property management SPA, 634 .vue files, mixed Composition/Options API, Bitbucket, no .claude components
metadata:
  type: project
---

## 2026-05-13 -- Lojii (Vue 3.5 / Vuetify 3.7 / Vite 6 / Pinia 3)

### Stack
- Vue 3.5.13, Vuetify 3.7.17, Vite 6.2.1, Pinia 3.0.1, Vue Router 4.5
- JavaScript (no TypeScript), SCSS, Prettier + ESLint flat config
- Vitest + Playwright (26 unit tests, 1 e2e test)
- Husky pre-commit (branch protection only)
- yarn.lock (lockfile), pnpm config in package.json but uses yarn
- CI: Bitbucket Pipelines on develop/test/prepilote/master

### Architecture
- 634 Vue files, ~87K lines total, 26MB src
- 338 <script setup> (Composition API) vs 258 export default (Options API) = ~57% migrated
- 29 Pinia stores + 1 legacy reactive store (plugins/store.js)
- 20 router files (hash history), 27 route modules
- Composables: useEcranConfig, useNeodocChat, useTiersList, FicheActeur (1163L), + _bibliotheque composables
- Giant files: NeoChat.vue (3140L), menus.js (5055L), lots-vacants.js (1620L), visite-immeuble.js (1286L), FicheActeur.js (1163L)

### Claude Code Config
- CLAUDE.md: 330 lines (trop long, references phantom components)
- .claude/: ONLY settings.local.json (chrome-devtools permissions)
- .claude is in .gitignore (NOT shared with team)
- NO agents, skills, rules, hooks exist
- CLAUDE.md references nonexistent skills/agents/commands
- No .mcp.json (chrome-devtools MCP referenced but not configured)

### Key Patterns
- API layer: neoteem.js wrapper (fetch + auth token from window.Auth)
- Auth: window.Auth, window.currentUser, window.cloud_run (global state)
- Event bus: vue-eventer ($eventBus.$emit for navigation)
- Global components: nt-* auto-registered from _bibliotheque/Fields, Boutons, Avatar, Autre
- SCSS: variables auto-imported globally via vite, Material Design Icons via CDN
- PWA: vite-plugin-pwa with workbox
- TinyMCE 6: loaded from CDN, not bundled
- Tiptap 3: newer rich text editor (replacing TinyMCE?)

### Tech Debt
- 2 eslint configs at root (.js and .mjs) = nondeterministic pick
- Options API components still use deprecated Vue 2 patterns (4 TODO comments in eslint.config.js)
- Legacy store.js (reactive object, 242L) coexists with Pinia
- menus.js at 5055 lines / 191KB
- NeoChat.vue at 3140 lines (should be decomposed)
- ia/chatbot = pre-built Vue 2 chatbot (chunk-vendors, separate app)
- `Bash(find:*)` permission format is wrong (colon instead of space)

### IA Module
- Routes: /ia (home), /ia/neochat/:threadId?, /ia/neodoc/:id?
- Views: NeoChat.vue (3140L), NeoDoc.vue (22254B), Home.vue
- Components: Conversations, FavoriteDetail, Favorites, FormFeedback, IAFooter, IAHeader, neodoc/, SourcesFeedback, ViewSwitcher
- Plugins: chatApi.js (25K), markdown.js (12K), neodocApi.js, neoteemLegacy.js
- Composables: useNeodocChat.js
- Separate chatbot build in ia/chatbot/ (legacy Vue 2 build)

### Business Modules (12)
Commercialisation, Banque, SuiviProprietaire, SuiviLocataire, FicheProprietaire, FicheLocataire, FicheCopropriete, FicheCoproprietaire, FicheActeur, Administration, Migration, MandatCopropriete + IA + Fournisseurs + Relances + Requetes + Mutation + Assurance
