# Figure rights and image policy

## Policy

Paper figures used on this site are cropped directly from the author's own PDF copies of each
article (`~/cv/papers/`, not part of this repository) and vendored locally as static PNGs under
`assets/figures/`. A figure is only cropped and used when the source PDF's own text confirms an
open-reuse licence (checked per-paper via the article's copyright/licence statement — see below).
Papers without a confirmed open licence are represented only by citation text and an outbound
link, never by a repackaged figure.

Each crop keeps the original figure's data/diagram content unaltered (no relabeling, no
recomposition of panels); multi-panel figures may be cropped to a single representative panel,
which is noted below. The site's own caption is a short original description, not a
reproduction of the paper's full figure legend, and every embedded figure sits next to its full
citation and an "Open article" link to the original.

Original explanatory SVGs in `assets/` are newly drawn for this portfolio and are labelled as
conceptual/adapted where applicable.

## Cropped paper figures

### Frank et al. 2018 — Current Biology
Article: *Circadian Entrainment in Arabidopsis by the Sugar-Responsive Transcription Factor bZIP63*
DOI: 10.1016/j.cub.2018.05.092 · PMC: PMC6108399
Licence confirmed in source PDF: "This is an open access article under the CC BY license" — **CC BY 4.0**.
Used: `assets/figures/frank2018-graphical-abstract.png` — the article's own Graphical Abstract, cropped from page 1 of the source PDF. Replaces a prior remote PMC hotlink of the same image.

### Viana et al. 2021 — New Phytologist
Article: *The sugar-responsive circadian clock regulator bZIP63 modulates plant growth*
DOI: 10.1111/nph.17518 · PMC: PMC9292441
Licence confirmed in source PDF: "This is an open access article under the terms of the Creative Commons Attribution License" — **CC BY**.
Used: `assets/figures/viana2021-fig5.png` — Figure 5 (the paper's summary model of bZIP63, the circadian clock and starch degradation), cropped from page 11.

### Alves et al. 2021 — Journal of Experimental Botany
Article: *Carbon/nitrogen metabolism and stress response networks – calcium-dependent protein kinases as the missing link?*
DOI: 10.1093/jxb/erab136
Licence confirmed in source PDF: "This is an Open Access article distributed under the terms of the Creative Commons Attribution License" — **CC BY 4.0**.
Used: `assets/figures/alves2021-fig2.png` — Figure 2, the review's representative model integrating CDPKs and SnRK1, cropped from page 9.

### Marques, Matiolli & Abreu 2022 — microPublication Biology (CDPK-OsPPIN)
Article: *Visualization of a curated Oryza sativa L. CDPKs Protein-Protein Interaction Network (CDPK-OsPPIN)*
DOI: 10.17912/micropub.biology.000513 · PMC: PMC8792674
Licence: microPublication Biology publishes all articles **Open Access / CC BY** by default; confirmed by "Open Access" marking in source PDF.
Used: `assets/figures/marques2022-fig1.png` — Figure 1, the full CDPK-OsPPIN network diagram (the article's only figure), cropped from page 2.

### Matiolli et al. 2022 — Frontiers in Plant Science
Article: *Turning the Knobs: The Impact of Post-translational Modifications on Carbon Metabolism*
DOI: 10.3389/fpls.2021.781508 · PMC: PMC8787203
Licence confirmed in source PDF: "distributed under the terms of the Creative Commons Attribution License (CC BY)."
Used: `assets/figures/matiolli2022-fig5.png` — Figure 5 (the review's final summary diagram, PTMs modulating carbon flow through glycolysis), cropped from page 12, diagram only (caption text excluded; a short original caption is used on the site instead).

### Fernandes et al. 2024 — Planta
Article: *SUMOylation of Rice DELLA SLR1 Modulates Transcriptional Responses and Improves Yield Under Salt Stress*
DOI: 10.1007/s00425-024-04565-1
Licence confirmed in source PDF: "This article is licensed under a Creative Commons Attribution 4.0 International License."
Used: `assets/figures/fernandes2024-fig4a.png` — Figure 4, panel (a) only (PCA plot separating genotype/treatment groups), cropped from page 12. The full Figure 4 also contains Venn diagrams and GO bar charts (panels b–e) not used here, in favor of the single clearest panel for a general narrative audience.

### gPPIpred — 2026, microPublication Biology
Article: *gPPIpred: A User-Friendly PPI Predictor Based on Protein Molecular Graphs*
DOI: 10.17912/micropub.biology.001796 · PMC: PMC13109786
Licence: microPublication Biology, **Open Access / CC BY** by default.
Used: `assets/figures/gppipred2026-fig1d.png` — Figure 1, panel (d) only (the model's ROC curve, AUC 0.8451), cropped from page 2. Replaces a prior remote PMC hotlink of the full multi-panel Figure 1.

## Not used as figures (no confirmed open licence, or no clear summary figure)

### Matiolli et al. 2011 — Plant Physiology
Source PDF states "© 2011 American Society of Plant Biologists. All Rights Reserved" — not CC BY.
No figure from this paper is reproduced. Chapter 01 instead uses `assets/mechanism.svg`, an original diagram.

### Matiolli & Melotto 2018 — MPMI
Public-domain US-government-funded work ("in the public domain and not copyrightable"), but the 4-page resource note contains no figure — text-only citation only.

### Oblessuc, Matiolli & Melotto 2020 — BMC Plant Biology
PMC states **CC BY 4.0**, but the paper's figures are data plots (bar charts, micrographs) rather than a conceptual summary figure suited to a general narrative audience. The site links to the article but does not repackage a figure.

## Original diagrams

### data-pipeline.svg
Original schematic, drawn for this portfolio, depicting the excelxtract ETL sequence described in Chapter 03 body text (`raw workbook → sheet classification → wide-to-long normalization → stable sample identity → PCA / t-SNE → interpretable developmental patterns`). Not a reproduction of any paper or repository figure.

### applied-portfolio.svg
Original schematic, drawn for this portfolio, illustrating the shared mechanism-first method applied across the four generalized engagement domains listed on the Portfolio page (agriculture, oncology, biomedical engineering, protein ML). Not a reproduction of any client material; no confidential client identity depicted.

## Important

Remote PMC image paths can change. If a local coding agent replaces them with downloaded assets:
1. confirm the exact article/figure licence;
2. store a source URL and attribution here;
3. do not crop or alter a figure in a scientifically misleading way;
4. if modified, state that the image was adapted.
