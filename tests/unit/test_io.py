"""Tests for the DepMap + Replogle loaders (synthetic-fixture path only)."""

from __future__ import annotations

import numpy as np
import pytest

from mitophagy_perturb_atlas.io.depmap import (
    DEPMAP_PINNED_RELEASE,
    make_synthetic_depmap,
    pivot_to_gene_matrix,
)
from mitophagy_perturb_atlas.io.replogle2022 import (
    REPLOGLE_CELL_LINES,
    make_synthetic_perturbseq,
    pivot_to_perturbation_matrix,
)


class TestDepMap:
    def test_pinned_release(self) -> None:
        assert DEPMAP_PINNED_RELEASE == "24Q2"

    def test_synthetic_shape(self) -> None:
        frame, meta = make_synthetic_depmap(n_cell_lines=8)
        assert meta.n_cell_lines == 8
        assert frame.height == 8 * meta.n_genes

    def test_synthetic_deterministic(self) -> None:
        a, _ = make_synthetic_depmap(seed=123)
        b, _ = make_synthetic_depmap(seed=123)
        assert a.equals(b)

    def test_pivot_round_trip(self) -> None:
        frame, _ = make_synthetic_depmap(n_cell_lines=6)
        matrix, cells, genes = pivot_to_gene_matrix(frame)
        assert matrix.shape == (len(cells), len(genes))
        assert "PRKN" in genes
        assert "PINK1" in genes


class TestReplogle:
    def test_cell_lines(self) -> None:
        assert set(REPLOGLE_CELL_LINES) == {"K562", "RPE1"}

    def test_synthetic_shape(self) -> None:
        frame, meta = make_synthetic_perturbseq(n_features=24)
        assert meta.cell_line == "K562"
        assert frame.height == meta.n_perturbations * meta.n_features

    def test_synthetic_deterministic(self) -> None:
        a, _ = make_synthetic_perturbseq(seed=7)
        b, _ = make_synthetic_perturbseq(seed=7)
        assert a.equals(b)

    def test_invalid_cell_line_raises(self) -> None:
        with pytest.raises(ValueError, match="unknown cell line"):
            make_synthetic_perturbseq()  # default OK
            # Trigger via load with bad cell line:
            from mitophagy_perturb_atlas.io.replogle2022 import (
                load_replogle_pseudobulk,
            )

            load_replogle_pseudobulk("/tmp/nonexistent.tsv", cell_line="HELA")

    def test_pivot(self) -> None:
        frame, _ = make_synthetic_perturbseq(n_features=24)
        matrix, perts, feats = pivot_to_perturbation_matrix(frame)
        assert matrix.shape == (len(perts), len(feats))
        assert "PRKN" in perts and "PINK1" in perts
        # No NaN — every (pert, feat) cell present.
        assert not np.isnan(matrix).any()
