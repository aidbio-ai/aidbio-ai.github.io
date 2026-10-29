# AGENTS.md — portfolio implementation rules

## Objective

Maintain a production-quality narrative website explaining **why AidBio exists**, using the scientific trajectory of founder Cleverson Carlos Matiolli, PhD as the causal story.

This is not a generic personal portfolio and not an academic CV dump.

## Narrative invariant

The site must preserve this progression:

`mechanism → regulatory systems → biological networks → data → computational models → reusable scientific software → AidBio`

Every project, paper, visual or technology included should earn its place by explaining one step in that progression.

## Scientific evidence rules

1. Never invent a scientific claim, metric, publication, role, client, citation, DOI or project result.
2. Prefer primary literature, official institutional sources and repository documentation.
3. Distinguish:
   - measured result;
   - interpretation;
   - inference;
   - current software capability.
4. If a numerical metric is used, keep the source in `docs/evidence-map.md`.
5. Do not upgrade exploratory analysis to publication-grade inference.
6. Do not identify confidential clients unless the source material explicitly authorizes public naming.
7. Preserve scientific caveats.

## Figure rules

- Reuse a paper figure only if its article/figure licence permits redistribution and attribution.
- Record the licence and source in `docs/figure-rights.md`.
- Otherwise make an original explanatory diagram labelled `Adapted from ...`.
- Do not imply an adapted diagram is an original paper figure.
- Remote paper images must have accessible fallbacks.

## AidBio design rules

The user-approved redesign uses the supplied AidBio Design System v2.4 and landing-page example under `../examples/` relative to the site root. This supersedes the earlier portfolio palette and font stack for presentation only.

- Share the site's Inter / JetBrains Mono typography, semantic domain colors, 4px rhythm, and light/dark surfaces.
- Preserve the established infinity mark in shared header/footer chrome only.
- Preserve the narrative, evidence records, attributions, and scientific caveats.
- Keep component styling in `assets/site.css`; shared tokens/chrome live at the site root.
- Use the shared Auto / Light / Dark bootstrap and reduced-motion support.
- Do not copy prototype promises, metrics, or internal UI details as factual claims.

## Technical rules

- Static baseline must remain deployable on GitHub Pages.
- Keep relative navigation functional.
- Mobile width 320px must not horizontally overflow.
- Keep semantic HTML and keyboard-accessible links/controls.
- Any JS enhancement must degrade gracefully.
- Do not introduce a framework merely for aesthetics.
- If migrating to Astro/Vite/React, document the rationale and update README.

## Content edits

When changing founder narrative content, update `docs/evidence-map.md` if the factual basis changes.
