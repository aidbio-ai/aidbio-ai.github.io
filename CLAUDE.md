# CLAUDE.md

## What this repo is
`aidbio-ai.github.io` — the public site for AidBio (aidbio.org), served by GitHub Pages. Plain `.html`, shared CSS/JS,
no package manager or test suite. English only for now; Portuguese comes after the English site is approved.
The previous site (spectrum-infinity design, portfolio/founder pages, i18n) is archived in
`../aidbio-ai.github.io-backup-2026-10-14/`.

## Architecture
- Design: AidBio Design System v2.4 (`../examples/aidbio_design_system.md`): emerald/amber/violet/cyan accents, Inter + JetBrains
  Mono, 4px spacing, dark default + light. All tokens are CSS custom properties at the top of `assets/css/aidbio.css`.
- No CDN or Tailwind: fonts are self-hosted, icons are inline SVG. `sample-report/` is the one exception (Plotly/MapLibre).
- Shared chrome: edit `assets/partials/{header,footer,mark}.html`, then `python3 scripts/build-chrome.py` (`--check` to verify).
  Never hand-edit inside `<!--chrome:...-->` markers. Pages load an inline theme script in `<head>` (key `aidbio-theme`).
- Logo: the infinity mark (`assets/img/aidbio-mark-{light,dark}.webp`) plus wordmark "Aid" (blue) "Bio" (orange).
- Verify by serving the folder and checking light/dark and 320px width (no horizontal scroll).

## Content rules
- Plain English, sentence case, lead with the reader's problem; technical terms only where needed.
- Audience: academic groups and industry. No founder-centred content. No prices.
- Do not invent metrics, clients, results or claims; demo visuals are labelled illustrative.
- Client work stays anonymised; confidential data (e.g. farm datasets) is never shown.
- Tools install by `git clone` + `uv tool install ./<repo>` (not pip). Contact is `contact@aidbio.org` (mailto).

## Domain, DNS, email
`aidbio.org` is on Cloudflare (registrar, DNS, Email Routing for contact@aidbio.org); no CNAME work in-repo besides the
`CNAME` file. For DNS/email questions use the `aidbio-domain` skill.
