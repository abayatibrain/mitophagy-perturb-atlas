# Status — week of 2026-05-19
Repo: mitophagy-perturb-atlas
Phase: Implementation — first slice landed

## Completed this week
- ADR sprint (six ADRs proposed; see `docs/decisions/`).
- **First implementation slice landed (2026-05-23):**
  - `pathway/mitophagy_spine.py` — canonical 18-gene PINK1/Parkin
    mitophagy spine + a curated extended spine. Sourced from Reactome
    R-HSA-5205647 + Pickrell & Youle (2015) + Lazarou et al. (2015).
  - `io/depmap.py` — `load_depmap_essentiality()` for the real
    DepMap CRISPRGeneEffect CSV (pinned to release 24Q2 per ADR-0002);
    `make_synthetic_depmap()` for a deterministic shippable fixture.
    Pivot helper to gene-matrix form.
  - `io/replogle2022.py` — TSV loader for both K562 and RPE1
    pseudobulk per ADR-0003; deterministic synthetic generator.
    Pivot helper.
  - `analysis/similarity.py` — cosine + Pearson + Spearman in one
    vectorised `gene_query` entry point per ADR-0004.
  - `analysis/phenocopy.py` — `detect_phenocopy()` with empirical-null
    sampling per metric (ADR-0006) + Benjamini-Hochberg q-values + a
    boolean `sig` flag at α=0.05.
  - PRKN-as-query end-to-end check baked into the synthetic data: the
    PRKN-PINK1 phenocopy signal is detected at rank 1 on cosine and
    Pearson, top-5 on Spearman; PINK1's cosine p_empirical ≈ 0.001.

## Tests
- 22 unit tests across `test_pathway`, `test_io`, `test_phenocopy`. All
  passing; ruff check clean.
- Engineered-signal acceptance test: PINK1 must appear in the top-5
  candidates for PRKN on every metric. Honest gate; rank #1 is *too*
  perfect on synthetic data for rank-based methods.

## ADRs added or updated this week
- All six ADRs (0001–0006) status unchanged: Proposed. Implementation
  was built under the "just go" posture; flip to Accepted on user
  review.

## Blockers and questions for Armin
- See `QUESTIONS.md` — sections Q1.x through Q6.x plus two cross-cutting
  items. None block the next implementation slice.

## Plan for next week
- Wire the real DepMap 24Q2 download into `scripts/download_data.sh`
  with SHA256 verification.
- Implement the Reactome client (currently stub) for ADR-0005's primary
  pathway annotation source.
- Add the context-stratification module (`analysis/context.py`) and
  buffering detector (`analysis/buffering.py`).
- Build the NetworkX + PyVis graph render for top-k phenocopy hits.
- Write a notebook walkthrough running the full pipeline on PRKN.

## Burn rate
- Hours this week: ~5 (ADR sprint + first implementation slice)
- Hours to `v0.1.0`: ~8 more (real-data wiring + context + viz + demo)
