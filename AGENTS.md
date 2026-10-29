# AGENTS.md

## Repository

AidBio's public site at aidbio.org. Static HTML on GitHub Pages: no framework, package manager, or build pipeline. Serve with `python3 -m http.server 8000`.

Marketing pages: `index.html`, `solutions.html`, `work.html`, `tools.html`, `about.html`, `aidweather.html`, `404.html`. `portfolio/` is the restored eight-page scientific narrative. `sample-report/` is an existing generated report and is excluded from chrome generation.

## Approved design and content

The October 2026 redesign follows the supplied `../examples/aidbio_design_system.md` (v2.4) and `../examples/aidbio_landing_page.html`. These user-approved references supersede the former Baloo/Jakarta/spectrum presentation. Do not copy unsupported claims, percentages, or prototype internals from the example.

- Shared semantic tokens and component styles: `assets/css/aidbio.css`.
- Inter / JetBrains Mono are self-hosted. Preserve the established infinity mark + Aid (blue) / Bio (orange) wordmark in shared chrome only.
- Use restrained emerald, amber, violet, and cyan accents, 4px spacing, fine borders, and light/dark surfaces. Keep heroes solid-text.
- Copy is precise, calm, and scientifically grounded. Explain domain vocabulary through questions, methods, and outputs; do not erase scientific specificity.
- Never invent clients, results, metrics, maturity, publication status, or installation commands. Distinguish predictions, annotations, exploratory analysis, measured results, and interpretation.
- Public examples use public sources or clearly labeled synthetic data. Client material stays private.

## Shared implementation

Edit chrome only in `assets/partials/`, then run `python3 scripts/build-chrome.py`. Header/footer/subnav marker pairs are generated. The script handles root and portfolio pages, correct relative paths, active navigation, and homepage-only language controls. New pages need a unique `main` ID and one h1.

All pages load blocking `assets/js/theme.js` after the theme-color meta and before styles. The preference key is `aidbio-theme-preference`, with legacy `aidbio-theme` fallback. Values are `system`, `light`, and `dark`; Auto follows OS changes live. Do not introduce another theme controller. `assets/js/app.js` wires controls, menu, tabs, and copy buttons.

Only the homepage is translated. Its strings are in `assets/i18n/home.js`; `assets/js/i18n.js` updates text, metadata, and accessibility labels. EN/PT controls appear only where translations exist; use natural Brazilian Portuguese. Other pages remain English.

## Portfolio and examples

Read `portfolio/AGENTS.md` before changing narrative content. Preserve mechanism → regulatory systems → biological networks → data → computational models → reusable scientific software → AidBio. Numerical claims require `portfolio/docs/evidence-map.md`; reproduced figures require `portfolio/docs/figure-rights.md`.

`scripts/collect-site-examples.py` extracts existing outputs only. Asset provenance and checksums live in `assets/examples/manifest.json`. Never silently replace archived outputs with a different application's current capabilities. Server and local checkouts differ: see `docs/application-examples.md`. Do not launch application downloads/training/model runs as part of ordinary site work.

## Verification

```bash
python3 scripts/build-chrome.py --check
python3 scripts/check-site.py
node scripts/theme.test.cjs
node --check assets/js/theme.js
node --check assets/js/app.js
node --check assets/js/i18n.js
git diff --check
```

Open pages in both themes and at mobile width 320px. Check keyboard focus, Auto mode, language controls, image loading, and no horizontal page overflow. Record actual checks in `docs/verification.md`. Preserve graceful navigation and OS-theme fallback when JavaScript fails.

## Domain

DNS, registrar, and email routing are managed on Cloudflare. Do not change DNS or the existing CNAME as part of a visual/content update. For DNS/email work, locate and read the `aidbio-domain` skill before acting; infrastructure credentials and account identifiers do not belong in this public repository.
