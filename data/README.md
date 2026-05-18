# Data sources for mitophagy-perturb-atlas

## Datasets

### DepMap — primary fitness source
- **Source**: DepMap portal (https://depmap.org/portal/download/)
- **Pinned release**: 24Q2 (see ADR-0001; reconfirm in Q2 of QUESTIONS.md)
- **Citation**: Tsherniak A. *et al.* (2017) *Cell* 170(3):564-576.
  doi:10.1016/j.cell.2017.06.010 (plus subsequent DepMap releases)
- **License**: CC-BY 4.0 on the release files
- **Approximate size**: ~500 MB for the fitness matrices we need

### Replogle 2022 — Perturb-Seq
- **Source**: GSE197561 / Figshare bundle linked in the paper
- **Citation**: Replogle J.M. *et al.* (2022) *Cell* 185(14):2559-2575.
  doi:10.1016/j.cell.2022.05.013
- **License**: terms in the GEO record
- **Approximate size**: substantial — see paper

### Reactome — pathway definitions
- **Source**: Reactome ContentService (https://reactome.org/ContentService/)
- **Citation**: Milacic M. *et al.* (2024) *Nucleic Acids Research*
  52(D1):D672-D678. doi:10.1093/nar/gkad1025
- **Snapshot**: the pathway gene set version is recorded per call.

## Cache layout
Downloads land under `$XDG_CACHE_HOME/mitophagy_perturb_atlas/`.

## Provenance
Every result figure has a `.caption.md` sidecar with dataset versions,
notebook cell, and commit SHA.