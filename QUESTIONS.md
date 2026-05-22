# Open questions for Armin — mitophagy-perturb-atlas

This file is **append-only with respect to Armin's responses**. Cowork
never edits Armin's responses. New questions go at the bottom under the
next-empty heading.

When Armin replies inline, prefix with a timestamp:
`> Armin (2026-05-24): ...`

The default protocol when a question is open: Cowork **does not** make
the decision unilaterally. See §1.3 of the brief for the authority
matrix.

---

## How to use this file
The repository now has six ADRs in `docs/decisions/`. Each ADR carries
its own "Open questions for Armin" section. This file is the rolled-up
review queue — every ADR question that needs sign-off appears here in
the same order as the ADRs. The intended workflow is one Saturday-
morning pass through this file with replies inline.

ADRs with no remaining open questions after your replies move from
**Proposed** to **Accepted**.

---

## ADR-0001 — Separate similarity spaces

**Q1.1** — Confirm Option A (separate DepMap and Replogle spaces, with
side-by-side display) or override to a joint embedding.

> Armin: <reply>

**Q1.2** — Confirm DepMap release pinning at 24Q2 (covered in detail
under ADR-0002 below).

> Armin: <reply>

---

## ADR-0002 — DepMap release pinning

**Q2.1** — Confirm pin at DepMap 24Q2, or specify a different release.

> Armin: <reply>

**Q2.2** — Should the release version appear in every result figure
caption as well as the README, or only in the dossier footnote?

> Armin: <reply>

---

## ADR-0003 — Replogle subset choice

**Q3.1** — Confirm Option C (K562 + RPE1 both, in parallel columns),
or restrict to a single subset for v1.0.0.

> Armin: <reply>

**Q3.2** — Convergence-badge threshold: should "convergent across
modalities" require all three (DepMap + K562 + RPE1), or two of three?

> Armin: <reply>

---

## ADR-0004 — Similarity metric

**Q4.1** — Confirm cosine as the headline metric.

> Armin: <reply>

**Q4.2** — Confirm Pearson side-by-side + Spearman robustness check
(both reported alongside) is in scope for v1.0.0.

> Armin: <reply>

**Q4.3** — Confirm MI is acceptably deferred. What would trigger
adding it later?

> Armin: <reply>

---

## ADR-0005 — Pathway scope

**Q5.1** — Confirm Reactome primary + KEGG/GO cross-checks (Option C).

> Armin: <reply>

**Q5.2** — Confirm receptor-mediated mitophagy (BNIP3 / BNIP3L /
FUNDC1) is in scope via the broad R-HSA-5205685 membership.

> Armin: <reply>

**Q5.3** — KEGG attribution requirement is fine?

> Armin: <reply>

---

## ADR-0006 — Phenocopy FDR

**Q6.1** — Confirm Option A (empirical null by random gene pairing,
per modality, n = 10,000).

> Armin: <reply>

**Q6.2** — Confirm the FDR cutoff (0.05) and top-N cutoff (100).

> Armin: <reply>

**Q6.3** — Should "convergent across modalities" require significance
in DepMap **and both** Replogle subsets, or DepMap **and any** Replogle
subset?

> Armin: <reply>

---

## Cross-cutting (not tied to a single ADR)

**Q-X1** — **README defensibility.** Should the README's main results
paragraph lead with a specific PRKN example (e.g., "Top phenocopies of
PRKN are PINK1, OPTN, USP30 with anti-correlation") or stay generic?
The former is more compelling but commits us to one example holding up
across release bumps.

> Armin: <reply (or "Cowork's call")>

**Q-X2** — **Network display cap** (from the original scaffold's Q5).
Top-N neighbors to display in the interactive HTML network: 25, 50, or
100? Default proposal 50 with a CSV of the full results adjacent.

> Armin: <reply (or "Cowork's call")>
