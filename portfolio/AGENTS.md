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

Canonical source of truth: `matiollipt/aidbio-design-system`.

Carry forward:
- synesthetic eight-hue data spectrum;
- AidBio infinity/biology/data identity;
- Baloo 2-style warm display typography;
- Plus Jakarta Sans-style body typography;
- IBM Plex Mono-style numerical/data labels;
- Fibonacci rhythm (4, 8, 13, 21, 34, 55, 89...);
- rounded ~18 px cards;
- soft cool shadows;
- scientific copy without hype;
- reduced-motion support.

Do not copy prototype internals blindly. Match the design intent.

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
