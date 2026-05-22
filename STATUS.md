# Status — week of 2026-05-19
Repo: mitophagy-perturb-atlas
Phase: Reasoning — ADR sprint complete, awaiting Armin sign-off

## Completed this week
- **ADR sprint complete** for the §5.4 reasoning checkpoints. Six ADRs
  in `docs/decisions/`, all in **Proposed — awaiting Armin sign-off**:
  - ADR-0001 — Separate similarity spaces (DepMap and Perturb-Seq).
  - ADR-0002 — DepMap release pinning (proposed 24Q2).
  - ADR-0003 — Replogle subset choice (proposed K562 + RPE1 both).
  - ADR-0004 — Similarity metric (proposed cosine, with Pearson and
    Spearman alongside).
  - ADR-0005 — Pathway-definition scope (proposed Reactome primary
    with KEGG/GO cross-checks).
  - ADR-0006 — Phenocopy FDR methodology (proposed empirical null,
    per modality, n=10,000).
- Decision-log index with dependency graph and reader-by-role guidance.
- QUESTIONS.md reorganized as a Saturday-morning review queue.

## Blockers and questions for Armin
- See `QUESTIONS.md` — sections Q1.x through Q6.x plus two cross-
  cutting items (network display cap, README example). All ADRs are
  Proposed pending sign-off.

## Plan for next week (post-sign-off)
- Implement DepMap loader against pinned 24Q2 release (real download
  with SHA256 verification, cache under `$XDG_CACHE_HOME/`).
- Implement Replogle K562 + RPE1 loaders.
- Implement the cosine + Pearson + Spearman similarity stack with the
  empirical-null FDR machinery.
- First end-to-end run on PRKN as the canonical query gene.

## Burn rate
- Hours this session: ~2 (ADR sprint only)
- Hours to `v0.1.0`: estimated 12-15 once ADRs are signed off
  (DepMap + Replogle loaders + similarity + FDR + demo notebook on
  PRKN-as-query).
