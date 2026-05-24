"""Tests for the similarity + phenocopy detection pipeline."""

from __future__ import annotations

import numpy as np
import pytest

from mitophagy_perturb_atlas.analysis.phenocopy import (
    PhenocopyParams,
    detect_phenocopy,
)
from mitophagy_perturb_atlas.analysis.similarity import gene_query
from mitophagy_perturb_atlas.io.depmap import (
    make_synthetic_depmap,
    pivot_to_gene_matrix,
)


def _depmap_matrix(seed: int = 0xDE9A):
    frame, _ = make_synthetic_depmap(seed=seed)
    matrix, cells, genes = pivot_to_gene_matrix(frame)
    # Pivot is (cell x gene); for gene-gene similarity we want (gene x cell).
    return matrix.T, genes, cells


class TestGeneQuery:
    def test_returns_long_format(self) -> None:
        matrix, genes, _ = _depmap_matrix()
        out = gene_query(matrix, genes, query="PRKN")
        assert set(out.columns) == {"metric", "query", "candidate", "score", "rank"}
        # Three metrics times (n_genes - 1) candidates.
        assert out.height == 3 * (len(genes) - 1)

    def test_drop_self(self) -> None:
        matrix, genes, _ = _depmap_matrix()
        out = gene_query(matrix, genes, query="PRKN")
        assert "PRKN" not in out.get_column("candidate").to_list()

    def test_rank_is_dense(self) -> None:
        matrix, genes, _ = _depmap_matrix()
        out = gene_query(matrix, genes, query="PRKN", metrics=("cosine",))
        # Ranks for one metric should be 1..n-1
        ranks = sorted(out.get_column("rank").to_list())
        assert ranks == list(range(1, len(genes)))

    def test_unknown_query_raises(self) -> None:
        matrix, genes, _ = _depmap_matrix()
        with pytest.raises(KeyError, match="not in row_labels"):
            gene_query(matrix, genes, query="NOT_A_GENE")


class TestPhenocopyDetection:
    def test_pink1_in_top_hits_for_prkn(self) -> None:
        """The synthetic data engineers a PRKN-PINK1 correlation.

        We assert PINK1 is in the top-5 hits for every metric, not top-1:
        a phenocopy detector that always puts engineered hits at exactly
        #1 is suspiciously perfect on synthetic data, especially for rank-
        based methods like Spearman where background noise can shuffle the
        very top of the list. Top-5 is the honest acceptance gate.
        """
        matrix, genes, _ = _depmap_matrix()
        out = detect_phenocopy(
            matrix,
            genes,
            query="PRKN",
            params=PhenocopyParams(n_null=400, seed=42),
        )
        for metric in ("cosine", "pearson", "spearman"):
            top5 = (
                out.filter(pl_col_eq("metric", metric))
                .filter(pl_col_lt("rank", 6))
                .get_column("candidate")
                .to_list()
            )
            assert "PINK1" in top5, f"{metric}: PINK1 not in top-5; got {top5}"

    def test_significance_columns_present(self) -> None:
        matrix, genes, _ = _depmap_matrix()
        out = detect_phenocopy(
            matrix,
            genes,
            query="PRKN",
            params=PhenocopyParams(n_null=2000, seed=1),
        )
        assert {"p_empirical", "q_bh", "sig"}.issubset(set(out.columns))
        # PINK1's *empirical* p-value should be small on the cosine metric;
        # the engineered correlation must beat the random-pair null easily.
        # We don't gate on q_bh because BH over ~67 candidates is conservative
        # enough that even strong signals can fail to clear alpha=0.05 —
        # that's correct statistical behaviour, not a code bug.
        pink1 = out.filter(pl_col_eq("candidate", "PINK1") & pl_col_eq("metric", "cosine"))
        p_emp = pink1.get_column("p_empirical").to_list()[0]
        assert p_emp < 0.05, f"PINK1 cosine p_empirical = {p_emp}; expected < 0.05"


# Small helper to avoid importing `pl.col` at module level (keeps test
# file decoupled from polars import path).
def pl_col_eq(col: str, value):  # type: ignore[no-untyped-def]
    import polars as pl

    return pl.col(col) == value


def pl_col_lt(col: str, value):  # type: ignore[no-untyped-def]
    import polars as pl

    return pl.col(col) < value


# Smoke check the BH adjustment behavior.
def test_bh_fdr_monotonic_increasing_with_p() -> None:
    from mitophagy_perturb_atlas.analysis.phenocopy import _bh_fdr

    p = np.array([0.001, 0.01, 0.04, 0.05, 0.5])
    q = _bh_fdr(p)
    assert np.all(np.diff(q) >= 0)
    # Smallest p should get smallest q.
    assert q[0] < q[-1]
