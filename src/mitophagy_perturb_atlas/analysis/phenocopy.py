"""Phenocopy detection: which perturbations look like a query?

Per ADRs 0001, 0004 and 0006: scores are reported for cosine, Pearson,
and Spearman simultaneously; significance is established by an empirical
null built from random gene-gene comparisons within the same matrix.

The pipeline:

1. Compute per-metric similarities of the query against every candidate
   (:func:`mitophagy_perturb_atlas.analysis.similarity.gene_query`).
2. Build an empirical null distribution per metric by sampling ``n_null``
   random gene-gene pairs from the same matrix.
3. For each candidate, compute an empirical p-value = fraction of null
   scores >= candidate score (one-sided, "is this candidate more
   similar than chance").
4. Apply Benjamini-Hochberg FDR within each metric.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import polars as pl
from numpy.random import PCG64, Generator
from numpy.typing import NDArray

from mitophagy_perturb_atlas.analysis.similarity import (
    _SIM_FUNCS,
    ALL_METRICS,
    Metric,
    gene_query,
)


@dataclass(frozen=True)
class PhenocopyParams:
    """Tuneable parameters for :func:`detect_phenocopy`."""

    n_null: int = 2000
    """Size of the empirical null per metric. ADR-0006 default."""

    seed: int = 0xC0DE
    """RNG seed for null sampling."""

    fdr_alpha: float = 0.05
    """BH-FDR alpha. Reported alongside raw p-values."""


def _bh_fdr(pvals: NDArray[np.float64]) -> NDArray[np.float64]:
    """Benjamini-Hochberg adjusted p-values (q-values)."""
    n = pvals.size
    if n == 0:
        return pvals.copy()
    order = np.argsort(pvals)
    ranks = np.arange(1, n + 1)
    sorted_p = pvals[order]
    adj = sorted_p * n / ranks
    # Enforce monotonicity (working from largest p downward).
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    adj = np.clip(adj, 0.0, 1.0)
    out = np.empty_like(adj)
    out[order] = adj
    return out


def _empirical_null(
    matrix: NDArray[np.float64], metric: Metric, n_null: int, rng: Generator
) -> NDArray[np.float64]:
    """Draw ``n_null`` random gene-gene scores from ``matrix`` for ``metric``."""
    n_rows = matrix.shape[0]
    if n_rows < 2:
        return np.array([], dtype=np.float64)
    sim_func = _SIM_FUNCS[metric]
    out = np.empty(n_null, dtype=np.float64)
    # Pre-pick the query rows once; for each call we compute the full row
    # similarity vector and pick a single random non-self partner. This is
    # ~10x faster than computing each pair fresh because we amortize the
    # rank-transform / centering inside ``sim_func``.
    query_indices = rng.integers(0, n_rows, size=n_null)
    for i, q_idx in enumerate(query_indices):
        sims = sim_func(matrix, int(q_idx))
        # Sample one partner != q_idx
        partner = int(rng.integers(0, n_rows))
        while partner == q_idx:
            partner = int(rng.integers(0, n_rows))
        out[i] = sims[partner]
    return out


def detect_phenocopy(
    matrix: NDArray[np.float64],
    row_labels: list[str],
    *,
    query: str,
    metrics: tuple[Metric, ...] = ALL_METRICS,
    params: PhenocopyParams | None = None,
) -> pl.DataFrame:
    """Rank candidates and attach empirical p + BH-q per metric.

    Returns a long-format DataFrame:
    ``(metric, query, candidate, score, rank, p_empirical, q_bh, sig)``
    where ``sig`` is ``True`` iff ``q_bh <= params.fdr_alpha``.
    """
    if params is None:
        params = PhenocopyParams()
    rng = Generator(PCG64(params.seed))
    base = gene_query(matrix, row_labels, query=query, metrics=metrics, drop_self=True)

    per_metric_frames: list[pl.DataFrame] = []
    for metric in metrics:
        null = _empirical_null(matrix, metric, params.n_null, rng)
        subset = base.filter(pl.col("metric") == metric)
        scores = subset.get_column("score").to_numpy().astype(np.float64)
        if null.size == 0:
            p_emp = np.full(scores.shape, np.nan)
        else:
            # one-sided p: fraction of null >= observed.
            sorted_null = np.sort(null)
            tail = sorted_null.size - np.searchsorted(sorted_null, scores, side="left")
            p_emp = (tail + 1) / (sorted_null.size + 1)  # add-one smoothing
        q_bh = _bh_fdr(np.asarray(p_emp, dtype=np.float64))
        sig = q_bh <= params.fdr_alpha
        per_metric_frames.append(
            subset.with_columns(
                pl.Series(name="p_empirical", values=p_emp),
                pl.Series(name="q_bh", values=q_bh),
                pl.Series(name="sig", values=sig),
            )
        )
    return pl.concat(per_metric_frames)


__all__ = ["PhenocopyParams", "detect_phenocopy"]
