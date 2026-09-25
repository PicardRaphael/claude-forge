---
titre: "PDF via Chrome headless — génération pro"
resume: "Chaîne Chrome headless + Poppler pour générer des PDF professionnels depuis HTML/CSS, avec gotchas CSS vérifiés (pages blanches, tables, en-têtes, flags)."
aliases:
  - pdf-chrome-headless
  - chrome-headless-pdf
  - génération-pdf-pro
  - chrome-print-to-pdf
  - pdf-headless-gotchas
derniere-maj: 2026-09-25
tags:
  - "#type/technique"
  - "#domaine/outils"
type: technique
---

## Chaîne d'outils

**Outils requis** : Chrome + Poppler (`scoop install poppler` → `pdftoppm`, `pdfinfo`). Pas besoin de weasyprint / reportlab / puppeteer.

**Commande qui marche** :
```bash
chrome --headless=new --disable-gpu \
  --user-data-dir="$tmp" \
  --no-pdf-header-footer \
  --print-to-pdf="$out" "file:///...html"
```

- `--headless=new` + `--user-data-dir` temporaire OBLIGATOIRES — sans eux, échec silencieux si Chrome tourne déjà.
- Génération Python : vérifier la présence de Chrome avec `shutil.which` avant d'appeler — absent en Cowork cloud (fallback markdown autoportant).

## Gotchas CSS / mise en page

### Flag en-têtes
- **`--no-pdf-header-footer`** (Chrome 130+) — supprime date + URL + numéro de page parasites.
- `--print-to-pdf-no-header` est **ignoré silencieusement** sur Chrome récent → ne pas utiliser.

### Pages blanches
- Ne PAS mettre header/footer comme éléments de flux HTML répétés par section : ils débordent et génèrent des pages orphelines avec seulement le footer.
- Choisir : soit en-têtes/pieds via Chrome natif (`--no-pdf-header-footer` retiré), soit aucun footer répété dans le HTML.

### Tables
- **NE PAS** mettre `break-inside: avoid` sur `<table>` → un grand tableau saute entier, laissant une demi-page vide.
- Mettre `break-inside: avoid` sur `tr` uniquement.
- Ajouter `thead { display: table-header-group }` pour répéter l'en-tête si le tableau est coupé sur plusieurs pages.
- **Double `<thead>`** dans un tableau HTML = double en-tête affiché — vérifier visuellement.

### Titres et sauts de page
- `h1` : garder `break-after: avoid`.
- `h2` : **PAS** de `break-after: avoid` — sinon « h2 + grand tableau » sautent ensemble → demi-page vide avant le tableau.

## Vérification visuelle

```bash
pdftoppm -png -r 55 doc.pdf out/p
```

Puis inspecter les images générées. Une page < 12 Ko PNG = potentielle page vide à inspecter.

Note : `chrome --headless --screenshot` rend le HTML mais PAS le viewer PDF (page noire) — ne pas utiliser pour vérifier le rendu PDF.

## Charte Neoteem

CSS de référence : `output/neoteem/_charte/neoteem-charte.css` + `CHARTE.md`.
- Couleurs : bleu `#0a3a5c`, teal `#00a78e`, dégradé teal → corail → magenta.
- Page de garde : fond clair + logo couleur. **PAS** de filtre `brightness` / `invert` sur le logo `.webp` (casse les couleurs).

## Liens

- [[ia-workbench-repo-management]] — usage dans le repo ia-workbench (PDF optionnel avec fallback)
- [[comprendre-neoteem-vue-responsable-ia]] — § trilogie CODIR, premier document généré avec cette chaîne (validé 29 mai 2026)
