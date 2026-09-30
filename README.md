# aidbio-ai.github.io

AidBio's public site — AI & data science for life sciences and agritech.

Static single-page site (GitHub Pages), no build step. Visual identity follows the
[AidBio Design System](https://github.com/matiollipt/aidbio-design-system):
spectrum infinity logomark, synesthetic 8-hue palette, Newsreader / Hanken Grotesk /
IBM Plex Mono typography, Fibonacci spacing, and light + dark themes.

## Assets

| File | Purpose |
| --- | --- |
| `assets/aidbio-mark-light.webp` | Infinity logomark for light surfaces (nav, hero, brand) |
| `assets/aidbio-mark-dark.webp` | Infinity logomark for dark surfaces (dark theme, footer) |
| `assets/network-light.webp` / `network-dark.webp` | Golden-angle network motif behind the hero |
| `assets/favicon.png` | Favicon derived from the logomark |
| `assets/apple-touch-icon.png` | iOS home-screen icon (opaque cloud background) |

Marks were derived from the design system's `project/assets/aidbio-logo-{light,dark}.png`
(background removed, trimmed, downscaled, converted to WebP).

## Shared chrome

The header, footer and local sub-nav are generated from `assets/partials/` into every page by
`python3 scripts/sync-chrome.py` (run with `--check` in CI or before committing). Shared styles and scripts:
`assets/css/chrome.css`, `assets/js/theme.js`, `assets/js/chrome.js`. See `CLAUDE.md` for the page contract.
