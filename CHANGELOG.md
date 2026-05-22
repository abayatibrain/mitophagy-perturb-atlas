# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
