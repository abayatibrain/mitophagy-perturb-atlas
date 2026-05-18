# Open questions for Armin — mitophagy-perturb-atlas

This file is **append-only**. Cowork never edits Armin's responses. Use
timestamps. New questions go at the bottom under the next-empty heading.

The default protocol when a question is open: Cowork **does not** make the
decision unilaterally. See §1.3 of the brief for the authority matrix.

---

## Q1 — Cross-platform integration strategy (ADR-0001) — *decision required*

ADR-0001 proposes side-by-side similarity tables rather than a joint
embedding. Confirm or override.

> Armin: <reply>

## Q2 — DepMap release to pin (§5.4 item 1) — *decision required*

Proposal: 24Q2. Frozen for reproducibility. Confirm or specify a different
release.

> Armin: <reply>

## Q3 — Replogle subsets (§5.4 item 2) — *decision required*

Use K562 only, RPE1 only, or both? Both gives more signal but doubles
interpretation surface. Recommendation: both, displayed as separate
columns.

> Armin: <reply>

## Q4 — Pathway scope (§5.4 item 5) — *decision required*

Default: Reactome R-HSA-5205647 (canonical PINK1/Parkin). Union with
BNIP3/BNIP3L/FUNDC1 receptor-mediated mitophagy as a separate view.
Add KEGG or GO union, or keep Reactome-only?

> Armin: <reply>

## Q5 — Network display cap — *Cowork can decide if Armin defers*

Top-N neighbors to display in the interactive HTML network: 25, 50, or
100? Default proposal 50 with a CSV of the full results adjacent.

> Armin: <reply (or "Cowork's call")>
