# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`aidbio-ai.github.io` — the public marketing site for AidBio (AI & data science for life sciences and agritech),
served directly by GitHub Pages. There is no build step, no package manager, and no test suite: every page is a
single self-contained `.html` file with inline `<style>` and `<script>`.

- `index.html` — main marketing site (nav, hero, sections, footer; theme toggle logic inline in `<head>`).
- `aidweather.html` — standalone page for the AidWeather project.
- `assets/` — logomarks, favicon, hero network graphics (WebP/PNG). See table in `README.md` for what each file is.
- `portfolio/` — a separate, self-contained static site (its own `README.md`, `AGENTS.md`, `index.html`, `pages/`,
  `assets/`, `docs/`). It is currently untracked in git (not yet committed) — check `git status` before assuming
  it's part of the deployed site. Treat it as an independent project with its own rules (see below).

## Running locally

No build step required. Serve the directory root and open in a browser:

```bash
python -m http.server 8000
```

There is no linter, formatter, or automated test command configured in this repo — verify changes by opening the
page in a browser (check both light and dark themes, and mobile width ~320px).

## Architecture notes (top-level site)

- **Theme system**: light/dark theme is resolved by an inline IIFE at the top of `<head>` in `index.html`
  (before CSS loads, to avoid a flash of wrong theme). It reads `localStorage` key `aidbio-theme-preference`
  (falling back to legacy key `aidbio-theme`), resolves `system` via `prefers-color-scheme`, and sets
  `data-theme` + `color-scheme` on `<html>`. A later toggle control in the page calls into
  `window.__aidbioTheme.applyTheme(...)`. If you add new pages, replicate this same inline snippet before any
  stylesheet/content that depends on theme, not just a CSS media query.
- **Design system**: visual identity (spectrum infinity logomark, 8-hue synesthetic palette, Newsreader /
  Hanken Grotesk / IBM Plex Mono typography, Fibonacci spacing, light+dark themes) follows the external
  `matiollipt/aidbio-design-system` repo — that repo is the source of truth for brand tokens; don't redefine them
  ad hoc here without checking it.
- Pages are long, single-file documents (2000+ lines for `index.html`) — sections are organized by HTML comments
  and id-anchored `<section>` blocks; search for the relevant section heading/id rather than reading top to bottom.

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
