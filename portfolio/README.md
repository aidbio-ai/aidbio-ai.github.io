# AidBio Founder Story Portfolio

A static, multi-page narrative portfolio explaining **why AidBio exists** through the scientific trajectory of founder Cleverson Carlos Matiolli, PhD.

## What this is

This is deliberately **not** a conventional CV website. The primary experience is a tutorial-like progression:

1. molecular mechanisms;
2. biological networks;
3. high-dimensional biological data;
4. graph-based prediction;
5. reproducible scientific software;
6. AidBio as the synthesis.

Scientific claims are grounded in primary publications or repository documentation. Original explanatory diagrams are labelled as adapted/schematic. Paper figures are used only when the underlying article is open access and an appropriate reuse licence is documented; they fall back gracefully if unavailable when browsing offline.

## Run locally

No build step is required.

```bash
python -m http.server 8000
```

Open http://localhost:8000

## Git setup

```bash
git init
git branch -M main
git add .
git commit -m "Initial AidBio founder story portfolio"
git remote add origin git@github.com:matiollipt/portfolio.git
git push -u origin main
```

## GitHub Pages

Repository settings → Pages → Deploy from branch → `main` / root.

Because the site uses relative links and static assets, no additional build configuration is needed.

## Design source of truth

The visual language is adapted from:

`matiollipt/aidbio-design-system`

Key rules carried into this repository:

- AidBio synesthetic spectrum;
- biology/network/infinity motifs;
- warm humanist headings + clean UI body + monospace data text;
- Fibonacci-derived spacing rhythm;
- soft graphite-tinted elevation;
- calm interactions and reduced-motion support;
- scientific, accurate copy without hype.

The original design-system repository remains canonical. Do not silently redefine AidBio brand tokens here without reconciling the change upstream.

## Paper imagery

The site currently attempts to display selected open-access paper figures from PMC as remote images and provides a text fallback. This avoids repackaging third-party figure files into the repository.

See `docs/figure-rights.md`.

## Next engineering step

A local coding agent may refactor this static baseline into Astro/Vite/React **only if there is a concrete benefit**. Preserve URLs, semantic content, citation provenance and the founder-story progression.
