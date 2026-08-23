# Evidence map

This document records the factual basis used by the website.

## Founder narrative

Primary internal source:
- `From Plant Molecular Biology to Scientific AI — The Trajectory of Cleverson Carlos Matiolli, PhD`
- `cleverson-matiolli-academic-cv-2026-08.md`
- `cleverson-matiolli-industry-cv-2026-08.md`

These files establish the career chronology, research themes, education, roles and software direction.

## Chapter 01 — Mechanism

### AtbZIP63 integrates glucose and ABA
Matiolli CC et al. *The Arabidopsis bZIP Gene AtbZIP63 Is a Sensitive Integrator of Transient Abscisic Acid and Glucose Signals.* Plant Physiology 157, 692–705 (2011).
DOI: 10.1104/pp.111.181743
PMC: PMC3192551

### Sugar-responsive circadian entrainment
Frank A, Matiolli CC (equal contribution), et al. *Circadian Entrainment in Arabidopsis by the Sugar-Responsive Transcription Factor bZIP63.* Current Biology 28, 2597–2606.e6 (2018).
DOI: 10.1016/j.cub.2018.05.092
PMC: PMC6108399
Key claim: bZIP63 regulates PRR7 and participates in sugar-dependent adjustment of circadian phase.

### Growth
Viana AJC, Matiolli CC (equal contribution), et al. *The sugar-responsive circadian clock regulator bZIP63 modulates plant growth.* New Phytologist 231, 1875–1889 (2021).
DOI: 10.1111/nph.17518
PMC: PMC9292441

## Chapter 02 — Networks

Matiolli CC, Melotto M. *A Comprehensive Arabidopsis Yeast Two-Hybrid Library for Protein-Protein Interaction Studies: A Resource to the Plant Research Community.* MPMI 31, 899–902 (2018).
DOI: 10.1094/MPMI-02-18-0047-A

Oblessuc PR, Matiolli CC, Melotto M. *Novel molecular components involved in callose-mediated Arabidopsis defense against Salmonella enterica and Escherichia coli O157:H7.* BMC Plant Biology 20, 16 (2020).
DOI: 10.1186/s12870-019-2232-x
PMC: PMC6950905

Marques J, Matiolli CC, Abreu IA. *Visualization of a curated Oryza sativa L. CDPKs Protein-Protein Interaction Network (CDPK-OsPPIN).* microPublication Biology (2022).
DOI: 10.17912/micropub.biology.000513
PMC: PMC8792674

Matiolli CC, Soares RC, et al. *Turning the Knobs: The Impact of Post-translational Modifications on Carbon Metabolism.* Frontiers in Plant Science 12:781508.
DOI: 10.3389/fpls.2021.781508
PMC: PMC8787203

Fernandes T, Gonçalves NM, Matiolli CC, Rodrigues MAA, Barros PM, Oliveira MM, Abreu IA. *SUMOylation of Rice DELLA SLR1 Modulates Transcriptional Responses and Improves Yield Under Salt Stress.* Planta 260 (2024).
DOI: 10.1007/s00425-024-04565-1
Source: verified against /home/clever/aidbio/site/add-ons/papers.html (title, author order, journal, year, DOI cross-checked).

## Chapter 03 — Data

The ~80% reduction in manual image-processing effort is supported by the 2026 academic/industry CV source supplied for this portfolio.

Repository evidence:
- `matiollipt/excelxtract` README: multi-sheet Excel ETL, wide-to-long normalization, persistent biological IDs, PCA/t-SNE.
- `matiollipt/aidgsea` README: GEO/SRA routes, Salmon, GSEA, explicit exploratory-vs-publication inference scope.

## Chapter 04 — Models

Matiolli CC, Marques J, Abreu IA. *gPPIpred: A User-Friendly PPI Predictor Based on Protein Molecular Graphs.* microPublication Biology (2026).
DOI: 10.17912/micropub.biology.001796
PMC: PMC13109786
Paper reports:
- GATv2-based Siamese network
- independent validation: 72,358 protein pairs
- MCC 0.4641
- sensitivity 96% at selected threshold

Repository evidence:
- `matiollipt/aid2go` README: heterogeneous graph combining PPI, GO hierarchy and protein-GO experimental annotations; GraphSAGE and GAT variants; ProtBERT sequence embedding stage.

## Chapter 05 — Software

### AidWeather
Repository README:
- NASA POWER integration
- point/transect/regional fetching
- SQLite cache
- Python API + CLI
- explicit source-grid/provenance caveats
- beta status

### AidViz
Repository README:
- visualization boundary only
- static figures
- dashboards
- climate storytelling
- no data fetching or modeling

### AidGSEA
Repository README:
- processed GEO and raw SRA routes
- modular package
- enrichment workflow
- explicit warning that exploratory log2FC is not publication-grade differential-expression inference

### AidFarm
Repository README:
- artifact-driven workflow
- schema-confirmation layer
- deterministic ETL, statistics and visualization
- Evidence V2 bundle
- claim ledger and reasoning plan
- context budgeting
- LangGraph reporting
- local Ollama support
- principle: file-backed/deterministic evidence before LLM interpretation

## Portfolio page — applied engagements

Primary internal sources:
- `cleverson-matiolli-industry-cv-2026-08.md`, "Founder and Lead Data Scientist, AidBio" bullets and "Selected Technical Projects" section.
- `consultancy_projects_cleverson_matiolli.md` (Agritech Consulting, Transcriptomics, 3D-Printed Implants summaries).

Claims used:
- Field-trial agroclimatic analytics for a "multinational food and beverage client," coffee reproductive-development analysis (industry CV). Client identity generalized per source; not authorized for public naming.
- Flower-to-pod conversion yield modeling: negative binomial regression, random forest/XGBoost (consultancy doc).
- Melanoma transcriptomics: RNA-seq, DESeq2, PCA/t-SNE, GSEA, sensitive-vs-resistant cohort signatures (consultancy doc; industry CV corroborates "transcriptomic patient stratification in precision oncology").
- 3D-printed Ti-6Al-4V lattice implants: mechanical testing (Young's modulus, yield stress, compressive strength) plus PLSR/random forest/XGBoost (consultancy doc; industry CV corroborates "regression-based optimization of 3D-printed metallic lattice implants").
- gPPIpred/Aid2GO entries link to and reuse only claims already sourced in Chapter 04 above.

Deliberately excluded: "Agrilyzer" (consultancy doc) — its description overlaps closely with AidWeather and is not corroborated by the more recent industry CV under a distinct name, so it was not presented as a separate product to avoid an unverifiable claim.

## Current repository evidence inspected

- matiollipt/aidbio-design-system
- matiollipt/aidweather
- matiollipt/excelxtract
- matiollipt/aid2go
- matiollipt/aidgsea
- matiollipt/aidviz
- matiollipt/aidfarm
