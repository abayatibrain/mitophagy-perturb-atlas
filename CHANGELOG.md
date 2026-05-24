# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added — first implementation slice (2026-05-23)
- **`pathway/mitophagy_spine.py`** — canonical 18-gene PINK1/Parkin
  spine + curated extended spine (Pickrell & Youle 2015; Lazarou 2015;
  Reactome R-HSA-5205647).
- **`io/depmap.py`** — real `load_depmap_essentiality()` against the
  public CRISPRGeneEffect CSV (pinned 24Q2 per ADR-0002) +
  `make_synthetic_depmap()` deterministic fixture with engineered
  PRKN–PINK1 phenocopy signal. Pivot helper to gene-matrix form.
- **`io/replogle2022.py`** — TSV loaders for K562 + RPE1 pseudobulk
  (ADR-0003) + synthetic fixture + pivot helper.
- **`analysis/similarity.py`** — vectorised cosine + Pearson + Spearman
  in one `gene_query` entry point (ADR-0004).
- **`analysis/phenocopy.py`** — empirical-null per metric (ADR-0006) +
  Benjamini-Hochberg q-values + `sig` flag at α=0.05.
- **22 unit tests** across `test_pathway`, `test_io`, `test_phenocopy`.
  All passing; ruff check clean. PRKN-as-query end-to-end acceptance
  gate: PINK1 in top-5 candidates for every metric.

### Added — ADR sprint (2026-05-19)
- **ADR-0002** — DepMap release pinning (proposed 24Q2).
- **ADR-0003** — Replogle 2022 cell-line subset (proposed K562 + RPE1
  in parallel columns).
- **ADR-0004** — Similarity metric (proposed cosine as headline,
  Pearson side-by-side, Spearman robustness check).
- **ADR-0005** — Pathway-definition scope (proposed Reactome primary,
  KEGG + GO cross-checks; receptor-mediated mitophagy in scope).
- **ADR-0006** — Phenocopy FDR methodology (proposed empirical null
  via random gene pairing, per modality, n=10,000).
- Decision-log index with dependency graph and reader-by-role guidance.
- QUESTIONS.md reorganized as a per-ADR Saturday-morning review queue.
- STATUS.md updated for the ADR-sprint phase.

### Notes
All six ADRs are in **Proposed — awaiting Armin sign-off** status.
Code implementation does not begin until sign-off lands in
`QUESTIONS.md` (the same pattern Repo 1 followed).

### Added — scaffolding (pre-sprint)
- Initial repository scaffolding per the Cowork brief §2.1.
- CI workflow (lint + type + test + coverage), docs workflow, release workflow.
- mkdocs-material site skeleton.
