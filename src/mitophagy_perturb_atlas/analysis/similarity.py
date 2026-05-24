"""Three-similarity gene-gene comparison per ADR-0004.

ADR-0004 commits to reporting all three of cosine, Pearson, and Spearman
similarity for every query — they catch different kinds of phenocopy
structure and the difference between them is itself diagnostic
(e.g. two genes with strong cosine but weak Pearson are aligned in
direction but differ in dynamic range).

This module exposes a single :func:`gene_query` entry point that takes
a matrix and a query-gene index and returns a long-format DataFrame
with one row per (similarity-metric, candidate) pair.

The implementation is intentionally vectorised at the matrix level so
the same code runs against the CRISPR-fitness matrix (cell-line space)
and the Perturb-Seq matrix (feature space) without modification.
"""

from __future__ import annotations

from typing import Final, Literal

import numpy as np
import polars as pl
from numpy.typing import NDArray
from scipy.stats import rankdata

Metric = Literal["cosine", "pearson", "spearman"]

ALL_METRICS: Final[tuple[Metric, ...]] = ("cosine", "pearson", "spearman")


def _cosine_similarity_row(matrix: NDArray[np.float64], row_idx: int) -> NDArray[np.float64]:
    """Cosine similarity of one row against every row."""
    query = matrix[row_idx]
    q_norm = float(np.linalg.norm(query))
    if q_norm == 0:
        return np.zeros(matrix.shape[0], dtype=np.float64)
    row_norms = np.linalg.norm(matrix, axis=1)
    safe = np.where(row_norms == 0, 1.0, row_norms)
    sims = (matrix @ query) / (safe * q_norm)
    sims[row_norms == 0] = 0.0
    return sims


def _pearson_similarity_row(matrix: NDArray[np.float64], row_idx: int) -> NDArray[np.float64]:
    """Pearson correlation of one row against every row."""
    centered = matrix - matrix.mean(axis=1, keepdims=True)
    sd = centered.std(axis=1, ddof=0)
    safe = np.where(sd == 0, 1.0, sd)
    standardized = centered / safe[:, None]
    standardized[sd == 0] = 0.0
    return _cosine_similarity_row(standardized, row_idx)


def _spearman_similarity_row(matrix: NDArray[np.float64], row_idx: int) -> NDArray[np.float64]:
    """Spearman correlation of one row against every row.

    Implementation: rank-transform every row, then Pearson.
    """
    ranks = np.apply_along_axis(lambda r: rankdata(r), axis=1, arr=matrix)
    return _pearson_similarity_row(ranks, row_idx)


_SIM_FUNCS = {
    "cosine": _cosine_similarity_row,
    "pearson": _pearson_similarity_row,
    "spearman": _spearman_similarity_row,
}


def gene_query(
    matrix: NDArray[np.float64],
    row_labels: list[str],
    *,
    query: str,
    metrics: tuple[Metric, ...] = ALL_METRICS,
    drop_self: bool = True,
) -> pl.DataFrame:
    """Rank every row in ``matrix`` against the query row.

    Parameters
    ----------
    matrix
        2-D float matrix; rows are genes, columns are features (the
        feature axis can be cell lines or readout genes).
    row_labels
        Length-``n_rows`` list of gene symbols aligned to ``matrix``.
    query
        The query gene symbol. Must appear in ``row_labels``.
    metrics
        Subset of ``("cosine", "pearson", "spearman")``.
    drop_self
        If True, the query row itself is omitted from the result.

    Returns
    -------
    Polars DataFrame with columns ``("metric", "query", "candidate",
    "score", "rank")``. Sorted by ``(metric, rank)``.
    """
    if query not in row_labels:
        raise KeyError(f"query gene {query!r} not in row_labels")
    if matrix.ndim != 2:
        raise ValueError(f"matrix must be 2-D; got shape {matrix.shape}")
    if len(row_labels) != matrix.shape[0]:
        raise ValueError(f"row_labels length {len(row_labels)} != matrix rows {matrix.shape[0]}")

    q_idx = row_labels.index(query)
    rows: list[dict[str, object]] = []
    for metric in metrics:
        sims = _SIM_FUNCS[metric](matrix, q_idx)
        order = np.argsort(-sims)  # descending
        rank = 0
        for j in order:
            if drop_self and j == q_idx:
                continue
            rank += 1
            rows.append(
                {
                    "metric": metric,
                    "query": query,
                    "candidate": row_labels[j],
                    "score": float(sims[j]),
                    "rank": rank,
                }
            )
    return pl.DataFrame(rows)


__all__ = ["ALL_METRICS", "Metric", "gene_query"]
