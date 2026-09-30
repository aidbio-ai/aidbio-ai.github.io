# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`aidbio-ai.github.io` — the public marketing site for AidBio (AI & data science for life sciences and agritech),
served directly by GitHub Pages. There is no build step, no package manager, and no test suite: every page is a
plain `.html` file. Page-specific styles stay inline; the header, footer, buttons and type helpers are shared
(see "Shared chrome" below).

- `index.html` — main marketing site (hero, sections; header and footer are stamped from `assets/partials/`).
- `aidweather.html` — standalone page for the AidWeather project.
- `assets/` — logomarks, favicon, hero network graphics (WebP/PNG). See table in `README.md` for what each file is.
- `portfolio/` — a separate, self-contained static site (its own `README.md`, `AGENTS.md`, `index.html`, `pages/`,
  `assets/`, `docs/`), tracked in git and merged into `main` — part of the deployed site. Treat it as an
  independent project with its own rules (see below).

## Running locally

No build step required. Serve the directory root and open in a browser:

```bash
python -m http.server 8000
```

There is no linter, formatter, or automated test command configured in this repo — verify changes by opening the
page in a browser (check both light and dark themes, and mobile width ~320px).

## Architecture notes (top-level site)

- **Shared chrome (single source of truth)**: the fixed header (logo, links, theme/language switchers, mobile
  menu), the optional local sub-nav, and the footer are identical on every page. Edit them only in
  `assets/partials/*.html`, then run `python3 scripts/sync-chrome.py` (use `--check` to verify). Pages contain
  `<!--chrome:header|subnav|footer ...-->` marker pairs that the script fills in; never hand-edit inside them.
  Shared CSS lives in `assets/css/chrome.css`, shared JS in `assets/js/chrome.js`. New pages: add the markers,
  link `assets/ds/styles.css` then `assets/css/chrome.css`, load `assets/js/theme.js` in `<head>` (after the
  `theme-color` meta) and `assets/js/chrome.js` at the end of `<body>`.
- **Local navigation**: page families (portfolio chapters, AidWeather sections) add a sticky `.subnav` strip
  under the header via `<!--chrome:subnav set="...">` and `<body class="has-subnav">`. The header never changes.
- **Language switcher**: `i18n="1"` on the header marker adds EN/PT. Only `index.html` has translated content,
  so only it sets the flag; flip it on a page only once that page has PT strings in `assets/i18n/`.
- **Theme system**: `assets/js/theme.js` (blocking, in `<head>`) reads `localStorage` key
  `aidbio-theme-preference` (legacy `aidbio-theme`), resolves `system` via `prefers-color-scheme`, sets
  `data-theme` + `color-scheme` on `<html>` before first paint, and exposes `window.__aidbioTheme`.
- **Design system**: visual identity (spectrum infinity logomark, 8-hue synesthetic palette, Baloo 2 /
  Plus Jakarta Sans / IBM Plex Mono typography, Fibonacci spacing, light+dark themes) follows the external
  `matiollipt/aidbio-design` repo (vendored into `assets/ds/` by `scripts/sync-design-system.sh`) — that repo is the source of truth for brand tokens; don't redefine them
  ad hoc here without checking it.
- Pages are long, single-file documents (2000+ lines for `index.html`) — sections are organized by HTML comments
  and id-anchored `<section>` blocks; search for the relevant section heading/id rather than reading top to bottom.

## Consistency rules

- Logo lockup is fixed everywhere: spectrum mark + wordmark with "Aid" in `--brand-blue` and "Bio" in
  `--brand-orange`, no caption. Only the header/footer partials may render it.
- Heading scale: hero `--fs-h1`, editorial page title `--fs-page-title`, section `--fs-h2`, card `--fs-h3`
  (all in `chrome.css`). One gradient accent word per section heading (`.accent-spectrum`), never in a hero.
- Buttons are `.btn .btn-primary|.btn-secondary|.btn-warm`; eyebrows are `.eyebrow`; alternate section bands
  are `.section-alt`; figures use `.figure` / `.figure-media`; cards use `--radius-lg`, `--shadow-sm`.
- Copy: sentence case, plain and de-hyped (Field Notes voice); no "AI" wording outside the Agentic AI card
  and the portfolio founder narrative; domain is aidbio.org.

## `portfolio/` subproject

This is a distinct narrative site ("why AidBio exists," told through founder Cleverson Carlos Matiolli's scientific
trajectory) with its own strict content rules in `portfolio/AGENTS.md`. If you're asked to work inside `portfolio/`,
read `portfolio/AGENTS.md` in full first — key constraints:

- Narrative must follow: mechanism → regulatory systems → biological networks → data → computational models →
  reusable scientific software → AidBio. Every included project/paper/visual must map to a step in that chain.
- Never invent scientific claims, metrics, publications, roles, clients, citations, DOIs, or results. Distinguish
  measured result vs. interpretation vs. inference vs. current software capability.
- Numerical metrics must be sourced in `portfolio/docs/evidence-map.md`.
- Reused paper figures require a documented redistribution licence in `portfolio/docs/figure-rights.md`; otherwise
  make an original diagram explicitly labelled "Adapted from ...".
- Must stay deployable as static GitHub Pages (no framework migration without documenting rationale in
  `portfolio/README.md` and updating it).
- Mobile width 320px must not overflow; keep semantic HTML and keyboard-accessible controls; JS enhancements must
  degrade gracefully.

Run locally the same way (`python -m http.server 8000` from inside `portfolio/`).

## Domain, DNS, and email (aidbio.org)

The custom domain `aidbio.org` is registered and DNS-managed on Cloudflare (Cloudflare Registrar + Cloudflare
DNS), pointed at this repo's GitHub Pages hosting, with Cloudflare Email Routing forwarding `contact@aidbio.org`.
This repo has no `CNAME` file to touch for that — DNS is managed entirely on Cloudflare's side, not in-repo.

For anything involving DNS records, SPF/DKIM/DMARC, email forwarding rules, or registrar/WHOIS status, use the
`aidbio-domain` Claude Code skill rather than guessing — it has the current zone setup and known gotchas (e.g.
the Cloudflare API token in use is read-only; writes must go through the dashboard). Account IDs and other
infra specifics are intentionally kept out of this public repo; see that skill instead.
