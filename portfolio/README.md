# AidBio founder story

Eight static narrative pages explain why AidBio exists through Cleverson Carlos Matiolli's scientific trajectory: mechanism → regulatory systems → biological networks → data → computational models → reusable scientific software → AidBio. The applied-work page shows how the method transfers to other domains.

This directory is part of the parent GitHub Pages site. Do not initialize a nested Git repository or deploy it separately.

## Preview and shared implementation

Serve from the **parent site root** so shared assets and navigation resolve:

```bash
python3 -m http.server 8000
```

Open `http://127.0.0.1:8000/portfolio/`.

The user-approved v2.4 redesign shares Inter / JetBrains Mono typography, semantic domain colors, surfaces, spacing, Auto / Light / Dark behavior, header, and footer with the marketing site. `assets/site.css` contains narrative-only components. Shared assets live in the parent `assets/` directory.

From the parent root:

```bash
python3 scripts/build-chrome.py
python3 scripts/build-chrome.py --check
python3 scripts/check-site.py
```

Chapter navigation is generated along with shared chrome. Preserve the existing chapter URLs. The portfolio remains English; only the homepage offers EN/PT.

## Evidence and imagery

Read [AGENTS.md](AGENTS.md) before editing. Numerical claims belong in [docs/evidence-map.md](docs/evidence-map.md); citation details and figure rights live in the other documents under `docs/`.

Original SVG diagrams are identified as explanatory/schematic. The selected paper figures are vendored locally, with licenses and original attribution recorded in [docs/figure-rights.md](docs/figure-rights.md). Preserve captions, scientific caveats, and distinctions between published findings and current software capabilities.

The previous design specification remains a historical record. Current presentation authority and the implementation/verification records are documented at the parent site root.
